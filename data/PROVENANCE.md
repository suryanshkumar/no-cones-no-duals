# Verified numerical sources for the website plots

These files were transcribed from the supplied PDFs, with a visual check against rendered source pages. No plot points were estimated from a graph image.

## Files and scopes

| File | Source | Data scope |
| --- | --- | --- |
| `mocap-rotation-table2.csv` | Main paper p.6, Table 2 | Four CMU MoCap sequences, five methods; rotation-stage runtime and mean Frobenius rotation error. TSM's initial and refined errors are separate. |
| `mocap-shape-table3.csv` | Main paper p.7, Table 3 | Eight sequences, five methods; shape-stage runtime after rotations are fixed, paired with normalized 3D error. |
| `dense-table5.csv` | Main paper p.7, Table 5 | Four dense face sequences, eight methods; normalized 3D error. Overall runtimes exist only for OPM, TSM, and Ours. |
| `stage-breakdown-table14.csv` | Supplement p.8, Table 14 | Rotation, shape, and combined time for Ours on eight MoCap and four dense face sequences. |
| `challenge-rmse-table4.csv` | Main paper p.7, Table 4 | Five challenge categories, eight methods. RMSE in millimeters averaged over six camera trajectory types. |
| `mocap-shape-means-derived.csv` | Derived from all eight rows per method in main Table 3 | Unweighted arithmetic means of runtime and error, independently computed from the same eight-sequence set. |
| `dense-runtime-ratios-derived.csv` | Derived from main Table 5 | Baseline runtime divided by Ours for the same sequence. |
| `verified-paper-data.json` | All sources above | Complete structured dataset, citations, metrics, missing-value notes, and derived values. |

## Metric and timing labels

- `error_e3d`: mean normalized 3D reconstruction error, dimensionless, lower is better. Estimated shape is registered to ground truth.
- `error_eR`: mean Frobenius rotation error, lower is better; it is not an angle in degrees.
- `rmse_mm`: 3D RMSE in millimeters, lower is better. Do not combine its scale with normalized e3d.
- Runtime: seconds. Table 2 is rotation stage; Table 3 is shape stage; Table 5 is overall dense solver time (caption); Table 14 separates the stages explicitly.
- Table 5 Ours totals exactly match Table 14 rotation plus shape. Main p.6's general description uses the phrase 'dense shape-space solver runtime'; the specific overall caption and the explicit stage totals resolve the appropriate display label.
- Runtime context (main pp.5-6): Apple M3 Max unless noted; dense experiments requiring CUDA SVD use NVIDIA RTX 6000 Ada. Released implementations/backends and hardware may vary; the paper presents those timings as reported measurements and scaling indicators. A short source note should remain attached to the runtime plots.

## Missing values

Blank fields in the CSV and `null` in JSON mean unavailable, not zero. Dense runtime is unavailable for SMSR, DS, GM, ND, and DV. ND has no Seq.1/2 reconstruction error. The ND Seq.3/4 cells report '3h+ train'; this is training time and should not be plotted as overall solver/inference time.

## Computed MoCap means

| Method | Mean shape runtime (s) | Mean normalized 3D error |
| --- | ---: | ---: |
| BMM | 125.87000 | 0.1244625 |
| R-BMM | 14.22000 | 0.0462625 |
| OPM | 12.08250 | 0.0398750 |
| TSM | 28.93875 | 0.0305125 |
| Ours | 5.64125 | 0.0404750 |

A fresh accuracy-runtime scatter using these values should say 'mean over 8 sequences; shape stage; main Table 3'. These are table-derived means, not digitized coordinates from main Figure 1. Rounding for display can use two runtime decimals and four or five error decimals; plotting should use the unrounded values in JSON.

## Plot recommendations

1. All four dense sequences: grouped dots or bars on one shared log-seconds axis, with exact time labels and Ours highlighted.
2. MoCap accuracy-runtime: the five table-derived mean points on a logarithmic runtime x-axis and a linear normalized-error y-axis. Optionally allow per-sequence inspection using the 40 source rows.
3. Our two stages: stacked horizontal bars on a zero-based linear seconds axis, using Table 14; distinguish rotation and shape consistently with the two attached method-stage images.

Frame and point counts identify the sequence; the source does not supply a controlled frame-count/point-count sweep here. A plot against sequence frame counts must be labeled as a sequence comparison rather than a controlled scaling experiment.

## Checks completed

- Main pp.6-7 and supplement p.8 rendered at 2x and inspected.
- All 12 Table 14 totals equal rotation plus shape.
- All 8 Table 3 Ours shape runtimes match Table 14 shape times.
- All 4 Table 5 Ours overall runtimes match Table 14 totals.
- Main Table 3 has no missing values for the five displayed methods; all means use exactly eight sequences.
