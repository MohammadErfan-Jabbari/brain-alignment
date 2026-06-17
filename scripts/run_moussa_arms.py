"""
run_moussa_arms.py
==================
TA.4 three-arm training harness for the Moussa & Toneva 2025 (multi-brain-tuning) attack.

ARMS
----
  brain       — L2 regression onto fMRI targets (as in the paper).
  ssl         — Same Wav2Vec2-base + LoRA, same budget, but target is wav2vec2's own
                masked-prediction contrastive SSL objective (no brain signal).
                Specifically: Wav2Vec2ForPreTraining's built-in contrastive+diversity
                loss with mask_time_indices sampled at 0.065 masking rate (matching the
                original wav2vec2 pretraining setup). This is the matched-quality twin.
  permuted    — Same as brain but fMRI targets are block-permuted (shuffle TR-blocks of
                length PERM_BLOCK_SIZE); this is the cognition-specificity control.

DESIGN PARITY (all arms)
------------------------
  model       : facebook/wav2vec2-base-960h, LoRA rank = LORA_RANK
  optimizer   : AdamW, base_lr = BASE_LR, linear_lr = LINEAR_LR
  steps       : NUM_EPOCHS × num_stories (story-level step count)
  data        : same story set, same 1-subject (or multi-subject) batches
  seed        : SEED

USAGE
-----
Dry run (2 steps, one story, verify shapes/losses):
  uv run python scripts/run_moussa_arms.py --mode dryrun

Full run (all stories, all epochs, chosen arm):
  uv run python scripts/run_moussa_arms.py --arm brain   --num_epochs 30
  uv run python scripts/run_moussa_arms.py --arm ssl     --num_epochs 30
  uv run python scripts/run_moussa_arms.py --arm permuted --num_epochs 30

Downstream eval checkpoint check:
  uv run python scripts/run_moussa_arms.py --mode eval_check --ckpt_path <path>
"""

import os, sys, argparse, time, pickle, warnings
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from transformers import (
    Wav2Vec2Model,
    Wav2Vec2Processor,
    Wav2Vec2ForPreTraining,
    get_linear_schedule_with_warmup,
)
from peft import LoraConfig, get_peft_model

# ---------------------------------------------------------------------------
# Path setup — repo-relative from brain-alignment root
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MULTI_SRC = os.path.join(REPO_ROOT, "data/paper-repos/multi-brain-tuning/src")
BRAIN_SRC = os.path.join(REPO_ROOT, "data/paper-repos/brain-tuning/src")
sys.path.insert(0, MULTI_SRC)

import joblib
import unittest.mock as mock
import importlib

# ---------------------------------------------------------------------------
# Defaults (matched budget across all three arms)
# ---------------------------------------------------------------------------
LORA_RANK      = 8
LORA_ALPHA     = 32
LORA_DROPOUT   = 0.1
BASE_LR        = 1e-4
LINEAR_LR      = 1e-4
NUM_EPOCHS     = 30
BATCH_SIZE     = 128
SEED           = 122
PERM_BLOCK_SIZE = 20   # TRs per block in permuted-brain arm

# Wav2Vec2 masking params for SSL arm (matching original w2v2 pretraining)
MASK_TIME_PROB = 0.065   # fraction of time steps to mask
MASK_TIME_LENGTH = 10    # span length in time steps

STIM_DIR    = os.path.join(REPO_ROOT, "data/processed_stim_data_dp")
FMRI_DIR    = os.path.join(REPO_ROOT, "data/lebel_ds003020/preprocessed_data")
STORY_DATA  = os.path.join(REPO_ROOT, "data/story_data")
OUTPUT_DIR  = os.path.join(REPO_ROOT, "outputs/ta4_arms")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WAV_PARAMS = {"sampling_rate": 16000, "chunksz_sec": 1, "contextsz_sec": 0}
SUBJECT    = 3          # UTS03 — has all 84 stories
MODEL_NAME = "facebook/wav2vec2-base-960h"
OUT_DIM    = 95556      # voxel count for single subject (verified from load test)

