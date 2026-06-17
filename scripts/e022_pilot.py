"""
e022_pilot.py — GATED PILOT for the Path-A Moussa demonstration (E022).

THE ONE QUESTION: does brain-tuning reproduce a downstream gain
(>= +2 phoneme-F1 over an un-tuned pretrained baseline) on our data at all?

TWO arms only (no SSL twin):
  pretrained  — facebook/wav2vec2-base, NO brain-tuning (reference)
  brain       — same wav2vec2-base + LoRA + linear head, L2 fMRI loss,
                single-subject UTS03, >=3 seeds.

CONFOUND FIX: BOTH arms start from facebook/wav2vec2-base (the pretrain
checkpoint), NOT wav2vec2-base-960h (the ASR fine-tune). This removes the
ASR head-start the original harness baked into the brain arm.

EVAL: phoneme-F1 (primary) + sentence-type-F1 (secondary) on TIMIT,
per seed, for pretrained vs brain-tuned. Contrast brain-pretrained with a
paired CI over seeds. TIMIT is acquired from the kylelovesllms/timit_asr
parquet mirror (full corpus, ungated) and decoded with soundfile, bypassing
the cortex/nltk import wall in the brain-tuning eval scripts.

Probing follows brain-tuning/src/eval_phonemes.py + eval_sentt.py: hidden
states at layers [2,5,7,8,10,11,12], mean-pooled over time, linear probe,
micro-F1. Phoneme task is multi-label (which 39-phone classes appear in the
utterance); sentence-type is 3-way (SA/SI/SX).
"""
import os, sys, io, json, time, argparse, pickle, warnings
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

warnings.simplefilter("ignore")
os.environ.setdefault("HF_HOME", "/home/centcom/data/hf-cache")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MULTI_SRC = os.path.join(REPO_ROOT, "data/paper-repos/multi-brain-tuning/src")
sys.path.insert(0, MULTI_SRC)
import joblib, importlib
import unittest.mock as mock

from transformers import Wav2Vec2Model, Wav2Vec2Processor, Wav2Vec2FeatureExtractor
from peft import LoraConfig, get_peft_model

# ----------------------------------------------------------------------------
# Config — matched budget, LoRA, single subject (as the harness)
# ----------------------------------------------------------------------------
PRETRAIN_CKPT = "facebook/wav2vec2-base"   # CONFOUND FIX: both arms start here
LORA_RANK, LORA_ALPHA, LORA_DROPOUT = 8, 32, 0.1
BASE_LR, LINEAR_LR = 1e-4, 1e-4
BATCH_SIZE = 64
SUBJECT = 3                  # UTS03 — has all 84 stories
OUT_DIM = 95556              # voxel count, single subject (harness OUT_DIM)
WAV_PARAMS = {"sampling_rate": 16000, "chunksz_sec": 1, "contextsz_sec": 0}

STIM_DIR   = os.path.join(REPO_ROOT, "data/processed_stim_data_dp")
FMRI_DIR   = os.path.join(REPO_ROOT, "data/lebel_ds003020/preprocessed_data")
STORY_DATA = os.path.join(REPO_ROOT, "data/story_data")
OUT_DIR    = os.path.join(REPO_ROOT, "outputs/e022")
os.makedirs(OUT_DIR, exist_ok=True)

TEST_STORY, VAL_STORY = "wheretheressmoke", "itsabox"
PROBE_LAYERS = [2, 5, 7, 8, 10, 11, 12]

# TIMIT 61 -> 39 phone map (Lee & Hon 1989), from brain-tuning/src/data_utils.py
PHON61_MAP39 = {
    'iy':'iy','ih':'ih','eh':'eh','ae':'ae','ix':'ih','ax':'ah','ah':'ah','uw':'uw',
    'ux':'uw','uh':'uh','ao':'aa','aa':'aa','ey':'ey','ay':'ay','oy':'oy','aw':'aw',
    'ow':'ow','l':'l','el':'l','r':'r','y':'y','w':'w','er':'er','axr':'er',
    'm':'m','em':'m','n':'n','nx':'n','en':'n','ng':'ng','eng':'ng','ch':'ch',
    'jh':'jh','dh':'dh','b':'b','d':'d','dx':'dx','g':'g','p':'p','t':'t',
    'k':'k','z':'z','zh':'sh','v':'v','f':'f','th':'th','s':'s','sh':'sh',
    'hh':'hh','hv':'hh','pcl':'h#','tcl':'h#','kcl':'h#','qcl':'h#','bcl':'h#','dcl':'h#',
    'gcl':'h#','h#':'h#','#h':'h#','pau':'h#','epi':'h#','ax-h':'ah','q':'h#'
}


