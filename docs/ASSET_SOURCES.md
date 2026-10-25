# Asset and data sources

The website combines the author's two supplied method diagrams, original
qualitative research figures, and newly drawn statistical plots. The plots use
numbers transcribed from the supplied paper tables; no measurements were
estimated by tracing or digitizing a graph image.

## Opening method diagrams

| File | Dimensions | Source and use |
| --- | ---: | --- |
| `assets/images/first-stage.png` | 2048 × 1084 | PNG supplied directly by the author for the first solver stage. |
| `assets/images/second-stage.png` | 2048 × 1130 | PNG supplied directly by the author for the second solver stage. |

Both PNG files are preserved unchanged. In the opening section,
`assets/css/hero-method.css` applies `filter: invert(1) hue-rotate(180deg)` and
`mix-blend-mode: screen` to adapt their screen presentation to the dark
background. This changes only their browser appearance. The full-resolution
figure viewer opens the original PNGs without that treatment.

## Newly drawn statistical plots

The SVG figures in `assets/plots/` are generated with Matplotlib from
`data/verified-paper-data.json`. Each has a separate `-mobile.svg` layout and
an optional PNG preview. The website uses the SVG files.

| Plot | Numerical source | Scope and axes |
| --- | --- | --- |
| `dense-runtime.svg` | Main paper p.7, Table 5 | Overall solver time in seconds for Ours, OPM, and TSM on four dense face sequences. All sequences share the same logarithmic runtime axis. |
| `dense-accuracy.svg` | Main paper p.7, Table 5 | Mean normalized 3D reconstruction error for the same three methods, on a linear axis starting at zero. The complete table, including other methods, remains in the data files. |
| `mocap-tradeoff.svg` | Main paper p.7, Table 3 | Each method's unweighted arithmetic mean over all eight sequences. Runtime is shape-stage time after rotations are fixed; its axis is logarithmic. Error is mean normalized 3D reconstruction error on a linear axis. |
| `stage-timing.svg` | Supplement p.8, Table 14 | Our rotation and shape times on eight MoCap sequences. Stacked segments and totals use a zero-based linear seconds axis. |

The `mocap-tradeoff` means are recomputed from Table 3, not copied from the
coordinates of the paper's Figure 1. Each method uses the same eight-sequence
set. Plotting uses the unrounded numerical values; displayed labels may be
rounded for readability.

### Data and reproducibility

- **Canonical data:** `data/verified-paper-data.json` includes source filenames,
  table numbers, pages, metrics, timing scope, and missing-value notes.
- **CSV files:** `data/` includes the original table transcriptions and derived
  summaries. `data/PROVENANCE.md` documents the numerical validation.
- **Browser data:** `data/plot-data.js` is generated from the canonical JSON.
  `assets/js/plots.js` supplies metric tabs and accessible exact-value tables;
  `assets/css/results.css` styles their presentation.
- **Generator:** `scripts/generate_plots.py`; dependencies are listed in
  `scripts/requirements.txt`. From the website folder, run
  `python3 -m pip install -r scripts/requirements.txt`, followed by
  `python3 scripts/generate_plots.py`. This regenerates eight SVGs, PNG
  previews, and the browser data file.

### Interpretation and checks

Runtime is reported in seconds. Main Table 2 contains rotation-stage time;
Table 3 contains shape-stage time; Table 5's caption reports overall dense
solver time. Its four Ours values exactly match rotation plus shape in
supplementary Table 14. The eight Table 3 Ours shape times also match Table 14.
All twelve stage totals were checked against their component sums.

Main pp.5–6 describe Apple M3 Max runs unless noted and NVIDIA RTX 6000 Ada
for dense experiments requiring CUDA SVD. Released implementations and
hardware vary across some comparisons; runtime plots retain that source
context. They display reported measurements rather than a hardware-normalized
comparison.

Missing times remain `null` in JSON or blank in CSV. ND's `3h+ train` entries
are training-time annotations and are excluded from solver-runtime plots.
Normalized 3D error is dimensionless; the additional challenge table uses RMSE
in millimeters, a different metric. Frame and point counts identify sequences
and should not be relabeled as controlled scaling sweeps.

## Original qualitative and pipeline figures

These assets were extracted from the supplied PDFs. They retain their original
scientific colors, reconstruction points, labels, and legends. WebP files are
optimized for display; PNG or SVG companions retain source detail where listed.
They are qualitative illustrations and a computational diagram, rather than
statistical plot screenshots.

| Filename in `assets/images/` | Dimensions | Source and contents |
| --- | ---: | --- |
| `challenge-reconstructions.webp` | 3038 × 1044 | Supplement p.10, Fig.12 (also main Fig.3): Articulated, Balloon, Paper, Stretch, and Tearing observations with 3D reconstruction/ground-truth comparisons. The source figure spells Balloon as Ballon. |
| `challenge-reconstructions.png` | 3038 × 1044 | Original raster companion of Fig.12. |
| `challenge-observations.webp` | 3038 × 493 | Observation row cropped from Fig.12; used for the video poster. These are input images, not reconstructed geometry. |
| `paper-observation-reconstruction.webp` | 595 × 1044 | Paper column from Fig.12, preserving the source label, legend, and axes. PNG companion supplied. |
| `tearing-observation-reconstruction.webp` | 588 × 1044 | Tearing column from Fig.12, preserving the source label, legend, and axes. PNG companion supplied. |
| `whole-body-reconstructions.webp` | 2001 × 459 | Supplement p.10, Fig.11: H3WB Waiting 2, Directions, Eating 2, Smoking, and Smoking1. |
| `mocap-reconstructions.webp` | 2020 × 548 | Supplement p.10, Fig.13: Drink, Pickup, Stretch, and Yoga reconstruction examples. |
| `dense-face-reconstructions.webp` | 2101 × 534 | Supplement p.10, Fig.14: four dense face sequences, with source frame labels and deformation-field color bar. |
| `real-dense-reconstructions.webp` | 1601 × 1005 | Supplement p.9, Fig.10: Back, Face, and Heart observations and recovered surfaces. The Heart input is an endoscopic image. |
| `method-pipeline.webp` | 2001 × 656 | Supplement p.3, Fig.9: measurement/SVD, factor-side Euclidean correction, fixed rotations, shape updates, spectral shrinkage, FISTA, and continuation. `method-pipeline.svg` is the vector crop. |

Captions are live HTML so their text remains readable and editable. Full
original scientific figures remain available in the figure viewer and PDFs.

## Typography and identity

Manrope and DM Sans are bundled as Latin WOFF2 fonts from Google Fonts
(`fonts.googleapis.com` / `fonts.gstatic.com`). Their SIL Open Font License
files are included in `assets/fonts/`. The favicon and typographic identity
are simple SVG/CSS artwork created for the project.

The author-supplied diagrams, paper, supplementary material, and scientific
figures retain their existing rights. Bundled font licenses remain applicable.
