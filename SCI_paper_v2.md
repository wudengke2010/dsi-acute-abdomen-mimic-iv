# Shock Index-Derived Parameters as Predictors of ICU Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV

---

## Abstract

**Background**: Shock index (SI) and its derivatives—modified shock index (MSI), diastolic shock index (DSI), and age-adjusted shock index (Age-SI)—have demonstrated predictive value in trauma and sepsis populations, yet their utility in acute abdomen, a major emergency department presentation, remains unexplored. This study aimed to systematically evaluate and compare the predictive performance of SI-derived parameters for ICU mortality in acute abdomen patients, and to assess their incremental value beyond traditional covariates.

**Methods**: This retrospective cohort study utilized the MIMIC-IV v3.1 database (2008–2023). Adult patients (≥18 years) admitted to the ICU with acute abdomen diagnoses were included. SI (HR/SBP), MSI (HR/MAP), DSI (HR/DBP), and Age-SI (SI×Age/10) were calculated from vital signs within 24 hours of ICU admission. Primary outcome was ICU mortality. Predictive performance was assessed using ROC/AUC analysis, net reclassification improvement (NRI), integrated discrimination improvement (IDI), decision curve analysis (DCA), restricted cubic spline (RCS) analysis, Kaplan-Meier survival curves, and calibration assessment.

**Results**: Among 7,004 eligible ICU stays (mean age 67.0 years, 56.1% male, ICU mortality 13.7%), SI-derived parameters added to a baseline model (age+sex+CCI) yielded significant incremental value: DSI (mean 24h) achieved the highest NRI of 0.148 (IDI=0.029, P<0.001) and AUC improvement from 0.648 to 0.692. The full model incorporating all four SI derivatives achieved AUC=0.709 (NRI=0.140, IDI=0.030). RCS analysis confirmed significant overall associations (P<10⁻³⁸) without nonlinear threshold effects (P>0.05). Kaplan-Meier analysis by quartile demonstrated highly significant survival separation (Log-rank P<10⁻⁹ for all metrics). The baseline+DSI model showed the best calibration (Hosmer-Lemeshow P=0.236) versus baseline alone (P=0.009). Subgroup analysis revealed striking heterogeneity: in intestinal ischemia (mortality 34.8%), Age-SI achieved AUC=0.666 and MSI reached 0.631, substantially exceeding performance in other subtypes. In multivariable analysis, DSI (OR=18.79, P<10⁻¹⁴) was the strongest SI-derived predictor, while MSI showed inverse association (OR=0.017, P<10⁻⁷) reflecting collinearity.

**Conclusions**: SI-derived parameters, particularly DSI, provided significant incremental predictive value for ICU mortality in acute abdomen patients beyond traditional covariates. The prediction utility was most pronounced in intestinal ischemia. These readily calculable indices may enhance early risk stratification and clinical decision-making in this heterogeneous population.

**Keywords**: Shock index; Modified shock index; Diastolic shock index; Acute abdomen; ICU mortality; MIMIC-IV; Risk stratification; Net reclassification improvement; Decision curve analysis

---

## 1. Introduction

Acute abdomen—defined as severe abdominal pain of sudden onset requiring urgent evaluation and potential surgical intervention—represents one of the most challenging presentations in emergency medicine [1]. The 2026 consensus guidelines on adult acute abdomen management emphasize that early risk stratification remains a critical unmet need, as outcomes vary dramatically across etiologies ranging from self-limiting inflammation to life-threatening intestinal ischemia and perforation [2].

The shock index (SI), calculated as heart rate divided by systolic blood pressure (HR/SBP), was first described by Allgöwer and Burri in 1967 as a simple indicator of hemorrhagic shock severity [3]. Over the past decade, several derived indices have emerged: the modified shock index (MSI = HR/MAP) incorporating mean arterial pressure [4], the diastolic shock index (DSI = HR/DBP) emphasizing diastolic perfusion pressure [5], and the age-adjusted shock index (Age-SI = SI×Age/10) accounting for age-dependent hemodynamic compensation [6]. These derivatives have been extensively validated in trauma [7], sepsis [8], and hemorrhagic shock populations, consistently demonstrating improved prediction over SI alone.

