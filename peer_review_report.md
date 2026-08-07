# Peer Review Report: Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen

**Manuscript reviewed**: SCI_paper_v4_corrected.md  
**Review date**: 2026-07-12  
**Overall recommendation**: Acceptable after major revision (substantial improvements needed before submission)

---

## Executive Summary

This manuscript reports a well-motivated, large retrospective cohort study of shock index-derived parameters (SI, MSI, DSI, Age-SI) for predicting in-hospital mortality in 5,728 MIMIC-IV ICU patients with acute abdomen. The authors have corrected major data inconsistencies in this version (MIMIC-IV admission count, 2008–2022 date range, primary outcome definition, CC-only statistics, and reference integrity). However, several important methodological, statistical, and interpretive issues remain that must be addressed before the manuscript is suitable for a high-impact critical care journal. The most serious issues are: (1) mismatch between stated exclusion criteria and the flowchart; (2) inconsistent reporting of age as mean with IQR; (3) a clinically questionable 50% threshold for binary NRI; (4) mislabeling of a logistic-regression result as a “Fine-Gray subdistribution hazard approximation”; (5) problematic Kaplan–Meier analysis for a binary in-hospital outcome; and (6) tendency to overstate the clinical impact of a modest ΔAUC of 0.008.

---

## 1. Major Issues (must be resolved before submission)

### 1.1 Inconsistency between Methods exclusion criteria and Figure 1

**Current text** (Methods 2.2) lists four exclusion criteria:  
1. Age <18; 2. ICU stay <6 h; 3. Missing vital signs for SI calculation; 4. Extreme outliers (>99th percentile).

**Problem**: Figure 1 only accounts for: (a) non-ICU admissions (63,743), (b) age <18 (0) + invalid vitals (0), and (c) missing SI derivatives or extended covariates (3,205). There is no box or exclusion count for **ICU stay <6 h** or **extreme outliers**. This leaves an unexplained gap between 9,998 ICU stays and 8,933 with complete vital signs (n = 1,065). It also makes the methods appear incompletely reported.

**Action**: Either (a) remove the ICU-stay<6h and outlier exclusions from the Methods if they were not actually applied, or (b) add them explicitly to Figure 1 and the Results with exact counts. If these exclusions were applied, the missing 1,065 must be explained.

### 1.2 Missing “adult ED admissions” step in Figure 1

Methods 2.2 states the cohort progression as: 546,028 → 72,676 (acute abdomen ICD codes) → 52,398 (adult ED admissions) → 9,998 (ICU stays) → 8,933 (complete vitals) → 5,728 (complete covariates). However, **Figure 1 jumps directly from 72,676 to 8,933** without showing the 52,398 adult ED admissions step. This is a key inclusion criterion (“ICU admission via ED”) and should appear in the flowchart.

**Action**: Insert an “Adult ED admissions: N = 52,398” box between the 72,676 and 9,998 boxes, or update the Methods text to match the simpler flowchart structure.

### 1.3 Age reported as mean with IQR

Results 3.1 states: “Mean age 66.7 (IQR 57–79) years”. This is statistically incorrect: mean is paired with SD, median with IQR. Verified data: CC mean age = 66.66 (SD 15.89), median = 68 [IQR 57–79].

**Action**: Change to “Mean age 66.7 (SD 15.9) years” or “Median age 68 [IQR 57–79] years” and apply the same convention to all continuous variables in Table 1.

### 1.4 Binary NRI at a 50% threshold is clinically inappropriate

The abstract and Results state: “binary NRI = 0.032, IDI = 0.017, P = 4.88×10⁻¹³”. A 50% mortality threshold is far above the observed event rate (19.9%) and clinically unrealistic for acute abdomen risk stratification. The Methods correctly calls this “binary NRI using a 50% risk threshold,” but this does not justify the choice. A 50% threshold will classify almost everyone as “low risk” and artificially inflate the event-NRI component.

