# No Cones, No Duals

Project website for **No Cones, No Duals: A Fast and Scalable Solver for NRSfM**.

**Author:** Suryansh Kumar  
**Publication:** Accepted at the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), 2027.

This is a portable, editable static website. It uses HTML, CSS, and JavaScript;
there is no npm installation, framework, build step, database, or server code.
The website can be hosted on GitHub Pages or another static web host.

## Open the website

Extract the ZIP and open `index.html` in a browser.

For a local web server, open a terminal inside the extracted website folder and run:

```bash
python3 -m http.server 8000
```

Then visit [http://localhost:8000](http://localhost:8000).
Press **Ctrl+C** in that terminal to stop the server.

The page text, styling, scripts, author-supplied diagrams, scientific figures,
redrawn plots, source data, fonts, and both PDFs are bundled.
The linked YouTube video requires an internet connection. An optional embedded player is also supported; see “Video playback” below.

## Folder guide

| File or folder | Purpose |
| --- | --- |
| `index.html` | Page structure, scientific text, author details, section headings, resource links, and accessibility labels. |
| `assets/css/styles.css` | Colors, typography, spacing, responsive layouts, and visual styling. |
| `assets/css/hero-method.css` | Opening section and presentation of the two author-supplied stage diagrams. |
| `assets/css/results.css` | Results layout, plot controls, and exact-value tables. |
| `assets/js/main.js` | Page interactions, figure controls, navigation, video behavior, and citation copying. |
| `assets/js/plots.js` | Plot metric tabs and accessible tables of the numerical values. |
| `assets/images/` | Author-supplied stage diagrams and qualitative research figures. |
| `assets/plots/` | Newly drawn SVG charts, with desktop and mobile layouts. PNG companions are optional preview files. |
| `data/verified-paper-data.json` | Canonical chart data, with source tables, pages, units, and timing scopes. |
| `data/plot-data.js` | Generated browser copy of the JSON; supports local-file browsing without fetching data. |
| `data/*.csv`, `data/PROVENANCE.md` | Numerical transcriptions, derived summaries, and source notes. |
| `scripts/generate_plots.py`, `scripts/requirements.txt` | Optional Python workflow to regenerate the plots and browser data after edits. |
| `assets/fonts/` | Locally bundled fonts and their licenses, when present. |
| `assets/papers/main-wacv.pdf` | Main paper supplied for this website. |
| `assets/papers/supp-wacv.pdf` | Supplementary material supplied for this website. |
| `citation.bib` | Downloadable BibTeX citation. |
| `docs/ASSET_SOURCES.md` | Sources and provenance of figures and other assets. |
| `.nojekyll` | Tells GitHub Pages to serve this static site without Jekyll processing. |
| `README.md` | This editing and hosting guide. |

## Publish on GitHub Pages

1. Create a GitHub repository, for example `no-cones-no-duals`.
2. Upload the **contents** of the extracted website folder to the repository's
   `main` branch. Put `index.html` directly at the repository root, alongside
   `assets/`, `citation.bib`, and `.nojekyll`.
3. Open the repository's **Settings → Pages**.
4. Under **Build and deployment → Source**, select **Deploy from a branch**.
5. Select the **main** branch and **/(root)** folder, then click **Save**.
6. Use the published website URL shown in the Pages settings.

For a project repository, the address normally has this form:

```text
https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/
```

Keep `.nojekyll` when uploading; it may be hidden in your file manager.
GitHub Pages supports public repositories on GitHub Free. Availability for
private repositories depends on the GitHub plan.

Official instructions:

- [Configure a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Create a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

## Edit the page

**Text and links:** Edit `index.html`. Its sections contain the main scientific
content. Update the displayed citation and `citation.bib` together if the
publication metadata changes.

**Appearance:** Edit `assets/css/styles.css` for the overall theme,
`assets/css/hero-method.css` for the opening section, and
`assets/css/results.css` for results and chart controls.

The theme uses a nearly black background, white headings, charcoal surfaces,
and a restrained blue-lilac accent. The main palette is defined in `:root`:
`--paper`, `--surface`, `--ink`, `--muted`, `--line`, and `--accent`.
Desktop and mobile layouts are organized in labeled CSS sections and media queries.

**Figures:** Replace or add files in `assets/images/` and update their references,
captions, and alternative text. Figure controls may also reference images in
`assets/js/main.js`. Keep source notes current in `docs/ASSET_SOURCES.md`.

The opening diagrams are `assets/images/first-stage.png` and
`assets/images/second-stage.png`, supplied by the author. Their PNG files are
unchanged. The `.stage-panel-image img` rule in `hero-method.css` uses
`filter: invert(1) hue-rotate(180deg)` and `mix-blend-mode: screen` to adapt
their on-screen colors to the dark theme. The enlarged viewer opens the
unfiltered originals. Remove those two CSS properties to display the original
colors in the opening section too.

**Video:** Search `index.html` and `assets/js/main.js` for the supplied YouTube
video ID, `NO25k2dfSFE`, when replacing the linked demonstration.

**Paper files:** Replace the PDFs in `assets/papers/` while retaining their
filenames, or update all corresponding links if you rename them.

Use relative paths such as `assets/images/figure.webp`. Avoid paths beginning
with `/assets/`, which point to the domain root and can break a GitHub project site.

## Edit data and regenerate plots

The statistics are fresh plots of the numerical tables, rather than screenshots
or digitized coordinates from the paper. SVGs remain sharp when enlarged;
the `-mobile.svg` variants provide layouts for narrow screens.

1. Edit **`data/verified-paper-data.json`**, preserving its source, units, and
   runtime-scope fields. Update the corresponding CSVs and derived summaries
   when source values change; `data/PROVENANCE.md` explains each dataset.
2. To change chart colors, fonts, labels, or layout, edit
   **`scripts/generate_plots.py`**.
3. From the website folder, run:

   ```bash
   python3 -m pip install -r scripts/requirements.txt
   python3 scripts/generate_plots.py
   ```

4. Check the regenerated plots and exact-value tables in the browser, then
   upload the updated files to your host.

The script checks stage sums and arithmetic means, then writes eight SVGs,
PNG previews, the two derived CSV summaries, and `data/plot-data.js`. Edit the canonical JSON rather than the
generated JavaScript. Python and its plotting packages are needed only to
regenerate figures; serving the finished website needs no installation or build.

| Plot | Source and interpretation |
| --- | --- |
| `dense-runtime` | Main p.7, Table 5: overall solver runtime for Ours, OPM, and TSM across four dense face sequences; shared logarithmic axis. |
| `dense-accuracy` | Main p.7, Table 5: normalized 3D error for the same three methods; linear axis. All source-table methods remain in the data. |
| `mocap-tradeoff` | Main p.7, Table 3: unweighted arithmetic mean of shape-stage runtime and normalized 3D error across eight sequences for each method. |
| `stage-timing` | Supplement p.8, Table 14: our rotation and shape times on eight MoCap sequences, with combined totals. |

Preserve the distinction between **shape-stage** and **overall** runtime.
Times are the paper's reported measurements; implementations and hardware
vary across comparisons. Missing runtimes remain unavailable. Sequence frame
and point counts are metadata, not a controlled scaling sweep.
See `docs/ASSET_SOURCES.md` and `data/PROVENANCE.md` for details.

## Check before publishing changes

- Open the page at both desktop and phone widths.
- Check navigation, figure controls, video playback, and citation copying.
- Confirm both PDF links open and the downloadable citation is current.
- Check that figures remain sharp and readable, with accurate captions.
- Verify that edits preserve keyboard navigation and visible focus indicators.

## Rights and licenses

The paper, supplementary material, and scientific figures retain their existing
author and publisher rights; including them in this website does not relicense
them. Third-party fonts and other third-party assets retain their own licenses.
Keep any bundled license and attribution files when redistributing the website.

## Video playback

The supplied YouTube video currently reports that playback on other websites
is disabled by its owner. The demo poster therefore opens the video directly
on YouTube in a new tab. This keeps the page usable with the current settings.

After allowing embedding for the video on YouTube, change `data-embed="false"`
to `data-embed="true"` on the `play-demo` link in `index.html`. The existing
JavaScript will then load the privacy-enhanced player when a visitor selects
the poster. No API key is needed. You can also change the poster subtitle to
`RECONSTRUCTION DEMONSTRATION` at that point.