def set_seed(seed):
    np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ----------------------------------------------------------------------------
# Backbone builder — wav2vec2-base + LoRA (brain arm) or plain (pretrained)
# ----------------------------------------------------------------------------
def build_backbone(with_lora: bool):
    wav2vec = Wav2Vec2Model.from_pretrained(PRETRAIN_CKPT)
    wav2vec.freeze_feature_encoder()
    if with_lora:
        cfg = LoraConfig(
            r=LORA_RANK, lora_alpha=LORA_ALPHA,
            target_modules=["attention.q_proj", "attention.k_proj",
                            "attention.v_proj", "attention.out_proj"],
            lora_dropout=LORA_DROPOUT, bias="none",
        )
        wav2vec = get_peft_model(wav2vec, cfg)
    return wav2vec


class BrainArm(nn.Module):
    """wav2vec2-base + LoRA backbone + linear head onto fMRI voxels."""
    def __init__(self, out_dim=OUT_DIM):
        super().__init__()
        self.lora_model = build_backbone(with_lora=True)
        self.processor = Wav2Vec2Processor.from_pretrained(
            PRETRAIN_CKPT, return_tensors="pt", return_attention_mask=True)
        self.linear = nn.Linear(768, out_dim)

    def encode(self, wav_batch):
        device = wav_batch.device
        B = wav_batch.shape[0]
        pv = self.processor(wav_batch.cpu().numpy().tolist(), return_tensors="pt",
                            sampling_rate=16000, padding=True
                            ).input_values.reshape(B, -1).to(device)
        return self.lora_model(pv).last_hidden_state.mean(dim=1)

    def forward(self, wav_batch):
        return self.linear(self.encode(wav_batch))


# ----------------------------------------------------------------------------
# Story dataset loading (reuse multi-brain-tuning dataset.py, patched paths)
# ----------------------------------------------------------------------------
def load_dataset_module():
    grids = joblib.load(os.path.join(STORY_DATA, "grids_huge.jbl"))
    trfiles = joblib.load(os.path.join(STORY_DATA, "trfiles_huge.jbl"))
    _orig = joblib.load
    def _patch(path, *a, **kw):
        if "grids_huge" in str(path): return grids
        if "trfiles_huge" in str(path): return trfiles
        return _orig(path, *a, **kw)
    with mock.patch("joblib.load", side_effect=_patch):
        import dataset as ds_mod
        importlib.reload(ds_mod)
    return ds_mod


def get_story_list(ds_mod):
    alls = sorted(ds_mod.wordseqs.keys())
    return [s for s in alls if s not in {TEST_STORY, VAL_STORY}]


def make_loader(ds_mod, story, bs=BATCH_SIZE):
    ds = ds_mod.FMRIStory(story_name=story, subject=SUBJECT,
                          read_stim_dir=STIM_DIR, read_fmri_dir=FMRI_DIR, **WAV_PARAMS)
    return DataLoader(ds, batch_size=bs, shuffle=False)


# ----------------------------------------------------------------------------
# BRAIN TRAINING — L2 fMRI loss, LoRA, matched budget
# ----------------------------------------------------------------------------
def train_brain(seed, num_epochs, max_stories, device):
    print(f"\n=== TRAIN brain  seed={seed}  epochs={num_epochs}  device={device} ===")
    set_seed(seed)
    ds_mod = load_dataset_module()
    stories = get_story_list(ds_mod)
    if max_stories:
        stories = stories[:max_stories]
    print(f"  training stories: {len(stories)}")

    model = BrainArm().to(device)
    lora_p = [p for p in model.lora_model.parameters() if p.requires_grad]
    lin_p = list(model.linear.parameters())
    n_train = sum(p.numel() for p in lora_p + lin_p)
    print(f"  trainable params: {n_train:,}")
    opt = optim.AdamW([{"params": lora_p, "lr": BASE_LR},
                       {"params": lin_p, "lr": LINEAR_LR}])

    t0 = time.time()
    for epoch in range(num_epochs):
        ep_losses = []
        for story in stories:
            loader = make_loader(ds_mod, story)
            loader.dataset.fetch_data()
            for wav, fmri in loader:
                opt.zero_grad()
                wav, fmri = wav.to(device), fmri.to(device)
                loss = nn.functional.mse_loss(model(wav), fmri)
                if not torch.isfinite(loss):
                    raise ValueError(f"non-finite loss seed={seed}")
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
                ep_losses.append(float(loss.item()))
            loader.dataset._clear()
        print(f"  epoch {epoch+1}/{num_epochs}  loss={np.mean(ep_losses):.5f}  "
              f"elapsed={time.time()-t0:.0f}s", flush=True)

    ckpt_dir = os.path.join(OUT_DIR, f"brain_seed{seed}")
    os.makedirs(ckpt_dir, exist_ok=True)
    # Merge LoRA into the base backbone so eval can use a plain Wav2Vec2Model
    merged = model.lora_model.merge_and_unload()
    torch.save(merged.state_dict(), os.path.join(ckpt_dir, "backbone_merged.pth"))
    print(f"  saved merged backbone -> {ckpt_dir}/backbone_merged.pth")
    return os.path.join(ckpt_dir, "backbone_merged.pth")


