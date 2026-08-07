# Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV

**Jiqiang Liu** [1]†, **Dengke Wu** [1]*

[1] Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China

† First author.

* Corresponding author: Dengke Wu, Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China. Electronic address: wudk2010@csu.edu.cn

---

## Abstract

**Background**: Shock index (SI) and its derivatives—modified shock index (MSI), diastolic shock index (DSI), and age-adjusted shock index (Age-SI)—have demonstrated predictive value in trauma and sepsis, yet their utility in acute abdomen remains unexplored. This study evaluated SI-derived parameters for in-hospital mortality prediction in acute abdomen, including incremental value beyond established ICU covariates including SOFA scores.

**Methods**: This retrospective cohort study utilized MIMIC-IV v3.1. Adult ICU patients with acute abdomen diagnoses were included. SI, MSI, DSI, and Age-SI were calculated from vital signs within 24 hours of ICU admission. Primary outcome was in-hospital mortality. Predictive performance was assessed using ROC/AUC, net reclassification improvement (NRI) with bootstrap 95% confidence intervals, integrated discrimination improvement (IDI), decision curve analysis (DCA), restricted cubic spline (RCS), cumulative incidence functions, calibration, and bootstrap internal validation. Models were constructed at three levels: (1) basic baseline (age+sex+CCI); (2) extended baseline (age+sex+CCI+lactate+WBC+vasopressor use+surgery+mechanical ventilation+SOFA); (3) extended baseline + SI derivatives. Multiple imputation, ICU type restriction, and surgery timing sensitivity analyses were performed. Reporting followed STROBE and TRIPOD+AI guidelines.

**Results**: Among 5,728 complete-case ICU stays (median age 68 [IQR 57-79] years, 56.0% male, in-hospital mortality 19.9%, median SOFA 7 [IQR 4-11]), the extended baseline model achieved AUC=0.787 (95% CI 0.771-0.800; optimism-corrected 0.788). Adding DSI (mean 24h) improved AUC to 0.792 (95% CI 0.778-0.806; ΔAUC=+0.005; DeLong P=0.012; categorical NRI=0.008, 95% CI −0.009 to 0.044; category-free NRI=0.252, 95% CI 0.183-0.331; IDI=0.013, 95% CI 0.007-0.020; DSI OR=2.27, 95% CI 1.86-2.76, P=4.53×10⁻¹⁶). While the categorical NRI confidence interval included zero, the category-free NRI and IDI remained statistically significant, and DSI remained an independent predictor after adjusting for SOFA. No multicollinearity was detected (all VIF<3.0). DSI quartile cutoffs were Q1<1.279, Q2 1.279-1.502, Q3 1.502-1.762, Q4>1.762, with a dramatic mortality gradient: Q1=12.1%, Q2=14.5%, Q3=20.3%, Q4=32.8% (P=2.02×10⁻⁴⁹). Of 1,141 in-hospital deaths, 758 (66.4%) occurred during the ICU stay and 383 (33.6%) after ICU discharge. Multiple imputation (N=8,933) confirmed DSI's predictive value (AUC=0.822, OR=2.65). Sensitivity analyses across 12 scenarios yielded consistent results (AUC range 0.75-0.83). The non-surgical subgroup showed the best prediction (AUC=0.826).

**External validation**: The extended+DSI model was externally validated in the eICU Collaborative Research Database (N=5,755 complete-case acute abdomen ICU stays, in-hospital mortality 20.0%). The discrimination performance was remarkably preserved: extended baseline AUC=0.785, extended+DSI AUC=0.792, ΔAUC=0.0074 (DeLong P=0.0026). After logistic recalibration, calibration was adequate (Brier=0.126, HL P=0.266). The category-free NRI (0.277, P<0.001) and IDI (0.014, P<0.001) were significant. The DSI quartile mortality gradient was closely replicated: Q1=12.0%, Q2=13.9%, Q3=17.1%, Q4=33.5%.

**Conclusions**: DSI remained an independent predictor of in-hospital mortality in acute abdomen after adjusting for SOFA and established ICU covariates, with a statistically significant incremental AUC (ΔAUC=0.005, DeLong P=0.012) and no multicollinearity concerns. External validation in eICU-CRD confirmed model robustness with preserved discrimination (AUC=0.792, ΔAUC=0.0074, DeLong P=0.0026), adequate recalibrated calibration, and replicated quartile mortality gradient. The significant category-free NRI and IDI, dramatic quartile mortality gradient, and robust sensitivity analyses—including multiple imputation—support DSI as a practical, zero-cost risk-stratification tool. Prediction utility was most pronounced in non-surgical acute abdomen.

**Keywords**: Shock index; Diastolic shock index; Acute abdomen; In-hospital mortality; MIMIC-IV; eICU-CRD; External validation; SOFA; Risk stratification

---

## 1. Introduction

Acute abdomen—severe abdominal pain of sudden onset requiring urgent evaluation—remains one of the most challenging presentations in emergency medicine [1]. Early risk stratification is a critical unmet need, as outcomes vary dramatically across etiologies ranging from self-limiting inflammation to life-threatening intestinal ischemia [1,2].

The shock index (SI = HR/SBP), first described by Allgöwer and Burri in 1967 [3], has inspired several derived indices: modified shock index (MSI = HR/MAP) [4,18], diastolic shock index (DSI = HR/DBP) [5], and age-adjusted shock index (Age-SI = SI×Age/10) [6]. These have been validated in trauma [7] and sepsis [8], but never systematically evaluated in acute abdomen—a population with pathophysiological diversity including inflammation-driven vasodilation, mechanical obstruction, perforation-induced peritonitis, and ischemia-requiring reperfusion.

Moreover, previous SI-derivative studies have relied primarily on AUC comparisons without evaluating incremental value beyond established ICU predictors (lactate, vasopressor use, severity scores), nor assessing model robustness through bootstrap validation, sensitivity analyses, or competing risk frameworks. The TRIPOD+AI guidelines [17,19] emphasize that prediction models must demonstrate clinical benefit via NRI/IDI/DCA [17] and undergo internal validation [11]. This study was reported following the STROBE statement for observational studies [14] and the TRIPOD+AI guidelines for prediction model reporting [19].

This study aims to: (1) compare SI, MSI, DSI, and Age-SI for in-hospital mortality prediction in acute abdomen; (2) evaluate incremental value beyond extended covariates (lactate, WBC, vasopressor, surgery, mechanical ventilation, SOFA) using NRI with confidence intervals, IDI, and DCA; (3) assess model robustness via bootstrap validation, multiple imputation, and sensitivity analyses; (4) evaluate competing risks using cumulative incidence functions; and (5) determine subtype-specific prediction performance.

---

## 2. Methods

### 2.1 Study Design and Data Source

