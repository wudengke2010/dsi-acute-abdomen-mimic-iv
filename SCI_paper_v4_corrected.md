# Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV

**Jiqiang Liu** [1]†, **Dengke Wu** [1]*

[1] Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China

† First author.

* Corresponding author: Dengke Wu, Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China. Electronic address: wudk2010@csu.edu.cn

---

## Abstract

**Background**: Shock index (SI) and its derivatives—modified shock index (MSI), diastolic shock index (DSI), and age-adjusted shock index (Age-SI)—have demonstrated predictive value in trauma and sepsis, yet their utility in acute abdomen remains unexplored. This study evaluated SI-derived parameters for in-hospital mortality prediction in acute abdomen, including incremental value beyond established ICU covariates.

**Methods**: This retrospective cohort study utilized MIMIC-IV v3.1. Adult ICU patients with acute abdomen diagnoses were included. SI, MSI, DSI, and Age-SI were calculated from vital signs within 24 hours of ICU admission. Primary outcome was in-hospital mortality. Predictive performance was assessed using ROC/AUC, net reclassification improvement (NRI), integrated discrimination improvement (IDI), decision curve analysis (DCA), restricted cubic spline (RCS), Kaplan-Meier survival curves, cumulative incidence functions, calibration, and bootstrap internal validation (1000 resamples). Models were constructed at three levels: (1) basic baseline (age+sex+CCI); (2) extended baseline (age+sex+CCI+lactate+WBC+vasopressor use+surgery+mechanical ventilation); (3) extended baseline + SI derivatives.

**Results**: Among 5,728 complete-case ICU stays (median age 68 [IQR 57-79] years, 56.0% male, in-hospital mortality 19.9%), the extended baseline model achieved AUC=0.765 (optimism-corrected 0.763). Adding DSI (mean 24h) improved AUC to 0.773 (ΔAUC=+0.008; categorical NRI=0.046, category-free NRI=0.283, IDI=0.017, P=4.88×10⁻¹³; optimism-corrected AUC=0.771). Although statistically significant, the magnitude of AUC improvement was modest. The full model incorporating all four SI derivatives achieved AUC=0.777 (optimism-corrected 0.774). DSI quartile demonstrated a dramatic mortality gradient: Q1=12.1%, Q2=14.5%, Q3=20.3%, Q4=32.8% (χ² P=2.02×10⁻⁴⁹). Of 1,141 in-hospital deaths, 758 (66.4%) occurred during the ICU stay and 383 (33.6%) after ICU discharge. RCS confirmed linear dose-response relationships (P_nonlinear>0.05). Sensitivity analyses across 10 scenarios yielded consistent results (AUC range 0.73-0.80). The ischemia subtype showed the highest mortality (40.5%) and non-surgical subgroup showed the best prediction (AUC=0.804).

**Conclusions**: DSI provided statistically significant incremental predictive value for in-hospital mortality in acute abdomen patients beyond established ICU covariates including lactate and vasopressor use, though the magnitude of AUC improvement was modest (ΔAUC=0.008) and should be interpreted alongside the categorical NRI, IDI, and DCA findings. The mortality gradient across DSI quartiles and robust sensitivity analyses support DSI as a practical risk-stratification tool. Prediction utility was most pronounced in intestinal ischemia and non-surgical acute abdomen.

**Keywords**: Shock index; Diastolic shock index; Acute abdomen; In-hospital mortality; MIMIC-IV; Net reclassification improvement; Bootstrap validation; Cumulative incidence function; Sensitivity analysis

---

## 1. Introduction

Acute abdomen—severe abdominal pain of sudden onset requiring urgent evaluation—remains one of the most challenging presentations in emergency medicine [1]. Early risk stratification is a critical unmet need, as outcomes vary dramatically across etiologies ranging from self-limiting inflammation to life-threatening intestinal ischemia [1,2].