# ----------------------------------------------------------------------------
# TIMIT EVAL — build from parquet mirror, probe, micro-F1
# ----------------------------------------------------------------------------
import glob
import soundfile as sf
import pyarrow.parquet as pq
from sklearn.metrics import f1_score

PHONE_VOCAB = sorted(set(PHON61_MAP39.values()) - {"h#"})   # 39-class set minus silence
PHONE_IDX = {p: i for i, p in enumerate(PHONE_VOCAB)}
SENT_MAP = {"SA": 0, "SI": 1, "SX": 2}


def find_timit_parquet():
    base = os.environ["HF_HOME"]
    cands = glob.glob(base + "/**/datasets--kylelovesllms--timit_asr/**/*.parquet",
                      recursive=True)
    tr = [c for c in cands if "train" in c][0]
    te = [c for c in cands if "test" in c][0]
    return tr, te


def load_timit_split(parquet_path):
    """Return list of dicts: {wav(np.float32 16k), phones39(set of idx), sent(int)}."""
    t = pq.read_table(parquet_path).to_pylist()
    out = []
    for row in t:
        wav, sr = sf.read(io.BytesIO(row["audio"]["bytes"]), dtype="float32")
        if wav.ndim > 1:
            wav = wav.mean(axis=1)
        # 16k assumed (TIMIT native); confirm
        phones = set()
        for seg in row["phonetic_detail"]:
            p = PHON61_MAP39.get(seg["utterance"])
            if p is not None and p in PHONE_IDX:
                phones.add(PHONE_IDX[p])
        out.append({"wav": wav, "sr": sr,
                    "phones": phones, "sent": SENT_MAP[row["sentence_type"]]})
    return out


def make_eval_backbone(ckpt_path, device):
    """Plain Wav2Vec2Model; load merged brain backbone if ckpt given, else pretrained."""
    lm = Wav2Vec2Model.from_pretrained(PRETRAIN_CKPT)
    lm.freeze_feature_encoder()
    if ckpt_path:
        sd = torch.load(ckpt_path, map_location="cpu")
        missing, unexpected = lm.load_state_dict(sd, strict=False)
        # merged backbone should match exactly; report any drift
        if missing or unexpected:
            print(f"  [eval load] missing={len(missing)} unexpected={len(unexpected)}")
    lm.eval().to(device)
    return lm


def extract_features(samples, lm, processor, device):
    """Return {layer: (N, 768)} mean-pooled hidden states, plus label arrays."""
    feats = {ly: [] for ly in PROBE_LAYERS}
    y_phone = np.zeros((len(samples), len(PHONE_VOCAB)), dtype=np.int64)
    y_sent = np.zeros(len(samples), dtype=np.int64)
    for i, s in enumerate(samples):
        iv = processor(s["wav"], sampling_rate=16000,
                       return_tensors="pt").input_values.to(device)
        with torch.no_grad():
            out = lm(iv, output_hidden_states=True)
        for ly in PROBE_LAYERS:
            feats[ly].append(out.hidden_states[ly].mean(dim=1).squeeze(0).cpu().numpy())
        for idx in s["phones"]:
            y_phone[i, idx] = 1
        y_sent[i] = s["sent"]
    feats = {ly: np.stack(v) for ly, v in feats.items()}
    return feats, y_phone, y_sent


