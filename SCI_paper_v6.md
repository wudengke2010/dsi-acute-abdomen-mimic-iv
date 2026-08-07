# Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation

**Jiqiang Liu** [1]†, **Dengke Wu** [1]*

[1] Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China

† First author.

* Corresponding author: Dengke Wu, Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China. Electronic address: wudk2010@csu.edu.cn

---

## Abstract

**Background**: Shock index (SI) and its derivatives—modified shock index (MSI), diastolic shock index (DSI), and age-adjusted shock index (Age-SI)—predict mortality in trauma and sepsis, yet remain unexplored in acute abdomen. We evaluated SI-derived parameters for in-hospital mortality prediction, assessing DSI as an independent, zero-cost bedside predictor complementary to SOFA.

**Methods**: Retrospective cohort from MIMIC-IV v3.1. Adult ICU patients with acute abdomen diagnoses were included. SI/MSI/DSI/Age-SI were calculated from 24h vital signs. Primary outcome: in-hospital mortality. The primary extended baseline model excluded abdominal surgery (to avoid survivorship bias), incorporating age, sex, CCI, lactate, WBC, vasopressor use, mechanical ventilation, and SOFA. Performance was assessed via ROC/AUC, NRI/IDI, DCA, RCS, cumulative incidence functions, calibration, and bootstrap validation. Multiple imputation (N=8,933) and 12 sensitivity analyses were performed. External validation used eICU-CRD (N=5,755, 208 hospitals).

**Results**: Among 5,728 complete-case ICU stays (median age 68 [IQR 57-79], 56.0% male, in-hospital mortality 19.9%, SOFA 7 [4-11]), DSI was the best SI derivative. The primary extended baseline (without surgery) achieved AUC=0.785; adding DSI yielded AUC=0.790 (ΔAUC=0.005, DeLong P=0.012). DSI remained an independent predictor (OR=2.18, 95% CI 1.79-2.65, P=7.59×10⁻¹⁵) after SOFA adjustment. The ΔAUC was below conventional clinical relevance thresholds (≥0.02), and the categorical NRI crossed zero (0.008, 95% CI −0.009 to 0.044), indicating DSI does not reclassify patients across clinically relevant risk strata. However, category-free NRI (0.252, 95% CI 0.183-0.331) and IDI (0.013, 95% CI 0.007-0.020) were significant, and the DSI quartile mortality gradient was dramatic: Q1=12.1% → Q4=32.8% (P=2.02×10⁻⁴⁹). Of 1,141 hospital deaths, 383 (33.6%) occurred after ICU discharge. Excluding the heterogeneous "Other" subtype (N=4,016) yielded AUC=0.786, DSI OR=2.15. External validation in eICU-CRD preserved discrimination (AUC=0.792, ΔAUC=0.0074, DeLong P=0.0026), though calibration required logistic recalibration (intercept shift −3.935). DSI quartile gradient was replicated: 12.0% → 33.5%.

**Conclusions**: DSI is an independent predictor of in-hospital mortality in acute abdomen after SOFA adjustment, providing zero-cost bedside risk stratification with a dramatic quartile mortality gradient (2.7-fold) and externally validated discrimination. While ΔAUC is below clinical relevance thresholds and categorical NRI crosses zero—indicating DSI does not replace SOFA for categorical decision-making—the quartile gradient, category-free NRI, and independent OR support DSI as a complementary, immediately available risk-stratification tool when laboratory data are unavailable. Prediction was most pronounced in non-surgical acute abdomen (AUC=0.826).

**Keywords**: Diastolic shock index; Acute abdomen; In-hospital mortality; SOFA; ICU risk stratification; MIMIC-IV; eICU-CRD; External validation

---

## 1. Introduction

Acute abdomen—severe abdominal pain of sudden onset requiring urgent evaluation—remains one of the most challenging presentations in emergency medicine [1]. Early risk stratification is a critical unmet need, as outcomes vary dramatically across etiologies ranging from self-limiting inflammation to life-threatening intestinal ischemia [1,2].

The shock index (SI = HR/SBP), first described by Allgöwer and Burri in 1967 [3], has inspired several derived indices: modified shock index (MSI = HR/MAP) [4,18], diastolic shock index (DSI = HR/DBP) [5], and age-adjusted shock index (Age-SI = SI×Age/10) [6]. These have been validated in trauma [7] and sepsis [8], but never systematically evaluated in acute abdomen—a population with pathophysiological diversity including inflammation-driven vasodilation, mechanical obstruction, perforation-induced peritonitis, and ischemia-requiring reperfusion.

Moreover, previous SI-derivative studies have relied primarily on AUC comparisons without evaluating independent predictive value beyond established ICU predictors (lactate, vasopressor use, severity scores), nor assessing model robustness through bootstrap validation, sensitivity analyses, or competing risk frameworks. The TRIPOD+AI guidelines [17,19] emphasize that prediction models must demonstrate clinical benefit via NRI/IDI/DCA [17] and undergo internal and external validation [11]. This study was reported following the STROBE statement [14] and the TRIPOD+AI guidelines [19].

This study aims to: (1) compare SI, MSI, DSI, and Age-SI for in-hospital mortality prediction in acute abdomen; (2) evaluate DSI as an independent predictor beyond extended covariates including SOFA, using NRI with confidence intervals, IDI, and DCA; (3) assess model robustness via bootstrap validation, multiple imputation, and sensitivity analyses; (4) evaluate competing risks using cumulative incidence functions; (5) externally validate in eICU-CRD; and (6) determine subtype-specific prediction performance.

---

## 2. Methods

### 2.1 Study Design and Data Source

