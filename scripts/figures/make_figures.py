"""Generate the thesis figures from RECORDED evidence (manuscript D011 rule).

Reads outputs/*.json (E006/E009/E010) + the recorded headline numbers (E005/E008,
cited inline). Renders to outputs/figures/ (gitignored); chosen figures are copied to
docs/manuscript/figures/ by hand.

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
    """E010: brain-specific gap(k) vs subjects averaged + noise-ceiling NC_k overlay."""
    d = json.load(open(ROOT / "outputs/E010_averaging_doseresponse.json"))
    bykseed = defaultdict(dict)
    for r in d["raw"]:
        bykseed[(r["k"], r["seed"])][r["arm"]] = r["unique_r2"]
    ks = sorted({r["k"] for r in d["raw"]})
    seeds = sorted({r["seed"] for r in d["raw"]})
    nc = d["nc"]
    gap_m, gap_e, nck = [], [], []
    for k in ks:
        gaps = [bykseed[(k, s)]["mse"] - bykseed[(k, s)]["mse_perm"] for s in seeds]
        gap_m.append(mean(gaps))
        gap_e.append((stdev(gaps) / math.sqrt(len(gaps))) if len(gaps) > 1 else 0)
        nck.append(nc / (nc + (1 - nc) / k))
    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.axhline(0, color="grey", lw=0.8, ls=":")
    ax1.errorbar(ks, gap_m, yerr=gap_e, marker="o", color="C3", capsize=3, lw=2, label="brain-specific gap (mse − perm)")
    ax1.set_xlabel("k  (subjects averaged into the fMRI target)")
    ax1.set_ylabel("held-out brain-specific gap  Δ unique R²", color="C3")
    ax1.set_xticks(ks)
    ax1.tick_params(axis="y", labelcolor="C3")
    ax2 = ax1.twinx()
    ax2.plot(ks, nck, marker="s", color="C0", ls="--", alpha=0.7, label="predicted ceiling NC_k")
    ax2.set_ylabel("predicted noise ceiling  NC_k", color="C0")
    ax2.tick_params(axis="y", labelcolor="C0")
    ax1.set_title("E010: averaging produces the apparent brain-specificity\n(gap ≈ 0 at k=1, grows with averaging)")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_dose_response.png", dpi=150)
    plt.close(fig)
    print(f"fig1: gap(k)={[round(g,5) for g in gap_m]} at k={ks}")


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


if __name__ == "__main__":
    fig1_dose_response()
    fig2_collapse()
    fig3_a2()
    fig4_a3()
    print(f"\nwrote 4 figures to {OUT}")