def probe_phoneme(Xtr, ytr, Xte, yte, device, num_epochs=50):
    """Multi-label linear probe; return best test micro-F1 over training."""
    model = nn.Linear(Xtr.shape[1], ytr.shape[1]).to(device)
    crit = nn.BCEWithLogitsLoss()
    opt = optim.Adam(model.parameters(), lr=1e-3)
    Xtr_t = torch.tensor(Xtr, dtype=torch.float32, device=device)
    ytr_t = torch.tensor(ytr, dtype=torch.float32, device=device)
    Xte_t = torch.tensor(Xte, dtype=torch.float32, device=device)
    best = 0.0
    for _ in range(num_epochs):
        model.train()
        opt.zero_grad()
        loss = crit(model(Xtr_t), ytr_t)
        loss.backward(); opt.step()
        model.eval()
        with torch.no_grad():
            pred = (torch.sigmoid(model(Xte_t)) >= 0.5).float().cpu().numpy()
        f1 = f1_score(yte, pred, average="micro", zero_division=0)
        best = max(best, f1)
    return best


def probe_sent(Xtr, ytr, Xte, yte, device, num_epochs=100):
    model = nn.Linear(Xtr.shape[1], 3).to(device)
    crit = nn.CrossEntropyLoss()
    opt = optim.Adam(model.parameters(), lr=1e-3)
    Xtr_t = torch.tensor(Xtr, dtype=torch.float32, device=device)
    ytr_t = torch.tensor(ytr, dtype=torch.long, device=device)
    Xte_t = torch.tensor(Xte, dtype=torch.float32, device=device)
    best = 0.0
    for _ in range(num_epochs):
        model.train(); opt.zero_grad()
        loss = crit(model(Xtr_t), ytr_t)
        loss.backward(); opt.step()
        model.eval()
        with torch.no_grad():
            pred = torch.argmax(model(Xte_t), dim=1).cpu().numpy()
        f1 = f1_score(yte, pred, average="micro", zero_division=0)
        best = max(best, f1)
    return best


def evaluate(ckpt_path, timit_tr, timit_te, device, tag):
    """Best-layer phoneme micro-F1 and sentence micro-F1 (scaled to F1*100)."""
    lm = make_eval_backbone(ckpt_path, device)
    processor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=16000,
                                         padding_value=0.0, do_normalize=True,
                                         return_attention_mask=True)
    print(f"  [{tag}] extracting train features (n={len(timit_tr)}) ...", flush=True)
    Ftr, yptr, ystr = extract_features(timit_tr, lm, processor, device)
    print(f"  [{tag}] extracting test features (n={len(timit_te)}) ...", flush=True)
    Fte, ypte, yste = extract_features(timit_te, lm, processor, device)
    del lm; torch.cuda.empty_cache()

    phone_by_layer, sent_by_layer = {}, {}
    for ly in PROBE_LAYERS:
        phone_by_layer[ly] = probe_phoneme(Ftr[ly], yptr, Fte[ly], ypte, device)
        sent_by_layer[ly] = probe_sent(Ftr[ly], ystr, Fte[ly], yste, device)
    best_phone = max(phone_by_layer.values()) * 100.0
    best_sent = max(sent_by_layer.values()) * 100.0
    print(f"  [{tag}] phoneme-F1={best_phone:.3f} (per-layer {[f'{v*100:.1f}' for v in phone_by_layer.values()]})")
    print(f"  [{tag}] sent-F1={best_sent:.3f} (per-layer {[f'{v*100:.1f}' for v in sent_by_layer.values()]})")
    return {"phoneme_f1": best_phone, "sent_f1": best_sent,
            "phone_by_layer": {k: v*100 for k, v in phone_by_layer.items()},
            "sent_by_layer": {k: v*100 for k, v in sent_by_layer.items()}}