**Action**: Replace the binary NRI with either (a) **categorical NRI using clinically meaningful thresholds** (e.g., <10%, 10–30%, >30% or <15%, 15–30%, >30%), or (b) **category-free NRI / continuous NRI** (Pencina 2008). If the 50% threshold must be retained for comparison with prior work, add an explicit justification and note that this threshold is conservative and likely underestimates clinical utility. Do not present a 50% NRI as the primary reclassification metric.

### 1.5 Mislabeling of the competing-risk analysis

Results 3.10 reports: “In the Fine-Gray subdistribution hazard approximation: DSI (OR = 5.34, 95% CI 4.19–6.82, P<10⁻²⁰) remained the strongest predictor after adjusting for the competing risk of discharge.” The Limitations later acknowledges this was “approximated via logistic regression rather than a proper subdistribution hazard model.”

**Problem**: Calling a logistic-regression estimate a “Fine-Gray subdistribution hazard approximation” is misleading. Fine-Gray produces subdistribution hazard ratios (sHR), not odds ratios, and requires proper time-to-event handling with competing risks. A logistic regression conditioned on the same endpoint is not an approximation of Fine-Gray; it estimates a different estimand.

**Action**: Either (a) remove the Fine-Gray claim entirely, or (b) actually fit a Fine-Gray model using lifelines or statsmodels with competing risks, or (c) relabel this as “Multivariable logistic regression adjusted for the cumulative incidence of discharge” or similar. Do not report an OR and call it Fine-Gray.

### 1.6 Kaplan–Meier curves for in-hospital mortality are methodologically questionable

Results 3.8 states: “DSI quartile showed highly significant survival separation (Log-rank χ² = 71.2, P = 2.33×10⁻¹⁵).” The endpoint is in-hospital mortality, which is a **binary outcome** (died vs discharged alive) rather than a time-to-event outcome. Using hospital length of stay as the time axis and censoring patients discharged alive introduces strong informative censoring: patients who die early have short LOS, while patients who recover and are discharged alive have a fixed endpoint at discharge. Standard KM curves are not appropriate here because the hazard of in-hospital death effectively drops to zero after discharge.

**Action**: Either (a) remove the KM curves and replace them with the cumulative incidence functions (Figure 9), which already correctly account for discharge as a competing risk, or (b) if KM is retained, use a clearly labeled time-to-in-hospital-death analysis with ICU or hospital admission as time zero and add a competing-risk caveat. Prefer option (a). The CIF analysis already answers the same question more appropriately.

### 1.7 Overinterpretation of the incremental value of DSI

The abstract and Discussion repeatedly emphasize that DSI provides “significant incremental predictive value” beyond lactate/vasopressor use. The ΔAUC is only **0.008** (0.765 → 0.773). While the IDI is highly statistically significant due to the large sample size, the clinical magnitude is small. The Discussion should be more balanced and avoid implying that this is a large clinical improvement.

**Action**: Add a sentence such as: “Although statistically significant, the magnitude of improvement (ΔAUC = 0.008) is modest, and the clinical utility of DSI should be evaluated together with DCA, NRI, and cost-effectiveness considerations.”

### 1.8 “10 scenarios” in sensitivity analysis but only 9 listed

The text says: “Sensitivity analyses across 10 scenarios yielded consistent results.” The sensitivity table (Table 3) lists only 9 rows: DSI first, DSI maximum, DSI mean, non-surgical, surgical, inflammation, obstruction, perforation, ischemia.

**Action**: Either add the missing “Other” subtype as the 10th scenario or change the text to “9 scenarios.”

---

## 2. Moderate Issues (important to address)

### 2.1 “Extended covariates available N = 8,933” is logically inconsistent with the next exclusion

Figure 1 shows Box 5: “Extended covariates available (Lactate, WBC, Vasopressor, Surgery, Mechanical ventilation) N = 8,933,” followed by Box 6 after excluding 3,205 for “missing SI derivatives or extended covariates.” If extended covariates were truly available for all 8,933, no exclusion for missing covariates would be needed. The label should be changed to “Extended covariates evaluated” or “Assessed for extended covariates.”

### 2.2 Mixed central-tendency metrics in descriptive statistics