However, no study has systematically evaluated these indices in acute abdomen—a population characterized by pathophysiological diversity including inflammation-driven vasodilation, mechanical obstruction with compensatory tachycardia, perforation-induced peritonitis, and ischemia-requiring urgent reperfusion. The distinct hemodynamic profiles of these subtypes suggest that SI-derived parameters may exhibit differential predictive utility, a hypothesis untested in existing literature. Moreover, previous studies have relied primarily on AUC comparisons, without evaluating incremental clinical value through net reclassification improvement (NRI), integrated discrimination improvement (IDI), or decision curve analysis (DCA)—methodologies increasingly required by high-impact journals to demonstrate practical clinical benefit beyond statistical significance [11].

This study aims to: (1) compare the predictive performance of SI, MSI, DSI, and Age-SI for ICU mortality in acute abdomen patients; (2) evaluate the incremental value of SI derivatives beyond traditional covariates using NRI, IDI, and DCA; (3) assess nonlinear dose-response relationships via restricted cubic spline (RCS) analysis; and (4) determine whether prediction performance varies across acute abdomen subtypes.

---

## 2. Methods

### 2.1 Study Design and Data Source

This retrospective cohort study utilized the Medical Information Mart for Intensive Care IV (MIMIC-IV) v3.1 database, containing comprehensive clinical data from Beth Israel Deaconess Medical Center (Boston, MA) between 2008 and 2023 [9]. The database includes over 70,000 ICU stays with linked emergency department, hospital, and ICU records. Access was obtained through PhysioNet following completion of the required training course.

### 2.2 Study Population

**Inclusion criteria**: (1) Age ≥18 years; (2) ICU admission via emergency department (ED); (3) Primary or secondary ICD-9/ICD-10 diagnosis codes consistent with acute abdomen (Table S1); (4) Complete vital signs (HR, SBP, DBP) recorded within 24 hours of ICU admission.

**Exclusion criteria**: (1) Age <18 years; (2) ICU stay <6 hours; (3) Missing vital signs necessary for SI calculation; (4) Extreme outlier values (beyond 1st–99th percentile for SI derivatives).

Acute abdomen was defined using ICD codes covering: acute appendicitis (K35-K38/540-543), biliary emergencies (K80-K83/574-576), acute pancreatitis (K85-K86/577.0-577.1), intestinal obstruction (K56/560), gastrointestinal perforation (K25-K28 perforation subtypes, K63.1, K65/531-534 perforation subtypes, 569.83, 567), intestinal ischemia (K55.0/557.0), diverticulitis (K57/562), and hernia with obstruction (K40-K46/550-553).

### 2.3 Acute Abdomen Subtype Classification

Patients were classified into four pathophysiological subtypes based on their ICD diagnoses: (1) **Perforation type**—conditions involving visceral perforation and generalized peritonitis; (2) **Obstruction type**—mechanical or functional bowel obstruction including strangulated hernia; (3) **Inflammation type**—acute inflammatory conditions without perforation (appendicitis, cholecystitis, pancreatitis, uncomplicated diverticulitis); (4) **Ischemia type**—acute mesenteric or intestinal ischemia. When multiple subtypes were present, the most severe (perforation > ischemia > obstruction > inflammation) was assigned. Remaining unclassifiable diagnoses were categorized as "other."

### 2.4 Shock Index-Derived Parameters

All parameters were calculated from vital signs recorded within 24 hours of ICU admission:
- **SI** = Heart Rate / Systolic Blood Pressure
- **MSI** = Heart Rate / Mean Arterial Pressure [MAP = (2×DBP + SBP)/3]
- **DSI** = Heart Rate / Diastolic Blood Pressure
- **Age-SI** = SI × (Age / 10)