The shock index (SI = HR/SBP), first described by Allgöwer and Burri in 1967 [3], has inspired several derived indices: modified shock index (MSI = HR/MAP) [4,18], diastolic shock index (DSI = HR/DBP) [5], and age-adjusted shock index (Age-SI = SI×Age/10) [6]. These have been validated in trauma [7] and sepsis [8], but never systematically evaluated in acute abdomen—a population with pathophysiological diversity including inflammation-driven vasodilation, mechanical obstruction, perforation-induced peritonitis, and ischemia-requiring reperfusion.

Moreover, previous SI-derivative studies have relied primarily on AUC comparisons without evaluating incremental value beyond established ICU predictors (lactate, vasopressor use, severity scores), nor assessing model robustness through bootstrap validation, sensitivity analyses, or competing risk frameworks. The TRIPOD+AI guidelines [17,19] emphasize that prediction models must demonstrate clinical benefit via NRI/IDI/DCA [17] and undergo internal validation [11]. This study was reported following the STROBE statement for observational studies [14].

This study aims to: (1) compare SI, MSI, DSI, and Age-SI for in-hospital mortality prediction in acute abdomen; (2) evaluate incremental value beyond extended covariates (lactate, WBC, vasopressor, surgery, mechanical ventilation) using NRI, IDI, and DCA; (3) assess model robustness via bootstrap validation and sensitivity analyses; (4) evaluate competing risks using cumulative incidence functions; and (5) determine subtype-specific prediction performance.

---

## 2. Methods

### 2.1 Study Design and Data Source

This retrospective cohort study utilized MIMIC-IV v3.1, containing comprehensive clinical data from Beth Israel Deaconess Medical Center (Boston, MA) between 2008 and 2022 [9]. Access was obtained through PhysioNet following required training. The study was reported in accordance with the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) guidelines [14]. As MIMIC-IV contains de-identified data, the Institutional Review Boards of BIDMC and MIT approved its use and waived the requirement for individual informed consent.

### 2.2 Study Population (Figure 1)

**Inclusion criteria**: (1) Age ≥18 years; (2) ICU admission via ED; (3) Acute abdomen ICD-9/10 diagnosis codes (Supplementary Table S1); (4) Complete vital signs (HR, SBP, DBP) within 24h of ICU admission.

**Exclusion criteria**: (1) Age <18 years; (2) Missing vital signs for SI calculation; (3) Missing extended covariates (lactate, WBC) for the complete-case analysis.

From 546,028 total MIMIC-IV admissions, 72,676 had acute abdomen ICD codes; 52,398 were adult ED admissions; 9,998 had ICU stays; 8,933 had complete vital signs (excluding 1,065 for age <18 or missing vital signs); and 5,728 had complete data for all extended covariates (excluding 3,205 for missing lactate [n=3,160] or WBC [n=45]) (Figure 1). The primary analysis cohort (complete cases, N=5,728) was used for all model comparisons; descriptive statistics are also reported from this cohort for consistency.

Acute abdomen was defined by ICD codes: appendicitis (K35-K38/540-543), biliary emergencies (K80-K83/574-576), pancreatitis (K85-K86/577.0-577.1), intestinal obstruction (K56/560), GI perforation (K25-K28 perforation, K63.1, K65/531-534 perforation, 569.83, 567), intestinal ischemia (K55.0/557.0), diverticulitis (K57/562), and strangulated hernia (K40-K46/550-553).

### 2.3 Acute Abdomen Subtype Classification

Four pathophysiological subtypes based on ICD diagnoses: (1) Perforation—visceral perforation and peritonitis; (2) Obstruction—mechanical/functional bowel obstruction; (3) Inflammation—acute inflammatory conditions without perforation; (4) Ischemia—acute mesenteric/intestinal ischemia. Priority: perforation > ischemia > obstruction > inflammation > other. Patients not meeting specific subtype criteria were classified as "other."

### 2.4 Shock Index-Derived Parameters