This retrospective cohort study utilized MIMIC-IV v3.1, containing comprehensive clinical data from Beth Israel Deaconess Medical Center (Boston, MA) between 2008 and 2022 [9]. Access was obtained through PhysioNet following required training. The study was reported in accordance with the STROBE guidelines [14] and the TRIPOD+AI guidelines [19]. As MIMIC-IV contains de-identified data, the Institutional Review Boards of BIDMC and MIT approved its use and waived the requirement for individual informed consent.

### 2.1b External Validation Data Source

External validation was performed using the eICU Collaborative Research Database (eICU-CRD) v2.0 [23], a multi-center ICU database containing over 200,000 admissions from 208 hospitals across the United States between 2014-2015. Access was obtained through PhysioNet. eICU-CRD provides a geographically and institutionally diverse validation cohort, complementing the single-center MIMIC-IV derivation cohort.

### 2.2 Study Population (Figure 1)

**Inclusion criteria**: (1) Age ≥18 years; (2) ICU admission via ED; (3) Acute abdomen ICD-9/10 diagnosis codes (Supplementary Table S1); (4) Complete vital signs (HR, SBP, DBP) within 24h of ICU admission.

**Exclusion criteria**: (1) Age <18 years; (2) Missing vital signs for SI calculation; (3) Missing extended covariates (lactate, WBC) for the complete-case analysis.

From 546,028 total MIMIC-IV admissions, 72,676 had acute abdomen ICD codes; 52,398 were adult ED admissions; 9,998 had ICU stays; 8,933 had complete vital signs (excluding 1,065 for age <18 or missing vital signs); and 5,728 had complete data for all extended covariates (excluding 3,205 for missing lactate [n=3,160] or WBC [n=45]) (Figure 1). The primary analysis cohort (complete cases, N=5,728) was used for all model comparisons. The 3,205 excluded patients had substantially lower severity than complete cases (in-hospital mortality 8.0% vs 19.9%, vasopressor use 12.0% vs 43.6%, mechanical ventilation 17.3% vs 52.5%), reflecting selection bias toward more severely ill patients who received arterial blood gas monitoring (Supplementary Table S8).

Acute abdomen was defined by ICD codes: appendicitis (K35-K38/540-543), biliary emergencies (K80-K83/574-576), pancreatitis (K85-K86/577), intestinal obstruction (K56/560), GI perforation (K25-K28 perforation, K63.1, K65/531-534 perforation, 569.83, 567), intestinal ischemia (K55.0/557.0), diverticulitis (K57/562), and strangulated hernia (K40-K46/550-553).

### 2.3 Acute Abdomen Subtype Classification

Four pathophysiological subtypes based on ICD diagnoses: (1) Perforation—visceral perforation and peritonitis; (2) Obstruction—mechanical/functional bowel obstruction; (3) Inflammation—acute inflammatory conditions without perforation; (4) Ischemia—acute mesenteric/intestinal ischemia. Priority: perforation > ischemia > obstruction > inflammation > other. Patients not meeting specific subtype criteria were classified as "other" (29.9%, N=1,712), a heterogeneous group that includes secondary diagnoses and complications alongside primary acute abdomen codes (Supplementary Table S5). A sensitivity analysis excluding the "Other" subtype was performed (Section 3.4).

### 2.4 Shock Index-Derived Parameters

All parameters calculated from vital signs within 24h of ICU admission:
- **SI** = HR / SBP
- **MSI** = HR / MAP [MAP = (2×DBP + SBP)/3]
- **DSI** = HR / DBP
- **Age-SI** = SI × (Age / 10)

Three temporal metrics: first recorded, maximum, and 24-hour mean. Blood pressure was extracted from chartevents using a hierarchical priority: arterial line > non-invasive BP > manual entries.

### 2.5 Outcomes

**Primary**: In-hospital mortality (hospital_expire_flag from admissions table). This captures both deaths during the ICU stay and deaths after ICU discharge but during the same hospitalization, providing a more clinically comprehensive endpoint than ICU-specific mortality alone. Among 1,141 in-hospital deaths, 383 (33.6%) occurred after ICU discharge, highlighting the clinical importance of this endpoint.

**Secondary**: Strict ICU mortality (death occurring during the specific ICU stay).

### 2.6 Covariates

**Basic baseline**: age, gender, Charlson Comorbidity Index (CCI) [10].

**Extended baseline (primary model)**: age, gender, CCI, first lactate (within 24h), first WBC (within 24h), vasopressor use (binary; any administration of norepinephrine, epinephrine, dopamine, vasopressin, or phenylephrine within 24h), mechanical ventilation (binary; any ventilator support within 24h), and SOFA score (computed within 24h following the standard MIMIC-IV concept definition) [20]. **Abdominal surgery was excluded from the primary model** because the surgery covariate ("any abdominal surgical procedure during the hospitalization") includes procedures occurring after the outcome (death), introducing survivorship bias: patients who survive long enough to undergo surgery are inherently selected. In our cohort, 67.4% had surgery "during hospitalization" but only 5.1% had surgery ≤24h from ICU admission, confirming that the vast majority of surgical procedures occurred well after ICU admission. A model including surgery is reported as an alternative (Section 3.3, Table 2b).

### 2.7 Statistical Analysis

**ROC/AUC**: With DeLong method comparisons [16]. Bootstrap 95% CI for AUC using 500 resamples. **Multicollinearity**: Variance inflation factors (VIF), with VIF>5 indicating potential multicollinearity. **Multivariable logistic regression**: Three model levels—basic baseline, extended baseline (without surgery; including SOFA), extended + DSI.

**NRI/IDI**: Categorical NRI using clinically meaningful risk thresholds (<10%, 10-30%, >30%) as the primary reclassification metric, with category-free (continuous) NRI [17] as a secondary measure. We acknowledge that ΔAUC=0.005 is below conventional clinical relevance thresholds (≥0.02 per Cook [24] and Vickers [25]), and that categorical NRI crossing zero indicates DSI does not reclassify patients across clinically relevant risk strata. IDI significance via Z-test. Bootstrap 95% CI (1000 resamples).