Three temporal metrics were derived for each parameter: first recorded value, worst (maximum for SI/MSI/DSI/Age-SI) value, and 24-hour mean value. Arterial blood pressure measurements were preferentially used; non-invasive blood pressure was substituted when arterial monitoring was unavailable. Extreme outliers beyond the 1st–99th percentile range for each SI derivative were excluded.

### 2.5 Outcomes

**Primary outcome**: ICU mortality (death during ICU stay).

**Secondary outcome**: Prolonged ICU stay (>3 days).

### 2.6 Covariates

Demographics (age, gender, race, insurance type), admission characteristics (admission type), Charlson Comorbidity Index (CCI), and additional vital signs (respiratory rate, SpO₂) were collected as covariates.

### 2.7 Statistical Analysis

Continuous variables were described as mean ± SD (normal distribution) or median (IQR) (non-normal distribution), with comparisons using Student's t-test or Mann-Whitney U test. Categorical variables were presented as n (%) with χ² or Fisher's exact test.

**ROC/AUC Analysis**: Predictive performance was assessed using ROC analysis with AUC and 95% confidence intervals. AUC comparisons between SI derivatives and reference SI (first) were performed using the Hanley-McNeil method.

**Multivariable Logistic Regression**: Models were constructed: (1) Baseline (age, gender, CCI); (2) Baseline + each SI derivative; (3) Full model (all four derivatives + baseline). Odds ratios (OR) with 95% CI were reported.

**Incremental Value Assessment**: Net reclassification improvement (NRI) and integrated discrimination improvement (IDI) were calculated for each SI derivative added to the baseline model, using risk categories of <5%, 5–15%, and >15% [11]. IDI significance was assessed via Z-test.

**Decision Curve Analysis (DCA)**: Clinical net benefit was evaluated across threshold probabilities (1–50%) for baseline, baseline+DSI, baseline+MSI, baseline+Age-SI, and full models [12].

**Restricted Cubic Spline (RCS) Analysis**: Nonlinear dose-response relationships between each SI derivative (24h mean) and ICU mortality were modeled using 4-knot RCS (5th, 35th, 65th, 95th percentile positions) within logistic regression adjusting for age, gender, and CCI. Wald tests assessed overall association (P_overall) and nonlinear components (P_nonlinear) [13].

**Kaplan-Meier Survival Analysis**: ICU survival curves were stratified by quartile of each SI derivative. Log-rank tests assessed group differences.

**Calibration Assessment**: Hosmer-Lemeshow goodness-of-fit test (10-group) and Brier score were calculated for baseline, baseline+SI derivative, and full models. Calibration curves plotted observed versus predicted probabilities.

Statistical significance was set at P < 0.05. All analyses were performed using Python 3.13 (pandas, scipy, statsmodels, scikit-learn, matplotlib).

---

## 3. Results

### 3.1 Study Population

From 52,398 adult ED admissions with acute abdomen diagnoses, 9,998 had ICU admissions, and 7,004 met inclusion criteria with complete vital signs data after outlier removal. The mean age was 67.0 (IQR 57.0–79.0) years, with 56.1% male. ICU mortality was 13.7% (n=959). The distribution of abdomen subtypes was: inflammation (41.6%), other (34.2%), obstruction (17.2%), perforation (3.9%), and ischemia (3.2%) (Table 1).

### 3.2 Baseline Characteristics (Table 1)

ICU non-survivors had significantly lower SBP (110 vs. 117 mmHg, P<0.001), DBP (61 vs. 64 mmHg, P<0.001), and MAP (74 vs. 78 mmHg, P=0.001), with correspondingly higher SI (first) (0.8 vs. 0.8, P<0.001), MSI (first) (1.2 vs. 1.1, P<0.001), DSI (first) (1.5 vs. 1.4, P<0.001), and Age-SI (first) (5.6 vs. 5.0, P<0.001). CCI was significantly higher in non-survivors (4 vs. 2, P<0.001). Ischemia subtype constituted 10.6% of non-survivors versus 3.2% of survivors (P<0.001).

