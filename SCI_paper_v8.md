# Diastolic Shock Index as an Independent Predictor of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation

**Yuzhong Cai** [1]†, **Jiqiang Liu** [1], **Dengke Wu** [1,2]*

ORCID Yuzhong Cai: 0009-0004-3425-3898; ORCID Jiqiang Liu: 0009-0000-9884-3089; ORCID Dengke Wu: 0000-0003-4101-8461

[1] Department of Emergency Medicine, Second Xiangya Hospital, Central South University, Changsha 410011, Hunan, China

[2] Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha, China

† First author: Yuzhong Cai, MD, Email: caiyuzhong@csu.edu.cn

* Corresponding author: Dengke Wu, MD, PhD, Department of Emergency Medicine, Second Xiangya Hospital, Central South University, 139 Renmin Middle Road, Changsha 410011, Hunan, China. Email: wudk2010@csu.edu.cn

---

## Abstract

**Background**: Shock index (SI) derivatives predict mortality in trauma and sepsis but are unexplored in acute abdomen. We evaluated SI-derived parameters for in-hospital mortality prediction, assessing diastolic shock index (DSI) as an independent bedside predictor.

**Methods**: Retrospective cohort from MIMIC-IV v3.1 (2008–2022). Adult ICU patients with acute abdomen ICD codes were included; SI/MSI/DSI/Age-SI were calculated from 24-hour vital signs. Primary outcome: in-hospital mortality. The primary model excluded surgery (survivorship bias), incorporating age, sex, CCI, lactate, WBC, vasopressor, ventilation, and SOFA. Performance was assessed via AUC/DeLong, NRI/IDI, DCA, calibration, bootstrap validation, multiple imputation (N=8,933), 14 sensitivity analyses, and E-values. Component decomposition tested whether isolated HR/DBP replicated DSI's predictive value. External validation used eICU-CRD v2.0 (N=5,755, 208 hospitals).

**Results**: Among 5,728 complete-case ICU stays (median age 68, 56.0% male, in-hospital mortality 19.9%), all four SI derivatives showed comparable discrimination (AUCs 0.635–0.651), and DSI was advanced to full evaluation. Extended baseline (no surgery) AUC=0.785; adding DSI yielded AUC=0.790 (ΔAUC=0.005, DeLong P=0.012). DSI was an independent predictor (OR=2.18, 95% CI 1.79–2.65, P=7.59×10⁻¹⁵). Isolated HR (AUC=0.571) and DBP (AUC=0.597) were poor predictors, while DSI (AUC=0.644) significantly outperformed both (DeLong P<0.001). Within matched DBP or HR quintiles, DSI tertile consistently stratified mortality (DBP Q3: 12.0%→18.8%→32.5%). ΔAUC was below clinical relevance thresholds (≥0.02), and categorical NRI crossed zero (0.008, 95% CI −0.009 to 0.044). However, category-free NRI (0.252, P<0.001) and IDI (0.013, P<0.001) were significant, and the DSI quartile gradient was dramatic: Q1=12.1%→Q4=32.8% (2.7-fold, P=2.02×10⁻⁴⁹). Of 1,141 hospital deaths, 33.6% occurred after ICU discharge. External validation in eICU-CRD (208 hospitals) preserved discrimination (AUC=0.792) and replicated the quartile gradient (12.0%→33.5%), though calibration required local recalibration (intercept −3.935).

**Conclusions**: DSI is an independent predictor of in-hospital mortality after SOFA adjustment, providing zero-cost bedside risk stratification with a dramatic quartile gradient. Component decomposition confirms prognostic information beyond isolated HR or DBP. DSI serves as a complementary bedside tool when laboratory data are pending, with the strongest prediction in non-surgical acute abdomen (AUC=0.826).

**Keywords**: Diastolic shock index; Acute abdomen; In-hospital mortality; SOFA; External validation

---

## Abbreviations

SI, shock index; MSI, modified shock index; DSI, diastolic shock index; Age-SI, age-adjusted shock index; HR, heart rate; SBP, systolic blood pressure; DBP, diastolic blood pressure; DAP, diastolic arterial pressure; MAP, mean arterial pressure; SOFA, Sequential Organ Failure Assessment; CCI, Charlson Comorbidity Index; ICU, intensive care unit; LOS, length of stay; ROC, receiver operating characteristic; AUC, area under the curve; NRI, net reclassification improvement; IDI, integrated discrimination improvement; cf-NRI, category-free NRI; cat-NRI, categorical NRI; DCA, decision curve analysis; RCS, restricted cubic splines; CIF, cumulative incidence function; HL, Hosmer-Lemeshow; VIF, variance inflation factor; MV, mechanical ventilation; ED, emergency department; ICD, International Classification of Diseases; WBC, white blood cell count; MI, multiple imputation

---

## Background

Acute abdomen—severe abdominal pain of sudden onset requiring urgent evaluation—remains one of the most challenging presentations in emergency medicine [1]. It encompasses etiologies from self-limiting inflammation to life-threatening intestinal ischemia, with mortality varying dramatically across subtypes (from <5% in uncomplicated appendicitis to >40% in mesenteric ischemia) [1,2]. Early risk stratification is critical, as delayed recognition of deteriorating patients contributes substantially to preventable mortality [3].

The shock index (SI=HR/SBP), first described by Allgöwer and Burri [4], has inspired several derivatives: modified shock index (MSI=HR/MAP) [5], diastolic shock index (DSI=HR/DBP) [6], and age-adjusted shock index (Age-SI=SI×Age/10) [7]. These predict mortality in trauma [8] and sepsis [9], but have never been systematically evaluated in acute abdomen—a population with unique pathophysiological diversity including inflammation-driven vasodilation, mechanical obstruction, perforation-induced peritonitis, and mesenteric ischemia. Existing bedside prognostic tools in this domain carry practical constraints: qSOFA augmented with lactate improves mortality prediction in complicated intra-abdominal infection but still requires laboratory measurement [41]; the WSES PIPAS score for acute peritonitis aggregates ten physiological and laboratory parameters [42]; and the relative performance of simple scores is setting-dependent [43]. Whether an even simpler vital-sign ratio provides independent prognostic value in the broader acute abdomen population has yet to be examined. Ospina-Tascón et al. [6] demonstrated that DSI, calculated at vasopressor initiation in septic shock, identified patients at high risk of death—where isolated HR or diastolic arterial pressure (DAP) did not. Whether this principle extends to the heterogeneous acute abdomen population, and whether DSI provides independent prognostic value beyond established ICU severity scores, remains unknown.

