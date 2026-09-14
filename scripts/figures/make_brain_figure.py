"""Left-hemisphere language-network figure for the defense deck.

Renders the five LH parcels of the EvLab SN220 language parcel set on the
fsaverage pial surface, lateral view, as a flat vector figure.

    uv run python scripts/figures/make_brain_figure.py

Pinned (from uv.lock at the time of writing): nilearn 0.13.1, nibabel 5.4.2,
matplotlib 3.10.9, numpy 2.4.6, scipy 1.17.1.

Outputs (outputs/presentations/brain-lh-language/):
    brain-lh-language.svg, brain-lh-language.png, parcel-anchors.json,
    PROVENANCE.md, and check-320px.png (acceptance render, not a deliverable).
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch
from nilearn import datasets, surface
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "evlab-parcels"
OUT = ROOT / "outputs" / "presentations" / "brain-lh-language"

PARCEL_URL = "https://www.evlab.mit.edu/s/allParcels-language-SN220-hgwm.nii"
INDEX_URL = "https://evlab.squarespace.com/s/allParcels-language-SN220.txt"
PARCEL_FILE = DATA / "allParcels-language-SN220.nii"
INDEX_FILE = DATA / "allParcels-language-SN220.txt"

REGIONS = ["AntTemp", "IFG", "IFGorb", "MFG", "PostTemp"]

CORTEX = "#e3dacc"
PARCEL = "#d97757"
LINE = "#141413"
VIEW_W = 320.0            # SVG user units across the hemisphere
STROKE = 1.25             # px at 320 px wide
RASTER_W = 2400           # px, working raster and PNG width
CREASE_MM = 3.0           # depth jump between neighbouring pixels that counts as a sulcal crease
# Landmark sulci kept, as MNI boxes (y_min, y_max, z_min, z_max); the longest crease with
# >= 70% of its pixels inside a box is that landmark.
LANDMARKS = {"Sylvian": (-45, 35, -22, 22), "Central": (-40, 2, 20, 80), "STS": (-70, 8, -32, -5)}
LINE_PX = 9.0             # crease line width in raster px (= STROKE at 320 px display)
MIN_PARCEL_COVERAGE = 0.5 # fraction of depth samples inside the parcel


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def download() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for url, dst in [(PARCEL_URL, PARCEL_FILE), (INDEX_URL, INDEX_FILE)]:
        if dst.exists():
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        dst.write_bytes(urllib.request.urlopen(req, timeout=120).read())


def parcel_labels() -> dict[str, int]:
    names = [l.strip() for l in INDEX_FILE.read_text().splitlines() if l.strip()]
    return {n.split("_", 1)[1]: i + 1 for i, n in enumerate(names) if n.startswith("LH_")}


def project(img, labels: dict[str, int], fs) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return pial coords, faces, per-vertex region index (-1 = none), sulc."""
    coords, faces = surface.load_surf_mesh(fs["pial_left"])
    white = fs["white_left"]
    vol = np.asarray(img.dataobj)
    cover = np.zeros((len(REGIONS), len(coords)))
    for k, r in enumerate(REGIONS):
        m = nib.Nifti1Image((vol == labels[r]).astype(np.float32), img.affine)
        # Fraction of samples between white and pial that fall inside the parcel.
        cover[k] = surface.vol_to_surf(m, fs["pial_left"], inner_mesh=white,
                                       interpolation="linear", depth=np.linspace(0, 1, 7))
    best = cover.argmax(0)
    region = np.where(cover.max(0) >= MIN_PARCEL_COVERAGE, best, -1)
    sulc = surface.load_surf_data(fs["sulc_left"])
    return coords, faces, region, sulc


def lateral_xy(coords: np.ndarray) -> np.ndarray:
    """Orthographic LH lateral view: anterior left, dorsal up (raster y down)."""
    return np.column_stack([-coords[:, 1], -coords[:, 2]])


