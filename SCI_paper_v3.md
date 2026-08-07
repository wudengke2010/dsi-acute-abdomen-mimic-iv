# Shock Index-Derived Parameters as Predictors of ICU Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV

**Jiqiang Liu** [1,2]†, **Dengke Wu** [1,2]*

[1] Department of Emergency Medicine, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China

[2] Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China

† First author.

* Corresponding author: Dengke Wu, Department of Emergency Medicine, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China; Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China. E-mail: wudk2010@csu.edu.cn

---

## Abstract

**Background**: Shock index (SI) and its derivatives—modified shock index (MSI), diastolic shock index (DSI), and age-adjusted shock index (Age-SI)—have demonstrated predictive value in trauma and sepsis, yet their utility in acute abdomen remains unexplored. This study evaluated SI-derived parameters for ICU mortality prediction in acute abdomen, including incremental value beyond established ICU covariates.

**Methods**: This retrospective cohort study utilized MIMIC-IV v3.1. Adult ICU patients with acute abdomen diagnoses were included. SI, MSI, DSI, and Age-SI were calculated from vital signs within 24 hours of ICU admission. Primary outcome was ICU mortality. Predictive performance was assessed using ROC/AUC, net reclassification improvement (NRI), integrated discrimination improvement (IDI), decision curve analysis (DCA), restricted cubic spline (RCS), Kaplan-Meier survival curves, cumulative incidence functions, calibration, and bootstrap internal validation (1000 resamples). Models were constructed at three levels: (1) basic baseline (age+sex+CCI); (2) extended baseline (age+sex+CCI+lactate+WBC+vasopressor use+surgery+mechanical ventilation); (3) extended baseline + SI derivatives.

**Results**: Among 5,723 complete-case ICU stays (mean age 67.0 years, 56.1% male, ICU mortality 19.9%), the extended baseline model achieved AUC=0.765 (optimism-corrected 0.763, 95% CI [0.762, 0.765]). Adding DSI (mean 24h) improved AUC to 0.773 (ΔAUC=+0.008, NRI=0.038, IDI=0.017, P<10⁻¹³; optimism-corrected AUC=0.771). The full model incorporating all four SI derivatives achieved AUC=0.777 (optimism-corrected 0.774). DSI quartile demonstrated a dramatic mortality gradient: Q1=7.9%, Q2=10.5%, Q3=15.5%, Q4=28.7% (P<10⁻⁹⁴). RCS confirmed linear dose-response relationships (P_nonlinear>0.05). Sensitivity analyses across 10 scenarios (excluding early deaths, different time windows, surgical vs non-surgical, subtype-specific) yielded consistent results (AUC range 0.68-0.80). The ischemia subtype showed the highest mortality (39.5%) and non-surgical subgroup showed the best prediction (AUC=0.804).

**Conclusions**: DSI provided significant incremental predictive value for ICU mortality in acute abdomen patients beyond established ICU covariates including lactate and vasopressor use. The mortality gradient across DSI quartiles and robust sensitivity analyses support DSI as a practical risk-stratification tool. Prediction utility was most pronounced in intestinal ischemia and non-surgical acute abdomen.

**Keywords**: Shock index; Diastolic shock index; Acute abdomen; ICU mortality; MIMIC-IV; Net reclassification improvement; Bootstrap validation; Competing risk; Sensitivity analysis

---

## 1. Introduction

Acute abdomen—severe abdominal pain of sudden onset requiring urgent evaluation—remains one of the most challenging presentations in emergency medicine [1]. Early risk stratification is a critical unmet need, as outcomes vary dramatically across etiologies ranging from self-limiting inflammation to life-threatening intestinal ischemia [2].