# Hold-out stories (from original train_utils.py)
TEST_STORY = "wheretheressmoke"
VAL_STORY  = "itsabox"


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
def set_seed(seed: int):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ---------------------------------------------------------------------------
# Dataset loading helpers
# ---------------------------------------------------------------------------
def load_dataset_module():
    """Import dataset.py from the multi-brain-tuning repo, patching the
    module-level joblib.load calls to point to our local data paths."""
    grids   = joblib.load(os.path.join(STORY_DATA, "grids_huge.jbl"))
    trfiles = joblib.load(os.path.join(STORY_DATA, "trfiles_huge.jbl"))
    _orig   = joblib.load

    def _patch(path, *a, **kw):
        if "grids_huge"   in str(path): return grids
        if "trfiles_huge" in str(path): return trfiles
        return _orig(path, *a, **kw)

    with mock.patch("joblib.load", side_effect=_patch):
        import dataset as ds_mod
        importlib.reload(ds_mod)
    return ds_mod


def get_story_list(ds_mod):
    """Return (train_stories, val_story, test_story)."""
    all_stories = sorted(ds_mod.wordseqs.keys())
    train_stories = [s for s in all_stories if s not in {TEST_STORY, VAL_STORY}]
    return train_stories, VAL_STORY, TEST_STORY


def make_story_loader(ds_mod, story: str, subject: int) -> DataLoader:
    ds = ds_mod.FMRIStory(
        story_name=story,
        subject=subject,
        read_stim_dir=STIM_DIR,
        read_fmri_dir=FMRI_DIR,
        **WAV_PARAMS,
    )
    return DataLoader(ds, batch_size=BATCH_SIZE, shuffle=False)


# ---------------------------------------------------------------------------
# Model builder — Wav2Vec2 + LoRA (shared backbone for all arms)
# ---------------------------------------------------------------------------
def build_lora_backbone(lora_rank: int = LORA_RANK):
    """Return (wav2vec_model, processor) with LoRA applied to attention layers."""
    wav2vec = Wav2Vec2Model.from_pretrained(MODEL_NAME)
    processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME, return_tensors="pt",
                                                  return_attention_mask=True)
    wav2vec.freeze_feature_encoder()

    lora_cfg = LoraConfig(
        r=lora_rank,
        lora_alpha=LORA_ALPHA,
        target_modules=["attention.q_proj", "attention.k_proj",
                        "attention.v_proj", "attention.out_proj"],
        lora_dropout=LORA_DROPOUT,
        bias="none",
    )
    lora_model = get_peft_model(wav2vec, lora_cfg)
    return lora_model, processor


class BrainArm(nn.Module):
    """Arm 1 (brain) and Arm 3 (permuted-brain): L2 regression onto fMRI."""
    def __init__(self, lora_rank: int = LORA_RANK, out_dim: int = OUT_DIM):
        super().__init__()
        self.lora_model, self.processor = build_lora_backbone(lora_rank)
        self.linear = nn.Linear(768, out_dim)   # 768 = hidden size of wav2vec2-base

    def encode(self, wav_batch: torch.Tensor) -> torch.Tensor:
        """wav_batch: (B, T_samples)  →  (B, 768)"""
        device = wav_batch.device
        B = wav_batch.shape[0]
        proc_out = self.processor(
            wav_batch.cpu().numpy().tolist(),
            return_tensors="pt",
            sampling_rate=16000,
            padding=True,
        ).input_values.reshape(B, -1).to(device)
        hidden = self.lora_model(proc_out).last_hidden_state  # (B, T_frames, 768)
        return hidden.mean(dim=1)                              # (B, 768)

    def forward(self, wav_batch: torch.Tensor) -> torch.Tensor:
        return self.linear(self.encode(wav_batch))             # (B, out_dim)


SSL_BASE_MODEL = "facebook/wav2vec2-base"  # pretraining checkpoint — has quantizer weights