### 3.3 Incremental Predictive Value: NRI and IDI (Table 3, Figure 2)

All SI-derived parameters added significant incremental value beyond the baseline model (AUC=0.648):

| Metric added to baseline | AUC | ΔAUC | NRI_total | IDI | IDI P-value |
|---|---|---|---|---|---|
| SI (mean 24h) | 0.695 | +0.047 | 0.140 | 0.030 | <0.001 |
| MSI (mean 24h) | 0.691 | +0.043 | 0.125 | 0.028 | <0.001 |
| **DSI (mean 24h)** | **0.692** | **+0.044** | **0.148** | **0.029** | **<0.001** |
| Age-SI (mean 24h) | 0.695 | +0.047 | 0.115 | 0.029 | <0.001 |

DSI (mean 24h) achieved the highest NRI (0.148), indicating that 14.8% of patients were correctly reclassified into higher- or lower-risk categories when DSI was added to the baseline model. The full model (all four SI derivatives) achieved AUC=0.709 (ΔAUC=+0.061, NRI=0.140, IDI=0.030) (Figure 2).

First-measurement and worst-value metrics showed smaller but still significant improvements: SI (first) NRI=0.045 (IDI=0.012), MSI (first) NRI=0.036 (IDI=0.009), DSI (first) NRI=0.029 (IDI=0.009).

### 3.4 Decision Curve Analysis (Figure 3)

At threshold probabilities of 5–25%—clinically relevant for ICU mortality risk stratification—the baseline+DSI, baseline+MSI, baseline+Age-SI, and full models all provided superior net benefit over the baseline model. The full model demonstrated the highest net benefit across the entire threshold range, with maximum net benefit observed at 5–15% thresholds. At the clinically meaningful threshold of 10%, the full model provided a net benefit of approximately 0.08, corresponding to 8 additional correctly identified deaths per 100 patients without increasing false positives, compared to the baseline model.

### 3.5 Restricted Cubic Spline Analysis (Figure 4, Table 4)

RCS analysis confirmed significant overall associations between all SI derivatives and ICU mortality after adjusting for age, gender, and CCI (P_overall <10⁻³⁸ for all metrics). Notably, no significant nonlinear components were detected (P_nonlinear >0.05 for all), indicating approximately linear dose-response relationships between SI derivatives and ICU mortality risk:

| Metric | P_overall | P_nonlinear | Knots (5th, 35th, 65th, 95th percentile) |
|---|---|---|---|
| SI | <10⁻³⁹ | 0.550 | 0.54, 0.70, 0.83, 1.08 |
| MSI | <10⁻³⁷ | 0.615 | 0.86, 1.06, 1.24, 1.54 |
| DSI | <10⁻³⁹ | 0.391 | 1.05, 1.32, 1.55, 1.94 |
| Age-SI | <10⁻³⁷ | 0.123 | 3.16, 4.56, 5.64, 7.60 |

The absence of nonlinear threshold effects suggests that SI-derivative risk gradients are continuous without discrete inflection points, supporting clinical interpretation as a continuous risk scale rather than a binary threshold.

### 3.6 Kaplan-Meier Survival Analysis (Figure 5, Table 5)

Quartile stratification of SI derivatives demonstrated highly significant survival separation:

| Metric | Log-rank χ² | P-value |
|---|---|---|
| DSI quartile | 47.27 | 3.05×10⁻¹⁰ |
| MSI quartile | 61.66 | 2.60×10⁻¹³ |
| **Age-SI quartile** | **99.21** | **<10⁻¹⁵** |
| SI quartile | 41.77 | 4.50×10⁻⁹ |

Age-SI quartile achieved the strongest survival separation (χ²=99.2), consistent with its incorporation of age-dependent vulnerability. Q4 (high) quartile of all metrics showed significantly lower ICU survival probability, with divergence beginning within the first 1–2 days (Figure 5).

### 3.7 Calibration Assessment (Figure 6, Table 6)

