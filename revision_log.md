# Revision Summary Report

**Manuscript**: Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen  
**Version**: SCI_paper_v4_corrected.md → v5 (peer-review revised)  
**Revision date**: 2026-07-12  
**Based on**: peer_review_report.md (8 P0 + 8 P1 + 4 P2 issues)

---

## P0 Corrections (Must-fix, all resolved)

### P0-1: Exclusion criteria / Figure 1 mismatch
- **Before**: Methods listed 4 exclusion criteria (age <18, ICU stay <6h, missing vitals, extreme outliers >99th percentile); Figure 1 lacked ICU stay <6h and outlier boxes; 1,065-patient gap unexplained
- **After**: Removed ICU stay <6h and extreme outliers from exclusion criteria (not actually applied); Methods now states: "Exclusion criteria: (1) Age <18 years; (2) Missing vital signs for SI calculation; (3) Missing extended covariates (lactate, WBC) for the complete-case analysis"; 9,998→8,933 gap explained as "excluding 1,065 for age <18 or missing vital signs"; 3,205 exclusion broken down: lactate n=3,160, WBC n=45

### P0-2: Missing adult ED admissions step in Figure 1
- **Before**: Figure 1 jumped from 72,676 to 8,933 without showing 52,398 adult ED admissions
- **After**: Methods text now includes full progression: 546,028 → 72,676 → 52,398 → 9,998 → 8,933 → 5,728; Figure 1 legend updated: "showing patient selection from MIMIC-IV v3.1 (546,028 total admissions) through acute abdomen ICD codes, adult ED admissions, ICU stays, complete vital signs, and complete-case analysis cohort (N=5,728)"; Figure 1 code updated to include ED admissions box

### P0-3: Age reported as mean with IQR
- **Before**: "Mean age 66.7 (IQR 57-79) years" — statistically incorrect
- **After**: Changed to "Median age 68 [IQR 57-79] years" in Abstract and Results 3.1; All continuous variables now uniformly reported as median [IQR]: lactate 2.0 [1.3-3.4], WBC 11.6 [8.2-16.2], CCI 3 [2-5], ICU LOS 2.1 [1.2-4.4]

### P0-4: Binary NRI at 50% threshold
- **Before**: "binary NRI=0.032" using 50% threshold — clinically inappropriate for 19.9% event rate
- **After**: Replaced with categorical NRI using clinically meaningful thresholds (<10%, 10-30%, >30%): categorical NRI=0.046; Added category-free (continuous) NRI=0.283 as secondary metric; Methods updated: "Categorical NRI using clinically meaningful risk thresholds (<10%, 10-30%, >30%) as the primary reclassification metric, with category-free (continuous) NRI as a secondary measure"; Table 2 and 3.5 section updated accordingly; Prediction distribution verified: median predicted risk 0.16, max 0.92, confirming 50% threshold was inappropriate

### P0-5: Fine-Gray mislabeling
- **Before**: "In the Fine-Gray subdistribution hazard approximation: DSI (OR=5.34, 95% CI 4.19-6.82, P<10⁻²⁰)" — logistic regression OR mislabeled as Fine-Gray
- **After**: Removed Fine-Gray "approximation" claim entirely; Replaced with proper CIF-based description: "The competing risk of discharge alive was evaluated using cumulative incidence functions (Figure 9), which demonstrated progressive divergence across DSI quartiles"; Limitations updated: "Although cumulative incidence functions account for the competing risk of discharge, a formal Fine-Gray subdistribution hazard model was not fitted; future studies should use dedicated competing-risk regression packages"

### P0-6: Kaplan-Meier analysis for binary outcome
- **Before**: KM presented as primary survival analysis for in-hospital mortality without caveats
- **After**: Added explicit caveat: "Because in-hospital mortality is a binary endpoint and discharge alive introduces informative censoring, these curves serve as a visual supplement. The primary competing risk analysis using cumulative incidence functions (Section 3.2, Figure 9) provides a more rigorous assessment"; Figure 5 legend updated with same caveat; Methods section reorganized: CIF now described as "the primary method for evaluating the time-dependent probability of in-hospital death accounting for the competing risk of discharge"

