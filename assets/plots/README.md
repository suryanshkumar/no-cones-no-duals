# Editable scientific charts

These figures are newly plotted from the supplied paper's tables. They are not
screenshots, interpolated measurements, or traced images.

| Plot | Input and interpretation |
| --- | --- |
| `dense-runtime.svg` | Main Table 5, page 7. Overall solver runtimes for Ours, OPM, and TSM on all four dense sequences; one shared logarithmic axis. |
| `dense-accuracy.svg` | Main Table 5, page 7. Mean normalized 3D error for the same three methods; one shared linear axis starting at zero. |
| `mocap-tradeoff.svg` | Main Table 3, page 7. Each method's unweighted arithmetic mean of shape-stage runtime and 3D error over eight sequences. The runtime axis is logarithmic. |
| `stage-timing.svg` | Supplement Table 14, page 8. Our rotation and shape timings for eight motion-capture sequences, with total runtime labels; linear axis starting at zero. |

Each plot has a `-mobile.svg` layout and a PNG companion. Use the mobile SVGs
below 600px, for example through a `<picture>` element. The four desktop SVG
files are best for enlargement. Colors and fonts are defined once in the
generation script; all labels stay editable as SVG text.

## Regenerate

From the website folder:

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/generate_plots.py
```

The script reads `data/verified-paper-data.json`, checks stage sums and the
arithmetic means, and writes all eight SVGs, their PNG companions, and
`data/plot-data.js`. The latter is a browser-friendly copy of the complete
canonical JSON for exact-value tables without network loading. The two derived
CSV summaries (MoCap means and dense runtime ratios) are recomputed from the
raw JSON rows each time. The other CSV files are the original transcriptions;
update those too if source values are revised. SVG text retains DejaVu Sans
with explicit Arial and generic sans-serif browser fallbacks.

The website itself needs no Python, package installation, or build step.

Runtimes describe the reported implementations and hardware, which vary across
methods; they are not normalized same-hardware estimates. Table 3 contains
shape-stage timings after rotations have been fixed, whereas Table 5 contains
overall dense-sequence timings. Sequence frame/point counts are metadata, not
a controlled scaling sweep. Missing source-table runtimes are not imputed.