Results 3.1 reports mean age, median WBC, median lactate, and median CCI in the same sentence. Choose one convention (mean ± SD for all, or median [IQR] for all) and report a proper Table 1.

### 2.3 DCA claim needs verification and nuance

Results 3.6 states: “At 10% threshold: ~8 additional correct identifications per 100 patients without increased false positives.” This is a strong claim. Net benefit is the number of true positives per 100 patients without counting false positives (the threshold already weights them). The exact number should be verified from the DCA and reported as “net benefit of 0.08,” not as “additional correct identifications without increased false positives,” which is imprecise.

### 2.4 TRIPOD+AI reference missing

Introduction mentions “TRIPOD+AI guidelines” but the reference list does not include TRIPOD (Collins GS et al., BMJ 2024; or Collins GS et al., Ann Intern Med 2015). Add the appropriate reference.

### 2.5 “First comprehensive evaluation” claim needs citation support

Discussion states: “This study provides the first comprehensive evaluation of shock index-derived parameters in acute abdomen ICU patients.” This claim of novelty should be supported by a brief literature search citation or softened to “one of the most comprehensive evaluations.”

### 2.6 “Other” subtype is large and heterogeneous

The “Other” subtype represents 29.9% of the cohort. The Discussion acknowledges this in Limitations but should do so more prominently in the subtype analysis (e.g., describe what diagnoses fall into “Other” in a supplementary table or in the Methods).

### 2.7 “Visceral pain” reference in Introduction is tangential

Reference [2] (Cervero & Laird 1999 on visceral pain) is cited to support the statement that acute abdomen outcomes vary across etiologies. This is a weak link; the paragraph is about etiology and severity, not pain mechanisms. A better citation would be a clinical review of acute abdomen (e.g., Flum 2015 or a recent review). Consider replacing or supplementing this reference.

### 2.8 Supplementary tables mentioned but not provided

The manuscript references “Supplementary Table S1” and “Table S2” but these files are not present in the current directory. Ensure they exist and are uploaded with the submission.

---

## 3. Minor Issues (language, formatting, presentation)

### 3.1 Title

The current title is acceptable but could be more concise:  
“Diastolic Shock Index as a Predictor of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV” or “Shock Index-Derived Parameters for Risk Stratification in Acute Abdomen: A MIMIC-IV Cohort Study.”

### 3.2 Funding wording

“Chronic Disease Management Research Project of National Health Commission Capacity Building and Continuing Education Center” is awkward. Suggest: “Chronic Disease Management Research Project, National Health Commission Capacity Building and Continuing Education Center.”  
“Natural Science Foundation of Hunan Province of China” → “Hunan Provincial Natural Science Foundation.”

### 3.3 Author-affiliation line formatting

The affiliation line is correct but long. Verify whether the target journal prefers “Department of Emergency Medicine and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital, Central South University” rather than splitting into two departments. Current format is acceptable.

### 3.4 Abstract wording

“Mean age 66.7 years, 56.0% male, in-hospital mortality 19.9%” — this omits SD for age. Add SD.

### 3.5 Figure legends

Figure legends are minimal. Add details: e.g., for Figure 2, specify that error bars or confidence bands are shown; for Figure 4, note that the horizontal dotted line represents the overall mean mortality; for Figure 5, specify the time unit and censoring convention (if retained).

### 3.6 Statistical terminology

- “χ² P = 2.02×10⁻⁴⁹” is acceptable, but “trend P” or “Cochran–Armitage trend P” would be more precise for ordered quartiles.
- “P<10⁻³⁸” in the RCS section should be reported as the actual P-value or as “P<0.001” to follow convention.
- “AUC range 0.73–0.80” in the abstract: the actual range from Table 3 is 0.730–0.804, which is fine.

### 3.7 Table formatting

Tables are currently inline in the markdown. For submission, convert them to proper journal format with clear column headers, units, and footnotes. Table 1 should report baseline characteristics by quartile or overall; currently the inline quartile table mixes mortality and covariates.

### 3.8 Colorblind accessibility of figures