This retrospective cohort study utilized MIMIC-IV v3.1, containing comprehensive clinical data from Beth Israel Deaconess Medical Center (Boston, MA) between 2008 and 2022 [9]. Access was obtained through PhysioNet following required training. The study was reported in accordance with the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) guidelines [14] and the TRIPOD+AI guidelines [19]. As MIMIC-IV contains de-identified data, the Institutional Review Boards of BIDMC and MIT approved its use and waived the requirement for individual informed consent.

### 2.1b External Validation Data Source

External validation was performed using the eICU Collaborative Research Database (eICU-CRD) v2.0 [23], a multi-center ICU database containing over 200,000 admissions from 208 hospitals across the United States between 2014-2015. Access was obtained through PhysioNet following required training. eICU-CRD provides a geographically and institutionally diverse validation cohort, complementing the single-center MIMIC-IV derivation cohort.

### 2.2 Study Population (Figure 1)

**Inclusion criteria**: (1) Age ≥18 years; (2) ICU admission via ED; (3) Acute abdomen ICD-9/10 diagnosis codes (Supplementary Table S1); (4) Complete vital signs (HR, SBP, DBP) within 24h of ICU admission.

**Exclusion criteria**: (1) Age <18 years; (2) Missing vital signs for SI calculation; (3) Missing extended covariates (lactate, WBC) for the complete-case analysis.

From 546,028 total MIMIC-IV admissions, 72,676 had acute abdomen ICD codes; 52,398 were adult ED admissions; 9,998 had ICU stays; 8,933 had complete vital signs (excluding 1,065 for age <18 or missing vital signs); and 5,728 had complete data for all extended covariates (excluding 3,205 for missing lactate [n=3,160] or WBC [n=45]) (Figure 1). The primary analysis cohort (complete cases, N=5,728) was used for all model comparisons; descriptive statistics are also reported from this cohort for consistency.

Acute abdomen was defined by ICD codes: appendicitis (K35-K38/540-543), biliary emergencies (K80-K83/574-576), pancreatitis (K85-K86/577.0-577.1), intestinal obstruction (K56/560), GI perforation (K25-K28 perforation, K63.1, K65/531-534 perforation, 569.83, 567), intestinal ischemia (K55.0/557.0), diverticulitis (K57/562), and strangulated hernia (K40-K46/550-553).

### 2.3 Acute Abdomen Subtype Classification

Four pathophysiological subtypes based on ICD diagnoses: (1) Perforation—visceral perforation and peritonitis; (2) Obstruction—mechanical/functional bowel obstruction; (3) Inflammation—acute inflammatory conditions without perforation; (4) Ischemia—acute mesenteric/intestinal ischemia. Priority: perforation > ischemia > obstruction > inflammation > other. Patients not meeting specific subtype criteria were classified as "other" (Supplementary Table S5).

### 2.4 Shock Index-Derived Parameters

All parameters calculated from vital signs within 24h of ICU admission:
- **SI** = HR / SBP
- **MSI** = HR / MAP [MAP = (2×DBP + SBP)/3]
- **DSI** = HR / DBP
- **Age-SI** = SI × (Age / 10)

Three temporal metrics: first recorded, maximum, and 24-hour mean. Blood pressure was extracted from chartevents using a hierarchical priority: arterial line > non-invasive BP > manual entries, selecting the most reliable available source per patient.

### 2.5 Outcomes

**Primary**: In-hospital mortality (hospital_expire_flag from admissions table). This captures both deaths occurring during the ICU stay and deaths after ICU discharge but during the same hospitalization, providing a more clinically comprehensive endpoint than ICU-specific mortality alone.

**Secondary**: Strict ICU mortality (death occurring during the specific ICU stay, determined by deathtime falling within the ICU admission-to-discharge interval).

### 2.6 Covariates

**Basic baseline**: age, gender, Charlson Comorbidity Index (CCI) [10].

**Extended baseline**: age, gender, CCI, first lactate (within 24h of ICU admission), first WBC (within 24h), vasopressor use (any administration of norepinephrine, epinephrine, dopamine, vasopressin, or phenylephrine within 24h of ICU admission; binary), abdominal surgery (any abdominal surgical procedure during the hospitalization; binary), mechanical ventilation (any ventilator support within 24h of ICU admission; binary), and Sequential Organ Failure Assessment (SOFA) score (computed within the first 24h of ICU admission following the standard MIMIC-IV concept definition, encompassing six organ systems: respiration, coagulation, liver, cardiovascular, central nervous system, and renal) [20].

### 2.7 Statistical Analysis

**ROC/AUC**: With DeLong method comparisons [16]. Bootstrap 95% confidence intervals for AUC values were computed using 500 resamples. **Multicollinearity**: Variance inflation factors (VIF) were computed for all predictors in the extended model, with VIF>5 indicating potential multicollinearity. **Multivariable logistic regression**: Three model levels—basic baseline, extended baseline (including SOFA), extended + SI derivatives.

**NRI/IDI**: Categorical NRI using clinically meaningful risk thresholds (<10%, 10-30%, >30%) as the primary reclassification metric, with category-free (continuous) NRI [17] as a secondary measure. IDI significance via Z-test. Bootstrap 95% confidence intervals (1000 resamples) for both NRI and IDI.

**DCA**: Clinical net benefit across threshold probabilities 1-50% [12].

**RCS**: 4-knot restricted cubic spline within logistic regression (5th, 35th, 65th, 95th percentiles), adjusting for age, gender, CCI [13].

**Time-to-event analysis**: Kaplan-Meier curves stratified by DSI quartile, using hospital length of stay as the time axis (Supplementary Figure S2). As in-hospital mortality is a binary endpoint, these curves serve as a visual supplement to the primary competing risk analysis. Log-rank tests for group separation.

**Cumulative incidence functions**: For competing risks (in-hospital death vs discharge alive) by DSI quartile [15]. This is the primary method for evaluating the time-dependent probability of in-hospital death accounting for the competing risk of discharge.

**Calibration**: Hosmer-Lemeshow test, Brier score, calibration plots.

**Bootstrap internal validation**: 200 resamples for optimism-corrected AUC.

**Sensitivity analyses**: (1) Excluding early deaths (ICU LOS<24h); (2) Different measurement windows (first vs max vs mean 24h); (3) Surgical vs non-surgical subgroups; (4) Subtype-specific models; (5) Surgery redefined as ≤24h from ICU admission (to address temporal bias); (6) Multiple imputation (5 imputations using IterativeImputer with sample_posterior=True) on the full dataset (N=8,933); (7) ICU type restriction (MICU/SICU/TSICU only).

**TRIPOD+AI compliance**: The 27-item TRIPOD+AI checklist [19] is provided in Supplementary Table S4. Full model coefficients (intercept and all β coefficients) are reported to facilitate external validation and model deployment.

### 2.8 External Validation

The MIMIC-IV-trained extended baseline and extended+DSI models were applied to the eICU-CRD validation cohort without retraining model coefficients (per TRIPOD+AI type 2b/3b validation framework [19]). The eICU validation cohort was constructed using identical inclusion/exclusion criteria: adult ICU patients with acute abdomen ICD-9/10 diagnoses and complete vital signs and extended covariates (HR, SBP, DBP, lactate, WBC) within 24h of ICU admission.