All parameters calculated from vital signs within 24h of ICU admission:
- **SI** = HR / SBP
- **MSI** = HR / MAP [MAP = (2×DBP + SBP)/3]
- **DSI** = HR / DBP
- **Age-SI** = SI × (Age / 10)

Three temporal metrics: first recorded, maximum, and 24-hour mean. Arterial BP preferred over NIBP.

### 2.5 Outcomes

**Primary**: In-hospital mortality (hospital_expire_flag from admissions table). This captures both deaths occurring during the ICU stay and deaths after ICU discharge but during the same hospitalization, providing a more clinically comprehensive endpoint than ICU-specific mortality alone.

**Secondary**: Strict ICU mortality (death occurring during the specific ICU stay, determined by deathtime falling within the ICU admission-to-discharge interval).

### 2.6 Covariates

**Basic baseline**: age, gender, Charlson Comorbidity Index (CCI) [10].

**Extended baseline**: age, gender, CCI, first lactate (within 24h of ICU admission), first WBC (within 24h), vasopressor use (any administration of norepinephrine, epinephrine, dopamine, vasopressin, or phenylephrine within 24h of ICU admission; binary), abdominal surgery (any abdominal surgical procedure during the hospitalization; binary), mechanical ventilation (any ventilator support within 24h of ICU admission, derived from chartevents itemids 220339, 224688, 224689, 224690; binary).

### 2.7 Statistical Analysis

**ROC/AUC**: With DeLong method comparisons [16]. **Multivariable logistic regression**: Three model levels—basic baseline, extended baseline, extended + SI derivatives.

**NRI/IDI**: Categorical NRI using clinically meaningful risk thresholds (<10%, 10-30%, >30%) as the primary reclassification metric, with category-free (continuous) NRI [17] as a secondary measure. IDI significance via Z-test.

**DCA**: Clinical net benefit across threshold probabilities 1-50% [12].

**RCS**: 4-knot restricted cubic spline within logistic regression (5th, 35th, 65th, 95th percentiles), adjusting for age, gender, CCI [13].

**Time-to-event analysis**: Kaplan-Meier curves stratified by SI-derivative quartile, using hospital length of stay as the time axis. As in-hospital mortality is a binary endpoint, these curves serve as a visual supplement to the primary competing risk analysis. Log-rank tests for group separation.

**Cumulative incidence functions**: For competing risks (in-hospital death vs discharge alive) by DSI quartile [15]. This is the primary method for evaluating the time-dependent probability of in-hospital death accounting for the competing risk of discharge.

**Calibration**: Hosmer-Lemeshow test, Brier score, calibration plots.

**Bootstrap internal validation**: 1000 resamples for optimism-corrected AUC and 95% CI.

**Sensitivity analyses**: (1) Excluding early deaths (ICU LOS<24h); (2) Different measurement windows (first vs max vs mean 24h); (3) Surgical vs non-surgical subgroups; (4) Subtype-specific models.

All analyses: Python 3.13 (pandas, scipy, statsmodels, scikit-learn, matplotlib). P<0.05 = significant.

---

## 3. Results

### 3.1 Study Population

From 546,028 MIMIC-IV admissions, 5,728 complete-case ICU stays with acute abdomen were analyzed (Figure 1). Median age 68 [IQR 57-79] years, 56.0% male, in-hospital mortality 19.9% (n=1,141). Among 1,141 in-hospital deaths, 758 (66.4%) occurred during the ICU stay and 383 (33.6%) occurred after ICU discharge. Baseline characteristics: vasopressor use 43.6%; mechanical ventilation 52.5%; abdominal surgery 67.4%; median lactate 2.0 [IQR 1.3-3.4] mmol/L; median WBC 11.6 [IQR 8.2-16.2] ×10⁹/L; median CCI 3 [IQR 2-5]; median ICU LOS 2.1 [IQR 1.2-4.4] days. Subtype distribution: inflammation (37.5%), other (29.9%), obstruction (20.6%), ischemia (6.2%), perforation (5.8%).