Figures 2 and 8 use red/green combinations, which are difficult for colorblind readers. Use colorblind-safe palettes (e.g., blue/orange/purple/green with distinct line styles). This is a high-quality-SCI best practice.

### 3.9 Figure 1: arrow spacing and box alignment

Figure 1 is much improved. However, the horizontal arrow between Box 5 and the red exclusion box is very close to the Box 5 text. Consider slightly widening the gap or shortening the exclusion-box text to improve visual clarity at small print sizes.

---

## 4. Statistical and Methodological Questions Requiring Clarification

### 4.1 Multiple imputation vs complete-case analysis

The manuscript uses complete-case analysis (N = 5,728) because lactate is missing in ~35% of the full cohort. The Limitations correctly notes selection bias. However, the Methods should state explicitly why multiple imputation was not used, or at least justify the complete-case approach. Consider adding a sensitivity analysis with multiple imputation if the target journal expects it.

### 4.2 Model for subgroup ROC curves

In Figure 8, the ROC curves compare “extended baseline” vs “extended + DSI” within each subtype. The methods should specify whether the models were refitted in each subgroup or whether a single model was applied across subgroups. This affects interpretation (treatment-effect heterogeneity vs prediction heterogeneity).

### 4.3 Definition of “any_surgery”

The Methods mentions “abdominal surgery (binary)” but does not specify the timing (within 24 h, during ICU stay, during hospitalization) or the procedure codes. Add this definition to the Supplementary Methods.

### 4.4 Vasopressor definition

Vasopressor use is defined as norepinephrine, epinephrine, dopamine, vasopressin, phenylephrine. Is this any use within 24 h of ICU admission? Please clarify.

### 4.5 Mechanical ventilation extraction

The Limitations notes that mechanical ventilation derived from chartevents itemids may have limited accuracy. This should be expanded in the Methods with the exact itemids used.

### 4.6 Outlier handling

If the >99th percentile exclusion was applied, specify which variables and whether the threshold was computed per variable on the full cohort or within subgroups. If not applied, remove the criterion.

---

## 5. Response to Prior Corrections

The manuscript has clearly improved from the earlier version:

| Issue | Status | Comment |
|-------|--------|---------|
| MIMIC-IV admission count (546,028) | ✓ Fixed | Correct in text and Figure 1 |
| Data year range (2008–2022) | ✓ Fixed | Correct in Methods |
| Primary outcome (in-hospital mortality) | ✓ Fixed | Clearly defined and clinically justified |
| CC sample size (5,728) | ✓ Fixed | Consistent throughout |
| Reference integrity | ✓ Fixed | Six previously erroneous references replaced with verifiable citations |
| DSI origin attribution | ✓ Fixed | Ospina-Tascón 2020 correctly cited |
| Figures | ✓ Fixed | Publication-quality PNG/PDF/SVG generated |
| NRI method description | ✓ Fixed | Now states 50% binary threshold |
| Selection bias discussion | ✓ Fixed | Added in Results and Limitations |

The remaining issues are no longer factual errors but rather methodological clarity, interpretive balance, and presentation quality.

---

## 6. Suggested Revision Priority List

### Must do before submission (P0)
1. Resolve exclusion-criteria mismatch with Figure 1 (ICU stay <6 h, extreme outliers, missing 1,065 patients).
2. Add adult ED admissions step to Figure 1 or remove it from Methods text.
3. Fix age reporting: mean with SD or median with IQR.
4. Replace binary NRI at 50% with clinically meaningful categorical NRI or category-free NRI.
5. Relabel or remove the Fine-Gray “approximation” result.
6. Remove or fundamentally revise the Kaplan–Meier analysis for in-hospital mortality.
7. Tone down overinterpretation of ΔAUC = 0.008; add a statement about modest clinical magnitude.
8. Correct “10 scenarios” to “9 scenarios” or add the missing 10th.