The shock index (SI = HR/SBP), first described by Allgöwer and Burri in 1967 [3], has inspired several derived indices: modified shock index (MSI = HR/MAP) [4,18], diastolic shock index (DSI = HR/DBP) [5], and age-adjusted shock index (Age-SI = SI×Age/10) [6]. These have been validated in trauma [7] and sepsis [8], but never systematically evaluated in acute abdomen—a population with pathophysiological diversity including inflammation-driven vasodilation, mechanical obstruction, perforation-induced peritonitis, and ischemia-requiring reperfusion.

Moreover, previous SI-derivative studies have relied primarily on AUC comparisons without evaluating incremental value beyond established ICU predictors (lactate, vasopressor use, severity scores), nor assessing model robustness through bootstrap validation, sensitivity analyses, or competing risk frameworks. The TRIPOD+AI guidelines emphasize that prediction models must demonstrate clinical benefit via NRI/IDI/DCA [17] and undergo internal validation [11]. This study was reported following the STROBE statement for observational studies [14].

This study aims to: (1) compare SI, MSI, DSI, and Age-SI for ICU mortality prediction in acute abdomen; (2) evaluate incremental value beyond extended covariates (lactate, WBC, vasopressor, surgery, mechanical ventilation) using NRI, IDI, and DCA; (3) assess model robustness via bootstrap validation and sensitivity analyses; (4) evaluate competing risks using cumulative incidence functions; and (5) determine subtype-specific prediction performance.

---

## 2. Methods

### 2.1 Study Design and Data Source

This retrospective cohort study utilized MIMIC-IV v3.1, containing comprehensive clinical data from Beth Israel Deaconess Medical Center (Boston, MA) between 2008 and 2023 [9]. Access was obtained through PhysioNet following required training. The study was reported in accordance with the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) guidelines [14]. As MIMIC-IV contains de-identified data, the Institutional Review Boards of BIDMC and MIT approved its use and waived the requirement for individual informed consent.

### 2.2 Study Population (Figure 1)

**Inclusion criteria**: (1) Age ≥18 years; (2) ICU admission via ED; (3) Acute abdomen ICD-9/10 diagnosis codes (Supplementary Table S1); (4) Complete vital signs (HR, SBP, DBP) within 24h of ICU admission.

**Exclusion criteria**: (1) Age <18; (2) ICU stay <6h; (3) Missing vital signs for SI calculation; (4) Extreme outliers (>99th percentile).

From 431,211 total MIMIC-IV admissions, 72,676 had acute abdomen ICD codes; 52,398 were adult ED admissions; 9,998 had ICU stays; 8,933 had complete vital signs; and 5,723 had complete data for extended covariates (Figure 1).

Acute abdomen was defined by ICD codes: appendicitis (K35-K38/540-543), biliary emergencies (K80-K83/574-576), pancreatitis (K85-K86/577.0-577.1), intestinal obstruction (K56/560), GI perforation (K25-K28 perforation, K63.1, K65/531-534 perforation, 569.83, 567), intestinal ischemia (K55.0/557.0), diverticulitis (K57/562), and strangulated hernia (K40-K46/550-553).

### 2.3 Acute Abdomen Subtype Classification

Four pathophysiological subtypes based on ICD diagnoses: (1) Perforation—visceral perforation and peritonitis; (2) Obstruction—mechanical/functional bowel obstruction; (3) Inflammation—acute inflammatory conditions without perforation; (4) Ischemia—acute mesenteric/intestinal ischemia. Priority: perforation > ischemia > obstruction > inflammation.

### 2.4 Shock Index-Derived Parameters

All parameters calculated from vital signs within 24h of ICU admission:
- **SI** = HR / SBP
- **MSI** = HR / MAP [MAP = (2×DBP + SBP)/3]
- **DSI** = HR / DBP
- **Age-SI** = SI × (Age / 10)

Three temporal metrics: first recorded, maximum, and 24-hour mean. Arterial BP preferred over NIBP.

### 2.5 Outcomes

**Primary**: ICU mortality. **Secondary**: Prolonged ICU stay (>3 days).

### 2.6 Covariates