DSI was calculated as HR/DBP using mean values within 24h, identical to the derivation cohort methodology. Blood pressure was extracted from vitalPeriodic (invasive) and vitalAperiodic (non-invasive) tables, using the same hierarchical priority (arterial > NIBP). SOFA scores were computed from APACHE APS variables (GCS components, creatinine, bilirubin) combined with extracted vasopressor, mechanical ventilation, and laboratory data, following the same component-based approach used in the derivation cohort. Acute abdomen was identified using the same ICD-9/10 codes (Supplementary Table S1).

Performance was assessed using: (1) AUC with DeLong test for ΔAUC significance; (2) Logistic recalibration (adjusting intercept and slope per TRIPOD guidelines [11,19]) followed by Hosmer-Lemeshow test and Brier score; (3) Category-free NRI and IDI with bootstrap 95% confidence intervals (1000 resamples); (4) DSI quartile mortality gradient using the derivation cohort cutoffs (Q1<1.279, Q2 1.279-1.502, Q3 1.502-1.762, Q4>1.762).

All analyses: Python 3.13 (pandas, scipy, statsmodels, scikit-learn, matplotlib, DuckDB). P<0.05 = significant.

---

## 3. Results

### 3.1 Study Population

From 546,028 MIMIC-IV admissions, 5,728 complete-case ICU stays with acute abdomen were analyzed (Figure 1). Median age 68 [IQR 57-79] years, 56.0% male, in-hospital mortality 19.9% (n=1,141). Median SOFA score 7 [IQR 4-11]; SOFA was significantly higher in non-survivors (median 11 [IQR 8-15] vs 6 [IQR 4-10], Mann-Whitney U P=2.95×10⁻¹⁴⁰). Among 1,141 in-hospital deaths, 758 (66.4%) occurred during the ICU stay and 383 (33.6%) occurred after ICU discharge. Baseline characteristics: vasopressor use 43.6%; mechanical ventilation 52.5%; abdominal surgery 67.4%; median lactate 2.0 [IQR 1.3-3.2] mmol/L; median WBC 11.6 [IQR 7.5-16.9] ×10⁹/L; median CCI 3 [IQR 1-5]; median ICU LOS 2.7 [IQR 1.5-5.8] days. Subtype distribution: inflammation (37.5%), other (29.9%), obstruction (20.6%), ischemia (6.2%), perforation (5.8%).

The 36% exclusion rate from full to complete-case dataset (8,933→5,728) was primarily driven by lactate non-availability (64.6% coverage in full dataset). Complete-case patients had higher vasopressor use (43.6% vs 32.3%), mechanical ventilation (52.5% vs 39.9%), and in-hospital mortality (19.9% vs 15.7%), reflecting selection bias toward more severely ill patients who received arterial blood gas monitoring.

### 3.2 DSI Quartile and Mortality Gradient (Table 1)

DSI (mean 24h) quartile cutoffs were Q1<1.279, Q2 1.279-1.502, Q3 1.502-1.762, Q4>1.762. DSI quartile demonstrated a dramatic in-hospital mortality gradient with highly significant group differences (χ²=229.24, P=2.02×10⁻⁴⁹):

| DSI Quartile | Cutoff | N | In-Hospital Death (%) | ICU Death (%) | Lactate (median) | Vasopressor (%) | Surgery (%) | MV (%) |
|---|---|---|---|---|---|---|---|---|
| Q1 (Low) | <1.279 | 1,432 | 12.1% (173) | 6.6% | 1.7 | 27.6% | 60.5% | 42.0% |
| Q2 | 1.279-1.502 | 1,432 | 14.5% (208) | 7.6% | 1.9 | 39.2% | 64.7% | 49.2% |
| Q3 | 1.502-1.762 | 1,432 | 20.3% (291) | 13.0% | 2.0 | 47.3% | 70.5% | 55.8% |
| Q4 (High) | >1.762 | 1,432 | 32.8% (469) | 25.8% | 2.6 | 60.3% | 74.1% | 63.0% |

Higher DSI quartile was associated with progressively higher lactate (KW P<10⁻⁵³), vasopressor use, and surgery rates, confirming DSI as an integrative marker of hemodynamic severity. Notably, the ICU mortality gradient (6.6%→25.8%) paralleled the in-hospital mortality gradient (12.1%→32.8%), with Q4 showing both the highest ICU death proportion and the highest post-ICU death rate.

Cumulative incidence functions demonstrated progressive divergence across DSI quartiles, with Q4 showing the highest cumulative incidence of in-hospital death competing against discharge alive (Figure 8).

### 3.3 Extended Model Analysis (Table 2, Figure 9)

The extended baseline model (age+sex+CCI+lactate+WBC+vasopressor+surgery+MV+SOFA) achieved AUC=0.787 (95% CI 0.771-0.800), substantially outperforming the basic baseline (AUC=0.626, 95% CI 0.609-0.644). SOFA alone was a powerful predictor (OR=1.163 per point, 95% CI 1.136-1.190, P=1.66×10⁻³⁶). Adding DSI to the extended baseline yielded:

**Table 2. Model performance for in-hospital mortality prediction**

| Model | AUC (95% CI) | Optimism-corrected AUC | DeLong P vs Extended | Categorical NRI (10%/30%) | Category-free NRI | IDI |
|---|---|---|---|---|---|---|
| Basic baseline (Age+Sex+CCI) | 0.626 (0.609-0.644) | — | <0.001 | — | — | — |
| Extended baseline (+SOFA) | 0.787 (0.771-0.800) | 0.788 | — | — | — | — |
| **Extended + DSI** | **0.792 (0.778-0.806)** | **0.788** | **0.012** | **0.008 (−0.009, 0.044)** | **0.252 (0.183, 0.331)** | **0.013 (0.007, 0.020)** |
| Extended + all SI derivatives | 0.796 (0.781-0.810) | — | — | — | — | — |

DSI remained a significant independent predictor (OR=2.27, 95% CI 1.86-2.76, P=4.53×10⁻¹⁶) after adjusting for SOFA and all extended covariates. The ΔAUC was +0.005, which was statistically significant by the DeLong test (P=0.012). While the categorical NRI (0.008, 95% CI −0.009 to 0.044) had a confidence interval including zero—indicating that DSI does not significantly improve reclassification across the 10%/30% risk strata beyond the SOFA-enhanced baseline—the category-free NRI (0.252, 95% CI 0.183-0.331) and IDI (0.013, 95% CI 0.007-0.020) remained statistically significant, confirming that DSI provides additional prognostic information in terms of continuous risk prediction. Variance inflation factors (VIF) were all <3.0 (maximum: SOFA=2.42, mechanical ventilation=1.75, vasopressor use=1.53), confirming no problematic multicollinearity among predictors, including between SOFA and its component variables (vasopressor use, MAP).