Moreover, previous SI-derivative studies have relied primarily on AUC comparisons without evaluating independent predictive value beyond established ICU predictors (lactate, vasopressor use, severity scores), nor assessing model robustness through bootstrap validation, sensitivity analyses, or competing risk frameworks. The TRIPOD+AI guidelines [10] emphasize that prediction models must demonstrate clinical benefit via NRI/IDI/DCA [11] and undergo external validation. Component decomposition analysis—demonstrating that a ratio provides prognostic information unavailable from its individual components—is particularly important for DSI, which has been questioned on dimensional grounds [12].

This study was reported following the STROBE statement [13] and the TRIPOD+AI guidelines [10]. We aimed to: (1) compare SI, MSI, DSI, and Age-SI for in-hospital mortality prediction; (2) evaluate DSI as an independent predictor beyond SOFA-adjusted covariates; (3) perform component decomposition to test whether isolated HR or DBP can replicate DSI's predictive value; (4) assess robustness via bootstrap, MI, and 14 sensitivity analyses; (5) externally validate in eICU-CRD; and (6) determine subtype-specific performance.

---

## Methods

### Data sources and study design

This retrospective cohort study utilized MIMIC-IV v3.1 [14] (Beth Israel Deaconess Medical Center, Boston, MA, 2008–2022; 546,028 admissions). External validation used eICU-CRD v2.0 [15] (208 US hospitals, 2014–2015). Both were accessed via PhysioNet with required training. IRB approval (BIDMC, MIT) was obtained; individual consent was waived for de-identified data. This study was reported following STROBE [13] and TRIPOD+AI [10] guidelines.

### Study population (Figure 1)

**Inclusion**: age ≥18; ICU admission via ED; acute abdomen ICD-9/10 codes (Supplementary Table S1); complete vital signs (HR, SBP, DBP) within 24h. **Exclusion**: missing extended covariates (lactate, WBC). From 546,028 admissions, 5,728 complete cases (CC) were analyzed. The 3,205 excluded patients had substantially lower severity (mortality 8.0% vs 19.9%, vasopressor 12% vs 43.6%, MV 17% vs 52.5%), reflecting selection bias toward patients receiving arterial blood gas monitoring (Supplementary Table S8). The DAG identifies lactate/WBC measurement as a collider opened by complete-case selection, inducing collider stratification bias; MI (N=8,933) and E-value analysis addressed this bias.

Acute abdomen subtypes based on ICD: perforation, ischemia, obstruction, inflammation, and other (29.9%, N=1,712, containing complications alongside primary codes; Supplementary Table S5). Priority: perforation > ischemia > obstruction > inflammation > other.

### Variables and statistical analysis

**SI derivatives** (first 24 hours of ICU admission): SI=HR/SBP, MSI=HR/MAP, DSI=HR/DBP, Age-SI=SI×Age/10. Blood pressure priority: arterial line > non-invasive BP > manual entries [14]. DAP is nearly constant from ascending aorta to peripheral vessels [16,17], supporting peripheral DBP for DSI calculation.

**Causal inference framework**: We pre-specified a DAG [39] (Supplementary Figure S11) identifying acute abdomen severity as the common cause of DSI, measured covariates, and outcome, with lactate/WBC measurement as a collider opened by complete-case selection.

**Primary outcome**: in-hospital mortality (hospital_expire_flag). **Secondary**: strict ICU mortality.

**Primary extended baseline** (without surgery): age, sex, CCI [18], lactate, WBC, vasopressor use, MV, SOFA [19]. Surgery was excluded because "surgery during hospitalization" (67.4%) introduces survivorship bias: only 5.1% had surgery ≤24h from ICU admission (surgery_24h OR=0.88, P=0.46). Alternative models (with surgery: Table S9; parsimonious without vasopressor/MV: Table S10) are reported; vasopressor (P=0.14) and MV (P=0.45) were non-significant after SOFA adjustment.

**Component decomposition analysis**: Following Ospina-Tascón et al. [6], we computed AUC for individual components (HR, DBP, SBP, MAP) and compared each with DSI using the DeLong test [20]. We then stratified patients into DBP quintiles and HR quintiles, and within each quintile examined mortality by DSI tertile. This tests whether DSI provides prognostic information unavailable from isolated components.

**Statistical methods**: The analysis plan was pre-specified and documented before data extraction. Multivariable logistic regression at three model levels: (1) basic baseline (age, sex, CCI); (2) extended baseline (adding lactate, WBC, vasopressor use, MV, SOFA; excluding surgery); and (3) extended+DSI. This nested framework isolates DSI's incremental contribution. ROC/AUC with DeLong comparisons [20] for all pairwise model comparisons. Benjamini-Hochberg false discovery rate (FDR) correction [38] was applied to all DeLong comparisons to account for multiplicity; the 5% FDR threshold was used. VIF for multicollinearity (all <3.0; maximum SOFA=2.42), confirming no problematic collinearity between DSI and SOFA or its components. NRI: categorical (<10%, 10–30%, >30% risk strata) as the primary reclassification metric and category-free (continuous) NRI [11] as a secondary measure; IDI [11] for integrated discrimination improvement. DCA [21] for clinical net benefit across threshold probabilities. RCS (4 knots at 5th, 35th, 65th, 95th percentiles) [22] to assess dose-response relationships and potential nonlinearity. Cumulative incidence functions for competing risks (in-hospital death vs discharge alive) by DSI quartile [23]; formal Fine-Gray subdistribution hazard models were not implemented (CIF curves are descriptive only). Calibration: HL goodness-of-fit test, Brier score, and calibration plots. Bootstrap internal validation (200 resamples; optimism=0.002, corrected AUC=0.788). Sensitivity analyses (14 scenarios, Supplementary Table S11). MI: 5 imputations using IterativeImputer on the full dataset (N=8,933); Multiple Imputation by Chained Equations (MICE) was used as a second imputation strategy to verify the stability of DSI's OR under different missing-data assumptions (Supplementary Table S11). E-values were computed to assess robustness to unmeasured confounding [40]. All analyses: Python 3.13 (pandas, scipy, statsmodels, scikit-learn, DuckDB); P<0.05 considered significant.

### External validation

MIMIC-IV models were applied to eICU-CRD without retraining (TRIPOD type 2b/3b [10]). **Methodological note**: eICU SOFA was computed from APACHE APS variables rather than identical MIMIC-IV concept definitions; platelets were unavailable (hematocrit substituted). This heterogeneity is reflected in higher eICU median SOFA (9 [7–12] vs MIMIC-IV 7 [4–11]). Both un-recalibrated and recalibrated (logistic intercept/slope adjustment) metrics are reported per TRIPOD+AI [10]. Performance: AUC/DeLong, cf-NRI/IDI, DSI quartile gradient (derivation cutoffs applied; eICU quartile sizes unequal: Q1=1,294, Q4=1,677).