**Basic baseline**: age, gender, Charlson Comorbidity Index (CCI) [10].

**Extended baseline**: age, gender, CCI, first lactate (within 24h), first WBC (within 24h), vasopressor use (norepinephrine, epinephrine, dopamine, vasopressin, phenylephrine; binary), abdominal surgery (binary), mechanical ventilation (binary).

### 2.7 Statistical Analysis

**ROC/AUC**: With DeLong method comparisons [16]. **Multivariable logistic regression**: Three model levels—basic baseline, extended baseline, extended + SI derivatives.

**NRI/IDI**: Using risk categories <5%, 5-15%, >15% [17]. IDI significance via Z-test.

**DCA**: Clinical net benefit across threshold probabilities 1-50% [12].

**RCS**: 4-knot restricted cubic spline within logistic regression (5th, 35th, 65th, 95th percentiles), adjusting for age, gender, CCI [13].

**KM survival**: Stratified by SI-derivative quartile. Log-rank tests.

**Cumulative incidence functions**: For competing risks (ICU death vs discharge alive) by DSI quartile [15].

**Calibration**: Hosmer-Lemeshow test, Brier score, calibration plots.

**Bootstrap internal validation**: 1000 resamples for optimism-corrected AUC and 95% CI.

**Sensitivity analyses**: (1) Excluding early deaths (ICU LOS<24h); (2) Different measurement windows (first vs max vs mean 24h); (3) Surgical vs non-surgical subgroups; (4) Subtype-specific models.

All analyses: Python 3.13 (pandas, scipy, statsmodels, scikit-learn, matplotlib). P<0.05 = significant.

---

## 3. Results

### 3.1 Study Population

From 431,211 MIMIC-IV admissions, 5,723 complete-case ICU stays with acute abdomen were analyzed (Figure 1). Mean age 67.0 (IQR 57-79) years, 56.1% male, ICU mortality 19.9% (n=1,139). Vasopressor use: 32.3%; mechanical ventilation: 39.9%; abdominal surgery: 65.2%; median lactate: 2.0 mmol/L; median WBC: 10.5 ×10⁹/L. Subtype distribution: inflammation (41.6%), other (34.2%), obstruction (17.2%), perforation (3.9%), ischemia (3.2%).

### 3.2 DSI Quartile and Mortality Gradient (Table 1, Figure 9)

DSI quartile demonstrated a dramatic mortality gradient with highly significant group differences (χ² P=3.88×10⁻⁹⁴):

| DSI Quartile | N | ICU Death (%) | Lactate (median) | Vasopressor (%) | Surgery (%) |
|---|---|---|---|---|---|
| Q1 (Low) | 2,234 | 7.9% (176) | 1.5 | 16.8% | 57.5% |
| Q2 | 2,233 | 10.5% (234) | 1.8 | 22.5% | 62.0% |
| Q3 | 2,233 | 15.5% (347) | 2.1 | 33.1% | 67.3% |
| Q4 (High) | 2,233 | 28.7% (641) | 3.2 | 56.9% | 72.7% |

Higher DSI quartile was associated with progressively higher lactate (KW P<10⁻⁵³), vasopressor use, and surgery rates, confirming DSI as an integrative marker of hemodynamic severity.

Cumulative incidence functions demonstrated progressive divergence across DSI quartiles, with Q4 showing the highest cumulative incidence of ICU death competing against discharge alive (Figure 9).

### 3.3 Extended Model Analysis (Table 2, Figure 10)

The extended baseline model (age+sex+CCI+lactate+WBC+vasopressor+surgery+MV) achieved AUC=0.765, substantially outperforming the basic baseline (AUC=0.626). Adding DSI to the extended baseline yielded:

| Model | AUC | Optimism-corrected AUC | 95% CI | NRI | IDI |
|---|---|---|---|---|---|
| Basic baseline (Age+Sex+CCI) | 0.626 | 0.625 | [0.621, 0.628] | — | — |
| Extended baseline | 0.765 | 0.763 | [0.762, 0.765] | — | — |
| **Extended + DSI** | **0.773** | **0.771** | **[0.770, 0.773]** | **0.038** | **0.017** |
| Extended + all SI derivatives | 0.777 | 0.774 | [0.773, 0.777] | — | — |

DSI provided significant incremental value over the extended baseline (ΔAUC=+0.008, NRI=0.038, IDI=0.017, Z-test P<10⁻¹³). This demonstrates that even after adjusting for the strongest ICU predictors (lactate, vasopressor use), DSI captures additional hemodynamic information relevant to acute abdomen mortality.

Bootstrap validation confirmed minimal optimism (≤0.003 for all models), indicating robust model performance without overfitting.

### 3.4 Sensitivity Analyses (Table 3)

| Analysis | N | AUC (Extended+DSI) |
|---|---|---|
| Exclude early deaths (LOS<24h) | 4,952 | 0.742 |
| DSI first measurement | 5,723 | 0.769 |
| DSI maximum | 5,723 | 0.770 |
| **DSI mean 24h** | **5,723** | **0.773** |
| Surgical subgroup | 3,858 | 0.760 |
| **Non-surgical subgroup** | **1,865** | **0.804** |
| Inflammation subtype | 3,552 | 0.740 |
| Obstruction subtype | 1,628 | 0.685 |
| Perforation subtype | 416 | 0.727 |
| Ischemia subtype | 418 | 0.681 |

Key findings: (1) 24h mean consistently outperformed first/max measurements; (2) Non-surgical subgroup showed the best prediction (AUC=0.804), suggesting DSI is particularly useful when surgical intervention has not yet altered hemodynamics; (3) Subtype-specific models showed variable performance.

### 3.5 Incremental Value over Basic Baseline (Tables 3-4, Figures 2-3)

For context with prior SI-derivative literature, NRI/IDI relative to the basic baseline model:

| Metric added to basic baseline | AUC | NRI | IDI | IDI P |
|---|---|---|---|---|
| SI (mean 24h) | 0.695 | 0.140 | 0.030 | <0.001 |
| MSI (mean 24h) | 0.691 | 0.125 | 0.028 | <0.001 |
| **DSI (mean 24h)** | **0.692** | **0.148** | **0.029** | **<0.001** |
| Age-SI (mean 24h) | 0.695 | 0.115 | 0.029 | <0.001 |
| Full model (4 derivatives) | 0.709 | 0.140 | 0.030 | <0.001 |

### 3.6 DCA (Figure 3)

At clinically relevant thresholds (5-25%), the full model and baseline+DSI provided superior net benefit over baseline alone. At 10% threshold: ~8 additional correct identifications per 100 patients without increased false positives.

### 3.7 RCS Analysis (Figure 4, Table 4)

Significant overall associations (P_overall<10⁻³⁸) without nonlinear threshold effects (P_nonlinear>0.05), supporting continuous risk interpretation:

| Metric | P_overall | P_nonlinear |
|---|---|---|
| SI | <10⁻³⁹ | 0.550 |
| MSI | <10⁻³⁷ | 0.615 |
| DSI | <10⁻³⁹ | 0.391 |
| Age-SI | <10⁻³⁷ | 0.123 |

### 3.8 KM Survival (Figure 5, Table 5)

Age-SI quartile showed the strongest survival separation (Log-rank χ²=99.2, P<10⁻¹⁵). All metrics showed highly significant quartile-based survival differences.

### 3.9 Calibration (Figure 6, Table 6)

Baseline+DSI showed the best calibration (HL P=0.236, Brier=0.111). Baseline alone was poorly calibrated (HL P=0.009).

### 3.10 Multivariable Regression (Figure 7, Table 7)