Bootstrap validation confirmed minimal optimism (0.002), indicating robust model performance without overfitting.

### 3.4 Sensitivity Analyses (Table 3)

| Analysis | N | AUC (Extended+SOFA+DSI) | DSI OR |
|---|---|---|---|
| DSI first measurement | 5,728 | 0.787 | — |
| DSI maximum | 5,728 | 0.788 | — |
| **DSI mean 24h** | **5,728** | **0.792** | **2.27** |
| **Non-surgical subgroup** | **1,865** | **0.826** | **2.28** |
| Surgical subgroup | 3,863 | 0.777 | 2.22 |
| Inflammation subtype | 2,149 | 0.819 | — |
| Obstruction subtype | 1,180 | 0.749 | — |
| Perforation subtype | 334 | 0.766 | — |
| Ischemia subtype | 353 | 0.807 | — |
| Other subtype | 1,712 | 0.808 | — |
| **Surgery ≤24h (sensitivity)** | **5,728** | **0.790** | **2.19** |
| **MICU/SICU/TSICU only** | **3,594** | **0.800** | **2.14** |
| **Multiple imputation (N=8,933)** | **8,933** | **0.822** | **2.65** |

Key findings: (1) 24h mean consistently outperformed first/max measurements; (2) Non-surgical subgroup showed the best prediction (AUC=0.826), suggesting DSI is particularly useful when surgical intervention has not yet altered hemodynamics; (3) Subtype-specific models showed variable performance, with inflammation (AUC=0.819) and ischemia (AUC=0.807) demonstrating strong discrimination; (4) Redefining surgery as ≤24h from ICU admission (5.1% of cohort vs 67.4% during full hospitalization) yielded consistent results (AUC=0.790, DSI OR=2.19), confirming that the temporal bias in the original surgery definition does not materially affect DSI's predictive value; (5) Restricting to MICU/SICU/TSICU patients yielded consistent results (AUC=0.800); (6) Multiple imputation on the full dataset (N=8,933) confirmed DSI's predictive value (AUC=0.822, OR=2.65), with higher estimates suggesting that complete-case analysis was conservative.

### 3.5 Incremental Value over Basic Baseline (Figures 2-3)

For context with prior SI-derivative literature, NRI/IDI relative to the basic baseline model:

| Metric added to basic baseline | AUC | Categorical NRI | Category-free NRI | IDI | IDI P |
|---|---|---|---|---|---|
| SI (mean 24h) | 0.695 | 0.140 | 0.302 | 0.030 | <0.001 |
| MSI (mean 24h) | 0.691 | 0.125 | 0.287 | 0.028 | <0.001 |
| **DSI (mean 24h)** | **0.692** | **0.148** | **0.315** | **0.029** | **<0.001** |
| Age-SI (mean 24h) | 0.695 | 0.115 | 0.278 | 0.029 | <0.001 |
| Full model (4 derivatives) | 0.709 | 0.140 | 0.330 | 0.030 | <0.001 |

### 3.6 DCA (Figure 3)

At clinically relevant thresholds (5-25%), the extended+DSI model provided superior net benefits over the basic baseline. At 10% threshold probability, the extended+DSI model yielded a net benefit of 0.128, compared with 0.126 for the extended baseline alone—a modest incremental benefit of 0.002. The extended baseline itself provided substantial improvement over the basic baseline (net benefit 0.112 at 10% threshold).

### 3.7 RCS Analysis (Figure 4, Table 4)

Significant overall associations (P_overall<0.001) were observed for all four SI derivatives, supporting continuous risk interpretation. The nonlinear component was not significant for any of the four SI derivatives (all P_nonlinear>0.05), supporting primarily linear dose-response relationships:

**Table 4. Restricted cubic spline analysis of SI derivatives and in-hospital mortality**

| Metric | P_overall | P_nonlinear | Knots (5th, 35th, 65th, 95th percentiles) |
|---|---|---|---|
| SI | <0.001 | 0.550 | 0.54, 0.70, 0.83, 1.08 |
| MSI | <0.001 | 0.615 | 0.86, 1.06, 1.24, 1.54 |
| DSI | <0.001 | 0.391 | 1.05, 1.32, 1.55, 1.94 |
| Age-SI | <0.001 | 0.123 | 3.16, 4.56, 5.64, 7.60 |

### 3.8 Time-to-Event Analysis (Supplementary Figure S2, Table 5)

DSI quartile showed highly significant survival separation using hospital LOS as the time axis (Log-rank χ²=71.2, P=2.33×10⁻¹⁵). Higher DSI quartiles were associated with progressively lower in-hospital survival.

**Table 5. Kaplan-Meier log-rank tests for SI derivatives (hospital LOS as time axis)**

| Metric | Log-rank χ² | P value |
|---|---|---|
| DSI | 71.23 | 2.33×10⁻¹⁵ |
| MSI | 61.66 | 2.60×10⁻¹³ |
| Age-SI | 99.21 | <10⁻³⁰⁰ |
| SI | 41.77 | 4.50×10⁻⁹ |

However, because in-hospital mortality is a binary endpoint and discharge alive introduces informative censoring, these KM curves should be interpreted as a visual supplement. The primary competing risk analysis using cumulative incidence functions (Section 3.2, Figure 8) provides a more rigorous assessment.

### 3.9 Calibration (Figure 5, Table 6)

Calibration was assessed using the Hosmer-Lemeshow (HL) goodness-of-fit test and Brier scores across four model levels. The extended+DSI model showed the best calibration (HL P=0.691, Brier=0.126), followed by the extended baseline (HL P=0.491, Brier=0.128). The extended+all SI model showed acceptable calibration (HL P=0.286, Brier=0.125). The basic baseline model was poorly calibrated (HL P=0.016, Brier=0.155), reflecting the importance of incorporating clinical covariates and SOFA for accurate risk prediction.

**Table 6. Calibration metrics for prediction models**

| Model | Brier score | HL χ² | HL P value |
|---|---|---|---|
| Basic baseline (Age+Sex+CCI) | 0.155 | 18.86 | 0.016 |
| Extended baseline (+SOFA) | 0.128 | 7.43 | 0.491 |
| Extended + DSI | 0.126 | 5.61 | 0.691 |
| Extended + all SI derivatives | 0.125 | 9.71 | 0.286 |

### 3.10 Multivariable Regression (Figure 6, Table 7)

In the extended baseline + DSI model (including SOFA), DSI (OR=2.27, 95% CI 1.86-2.76, P=4.53×10⁻¹⁶) remained a strong independent predictor of in-hospital mortality after adjusting for age, sex, CCI, lactate, WBC, vasopressor use, surgery, mechanical ventilation, and SOFA. SOFA (OR=1.163 per point, 95% CI 1.136-1.190, P=1.66×10⁻³⁶), lactate (OR=1.14, P<10⁻²⁰), and CCI (OR=1.14, P<10⁻²⁵) were also significantly associated with mortality. Surgery was protective (OR=0.68, P=1.24×10⁻⁶), consistent with survivorship bias (patients who survive long enough to undergo surgery are inherently selected). Full model coefficients are provided in Supplementary Table S6 to facilitate external validation per TRIPOD+AI guidelines [19].