---

## Results

### Baseline characteristics (Table 1)

Among 5,728 CC ICU stays: median age 68 [57–79], 56.0% male, in-hospital mortality 19.9% (1,141 deaths; 33.6% after ICU discharge). SOFA 7 [4–11]; significantly higher in non-survivors (11 [8–15] vs 6 [4–10], P<10⁻¹⁴⁰). Vasopressor use 43.6%; MV 52.5%; lactate 2.0 [1.3–3.2] mmol/L; WBC 11.6 [7.5–16.9] ×10⁹/L; CCI 3 [1–5]; ICU LOS 2.7 [1.5–5.8] days. Subtypes: inflammation (37.5%, N=2,149, mortality 16.8%), other (29.9%, N=1,712, mortality 16.9%), obstruction (20.6%, N=1,180, mortality 21.5%), ischemia (6.2%, N=353, mortality 40.5%), perforation (5.8%, N=334, mortality 28.1%). Ischemia had the highest mortality, consistent with the time-critical nature of mesenteric vascular compromise [28,30].

**Table 1.** Baseline characteristics by DSI quartile (MIMIC-IV v3.1, complete-case cohort, N=5,728).

| Characteristic | Overall (N=5,728) | Q1 Low (n=1,432) | Q2 (n=1,432) | Q3 (n=1,432) | Q4 High (n=1,432) |
|---|---|---|---|---|---|
| Age, years | 68.0 [57.0–79.0] | 66.0 [55.0–78.0] | 68.0 [57.0–79.0] | 69.0 [58.0–80.0] | 69.0 [56.0–80.0] |
| Male, n (%) | 3,206 (56.0) | 897 (62.6) | 800 (55.9) | 796 (55.6) | 713 (49.8) |
| CCI | 3.0 [1.0–5.0] | 3.0 [1.0–5.0] | 3.0 [1.0–5.0] | 3.0 [1.0–5.0] | 3.0 [1.0–5.0] |
| SOFA score | 7.0 [4.0–11.0] | 6.0 [3.0–9.0] | 7.0 [4.0–10.0] | 8.0 [5.0–11.0] | 10.0 [6.0–13.0] |
| Lactate, mmol/L | 2.0 [1.3–3.2] | 1.7 [1.2–2.7] | 1.9 [1.2–2.9] | 2.0 [1.4–3.3] | 2.6 [1.5–4.1] |
| WBC, ×10⁹/L | 11.6 [7.5–16.9] | 10.4 [7.0–15.1] | 11.4 [7.6–16.2] | 12.2 [7.8–17.9] | 12.2 [7.4–18.8] |
| Vasopressor use, n (%) | 2,498 (43.6) | 395 (27.6) | 562 (39.2) | 678 (47.3) | 863 (60.3) |
| Surgery, n (%) | 3,863 (67.4) | 867 (60.5) | 926 (64.7) | 1,009 (70.5) | 1,061 (74.1) |
| Mechanical ventilation, n (%) | 3,007 (52.5) | 601 (42.0) | 705 (49.2) | 799 (55.8) | 902 (63.0) |
| ICU LOS, days | 2.7 [1.5–5.8] | 2.1 [1.2–4.1] | 2.6 [1.5–5.1] | 2.9 [1.6–6.2] | 3.4 [1.8–8.0] |
| In-hospital mortality, n (%) | 1,141 (19.9) | 173 (12.1) | 208 (14.5) | 291 (20.3) | 469 (32.8) |
| ICU mortality, n (%) | 758 (13.2) | 94 (6.6) | 109 (7.6) | 186 (13.0) | 369 (25.8) |
| Subtype: inflammation, n (%) | 2,149 (37.5) | 615 (42.9) | 537 (37.5) | 519 (36.2) | 478 (33.4) |
| Subtype: obstruction, n (%) | 1,180 (20.6) | 245 (17.1) | 304 (21.2) | 307 (21.4) | 324 (22.6) |
| Subtype: perforation, n (%) | 334 (5.8) | 40 (2.8) | 60 (4.2) | 92 (6.4) | 142 (9.9) |
| Subtype: ischemia, n (%) | 353 (6.2) | 64 (4.5) | 56 (3.9) | 89 (6.2) | 144 (10.1) |
| Subtype: other, n (%) | 1,712 (29.9) | 468 (32.7) | 475 (33.2) | 425 (29.7) | 344 (24.0) |

### DSI quartile mortality gradient (Table 1)

DSI (mean 24h) quartiles demonstrated a dramatic gradient (χ²=229, P=2.02×10⁻⁴⁹): Q1<1.279 (12.1%), Q2 1.279–1.502 (14.5%), Q3 1.502–1.762 (20.3%), Q4>1.762 (32.8%)—a 2.7-fold increase. Higher quartiles had progressively higher lactate, vasopressor use, and MV rates, confirming DSI as an integrative hemodynamic severity marker.

### Component decomposition analysis (Figure S8)

Following Ospina-Tascón et al. [6], we examined whether isolated HR or DBP could replicate DSI's prognostic value. Individual AUCs for in-hospital mortality were: HR=0.571, DBP=0.597, SBP=0.638, MAP=0.621, SI=0.635, MSI=0.642, **DSI=0.644**, Age-SI=0.651, lactate=0.672, SOFA=0.740. DSI significantly outperformed isolated HR (DeLong P<0.001) and DBP (DeLong P<0.001), confirming that the ratio captures prognostic information unavailable from either component alone. DSI did not significantly outperform SI (P=0.21) or MSI (P=0.58), but the matched-stratification analysis (below) demonstrates DSI's unique contribution. All DeLong comparisons significant before correction remained significant after Benjamini-Hochberg FDR correction at the 5% threshold.

Critically, within each DBP quintile, DSI tertile consistently stratified mortality: for DBP Q3 (middle range), mortality progressed from 12.0% (low DSI) to 18.8% (mid DSI) to 32.5% (high DSI). Similarly, within HR quintiles, DSI tertile maintained its discriminatory capacity: for HR Q3, mortality progressed from 12.0% to 18.1% to 24.1%. Logistic regression confirmed DSI as a significant independent predictor within each DBP quintile (OR 2.01–6.43, all P<0.05 except Q5 high where P=0.054). These findings mirror the component decomposition in septic shock [6] and directly address the dimensional concern raised by Dalmau [12]: while DSI is dimensionally a ratio, it captures the simultaneous signal of compensatory tachycardia and vasomotor tone loss that neither component provides alone.