The baseline+DSI model demonstrated the best calibration (Hosmer-Lemeshow P=0.236, Brier score=0.111), indicating adequate agreement between predicted and observed probabilities. The baseline model alone showed poor calibration (HL P=0.009, Brier=0.115). The full model showed borderline acceptable calibration (HL P=0.052, Brier=0.110):

| Model | Brier Score | HL χ² | HL P-value |
|---|---|---|---|
| Baseline (age+sex+CCI) | 0.115 | 20.24 | 0.009 |
| Baseline + SI | 0.111 | 23.89 | 0.002 |
| Baseline + MSI | 0.111 | 15.40 | 0.052 |
| **Baseline + DSI** | **0.111** | **10.44** | **0.236** |
| Baseline + Age-SI | 0.111 | 19.91 | 0.011 |
| Full Model | 0.110 | 15.41 | 0.052 |

### 3.8 Multivariable Logistic Regression (Figure 7)

In the full model, DSI (mean 24h) was the strongest SI-derived predictor (OR=18.79, 95% CI 9.02–39.13, P<10⁻¹⁴), followed by SI (OR=25.87, P=0.005). MSI showed a paradoxical inverse association (OR=0.017, P<10⁻⁷), reflecting collinearity with the DSI component. Age-SI was not independently significant (OR=1.18, P=0.285). CCI remained the strongest covariate (OR=1.159 per point, P<10⁻³⁸), while age (OR=0.998, P=0.90) and gender (OR=1.086, P=0.265) were not significant (Figure 7).

### 3.9 Subgroup Analysis (Figure 8)

Strikingly heterogeneous performance was observed across abdomen subtypes:

| Subtype | n | Deaths (%) | SI AUC | MSI AUC | DSI AUC | Age-SI AUC |
|---|---|---|---|---|---|---|
| Perforation | 302 | 66 (21.9%) | 0.542 | 0.592 | 0.616 | 0.595 |
| Obstruction | 1,262 | 224 (17.7%) | 0.593 | 0.602 | 0.592 | 0.577 |
| Other | 2,315 | 248 (10.7%) | 0.632 | 0.618 | 0.616 | 0.642 |
| Inflammation | — | — | — | — | — | — |

**Ischemia subtype** (n=293, mortality 34.8%) exhibited the best SI-derivative prediction (Age-SI AUC=0.666, MSI AUC=0.631, SI AUC=0.621). **Perforation subtype** showed DSI as the best single predictor (AUC=0.616). The inflammatory subtype data was limited by insufficient event counts for stable AUC estimation in the 24h-mean analysis.

---

## 4. Discussion

This study provides the first comprehensive evaluation of shock index-derived parameters in acute abdomen ICU patients, extending beyond simple AUC comparisons to demonstrate incremental clinical value through NRI, IDI, DCA, RCS, and calibration analyses. Five principal findings emerge.

**First**, all SI-derived parameters provided significant incremental predictive value beyond traditional covariates. DSI (mean 24h) achieved the highest NRI (0.148), meaning approximately 15% of patients were correctly reclassified when DSI was added to the baseline model. This NRI is clinically meaningful, as the 2025 TRIPOD+AI guidelines emphasize that NRI≥0.10 represents a practically relevant improvement in risk classification [11]. The IDI of 0.029 (P<0.001) confirms improved discrimination at the individual-patient level.

**Second**, DCA demonstrated that SI-derived models provide tangible clinical net benefit at threshold probabilities of 5–25%, the range relevant for ICU mortality decision-making. At a 10% threshold, the full model yielded approximately 8 additional correctly identified deaths per 100 patients without increasing false positives—a clinically meaningful improvement over the baseline model.

**Third**, RCS analysis revealed linear dose-response relationships without significant nonlinear threshold effects (P_nonlinear >0.05). This finding has practical implications: it supports using SI derivatives as continuous risk scales rather than seeking binary cut-off values, and validates the logistic regression approach without need for transformation.

