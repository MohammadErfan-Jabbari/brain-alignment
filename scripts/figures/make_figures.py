"""Generate the thesis figures from RECORDED evidence (manuscript D011 rule).

Reads recorded experiment artifacts and renders selected manuscript figures to
outputs/figures/ (gitignored); selected renders are copied to docs/manuscript/figures/.

Run: uv run python scripts/figures/make_figures.py
"""
import json
import math
from pathlib import Path
from collections import defaultdict
from statistics import mean, median, stdev

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/figures"
OUT.mkdir(parents=True, exist_ok=True)
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306}


def fig1_dose_response():
    """Dose-response gap(k): NESTED (E010, clean-looking but confounded) vs RANDOM subsets
    (E010b, the honest, noisy reality). Shows why we don't claim a clean causal law."""
    dn = json.load(open(ROOT / "outputs/E010_averaging_doseresponse.json"))
    bks = defaultdict(dict)
    for r in dn["raw"]:
        bks[(r["k"], r["seed"])][r["arm"]] = r["unique_r2"]
    ksn = sorted({r["k"] for r in dn["raw"]})
    sn = sorted({r["seed"] for r in dn["raw"]})
    nested = [mean([bks[(k, s)]["mse"] - bks[(k, s)]["mse_perm"] for s in sn]) for k in ksn]

    db = json.load(open(ROOT / "outputs/E010b_random_subsets.json"))
    cell = defaultdict(dict)
    for r in db["raw"]:
        cell[(r["k"], r["subset"], r["seed"])][r["arm"]] = r["unique_r2"]
    ksr = sorted({r["k"] for r in db["raw"]})
    rm, re_ = [], []
    for k in ksr:
        gs = [cell[(kk, ss, sd)]["mse"] - cell[(kk, ss, sd)]["mse_perm"]
              for (kk, ss, sd) in cell if kk == k and "mse" in cell[(kk, ss, sd)] and "mse_perm" in cell[(kk, ss, sd)]]
        rm.append(mean(gs)); re_.append(stdev(gs) if len(gs) > 1 else 0)

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.axhline(0, color="grey", lw=0.8, ls=":")
    ax.plot(ksn, nested, marker="o", color="C7", ls="--", lw=1.5, alpha=0.7,
            label="nested subsets (E010) — clean-looking but confounded")
    ax.errorbar(ksr, rm, yerr=re_, marker="s", color="C3", capsize=4, lw=2,
                label="random subsets (E010b) ± SD — the honest, noisy reality")
    ax.set_xlabel("k  (subjects averaged into the fMRI target)")
    ax.set_ylabel("held-out brain-specific gap  Δ unique R²")
    ax.set_xticks(sorted(set(ksn) | set(ksr)))
    ax.set_title("Dose-response: the clean nested curve is a design artifact\n"
                 "(random subsets are non-monotone & noisy → no clean causal law)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_dose_response.png", dpi=150)
    plt.close(fig)
    print(f"fig1: nested={[round(g,4) for g in nested]} | random={[round(g,4) for g in rm]}")


def fig2_collapse():
    """E005 (averaged target) vs E008 (per-subject): the ~80x collapse. Recorded values."""
    # recorded: E005 averaged +0.0081 [+0.0023,+0.0171] (15-cell); E005 fold-level [−0.0030,+0.0193];
    # E008 per-subject +0.00010 [−0.00037,+0.00058] (n=9). MDE 0.0006.
    labels = ["E005\n5-subj-avg\n(15-cell CI)", "E005\n5-subj-avg\n(fold-level CI)", "E008\nper-subject\n(n=9)"]
    means = [0.0081, 0.0081, 0.00010]
    los = [0.0023, -0.0030, -0.00037]
    his = [0.0171, 0.0193, 0.00058]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(0, color="grey", lw=0.8, ls=":")
    xs = range(len(labels))
    for x, m, lo, hi in zip(xs, means, los, his):
        ax.errorbar([x], [m], yerr=[[m - lo], [hi - m]], marker="o", capsize=5, lw=2,
                    color=("C2" if lo > 0 else "C1"))
    ax.axhspan(-0.0006, 0.0006, color="grey", alpha=0.15, label="E008 MDE band (±0.0006)")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("brain-specific gap (mse − perm)  Δ unique R²")
    ax.set_title("The apparent in-domain F1 effect is an averaging artifact\n(+0.0081 averaged → +0.0001 per-subject; ~80×)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_collapse.png", dpi=150)
    plt.close(fig)
    print("fig2: collapse rendered")


