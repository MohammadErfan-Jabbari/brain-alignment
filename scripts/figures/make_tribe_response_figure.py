#!/usr/bin/env python3
"""Defense-deck figure: one TRIBE v2 synthetic brain response on the fsaverage5 surface.

Two stages, two environments (TRIBE's venv has no nilearn; the thesis env has no TRIBE):

    # 1. predict: run from the TRIBE checkout, exactly the E016 phase-3 route
    cd data/paper-repos/tribev2 && CUDA_VISIBLE_DEVICES=0 .venv-tribe/bin/python \
        /home/centcom/data/brain-alignment/scripts/figures/make_tribe_response_figure.py predict

    # 2. render: thesis env
    uv run python scripts/figures/make_tribe_response_figure.py render

Outputs (outputs/presentations/tribe-response/):
    response.npz      raw per-segment TRIBE predictions + the phase-3 pooled target + config
    both-lateral.png  LH lateral + RH lateral, shared scale, transparent
    lh-lateral.png    LH lateral alone, same scale
    colorbar.png      the colourbar alone
    PROVENANCE.md     what was rendered and how it was verified
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "presentations" / "tribe-response"
CORPUS = ROOT / "data/kd_corpus/wikitext103_sentences_train.txt"
LINE = 744  # 1-based line in the WikiText-103 train slice
N_VERTICES = 20484


def predict() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import tribe_predict_kd_corpus as p3  # the E016 phase-3 builder: same events, same config

    text = CORPUS.read_text(encoding="utf-8").splitlines()[LINE - 1].strip()
    model, cfg = p3.load_model(["text"])
    events, tl = p3.synthetic_word_events(
        [text], np.array([LINE - 1]), word_duration=0.35, word_gap=0.05, min_duration=1.0
    )
    preds, segments = model.predict(events, verbose=True)
    if preds.ndim != 2 or preds.shape[1] != N_VERTICES:
        raise RuntimeError(f"expected (T,{N_VERTICES}); got {preds.shape}")
    target, counts = p3.pool_by_timeline(preds, segments, tl, 1, np.arange(N_VERTICES))

    from neuralset.extractors.neuro import FSAVERAGE_SIZES

    # tribev2/main.py:512-515 sizes the output head as 2 * FSAVERAGE_SIZES[data.neuro.projection.mesh]
    mesh = model.data.neuro.projection.mesh
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez(
        OUT / "response.npz",
        sentence=text,
        corpus=str(CORPUS.relative_to(ROOT)),
        line=LINE,
        preds=preds.astype(np.float32),
        seg_start=np.array([float(getattr(s, "start", np.nan)) for s in segments]),
        target=target[0],
        counts=counts,
        config_update=json.dumps(cfg),
        mesh=str(mesh),
        fsaverage_sizes=json.dumps({k: int(v) for k, v in FSAVERAGE_SIZES.items()}),
        events=events.to_json(),
    )
    print(f"sentence: {text!r}")
    print(f"preds {preds.shape} dtype={preds.dtype}; segments={len(segments)}; mesh={mesh}")
    print(f"FSAVERAGE_SIZES={dict(FSAVERAGE_SIZES)}")
    print(f"target min/max/mean/std: {target.min():.4f} {target.max():.4f} {target.mean():.4f} {target.std():.4f}")


def render() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    from nilearn import datasets, surface
    from nilearn.plotting import plot_surf
    from PIL import Image

    z = np.load(OUT / "response.npz", allow_pickle=False)
    preds, target = z["preds"], z["target"]
    sentence, mesh = str(z["sentence"]), str(z["mesh"])
    sizes = json.loads(str(z["fsaverage_sizes"]))

    # Geometry verification: TRIBE's declared mesh, its vertex table, and nilearn's fsaverage5 meshes must agree.
    fs = datasets.fetch_surf_fsaverage("fsaverage5")
    lh = surface.load_surf_mesh(fs["pial_left"])
    rh = surface.load_surf_mesh(fs["pial_right"])
    n_lh, n_rh = len(lh.coordinates), len(rh.coordinates)
    assert mesh == "fsaverage5", f"TRIBE mesh is {mesh!r}, not fsaverage5"
    assert sizes["fsaverage5"] == n_lh == n_rh == N_VERTICES // 2, (sizes, n_lh, n_rh)
    assert target.shape == (N_VERTICES,), target.shape
    lh_vals, rh_vals = target[:n_lh], target[n_lh:]

    lim = float(np.abs(target).max())  # symmetric, no clipping: every value lies inside the range
    cmap, norm = "RdBu_r", Normalize(-lim, lim)
    W = 2200  # px per hemisphere panel before cropping to the painted pixels

    def panel(ax, mesh_, vals, hemi):
        plot_surf(
            mesh_, vals, hemi=hemi, view="lateral", bg_map=None, cmap=cmap, vmin=-lim, vmax=lim,
            colorbar=False, axes=ax, avg_method="mean",
        )
        ax.set_facecolor("none")

    def save(fig, name):
        fig.savefig(OUT / name, dpi=100, transparent=True, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        im = Image.open(OUT / name)  # the 3-D axes keep their full box; crop to the painted pixels
        im.crop(im.getchannel("A").getbbox()).save(OUT / name)

    fig, axes = plt.subplots(1, 2, figsize=(2 * W / 100, W / 100), subplot_kw={"projection": "3d"})
    panel(axes[0], lh, lh_vals, "left")
    panel(axes[1], rh, rh_vals, "right")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0)
    save(fig, "both-lateral.png")

    fig, ax = plt.subplots(figsize=(W / 100, W / 100), subplot_kw={"projection": "3d"})
    panel(ax, lh, lh_vals, "left")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    save(fig, "lh-lateral.png")

    fig, ax = plt.subplots(figsize=(W / 100, 1.6))
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation="horizontal")
    cb.set_ticks([-lim, 0, lim])
    cb.set_ticklabels([f"{-lim:.2f}", "0", f"{lim:.2f}"])
    cb.ax.tick_params(labelsize=28)
    save(fig, "colorbar.png")

    px = {n: Image.open(OUT / n).size for n in ["both-lateral.png", "lh-lateral.png", "colorbar.png"]}
    prov = f"""# TRIBE v2 synthetic response figure