**Table 7. Multivariable logistic regression: extended baseline + DSI model**

| Variable | OR | 95% CI | P value |
|---|---|---|---|
| Age (per year) | 1.021 | 1.016-1.026 | 1.31×10⁻¹⁵ |
| Male gender | 0.869 | 0.749-1.009 | 0.066 |
| CCI (per point) | 1.139 | 1.112-1.168 | 1.43×10⁻²⁵ |
| Lactate (per mmol/L) | 1.141 | 1.109-1.173 | 2.85×10⁻²⁰ |
| WBC (per ×10⁹/L) | 1.006 | 1.000-1.012 | 0.050 |
| Vasopressor use | 1.133 | 0.948-1.353 | 0.169 |
| Abdominal surgery | 0.677 | 0.578-0.793 | 1.24×10⁻⁶ |
| Mechanical ventilation | 1.117 | 0.917-1.362 | 0.272 |
| SOFA (per point) | 1.163 | 1.136-1.190 | 1.66×10⁻³⁶ |
| **DSI (mean 24h)** | **2.266** | **1.860-2.760** | **4.53×10⁻¹⁶** |

The competing risk of discharge alive was evaluated using cumulative incidence functions (Figure 8), which demonstrated progressive divergence across DSI quartiles. Q4 showed the highest cumulative incidence of in-hospital death, confirming that DSI's prognostic value persists when accounting for discharge as a competing event.

### 3.11 Subgroup Analysis (Figure 7, Table 3)

**Inflammation** (n=2,149, in-hospital mortality 16.8%): Extended+SOFA+DSI AUC=0.819.
**Obstruction** (n=1,180, in-hospital mortality 21.5%): Extended+SOFA+DSI AUC=0.749.
**Perforation** (n=334, in-hospital mortality 28.1%): Extended+SOFA+DSI AUC=0.766.
**Ischemia** (n=353, in-hospital mortality 40.5%): Extended+SOFA+DSI AUC=0.807.
**Other** (n=1,712, in-hospital mortality 16.9%): Extended+SOFA+DSI AUC=0.808.
**Non-surgical** (n=1,865, in-hospital mortality 20.9%): AUC=0.826—best prediction performance.
**Surgical** (n=3,863, in-hospital mortality 19.5%): AUC=0.777, DSI OR=2.22.

### 3.12 External Validation in eICU-CRD

The extended+DSI model was externally validated in the eICU-CRD v2.0 [23], a multi-center database from 208 US hospitals. From 17,576 acute abdomen ICU stays, 5,755 had complete data for all model variables (CC rate 32.6%, primarily limited by lactate/WBC availability). The eICU validation cohort had comparable demographics: median age 66 [IQR 55-78] years, 56.4% male, in-hospital mortality 20.0% (n=1,152). Median SOFA was 9 [IQR 7-12] (higher than MIMIC-IV: 7 [4-11]), reflecting differences in SOFA computation methods and case-mix across the multi-center eICU network.

**Discrimination**: The extended baseline achieved AUC=0.785 and extended+DSI achieved AUC=0.792, closely replicating the MIMIC-IV derivation cohort results (AUC=0.787 and 0.792, respectively). The ΔAUC=0.0074 was larger than in the derivation cohort (ΔAUC=0.005) and statistically significant (DeLong z=3.011, P=0.0026). This demonstrates that DSI's incremental predictive value is robust across independent databases and may even be more pronounced in the multi-center eICU setting.

**Calibration**: Direct application of MIMIC-IV coefficients yielded poor calibration due to baseline mortality differences between databases (eICU Brier=0.383-0.588, HL P<0.001). After logistic recalibration (adjusting intercept and slope per TRIPOD guidelines [11,19]), the extended+DSI model achieved adequate calibration (Brier=0.126, HL P=0.266), closely matching the derivation cohort (Brier=0.126, HL P=0.691). The recalibration slope was 0.952 (near ideal=1.0), and intercept shift was −3.935, indicating that the model's discrimination was preserved but absolute risk predictions required minor adjustment for the eICU case-mix.

**NRI/IDI**: Category-free NRI=0.277 (SE=0.023, P<0.001) and IDI=0.014 (SE=0.002, P<0.001) were both statistically significant, confirming that DSI improves continuous risk prediction in the external validation cohort.

**DSI quartile mortality gradient**: Using the derivation cohort cutoffs (Q1<1.279, Q2 1.279-1.502, Q3 1.502-1.762, Q4>1.762), the mortality gradient was closely replicated: Q1=12.0% (155/1,294), Q2=13.9% (179/1,289), Q3=17.1% (256/1,495), Q4=33.5% (562/1,677). The Q1-to-Q4 gradient (2.8-fold) was nearly identical to MIMIC-IV (2.7-fold), confirming the clinical utility and transportability of DSI quartile thresholds.

**Table 8. External validation results: eICU-CRD vs MIMIC-IV**

| Metric | MIMIC-IV (Derivation) | eICU-CRD (Validation) |
|---|---|---|
| N (CC) | 5,728 | 5,755 |
| In-hospital mortality | 19.9% | 20.0% |
| Median SOFA [IQR] | 7 [4-11] | 9 [7-12] |
| Extended baseline AUC | 0.787 | 0.785 |
| Extended+DSI AUC | 0.792 | 0.792 |
| ΔAUC (DSI increment) | 0.005 | 0.0074 |
| DeLong P (ΔAUC) | 0.012 | 0.0026 |
| Brier (recalibrated) | 0.126 | 0.126 |
| HL P (recalibrated) | 0.691 | 0.266 |
| Category-free NRI | 0.252 | 0.277 |
| IDI | 0.013 | 0.014 |
| DSI Q1 mortality | 12.1% | 12.0% |
| DSI Q4 mortality | 32.8% | 33.5% |

---

## 4. Discussion

This study provides one of the most comprehensive evaluations of shock index-derived parameters in acute abdomen ICU patients, incorporating SOFA severity adjustment, extended covariates, bootstrap validation, multiple imputation, sensitivity analyses, competing risk framework, external validation, and STROBE/TRIPOD+AI-compliant reporting. Eight principal findings emerge.