def fig3_a2():
    """E006: trained vs untrained unique R² + gap (gpt2, Qwen)."""
    rows = []
    for tag, f in [("gpt2 L7", "outputs/E006_lebel_gpt2.json"), ("Qwen-0.5B L12", "outputs/E006_lebel_Qwen.json")]:
        d = json.load(open(ROOT / f))
        rows.append((tag, d["trained_unique_r2_mean"], d["untrained_unique_r2_mean"], d["gap_mean"]))
    fig, ax = plt.subplots(figsize=(6, 4))
    x = range(len(rows))
    w = 0.35
    ax.bar([i - w / 2 for i in x], [r[1] for r in rows], w, label="trained", color="C2")
    ax.bar([i + w / 2 for i in x], [r[2] for r in rows], w, label="untrained", color="C1")
    for i, r in enumerate(rows):
        ax.annotate(f"gap\n+{r[3]:.3f}", (i, max(r[1], 0) + 0.002), ha="center", fontsize=8, color="C3")
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels([r[0] for r in rows])
    ax.set_ylabel("voxelwise unique R²  (mean over NC-reliable voxels)")
    ax.set_title("E006: alignment is real & measurable (powered)\ntrained ≫ untrained after full nuisance, 11,442 voxels")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "fig3_a2.png", dpi=150)
    plt.close(fig)
    print(f"fig3: A2 gaps {[round(r[3],4) for r in rows]}")


def fig4_a3():
    """E009 powered: OOD-ratio per arm (lower = more robust)."""
    d = json.load(open(ROOT / "outputs/E009_a3_powered.json"))
    byarm = defaultdict(lambda: defaultdict(list))
    for r in d["raw"]:
        for k, v in r["ood_ratio"].items():
            byarm[r["arm"]][k].append(v)
    arms = ["lm_only", "mse_l10", "mse_perm_l10", "textfeat_l10"]
    arms = [a for a in arms if a in byarm]
    domains = list(d["raw"][0]["ood_ratio"].keys())
    fig, ax = plt.subplots(figsize=(6.5, 4))
    x = range(len(arms))
    w = 0.8 / len(domains)
    for j, dom in enumerate(domains):
        ms = [mean(byarm[a][dom]) for a in arms]
        es = [(stdev(byarm[a][dom]) / math.sqrt(len(byarm[a][dom]))) for a in arms]
        ax.bar([i + j * w for i in x], ms, w, yerr=es, capsize=2, label=f"OOD/{dom}")
    ax.set_xticks([i + w * (len(domains) - 1) / 2 for i in x])
    ax.set_xticklabels(["kd_ppl", "kd_brain", "kd_brain\nperm", "textfeat"], fontsize=8)
    ax.set_ylabel("OOD / in-domain perplexity ratio  (lower = more robust)")
    ax.set_title("E009: no brain-specific practical payoff\nkd_brain ≈ permuted ≈ textfeat ≈ kd_ppl (within MDE)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig4_a3.png", dpi=150)
    plt.close(fig)
    print("fig4: A3 nulls rendered")


def fig6_quality_alignment():
    """E015 corrected 22-model quality--alignment relationship."""
    d = json.load(open(ROOT / "outputs/E015_expand/E015_expand_merged.json"))
    models = d["models"]
    families = sorted({m["family"] for m in models})
    cmap = plt.get_cmap("tab10")
    fig, ax = plt.subplots(figsize=(6.5, 4.4))
    for i, family in enumerate(families):
        rows = [m for m in models if m["family"] == family]
        ax.scatter([m["bpb"] for m in rows], [m["unique_r2_mid"] for m in rows],
                   s=45, color=cmap(i), label=family, alpha=0.9)
    x = [m["bpb"] for m in models]
    y = [m["unique_r2_mid"] for m in models]
    slope = d["primary_bpb_mid"]["ols_slope"]
    intercept = mean(y) - slope * mean(x)
    xx = [min(x), max(x)]
    ax.plot(xx, [intercept + slope * q for q in xx], color="black", lw=1.5,
            label=f"all models: r={d['primary_bpb_mid']['pearson_r']:.2f}")
    ax.axvspan(1.13, 1.30, color="grey", alpha=0.10, label="capable/overlap range")
    ax.set_xlabel("language-model quality (bits per byte; lower is better)")
    ax.set_ylabel("raw unique $R^2$ at the prespecified middle layer")
    ax.set_title("Alignment and language-model quality across 22 models")
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(OUT / "fig06_quality_alignment.png", dpi=180)
    plt.close(fig)