- Sentence: `{sentence}` — `{z['corpus']}` line {int(z['line'])} (WikiText-103 train slice, the E016 phase-3 KD corpus).
- Generator: `facebook/tribev2`, `config_update={z['config_update']}`, features `["text"]`, synthetic timed Word events (0.35 s per word, 0.05 s gap, minimum 1.0 s), i.e. `scripts/tribe_predict_kd_corpus.py` phase-3 route.
- Raw output: `preds` shape {preds.shape} = {preds.shape[0]} TRIBE time segment(s) x {N_VERTICES} vertices. The phase-3 target is the per-timeline mean over kept segments ({int(z['counts'][0])} here); it is what is rendered.
- Geometry: TRIBE declares mesh `{mesh}`; its vertex table gives fsaverage5 = {sizes['fsaverage5']} per hemisphere; nilearn `fetch_surf_fsaverage("fsaverage5")` pial meshes have {n_lh} (LH) and {n_rh} (RH) vertices. Columns 0..{n_lh-1} = LH, {n_lh}..{N_VERTICES-1} = RH (tribev2/utils_fmri.py concatenates left then right). Rendered on the fsaverage5 pial surface, lateral view.
- Colour: `RdBu_r` (matplotlib diverging), symmetric limits ±{lim:.4f} = max |value|. No clipping, no thresholding, no smoothing, no background/sulcal shading. Value range of the rendered vector: [{target.min():.4f}, {target.max():.4f}], mean {target.mean():.4f}, sd {target.std():.4f}.
- Pixel sizes: {px}.
"""
    (OUT / "PROVENANCE.md").write_text(prov)
    print(prov)


if __name__ == "__main__":
    {"predict": predict, "render": render}[sys.argv[1]]()