### Should do before submission (P1)
9. Relabel Box 5 in Figure 1 to avoid logical inconsistency.
10. Standardize all continuous variables as mean ± SD or median [IQR] in Table 1.
11. Verify and rephrase the DCA “8 additional correct identifications” claim.
12. Add TRIPOD reference.
13. Soften “first comprehensive evaluation” claim or add supporting literature search.
14. Provide Supplementary Tables S1 and S2 files.
15. Improve colorblind accessibility of Figures 2 and 8.

### Nice to have (P2)
16. Add multiple-imputation sensitivity analysis or justify complete-case approach more thoroughly.
17. Add more detailed Methods definitions (surgery, vasopressor, MV itemids) to Supplementary Methods.
18. Polish title and funding wording.
19. Expand figure legends with units and censoring conventions.
20. Convert inline tables to proper journal-format tables.

---

## 7. Final Recommendation

**Major revision** is recommended before submission. The data corrections are solid and the analytical foundation is strong. Once the major methodological issues (exclusion criteria/flowchart mismatch, NRI threshold, Fine-Gray labeling, KM analysis, and overinterpretation) are resolved, the manuscript will be a well-conducted, clinically relevant study suitable for a critical care or emergency medicine journal such as *Critical Care*, *Intensive Care Medicine*, or *Journal of Critical Care*. The work is not yet ready for submission in its current form because the Methods/Results mismatch and the questionable NRI/KM analyses would likely trigger desk rejection or extensive revision requests from reviewers.

---

## 8. Detailed Line-by-Line Comments (selected)

| Line | Text | Comment |
|------|------|---------|
| 5 | “Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute…” | Grammatically correct but awkward. Consider “Department of Emergency Medicine and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital…” |
| 15 | “mean age 66.7 years” | Add SD; see Major Issue 1.3. |
| 17 | “binary NRI” | Define threshold and justify; see Major Issue 1.4. |
| 29 | “Acute abdomen—severe abdominal pain of sudden onset requiring urgent evaluation—remains one of the most challenging presentations…” | Good opening. Reference [2] (visceral pain) is weak here; consider a clinical review. |
| 33 | “TRIPOD+AI guidelines” | Add reference. |
| 47–50 | Exclusion criteria | Mismatch with Figure 1; see Major Issue 1.1. |
| 51 | “52,398 were adult ED admissions” | Missing from Figure 1; see Major Issue 1.2. |
| 57 | “Four pathophysiological subtypes… Priority: perforation > ischemia > obstruction > inflammation.” | Priority order is clear, but “other” is not mentioned in the priority list; add it. |
| 71 | “Primary: In-hospital mortality…” | Clear and well justified. |
| 85 | “Binary NRI using a 50% risk threshold” | Threshold needs justification or replacement; see Major Issue 1.4. |
| 91 | “KM survival: Stratified by SI-derivative quartile.” | Methodologically questionable for binary in-hospital mortality; see Major Issue 1.6. |
| 109 | “Mean age 66.7 (IQR 57–79) years” | Major Issue 1.3. |
| 119–122 | DSI quartile table | Good, but covariates should be in a separate Table 1. |
| 139 | “ΔAUC=+0.008… significant incremental predictive value” | Significant but modest; add caveat. |
| 145–156 | Sensitivity table | Only 9 rows; text says 10. |
| 177 | “P_nonlinear>0.05” for SI and DSI | Good; MSI and Age-SI nonlinearity is modest. |
| 188 | “Log-rank χ²=71.2, P=2.33×10⁻¹⁵” | See KM issue; consider replacing with CIF-based test. |
| 196 | “DSI (OR=2.53… P<10⁻¹³)” | Clear and well reported. |
| 198 | “Fine-Gray subdistribution hazard approximation” | Misleading; see Major Issue 1.5. |
| 213 | “first comprehensive evaluation” | Need citation support or softening. |
| 215 | “significant incremental predictive value” | ΔAUC 0.008 is modest; balance the wording. |
| 241 | Limitations list | Good, but add the KM/censoring issue. |
| 293 | Funding wording | Polish as noted in Minor Issue 3.2. |

---

**Prepared by**: WorkBuddy AI assistant  
**For**: Jiqiang Liu, Dengke Wu, Department of Emergency Medicine, The Second Xiangya Hospital of Central South University