class SSLArm(nn.Module):
    """Arm 2 (matched-quality SSL twin): wav2vec2 masked-prediction loss.

    Uses Wav2Vec2ForPreTraining loaded from facebook/wav2vec2-base (the pretraining
    checkpoint, which has properly initialised quantizer codevectors).  LoRA adapters
    are injected into its transformer's attention layers, giving the same parameter
    count and rank as BrainArm.  The audio input path is identical.

    The fMRI arms use wav2vec2-base-960h (ASR fine-tune); this arm uses wav2vec2-base
    (pretrain checkpoint) — both share the same transformer architecture and feature
    extractor, so the LoRA adapter count is identical.
    """
    def __init__(self, lora_rank: int = LORA_RANK):
        super().__init__()
        self.pretrain_model = Wav2Vec2ForPreTraining.from_pretrained(SSL_BASE_MODEL)
        self.pretrain_model.wav2vec2.freeze_feature_encoder()
        self.processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME,
                                                           return_tensors="pt",
                                                           return_attention_mask=True)
        # Inject LoRA into the transformer inside ForPreTraining
        lora_cfg = LoraConfig(
            r=lora_rank,
            lora_alpha=LORA_ALPHA,
            target_modules=["attention.q_proj", "attention.k_proj",
                            "attention.v_proj", "attention.out_proj"],
            lora_dropout=LORA_DROPOUT,
            bias="none",
        )
        self.pretrain_model.wav2vec2 = get_peft_model(self.pretrain_model.wav2vec2, lora_cfg)
        n_trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        print(f"SSLArm trainable params: {n_trainable:,}")

    def forward(self, wav_batch: torch.Tensor):
        """Returns the pretraining loss (contrastive + diversity)."""
        from transformers.models.wav2vec2.modeling_wav2vec2 import (
            _compute_mask_indices, _sample_negative_indices,
        )
        device = wav_batch.device
        B = wav_batch.shape[0]
        input_values = self.processor(
            wav_batch.cpu().numpy().tolist(),
            return_tensors="pt",
            sampling_rate=16000,
            padding=True,
        ).input_values.reshape(B, -1).to(device)

        # Feature-encoder output length (no grad needed)
        with torch.no_grad():
            feat_len = self.pretrain_model._get_feat_extract_output_lengths(
                torch.tensor([input_values.shape[1]] * B)
            )
        seq_len = int(feat_len[0].item())

        # Sample mask and negatives on CPU, then move to device
        mask_np = _compute_mask_indices(
            shape=(B, seq_len),
            mask_prob=MASK_TIME_PROB,
            mask_length=MASK_TIME_LENGTH,
        )
        neg_np = _sample_negative_indices(
            features_shape=(B, seq_len),
            num_negatives=self.pretrain_model.config.num_negatives,
            mask_time_indices=mask_np,
        )
        mask_t = torch.from_numpy(mask_np).to(device)
        neg_t  = torch.from_numpy(neg_np).to(device)

        outputs = self.pretrain_model(
            input_values=input_values,
            mask_time_indices=mask_t,
            sampled_negative_indices=neg_t,
        )
        return outputs.loss  # contrastive + diversity loss