The 36% exclusion rate from full to complete-case dataset (8,933→5,728) was primarily driven by lactate non-availability (64.6% coverage in full dataset). Complete-case patients had higher vasopressor use (43.6% vs 32.3%), mechanical ventilation (52.5% vs 39.9%), and in-hospital mortality (19.9% vs 15.7%), reflecting selection bias toward more severely ill patients who received arterial blood gas monitoring.

### 3.2 DSI Quartile and Mortality Gradient (Table 1)

DSI quartile demonstrated a dramatic in-hospital mortality gradient with highly significant group differences (χ²=229.24, P=2.02×10⁻⁴⁹):

| DSI Quartile | N | In-Hospital Death (%) | ICU Death (%) | Lactate (median) | Vasopressor (%) | Surgery (%) | MV (%) |
|---|---|---|---|---|---|---|---|
| Q1 (Low) | 1,432 | 12.1% (173) | 6.6% | 1.7 | 27.6% | 60.5% | 42.0% |
| Q2 | 1,432 | 14.5% (208) | 7.6% | 1.9 | 39.2% | 64.7% | 49.2% |
| Q3 | 1,432 | 20.3% (291) | 13.0% | 2.0 | 47.3% | 70.5% | 55.8% |
| Q4 (High) | 1,432 | 32.8% (469) | 25.8% | 2.6 | 60.3% | 74.1% | 63.0% |

Higher DSI quartile was associated with progressively higher lactate (KW P<10⁻⁵³), vasopressor use, and surgery rates, confirming DSI as an integrative marker of hemodynamic severity. Notably, the ICU mortality gradient (6.6%→25.8%) paralleled the in-hospital mortality gradient (12.1%→32.8%), with Q4 showing both the highest ICU death proportion and the highest post-ICU death rate.

Cumulative incidence functions demonstrated progressive divergence across DSI quartiles, with Q4 showing the highest cumulative incidence of in-hospital death competing against discharge alive (Figure 9).

### 3.3 Extended Model Analysis (Table 2, Figure 10)

The extended baseline model (age+sex+CCI+lactate+WBC+vasopressor+surgery+MV) achieved AUC=0.765, substantially outperforming the basic baseline (AUC=0.626). Adding DSI to the extended baseline yielded:

| Model | AUC | Optimism-corrected AUC | Categorical NRI (10%/30%) | Category-free NRI | IDI | IDI P |
|---|---|---|---|---|---|---|
| Basic baseline (Age+Sex+CCI) | 0.626 | 0.625 | — | — | — | — |
| Extended baseline | 0.765 | 0.763 | — | — | — | — |
| **Extended + DSI** | **0.773** | **0.771** | **0.046** | **0.283** | **0.017** | **4.88×10⁻¹³** |
| Extended + all SI derivatives | 0.777 | 0.774 | — | — | — | — |

DSI provided statistically significant incremental value over the extended baseline (ΔAUC=+0.008, categorical NRI=0.046, category-free NRI=0.283, IDI=0.017, Z-test P=4.88×10⁻¹³). Although the AUC improvement is modest in magnitude, the categorical NRI indicates that 4.6% of patients were correctly reclassified across clinically meaningful risk strata (<10%, 10-30%, >30%). This demonstrates that even after adjusting for the strongest ICU predictors (lactate, vasopressor use), DSI captures additional hemodynamic information relevant to acute abdomen mortality.

Bootstrap validation confirmed minimal optimism (≤0.003 for all models), indicating robust model performance without overfitting.

### 3.4 Sensitivity Analyses (Table 3)

| Analysis | N | AUC (Extended+DSI) |
|---|---|---|
| DSI first measurement | 5,728 | 0.769 |
| DSI maximum | 5,728 | 0.770 |
| **DSI mean 24h** | **5,728** | **0.773** |
| **Non-surgical subgroup** | **1,865** | **0.804** |
| Surgical subgroup | 3,863 | 0.760 |
| Inflammation subtype | 2,149 | 0.795 |
| Obstruction subtype | 1,180 | 0.736 |
| Perforation subtype | 334 | 0.759 |
| Ischemia subtype | 353 | 0.789 |
| Other subtype | 1,712 | 0.779 |