def rasterize(xy, faces, depth, values, extent, shape) -> np.ndarray:
    """Painter's-algorithm flat rasterization of integer face values.

    Returns an int array (shape) with -1 where nothing was drawn.
    """
    order = np.argsort(depth)              # far first, near last
    h, w = shape
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(extent[0], extent[1]); ax.set_ylim(extent[3], extent[2])  # y down
    fig.patch.set_facecolor("black")
    v = values[order] + 1                  # 0 = background
    cols = np.zeros((len(v), 3)); cols[:, 0] = v / 255.0
    pc = PolyCollection(xy[faces[order]], facecolors=cols, edgecolors=cols,
                        linewidths=0.3, antialiased=False)
    ax.add_collection(pc)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, 0].astype(int)
    plt.close(fig)
    return buf - 1


def contours(mask: np.ndarray, sigma: float = 2.5, min_area: float = 0.0) -> list[np.ndarray]:
    """Smoothed 0.5-level contours of a binary mask, largest components only."""
    lab, n = ndimage.label(mask)
    if n == 0:
        return []
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    keep = np.isin(lab, 1 + np.flatnonzero(sizes >= max(min_area, 1)))
    keep = ndimage.binary_fill_holes(keep)
    sm = ndimage.gaussian_filter(keep.astype(float), sigma)
    fig, ax = plt.subplots()
    cs = ax.contour(sm, levels=[0.5])
    polys = []
    for path in cs.get_paths():
        for poly in path.to_polygons(closed_only=False):
            if len(poly) > 8:
                polys.append(np.asarray(poly))
    plt.close(fig)
    return polys