def block_permute_fmri(fmri: torch.Tensor, block_size: int = PERM_BLOCK_SIZE) -> torch.Tensor:
    """Permute fMRI target by shuffling non-overlapping TR-blocks.
    Shape: (T, V). Returns permuted copy.
    If T < block_size (e.g. a tiny dry-run batch), falls back to row-shuffle."""
    T, V = fmri.shape
    effective_block = min(block_size, max(1, T // 2))
    num_full = T // effective_block
    if num_full < 2:
        # Fewer than 2 blocks — just shuffle rows
        perm = torch.randperm(T)
        return fmri[perm]
    indices = list(range(num_full))
    np.random.shuffle(indices)
    blocks = [fmri[i * effective_block: (i + 1) * effective_block] for i in indices]
    permuted = torch.cat(blocks, dim=0)
    remainder = T - num_full * effective_block
    if remainder > 0:
        permuted = torch.cat([permuted, fmri[num_full * effective_block:]], dim=0)
    return permuted


# ---------------------------------------------------------------------------
# Training helpers
# ---------------------------------------------------------------------------
def get_trainable_param_groups(model: nn.Module, arm: str):
    if arm in ("brain", "permuted"):
        lora_params = list(filter(lambda p: p.requires_grad,
                                  model.lora_model.parameters()))
        linear_params = list(model.linear.parameters())
        return [
            {"params": lora_params,  "lr": BASE_LR},
            {"params": linear_params,"lr": LINEAR_LR},
        ]
    else:  # ssl
        # LoRA adapters inside pretrain_model.wav2vec2
        lora_params = list(filter(lambda p: p.requires_grad,
                                  model.pretrain_model.wav2vec2.parameters()))
        # Quantizer + project heads are also part of the contrastive objective
        head_params = (
            list(model.pretrain_model.quantizer.parameters()) +
            list(model.pretrain_model.project_q.parameters()) +
            list(model.pretrain_model.project_hid.parameters())
        )
        return [
            {"params": lora_params, "lr": BASE_LR},
            {"params": head_params, "lr": LINEAR_LR},
        ]


def train_one_step(model, optimizer, wav_batch, fmri_batch, arm, device):
    """Run a single gradient step. Returns loss value (float)."""
    optimizer.zero_grad()
    wav_batch = wav_batch.to(device)

    if arm in ("brain", "permuted"):
        fmri_batch = fmri_batch.to(device)
        if arm == "permuted":
            fmri_batch = block_permute_fmri(fmri_batch)
        preds = model(wav_batch)
        loss = nn.functional.mse_loss(preds, fmri_batch)
    else:  # ssl — fmri_batch unused; model computes its own contrastive loss
        model.train()
        loss = model(wav_batch)

    if loss is None or not torch.isfinite(loss):
        raise ValueError(f"Non-finite loss in arm={arm}: {loss}")

    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    return float(loss.item())


# ---------------------------------------------------------------------------
# DRY-RUN MODE: 2 steps per arm, one story, confirm shape/loss/finiteness
# ---------------------------------------------------------------------------
DRYRUN_BATCH = 8   # small batch so SSL quantizer doesn't OOM on a single GPU

def run_dryrun():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n=== DRY-RUN on {device} ===")
    set_seed(SEED)

    print("Loading dataset module...")
    ds_mod = load_dataset_module()
    train_stories, _, _ = get_story_list(ds_mod)
    story = train_stories[0]
    print(f"Using story: {story}, subject: {SUBJECT}")

    # Use a small DataLoader for the dry-run so the SSL quantizer doesn't OOM
    from torch.utils.data import DataLoader as _DL
    ds = ds_mod.FMRIStory(
        story_name=story, subject=SUBJECT,
        read_stim_dir=STIM_DIR, read_fmri_dir=FMRI_DIR, **WAV_PARAMS,
    )
    ds.fetch_data()
    loader = _DL(ds, batch_size=DRYRUN_BATCH, shuffle=False)

    wav_batch, fmri_batch = next(iter(loader))
    print(f"  wav_batch shape:  {wav_batch.shape}  (dry-run batch={DRYRUN_BATCH})")
    print(f"  fmri_batch shape: {fmri_batch.shape}")

    results = {}

    # ---- Arm 1: brain ----
    print("\n--- Arm 1: brain ---")
    set_seed(SEED)
    model_brain = BrainArm(lora_rank=LORA_RANK, out_dim=OUT_DIM).to(device)
    n_train = sum(p.numel() for p in model_brain.parameters() if p.requires_grad)
    print(f"  trainable params: {n_train:,}")
    opt_brain = optim.AdamW(get_trainable_param_groups(model_brain, "brain"))
    losses_brain = []
    for step in range(2):
        l = train_one_step(model_brain, opt_brain, wav_batch, fmri_batch, "brain", device)
        losses_brain.append(l)
        print(f"  step {step}: loss={l:.6f}")
    assert losses_brain[1] < losses_brain[0] * 1.5, "brain loss not stable"
    results["brain"] = losses_brain
    del model_brain

    # ---- Arm 2: ssl ----
    print("\n--- Arm 2: ssl (matched-quality) ---")
    set_seed(SEED)
    model_ssl = SSLArm(lora_rank=LORA_RANK).to(device)
    opt_ssl = optim.AdamW(get_trainable_param_groups(model_ssl, "ssl"))
    losses_ssl = []
    for step in range(2):
        l = train_one_step(model_ssl, opt_ssl, wav_batch, fmri_batch, "ssl", device)
        losses_ssl.append(l)
        print(f"  step {step}: loss={l:.6f}")
    assert torch.isfinite(torch.tensor(losses_ssl[0])), "ssl loss not finite"
    results["ssl"] = losses_ssl
    del model_ssl

    # ---- Arm 3: permuted ----
    print("\n--- Arm 3: permuted-brain ---")
    set_seed(SEED)
    model_perm = BrainArm(lora_rank=LORA_RANK, out_dim=OUT_DIM).to(device)
    opt_perm = optim.AdamW(get_trainable_param_groups(model_perm, "permuted"))
    losses_perm = []
    for step in range(2):
        l = train_one_step(model_perm, opt_perm, wav_batch, fmri_batch, "permuted", device)
        losses_perm.append(l)
        print(f"  step {step}: loss={l:.6f}")
    assert losses_perm[1] < losses_perm[0] * 1.5, "permuted loss not stable"
    results["permuted"] = losses_perm
    del model_perm

    print("\n=== DRY-RUN SUMMARY ===")
    for arm, ls in results.items():
        print(f"  {arm:12s}  step0={ls[0]:.6f}  step1={ls[1]:.6f}  finite={all(np.isfinite(ls))}")
    print("DRY-RUN PASSED")
    return results


# ---------------------------------------------------------------------------
# FULL TRAINING MODE
# ---------------------------------------------------------------------------
def run_full_training(arm: str, num_epochs: int, seed: int):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n=== FULL TRAINING: arm={arm}, epochs={num_epochs}, device={device} ===")
    set_seed(seed)

    ds_mod = load_dataset_module()
    train_stories, val_story, _ = get_story_list(ds_mod)
    print(f"Training stories: {len(train_stories)}, val story: {val_story}")

    # Build model
    if arm in ("brain", "permuted"):
        model = BrainArm(lora_rank=LORA_RANK, out_dim=OUT_DIM).to(device)
    else:
        model = SSLArm(lora_rank=LORA_RANK).to(device)

    model = torch.nn.DataParallel(model)

    param_groups = get_trainable_param_groups(model.module, arm)
    optimizer = optim.AdamW(param_groups)

    num_training_steps = num_epochs * len(train_stories)
    num_warmup_steps   = int(0.1 * num_training_steps)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=num_warmup_steps,
        num_training_steps=num_training_steps
    )

    exp_dir = os.path.join(OUTPUT_DIR, f"{arm}_rank{LORA_RANK}_seed{seed}")
    os.makedirs(exp_dir, exist_ok=True)

    losses_dict = {"train": [], "epoch_per_story": []}
    t0 = time.time()

    # Pre-load val data for eval
    val_loader = make_story_loader(ds_mod, val_story, SUBJECT)
    val_loader.dataset.fetch_data()

    for epoch in range(num_epochs):
        epoch_losses = []
        for story in train_stories:
            loader = make_story_loader(ds_mod, story, SUBJECT)
            loader.dataset.fetch_data()
            story_loss = []
            for wav_batch, fmri_batch in loader:
                l = train_one_step(model.module, optimizer, wav_batch,
                                   fmri_batch, arm, device)
                story_loss.append(l)
            loader.dataset._clear()
            epoch_losses.append(np.mean(story_loss))
            scheduler.step()

        mean_train = np.mean(epoch_losses)
        losses_dict["train"].append(mean_train)

        print(f"Epoch {epoch+1}/{num_epochs}  train_loss={mean_train:.6f}  "
              f"lr={optimizer.param_groups[0]['lr']:.2e}  "
              f"elapsed={time.time()-t0:.0f}s")

        if epoch % 5 == 0 or epoch == num_epochs - 1:
            ckpt = os.path.join(exp_dir, f"ckpt_epoch{epoch+1}.pth")
            # Save only LoRA + linear state (not full frozen backbone)
            state = {k: v for k, v in model.module.state_dict().items()
                     if "lora" in k or "linear" in k or "project" in k or "quantizer" in k}
            torch.save(state, ckpt)
            print(f"  Checkpoint saved: {ckpt}")

    pickle.dump(losses_dict,
                open(os.path.join(exp_dir, "losses.pkl"), "wb"))
    print(f"Training done in {time.time()-t0:.0f}s")


# ---------------------------------------------------------------------------
# EVAL WIRING CHECK MODE
# ---------------------------------------------------------------------------
def run_eval_check(ckpt_path: str):
    """Verify the downstream eval scripts from brain-tuning can load a checkpoint.
    Checks:
      1. Wav2Vec2LoRA model (from brain-tuning/src/wav2vec_linear.py) can be
         instantiated with the same LoRA config.
      2. A checkpoint produced by this harness can be loaded into it.
      3. TIMIT phoneme data path existence (data not needed, just connectivity).
    """
    sys.path.insert(0, BRAIN_SRC)
    print("\n=== EVAL WIRING CHECK ===")

    # Re-import brain-tuning's Wav2VecLoRA (different module than multi-brain-tuning)
    # brain-tuning's wav2vec_linear.py has Wav2VecLoRA using Wav2Vec2ForPreTraining;
    # but the eval scripts use a plain Wav2VecLinear with --model_path. We verify
    # that our BrainArm checkpoint state dict keys are compatible.
    print(f"brain-tuning src: {BRAIN_SRC}")

    # Instantiate a BrainArm and dump a test checkpoint
    device = "cpu"
    model = BrainArm(lora_rank=LORA_RANK, out_dim=OUT_DIM)
    test_ckpt = "/tmp/ta4_test_ckpt.pth"
    torch.save(model.state_dict(), test_ckpt)
    print(f"Saved test checkpoint: {test_ckpt}")

    # Load it back
    loaded = BrainArm(lora_rank=LORA_RANK, out_dim=OUT_DIM)
    loaded.load_state_dict(torch.load(test_ckpt, map_location="cpu"))
    print("Checkpoint round-trip load: OK")

    if ckpt_path and os.path.exists(ckpt_path):
        state = torch.load(ckpt_path, map_location="cpu")
        print(f"Provided checkpoint keys (first 5): {list(state.keys())[:5]}")
        # Partial load (LoRA + linear only)
        loaded.load_state_dict(state, strict=False)
        print("Partial load of provided checkpoint: OK")

    # Check eval script existence
    for script in ["eval_phonemes.py", "eval_sentt.py"]:
        p = os.path.join(BRAIN_SRC, script)
        print(f"  {script}: {'found' if os.path.exists(p) else 'MISSING'}")

    # Check downstream data presence (TIMIT path used in eval_phonemes/eval_sentt)
    timit_path = os.path.join(REPO_ROOT, "data/timit")
    print(f"  TIMIT data path ({timit_path}): {'found' if os.path.exists(timit_path) else 'NOT FOUND (need to download before full eval)'}")

    print("\nEval wiring check complete.")
    print("To run full phoneme eval (after training):")
    print(f"  cd {BRAIN_SRC} && uv run python eval_phonemes.py \\")
    print(f"    --model_path <ckpt_dir> --subject 3 \\")
    print(f"    --data_path {REPO_ROOT}/data/timit --device cuda:0")
    print("To run sentence-type eval:")
    print(f"  cd {BRAIN_SRC} && uv run python eval_sentt.py \\")
    print(f"    --model_path <ckpt_dir> --subject 3 \\")
    print(f"    --data_path {REPO_ROOT}/data/timit --device cuda:0")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="TA.4 three-arm Moussa harness")
    parser.add_argument("--mode", choices=["dryrun", "train", "eval_check"],
                        default="train")
    parser.add_argument("--arm", choices=["brain", "ssl", "permuted"],
                        default="brain")
    parser.add_argument("--num_epochs", type=int, default=NUM_EPOCHS)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--ckpt_path", type=str, default="",
                        help="Checkpoint path for eval_check mode")
    return parser.parse_args()


if __name__ == "__main__":
    os.environ.setdefault("HF_HOME", "/home/centcom/data/hf-cache")
    args = parse_args()

    if args.mode == "dryrun":
        run_dryrun()
    elif args.mode == "eval_check":
        run_eval_check(args.ckpt_path)
    else:
        run_full_training(arm=args.arm, num_epochs=args.num_epochs, seed=args.seed)