Key findings: (1) 24h mean consistently outperformed first/max measurements; (2) Non-surgical subgroup showed the best prediction (AUC=0.804), suggesting DSI is particularly useful when surgical intervention has not yet altered hemodynamics; (3) Subtype-specific models showed variable performance, with ischemia (AUC=0.780) and inflammation (AUC=0.794) demonstrating the best discrimination.

### 3.5 Incremental Value over Basic Baseline (Tables 3-4, Figures 2-3)

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

Significant overall associations (P_overall<0.001) were observed for all four SI derivatives, supporting continuous risk interpretation. The nonlinear component was not significant for SI and DSI (P_nonlinear>0.05), but showed modest nonlinearity for MSI (P=0.004) and Age-SI (P=0.040):

| Metric | P_overall | P_nonlinear |
|---|---|---|
| SI | <0.001 | 0.417 |
| MSI | <0.001 | 0.004 |
| DSI | <0.001 | 0.067 |
| Age-SI | <0.001 | 0.040 |

### 3.8 Time-to-Event Analysis (Figure 5, Table 5)

DSI quartile showed highly significant survival separation using hospital LOS as the time axis (Log-rank χ²=71.2, P=2.33×10⁻¹⁵). Higher DSI quartiles were associated with progressively lower in-hospital survival. However, because in-hospital mortality is a binary endpoint and discharge alive introduces informative censoring, these KM curves should be interpreted as a visual supplement. The primary competing risk analysis using cumulative incidence functions (Section 3.2, Figure 9) provides a more rigorous assessment of the time-dependent probability of in-hospital death.

### 3.9 Calibration (Figure 6, Table 6)

Baseline+DSI showed the best calibration (HL P=0.236, Brier=0.111). Baseline alone was poorly calibrated (HL P=0.009).

### 3.10 Multivariable Regression (Figure 7, Table 7)

In the extended baseline + DSI model, DSI (OR=2.53, 95% CI 2.08-3.07, P<10⁻¹³) remained a strong independent predictor of in-hospital mortality after adjusting for age, sex, CCI, lactate, WBC, vasopressor use, surgery, and mechanical ventilation. Lactate (OR=1.21, P<10⁻¹⁵), mechanical ventilation (OR=2.11, P<10⁻¹⁵), and vasopressor use (OR=1.80, P<10⁻¹³) were also significantly associated with mortality. Surgery was protective (OR=0.70, P<10⁻⁴). This model avoids the multicollinearity among the four SI derivatives while demonstrating DSI's independent contribution.

The competing risk of discharge alive was evaluated using cumulative incidence functions (Figure 9), which demonstrated progressive divergence across DSI quartiles. Q4 showed the highest cumulative incidence of in-hospital death, confirming that DSI's prognostic value persists when accounting for discharge as a competing event.

### 3.11 Subgroup Analysis (Figure 8, Table 8)

**Inflammation** (n=2,149, in-hospital mortality 16.8%): Extended+DSI AUC=0.795 [0.768-0.818].
**Obstruction** (n=1,180, in-hospital mortality 21.5%): Extended+DSI AUC=0.736 [0.704-0.769].
**Perforation** (n=334, in-hospital mortality 28.1%): Extended+DSI AUC=0.759 [0.699-0.817].
**Ischemia** (n=353, in-hospital mortality 40.5%): Extended+DSI AUC=0.789 [0.740-0.834].
**Other** (n=1,712, in-hospital mortality 16.9%): Extended+DSI AUC=0.779 [0.748-0.810].
**Non-surgical** (n=1,865, in-hospital mortality 20.9%): AUC=0.804—best prediction performance.

---

## 4. Discussion

This study provides one of the most comprehensive evaluations of shock index-derived parameters in acute abdomen ICU patients, incorporating extended covariates, bootstrap validation, sensitivity analyses, competing risk framework, and STROBE-compliant reporting. Six principal findings emerge.