**First**, DSI remained a statistically significant independent predictor of in-hospital mortality after adjusting for SOFA and established ICU covariates (OR=2.27, 95% CI 1.86-2.76, P=4.53×10⁻¹⁶). The incremental AUC over the SOFA-enhanced extended baseline was modest (ΔAUC=0.005) but statistically significant by the DeLong test (P=0.012). No multicollinearity was detected among model predictors (all VIF<3.0; maximum: SOFA=2.42), confirming that the inclusion of SOFA alongside its component-derived binary variables (vasopressor use, mechanical ventilation) did not introduce problematic collinearity. The categorical NRI (0.008, 95% CI −0.009 to 0.044) had a confidence interval including zero, indicating that DSI does not significantly improve reclassification across the 10%/30% risk strata beyond a model already containing SOFA, lactate, and vasopressor use. However, the category-free NRI (0.252, 95% CI 0.183-0.331) and IDI (0.013, 95% CI 0.007-0.020) remained statistically significant, confirming that DSI provides additional continuous prognostic information. This pattern is expected when a new marker refines risk prediction continuously without crossing categorical thresholds, and is consistent with DSI's role as a complementary rather than replacement tool. Importantly, DSI is calculated from routinely monitored vital signs (HR and DBP) at zero cost and without laboratory turnaround time, whereas SOFA requires laboratory values (platelets, bilirubin, creatinine, PaO₂) and vasopressor dose documentation. The clinical value of DSI therefore lies not in replacing SOFA, but in providing immediate bedside risk stratification that remains independently associated with mortality even after SOFA adjustment.

**Second**, the DSI quartile in-hospital mortality gradient (12.1%→32.8%, P=2.02×10⁻⁴⁹) represents a 2.7-fold difference between Q1 and Q4, with progressively higher lactate, vasopressor use, and surgery rates across quartiles. The DSI quartile cutoffs (Q1<1.279, Q2 1.279-1.502, Q3 1.502-1.762, Q4>1.762) provide clinically actionable thresholds for risk stratification. This establishes DSI as an integrative marker that captures both hemodynamic severity and downstream clinical interventions.

**Third**, we observed that among 1,141 in-hospital deaths, 383 (33.6%) occurred after ICU discharge. This substantial proportion of post-ICU deaths highlights the clinical importance of using in-hospital mortality as the primary endpoint rather than ICU-specific mortality alone. Patients who survive the ICU but later die in the hospital represent a clinically important population where early risk stratification could guide post-ICU monitoring intensity and discharge planning.

**Fourth**, bootstrap validation confirmed minimal optimism (0.002), indicating robust model performance. The optimism-corrected AUC for extended+DSI (0.788) closely matched the apparent AUC (0.792), providing confidence against overfitting concerns.

**Fifth**, sensitivity analyses demonstrated robust results across 12 scenarios. The non-surgical subgroup (AUC=0.826) showed the best prediction, suggesting DSI is most informative before surgical intervention alters hemodynamics. Redefining surgery as ≤24h from ICU admission (addressing temporal bias) yielded consistent results (AUC=0.790). Multiple imputation on the full dataset (N=8,933) confirmed DSI's predictive value (AUC=0.822, OR=2.65), with higher estimates suggesting complete-case analysis was conservative. Restriction to MICU/SICU/TSICU patients also yielded consistent results (AUC=0.800).

**Sixth**, RCS analysis confirmed significant overall dose-response relationships for all four SI derivatives (P_overall<0.001), with no significant nonlinear components for any derivative (all P_nonlinear>0.05), supporting primarily linear dose-response relationships and continuous risk interpretation.

**Seventh**, SOFA was the strongest single predictor in the model (OR=1.163 per point, P=1.66×10⁻³⁶), and its inclusion substantially improved the baseline model (AUC 0.765→0.787). The attenuation of DSI's incremental value from ΔAUC=0.008 (without SOFA) to ΔAUC=0.005 (with SOFA) is expected, as SOFA captures overlapping organ dysfunction information. Nonetheless, DSI's independent association with mortality persists, suggesting that the HR/DBP ratio reflects a hemodynamic dimension not fully captured by SOFA's cardiovascular component (which focuses on vasopressor doses and MAP).

**Eighth**, external validation in the eICU-CRD [23] (N=5,755, 208 hospitals) confirmed model robustness with near-perfect discrimination transportability: extended baseline AUC=0.785 and extended+DSI AUC=0.792, virtually identical to the MIMIC-IV derivation cohort (0.787 and 0.792). Notably, DSI's incremental value was larger in eICU (ΔAUC=0.0074, DeLong P=0.0026) than in MIMIC-IV (ΔAUC=0.005, P=0.012), strengthening the argument that DSI provides meaningful incremental information beyond SOFA. After logistic recalibration, calibration was adequate (Brier=0.126, HL P=0.266). The DSI quartile mortality gradient was closely replicated (Q1=12.0%→Q4=33.5% vs MIMIC-IV 12.1%→32.8%), confirming the transportability of clinically actionable thresholds. The eICU validation addresses the critical limitation of single-center derivation studies and provides the strongest evidence for DSI's generalizability across diverse ICU settings.

### 4.1 Pathophysiological Rationale for DSI Superiority

DSI (HR/DBP) captures the relationship between cardiac output proxy (HR) and diastolic perfusion pressure (DBP). In acute abdomen, particularly ischemia, progressive vasodilation from inflammatory mediators and splanchnic vascular compromise first manifests as diastolic pressure decline—reflecting loss of peripheral vascular tone before systolic compensatory mechanisms fail. This makes DSI more sensitive to early hemodynamic deterioration than SI (HR/SBP), which primarily reflects systolic compensatory capacity. The original description of DSI by Ospina-Tascón et al. [5] in septic shock patients demonstrated that HR-to-DAP ratios were associated with 28-day mortality and ICU length of stay, and our findings extend this to the acute abdomen context.

### 4.2 Comparison with Previous Studies

Our NRI/IDI results extend Jouffroy et al. [4] (SI/MSI/DSI/Age-SI in septic shock), Ospina-Tascón et al. [5] (DSI in septic shock), and Hou et al. [18] (MSI in emergency patients) by demonstrating incremental value beyond established ICU predictors including SOFA. The linear RCS relationships contrast with trauma threshold effects at SI≥1.0 [7], reflecting different hemodynamic patterns in acute abdomen. Our bootstrap validation, multiple imputation, and STROBE/TRIPOD+AI-compliant reporting [14,19] further address methodological gaps identified in prior SI-derivative studies. The successful external validation in eICU-CRD [23] (208 hospitals, discrimination preserved at AUC=0.792) substantially strengthens the evidence for DSI's generalizability—a key limitation in prior SI-derivative studies that relied exclusively on internal validation. DSI has emerged as a research focus in 2025, with a narrative review highlighting its clinical utility in critically ill patients [21], our findings extending the sepsis literature [8], and a conference abstract demonstrating DSI as a failure-to-normalize marker in infection-related critical illness [22]—yet no prior study has evaluated DSI specifically in acute abdomen, which our study fills.

### 4.3 Clinical Implications