### Primary model results (Table 2)

**Table 2, Panel A (MIMIC-IV)**: Extended baseline (no surgery) AUC=0.785 [0.769–0.801]; adding DSI: AUC=0.790 [0.775–0.805], ΔAUC=0.005 (DeLong P=0.012). DSI: OR=2.18 [1.79–2.65], P=7.59×10⁻¹⁵; SOFA: OR=1.16 [1.13–1.19], P<10⁻³⁶; lactate: OR=1.14 [1.11–1.17]; CCI: OR=1.14 [1.11–1.16]. Vasopressor (P=0.14), MV (P=0.45), gender (P=0.08), and WBC (P=0.07) were non-significant after SOFA adjustment. ΔAUC=0.005 was below clinical relevance thresholds (≥0.02 per Cook [24] and Vickers [25]); categorical NRI (0.008, CI −0.009 to 0.044) crossed zero. Category-free NRI (0.252, CI 0.183–0.331) and IDI (0.013, CI 0.007–0.020) were significant, confirming additional continuous prognostic information. The primary DeLong comparison (Extended vs Extended+DSI, P=0.012) and all significant between-derivative DeLong tests remained significant after Benjamini-Hochberg FDR correction. VIF all <3.0; bootstrap optimism=0.002. Full coefficients: Supplementary Table S6; Forest plot: Figure 3; ROC curves: Figure 2.

**Table 2, Panel B (eICU-CRD)**: N=5,755 (208 hospitals), mortality 20.0%, SOFA 9 [7–12]. Extended baseline AUC=0.785; Extended+DSI AUC=0.792; ΔAUC=0.0074 (DeLong P=0.0026). Un-recalibrated: Brier=0.38–0.59, HL P<0.001 (catastrophically poor). After logistic recalibration (intercept −3.935, slope 0.952): Brier=0.126, HL P=0.266. cf-NRI=0.277, IDI=0.014. DSI quartile gradient: Q1=12.0%→Q4=33.5% (2.8-fold). The large intercept shift indicates discrimination is transportable (slope near 1.0), but absolute risk estimates require local recalibration.

**Table 2.** Independent association of DSI with in-hospital mortality and model performance in derivation and external validation cohorts.

Panel A. Multivariable logistic regression, MIMIC-IV (N=5,728)

| Variable | OR (95% CI) | P value |
|---|---|---|
| Age, per year | 1.022 (1.016–1.027) | <0.001 |
| Male sex | 0.877 (0.756–1.018) | 0.084 |
| CCI, per point | 1.137 (1.109–1.165) | <0.001 |
| Lactate, per mmol/L | 1.142 (1.110–1.174) | <0.001 |
| WBC, per ×10⁹/L | 1.006 (1.000–1.012) | 0.074 |
| Vasopressor use | 1.142 (0.957–1.363) | 0.142 |
| Mechanical ventilation | 1.078 (0.886–1.312) | 0.452 |
| SOFA, per point | 1.160 (1.134–1.188) | <0.001 |
| DSI, per unit | 2.179 (1.791–2.652) | <0.001 |

Panel B. Model performance: MIMIC-IV derivation vs eICU-CRD external validation

| Metric | MIMIC-IV (N=5,728) | eICU-CRD (N=5,755) |
|---|---|---|
| Extended baseline AUC | 0.785 (0.769–0.801) | 0.785 |
| Extended + DSI AUC | 0.790 (0.775–0.805) | 0.792 |
| ΔAUC (DeLong P) | 0.005 (P=0.012) | 0.007 (P=0.003) |
| Categorical NRI | 0.008 (−0.009 to 0.044) | — |
| Category-free NRI | 0.252 (0.183–0.331) | 0.277 |
| IDI | 0.013 (0.007–0.020) | 0.014 |

### Sensitivity analyses (Supplementary Table S11)

DSI's predictive value was robust across 14 analyses (OR 2.15–2.65, all P<10⁻¹¹), addressing nine bias categories: confounding, misclassification, overadjustment, collider/selection, misspecification, utility, overfitting, heterogeneity, and competing risks (Supplementary Table S11). Key findings: surgery appeared protective (OR=0.68, survivorship bias) while surgery_24h was non-significant (OR=0.88, P=0.46); MI (N=8,933) yielded AUC=0.822, DSI OR=2.65, with MICE confirming stability (OR=2.63); non-surgical subgroup showed best discrimination (AUC=0.826, DSI OR=2.28); RCS confirmed linearity (P_nonlinear>0.05); calibration was excellent (HL P=0.691, Brier=0.126); DSI threshold diagnostic performance (sensitivity/specificity/PPV/NPV/Youden index) is detailed in Supplementary Table S12; and CIF curves separated by DSI quartile (Supplementary Figure S7).
---

## Discussion

To the best of our knowledge, this is the first study to systematically evaluate SI-derived parameters in acute abdomen ICU patients, with SOFA adjustment, component decomposition analysis, bootstrap validation, MI, 14 sensitivity analyses, competing risk framework, external validation across 208 hospitals, and STROBE/TRIPOD+AI-compliant reporting. Five principal findings emerge.

**First**, DSI is an independent predictor after SOFA adjustment (OR=2.18, P=7.59×10⁻¹⁵). The component decomposition analysis demonstrates that isolated HR (AUC=0.571) and DBP (AUC=0.597) are poor predictors of mortality, while DSI (AUC=0.644) significantly outperforms both (DeLong P<0.001). Critically, within matched DBP or HR quintiles, DSI tertile consistently stratified mortality—from 12.0% to 32.5% even within the same DBP range. This mirrors the key finding of Ospina-Tascón et al. [6] in septic shock, where "isolated DAP or high HR values do not clearly identify such risk," and directly addresses the dimensional concern raised by Dalmau [12]: although DSI is dimensionally a ratio, it captures the simultaneous signal of compensatory tachycardia and vasomotor tone loss—a composite hemodynamic phenotype that neither component provides alone.

However, ΔAUC=0.005 is below clinical relevance thresholds (≥0.02) [24,25], and categorical NRI crossing zero means DSI does not reclassify patients across the 10%/30% risk strata beyond a model already containing SOFA and lactate. This is expected when a marker refines continuous prediction without shifting categorical thresholds [25]. We position DSI not as a SOFA replacement, but as a **complementary zero-cost bedside tool** providing independent risk information from routinely monitored HR and DBP—available without laboratory turnaround time. DSI's clinical value lies in immediate risk stratification when SOFA components (platelets, bilirubin, PaO₂, vasopressor doses) are pending.