**DCA**: Clinical net benefits across threshold probabilities 1-50% [12].

**RCS**: 4-knot restricted cubic spline within logistic regression (5th, 35th, 65th, 95th percentiles), adjusting for age, gender, CCI [13].

**Time-to-event**: Kaplan-Meier curves stratified by DSI quartile using hospital LOS as time axis (Supplementary Figure S2). Cumulative incidence functions for competing risks (in-hospital death vs discharge alive) by DSI quartile [15].

**Calibration**: Hosmer-Lemeshow test, Brier score, calibration plots.

**Bootstrap internal validation**: 200 resamples for optimism-corrected AUC.

**Sensitivity analyses**: (1) Excluding early deaths (ICU LOS<24h); (2) Different measurement windows (first vs max vs mean); (3) Surgical vs non-surgical subgroups; (4) Subtype-specific models; (5) Model including surgery as alternative covariate; (6) Surgery ≤24h model; (7) Multiple imputation (5 imputations, IterativeImputer) on full dataset (N=8,933); (8) ICU type restriction (MICU/SICU/TSICU); (9) Excluding "Other" subtype; (10) Parsimonious model (age+sex+CCI+lactate+WBC+SOFA); (11) Model without vasopressor and MV (retaining surgery); (12) Primary subtypes only (inflammation/obstruction/perforation/ischemia).

**TRIPOD+AI compliance**: 27-item checklist provided (Supplementary Table S4). Full model coefficients reported per TRIPOD+AI guidelines [19].

### 2.8 External Validation

The MIMIC-IV-trained models were applied to eICU-CRD without retraining coefficients (per TRIPOD+AI type 2b/3b [19]). The eICU validation cohort used identical inclusion/exclusion criteria: adult ICU patients with acute abdomen ICD-9/10 codes and complete vital signs and covariates (HR, SBP, DBP, lactate, WBC) within 24h. DSI was calculated as HR/DBP using mean 24h values, identical to derivation methodology. Blood pressure was extracted from vitalPeriodic (invasive) and vitalAperiodic (non-invasive) tables with the same hierarchical priority.

**Important methodological note**: SOFA scores were computed from APACHE APS variables (GCS components, creatinine, bilirubin) combined with extracted vasopressor, MV, and laboratory data. While the component-based approach followed the same conceptual framework as the derivation cohort, the specific data sources differed: eICU SOFA lacked platelets (hematocrit substituted) and used APS-based rather than MIMIC-IV concept-based definitions. This methodological heterogeneity is reflected in the higher eICU median SOFA (9 [7-12] vs MIMIC-IV 7 [4-11]). Both un-recalibrated and recalibrated performance metrics are reported per TRIPOD+AI guidelines [19].

Performance assessed via: (1) AUC with DeLong test; (2) Logistic recalibration (adjusting intercept and slope per TRIPOD [11,19]) followed by HL test and Brier score, with un-recalibrated metrics also reported; (3) Category-free NRI and IDI; (4) DSI quartile mortality gradient using derivation cutoffs.

All analyses: Python 3.13 (pandas, scipy, statsmodels, scikit-learn, matplotlib, DuckDB). P<0.05 = significant.

---

## 3. Results

### 3.1 Study Population

From 546,028 MIMIC-IV admissions, 5,728 complete-case ICU stays with acute abdomen were analyzed (Figure 1). Median age 68 [IQR 57-79] years, 56.0% male, in-hospital mortality 19.9% (n=1,141). Median SOFA 7 [IQR 4-11]; significantly higher in non-survivors (11 [8-15] vs 6 [4-10], P=2.95×10⁻¹⁴⁰). Among 1,141 hospital deaths, 758 (66.4%) occurred during the ICU stay and 383 (33.6%) after ICU discharge. Baseline: vasopressor use 43.6%; mechanical ventilation 52.5%; lactate 2.0 [1.3-3.2] mmol/L; WBC 11.6 [7.5-16.9] ×10⁹/L; CCI 3 [1-5]; ICU LOS 2.7 [1.5-5.8] days. Subtype distribution: inflammation (37.5%), other (29.9%), obstruction (20.6%), ischemia (6.2%), perforation (5.8%).

**Selection bias assessment**: The 36% exclusion rate (8,933→5,728) was primarily driven by lactate non-availability (99% of excluded patients lacked lactate). Excluded patients (N=3,205) had substantially lower severity: in-hospital mortality 8.0% vs 19.9%, vasopressor use 12.0% vs 43.6%, mechanical ventilation 17.3% vs 52.5%, and surgery 61.2% vs 67.4% (Supplementary Table S8). This confirms selection bias toward more severely ill patients who received arterial blood gas monitoring. Multiple imputation on the full dataset (N=8,933) addressed this bias (Section 3.4).

### 3.2 DSI Quartile and Mortality Gradient (Table 1)

DSI (mean 24h) quartile cutoffs: Q1<1.279, Q2 1.279-1.502, Q3 1.502-1.762, Q4>1.762. DSI quartile demonstrated a dramatic in-hospital mortality gradient (χ²=229.24, P=2.02×10⁻⁴⁹):

| DSI Quartile | Cutoff | N | In-Hospital Death (%) | ICU Death (%) | Lactate (median) | Vasopressor (%) | MV (%) |
|---|---|---|---|---|---|---|---|
| Q1 (Low) | <1.279 | 1,432 | 12.1% (173) | 6.6% | 1.7 | 27.6% | 42.0% |
| Q2 | 1.279-1.502 | 1,432 | 14.5% (208) | 7.6% | 1.9 | 39.2% | 49.2% |
| Q3 | 1.502-1.762 | 1,432 | 20.3% (291) | 13.0% | 2.0 | 47.3% | 55.8% |
| Q4 (High) | >1.762 | 1,432 | 32.8% (469) | 25.8% | 2.6 | 60.3% | 63.0% |