# ----------------------------------------------------------------------------
# Orchestration
# ----------------------------------------------------------------------------
def paired_ci(diffs):
    """Paired mean diff + 95% CI via t-dist over seeds."""
    from scipy import stats
    d = np.asarray(diffs, dtype=float)
    n = len(d)
    mean = d.mean()
    if n < 2:
        return mean, (np.nan, np.nan)
    se = d.std(ddof=1) / np.sqrt(n)
    tcrit = stats.t.ppf(0.975, n - 1)
    return mean, (mean - tcrit * se, mean + tcrit * se)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[122, 123, 124])
    ap.add_argument("--num_epochs", type=int, default=15)
    ap.add_argument("--max_stories", type=int, default=0,
                    help="cap train stories (0 = all)")
    ap.add_argument("--device", type=str, default="cuda:0")
    ap.add_argument("--timing_probe", action="store_true")
    ap.add_argument("--mode", choices=["all", "train_one", "eval_all"], default="all")
    args = ap.parse_args()
    device = args.device if torch.cuda.is_available() else "cpu"

    if args.mode == "train_one":
        # Train a single seed and save its merged backbone, then exit.
        # (Used to parallelise seeds across GPUs.)
        seed = args.seeds[0]
        train_brain(seed, args.num_epochs, args.max_stories or None, device)
        return

    # --- TIMIT acquisition ---
    tr_pq, te_pq = find_timit_parquet()
    print(f"TIMIT parquet: train={os.path.basename(tr_pq)} test={os.path.basename(te_pq)}")
    print("Loading TIMIT (decoding audio via soundfile) ...", flush=True)
    timit_tr = load_timit_split(tr_pq)
    timit_te = load_timit_split(te_pq)
    srs = set(s["sr"] for s in timit_tr[:50])
    print(f"TIMIT loaded: train={len(timit_tr)} test={len(timit_te)} sample_rates={srs}")

    if args.timing_probe:
        t0 = time.time()
        train_brain(args.seeds[0], num_epochs=1, max_stories=2, device=device)
        print(f"TIMING: 1 epoch x 2 stories = {time.time()-t0:.0f}s")
        return

    results = {"config": {"pretrain_ckpt": PRETRAIN_CKPT, "seeds": args.seeds,
                          "num_epochs": args.num_epochs, "max_stories": args.max_stories,
                          "subject": SUBJECT, "out_dim": OUT_DIM,
                          "lora_rank": LORA_RANK, "probe_layers": PROBE_LAYERS},
               "seeds": {}}

    # --- pretrained baseline (seed-independent backbone, but eval probes are
    #     stochastic; eval once — it's the same un-tuned backbone for all seeds) ---
    print("\n##### PRETRAINED BASELINE (no brain-tuning) #####")
    pre = evaluate(None, timit_tr, timit_te, device, tag="pretrained")
    results["pretrained"] = pre

    diffs_phone, diffs_sent = [], []
    for seed in args.seeds:
        if args.mode == "eval_all":
            ckpt = os.path.join(OUT_DIR, f"brain_seed{seed}", "backbone_merged.pth")
            assert os.path.exists(ckpt), f"missing trained ckpt for seed {seed}: {ckpt}"
        else:
            ckpt = train_brain(seed, args.num_epochs, args.max_stories or None, device)
        print(f"\n##### BRAIN-TUNED EVAL  seed={seed} #####")
        bt = evaluate(ckpt, timit_tr, timit_te, device, tag=f"brain_seed{seed}")
        dp = bt["phoneme_f1"] - pre["phoneme_f1"]
        dsent = bt["sent_f1"] - pre["sent_f1"]
        diffs_phone.append(dp); diffs_sent.append(dsent)
        results["seeds"][seed] = {"brain": bt,
                                  "delta_phoneme": dp, "delta_sent": dsent}
        print(f"  seed {seed}: brain phoneme-F1={bt['phoneme_f1']:.3f}  "
              f"delta={dp:+.3f}  | brain sent-F1={bt['sent_f1']:.3f} delta={dsent:+.3f}")
        with open(os.path.join(OUT_DIR, "pilot_results.json"), "w") as f:
            json.dump(results, f, indent=2, default=float)

    # --- contrast + verdict ---
    mean_dp, ci_dp = paired_ci(diffs_phone)
    mean_ds, ci_ds = paired_ci(diffs_sent)
    reproduces = (mean_dp >= 2.0) and (ci_dp[0] > 0)
    verdict = "REPRODUCES (GO-to-full)" if reproduces else "NON-REPRODUCTION (STOP)"
    results["contrast"] = {
        "phoneme_delta_mean": mean_dp, "phoneme_delta_ci95": list(ci_dp),
        "sent_delta_mean": mean_ds, "sent_delta_ci95": list(ci_ds),
        "phoneme_deltas_per_seed": diffs_phone,
        "threshold": 2.0, "verdict": verdict}
    with open(os.path.join(OUT_DIR, "pilot_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=float)

    print("\n" + "=" * 60)
    print(f"PRETRAINED phoneme-F1 = {pre['phoneme_f1']:.3f}")
    print(f"BRAIN delta phoneme-F1 (mean over {len(args.seeds)} seeds) = "
          f"{mean_dp:+.3f}  95% CI [{ci_dp[0]:+.3f}, {ci_dp[1]:+.3f}]")
    print(f"sent-F1 delta = {mean_ds:+.3f}  95% CI [{ci_ds[0]:+.3f}, {ci_ds[1]:+.3f}]")
    print(f"VERDICT (threshold +2, CI excludes 0): {verdict}")
    print("=" * 60)


if __name__ == "__main__":
    main()