**First**, DSI provided statistically significant incremental value beyond the extended baseline model (AUC 0.765→0.773, categorical NRI=0.046, category-free NRI=0.283, IDI=0.017, P=4.88×10⁻¹³). Although the magnitude of AUC improvement is modest (ΔAUC=0.008), the categorical NRI indicates meaningful reclassification across clinical risk strata. This is particularly noteworthy because the extended baseline already includes lactate—the strongest single mortality predictor—and vasopressor use, both established markers of hemodynamic instability. That DSI captures additional prognostic information beyond these suggests that the HR/DBP ratio reflects a hemodynamic dimension not fully captured by lactate (tissue perfusion) or vasopressor use (pharmacologic support). The clinical utility of DSI should be evaluated together with DCA, NRI, and cost-effectiveness considerations.

**Second**, the DSI quartile in-hospital mortality gradient (12.1%→32.8%, P=2.02×10⁻⁴⁹) represents a 2.7-fold difference between Q1 and Q4, with progressively higher lactate, vasopressor use, and surgery rates across quartiles. This establishes DSI as an integrative marker that captures both hemodynamic severity and downstream clinical interventions.

**Third**, we observed that among 1,141 in-hospital deaths, 383 (33.6%) occurred after ICU discharge. This substantial proportion of post-ICU deaths highlights the clinical importance of using in-hospital mortality as the primary endpoint rather than ICU-specific mortality alone. Patients who survive the ICU but later die in the hospital represent a clinically important population where early risk stratification could guide post-ICU monitoring intensity and discharge planning.

**Fourth**, bootstrap validation confirmed minimal optimism (≤0.003 across all models), indicating robust model performance. The optimism-corrected AUC for extended+DSI (0.771) closely matched the apparent AUC (0.773), providing confidence against overfitting concerns.

**Fifth**, sensitivity analyses demonstrated robust results across 10 scenarios. The non-surgical subgroup (AUC=0.804) showed the best prediction, suggesting DSI is most informative before surgical intervention alters hemodynamics. The 24h mean consistently outperformed first/max measurements, supporting sustained hemodynamic assessment rather than single-point evaluation.

**Sixth**, RCS analysis confirmed significant overall dose-response relationships for all four SI derivatives (P_overall<0.001), with modest nonlinear components for MSI and Age-SI, supporting continuous risk interpretation. This aligns with the quartile-based mortality gradient and contrasts with trauma studies showing SI≥1.0 thresholds.

### 4.1 Pathophysiological Rationale for DSI Superiority

DSI (HR/DBP) captures the relationship between cardiac output proxy (HR) and diastolic perfusion pressure (DBP). In acute abdomen, particularly ischemia, progressive vasodilation from inflammatory mediators and splanchnic vascular compromise first manifests as diastolic pressure decline—reflecting loss of peripheral vascular tone before systolic compensatory mechanisms fail. This makes DSI more sensitive to early hemodynamic deterioration than SI (HR/SBP), which primarily reflects systolic compensatory capacity. The original description of DSI by Ospina-Tascón et al. [5] in septic shock patients demonstrated that HR-to-DAP ratios were associated with 28-day mortality and ICU length of stay, and our findings extend this to the acute abdomen context.

### 4.2 Comparison with Previous Studies

Our NRI/IDI results extend Jouffroy et al. [4] (SI/MSI/DSI/Age-SI in septic shock), Ospina-Tascón et al. [5] (DSI in septic shock), and Hou et al. [18] (MSI in emergency patients) by demonstrating incremental value beyond established ICU predictors. The linear RCS relationships contrast with trauma threshold effects at SI≥1.0 [7], reflecting different hemodynamic patterns in acute abdomen. Our bootstrap validation and STROBE-compliant reporting [14] further address methodological gaps identified in prior SI-derivative studies.

### 4.3 Clinical Implications