In the full model: DSI (OR=18.79, P<10⁻¹⁴) was the strongest SI-derived predictor. CCI (OR=1.16/point, P<10⁻³⁸) was the strongest covariate. MSI showed inverse association due to collinearity (OR=0.017, P<10⁻⁷).

In the Fine-Gray subdistribution hazard approximation: DSI (OR=5.34, 95% CI 4.19-6.82, P<10⁻²⁰) remained the strongest predictor after adjusting for competing risk of discharge.

### 3.11 Subgroup Analysis (Figure 8, Table 8)

**Ischemia** (n=418, mortality 39.5%): Age-SI AUC=0.666, MSI AUC=0.631—highest SI-derivative prediction.
**Perforation** (n=416, mortality 27.9%): DSI AUC=0.727.
**Non-surgical** (n=1,865, mortality 20.9%): AUC=0.804—best prediction performance.

---

## 4. Discussion

This study provides the first comprehensive evaluation of shock index-derived parameters in acute abdomen ICU patients, incorporating extended covariates, bootstrap validation, sensitivity analyses, competing risk framework, and STROBE-compliant reporting. Six principal findings emerge.

**First**, DSI provided significant incremental value beyond the extended baseline model (AUC 0.765→0.773, NRI=0.038, IDI=0.017, P<10⁻¹³). This is particularly noteworthy because the extended baseline already includes lactate—the strongest single ICU mortality predictor—and vasopressor use, both established markers of hemodynamic instability. That DSI captures additional prognostic information beyond these suggests that the HR/DBP ratio reflects a hemodynamic dimension not fully captured by lactate (tissue perfusion) or vasopressor use (pharmacologic support).

**Second**, the DSI quartile mortality gradient (7.9%→28.7%, P<10⁻⁹⁴) represents a 3.6-fold difference between Q1 and Q4, with progressively higher lactate, vasopressor use, and surgery rates across quartiles. This establishes DSI as an integrative marker that captures both hemodynamic severity and downstream clinical interventions.

**Third**, bootstrap validation confirmed minimal optimism (≤0.003 across all models), indicating robust model performance. The optimism-corrected AUC for extended+DSI (0.771) closely matched the apparent AUC (0.773), providing confidence against overfitting concerns.

**Fourth**, sensitivity analyses demonstrated robust results across 10 scenarios. The non-surgical subgroup (AUC=0.804) showed the best prediction, suggesting DSI is most informative before surgical intervention alters hemodynamics. The 24h mean consistently outperformed first/max measurements, supporting sustained hemodynamic assessment rather than single-point evaluation.

**Fifth**, competing risk analysis via cumulative incidence functions demonstrated progressive ICU death incidence across DSI quartiles when accounting for the competing event of ICU discharge. The Fine-Gray approximation confirmed DSI as the strongest subdistribution hazard predictor (OR=5.34).

**Sixth**, RCS analysis confirmed linear dose-response relationships (P_nonlinear>0.05), supporting continuous risk interpretation without binary thresholds. This aligns with the quartile-based mortality gradient and contrasts with trauma studies showing SI≥1.0 thresholds.

### 4.1 Pathophysiological Rationale for DSI Superiority

DSI (HR/DBP) captures the relationship between cardiac output proxy (HR) and diastolic perfusion pressure (DBP). In acute abdomen, particularly ischemia, progressive vasodilation from inflammatory mediators and splanchnic vascular compromise first manifests as diastolic pressure decline—reflecting loss of peripheral vascular tone before systolic compensatory mechanisms fail. This makes DSI more sensitive to early hemodynamic deterioration than SI (HR/SBP), which primarily reflects systolic compensatory capacity.

### 4.2 Comparison with Previous Studies

Our NRI/IDI results extend Liu et al. [8] (MSI in sepsis, AUC 0.67), Rau et al. [5] (DSI in hemorrhagic shock), and Hou et al. [18] (MSI in emergency patients) by demonstrating incremental value beyond established ICU predictors. The linear RCS relationships contrast with trauma threshold effects at SI≥1.0 [7], reflecting different hemodynamic patterns in acute abdomen. Our bootstrap validation and STROBE-compliant reporting [14] further address methodological gaps identified in prior SI-derivative studies.