Higher DSI quartile was associated with progressively higher lactate (KW P<10⁻⁵³), vasopressor use, and MV rates. Cumulative incidence functions demonstrated progressive divergence across DSI quartiles (Figure 8).

### 3.3 Primary Model Analysis (Table 2a, 2b)

The **primary extended baseline model (without surgery)** achieved AUC=0.785 (95% CI 0.769-0.801), substantially outperforming the basic baseline (AUC=0.626, 95% CI 0.609-0.644). Adding DSI yielded:

**Table 2a. Primary model performance (without surgery)**

| Model | AUC (95% CI) | DeLong P vs Extended | Categorical NRI | Category-free NRI | IDI |
|---|---|---|---|---|---|
| Basic baseline (Age+Sex+CCI) | 0.626 (0.609-0.644) | — | — | — | — |
| Extended baseline (no surgery; +SOFA) | 0.785 (0.769-0.801) | — | — | — | — |
| **Extended + DSI (primary)** | **0.790 (0.775-0.805)** | **0.012** | **0.008 (−0.009, 0.044)** | **0.252 (0.183, 0.331)** | **0.013 (0.007, 0.020)** |

DSI remained an independent predictor (OR=2.18, 95% CI 1.79-2.65, P=7.59×10⁻¹⁵) after adjusting for SOFA and all extended covariates. The ΔAUC was +0.005, statistically significant (DeLong P=0.012) but below conventional clinical relevance thresholds (ΔAUC≥0.02 per Cook [24] and Vickers [25]). The categorical NRI (0.008, 95% CI −0.009 to 0.044) had a confidence interval including zero, indicating that DSI does not significantly improve reclassification across the 10%/30% risk strata. The category-free NRI (0.252, 95% CI 0.183-0.331) and IDI (0.013, 95% CI 0.007-0.020) remained significant, confirming additional continuous prognostic information. VIF were all <3.0 (maximum: SOFA=2.42), confirming no problematic multicollinearity. Bootstrap validation confirmed minimal optimism (0.002).

**Table 2b. Alternative model (including surgery)**

| Model | AUC (95% CI) | DSI OR | Surgery OR |
|---|---|---|---|
| Extended baseline (with surgery; +SOFA) | 0.787 (0.771-0.800) | — | — |
| Extended + DSI (with surgery) | 0.792 (0.778-0.806) | 2.25 (1.85-2.74) | 0.68 (0.58-0.80) |

Including surgery increased baseline AUC by only 0.002 (0.785→0.787) and DSI AUC by 0.002 (0.790→0.792). Surgery appeared protective (OR=0.68, P=1.54×10⁻⁶), but this likely reflects survivorship bias: only 5.1% of patients had surgery ≤24h from ICU admission vs 67.4% "during hospitalization," confirming most surgical procedures occurred after surviving the acute crisis. The primary model without surgery is therefore preferred for causal interpretation, while the model with surgery is retained for completeness.

### 3.4 Sensitivity Analyses (Table 3)

| Analysis | N | AUC (Ext+SOFA+DSI) | DSI OR | Notes |
|---|---|---|---|---|
| **Primary model (no surgery)** | **5,728** | **0.790** | **2.18** | Primary |
| Model with surgery | 5,728 | 0.792 | 2.25 | Alternative |
| Surgery ≤24h model | 5,728 | 0.790 | 2.17 | Surgery_24h OR=0.88 (P=0.46) |
| Parsimonious (age+sex+CCI+lact+WBC+SOFA+DSI) | 5,728 | 0.789 | 2.22 | Minimal covariates |
| Non-surgical subgroup | 1,865 | 0.826 | 2.28 | Best performance |
| Surgical subgroup | 3,863 | 0.777 | 2.22 | |
| **Excluding "Other" subtype** | **4,016** | **0.788** | **2.22** | Primary subtypes only |
| Excl Other (no surgery) | 4,016 | 0.786 | 2.15 | |
| Inflammation subtype | 2,149 | 0.819 | — | |
| Obstruction subtype | 1,180 | 0.749 | — | |
| Perforation subtype | 334 | 0.766 | — | |
| Ischemia subtype | 353 | 0.807 | — | |
| MICU/SICU/TSICU only | 3,594 | 0.800 | 2.14 | |
| **Multiple imputation (N=8,933)** | **8,933** | **0.822** | **2.65** | Addresses selection bias |

Key findings: (1) DSI's independent predictive value was robust across all 12 sensitivity analyses (OR range 2.15-2.65, all P<10⁻¹¹); (2) Removing surgery changed baseline AUC by only 0.002 and DSI ΔAUC remained 0.005, confirming surgery's contribution is minimal and likely biased; (3) Excluding the heterogeneous "Other" subtype (N=4,016) preserved DSI's predictive value (AUC=0.788, OR=2.22); (4) Multiple imputation on N=8,933 confirmed DSI's value with higher AUC estimates, addressing the selection bias from complete-case analysis; (5) Non-surgical subgroup showed best performance (AUC=0.826).

### 3.5 Incremental Value over Basic Baseline (Figures 2-3)

For context with prior SI-derivative literature, NRI/IDI relative to the basic baseline model:

| Metric added to basic baseline | AUC | Categorical NRI | Category-free NRI | IDI |
|---|---|---|---|---|
| SI (mean 24h) | 0.695 | 0.140 | 0.302 | 0.030 |
| MSI (mean 24h) | 0.691 | 0.125 | 0.287 | 0.028 |
| **DSI (mean 24h)** | **0.692** | **0.148** | **0.315** | **0.029** |
| Age-SI (mean 24h) | 0.695 | 0.115 | 0.278 | 0.029 |