DSI (mean 24h) provides the most effective risk stratification with: (1) statistically significant incremental value over lactate/vasopressor-adjusted models, though modest in AUC magnitude; (2) dramatic quartile mortality gradient; (3) robust sensitivity analyses across 10 scenarios; (4) validated by bootstrap. In ischemia (in-hospital mortality 40.5%), the extended+DSI model showed good discrimination (AUC=0.789). These indices, from routinely monitored vital signs, can be integrated into ICU workflow without additional cost. The substantial proportion of post-ICU deaths (33.6%) underscores that DSI-based risk stratification should also guide post-ICU monitoring and discharge decisions.

### 4.4 Limitations

(1) Single-center retrospective study from a US tertiary academic hospital, potentially limiting generalizability; (2) 36% exclusion rate for incomplete extended covariates (primarily lactate, 64.6% coverage in full dataset) introduces selection bias toward more severely ill patients who received arterial blood gas monitoring, as reflected by higher vasopressor use (43.6% vs 32.3%) and mechanical ventilation (52.5% vs 39.9%) in complete cases; (3) The "Other" subtype (29.9%) is heterogeneous, potentially diluting subtype-specific effects; (4) Although cumulative incidence functions account for the competing risk of discharge, a formal Fine-Gray subdistribution hazard model was not fitted; future studies should use dedicated competing-risk regression packages; (5) The mechanical ventilation indicator derived from chartevents itemids may have limited accuracy; (6) The Kaplan-Meier analysis uses hospital LOS as the time axis for a binary outcome (in-hospital mortality) and is subject to informative censoring; the CIF analysis (Figure 9) provides a more rigorous competing-risk assessment; (7) No external validation cohort was used, and the bootstrap internal validation, while robust, cannot replace external validation in a different population; (8) Multiple imputation was not performed; future studies should evaluate whether imputation-based approaches yield consistent results.

### 4.5 Future Directions

Prospective multicenter validation; integration with SOFA/APACHE scores; time-series trajectory analysis; formal Fine-Gray subdistribution hazard modeling with dedicated survival packages; external validation in eICU or other databases; evaluation of DSI trajectory patterns as dynamic risk markers; multiple imputation sensitivity analysis.

---

## 5. Conclusions

DSI provided statistically significant incremental predictive value for in-hospital mortality in acute abdomen beyond established ICU covariates (lactate, vasopressor use, surgery), though the magnitude of AUC improvement was modest (ΔAUC=0.008) and should be interpreted alongside the categorical NRI (0.046) and IDI (0.017). The mortality gradient across DSI quartiles (12.1%→32.8%, P=2.02×10⁻⁴⁹), bootstrap validation (optimism ≤0.003), and consistent sensitivity analyses across 10 scenarios support DSI as a practical risk-stratification tool. The substantial proportion of post-ICU deaths (33.6% of hospital deaths) underscores the value of in-hospital mortality as the primary endpoint. Prediction was most pronounced in ischemia (in-hospital mortality 40.5%) and non-surgical acute abdomen (AUC=0.804). These readily calculable vital sign indices may enhance early risk stratification in this heterogeneous population.

---

## Supplementary Materials

**Table S1**: Complete list of ICD-9 and ICD-10 codes used for acute abdomen identification and subtype classification.

**Table S2**: STROBE checklist (completed).

**Table S3**: Baseline characteristics of the complete-case cohort (N=5,728) by DSI quartile, including all continuous variables reported as median [IQR] and categorical variables as n (%).

**Figure S1**: Calibration plots for basic baseline, basic baseline + DSI, basic baseline + all SI derivatives models.

**Note on complete-case analysis**: Complete-case analysis was chosen over multiple imputation because (1) the primary missing variable (lactate, 35.4% missing) is not missing completely at random—patients with arterial blood gas monitoring are more severely ill; (2) imputation under a missing-at-random assumption could introduce bias; and (3) the complete-case cohort (N=5,728) retains sufficient statistical power for all pre-specified analyses. The selection bias introduced by this approach is acknowledged in the Limitations.