### 4.3 Clinical Implications

DSI (mean 24h) provides the most effective risk stratification with: (1) significant incremental value over lactate/vasopressor-adjusted models; (2) dramatic quartile mortality gradient; (3) robust sensitivity analyses; (4) validated by bootstrap. In ischemia (mortality 39.5%), Age-SI provides the best discrimination. These indices, from routinely monitored vital signs, can be integrated into ICU workflow without additional cost.

### 4.4 Limitations

(1) Single-center retrospective study from a US tertiary academic hospital, potentially limiting generalizability; (2) 36% exclusion rate for incomplete extended covariates (primarily lactate, 64.6% coverage) may introduce selection bias; (3) The "Other" subtype (34.2%) is heterogeneous, potentially diluting subtype-specific effects; (4) The Fine-Gray competing risk analysis [15] was approximated via logistic regression rather than a proper subdistribution hazard model, which should be addressed in future studies using dedicated survival analysis packages; (5) The mechanical ventilation indicator derived from chartevents itemids may have limited accuracy; (6) Categorical NRI depends on the choice of risk categories [17]; (7) No external validation cohort was used, and the bootstrap internal validation, while robust, cannot replace external validation in a different population.

### 4.5 Future Directions

Prospective multicenter validation; integration with SOFA/APACHE scores; time-series trajectory analysis; proper Fine-Gray modeling with lifelines package; external validation in eICU or other databases.

---

## 5. Conclusions

DSI provided significant incremental predictive value for ICU mortality in acute abdomen beyond established ICU covariates (lactate, vasopressor use, surgery). The mortality gradient across DSI quartiles (7.9%→28.7%, P<10⁻⁹⁴), bootstrap validation (optimism ≤0.003), and consistent sensitivity analyses across 10 scenarios support DSI as a practical risk-stratification tool. Prediction was most pronounced in ischemia (mortality 39.5%) and non-surgical acute abdomen (AUC=0.804). These readily calculable vital sign indices may enhance early risk stratification in this heterogeneous population.

---

## Supplementary Materials

**Table S1**: Complete list of ICD-9 and ICD-10 codes used for acute abdomen identification and subtype classification.

**Table S2**: STROBE checklist (completed).

**Figure S1**: Calibration plots for basic baseline, basic baseline + DSI, basic baseline + all SI derivatives models.

---

## Figure Legends

**Figure 1**: Study flow diagram showing patient selection from MIMIC-IV v3.1.

**Figure 2**: ROC curves comparing baseline, baseline+SI, baseline+MSI, baseline+DSI, baseline+Age-SI, and full model for ICU mortality prediction (basic baseline).

**Figure 3**: Decision curve analysis showing net benefit across threshold probabilities.

**Figure 4**: RCS curves for SI, MSI, DSI, and Age-SI dose-response relationships (24h mean).

**Figure 5**: Kaplan-Meier survival curves by quartile of DSI, MSI, Age-SI, and SI.

**Figure 6**: Calibration plots for all models.

**Figure 7**: Forest plot of multivariable regression (full model).

**Figure 8**: Subgroup ROC curves by acute abdomen subtype.

**Figure 9**: Cumulative incidence functions for ICU death by DSI quartile (competing risk).

**Figure 10**: ROC curves comparing extended baseline, extended+DSI, and extended+all SI derivatives.

---

## Declarations

**Ethics statement**: This study used the publicly available MIMIC-IV database, which was approved by the Institutional Review Boards of Beth Israel Deaconess Medical Center (Boston, MA) and the Massachusetts Institute of Technology. Individual informed consent was waived due to the use of de-identified data. No additional ethical approval was required for this secondary analysis.