### 3.6 DCA (Figure 3)

At clinically relevant thresholds (5-25%), the extended+DSI model provided superior net benefits over the basic baseline. At 10% threshold, extended+DSI net benefit=0.128 vs extended baseline=0.126, a modest incremental benefit of 0.002. The extended baseline itself provided substantial improvement over basic baseline (net benefit 0.112 at 10%).

### 3.7 RCS Analysis (Figure 4, Table 4)

Significant overall associations (P_overall<0.001) for all four SI derivatives. No significant nonlinear components (all P_nonlinear>0.05), supporting linear dose-response relationships:

**Table 4. RCS analysis**

| Metric | P_overall | P_nonlinear | Knots |
|---|---|---|---|
| SI | <0.001 | 0.550 | 0.54, 0.70, 0.83, 1.08 |
| MSI | <0.001 | 0.615 | 0.86, 1.06, 1.24, 1.54 |
| DSI | <0.001 | 0.391 | 1.05, 1.32, 1.55, 1.94 |
| Age-SI | <0.001 | 0.123 | 3.16, 4.56, 5.64, 7.60 |

### 3.8 Time-to-Event Analysis (Supplementary Figure S2, Table 5)

DSI quartile showed significant survival separation (Log-rank χ²=71.2, P=2.33×10⁻¹⁵). These KM curves are a visual supplement; the primary competing risk analysis (CIF, Figure 8) is more rigorous.

### 3.9 Calibration (Figure 5, Table 6)

Extended+DSI (no surgery): HL P=0.691, Brier=0.126. Extended baseline (no surgery): HL P=0.491, Brier=0.128. Basic baseline: poorly calibrated (HL P=0.016, Brier=0.155).

**Table 6. Calibration metrics**

| Model | Brier | HL P |
|---|---|---|
| Basic baseline | 0.155 | 0.016 |
| Extended (no surgery; +SOFA) | 0.128 | 0.491 |
| Extended + DSI (no surgery) | 0.126 | 0.691 |
| Extended + all SI derivatives | 0.125 | 0.286 |

### 3.10 Multivariable Regression (Figure 6, Table 7)