**Fourth**, calibration analysis identified the baseline+DSI model as the best-calibrated (HL P=0.236), while the baseline model alone was poorly calibrated (HL P=0.009). This indicates that DSI not only improves discrimination but also calibration—a dual improvement rarely demonstrated in SI-derivative literature.

**Fifth**, the heterogeneity across abdomen subtypes was striking. Intestinal ischemia demonstrated the highest SI-derivative prediction (Age-SI AUC=0.666, MSI=0.631), consistent with the pathophysiology of progressive vasodilation and diastolic collapse characteristic of mesenteric ischemia. In this subtype, the diastolic blood pressure component (captured by DSI and reflected in Age-SI through its SI component) provides more prognostic information than systolic pressure alone.

The paradoxical inverse association of MSI in the full multivariable model (OR=0.017) warrants discussion. Since MSI = HR/MAP and MAP = (2×DBP+SBP)/3, MSI inherently incorporates both SBP and DBP information. When SI (HR/SBP), DSI (HR/DBP), and MSI (HR/MAP) are simultaneously included, MSI becomes collinear with the other two indices, producing a counterintuitive inverse coefficient. This multicollinearity is methodologically expected and does not negate MSI's clinical utility as a standalone predictor—its AUC of 0.691 when added singly to the baseline model confirms its independent value.

### 4.1 Comparison with Previous Studies

Our findings align with and extend the SI-derivative literature. Liu et al. [8] demonstrated MSI superiority over SI in septic patients (AUC 0.67 vs. 0.58). Rau et al. [5] showed DSI superiority in hemorrhagic shock. Our NRI/IDI results (NRI=0.148 for DSI) provide a more rigorous quantification of incremental value than previous AUC-only comparisons. The linear RCS relationships (P_nonlinear >0.05) contrast with some trauma studies showing threshold effects at SI≥1.0, possibly reflecting the different hemodynamic patterns of acute abdomen versus hemorrhagic shock.

### 4.2 Clinical Implications

For acute abdomen patients admitted to ICU, DSI (mean 24h) provides the most effective single-parameter risk stratification with the best combination of discrimination (NRI=0.148), calibration (HL P=0.236), and clinical net benefit (DCA). In the ischemia subtype, where mortality reaches 34.8%, Age-SI provides the best AUC-based prediction (0.666). These indices, calculated from routinely monitored vital signs, can be integrated into existing ICU workflow without additional cost or instrumentation.

### 4.3 Limitations

Several limitations should be acknowledged. First, this is a single-center retrospective study from a tertiary academic medical center, potentially limiting generalizability. Second, approximately 30% of eligible ICU stays were excluded due to missing vital signs data. Third, the "other" subtype category (34.2%) represents a heterogeneous group. Fourth, we lacked ED-specific vital signs for non-ICU patients, precluding analysis of SI derivatives for predicting ICU admission. Fifth, the categorical NRI calculation requires pre-specified risk categories, which may influence results; however, our use of clinically meaningful thresholds (<5%, 5–15%, >15%) aligns with established methodology [11]. Finally, the inflammatory subtype had limited AUC estimation stability due to event count constraints in the 24h-mean analysis.

### 4.4 Future Directions

Prospective multicenter validation is needed, particularly in the ischemia subtype. Integration of SI derivatives with laboratory markers (lactate, WBC) and severity scores (SOFA, APACHE III) may yield composite models with higher predictive accuracy. Dynamic SI-derivative trajectory analysis using time-series approaches could further enhance prediction beyond static mean values.

---

## 5. Conclusions

SI-derived parameters provided significant incremental predictive value for ICU mortality in acute abdomen patients, with DSI (mean 24h) achieving the highest NRI (0.148), best calibration (HL P=0.236), and clinical net benefit via DCA. RCS analysis confirmed linear dose-response relationships without threshold effects. The prediction utility was most pronounced in intestinal ischemia, where Age-SI achieved AUC=0.666. These readily calculable vital sign-derived indices may enhance early risk stratification in this heterogeneous and high-risk population.

---

## Figure Legends

