#!/usr/bin/env python3
"""Regenerate the website's scientific plots from transcribed paper tables.

Run from any directory: python3 scripts/generate_plots.py
Input: data/verified-paper-data.json. Output: assets/plots/*.svg and *.png.
No network, model, or browser is needed. All coordinates come from table data.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, NullLocator
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/verified-paper-data.json").read_text())
OUT = ROOT / "assets/plots"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#101014"
FG = "#f5f5f7"
MUTED = "#b6b6c4"
GRID = "#303038"
COLORS = {"Ours": "#a7b0ff", "OPM": "#69d5d9", "TSM": "#e8b47e",
          "BMM": "#d49bc2", "R-BMM": "#a9b1c5"}
MARKERS = {"Ours": "o", "OPM": "D", "TSM": "s", "BMM": "^", "R-BMM": "P"}
METHODS = ["Ours", "OPM", "TSM"]
SEQUENCES = [f"Face Seq.{i}" for i in range(1, 5)]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12,
    "figure.facecolor": BG, "axes.facecolor": BG,
    "text.color": FG, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": GRID, "grid.color": GRID,
    "svg.fonttype": "none", "svg.hashsalt": "no-cones-no-duals",
    "savefig.facecolor": BG, "axes.unicode_minus": False,
})


def clean(ax, *, grid="x", ticks=12):
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", which="both", length=0, labelsize=ticks, pad=9)
    ax.set_axisbelow(True)
    if grid:
        ax.grid(axis=grid, linewidth=.8, alpha=.75)


def save(fig, name, description):
    """Keep vector text editable and attach descriptive accessible SVG metadata."""
    svg = OUT / f"{name}.svg"
    svg_temporary = OUT / f".{name}.svg.tmp"
    png_temporary = OUT / f".{name}.png.tmp"
    fig.savefig(svg_temporary, format="svg", metadata={"Date": None, "Description": description})
    fig.savefig(png_temporary, format="png", dpi=160)
    png_temporary.replace(OUT / f"{name}.png")
    # A native SVG description also helps when the file is opened by itself.
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(svg_temporary)
    root = tree.getroot()
    # Matplotlib measures with DejaVu Sans. Add browser fallbacks only after
    # drawing, preserving the plotted layout and original text coordinates.
    for element in root.iter():
        style = element.get("style")
        if style and "font-family: 'DejaVu Sans'" in style:
            element.set("style", style.replace(
                "font-family: 'DejaVu Sans'", "font-family: 'DejaVu Sans', Arial, sans-serif"
            ))
    root.set("role", "img")
    root.set("aria-labelledby", f"{name}-title {name}-description")
    title = ET.Element("{http://www.w3.org/2000/svg}title", {"id": f"{name}-title"})
    title.text = name.replace("-mobile", "").replace("-", " ").title()
    desc = ET.Element("{http://www.w3.org/2000/svg}desc", {"id": f"{name}-description"})
    desc.text = description
    root.insert(0, title)
    root.insert(1, desc)
    tree.write(svg_temporary, encoding="utf-8", xml_declaration=True)
    svg_temporary.replace(svg)
    plt.close(fig)


def dense_rows():
    return {(r["sequence"], r["method"]): r for r in DATA["dense"] if r["method"] in METHODS}


def legend(ax, *, mobile=False, labels=None):
    names = labels or METHODS
    handles = [Line2D([], [], color=COLORS[m], marker=MARKERS[m], lw=0,
                      markersize=8 if mobile else 9, markeredgewidth=0, label=m) for m in names]
    ax.legend(handles=handles, ncol=len(names), frameon=False, loc="lower left",
              bbox_to_anchor=(-.01, 1.02), borderaxespad=0,
              handletextpad=.5, columnspacing=1.6 if not mobile else 1.0,
              labelcolor=FG, fontsize=13.5 if mobile else 13)


def dense_runtime(mobile=False):
    data = dense_rows()
    if mobile:
        fig, ax = plt.subplots(figsize=(4.6, 7.8))
        fig.subplots_adjust(left=.17, right=.76, top=.91, bottom=.12)
        ymax = 14.8
        for i, seq in enumerate(SEQUENCES):
            base = 13.5 - i * 3.65
            frames = data[seq, "Ours"]["frames"]
            ax.text(0, base + .65, f"Face {i+1}  ·  {frames} frames",
                    transform=ax.get_yaxis_transform(), color=FG, size=14, weight="bold")
            for j, m in enumerate(METHODS):
                y = base - j * .83
                val = data[seq, m]["runtime_seconds"]
                ax.plot([3, val], [y, y], color=COLORS[m], alpha=.2, lw=3, solid_capstyle="round")
                ax.scatter(val, y, color=COLORS[m], marker=MARKERS[m], s=65, zorder=4)
                ax.text(-.035, y, m, transform=ax.get_yaxis_transform(), ha="right", va="center",
                        color=COLORS[m], size=12.5, weight="bold" if m == "Ours" else "normal")
                # Values in a dedicated label column avoid occluding close marks.
                ax.text(1.35593, y, f"{val:,.2f}", transform=ax.get_yaxis_transform(),
                        ha="right", va="center", color=FG, size=13.5,
                        bbox={"facecolor": BG, "edgecolor": "none", "pad": 1.5})
        ax.set_ylim(-.5, ymax)
        ax.set_yticks([])
        ax.set_xscale("log")
        ax.set_xlim(3, 25000)
        ax.set_xticks([10, 100, 1000, 10000], ["10", "100", "1k", "10k"])
        ax.xaxis.set_minor_locator(NullLocator())
        clean(ax, ticks=12)
        ax.set_xlabel("Overall runtime (seconds)\nLogarithmic scale · lower is better", size=12, labelpad=15, linespacing=1.7)
        legend(ax, mobile=True)
    else:
        fig, ax = plt.subplots(figsize=(11, 4.5))
        fig.subplots_adjust(left=.13, right=.98, top=.83, bottom=.19)
        for i, seq in enumerate(SEQUENCES):
            y = 3 - i
            vals = [data[seq, m]["runtime_seconds"] for m in METHODS]
            ax.plot([min(vals), max(vals)], [y, y], color="#454550", lw=1.5, zorder=1)
            for m, val in zip(METHODS, vals):
                if m == "Ours":
                    ax.scatter(val, y, color=COLORS[m], s=410, alpha=.10, zorder=2)
                ax.scatter(val, y, color=COLORS[m], marker=MARKERS[m], s=95 if m == "Ours" else 70, zorder=4)
                ax.annotate(f"{val:,.2f} s", (val, y), xytext=(0, 13), textcoords="offset points",
                            ha="center", va="bottom", color=COLORS[m], size=12.5,
                            weight="bold" if m == "Ours" else "normal")
        ax.set_ylim(-.45, 3.65)
        ax.set_yticks([3, 2, 1, 0], [f"Face {i+1}\n{data[s, 'Ours']['frames']} frames" for i, s in enumerate(SEQUENCES)])
        ax.set_xscale("log")
        ax.set_xlim(3, 25000)
        ax.set_xticks([10, 100, 1000, 10000], ["10", "100", "1,000", "10,000"])
        ax.xaxis.set_minor_locator(NullLocator())
        clean(ax, ticks=12.5)
        ax.set_xlabel("Overall runtime (seconds)  ·  logarithmic scale  ·  lower is better", size=12.5, labelpad=15)
        legend(ax)
    save(fig, "dense-runtime" + ("-mobile" if mobile else ""),
         "Overall solver runtime in seconds for four dense face sequences with 28,887 points each. "
         "Ours, OPM, and TSM. Shared logarithmic axis. Main paper Table 5, page 7; "
         "Ours totals match supplementary Table 14. Runtime implementations and hardware vary.")


def dense_accuracy(mobile=False):
    data = dense_rows()
    if mobile:
        fig, ax = plt.subplots(figsize=(4.6, 7.8))
        fig.subplots_adjust(left=.17, right=.76, top=.91, bottom=.12)
        for i, seq in enumerate(SEQUENCES):
            base = 13.5 - i * 3.65
            frames = data[seq, "Ours"]["frames"]
            ax.text(0, base + .65, f"Face {i+1}  ·  {frames} frames",
                    transform=ax.get_yaxis_transform(), color=FG, size=14, weight="bold")
            for j, m in enumerate(METHODS):
                y = base - j * .83
                val = data[seq, m]["error_e3d"]
                ax.plot([0, val], [y, y], color=COLORS[m], alpha=.2, lw=3, solid_capstyle="round")
                ax.scatter(val, y, color=COLORS[m], marker=MARKERS[m], s=65, zorder=4)
                ax.text(-.035, y, m, transform=ax.get_yaxis_transform(), ha="right", va="center",
                        color=COLORS[m], size=12.5, weight="bold" if m == "Ours" else "normal")
                ax.text(1.35593, y, f"{val:.4f}", transform=ax.get_yaxis_transform(), ha="right", va="center",
                        color=FG, size=13.5, bbox={"facecolor": BG, "edgecolor": "none", "pad": 1.5})
        ax.set_ylim(-.5, 14.8)
        ax.set_xlim(0, .25)
        ax.set_yticks([])
        ax.set_xticks([0, .1, .2], ["0", "0.10", "0.20"])
        clean(ax, ticks=12)
        ax.set_xlabel("Normalized 3D error, $e_{3d}$\nLinear scale · lower is better", size=12, labelpad=15, linespacing=1.7)
        legend(ax, mobile=True)
    else:
        fig, ax = plt.subplots(figsize=(11, 4.5))
        fig.subplots_adjust(left=.13, right=.98, top=.83, bottom=.19)
        for i, seq in enumerate(SEQUENCES):
            base = 3 - i
            for j, m in enumerate(METHODS):
                val = data[seq, m]["error_e3d"]
                y = base + (.22 - j * .22)
                ax.plot([0, val], [y, y], color=COLORS[m], alpha=.15, lw=2.6, solid_capstyle="round")
                ax.scatter(val, y, color=COLORS[m], marker=MARKERS[m], s=68, zorder=4)
                ax.annotate(f"{val:.4f}", (val, y), xytext=(9, 0), textcoords="offset points",
                            ha="left", va="center", color=COLORS[m], size=11.5,
                            weight="bold" if m == "Ours" else "normal")
            if i < 3:
                ax.axhline(base - .5, color=GRID, lw=.6, alpha=.6)
        ax.set_ylim(-.6, 3.65)
        ax.set_yticks([3, 2, 1, 0], [f"Face {i+1}\n{data[s, 'Ours']['frames']} frames" for i, s in enumerate(SEQUENCES)])
        ax.set_xlim(0, .26)
        ax.set_xticks([0, .05, .10, .15, .20, .25], ["0", "0.05", "0.10", "0.15", "0.20", "0.25"])
        clean(ax, ticks=12.5)
        ax.set_xlabel("Normalized 3D reconstruction error, $e_{3d}$  ·  lower is better", size=12.5, labelpad=15)
        legend(ax)
    save(fig, "dense-accuracy" + ("-mobile" if mobile else ""),
         "Mean normalized 3D reconstruction error for Ours, OPM and TSM on the four dense face sequences. "
         "Lower is better. Linear axis starting at zero. Main paper Table 5, page 7. "
         "The three methods match the accompanying runtime comparison; all source-table methods are in the downloadable data.")


def mocap_tradeoff(mobile=False):
    rows = DATA["mocap_shape"]
    names = ["Ours", "OPM", "R-BMM", "TSM", "BMM"]
    means = {m: (mean(r["runtime_seconds"] for r in rows if r["method"] == m),
                 mean(r["error_e3d"] for r in rows if r["method"] == m)) for m in names}
    fig, ax = plt.subplots(figsize=(4.6, 5.2) if mobile else (6.6, 5.2))
    fig.subplots_adjust(left=.20 if mobile else .15, right=.96, top=.95, bottom=.19)
    clean(ax, grid="both", ticks=11.5 if mobile else 12)
    ax.set_xscale("log")
    ax.set_xlim(3.8, 220)
    ax.set_ylim(0, .155)
    ax.set_xticks([5, 10, 30, 100], ["5", "10", "30", "100"])
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_yticks([0, .04, .08, .12], ["0", "0.04", "0.08", "0.12"])
    offsets = {"Ours": (8, 18), "OPM": (-9, -27), "R-BMM": (11, 25), "TSM": (12, -14), "BMM": (-9, 16)}
    if mobile:
        offsets = {"Ours": (2, 19), "OPM": (-10, -33), "R-BMM": (10, 24), "TSM": (10, -14), "BMM": (-7, 14)}
    for m in names:
        x, y = means[m]
        if m == "Ours":
            ax.scatter(x, y, s=800, color=COLORS[m], alpha=.09, zorder=3)
            ax.scatter(x, y, s=380, color=COLORS[m], alpha=.13, zorder=3)
        ax.scatter(x, y, s=130 if m == "Ours" else 85, color=COLORS[m], marker=MARKERS[m],
                   edgecolor=BG, linewidth=.8, zorder=5)
        dx, dy = offsets[m]
        ax.annotate(m, (x, y), xytext=(dx, dy), textcoords="offset points",
                    ha="right" if m == "BMM" else "left", va="center",
                    size=12.5 if not mobile else 12, color=COLORS[m],
                    weight="bold" if m == "Ours" else "normal",
                    arrowprops={"arrowstyle": "-", "color": COLORS[m], "lw": .65,
                                "shrinkA": 4, "shrinkB": 7})
    ax.set_xlabel("Mean shape runtime (s) · log scale", size=11.5 if mobile else 12, labelpad=16)
    ax.set_ylabel("Mean normalized 3D error, $e_{3d}$", size=11.5 if mobile else 12, labelpad=12)
    ax.text(.025, .97, "Lower and left is better", transform=ax.transAxes, va="top",
            color=MUTED, size=10.5 if mobile else 11)
    save(fig, "mocap-tradeoff" + ("-mobile" if mobile else ""),
         "Shape recovery accuracy and runtime: each marker is the unweighted arithmetic mean of eight "
         "CMU MoCap sequences in main paper Table 3, page 7. Rotations are fixed for this stage. "
         "Runtime axis is logarithmic and error axis linear. Ours: 5.64125 seconds and 0.040475 error. "
         "OPM: 12.0825 and 0.039875. R-BMM: 14.22 and 0.0462625. TSM: 28.93875 and 0.0305125. "
         "BMM: 125.87 and 0.1244625. These are reported implementation timings, not normalized same-hardware estimates.")


def stage_timing(mobile=False):
    rows = [r for r in DATA["stage_breakdown"] if r["benchmark"] == "CMU MoCap"]
    fig, ax = plt.subplots(figsize=(4.6, 6.6) if mobile else (6.6, 5.2))
    fig.subplots_adjust(left=.24 if mobile else .19, right=.98, top=.87, bottom=.17)
    y = np.arange(len(rows))[::-1]
    rotation = np.array([r["rotation_seconds"] for r in rows])
    shape = np.array([r["shape_seconds"] for r in rows])
    rot_color = COLORS["Ours"]
    shape_color = "#626fbc"
    ax.barh(y, rotation, height=.48, color=rot_color, zorder=3, label="Rotation")
    ax.barh(y, shape, left=rotation, height=.48, color=shape_color, zorder=3, label="Shape")
    for yi, r in zip(y, rows):
        total = r["total_seconds"]
        ax.text(total + .45, yi, f"{total:.2f}", va="center", color=FG,
                fontsize=11.5 if not mobile else 11.5, weight="bold")
        if not mobile:
            ax.text(r["rotation_seconds"]/2, yi, f"{r['rotation_seconds']:.2f}", ha="center",
                    va="center", color="#141720", fontsize=9.5, weight="bold")
            ax.text(r["rotation_seconds"] + r["shape_seconds"]/2, yi, f"{r['shape_seconds']:.2f}",
                    ha="center", va="center", color=FG, fontsize=9.5)
    ax.set_xlim(0, 21)
    ax.set_ylim(-.65, len(rows) - .25)
    ax.set_yticks(y, [r["sequence"] for r in rows])
    ax.set_xticks([0, 5, 10, 15, 20], ["0", "5", "10", "15", "20"])
    clean(ax, ticks=11.5 if mobile else 11.5)
    ax.set_xlabel("Rotation + shape runtime (seconds)", size=11.5, labelpad=14)
    ax.legend(ncol=2, frameon=False, loc="lower left", bbox_to_anchor=(-.02, 1.025),
              fontsize=11.5, handlelength=1.2, handleheight=.7, columnspacing=1.5, labelcolor=FG)
    save(fig, "stage-timing" + ("-mobile" if mobile else ""),
         "Our two-stage solver runtime on eight CMU MoCap sequences. Stacked segments show rotation recovery "
         "and shape recovery in seconds, and labels at the bar ends show total time. Linear axis starts at zero. "
         "Supplementary material Table 14, page 8. Drink: 8.51 plus 6.45 equals 14.96 seconds for 1,102 frames.")


def validate():
    for r in DATA["stage_breakdown"]:
        assert abs(r["rotation_seconds"] + r["shape_seconds"] - r["total_seconds"]) < 1e-8, r
    for m in ["BMM", "R-BMM", "OPM", "TSM", "Ours"]:
        rows = [r for r in DATA["mocap_shape"] if r["method"] == m]
        assert len(rows) == 8
        reference = next(r for r in DATA["mocap_shape_means"] if r["method"] == m)
        assert abs(mean(r["runtime_seconds"] for r in rows) - reference["mean_runtime_seconds"]) < 1e-8
        assert abs(mean(r["error_e3d"] for r in rows) - reference["mean_error_e3d"]) < 1e-8
    assert len(dense_rows()) == 12


def write_derived_csvs():
    """Export derived summaries from raw rows, not rounded displayed values."""
    means = []
    for method in ["BMM", "R-BMM", "OPM", "TSM", "Ours"]:
        rows = [r for r in DATA["mocap_shape"] if r["method"] == method]
        means.append({
            "method": method, "sequence_count": len(rows),
            "mean_error_e3d": mean(r["error_e3d"] for r in rows),
            "mean_runtime_seconds": mean(r["runtime_seconds"] for r in rows),
            "aggregation": "unweighted arithmetic mean of the eight Table 3 sequences",
            "source": "main-wacv.pdf", "page": 7, "table": 3,
        })
    data = dense_rows()
    ratios = [{
        "sequence": sequence,
        "opm_over_ours": data[sequence, "OPM"]["runtime_seconds"] / data[sequence, "Ours"]["runtime_seconds"],
        "tsm_over_ours": data[sequence, "TSM"]["runtime_seconds"] / data[sequence, "Ours"]["runtime_seconds"],
    } for sequence in SEQUENCES]
    for name, rows in [("mocap-shape-means-derived.csv", means),
                       ("dense-runtime-ratios-derived.csv", ratios)]:
        with (ROOT / "data" / name).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    validate()
    write_derived_csvs()
    (ROOT / "data/plot-data.js").write_text(
        "/* Generated from verified-paper-data.json by scripts/generate_plots.py. */\n"
        "window.NRSFM_PAPER_DATA = " + json.dumps(DATA, indent=2, ensure_ascii=False) + ";\n"
    )
    for small in (False, True):
        dense_runtime(small)
        dense_accuracy(small)
        mocap_tradeoff(small)
        stage_timing(small)
    print(f"Wrote 8 SVG plots and 8 PNG companions to {OUT}")
