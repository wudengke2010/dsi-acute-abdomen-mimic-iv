# Figure Quality Validation Report

**Project**: Shock Index-derived indicators for predicting in-hospital mortality in acute abdomen ICU patients  
**Date**: 2026-07-09 (updated 2026-07-09 after box-size/spacing refinements)
**Outcome**: In-hospital mortality (`hospital_expire_flag`) in complete-case cohort (N=5,728)  
**Figure directory**: `shock_index_abdomen/figures/`  
**DPI**: 300 for all PNG/PDF outputs

---

## Summary

All 10 figures were regenerated using the corrected dataset (`analysis_dataset_corrected.csv`) and the primary outcome of **in-hospital mortality**. The previous critical issues have been resolved:

| Issue | Status |
|---|---|
| Outcome labels ("ICU Mortality" → "In-Hospital Mortality") | ✅ Fixed in Figs 2, 3, 5, 6, 7, 8, 9, 10 |
| Fig1 missing final CC cohort box | ✅ Added N=5,728 final box |
| Fig4 RCS flat curves | ✅ Corrected; now shows clear dose-response |
| Fig7 forest plot multicollinearity | ✅ Changed to Extended+DSI model only |
| Fig8 missing subtypes | ✅ Now includes inflammation, obstruction, perforation, ischemia, other |
| Fig9 CIF >100% | ✅ Corrected formula; Y-axis capped at 40% (max ~32%) |
| Fig2/Fig3/Fig6/Fig10 based on old data | ✅ Regenerated with corrected dataset |
| Text/data overlaps | ✅ Fixed: Fig1 box-arrow spacing tightened and final box widened/taller; Fig4 P-value boxes relocated to top-left |

---

## Figure-by-Figure Validation

### Figure 1. Patient Selection Flowchart
- **Size**: 1687×2218 px
- **Layout**: Vertical flowchart with explicitly sized boxes; main boxes widened to 4.2 units, final green box widened to 4.6 units and height 1.8 units; uniform arrow spacing (0.40 units) between boxes
- **Content**: Complete from MIMIC-IV N=546,028 → acute abdomen N=72,676 → ICU N=8,933 → complete vitals N=8,933 → extended covariates N=8,933 → final complete-case cohort **N=5,728**
- **Exclusions**: Non-ICU (63,743), age<18 (0), invalid vitals (0), missing SI/covariates (3,205)
- **Overlaps**: None; main boxes, exclusion boxes, and connecting arrows are clearly separated
- **Readability**: Excellent
- **Status**: ✅ Pass

### Figure 2. ROC Curves for In-Hospital Mortality Prediction
- **Size**: 1615×1407 px
- **AUCs displayed**: Basic baseline 0.626 [0.609-0.643]; Extended baseline 0.765 [0.749-0.780]; Extended+DSI 0.773 [0.758-0.787]; Extended+all SI 0.774 [0.760-0.789]
- **Legend**: Lower right, no overlap with curves
- **Axis labels**: Clear
- **Overlaps**: None
- **Status**: ✅ Pass

### Figure 3. Decision Curve Analysis for In-Hospital Mortality
- **Size**: 1716×1407 px
- **Curves**: Basic baseline, Extended baseline, Extended+DSI, Treat all, Treat none
- **Y-axis**: Net Benefit, -0.05 to 0.15
- **X-axis**: Threshold probability 0.05 to 0.80
- **Legend**: Upper right, clear
- **Overlaps**: None
- **Status**: ✅ Pass

### Figure 4. Restricted Cubic Spline Analysis of SI Derivatives
- **Size**: 2969×2367 px
- **Layout**: 2×2 grid
- **Y-axis range**: 0 to 0.50 (predicted probability of in-hospital mortality)
- **Reference line**: 19.9% (observed in-hospital mortality)
- **Dose-response**: Clear monotonic increasing relationships for SI, MSI, DSI, Age-SI
- **P-values**: Annotated in each panel, moved to top-left corner to avoid overlap with curves; displayed as P < 1.0×10⁻³ for overall effect and P nonlinear to 3 decimals
- **Overlaps**: None; P-value annotations no longer overlap with spline curves
- **Status**: ✅ Pass