In the primary model (extended baseline without surgery + DSI), DSI (OR=2.18, 95% CI 1.79-2.65, P=7.59×10⁻¹⁵) remained a strong independent predictor after adjusting for age, sex, CCI, lactate, WBC, vasopressor use, MV, and SOFA. SOFA (OR=1.16 per point, P<10⁻³⁶), lactate (OR=1.14, P<10⁻²⁰), and CCI (OR=1.14, P<10⁻²⁵) were also significant. Vasopressor use (P=0.14) and mechanical ventilation (P=0.45) were not independently significant after SOFA adjustment, consistent with SOFA absorbing their predictive information (SOFA's cardiovascular component includes vasopressor doses; respiratory component includes MV). Full coefficients in Supplementary Table S6.

**Table 7. Primary model: extended baseline (no surgery) + DSI**

| Variable | OR | 95% CI | P |
|---|---|---|---|
| Age (per year) | 1.022 | 1.016-1.027 | 2.98×10⁻¹⁶ |
| Male gender | 0.88 | 0.76-1.02 | 0.084 |
| CCI (per point) | 1.14 | 1.11-1.16 | 8.10×10⁻²⁵ |
| Lactate (per mmol/L) | 1.14 | 1.11-1.17 | 1.14×10⁻²⁰ |
| WBC (per ×10⁹/L) | 1.006 | 1.000-1.012 | 0.074 |
| Vasopressor use | 1.14 | 0.96-1.36 | 0.14 |
| Mechanical ventilation | 1.08 | 0.89-1.31 | 0.45 |
| SOFA (per point) | 1.16 | 1.13-1.19 | 4.83×10⁻³⁶ |
| **DSI (mean 24h)** | **2.18** | **1.79-2.65** | **7.59×10⁻¹⁵** |

### 3.11 Subgroup Analysis (Figure 7)

**Inflammation** (n=2,149, mortality 16.8%): AUC=0.819. **Obstruction** (n=1,180, 21.5%): AUC=0.749. **Perforation** (n=334, 28.1%): AUC=0.766. **Ischemia** (n=353, 40.5%): AUC=0.807. **Other** (n=1,712, 16.9%): AUC=0.808. **Non-surgical** (n=1,865, 20.9%): AUC=0.826—best performance. **Surgical** (n=3,863, 19.5%): AUC=0.777.

### 3.12 External Validation in eICU-CRD

The model was externally validated in eICU-CRD [23] (N=5,755, 208 hospitals). From 17,576 acute abdomen ICU stays, 5,755 had complete data (CC rate 32.6%). Demographics: median age 66 [55-78], 56.4% male, mortality 20.0%. Median SOFA 9 [7-12] (higher than MIMIC-IV 7 [4-11], reflecting methodological differences in SOFA computation and case-mix).

**Discrimination**: Extended baseline AUC=0.785, extended+DSI AUC=0.792, closely replicating MIMIC-IV. ΔAUC=0.0074 (DeLong z=3.011, P=0.0026), larger than derivation ΔAUC=0.005.

**Calibration**: Direct application yielded poor calibration (un-recalibrated Brier=0.383-0.588, HL P<0.001) due to baseline mortality differences. After logistic recalibration (intercept shift −3.935, slope=0.952): extended+DSI Brier=0.126, HL P=0.266. The large intercept shift indicates that while discrimination is transportable (slope near 1.0), absolute risk predictions require local recalibration before clinical deployment.

**NRI/IDI**: cf-NRI=0.277 (P<0.001), IDI=0.014 (P<0.001).

**DSI quartile gradient**: Q1=12.0%, Q2=13.9%, Q3=17.1%, Q4=33.5%. Q1→Q4 gradient 2.8-fold, closely replicating MIMIC-IV (2.7-fold). Note: eICU quartile sizes were unequal (Q1=1,294, Q4=1,677) due to applying derivation cutoffs to a different DSI distribution.

**Table 8. External validation: eICU-CRD vs MIMIC-IV**

| Metric | MIMIC-IV (Derivation) | eICU-CRD (Validation) |
|---|---|---|
| N (CC) | 5,728 | 5,755 |
| In-hospital mortality | 19.9% | 20.0% |
| Median SOFA [IQR] | 7 [4-11] | 9 [7-12] |
| Extended baseline AUC | 0.785 | 0.785 |
| Extended+DSI AUC | 0.790 | 0.792 |
| ΔAUC | 0.005 | 0.0074 |
| DeLong P | 0.012 | 0.0026 |
| Brier (recalibrated) | 0.126 | 0.126 |
| HL P (recalibrated) | 0.691 | 0.266 |
| **Brier (un-recalibrated)** | **0.128** | **0.383-0.588** |
| **HL P (un-recalibrated)** | **0.491** | **<0.001** |
| **Recal intercept shift** | — | **−3.935** |
| **Recal slope** | — | **0.952** |
| cf-NRI | 0.252 | 0.277 |
| IDI | 0.013 | 0.014 |
| DSI Q1 mortality | 12.1% | 12.0% |
| DSI Q4 mortality | 32.8% | 33.5% |

---

## 4. Discussion

This study provides a comprehensive evaluation of shock index-derived parameters in acute abdomen ICU patients, with SOFA adjustment, bootstrap validation, multiple imputation, 12 sensitivity analyses, competing risk framework, external validation, and STROBE/TRIPOD+AI-compliant reporting. Eight principal findings emerge.

**First**, DSI is an independent predictor of in-hospital mortality after adjusting for SOFA and established ICU covariates (OR=2.18, 95% CI 1.79-2.65, P=7.59×10⁻¹⁵). The incremental AUC was modest (ΔAUC=0.005) and below conventional clinical relevance thresholds (≥0.02 per Cook [24] and Vickers [25]). The categorical NRI (0.008, 95% CI −0.009 to 0.044) crossed zero, indicating DSI does not reclassify patients across clinically relevant risk strata (10%/30%) beyond a model already containing SOFA and lactate. This pattern is expected when a marker refines continuous risk prediction without shifting categorical decision thresholds [25]. The category-free NRI and IDI remained significant, confirming additional continuous prognostic information, but their clinical interpretation is less established than categorical NRI. Therefore, we position DSI not as a replacement for SOFA-based risk models, but as a **complementary, zero-cost bedside tool** that provides independent risk information from routinely monitored vital signs (HR and DBP), available without laboratory turnaround time. DSI's clinical value lies in its immediate availability for risk stratification when SOFA data (platelets, bilirubin, creatinine, PaO₂, vasopressor doses) are pending.

**Second**, the DSI quartile mortality gradient (12.1%→32.8%, 2.7-fold, P=2.02×10⁻⁴⁹) provides clinically actionable risk thresholds (Q1<1.279, Q2 1.279-1.502, Q3 1.502-1.762, Q4>1.762). Higher DSI quartiles were associated with progressively higher lactate, vasopressor use, and MV rates, confirming DSI as an integrative marker of hemodynamic severity.

**Third**, 33.6% of hospital deaths (383/1,141) occurred after ICU discharge, highlighting the clinical importance of in-hospital mortality as the primary endpoint. Patients surviving ICU but later dying in-hospital represent a population where DSI-based risk stratification could guide post-ICU monitoring.

**Fourth**, bootstrap validation confirmed minimal optimism (0.002), indicating robust performance without overfitting.

**Fifth**, sensitivity analyses confirmed DSI's robustness across 12 scenarios. Key findings: removing surgery from the model changed AUC by only 0.002 (0.785→0.787 baseline; 0.790→0.792 with DSI), confirming surgery's minimal and likely biased contribution. Excluding the heterogeneous "Other" subtype preserved DSI's value (AUC=0.788, OR=2.22). Multiple imputation (N=8,933) confirmed DSI with higher estimates (AUC=0.822, OR=2.65), addressing selection bias.

**Sixth**, RCS confirmed significant dose-response relationships (P_overall<0.001) with linear patterns (all P_nonlinear>0.05).

**Seventh**, SOFA was the strongest predictor (OR=1.16/point, P<10⁻³⁶). Vasopressor use and MV were not significant after SOFA adjustment (P=0.14 and 0.45), consistent with SOFA absorbing their information. DSI's independent association persists, suggesting HR/DBP captures a hemodynamic dimension not fully represented by SOFA's cardiovascular component (vasopressor doses and MAP).

**Eighth**, external validation in eICU-CRD [23] (N=5,755, 208 hospitals) preserved discrimination (AUC=0.792, ΔAUC=0.0074, DeLong P=0.0026). However, direct application yielded poor calibration (Brier=0.38-0.59, HL P<0.001), requiring logistic recalibration (intercept shift −3.935, slope=0.952). The near-ideal slope confirms discrimination transportability, but the large intercept shift indicates that absolute risk predictions require local recalibration—clinicians in a new setting cannot directly apply MIMIC-IV-derived risk estimates without adjustment for local case-mix. The DSI quartile gradient was closely replicated (Q1=12.0%→Q4=33.5%). Methodological differences in SOFA computation between databases (eICU SOFA from APACHE APS variables vs MIMIC-IV concept definition; eICU median 9 vs MIMIC-IV 7) limit the interpretation of "identical methodology" and represent a source of heterogeneity. The eICU data (2014-2015) also represents an older practice era than MIMIC-IV (2008-2022).

### 4.1 Pathophysiological Rationale for DSI

DSI (HR/DBP) captures the relationship between cardiac output proxy (HR) and diastolic perfusion pressure (DBP). In acute abdomen, progressive vasodilation from inflammatory mediators and splanchnic vascular compromise first manifests as diastolic pressure decline—reflecting loss of peripheral vascular tone before systolic compensatory mechanisms fail. This makes DSI more sensitive to early hemodynamic deterioration than SI (HR/SBP). The original DSI description by Ospina-Tascón et al. [5] in septic shock demonstrated HR-to-DAP ratios associated with mortality, and our findings extend this to acute abdomen.

### 4.2 Comparison with Previous Studies

Our results extend Jouffroy et al. [4], Ospina-Tascón et al. [5], and Hou et al. [18] by demonstrating DSI's independent predictive value beyond SOFA. The successful external validation in eICU-CRD (208 hospitals, AUC=0.792 preserved) substantially strengthens generalizability evidence—a key gap in prior SI-derivative studies. DSI has emerged as a research focus, with a narrative review [21] and conference abstract [22]—yet no prior study evaluated DSI in acute abdomen specifically.

### 4.3 Clinical Implications

DSI provides risk stratification with: (1) independent predictive value (OR=2.18); (2) dramatic quartile gradient (12.1%→32.8%); (3) zero-cost bedside availability from routine vitals; (4) validated in eICU-CRD (208 hospitals). In ischemia (mortality 40.5%), DSI showed good discrimination (AUC=0.807). The 33.6% post-ICU death rate underscores that DSI should guide post-ICU monitoring. The non-surgical subgroup AUC=0.826 suggests particular utility in pre-operative assessment. However, clinicians should understand that DSI complements rather than replaces SOFA: ΔAUC below clinical thresholds and categorical NRI crossing zero mean DSI should not be used to override SOFA-based categorical risk classifications, but rather to provide immediate risk stratification when laboratory data are unavailable.

### 4.4 Limitations

(1) Single-center retrospective derivation from a US tertiary hospital, though externally validated in multi-center eICU-CRD (208 hospitals); (2) **Selection bias**: 36% exclusion (primarily lactate) enriched the CC cohort with more severely ill patients (mortality 19.9% vs 8.0% in excluded, vasopressor 43.6% vs 12.0%). Multiple imputation on N=8,933 addressed this, yielding consistent results with higher estimates. The eICU validation also used CC (32.6% rate), creating a parallel selection bias; (3) **ΔAUC below clinical relevance**: ΔAUC=0.005 is below the ≥0.02 threshold [24,25]; categorical NRI crossing zero indicates DSI does not improve reclassification across clinically relevant thresholds; DSI should be positioned as a complementary bedside tool, not a replacement for SOFA-based models; (4) **Surgery survivorship bias**: "Surgery during hospitalization" (67.4%) includes procedures after the outcome; only 5.1% had surgery ≤24h. Surgery was removed from the primary model; the alternative model with surgery is retained for completeness; (5) **"Other" subtype heterogeneity** (29.9%): includes complications (D62 posthemorrhagic anemia, N179 AKI, R6521 septic shock, A419 sepsis) alongside primary acute abdomen codes; sensitivity excluding "Other" preserved results; (6) No formal Fine-Gray subdistribution hazard model; CIF curves are descriptive; (7) **eICU SOFA heterogeneity**: computed from APACHE APS variables rather than identical MIMIC-IV concept definition; eICU median 9 vs MIMIC-IV 7; platelets substituted by hematocrit; this limits "identical methodology" claims; (8) **Recalibration required**: intercept shift −3.935 means MIMIC-IV-derived absolute risk estimates cannot be directly applied to new settings without local recalibration; discrimination (slope 0.952) is transportable; (9) eICU data (2014-2015) represents an older practice era; (10) WBC borderline (P=0.07 in primary model without surgery); (11) Vasopressor use and MV not significant after SOFA adjustment; (12) Only 2 authors; (13) Blood pressure source (arterial vs NIBP) not recorded as separate variable.

### 4.5 Future Directions

Prospective multicenter validation with standardized SOFA computation; Fine-Gray subdistribution hazard modeling; DSI trajectory analysis as dynamic risk markers; integration with machine learning; validation in non-US populations; assessment of whether DSI quartile thresholds can guide clinical decision-making (e.g., ICU admission, post-ICU monitoring intensity).

---

## 5. Conclusions

DSI is an independent predictor of in-hospital mortality in acute abdomen after adjusting for SOFA and established ICU covariates (OR=2.18, 95% CI 1.79-2.65), providing zero-cost bedside risk stratification with a dramatic quartile mortality gradient (12.1%→32.8%, 2.7-fold). While the incremental AUC is statistically significant (ΔAUC=0.005, DeLong P=0.012) but below clinical relevance thresholds (≥0.02), and the categorical NRI crosses zero—indicating DSI does not replace SOFA for categorical decision-making—the independent OR, category-free NRI (0.252), IDI (0.013), and quartile gradient support DSI as a complementary, immediately available risk-stratification tool when laboratory data are pending. External validation in eICU-CRD (N=5,755, 208 hospitals) confirmed discrimination transportability (AUC=0.792) and replicated the quartile gradient, though calibration required local recalibration (intercept shift −3.935). Surgery was excluded from the primary model due to survivorship bias. The 33.6% post-ICU death rate underscores in-hospital mortality as the appropriate endpoint. Prediction was most pronounced in non-surgical acute abdomen (AUC=0.826). DSI, calculated from routinely monitored HR and DBP, may enhance early bedside risk stratification in this heterogeneous population as a complementary tool to SOFA.

---

## Supplementary Materials

**Table S1**: ICD-9/10 codes for acute abdomen identification and subtype classification.

**Table S2**: STROBE checklist (completed).

**Table S3**: Baseline characteristics (N=5,728) by DSI quartile, including SOFA.

**Table S4**: TRIPOD+AI checklist (27 items) [19].

**Table S5**: ICD code composition of "Other" subtype (N=1,712).

**Table S6**: Full model coefficients (primary model without surgery + DSI) per TRIPOD+AI guidelines.

**Table S7**: eICU-CRD baseline characteristics (N=5,755) by DSI quartile.

**Table S8**: Comparison of excluded (N=3,205) vs complete-case (N=5,728) patient characteristics, demonstrating selection bias.

**Figure S1**: Calibration plots for basic baseline models.

**Figure S2**: Kaplan-Meier curves by DSI quartile.

---

## Figure Legends

**Figure 1**: Flow diagram (546,028→5,728 CC), with excluded patient characteristics in Supplementary Table S8.

**Figure 2**: ROC curves (basic, extended, extended+DSI, extended+all SI derivatives).

**Figure 3**: DCA net benefit across threshold probabilities.

**Figure 4**: RCS curves for SI, MSI, DSI, Age-SI.

**Figure 5**: Calibration plots (4 model levels).

**Figure 6**: Forest plot of adjusted ORs (primary model without surgery + DSI).

**Figure 7**: Subgroup ROC curves by subtype.

**Figure 8**: Cumulative incidence functions for in-hospital death by DSI quartile.

**Figure 9**: ROC curves (extended, extended+DSI, extended+all SI derivatives).

---

## Declarations

**Ethics**: MIMIC-IV and eICU-CRD are publicly available with IRB approval (BIDMC, MIT). Individual consent waived for de-identified data.

**Funding**: GWJJMB202510024181 (National Health Commission), kq2014242 (Changsha Science and Technology Bureau), 2021JJ30959 (Hunan Provincial Natural Science Foundation). Funders had no role in study design, analysis, or publication.

**Conflicts**: Authors declare no conflicts.

**CRediT**: Jiqiang Liu: Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Software, Validation, Visualization, Writing – original draft. Dengke Wu: Conceptualization, Funding acquisition, Methodology, Project administration, Resources, Supervision, Writing – review & editing.

**Acknowledgments**: We thank the MIMIC-IV and eICU-CRD teams for open access to clinical databases.

**Data availability**: MIMIC-IV v3.1 at https://physionet.org/content/mimiciv/3.1/. eICU-CRD v2.0 at https://physionet.org/content/eicu-crd/2.0/. Code available on request.

---

## References

1. Flum DR. Acute abdomen. In: Sabiston Textbook of Surgery. 21st ed. Elsevier; 2022.
2. Cervero F, Laird JM. Visceral pain. Lancet. 1999;353(9170):2145-2148.
3. Allgöwer M, Burri C. Schockindex. Deutsche Med Wochenschr. 1967;92(43):1947-1950.
4. Jouffroy R, Gille S, Gilbert B, et al. Shock index derivatives and 28-day mortality in prehospital septic shock. J Emerg Med. 2024;66(2):144-153.
5. Ospina-Tascón GA, Teboul JL, Hernandez G, et al. Diastolic shock index and clinical outcomes in septic shock. Ann Intensive Care. 2020;10:41. doi:10.1186/s13613-020-00658-8.
6. Kim SY, Hong KJ, Shin SD, et al. Validation of shock indices for predicting geriatric trauma mortality. J Korean Med Sci. 2016;31(12):2026-2032.
7. Olaussen A, Peterson G, Synnot A, et al. Shock index and mortality in trauma: systematic review. Crit Care. 2023;27:88.
8. Liu YC, Lee CT, Su HY, et al. Shock indices and in-hospital mortality in sepsis. PLoS One. 2024;19(3):e0298617.
9. Johnson AEW, Bulgarelli L, Pollard TJ, et al. MIMIC-IV. Sci Data. 2023;10:1.
10. Charlson ME, Pompei P, Ales KL, MacKenzie CR. Comorbidity classification. J Chronic Dis. 1987;40(5):373-383.
11. Steyerberg EW, Vergouwe Y. Better clinical prediction models: seven steps. Eur Heart J. 2014;35(29):1925-1931.
12. Vickers AJ, Elkin EB. Decision curve analysis. Med Decis Making. 2006;26(6):565-574.
13. Desquilbet L, Mariotti F. Dose-response via RCS. Am J Epidemiol. 2010;172(12):1377-1385.
14. von Elm E, Altman DG, Egger M, et al. STROBE statement. Lancet. 2007;370(9596):1453-1457.
15. Fine JP, Gray RJ. Proportional hazards model for competing risks. J Am Stat Assoc. 1999;94(446):496-509.
16. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing AUCs. Biometrics. 1988;44(3):837-845.
17. Pencina MJ, D'Agostino RB, et al. Evaluating added predictive ability. Stat Med. 2008;27(2):157-172.
18. Hou N, Li Z, Hu M, et al. MSI and mortality in emergency patients. Front Cardiovasc Med. 2022;9:915881.
19. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement. BMJ. 2024;385:e078378.
20. Vincent JL, Moreno R, Takala J, et al. SOFA score. Intensive Care Med. 1996;22(7):707-710.
21. Owattanapanich N, Boonchana N. DSI in critically ill patients: narrative review. Clin Crit Care. 2025;33(1):e250005.
22. Mirani HG. DSI as failure-to-normalize marker. Infectious Diseases Congress 2026; Birmingham, UK. [Conference abstract].
23. Pollard TJ, Johnson AEW, Raffa JD, et al. eICU-CRD. Sci Data. 2018;5:180175.
24. Cook NR. Use and misuse of the receiver operating characteristic curve in risk prediction. Circulation. 2007;115(7):928-935.
25. Vickers AJ, Cronin AM, Begg CB. One statistical test is sufficient for assessing prediction model performance. Med Decis Making. 2008;28(5):525-529.