---

## Figure Legends

**Figure 1**: Study flow diagram showing patient selection from MIMIC-IV v3.1 (546,028 total admissions) through acute abdomen ICD codes, adult ED admissions, ICU stays, complete vital signs, and complete-case analysis cohort (N=5,728).

**Figure 2**: ROC curves comparing basic baseline, extended baseline, extended+DSI, and extended+all SI derivatives for in-hospital mortality prediction (complete-case cohort, N=5,728). Shaded areas represent 95% confidence bands. AUC values with 95% CIs are shown in the legend.

**Figure 3**: Decision curve analysis showing net benefit across threshold probabilities (1-50%) for basic baseline, extended baseline, extended+DSI, and full model. Net benefit represents true positives per 100 patients, with false positives weighted by the threshold probability.

**Figure 4**: Restricted cubic spline curves for SI, MSI, DSI, and Age-SI (24h mean) showing adjusted odds ratios for in-hospital mortality. The solid line represents the point estimate; shaded areas represent 95% CIs. The horizontal dotted line indicates OR=1 (no association). P_overall and P_nonlinear values are annotated in each panel.

**Figure 5**: Kaplan-Meier in-hospital survival curves by DSI quartile (Q1=lowest to Q4=highest), using hospital length of stay (days) as the time axis. Note: Because in-hospital mortality is a binary endpoint and discharge alive introduces informative censoring, these curves serve as a visual supplement to the competing risk analysis (Figure 9). Log-rank P-value is shown.

**Figure 6**: Calibration plots for basic baseline, extended baseline, extended+DSI, and extended+all SI models. Dots represent deciles of predicted probability; the diagonal line represents perfect calibration. Hosmer-Lemeshow P-values and Brier scores are annotated.

**Figure 7**: Forest plot of adjusted odds ratios from the extended baseline + DSI multivariable logistic regression model. Squares represent point estimates; horizontal lines represent 95% CIs. The vertical dotted line indicates OR=1 (no effect).

**Figure 8**: Subgroup ROC curves for extended baseline (dashed) versus extended+DSI (solid) by acute abdomen subtype (inflammation, obstruction, perforation, ischemia, other). Panel F shows the summary AUC comparison. Colorblind-safe palette used throughout.

**Figure 9**: Cumulative incidence functions for in-hospital death by DSI quartile under the competing risk of discharge alive. The Y-axis represents the cumulative probability of in-hospital death. This is the primary competing risk analysis.

**Figure 10**: ROC curves comparing extended baseline, extended+DSI, and extended+all SI derivatives for in-hospital mortality prediction. AUC values with 95% CIs and ΔAUC are annotated.

---

## Declarations

**Ethics statement**: This study used the publicly available MIMIC-IV database, which was approved by the Institutional Review Boards of Beth Israel Deaconess Medical Center (Boston, MA) and the Massachusetts Institute of Technology. Individual informed consent was waived due to the use of de-identified data. No additional ethical approval was required for this secondary analysis.

**Funding**: This work was supported by the Chronic Disease Management Research Project, National Health Commission Capacity Building and Continuing Education Center (Grant No. GWJJMB202510024181), the Changsha Science and Technology Bureau Project [kq2014242], and the Hunan Provincial Natural Science Foundation [2021JJ30959]. **Conflicts of interest**: The authors declare no conflicts of interest.

**Author contributions**: Jiqiang Liu: Conceptualization, Data curation, Formal analysis, Methodology, Software, Visualization, Writing – original draft. Dengke Wu: Conceptualization, Supervision, Writing – review & editing, Funding acquisition, Project administration. All authors read and approved the final manuscript.

**Acknowledgments**: The authors thank the MIMIC-IV team for providing open access to the clinical database used in this study.

**Data availability**: MIMIC-IV v3.1 at https://physionet.org/content/mimiciv/3.1/. Code available on request from the corresponding author.

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