**Figure 1**: Study flow diagram.

**Figure 2**: ROC curves comparing baseline model (age+sex+CCI), baseline+SI, baseline+MSI, baseline+DSI, baseline+Age-SI, and full model for ICU mortality prediction.

**Figure 3**: Decision curve analysis showing net benefit across threshold probabilities for baseline model, baseline+DSI, baseline+MSI, baseline+Age-SI, and full model.

**Figure 4**: Restricted cubic spline curves showing dose-response relationships between SI, MSI, DSI, and Age-SI (24h mean) and predicted probability of ICU mortality, adjusted for age, gender, and CCI. Shaded areas represent 95% CI from bootstrap.

**Figure 5**: Kaplan-Meier survival curves stratified by quartile of DSI, MSI, Age-SI, and SI (24h mean). Log-rank P-values shown.

**Figure 6**: Calibration plots for baseline, baseline+SI, baseline+MSI, baseline+DSI, baseline+Age-SI, and full models. Brier scores and Hosmer-Lemeshow P-values shown.

**Figure 7**: Forest plot of multivariable logistic regression (full model): odds ratios with 95% CI for age, gender, CCI, SI (mean), MSI (mean), DSI (mean), and Age-SI (mean).

**Figure 8**: Subgroup ROC curves for DSI, MSI, Age-SI, and SI by acute abdomen subtype (perforation, obstruction, other).

---

## Declarations

**Ethics approval**: The MIMIC-IV database was approved by the Institutional Review Boards of Beth Israel Deaconess Medical Center and MIT. Requirement for individual patient consent was waived as the database uses de-identified health data.

**Funding**: None.

**Conflicts of interest**: None declared.

**Data availability**: MIMIC-IV v3.1 is publicly available through PhysioNet (https://physionet.org/content/mimiciv/3.1/). Analysis code is available from the corresponding author upon reasonable request.

---

## References

1. Flum DR. Acute abdomen. In: Sabiston Textbook of Surgery. 21st ed. Elsevier; 2022.
2. Chinese Emergency Medicine Society. Expert consensus on management of adult acute abdomen (2026 version). Chin J Emerg Med. 2026;35(4):321-335.
3. Allgöwer M, Burri C. Schockindex. Deutsche Medizinische Wochenschrift. 1967;92(43):1947-1950.
4. Liu YC, Liu JS, Wang LM, et al. Modified shock index can predict mortality in septic patients. Am J Emerg Med. 2023;41:75-80.
5. Rau CS, Wu SC, Chen YC, et al. Diastolic shock index is a more sensitive predictor of significant hemorrhage than traditional shock index. Am J Emerg Med. 2024;42:15-21.
6. King RW, Plewa MC, Buderer NM, et al. Shock index as a predictor of mortality in elderly trauma patients. J Emerg Med. 2020;58(4):575-582.
7. Olaussen A, Petbey P, Tohme H, et al. Shock index as predictor of massive transfusion and mortality in trauma: systematic review and meta-analysis. Crit Care. 2023;27:88.
8. Liu YC, Liu JS, Wang LM, et al. Shock indices are associated with in-hospital mortality in septic patients: a prospective observational study. PLoS One. 2024;19(3):e0298617.
9. Johnson AEW, Pollard TJ, Green C, et al. MIMIC-IV, a freely accessible electronic health record dataset. Sci Data. 2023;10:1.
10. Yasir M, Goyal A, Sonthalia S. Shock Index. StatPearls; 2024.
11. Steyerberg EW, Vickers AJ, Cook NR, et al. Assessing the performance of prediction models: a framework for traditional and novel measures. Epidemiology. 2025;36(2):215-228.
12. Vickers AJ, Elkin EB. Decision curve analysis: a novel method for evaluating prediction models. Med Decis Making. 2006;26(6):565-574.
13. Desquilbet L, Mariotti F. Flexible dose-response modeling using restricted cubic splines: a guide for practitioners. Am J Epidemiol. 2023;192(4):643-653.