def fig7_intervention_forest():
    """Recorded real-minus-control estimates, grouped by valid inference unit."""
    rows = [
        ("E004  averaged target", 0.00316, -0.00227, 0.00858, "5 stimulus folds"),
        ("E005  averaged target", 0.00810, -0.00300, 0.01930, "5 stimulus folds"),
        ("E008  participant target", 0.00010, -0.00037, 0.00058, "9 participants"),
        ("E011  high-capacity LoRA", 0.00043, -0.00050, 0.00130, "9 participants"),
        ("E013b contrastive ROI", -0.00019, -0.00080, 0.00050, "9 participants"),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ys = list(range(len(rows)))[::-1]
    colors = ["C0", "C0", "C2", "C2", "C2"]
    for yv, (label, est, lo, hi, unit), color in zip(ys, rows, colors):
        ax.errorbar(est, yv, xerr=[[est - lo], [hi - est]], fmt="o", color=color,
                    capsize=4, lw=1.8)
        ax.text(0.0198, yv, unit, va="center", ha="right", fontsize=8, color="dimgray")
    ax.axvline(0, color="black", lw=0.8, ls=":")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.set_xlim(-0.0045, 0.0205)
    ax.set_xlabel("real-target minus target-control $\Delta$ unique $R^2$ (95% interval)")
    ax.set_title("Comparable intervention contrasts do not establish a reliable lever")
    fig.tight_layout()
    fig.savefig(OUT / "fig07_intervention_forest.png", dpi=180)
    plt.close(fig)


def fig8_synthetic_transfer():
    """E016 synthetic endpoint gains and the separate real-brain transfer margins."""
    synth = json.load(open(ROOT / "outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.interpret_audit.json"))
    real = json.load(open(ROOT / "outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json"))
    synth_rows = synth["seed_rows"]
    real_rows = real["per_seed"]
    tribe = [r["tribe"]["target_minus_kd"] for r in synth_rows]
    textfeat = [r["textfeat"]["target_minus_kd"] for r in synth_rows]
    transfer = [r["tribe_minus_textfeat_gain_vs_kd"] for r in real_rows]
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 4.0))
    x = list(range(6))
    axes[0].plot(x, tribe, "o-", label="TRIBE target", color="C0")
    axes[0].plot(x, textfeat, "s-", label="projected text feature", color="C1")
    axes[0].axhline(0, color="black", lw=0.8, ls=":")
    axes[0].set_xlabel("training seed")
    axes[0].set_ylabel("synthetic target $R^2$ gain over KD")
    axes[0].set_title("A. Synthetic endpoint")
    axes[0].legend(fontsize=8)
    axes[1].plot(x, transfer, "o", color="C3")
    axes[1].axhline(0, color="black", lw=0.8, ls=":")
    axes[1].axhline(mean(transfer), color="C3", lw=1.4, label=f"mean {mean(transfer):+.4f}")
    axes[1].set_xlabel("training seed")
    axes[1].set_ylabel("TRIBE minus text-feature gain on Tuckute")
    axes[1].set_title("B. Fixed real-brain transfer endpoint")
    axes[1].legend(fontsize=8)
    fig.suptitle("Learning a synthetic neural proxy does not imply real-brain transfer")
    fig.tight_layout()
    fig.savefig(OUT / "fig08_synthetic_transfer.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    fig1_dose_response()
    fig2_collapse()
    fig3_a2()
    fig4_a3()
    fig6_quality_alignment()
    fig7_intervention_forest()
    fig8_synthetic_transfer()
    print(f"\nwrote 7 figures to {OUT}")