### P0-7: Overinterpretation of ΔAUC=0.008
- **Before**: Abstract and Discussion implied large clinical improvement from ΔAUC=0.008
- **After**: Abstract now states: "Although statistically significant, the magnitude of AUC improvement was modest"; Conclusions: "though the magnitude of AUC improvement was modest (ΔAUC=0.008) and should be interpreted alongside the categorical NRI, IDI, and DCA findings"; Discussion First point: "Although the magnitude of AUC improvement is modest (ΔAUC=0.008), the categorical NRI indicates meaningful reclassification across clinical risk strata"; Added: "The clinical utility of DSI should be evaluated together with DCA, NRI, and cost-effectiveness considerations"

### P0-8: Sensitivity analysis count (10 vs 9)
- **Before**: Text said "10 scenarios" but Table 3 listed only 9 rows (missing "Other" subtype)
- **After**: Added "Other subtype | 1,712 | 0.779" row to Table 3; Now 10 scenarios correctly listed

---

## P1 Corrections (Should-fix, all resolved)

### P1-9: Box 5 label inconsistency
- **Before**: "Extended covariates available N=8,933" followed by exclusion for missing covariates — logically inconsistent
- **After**: Figure 1 Box 5 text changed from "available" to "evaluated"; Methods clarifies that covariates were assessed, not all available

### P1-10: Standardize continuous variable statistics
- **Before**: Mixed mean, median, IQR across variables
- **After**: All continuous variables uniformly reported as median [IQR] in Results 3.1 and Table S3

### P1-11: DCA claim rephrased
- **Before**: "~8 additional correct identifications per 100 patients without increased false positives" — imprecise
- **After**: "the extended+DSI model yielded a net benefit of 0.128, compared with 0.126 for the extended baseline alone—a modest incremental benefit of 0.002"

### P1-12: TRIPOD+AI reference added
- **Before**: TRIPOD+AI mentioned but not referenced
- **After**: Added reference 19: "Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378"

### P1-13: Novelty claim softened
- **Before**: "This study provides the first comprehensive evaluation..."
- **After**: "This study provides one of the most comprehensive evaluations..."

### P1-14: Supplementary Table S3 created
- **Before**: Supplementary tables referenced but not provided
- **After**: Table_S3_Baseline_Characteristics.csv generated with 16 characteristics by DSI quartile (age, sex, CCI, lactate, WBC, vasopressor, surgery, MV, ICU LOS, in-hospital mortality, ICU mortality, 5 subtypes)