**Second**, the DSI quartile gradient (12.1%→32.8%, 2.7-fold) provides clinically actionable thresholds (Q1<1.279, Q4>1.762). Higher quartiles had progressively higher lactate, vasopressor, and MV rates, confirming DSI as an integrative hemodynamic severity marker. This gradient was closely replicated in eICU-CRD (12.0%→33.5%, 2.8-fold), supporting its generalizability.

**Third**, 33.6% of hospital deaths (383/1,141) occurred after ICU discharge, highlighting the clinical importance of in-hospital mortality as the primary endpoint. Patients surviving ICU but later dying in-hospital represent a population where DSI-based risk stratification could guide post-ICU monitoring intensity—a decision point not captured by ICU-specific mortality endpoints.

**Fourth**, surgery was excluded from the primary model due to survivorship bias: 67.4% "during hospitalization" vs 5.1% ≤24h, with surgery_24h non-significant (P=0.46). Including surgery increased baseline AUC by only 0.002, confirming its minimal and biased contribution. This bias affects any model including "surgery during hospitalization" as a covariate—a caution for future ICU prediction studies.

**Fifth**, external validation in eICU-CRD (208 hospitals) preserved discrimination (AUC=0.792, ΔAUC=0.0074) and replicated the quartile gradient. However, direct application yielded catastrophically poor calibration (Brier 0.38–0.59), requiring logistic recalibration (intercept −3.935, slope 0.952). The near-ideal slope confirms discrimination transportability, but the large intercept shift means MIMIC-IV-derived absolute risk estimates cannot be directly applied to new settings without local recalibration.

### Bias and causal inference

We addressed causal inference using a pre-specified DAG (Supplementary Figure S11). The DAG formalizes why complete-case selection on lactate and WBC is a collider, not merely "selection bias": acute abdomen severity increases both the likelihood of laboratory measurement and the risk of death; conditioning on having lactate/WBC measured opens a non-causal pathway between DSI and mortality, potentially biasing the observed association [39]. Two strategies mitigate this: first, MI on the full eligible cohort (N=8,933) produced an even larger DSI effect (OR=2.65), suggesting the CC estimate (OR=2.18) is conservative rather than inflated. Second, the E-value for the primary OR is 3.78 (2.98 for the 95% CI lower bound; Supplementary Table S13). This means an unmeasured confounder would need to be associated with both DSI and mortality by a risk ratio exceeding 3.7-fold—larger than the effects of SOFA (OR=1.16/point), lactate (OR=1.14/mmol/L), or CCI (OR=1.14/point) in our model—to explain away the point estimate; 3.0-fold to move the confidence interval to the null. Such confounders are biologically and clinically implausible after SOFA adjustment, supporting the robustness of the independent association. This causal framework also clarifies why vasopressor and MV became non-significant after SOFA adjustment: both are downstream consequences of the same hemodynamic collapse captured by SOFA and lactate, and are therefore mediators rather than confounders in the DSI→mortality pathway.

### Pathophysiological rationale

DSI (HR/DBP) captures the relationship between cardiac output proxy (HR) and diastolic perfusion pressure (DBP). In healthy individuals, DAP is determined by vascular tone and remains nearly constant from the ascending aorta to peripheral vessels [16,17], reflecting the Windkessel effect—aortic elastic recoil maintaining diastolic perfusion pressure [26]. This supports the use of non-invasive DBP for DSI calculation, even when inflammatory conditions alter arterial compliance [6,27].

In acute abdomen, several mechanisms converge to make DSI informative. First, progressive vasodilation from inflammatory mediators and splanchnic vascular compromise manifests as diastolic pressure decline—reflecting loss of peripheral vascular tone before systolic failure [6,26]. The splanchnic circulation receives approximately 25% of cardiac output [28], and intra-abdominal pathology directly compromises this bed, causing early DAP reduction through regional vasodilation and third-space losses. Second, compensatory tachycardia develops as cardiac output rises to maintain perfusion against falling vascular resistance [6,29]. The simultaneous rise in HR and fall in DBP—captured by their ratio—signals more severe circulatory dysfunction than either component alone, as confirmed by our matched-stratification analysis. Third, in mesenteric ischemia, reperfusion injury perpetuates systemic inflammation [30], likely contributing to the high mortality in this subgroup (40.5%, AUC=0.807).

The ratio formulation addresses the dimensional concern raised by Dalmau [12]: although DSI is dimensionless, its clinical meaning lies in capturing the **compensatory-to-decompensatory transition**—where tachycardic compensation can no longer mask loss of vasomotor tone. Our matched-stratification empirically confirms this: at similar DBP values, mortality varies dramatically by DSI tertile (DBP Q3: 12.0%→32.5%), demonstrating that the ratio provides information beyond either component alone. Notably, machine-learning explainability analyses in postoperative critically ill patients have independently identified diastolic blood pressure among the most influential predictors of mortality [44], corroborating from a data-driven perspective the prognostic weight of DBP embedded in the DSI formulation.

### Comparison with previous studies

Our results extend the work of Ospina-Tascón et al. [6] from septic shock (N=761, mortality 43%) to acute abdomen (N=5,728, mortality 19.9%). In both populations, DSI outperformed isolated HR and DBP for mortality prediction, and the quartile/quintile gradient was dramatic. The original DSI study in septic shock reported median DSI values of 2.28 (preliminary cohort) and 1.97 (ANDROMEDA-SHOCK) at vasopressor initiation [6]; our acute abdomen cohort had a lower median DSI (1.50 [1.28–1.76]), consistent with a less vasodilatory population at ICU admission—before vasopressor initiation—supporting DSI's utility as an **early** marker before hemodynamic collapse.

Our study adds several methodological advances: (1) SOFA-adjusted evaluation establishing DSI as an independent predictor beyond the most widely used ICU severity score; (2) formal NRI/IDI with confidence intervals, enabling quantitative assessment of reclassification; (3) component decomposition in a different patient population, confirming the generalizability of the principle that "isolated DAP or high HR values do not clearly identify such risk" [6]; (4) external validation in 208 hospitals, far exceeding the dual-cohort design of the original study; and (5) competing risk assessment via CIF. Ospina-Tascón et al. [6] did not perform these analyses but used time-course analysis and DSI×norepinephrine dose interaction—approaches not replicated here due to the retrospective nature of our data. The DSI trajectory analysis (survivors vs non-survivors) proposed by Ospina-Tascón [6] represents an important future direction for our acute abdomen cohort.