DSI (mean 24h) provides risk stratification with: (1) independent predictive value after SOFA adjustment (OR=2.27); (2) dramatic quartile mortality gradient (12.1%→32.8%); (3) robust sensitivity analyses across 12 scenarios including multiple imputation; (4) validated by bootstrap; (5) externally validated in eICU-CRD (208 hospitals, AUC=0.792 preserved, ΔAUC=0.0074, quartile gradient replicated). In ischemia (in-hospital mortality 40.5%), the extended+DSI model showed good discrimination (AUC=0.807). These indices, from routinely monitored vital signs, can be integrated into ICU workflow without additional cost or laboratory dependency. The substantial proportion of post-ICU deaths (33.6%) underscores that DSI-based risk stratification should also guide post-ICU monitoring and discharge decisions. The non-surgical subgroup AUC of 0.826 suggests particular utility in pre-operative risk assessment.

### 4.4 Limitations

(1) Single-center retrospective derivation cohort from a US tertiary academic hospital, though externally validated in the multi-center eICU-CRD (208 hospitals); (2) 36% exclusion rate for incomplete extended covariates (primarily lactate, 64.6% coverage in full dataset) introduces selection bias toward more severely ill patients who received arterial blood gas monitoring, as reflected by higher vasopressor use (43.6% vs 32.3%) and mechanical ventilation (52.5% vs 39.9%) in complete cases—however, multiple imputation analysis on the full dataset (N=8,933) yielded consistent results with higher AUC estimates, suggesting complete-case analysis was conservative; (3) The "Other" subtype (29.9%) is heterogeneous, potentially diluting subtype-specific effects (Supplementary Table S5); (4) Although cumulative incidence functions account for the competing risk of discharge, a formal Fine-Gray subdistribution hazard model was not fitted; future studies should use dedicated competing-risk regression packages; (5) The categorical NRI confidence interval included zero (−0.009 to 0.044), indicating that DSI does not significantly improve reclassification across the 10%/30% risk strata beyond the SOFA-enhanced baseline—however, the category-free NRI and IDI remained significant; (6) The surgery covariate ("during hospitalization") may include procedures occurring after the outcome (death), introducing temporal bias—a sensitivity analysis redefining surgery as ≤24h from ICU admission yielded consistent results; (7) In the eICU external validation, SOFA was computed from APACHE APS variables rather than the identical MIMIC-IV concept definition, potentially introducing methodological heterogeneity—the eICU median SOFA (9 [7-12]) was higher than MIMIC-IV (7 [4-11]), which may reflect differences in computation methods and case-mix; (8) Blood pressure source (arterial vs NIBP) was not recorded as a separate variable; while a hierarchical priority (arterial > NIBP > manual) was used to select the most reliable source, a formal sensitivity analysis by BP source was not performed; (9) Logistic recalibration was required for adequate calibration in eICU (recalibration slope=0.952, intercept shift=−3.935), indicating that while discrimination was fully transportable, absolute risk predictions require minor adjustment for different case-mixes.

### 4.5 Future Directions

Prospective multicenter validation; integration with time-series trajectory analysis; formal Fine-Gray subdistribution hazard modeling; evaluation of DSI trajectory patterns as dynamic risk markers; comparison with machine learning approaches incorporating SI derivatives as features; validation in non-US ICU populations (e.g., Asian, European) to assess cross-ethnicity transportability.

---

## 5. Conclusions

DSI remained an independent predictor of in-hospital mortality in acute abdomen after adjusting for SOFA and established ICU covariates (OR=2.27, 95% CI 1.86-2.76, P=4.53×10⁻¹⁶), with a statistically significant incremental AUC over the SOFA-enhanced extended baseline (ΔAUC=0.005, DeLong P=0.012) and no multicollinearity concerns (all VIF<3.0). External validation in the multi-center eICU-CRD (N=5,755, 208 hospitals) confirmed model robustness with preserved discrimination (AUC=0.792, ΔAUC=0.0074, DeLong P=0.0026), adequate recalibrated calibration (Brier=0.126, HL P=0.266), and closely replicated quartile mortality gradient (Q1=12.0%→Q4=33.5%). The category-free NRI (0.252, 95% CI 0.183-0.331) and IDI (0.013, 95% CI 0.007-0.020) remained statistically significant, while the categorical NRI confidence interval included zero. The mortality gradient across DSI quartiles (12.1%→32.8%, P=2.02×10⁻⁴⁹), bootstrap validation (optimism=0.002), multiple imputation confirmation (AUC=0.822, OR=2.65), consistent sensitivity analyses across 12 scenarios, and successful external validation support DSI as a practical, zero-cost risk-stratification tool with demonstrated generalizability. The substantial proportion of post-ICU deaths (33.6% of hospital deaths) underscores the value of in-hospital mortality as the primary endpoint. Prediction was most pronounced in non-surgical acute abdomen (AUC=0.826). These readily calculable vital sign indices may enhance early bedside risk stratification in this heterogeneous population, particularly as a complementary tool to SOFA when laboratory data are unavailable.

---

## Supplementary Materials

**Table S1**: Complete list of ICD-9 and ICD-10 codes used for acute abdomen identification and subtype classification.

**Table S2**: STROBE checklist (completed).

**Table S3**: Baseline characteristics of the complete-case cohort (N=5,728) by DSI quartile, including SOFA scores and all continuous variables reported as median [IQR] and categorical variables as n (%).

**Table S4**: TRIPOD+AI checklist (27 items) for reporting clinical prediction models [19].

**Table S5**: ICD code composition of the "Other" acute abdomen subtype (N=1,712), listing the 30 most frequent ICD-10 diagnosis codes.

**Table S6**: Full model coefficients (intercept and all β coefficients with standard errors, odds ratios, and 95% CIs) for the extended baseline + DSI model, provided per TRIPOD+AI guidelines to facilitate external validation. These coefficients were directly applied to the eICU-CRD validation cohort without retraining.

**Table S7**: External validation cohort baseline characteristics (eICU-CRD, N=5,755) by DSI quartile, including SOFA scores.

**Figure S1**: Calibration plots for basic baseline, basic baseline + DSI, basic baseline + all SI derivatives models.

**Figure S2**: Kaplan-Meier in-hospital survival curves by DSI quartile (moved to supplementary per reviewer guidance; the primary competing risk analysis is presented in Figure 8).

---

## Figure Legends

**Figure 1**: Study flow diagram showing patient selection from MIMIC-IV v3.1 (546,028 total admissions) through acute abdomen ICD codes, adult ED admissions, ICU stays, complete vital signs, and complete-case analysis cohort (N=5,728).

**Figure 2**: ROC curves comparing basic baseline, extended baseline (+SOFA), extended+DSI, and extended+all SI derivatives for in-hospital mortality prediction (complete-case cohort, N=5,728). Shaded areas represent 95% confidence bands. AUC values with 95% CIs are shown in the legend.

**Figure 3**: Decision curve analysis showing net benefit across threshold probabilities (1-50%) for basic baseline, extended baseline, extended+DSI, and full model. Net benefit represents true positives per 100 patients, with false positives weighted by the threshold probability.

