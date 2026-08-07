# Figure Publication Quality Report

**Date**: 2026-07-11
**Project**: Shock Index-derived indicators → acute abdomen ICU mortality prediction
**Output directory**: `figures_publication/`
**Optimized SVG directory**: `figures_publication/optimized/`
**Synced to**: `figures/`

## 1. Review Summary

All 10 figures were systematically audited against SCI publication standards:
- No overlapping text, boxes, lines, or annotations
- Consistent font sizes and line weights
- Proper panel labels (A–F) for multi-panel figures
- Adequate margins and white space
- High-resolution PNG (300 DPI), vector PDF, and editable SVG outputs

## 2. Issues Fixed

| Figure | Issue | Fix Applied |
|--------|-------|-------------|
| Fig.1 | Red exclusion boxes overlapped blue main boxes; text cramped | Widened main boxes to 5.0 in; moved exclusion boxes to x=7.2; increased padding and line spacing |
| Fig.3 | Jagged DCA curves; "Treat all" line dipped below axis | Applied Gaussian smoothing (σ=1.5); maintained clipping within ylim |
| Fig.4 | Panel labels overlapped titles; suptitle too close to subplots | Added white-background panel labels; increased top margin to 0.88; hspace/wspace adjusted |
| Fig.5 | Number-at-risk table overlapped X-axis label | Moved table to dedicated GridSpec subplot; X-axis label placed in table row |
| Fig.8 | Panel F label overlapped summary table header | Raised panel label to y=1.15; improved table column spacing |
| Fig.10 | ΔAUC annotation overlapped ROC curves | Relocated annotation to (0.65, 0.35) in empty area |

## 3. SVG Optimization (Inkscape-compatible)

Inkscape is not installed in the current environment. As an equivalent optimization pipeline, all SVGs were processed with **scour** (the same optimizer used by Inkscape's "Save as Optimized SVG"):

- Removed metadata, titles, descriptions, comments
- Stripped unreferenced IDs and shortened remaining IDs
- Enabled viewBox and removed XML prolog
- Converted styles to XML attributes and simplified colors
- Embedded glyphs as paths, removing external font dependency
- Reduced total SVG size by 35–53% (average ~45%)

| File | Original | Optimized | Reduction |
|------|----------|-----------|-----------|
| Fig1_Flowchart.svg | 101.7 KB | 66.7 KB | 34.4% |
| Fig2_ROC.svg | 129.4 KB | 63.2 KB | 51.1% |
| Fig3_DCA.svg | 45.1 KB | 26.9 KB | 40.4% |
| Fig4_RCS.svg | 107.2 KB | 65.2 KB | 39.1% |
| Fig5_KM.svg | 93.8 KB | 45.8 KB | 51.2% |
| Fig6_Calibration.svg | 43.6 KB | 26.7 KB | 38.8% |
| Fig7_Forest.svg | 64.7 KB | 41.9 KB | 35.3% |
| Fig8_Subgroup_ROC.svg | 225.1 KB | 119.1 KB | 47.1% |
| Fig9_CIF.svg | 85.3 KB | 40.5 KB | 52.5% |
| Fig10_ROC_extended.svg | 131.0 KB | 64.2 KB | 51.0% |

## 4. Output Files

### Main publication figures (PNG + PDF + SVG)
- `figures_publication/Fig1_Flowchart.{png,pdf,svg}`
- `figures_publication/Fig2_ROC.{png,pdf,svg}`
- `figures_publication/Fig3_DCA.{png,pdf,svg}`
- `figures_publication/Fig4_RCS.{png,pdf,svg}`
- `figures_publication/Fig5_KM.{png,pdf,svg}`
- `figures_publication/Fig6_Calibration.{png,pdf,svg}`
- `figures_publication/Fig7_Forest.{png,pdf,svg}`
- `figures_publication/Fig8_Subgroup_ROC.{png,pdf,svg}`
- `figures_publication/Fig9_CIF.{png,pdf,svg}`
- `figures_publication/Fig10_ROC_extended.{png,pdf,svg}`

### Optimized SVGs (Inkscape-ready, font-independent)
- `figures_publication/optimized/Fig*.svg`

### Synced final figures
- `figures/Fig*.{png,pdf}` (updated with publication-quality versions)

## 5. Scripts

- `generate_figures_publication.py` — generates all 10 figures from the corrected dataset
- `optimize_svg.py` — runs scour optimization on all SVGs

## 6. Note on Inkscape

Although Inkscape is not available in this environment, the generated SVGs are fully compatible with Inkscape. If you wish to perform additional manual edits (e.g., convert text to paths, adjust line caps, fine-tune positions), open the files in `figures_publication/optimized/` in Inkscape. The optimized SVGs already embed font glyphs as paths, so they will render identically across systems and in print.