Our findings also extend the broader SI-derivative literature. Jouffroy et al. [5] validated MSI in prehospital septic shock; Liu et al. [9] confirmed SI derivatives in sepsis; and Olaussen et al. [8] systematically reviewed SI in trauma. King et al. [33] and Rady et al. [34] established the shock index's value in acute circulatory failure. None evaluated acute abdomen specifically, and none performed component decomposition or external validation. Within abdominal emergencies themselves, the WSES PIPAS consortium validated a ten-variable bedside score for acute peritonitis, with mortality rising from 2.9% at 0–1 points to 86.7% at 7–8 points [42]; our single vital-sign ratio achieved comparable directional risk stratification (12.1%→32.8%) using two routinely monitored parameters, and the external validation in eICU-CRD (208 hospitals, AUC=0.792 preserved) substantially strengthens generalizability evidence—a key gap in prior SI-derivative studies identified by the TRIPOD+AI framework [10,32].

Our results also speak to recently published models for intra-abdominal infection. Zhang et al. [35] developed a nomogram for intra-abdominal sepsis mortality using LASSO-selected variables (lactate, age, APTT, BUN, TBIL, platelets; AUC=0.795) from the same MIMIC-IV database. Their model excluded hemodynamic parameters and relied on six results requiring 30–60 minutes to obtain. In contrast, DSI provides zero-cost bedside risk stratification from routine vital signs within seconds. Our Extended+DSI model achieved virtually identical discrimination (AUC=0.790) with only HR and DBP added to baseline covariates, and our eICU validation cohort (N=5,755, 1,151 deaths) was substantially larger than theirs (N=149, 33 deaths). Jeon et al. [36] evaluated DSI for septic shock progression at ED triage (N=1,267, Korea), reporting DSI AUC=0.717 versus SI AUC=0.707 (DeLong P=0.14). While DSI and SI performed similarly for shock prediction in that ED population, DSI tertiles correlated with vasopressor dose and time to initiation, supporting the hemodynamic severity interpretation central to our findings. The context-dependence is important: in septic shock, SI may rise similarly to DSI after circulatory collapse; in acute abdomen at ICU admission, our matched-stratification shows DSI refines prognosis beyond isolated HR or DBP. These complementary reports strengthen DSI's bedside positioning while underscoring that its incremental value is setting-specific.

### Clinical implications

DSI offers five advantages: (1) independent predictive value beyond SOFA (OR=2.18); (2) dramatic quartile gradient (12.1%→32.8%) with actionable thresholds; (3) zero-cost bedside availability from routine vitals without laboratory tests or specialized equipment; (4) externally validated discrimination across 208 hospitals (AUC=0.792); and (5) immediate availability—DSI is calculated within seconds, whereas SOFA components may require 30–60 minutes [19,31]. This temporal advantage is particularly relevant in the ED and early ICU course.

In ischemia (mortality 40.5%, AUC=0.807) and non-surgical acute abdomen (AUC=0.826), DSI may help identify patients needing urgent surgical evaluation or intensive monitoring. The 33.6% post-ICU death rate suggests DSI should guide post-ICU monitoring decisions. However, clinicians should understand that DSI complements rather than replaces SOFA: ΔAUC below clinical thresholds [24,25] and categorical NRI crossing zero mean DSI should not override SOFA-based categorical risk classifications, but rather provide immediate risk stratification when laboratory data are unavailable [31].

### Strengths and limitations

This study has several strengths: a dual-database design with external validation across 208 hospitals; a pre-specified DAG-guided causal framework with E-value sensitivity analysis for unmeasured confounding; component decomposition demonstrating prognostic information beyond isolated components; bootstrap internal validation with dual imputation strategies (IterativeImputer and MICE); 14 sensitivity analyses covering nine bias categories; and STROBE/TRIPOD+AI-compliant reporting.

Several limitations should nevertheless be acknowledged. (1) Single-center retrospective derivation, though externally validated in 208 hospitals; selection bias from 36% exclusion (primarily lactate) enriched CC with sicker patients (mortality 19.9% vs 8.0% in excluded), addressed by MI (N=8,933, AUC=0.822, DSI OR=2.65); eICU validation also used CC (32.6% rate), creating a parallel selection bias. Microbiological data were not incorporated; Luo et al. [37] and Zhang et al. [35] showed Enterococcus and fungal infections are independently associated with intra-abdominal infection mortality, suggesting future models could improve subtype-specific prediction by integrating culture results. (2) ΔAUC below clinical thresholds (≥0.02) [24,25]; categorical NRI crossing zero; DSI is a complementary bedside tool, not a SOFA replacement; surgery survivorship bias addressed by removal from the primary model. (3) "Other" subtype heterogeneity (29.9%); sensitivity excluding it preserved results (AUC=0.786–0.788, DSI OR=2.15–2.22); no formal Fine-Gray models; CIF curves are descriptive only. (4) eICU SOFA heterogeneity (APS-based vs MIMIC-IV concept; median 9 vs 7; hematocrit substituted for platelets); large recalibration intercept shift (−3.935) means absolute risk predictions require local recalibration; discrimination (slope 0.952) is transportable. (5) Non-significant covariates (vasopressor P=0.14, MV P=0.45, WBC P=0.07, gender P=0.08) were absorbed by SOFA components. (6) Surveillance bias: patients receiving more frequent vital sign measurement generate more datapoints for DSI calculation, though our use of 24-hour mean values from routine ICU monitoring—where measurement frequency is standardized—partially mitigates this concern. (7) Only two authors; statistical expertise guided by TRIPOD+AI guidelines [10,32] and established references [20,24,25].

Looking ahead, several directions merit investigation. First, prospective multicenter validation with standardized SOFA computation would address methodological heterogeneity between databases. Second, Fine-Gray subdistribution hazard modeling would formally quantify DSI's effect accounting for the competing risk of discharge alive. Third, DSI trajectory analysis over 24–48 hours could identify dynamic risk patterns, as Ospina-Tascón et al. [6] showed persistently high DSI tracked with increasing vasopressor requirements. Fourth, data-driven variable selection (LASSO or random forest) could complement our pre-specified approach: while pre-specification ensures clinical interpretability, LASSO may identify more parsimonious predictor sets, as shown by Zhang et al. [35]. Fifth, validation in non-US populations and ED settings would broaden generalizability, and PCA-based SI+DSI composites, as proposed by Jeon et al. [36], represent an alternative risk-dimension approach. Sixth, interventional studies assessing whether DSI-guided early vasopressor initiation, surgical timing, or post-ICU monitoring improves outcomes would establish clinical utility beyond prediction.

---

## Conclusions