### Figure 5. Kaplan-Meier Curves by DSI Quartile (In-Hospital Survival)
- **Size**: 1630×1472 px
- **Y-axis**: In-hospital survival probability 0.5 to 1.0
- **X-axis**: Hospital LOS 0 to 30 days
- **Log-rank P**: **P < 0.001** (corrected from previous 1.00)
- **Curves**: Clear separation Q1 (highest survival) → Q4 (lowest survival)
- **Legend**: Lower left, no overlap
- **Overlaps**: None
- **Status**: ✅ Pass

### Figure 6. Calibration Plot for In-Hospital Mortality Models
- **Size**: 1502×1407 px
- **Models**: 4 models with distinct colors (blue, red, green, purple)
- **Perfect calibration**: Dashed diagonal line
- **Axis**: Equal aspect, 0 to 0.50
- **Overlaps**: None
- **Status**: ✅ Pass

### Figure 7. Forest Plot: Extended Baseline + DSI Model
- **Size**: 2395×1770 px
- **Model**: Extended+DSI (avoids multicollinearity of all 4 SI derivatives)
- **X-axis**: Odds Ratio 0 to 3.5
- **Reference line**: OR=1
- **Variables**: Age, Male sex, CCI, Lactate, WBC, Vasopressor, Surgery, Mechanical ventilation, DSI
- **Labels**: OR and 95% CI on right of each error bar; no overlap
- **Status**: ✅ Pass

### Figure 8. Subgroup ROC Analysis by Acute Abdomen Subtype
- **Size**: 3567×2367 px
- **Layout**: 2×3 grid (5 subtypes + 1 empty panel)
- **Subtypes included**: Inflammation, Obstruction, Perforation, Ischemia, Other
- **Each panel**: Extended+DSI (solid) vs Extended baseline (dashed) with AUCs
- **Legend**: Within each panel, readable
- **Overlaps**: None
- **Status**: ✅ Pass

### Figure 9. Cumulative Incidence Function by DSI Quartile
- **Size**: 1654×1472 px
- **Y-axis**: Cumulative incidence of in-hospital death, 0 to 0.40
- **X-axis**: Hospital LOS 0 to 30 days
- **Curves**: Q1 (~11%), Q2 (~14%), Q3 (~20%), Q4 (~32%) plateau values
- **Title**: Correctly states competing risk (in-hospital death vs discharge alive)
- **Overlaps**: None
- **Status**: ✅ Pass

### Figure 10. ROC Curves: Incremental Value of DSI over Extended Baseline
- **Size**: 1610×1472 px
- **AUCs**: Basic 0.626; Extended 0.765 [0.750-0.780]; Extended+DSI 0.773 [0.758-0.788]; Extended+all SI 0.774 [0.759-0.788]
- **Title**: Corrected to in-hospital mortality
- **Legend**: Lower right, clear
- **Overlaps**: None
- **Status**: ✅ Pass

---

## Technical Notes

1. **Dataset**: All figures use `analysis_dataset_corrected.csv` with `hospital_expire_flag` as primary outcome.
2. **Sample size**: Complete-case N=5,728; in-hospital mortality 19.9% (1,141 deaths).
3. **CIF correction**: Formula now correctly applies overall survival product: CIF(t) = Σ(d_j/n_j) × S(t_j−).
4. **Log-rank test**: Computed with `lifelines.statistics.multivariate_logrank_test`; P = 2.33×10⁻¹⁵.
5. **Forest plot**: Switched from full model with 4 collinear SI derivatives to the primary Extended+DSI model.
6. **Color palette**: Consistent, distinguishable, colorblind-friendly.

---

## Conclusion

All 10 figures meet high-quality SCI journal standards. No text-text or text-data overlaps were detected. Layouts are clean, labels are readable, and all scientific content is consistent with the corrected dataset and primary outcome (in-hospital mortality).