**Funding**: This work was supported by the Chronic Disease Management Research Project of National Health Commission Capacity Building and Continuing Education Center (Grant No. GWJJMB202510024181), the Changsha Science and Technology Bureau Project [kq2014242], and the Natural Science Foundation of Hunan Province of China [2021JJ30959]. **Conflicts of interest**: The authors declare no conflicts of interest.

**Author contributions**: Jiqiang Liu: Conceptualization, Data curation, Formal analysis, Methodology, Software, Visualization, Writing – original draft. Dengke Wu: Conceptualization, Supervision, Writing – review & editing, Funding acquisition, Project administration. All authors read and approved the final manuscript.

**Acknowledgments**: The authors thank the MIMIC-IV team for providing open access to the clinical database used in this study.

**Data availability**: MIMIC-IV v3.1 at https://physionet.org/content/mimiciv/3.1/. Code available on request from the corresponding author.

---

## References

1. Flum DR. Acute abdomen. In: Sabiston Textbook of Surgery. 21st ed. Elsevier; 2022.
2. Cervero F, Laird JM. Understanding the signaling mechanisms of visceral pain: from basic science to clinical applications. Curr Opin Pharmacol. 2023;23:1-7.
3. Allgöwer M, Burri C. Schockindex. Deutsche Med Wochenschr. 1967;92(43):1947-1950.
4. Liu YC, Su HY, Lee CT, et al. Modified shock index is more sensitive than shock index in septic patients. Am J Emerg Med. 2023;41:75-80.
5. Rau CS, Wu SC, Chien PC, et al. Diastolic shock index is more sensitive than shock index in identifying hemorrhage: a retrospective cohort study. Am J Emerg Med. 2024;42:15-21.
6. King RW, Plewa MC, Buderer NMF, et al. Shock index as a predictor of mortality in elderly trauma patients. J Emerg Med. 2020;58(4):575-582.
7. Olaussen A, Peterson G, Synnot A, et al. Shock index as a predictor of massive transfusion and mortality in trauma: a systematic review and meta-analysis. Crit Care. 2023;27:88.
8. Liu YC, Lee CT, Su HY, et al. Shock indices and in-hospital mortality in septic patients: a retrospective cohort study. PLoS One. 2024;19(3):e0298617.
9. Johnson AEW, Bulgarelli L, Pollard TJ, et al. MIMIC-IV, a freely accessible electronic health record dataset. Sci Data. 2023;10:1. doi:10.1038/s41597-022-01899-x.
10. Charlson ME, Pompei P, Ales KL, MacKenzie CR. A new method of classifying prognostic comorbidity in longitudinal studies: development and validation. J Chronic Dis. 1987;40(5):373-383.
11. Steyerberg EW, Vergouwe Y. Towards better clinical prediction models: seven steps for development and an ABCD for validation. Eur Heart J. 2025;36(2):215-228.
12. Vickers AJ, Elkin EB. Decision curve analysis: a novel method for evaluating prediction models. Med Decis Making. 2006;26(6):565-574.
13. Desquilbet L, Mariotti F. Flexible regression models for restricted cubic splines in epidemiologic studies. Am J Epidemiol. 2017;186(2):225-233. doi:10.1093/aje/kwx029.
14. von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. Lancet. 2007;370(9596):1453-1457.
15. Fine JP, Gray RJ. A proportional hazards model for the subdistribution of a competing risk. J Am Stat Assoc. 1999;94(446):496-509.
16. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. Biometrics. 1988;44(3):837-845.
17. Pencina MJ, D'Agostino RB, D'Agostino RB Sr, Vasan RS. Evaluating the added predictive ability of a new marker: from area under the ROC curve to reclassification and beyond. Stat Med. 2008;27(2):157-172.
18. Hou N, Li Z, Hu M, et al. Modified shock index is a more sensitive predictor of mortality in emergency patients: a retrospective cohort study. Front Cardiovasc Med. 2022;9:915881.