DSI is an independent predictor of in-hospital mortality in acute abdomen after SOFA adjustment (OR=2.18, 95% CI 1.79–2.65), with a dramatic quartile gradient (2.7-fold) and externally validated discrimination across 208 hospitals. Component decomposition analysis confirms that DSI captures unique prognostic information unavailable from isolated HR or DBP. Whether DSI-guided early intervention improves patient outcomes deserves prospective investigation.

---

## Supplementary Materials

**Table S1**: ICD-9/10 codes for acute abdomen identification and subtype classification.
**Table S2**: STROBE checklist (completed).
**Table S3**: Baseline characteristics (N=5,728) by DSI quartile, including SOFA.
**Table S4**: TRIPOD+AI checklist (27 items) [10].
**Table S5**: ICD code composition of "Other" subtype (N=1,712).
**Table S6**: Full model coefficients (primary model without surgery + DSI).
**Table S7**: eICU-CRD baseline characteristics (N=5,755) by DSI quartile.
**Table S8**: Excluded (N=3,205) vs CC (N=5,728) patient characteristics.
**Table S9**: Alternative model (with surgery) coefficients and performance.
**Table S10**: Parsimonious model (without vasopressor/MV) performance.
**Table S11**: Sensitivity analyses summary (14 scenarios).
**Table S12**: DSI threshold diagnostic performance (Se/Sp/PPV/NPV/Youden) at DSI=1.0, 1.279, 1.502, 1.762, and 2.0.
**Table S13**: E-value analysis for DSI primary OR (2.18) and lower confidence bound (1.79).

**Figure S1**: Calibration plots for basic baseline models.
**Figure S2**: Kaplan-Meier curves by DSI quartile.
**Figure S3**: RCS dose-response curves for SI, MSI, DSI, Age-SI.
**Figure S4**: DCA net benefit across threshold probabilities.
**Figure S5**: Calibration plots (4 model levels).
**Figure S6**: Subgroup ROC curves by subtype.
**Figure S7**: Cumulative incidence functions by DSI quartile.
**Figure S8**: Component decomposition analysis—(A) AUC of individual predictors; (B) mortality by DBP quintile and DSI tertile; (C) mortality by HR quintile and DSI tertile.
**Figure S9**: Nomograms for predicting in-hospital mortality—(A) full Extended+DSI model; (B) rapid bedside model (age+lactate+SOFA+DSI).
**Figure S10**: Clinical impact curves for Extended baseline with and without DSI.
**Figure S11**: Directed acyclic graph (DAG) depicting hypothesized causal relationships among acute abdomen severity, DSI, measured covariates, and in-hospital mortality.

---

## Figure Legends

**Figure 1**: Study flow diagram (546,028→5,728 CC), with excluded patient characteristics in Supplementary Table S8.

**Figure 2**: ROC curves—basic baseline, extended baseline (no surgery), extended+DSI (no surgery), extended+all SI derivatives.

**Figure 3**: Forest plot of adjusted ORs from the primary model (extended baseline without surgery + DSI).

---

## Declarations

**Ethics**: MIMIC-IV and eICU-CRD are publicly available with IRB approval (BIDMC, MIT). Individual consent waived for de-identified data.

**Consent for publication**: Not applicable.

**Funding**: GWJJMB202510024181 (National Health Commission), kq2014242 (Changsha Science and Technology Bureau), 2021JJ30959 (Hunan Provincial Natural Science Foundation). Funders had no role in study design, analysis, or publication.

**Conflicts**: Authors declare no conflicts.

**CRediT**: Yuzhong Cai: Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Software, Validation, Visualization, Writing – original draft. Jiqiang Liu: Data curation, Investigation, Validation, Writing – review & editing. Dengke Wu: Conceptualization, Funding acquisition, Methodology, Project administration, Resources, Supervision, Writing – review & editing.

**AI use declaration**: During the preparation of this manuscript, the authors used a large language model for language polishing and manuscript editing only. All data extraction, statistical analyses, figure generation, and scientific interpretation were performed independently by the authors. After using the tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.

**Acknowledgments**: We thank the MIMIC-IV and eICU-CRD teams for open access to clinical databases.

**Data availability**: MIMIC-IV v3.1 at https://physionet.org/content/mimiciv/3.1/. eICU-CRD v2.0 at https://physionet.org/content/eicu-crd/2.0/. Analysis code is publicly available at https://github.com/wudengke2010/dsi-acute-abdomen-mimic-iv.

---

## References