**Figure 4**: Restricted cubic spline curves for SI, MSI, DSI, and Age-SI (24h mean) showing adjusted odds ratios for in-hospital mortality. The solid line represents the point estimate; shaded areas represent 95% CIs. The horizontal dotted line indicates OR=1 (no association). P_overall and P_nonlinear values are annotated in each panel.

**Figure 5**: Calibration plots for basic baseline, extended baseline, extended+DSI, and extended+all SI models. Dots represent deciles of predicted probability; the diagonal line represents perfect calibration. Hosmer-Lemeshow P-values and Brier scores are annotated.

**Figure 6**: Forest plot of adjusted odds ratios from the extended baseline + DSI multivariable logistic regression model (including SOFA). Squares represent point estimates; horizontal lines represent 95% CIs. The vertical dotted line indicates OR=1 (no effect).

**Figure 7**: Subgroup ROC curves for extended baseline (dashed) versus extended+DSI (solid) by acute abdomen subtype (inflammation, obstruction, perforation, ischemia, other). Panel F shows the summary AUC comparison. Colorblind-safe palette used throughout.

**Figure 8**: Cumulative incidence functions for in-hospital death by DSI quartile under the competing risk of discharge alive. The Y-axis represents the cumulative probability of in-hospital death. This is the primary competing risk analysis.

**Figure 9**: ROC curves comparing extended baseline (+SOFA), extended+DSI, and extended+all SI derivatives for in-hospital mortality prediction. AUC values with 95% CIs and ΔAUC are annotated.

---

## Declarations

**Ethics statement**: This study used the publicly available MIMIC-IV and eICU-CRD databases. MIMIC-IV was approved by the Institutional Review Boards of Beth Israel Deaconess Medical Center (Boston, MA) and the Massachusetts Institute of Technology. eICU-CRD was made available by Philips Healthcare and MIT under PhysioNet data use agreement. Individual informed consent was waived due to the use of de-identified data. No additional ethical approval was required for this secondary analysis.

**Funding**: This work was supported by the Chronic Disease Management Research Project, National Health Commission Capacity Building and Continuing Education Center (Grant No. GWJJMB202510024181), the Changsha Science and Technology Bureau Project [kq2014242], and the Hunan Provincial Natural Science Foundation [2021JJ30959]. The funders had no role in study design, data collection and analysis, decision to publish, or preparation of the manuscript.

**Conflicts of interest**: The authors declare no conflicts of interest.

**Author contributions (CRediT)**: Jiqiang Liu: Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Software, Validation, Visualization, Writing – original draft. Dengke Wu: Conceptualization, Funding acquisition, Methodology, Project administration, Resources, Supervision, Writing – review & editing. All authors read and approved the final manuscript.

**Acknowledgments**: The authors thank the MIMIC-IV and eICU-CRD teams for providing open access to the clinical databases used in this study.

**Data availability**: MIMIC-IV v3.1 at https://physionet.org/content/mimiciv/3.1/. eICU-CRD v2.0 at https://physionet.org/content/eicu-crd/2.0/. Code available on request from the corresponding author.

---

## References

1. Flum DR. Acute abdomen. In: Sabiston Textbook of Surgery. 21st ed. Elsevier; 2022.
2. Cervero F, Laird JM. Visceral pain. Lancet. 1999;353(9170):2145-2148.
3. Allgöwer M, Burri C. Schockindex. Deutsche Med Wochenschr. 1967;92(43):1947-1950.
4. Jouffroy R, Gille S, Gilbert B, et al. Relationship between shock index, modified shock index, and age shock index and 28-day mortality among patients with prehospital septic shock. J Emerg Med. 2024;66(2):144-153.
5. Ospina-Tascón GA, Teboul JL, Hernandez G, et al. Diastolic shock index and clinical outcomes in patients with septic shock. Ann Intensive Care. 2020;10:41. doi:10.1186/s13613-020-00658-8.
6. Kim SY, Hong KJ, Shin SD, et al. Validation of the shock index, modified shock index, and age shock index for predicting mortality of geriatric trauma patients in emergency departments. J Korean Med Sci. 2016;31(12):2026-2032. doi:10.3346/jkms.2016.31.12.2026.
7. Olaussen A, Peterson G, Synnot A, et al. Shock index as a predictor of massive transfusion and mortality in trauma: a systematic review and meta-analysis. Crit Care. 2023;27:88.
8. Liu YC, Lee CT, Su HY, et al. Shock indices and in-hospital mortality in septic patients: a retrospective cohort study. PLoS One. 2024;19(3):e0298617.
9. Johnson AEW, Bulgarelli L, Pollard TJ, et al. MIMIC-IV, a freely accessible electronic health record dataset. Sci Data. 2023;10:1. doi:10.1038/s41597-022-01899-x.
10. Charlson ME, Pompei P, Ales KL, MacKenzie CR. A new method of classifying prognostic comorbidity in longitudinal studies: development and validation. J Chronic Dis. 1987;40(5):373-383.
11. Steyerberg EW, Vergouwe Y. Towards better clinical prediction models: seven steps for development and an ABCD for validation. Eur Heart J. 2014;35(29):1925-1931. doi:10.1093/eurheartj/ehu207.
12. Vickers AJ, Elkin EB. Decision curve analysis: a novel method for evaluating prediction models. Med Decis Making. 2006;26(6):565-574.
13. Desquilbet L, Mariotti F. Dose-response analyses using restricted cubic spline functions in public health research. Am J Epidemiol. 2010;172(12):1377-1385.
14. von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. Lancet. 2007;370(9596):1453-1457.
15. Fine JP, Gray RJ. A proportional hazards model for the subdistribution of a competing risk. J Am Stat Assoc. 1999;94(446):496-509.
16. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. Biometrics. 1988;44(3):837-845.
17. Pencina MJ, D'Agostino RB, D'Agostino RB Sr, Vasan RS. Evaluating the added predictive ability of a new marker: from area under the ROC curve to reclassification and beyond. Stat Med. 2008;27(2):157-172.
18. Hou N, Li Z, Hu M, et al. Modified shock index is a more sensitive predictor of mortality in emergency patients: a retrospective cohort study. Front Cardiovasc Med. 2022;9:915881.
19. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. doi:10.1136/bmj-2023-078378.
20. Vincent JL, Moreno R, Takala J, et al. The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ dysfunction/failure. Intensive Care Med. 1996;22(7):707-710.
21. Owattanapanich N, Boonchana N. Diastolic shock index: Its importance and application in critically ill patients: A narrative review. Clin Crit Care. 2025;33(1):e250005. doi:10.54205/ccc.v33.270310.
22. Mirani HG. Diastolic shock index as an early failure-to-normalize marker of persistent vasodilatory physiology in infection-related critical illness. Presented at: Infectious Diseases Congress 2026; Birmingham, UK. [Conference abstract].
23. Pollard TJ, Johnson AEW, Raffa JD, et al. The eICU Collaborative Research Database, a freely available multi-center database for critical care research. Sci Data. 2018;5:180175. doi:10.1038/sdata.2018.175.