def creases(xy, faces, depth, extent, shape, cortex_mask, mm_per_px):
    """Depth-discontinuity lines of the lateral pial view: the longest ones, as filled slivers.

    A sulcus seen from the side is a jump in depth between the near bank and the far bank
    (or the fissure floor), so thresholding the depth gradient draws the sulcal map without
    any shading. Returns polygons (raster px) of the landmark creases in LANDMARKS.
    """
    q = np.round((depth - depth.min()) / (depth.max() - depth.min()) * 240).astype(int)
    d = rasterize(xy, faces, depth, q, extent, shape).astype(float)
    d[~cortex_mask] = np.nan
    gy, gx = np.gradient(d)
    jump = np.nan_to_num(np.hypot(gx, gy)) * (depth.max() - depth.min()) / 240
    crease = ndimage.binary_closing(jump > CREASE_MM, iterations=2)
    crease &= ndimage.binary_erosion(cortex_mask, iterations=int(LINE_PX))  # keep off the silhouette
    lab, n = ndimage.label(crease)
    sizes = ndimage.sum(crease, lab, range(1, n + 1))
    chosen = []
    for name, (y0, y1, z0, z1) in LANDMARKS.items():
        best = None
        for i in np.argsort(sizes)[::-1][:40]:
            ys, xs = np.nonzero(lab == i + 1)
            Y = -(extent[0] + xs * mm_per_px); Z = -(extent[2] + ys * mm_per_px)   # MNI y, z
            inside = ((Y >= y0) & (Y <= y1) & (Z >= z0) & (Z <= z1)).mean()
            if inside >= 0.7 and (best is None or sizes[i] > sizes[best]):
                best = i
        assert best is not None, f"no crease found for {name}"
        chosen.append(best + 1)
        print(f"{name}: crease of {int(sizes[best])} px")
    keep = ndimage.binary_dilation(np.isin(lab, chosen), iterations=int(LINE_PX // 2))
    return contours(keep, sigma=2.0)


def simplify(poly: np.ndarray, tol: float) -> np.ndarray:
    """Drop points closer than tol to the previously kept point."""
    keep = [poly[0]]
    for p in poly[1:]:
        if np.hypot(*(p - keep[-1])) >= tol:
            keep.append(p)
    return np.asarray(keep)


def svg_path(polys: list[np.ndarray], scale: float) -> str:
    parts = []
    for poly in polys:
        pts = poly * scale
        parts.append("M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z")
    return " ".join(parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    download()
    labels = parcel_labels()
    assert set(REGIONS) <= labels.keys(), labels
    img = nib.load(PARCEL_FILE)
    fs = datasets.fetch_surf_fsaverage("fsaverage")
    coords, faces, region, sulc = project(img, labels, fs)

    # Per-face values (majority of a face's three vertices; -1 if fewer than 2 agree).
    fr = region[faces]
    face_region = np.where((fr[:, 0] == fr[:, 1]) | (fr[:, 0] == fr[:, 2]), fr[:, 0],
                           np.where(fr[:, 1] == fr[:, 2], fr[:, 1], -1))
    depth = -coords[faces, 0].mean(1)  # viewer at -x: smaller x is nearer -> larger key

    xy = lateral_xy(coords)
    x0, y0 = xy.min(0); x1, y1 = xy.max(0)
    pad = 0.01 * (x1 - x0)
    extent = (x0 - pad, x1 + pad, y0 - pad, y1 + pad)
    w = RASTER_W
    h = int(round(w * (extent[3] - extent[2]) / (extent[1] - extent[0])))
    shape = (h, w)

    reg_img = rasterize(xy, faces, depth, face_region, extent, shape)   # 0..4 = region, -1 = other
    cortex_mask = rasterize(xy, faces, depth, np.zeros(len(faces), int), extent, shape) >= 0

    scale = VIEW_W / w
    tol = 0.6 * (w / VIEW_W)   # ~0.6 user units

    cortex_polys = [simplify(p, tol) for p in contours(cortex_mask, sigma=3.0, min_area=0.05 * cortex_mask.sum())]
    parcel_polys: dict[str, list[np.ndarray]] = {}
    coverage: dict[str, dict] = {}
    for k, r in enumerate(REGIONS):
        m = reg_img == k
        n_vis = int(m.sum())
        polys = contours(m, sigma=2.5, min_area=0.03 * max(n_vis, 1))
        parcel_polys[r] = [simplify(p, tol) for p in polys]
        coverage[r] = {"visible_px": n_vis, "vertices": int((region == k).sum()), "pieces": len(polys)}
        assert polys, f"{r} not visible in lateral view"

    # Major sulci: the longest depth-discontinuity creases of the lateral view.
    sulc_polys = [simplify(p, tol) for p in creases(xy, faces, depth, extent, shape, cortex_mask, (extent[1] - extent[0]) / w)]

    # --- SVG ---------------------------------------------------------------
    W = w * scale; H = h * scale
    sw = STROKE
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.2f}" height="{H:.2f}">']
    parts.append(f'<g id="cortex"><path d="{svg_path(cortex_polys, scale)}" fill="{CORTEX}" stroke="{LINE}" '
                 f'stroke-width="{sw}" stroke-linejoin="round" fill-rule="evenodd"/></g>')
    parts.append(f'<g id="sulci"><path d="{svg_path(sulc_polys, scale)}" fill="{LINE}" stroke="none" fill-rule="evenodd"/></g>')
    parts.append('<g id="parcels">')
    for r in REGIONS:
        parts.append(f'<g id="{r}"><path d="{svg_path(parcel_polys[r], scale)}" fill="{PARCEL}" stroke="{LINE}" '
                     f'stroke-width="{sw}" stroke-linejoin="round" fill-rule="evenodd"/></g>')
    parts.append("</g></svg>")
    (OUT / "brain-lh-language.svg").write_text("\n".join(parts))

    # --- anchors (from the SVG polygons themselves) ------------------------
    def centroid(polys):
        a = c = 0.0
        for q in polys:
            x, y = q[:, 0], q[:, 1]; xn, yn = np.roll(x, -1), np.roll(y, -1)
            cross = x * yn - xn * y; area = cross.sum() / 2
            a += area; c += np.array([((x + xn) * cross).sum(), ((y + yn) * cross).sum()]) / 6
        return c / a
    anchors = {}
    for r in REGIONS:
        pts = np.vstack(parcel_polys[r]) * scale; cx, cy = centroid(parcel_polys[r]) * scale
        (x0_, y0_), (x1_, y1_) = pts.min(0), pts.max(0)
        anchors[r] = {k: round(float(v), 2) for k, v in
                      dict(cx=cx, cy=cy, x=x0_, y=y0_, w=x1_ - x0_, h=y1_ - y0_).items()}
    (OUT / "parcel-anchors.json").write_text(json.dumps(anchors, indent=2))

    # --- PNG (same geometry, matplotlib) -----------------------------------
    def draw(path: Path, width_px: int, ground: str | None):
        fig = plt.figure(figsize=(width_px / 100, width_px / 100 * H / W), dpi=100)
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
        ax.set_xlim(0, W); ax.set_ylim(H, 0)
        fig.patch.set_alpha(0.0 if ground is None else 1.0)
        if ground:
            fig.patch.set_facecolor(ground)
        lw = sw * width_px / VIEW_W * 72 / 100  # user units -> points at this dpi
        def patch(polys, **kw):
            verts = np.vstack([np.vstack([p * scale, p[:1] * scale]) for p in polys])
            codes = np.hstack([[MplPath.MOVETO] + [MplPath.LINETO] * (len(p) - 1) + [MplPath.CLOSEPOLY] for p in polys])
            ax.add_patch(PathPatch(MplPath(verts, codes), **kw))
        patch(cortex_polys, facecolor=CORTEX, edgecolor=LINE, linewidth=lw, joinstyle="round")
        patch(sulc_polys, facecolor=LINE, edgecolor="none", linewidth=0)
        for r in REGIONS:
            patch(parcel_polys[r], facecolor=PARCEL, edgecolor=LINE, linewidth=lw, joinstyle="round")
        fig.savefig(path, dpi=100, transparent=ground is None, facecolor=fig.get_facecolor())
        plt.close(fig)

    draw(OUT / "brain-lh-language.png", RASTER_W, None)
    draw(OUT / "check-320px.png", 320, "#f0eee6")

    # --- provenance --------------------------------------------------------
    centroids = {}
    vol = np.asarray(img.dataobj)
    for r in REGIONS:
        ijk = np.argwhere(vol == labels[r])
        mni = nib.affines.apply_affine(img.affine, ijk)
        centroids[r] = {"n_voxels": int(len(ijk)), "mni_centroid": mni.mean(0).round(1).tolist(),
                        "mni_min": mni.min(0).round(0).tolist(), "mni_max": mni.max(0).round(0).tolist()}
    import importlib.metadata as md
    vers = {p: md.version(p) for p in ["nilearn", "nibabel", "matplotlib", "numpy", "scipy"]}
    prov = f"""# Provenance: brain-lh-language

## Parcel source

- File: `{PARCEL_FILE.name}` (served as `allParcels-language-SN220-hgwm.nii`), SHA-256 `{sha256(PARCEL_FILE)}`
- Index: `{INDEX_FILE.name}`, SHA-256 `{sha256(INDEX_FILE)}`
- Download: {PARCEL_URL} and {INDEX_URL}, from the EvLab parcels page https://www.evlab.mit.edu/resources-all/download-parcels (fetched 2026-09-14).
- Version: the "updated parcels created from a probabilistic overlap map from 220 participants (currently in use in EvLab)", the SN220 set. The page states this version merges the two anterior temporal and the two posterior temporal parcels of Fedorenko et al. (2010). This release contains ten labels, five per hemisphere; there is no AngG label in it.
- Volume: {img.shape}, 2 mm isotropic, MNI152 (SPM) space. Labels used: {json.dumps({r: labels[r] for r in REGIONS})}.

## Citations

- Parcel set: Fedorenko E., Hsieh P.-J., Nieto-Castañón A., Whitfield-Gabrieli S., Kanwisher N. (2010). New method for fMRI investigations of language: defining ROIs functionally in individual subjects. *Journal of Neurophysiology* 104(2):1177-1194. https://doi.org/10.1152/jn.00032.2010. Parcels distributed at https://evlab.mit.edu/funcloc.
- fROI definition used by the thesis data: Tuckute G., Sathe A., Srikant S., Taliaferro M., Wang M., Schrimpf M., Kay K., Fedorenko E. (2024). Driving and suppressing the human language network using large language models. *Nature Human Behaviour* 8:544-561. https://doi.org/10.1038/s41562-023-01783-7.

## Rendering

- Surface: nilearn `fetch_surf_fsaverage("fsaverage")` (FreeSurfer fsaverage, 163,842 vertices per hemisphere), left hemisphere, **pial** surface. Pial was chosen over inflated because the silhouette stays recognisably a brain at slide size; all five parcels remain visible on the lateral pial surface (per-parcel visible pixel counts below).
- Projection: each parcel mask sampled along the white-to-pial depth at seven points (`vol_to_surf`, linear interpolation of the binary mask); a vertex belongs to the parcel with the highest coverage if that coverage is at least {MIN_PARCEL_COVERAGE:.0%}. Faces take the majority vertex label.
- View: orthographic lateral projection (drop MNI x; screen x = -y so anterior is left, screen y = -z so dorsal is up). Hidden surfaces removed by depth-sorted painting at {RASTER_W} px width, then vector outlines traced from the label raster (Gaussian smoothing sigma 2.5 px at {RASTER_W} px, 0.5-level contour, components below 3% of the parcel's visible area dropped).
- Sulcal lines: the lateral view is depth-buffered, so a sulcus appears as a jump in depth between neighbouring pixels. Pixels where that jump exceeds {CREASE_MM} mm are creases; the longest connected crease lying (70% of its pixels) inside each landmark box {json.dumps(LANDMARKS)} (MNI y_min, y_max, z_min, z_max; Sylvian fissure, central sulcus, superior temporal sulcus) is kept and drawn as filled {LINE_PX:.0f} px slivers (the same visual weight as the {STROKE} px strokes at 320 px). No `sulc` map or shading is used.
- Colours: cortex {CORTEX}, parcels {PARCEL}, lines {LINE}; strokes {STROKE} user units where the SVG viewBox is {VIEW_W:.0f} units wide, so {STROKE} px at 320 px display. No shading, gradients, transparency in fills, or text. Background alpha 0.
- Library versions: {json.dumps(vers)}.

## Parcel geometry (from the volume, MNI mm)

| Region | voxels | centroid | min | max | visible px @{RASTER_W} | pieces |
| --- | --- | --- | --- | --- | --- | --- |
""" + "\n".join(
        f"| {r} | {centroids[r]['n_voxels']} | {centroids[r]['mni_centroid']} | {centroids[r]['mni_min']} | {centroids[r]['mni_max']} | {coverage[r]['visible_px']} | {coverage[r]['pieces']} |"
        for r in REGIONS) + f"""

## Deviations from the brief

- The brief calls the set "langloc / SN220"; the distributed file is `allParcels-language-SN220`. Same set.
- The brief suggested the Sylvian fissure, STS and inferior frontal sulcus as landmarks. The central sulcus replaces the inferior frontal sulcus: in the depth-buffered lateral pial view the IFS is fragmented into short creases, while the central sulcus is one continuous crease and separates the MFG parcel from parietal cortex, which is the orientation the figure has to defend.
- `check-320px.png` is written alongside the deliverables as the 320 px acceptance render on #f0eee6; it is not part of the figure set.
- Parcel geometry is what the atlas defines. The MFG parcel (MNI y {centroids['MFG']['mni_min'][1]:.0f} to {centroids['MFG']['mni_max'][1]:.0f}) sits in posterior middle frontal gyrus adjacent to, but as labelled by the atlas not inside, precentral cortex.
"""
    (OUT / "PROVENANCE.md").write_text(prov)
    print(json.dumps({"coverage": coverage, "anchors": anchors, "sulci_polys": len(sulc_polys), "svg_kb": round((OUT / 'brain-lh-language.svg').stat().st_size / 1024)}, indent=1))


if __name__ == "__main__":
    main()