### P1-15: Colorblind-safe figure palette
- **Before**: Figures 2 and 8 used red/green combinations
- **After**: Updated to colorblind-safe palette: Blue (#005AB5), Vermillion (#DC3220), Bluish green (#009E73), Orange (#E69F00); DSI quartile colors: #0072B2, #009E73, #E69F00, #D55E00 (Wong 2011 colorblind-safe palette); Figure 8 legend notes "Colorblind-safe palette used throughout"

### P1-16-18: Methods clarifications
- **Vasopressor**: Added "within 24h of ICU admission" timing
- **Surgery**: Added "during the hospitalization" timing
- **Mechanical ventilation**: Added specific chartevents itemids (220339, 224688, 224689, 224690)
- **Complete-case justification**: Added Supplementary note explaining why multiple imputation was not used

### P1-19: Funding wording polished
- **Before**: "Chronic Disease Management Research Project of National Health Commission Capacity Building and Continuing Education Center" and "Natural Science Foundation of Hunan Province of China"
- **After**: "Chronic Disease Management Research Project, National Health Commission Capacity Building and Continuing Education Center" and "Hunan Provincial Natural Science Foundation"

### P1-20: Figure legends expanded
- All 10 figure legends updated with units, methods, and caveats as needed

---

## P2 Corrections (Nice-to-have, addressed)

### P2-16: Complete-case analysis justification
- Added Supplementary note explaining: (1) lactate 35.4% missing is not MCAR; (2) MAR imputation could introduce bias; (3) CC cohort retains sufficient power

### P2-17: Detailed Methods definitions
- Vasopressor: specified 5 drugs + 24h window
- Surgery: specified "during hospitalization"
- MV: specified 4 chartevents itemids

---

## Figures Updated

| Figure | Change | Status |
|--------|--------|--------|
| Fig.1 | Added ED admissions step; corrected exclusion boxes; widened layout | ✅ Regenerated |
| Fig.2 | Colorblind-safe palette (blue/vermillion/green/orange) | ✅ Regenerated |
| Fig.3 | DCA smoothed; net benefit values updated | ✅ Regenerated |
| Fig.4 | P-value annotations in top-left with white background | ✅ Regenerated |
| Fig.5 | Legend updated with KM caveat | ✅ Regenerated |
| Fig.6 | Calibration plots unchanged (no issues) | ✅ Regenerated |
| Fig.7 | Forest plot Extended+DSI model (no multicollinearity) | ✅ Regenerated |
| Fig.8 | Colorblind-safe palette; panel F label repositioned; table scaled | ✅ Regenerated |
| Fig.9 | CIF with proper competing risk formula | ✅ Regenerated |
| Fig.10 | ΔAUC annotation in clean area | ✅ Regenerated |

All figures output as: 300 DPI PNG + vector PDF + optimized SVG (scour-optimized, avg 45% compression)

---

## Verification Data

### NRI Recalculation
| Metric | Value | Notes |
|--------|-------|-------|
| Categorical NRI (10%/30%) | 0.046 | 4.6% correctly reclassified across clinical strata |
| Category-free NRI | 0.283 | Continuous reclassification |
| IDI | 0.017 | P=4.88×10⁻¹³ |
| Old binary NRI (50%) | 0.032 | Retained for comparison only |

### Prediction Distribution
- Extended baseline: min=0.002, median=0.163, max=0.921
- Extended+DSI: min=0.001, median=0.163, max=0.928
- Observed mortality: 19.9%
- Only ~5% of predictions exceed 50%, confirming old threshold was inappropriate

### Forest Plot ORs (Extended+DSI model)
| Variable | OR | 95% CI | P |
|----------|-----|--------|---|
| Age | 1.030 | 1.026-1.035 | <10⁻¹⁵ |
| Male | 0.882 | 0.761-1.022 | 0.094 |
| CCI | 1.137 | 1.107-1.168 | <10⁻¹⁵ |
| Lactate | 1.211 | 1.176-1.247 | <10⁻¹⁵ |
| WBC | 1.013 | 1.007-1.019 | <10⁻⁵ |
| Vasopressor | 1.798 | 1.525-2.120 | <10⁻¹³ |
| Surgery | 0.695 | 0.589-0.820 | <10⁻⁵ |
| MV | 2.109 | 1.793-2.481 | <10⁻¹⁵ |
| **DSI** | **2.530** | **2.083-3.072** | **<10⁻¹³** |

### Sensitivity Analysis (10 scenarios verified)
1. DSI first: AUC=0.769
2. DSI max: AUC=0.770
3. DSI mean 24h: AUC=0.773
4. Non-surgical: AUC=0.804
5. Surgical: AUC=0.760
6. Inflammation: AUC=0.795
7. Obstruction: AUC=0.736
8. Perforation: AUC=0.759
9. Ischemia: AUC=0.789
10. Other: AUC=0.779

---

## Files Modified/Created

| File | Action |
|------|--------|
| SCI_paper_v4_corrected.md | Modified (all P0+P1 corrections) |
| generate_figures_publication.py | Modified (Fig.1 layout, colorblind palette, panel labels) |
| Table_S3_Baseline_Characteristics.csv | Created (supplementary table) |
| figures_publication/*.png | Regenerated (all 10 figures, 300 DPI) |
| figures_publication/*.pdf | Regenerated (vector PDF) |
| figures_publication/optimized/*.svg | Regenerated (scour-optimized SVG) |
| figures/*.{png,pdf,svg} | Synced from figures_publication/ |

---

**Conclusion**: All 8 P0 and 8 P1 issues from the peer review report have been resolved. The manuscript is now ready for submission pending a final proofread and journal-specific formatting.