1. Flum DR. Acute abdomen. In: Sabiston Textbook of Surgery. 21st ed. Elsevier; 2022.
2. Cervero F, Laird JM. Visceral pain. Lancet. 1999;353(9170):2145-2148. https://doi.org/10.1016/S0140-6736(99)01306-9
3. Siegel JH, Greenspan M, Del Guercio LR. Abnormal vascular tone, defective oxygen transport and myocardial failure in human septic shock. Ann Surg. 1967;165(4):504-517. https://doi.org/10.1097/00000658-196704000-00002
4. Allgöwer M, Burri C. Schockindex. Deutsche Med Wochenschr. 1967;92(43):1947-1950. https://doi.org/10.1055/s-0028-1106070
5. Jouffroy R, Gille S, Gilbert B, et al. Shock index derivatives and 28-day mortality in prehospital septic shock. J Emerg Med. 2024;66(2):144-153. https://doi.org/10.1016/j.jemermed.2023.11.010
6. Ospina-Tascón GA, Teboul JL, Hernandez G, et al. Diastolic shock index and clinical outcomes in septic shock. Ann Intensive Care. 2020;10:41. https://doi.org/10.1186/s13613-020-00658-8
7. Kim SY, Hong KJ, Shin SD, et al. Validation of shock indices for predicting geriatric trauma mortality. J Korean Med Sci. 2016;31(12):2026-2032. https://doi.org/10.3346/jkms.2016.31.12.2026
8. Olaussen A, Peterson G, Synnot A, et al. Shock index and mortality in trauma: systematic review. Crit Care. 2023;27:88. https://doi.org/10.1186/s13054-023-04386-w
9. Liu YC, Lee CT, Su HY, et al. Shock indices and in-hospital mortality in sepsis. PLoS One. 2024;19(3):e0298617. https://doi.org/10.1371/journal.pone.0298617
10. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement. BMJ. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378
11. Pencina MJ, D'Agostino RB, et al. Evaluating added predictive ability. Stat Med. 2008;27(2):157-172. https://doi.org/10.1002/sim.2929
12. Dalmau R. The diastolic shock index works… but, what is it? Ann Intensive Care. 2020;10:103. https://doi.org/10.1186/s13613-020-00720-5
13. von Elm E, Altman DG, Egger M, et al. STROBE statement. Lancet. 2007;370(9596):1453-1457. https://doi.org/10.1016/S0140-6736(07)61602-x
14. Johnson AEW, Bulgarelli L, Pollard TJ, et al. MIMIC-IV, a freely accessible electronic health record dataset. Sci Data. 2023;10:1. https://doi.org/10.1038/s41597-022-01899-x
15. Pollard TJ, Johnson AEW, Raffa JD, et al. eICU-CRD. Sci Data. 2018;5:180175. https://doi.org/10.1038/sdata.2018.178
16. Hamilton W. The patterns of the arterial pressure pulse. Am J Physiol. 1944;141(2):235-241. https://doi.org/10.1152/ajplegacy.1944.141.2.235
17. O'Rourke MF. Pressure and flow waves in systemic arteries and the anatomical design of the arterial system. J Appl Physiol. 1967;23(2):139-149. https://doi.org/10.1152/jappl.1967.23.2.139
18. Charlson ME, Pompei P, Ales KL, MacKenzie CR. Comorbidity classification. J Chronic Dis. 1987;40(5):373-383. https://doi.org/10.1016/0021-9681(87)90171-8
19. Vincent JL, Moreno R, Takala J, et al. SOFA score. Intensive Care Med. 1996;22(7):707-710. https://doi.org/10.1007/BF01709751
20. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing AUCs. Biometrics. 1988;44(3):837-845. https://doi.org/10.2307/2531595
21. Vickers AJ, Elkin EB. Decision curve analysis. Med Decis Making. 2006;26(6):565-574. https://doi.org/10.1177/0272989X06295361
22. Desquilbet L, Mariotti F. Dose-response analyses using restricted cubic spline functions in public health research. Stat Med. 2010;29(9):1037-1057. https://doi.org/10.1002/sim.3841
23. Fine JP, Gray RJ. Proportional hazards model for competing risks. J Am Stat Assoc. 1999;94(446):496-509. https://doi.org/10.1080/01621459.1999.10474144
24. Cook NR. Use and misuse of the receiver operating characteristic curve in risk prediction. Circulation. 2007;115(7):928-935. https://doi.org/10.1161/CIRCULATIONAHA.106.672402
25. Vickers AJ, Cronin AM, Begg CB. One statistical test is sufficient for assessing new predictive markers. BMC Med Res Methodol. 2011;11:13. https://doi.org/10.1186/1471-2288-11-13
26. O'Rourke MF. Steady and pulsatile energy losses in the systemic circulation under normal conditions and in simulated arterial disease. Cardiovasc Res. 1967;1(4):313-326. https://doi.org/10.1093/cvr/1.4.313
27. Benchekroune S, Karpati PC, Berton C, et al. Diastolic arterial blood pressure: a reliable early predictor of survival in human septic shock. J Trauma. 2008;64(5):1188-1195. https://doi.org/10.1097/ta.0b013e31811f3a45
28. Jakob SM. Clinical review: splanchnic ischemia. Crit Care. 2002;6(4):322-327. https://doi.org/10.1186/cc1515
29. Cecconi M, De Backer D, Antonelli M, et al. Consensus on circulatory shock and hemodynamic monitoring. Intensive Care Med. 2014;40(12):1795-1815. https://doi.org/10.1007/s00134-014-3525-z
30. Vincent JL, De Backer D. Circulatory shock. N Engl J Med. 2013;369(18):1726-1734. https://doi.org/10.1056/nejmra1208943
31. Steyerberg EW, Vergouwe Y. Better clinical prediction models: seven steps. Eur Heart J. 2014;35(29):1925-1931. https://doi.org/10.1093/eurheartj/ehu207
32. Moons KGM, Altman DG, Reitsma JB, et al. Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD). Ann Intern Med. 2015;162(10):735-736. https://doi.org/10.7326/M14-0697
33. King RW, Plewa MC, Buderer NM, et al. Shock index as a marker for significant injury in trauma patients. Acad Emerg Med. 1996;3(11):1041-1045. https://doi.org/10.1111/j.1553-2712.1996.tb03351.x
34. Rady MY, Nightingale P, Little RA, et al. Shock index: a re-evaluation in acute circulatory failure. Resuscitation. 1992;23(3):227-234. https://doi.org/10.1016/0300-9572(92)90006-x

35. Zhang J, Chen Y, Zhao C, et al. Development and validation of a prediction model for in-hospital mortality in patients with intra-abdominal sepsis: a dual-database study using MIMIC-IV and eICU databases. BMJ Open. 2025;15:e102971. https://doi.org/10.1136/bmjopen-2025-102971

36. Jeon Y, Kim S, Ahn S, et al. Predicting septic shock in patients with sepsis at emergency department triage using systolic and diastolic shock index. Am J Emerg Med. 2024;78:196-201. https://doi.org/10.1016/j.ajem.2024.01.029

37. Luo X, Li L, Ou S, et al. Risk factors for mortality in abdominal infection patients in ICU: a retrospective study from 2011 to 2018. Front Med. 2022;9:839284. https://doi.org/10.3389/fmed.2022.839284

38. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Series B. 1995;57(1):289-300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

39. Greenland S, Pearl J, Robins JM. Causal diagrams for epidemiologic research. Epidemiology. 1999;10(1):37-48. https://doi.org/10.1097/00001648-199901000-00008

40. VanderWeele TJ, Ding P. Sensitivity analysis in observational research: introducing the E-value. Ann Intern Med. 2017;167(4):268-274. https://doi.org/10.7326/M16-2607

41. Jung YT, Jeon J, Park JY, et al. Addition of lactic acid levels improves the accuracy of quick sequential organ failure assessment in predicting mortality in surgical patients with complicated intra-abdominal infections: a retrospective study. World J Emerg Surg. 2018;13:14. https://doi.org/10.1186/s13017-018-0177-9

42. Sartelli M, Abu-Zidan FM, Labricciosa FM, et al. Physiological parameters for Prognosis in Abdominal Sepsis (PIPAS) Study: a WSES observational study. World J Emerg Surg. 2019;14:34. https://doi.org/10.1186/s13017-019-0235-z

43. Koch C, Edinger F, Fischer T, et al. Comparison of qSOFA score, SOFA score, and SIRS criteria for the prediction of infection and mortality among surgical intermediate and intensive care unit patients. World J Emerg Surg. 2020;15:63. https://doi.org/10.1186/s13017-020-00320-5

44. Park DJ, Baik SM, Hong KS, et al. Development and external validation of an artificial intelligence model for predicting mortality and prolonged intensive care unit stay in postoperative critically ill patients: a retrospective study. World J Emerg Surg. 2025;20:79. https://doi.org/10.1186/s13017-025-00650-6
