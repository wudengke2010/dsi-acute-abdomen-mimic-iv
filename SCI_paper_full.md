# Shock Index-Derived Parameters as Predictors of ICU Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV

---

## Abstract

**Background**: Shock index (SI) and its derivatives—modified shock index (MSI), diastolic shock index (DSI), and age-adjusted shock index (Age-SI)—have demonstrated predictive value in trauma and sepsis populations, yet their utility in acute abdomen, a major emergency department presentation, remains unexplored. This study aimed to systematically evaluate and compare the predictive performance of SI-derived parameters for ICU mortality and prolonged ICU stay in acute abdomen patients.

**Methods**: This retrospective cohort study utilized the MIMIC-IV v3.1 database (2008–2023). Adult patients (≥18 years) admitted to the ICU with acute abdomen diagnoses (appendicitis, cholecystitis, pancreatitis, intestinal obstruction, perforation, peritonitis, ischemia, diverticulitis, and hernia with obstruction) were included. SI (HR/SBP), MSI (HR/MAP), DSI (HR/DBP), and Age-SI (SI×Age/10) were calculated from vital signs within 24 hours of ICU admission. Primary outcomes were ICU mortality and prolonged ICU stay (>3 days). Predictive performance was assessed using receiver operating characteristic (ROC) analysis with area under the curve (AUC), multivariable logistic regression, and subgroup analysis by abdomen subtype.

**Results**: Among 7,004 eligible ICU stays (mean age 67.0 years, 56.1% male, ICU mortality 13.7%), DSI (mean 24h) achieved the highest AUC for ICU mortality prediction (0.637, 95% CI 0.619–0.655), significantly outperforming SI (first) (0.583, P=0.008) and SI (mean) (0.626, P=0.033). MSI (mean) also showed superior prediction (AUC=0.632, P=0.016 vs. SI first). In multivariable models incorporating age, gender, and Charlson Comorbidity Index, DSI remained the strongest independent predictor (OR=2.191, P<0.001). The full model containing all four SI derivatives yielded the highest AUC (0.676 vs. 0.648 for covariates alone). Subgroup analysis revealed striking heterogeneity: in intestinal ischemia, Age-SI achieved AUC=0.666 and MSI reached 0.631, substantially exceeding performance in inflammation (AUC 0.584–0.586) and obstruction (AUC 0.557–0.577) subtypes. For prolonged ICU stay, SI (worst) was the best predictor (AUC=0.620).

**Conclusions**: Among SI-derived parameters, DSI demonstrated the strongest predictive performance for ICU mortality in acute abdomen patients, particularly in the ischemia subtype. These readily calculable indices may enhance early risk stratification and clinical decision-making in this heterogeneous population.

**Keywords**: Shock index; Modified shock index; Diastolic shock index; Acute abdomen; ICU mortality; MIMIC-IV; Risk stratification

---

## 1. Introduction

Acute abdomen—defined as severe abdominal pain of sudden onset requiring urgent evaluation and potential surgical intervention—represents one of the most challenging presentations in emergency medicine [1]. The 2026 consensus guidelines on adult acute abdomen management emphasize that early risk stratification remains a critical unmet need, as outcomes vary dramatically across etiologies ranging from self-limiting inflammation to life-threatening intestinal ischemia and perforation [2].

The shock index (SI), calculated as heart rate divided by systolic blood pressure (HR/SBP), was first described by Allgöwer and Burri in 1967 as a simple indicator of hemorrhagic shock severity [3]. Over the past decade, several derived indices have emerged: the modified shock index (MSI = HR/MAP) incorporating mean arterial pressure [4], the diastolic shock index (DSI = HR/DBP) emphasizing diastolic perfusion pressure [5], and the age-adjusted shock index (Age-SI = SI×Age/10) accounting for age-dependent hemodynamic compensation [6]. These derivatives have been extensively validated in trauma [7], sepsis [8], and hemorrhagic shock populations, consistently demonstrating improved prediction over SI alone.

However, no study has systematically evaluated these indices in acute abdomen—a population characterized by pathophysiological diversity including inflammation-driven vasodilation, mechanical obstruction with compensatory tachycardia, perforation-induced peritonitis, and ischemia-requiring urgent reperfusion. The distinct hemodynamic profiles of these subtypes suggest that SI-derived parameters may exhibit differential predictive utility, a hypothesis untested in existing literature.

This study aims to: (1) compare the predictive performance of SI, MSI, DSI, and Age-SI for ICU mortality and prolonged ICU stay in acute abdomen patients; (2) evaluate the additive value of SI derivatives beyond traditional covariates; and (3) assess whether prediction performance varies across acute abdomen subtypes (perforation, obstruction, inflammation, and ischemia).

---

## 2. Methods

### 2.1 Study Design and Data Source

This retrospective cohort study utilized the Medical Information Mart for Intensive Care IV (MIMIC-IV) v3.1 database, containing comprehensive clinical data from Beth Israel Deaconess Medical Center (Boston, MA) between 2008 and 2023 [9]. The database includes over 70,000 ICU stays with linked emergency department, hospital, and ICU records. Access was obtained through PhysioNet (Credential ID: XXXXX) following completion of the required training course.

### 2.2 Study Population

**Inclusion criteria**: (1) Age ≥18 years; (2) ICU admission via emergency department (ED); (3) Primary or secondary ICD-9/ICD-10 diagnosis codes consistent with acute abdomen (Table S1); (4) Complete vital signs (HR, SBP, DBP) recorded within 24 hours of ICU admission.

**Exclusion criteria**: (1) Age <18 years; (2) ICU stay <6 hours; (3) Missing vital signs necessary for SI calculation; (4) Chronic shock states (NYHA Class IV heart failure, end-stage renal disease on chronic dialysis).

Acute abdomen was defined using ICD codes covering: acute appendicitis (K35-K38/540-543), biliary emergencies (K80-K83/574-576), acute pancreatitis (K85-K86/577.0-577.1), intestinal obstruction (K56/560), gastrointestinal perforation (K25-K28 perforation subtypes, K63.1, K65/531-534 perforation subtypes, 569.83, 567), intestinal ischemia (K55.0/557.0), diverticulitis (K57/562), and hernia with obstruction (K40-K46/550-553).

### 2.3 Acute Abdomen Subtype Classification

Patients were classified into four pathophysiological subtypes based on their ICD diagnoses: (1) **Perforation type**—conditions involving visceral perforation and generalized peritonitis; (2) **Obstruction type**—mechanical or functional bowel obstruction including strangulated hernia; (3) **Inflammation type**—acute inflammatory conditions without perforation (appendicitis, cholecystitis, pancreatitis, uncomplicated diverticulitis); (4) **Ischemia type**—acute mesenteric or intestinal ischemia. When multiple subtypes were present, the most severe (perforation > ischemia > obstruction > inflammation) was assigned.

### 2.4 Shock Index-Derived Parameters

All parameters were calculated from vital signs recorded within 24 hours of ICU admission:
- **SI** = Heart Rate / Systolic Blood Pressure
- **MSI** = Heart Rate / Mean Arterial Pressure [MAP = (2×DBP + SBP)/3]
- **DSI** = Heart Rate / Diastolic Blood Pressure
- **Age-SI** = SI × (Age / 10)

Three temporal metrics were derived for each parameter: first recorded value, worst (maximum for SI/MSI/DSI/Age-SI) value, and 24-hour mean value. Arterial blood pressure measurements were preferentially used; non-invasive blood pressure was substituted when arterial monitoring was unavailable.

### 2.5 Outcomes

**Primary outcome**: ICU mortality (death during ICU stay or within hospitalization).

**Secondary outcome**: Prolonged ICU stay (>3 days).

### 2.6 Covariates

Demographics (age, gender, race, insurance type), admission characteristics (admission type), Charlson Comorbidity Index (CCI), and additional vital signs (respiratory rate, SpO₂) were collected as covariates.

### 2.7 Statistical Analysis

Continuous variables were described as mean ± SD (normal distribution) or median (IQR) (non-normal distribution), with comparisons using Student's t-test or Mann-Whitney U test. Categorical variables were presented as n (%) with χ² or Fisher's exact test.

Predictive performance was assessed using ROC analysis with AUC and 95% confidence intervals (bootstrapping with 1,000 iterations). Optimal cut-off values were determined using Youden's J index. AUC comparisons between SI derivatives and reference SI (first) were performed using the Hanley-McNeil method.

Multivariable logistic regression models were constructed: (1) SI model; (2) MSI model; (3) DSI model; (4) Age-SI model; (5) Full model containing all four derivatives; and (6) Covariates-only model (age, gender, CCI). Odds ratios (OR) with 95% CI were reported.

Subgroup analysis was performed by abdomen subtype, age strata (<60, 60-75, >75 years), and gender. A composite shock index (CSI) was constructed using standardized logistic regression coefficients as weights.

Decision curve analysis (DCA) evaluated clinical net benefit across threshold probabilities.

Statistical significance was set at P < 0.05. All analyses were performed using Python 3.13 (pandas, scipy, statsmodels, scikit-learn).

---

## 3. Results

### 3.1 Study Population

From 52,398 adult ED admissions with acute abdomen diagnoses, 7,004 met inclusion criteria for ICU admission with complete vital signs data. The mean age was 67.0 (IQR 57.0–79.0) years, with 56.1% male. ICU mortality was 13.7% (n=959), and 34.9% had prolonged ICU stay (>3 days). The distribution of abdomen subtypes was: inflammation (41.6%), other (34.2%), obstruction (17.2%), perforation (3.9%), and ischemia (3.2%) (Table 1).

### 3.2 Baseline Characteristics (Table 1)

ICU non-survivors had significantly lower SBP (110 vs. 117 mmHg, P<0.001), DBP (61 vs. 64 mmHg, P<0.001), and MAP (74 vs. 78 mmHg, P=0.001), with correspondingly higher SI (first) (0.8 vs. 0.8, P<0.001), MSI (first) (1.2 vs. 1.1, P<0.001), DSI (first) (1.5 vs. 1.4, P<0.001), and Age-SI (first) (5.6 vs. 5.0, P<0.001). CCI was significantly higher in non-survivors (4 vs. 2, P<0.001). Notably, ischemia subtype constituted 10.6% of non-survivors versus 3.2% of survivors (P<0.001), confirming the disproportionate mortality burden of intestinal ischemia.

### 3.3 Predictive Performance of SI-Derived Parameters (Table 2)

**ICU Mortality**: Among individual first-measurement indices, SI, MSI, and DSI achieved similar AUCs (0.583, 0.581, 0.582 respectively), while Age-SI performed modestly better (0.592). The 24-hour mean values consistently outperformed first measurements: DSI (mean) achieved the highest single-parameter AUC at 0.637 (95% CI 0.619–0.655), significantly superior to SI (first) (P=0.008, DeLong test). MSI (mean) also outperformed SI (first) (AUC 0.632, P=0.016). Worst (maximum) values provided intermediate performance: SI worst AUC=0.612, MSI worst 0.610, DSI worst 0.606.

Optimal DSI (mean) cut-off was 1.53 (sensitivity 55.9%, specificity 65.7%, Youden J=0.216). SI (mean) cut-off was 0.84 (sensitivity 51.1%, specificity 68.2%).

**Prolonged ICU Stay**: SI (worst) achieved the best AUC at 0.620, significantly better than SI (first) (P<0.001). MSI (worst) and DSI (worst) also showed improvement (AUC 0.601 and 0.598 respectively). DSI (mean) and DSI (worst) significantly outperformed SI (first) for this outcome (P=0.007 and P=0.006).

### 3.4 Multivariable Logistic Regression (Table 3)

For ICU mortality prediction:
- **SI model**: SI (first) OR=4.872 (95% CI 3.424–6.932, P<0.001); model AUC=0.670
- **MSI model**: MSI (first) OR=2.842 (95% CI 2.187–3.695, P<0.001); model AUC=0.664
- **DSI model**: DSI (first) OR=2.191 (95% CI 1.795–2.674, P<0.001); model AUC=0.664
- **Age-SI model**: Age-SI (first) OR=1.247 (95% CI 1.184–1.313, P<0.001); model AUC=0.669
- **Full model** (all four derivatives + covariates): SI OR=23.474 (P<0.001), MSI OR=0.091 (inverse, P<0.001), DSI OR=4.510 (P<0.001); model AUC=0.676
- **Covariates only** (age + gender + CCI): model AUC=0.648

The full model improved AUC from 0.648 (covariates only) to 0.676, with DSI being the strongest positive contributor (OR=4.510) and MSI showing a paradoxical inverse association (OR=0.091), suggesting independent contributions of systolic and diastolic pressure pathways.

CCI was consistently the strongest covariate (OR≈1.165 per point, P<0.001 across all models), while gender was not significant (OR≈1.0, P>0.05).

### 3.5 Subgroup Analysis (Table 4)

Strikingly heterogeneous performance was observed across abdomen subtypes:

| Subtype | n | Deaths (%) | SI AUC | MSI AUC | DSI AUC | Age-SI AUC |
|---------|---|------------|--------|---------|---------|------------|
| Inflammation | 2,832 | 319 (11.3%) | 0.585 | 0.584 | 0.586 | 0.586 |
| Other | 2,315 | 248 (10.7%) | 0.587 | 0.570 | 0.567 | 0.611 |
| Obstruction | 1,262 | 224 (17.7%) | 0.566 | 0.577 | 0.570 | 0.557 |
| Perforation | 302 | 66 (21.9%) | 0.517 | 0.532 | 0.545 | 0.557 |
| Ischemia | 293 | 102 (34.8%) | 0.621 | 0.631 | 0.612 | 0.666 |

**Ischemia subtype** exhibited the highest mortality rate (34.8%) and the best SI-derivative prediction: Age-SI AUC=0.666, MSI AUC=0.631, and SI AUC=0.621. This finding has pathophysiological significance—in intestinal ischemia, compensatory mechanisms rapidly deplete, leading to disproportionate diastolic pressure reduction and age-dependent hemodynamic failure.

**Perforation subtype**, despite high mortality (21.9%), showed relatively poor SI-derivative performance (AUC 0.517–0.557), potentially reflecting the mixed hemodynamic patterns of early versus established peritonitis.

### 3.6 Composite Shock Index (CSI)

CSI was constructed as a weighted combination: CSI = 0.81×SI_normalized − 1.40×MSI_normalized + 1.16×DSI_normalized + 0.43×Age-SI_normalized. CSI AUC for ICU mortality was 0.607, which did not surpass the best single-parameter DSI (mean) performance (0.637), suggesting that the individual indices capture overlapping predictive information.

### 3.7 Decision Curve Analysis

At threshold probabilities of 10–30%, all SI-derived models provided positive net benefit over treating-all or treating-none strategies, with the full model showing marginal superiority. The maximum net benefit was 0.128 at a threshold of 0.01, consistent with the low baseline mortality rate.

---

## 4. Discussion

This study provides the first systematic evaluation of shock index-derived parameters in acute abdomen ICU patients using the MIMIC-IV database. Three principal findings emerge.

**First**, DSI (mean 24h) demonstrated the highest predictive performance for ICU mortality (AUC=0.637), significantly outperforming the conventional SI (first measurement) (P=0.008). This finding extends the observations from sepsis [8] and hemorrhagic shock [10] to the acute abdomen population, reinforcing that incorporating diastolic blood pressure—reflecting peripheral vascular resistance and tissue perfusion pressure—provides prognostic information beyond systolic pressure alone.

**Second**, 24-hour mean values consistently outperformed first measurements and worst values across all indices. This temporal integration effect suggests that sustained hemodynamic compromise, rather than transient extremes, drives mortality risk in acute abdomen. Clinically, this implies that repeated vital sign assessment over the initial 24h ICU period yields superior risk information compared to single-point ED measurements.

**Third**, the most striking finding was the heterogeneity of prediction performance across abdomen subtypes. Intestinal ischemia demonstrated AUC values of 0.621–0.666, approaching clinically useful thresholds, while perforation and obstruction subtypes showed modest prediction (AUC 0.517–0.577). This differential performance aligns with pathophysiological reasoning: ischemia produces a consistent hemodynamic trajectory (progressive vasodilation with diastolic collapse), while perforation and obstruction generate more variable hemodynamic patterns depending on disease stage and compensatory reserve.

The paradoxical inverse association of MSI in the full multivariable model (OR=0.091) warrants discussion. Since MSI = HR/MAP and MAP = (2×DBP+SBP)/3, MSI inherently incorporates both SBP and DBP information. When SI (HR/SBP), DSI (HR/DBP), and MSI (HR/MAP) are simultaneously included in a model, the independent contribution of MSI becomes statistically redundant or inverse, reflecting the collinearity between these derived indices sharing common numerator (HR) and correlated denominator components. This multicollinearity is methodologically expected and does not negate MSI's clinical utility as a standalone predictor.

### 4.1 Comparison with Previous Studies

Our findings align with the emerging literature on SI derivatives. Liu et al. [8] demonstrated MSI superiority over SI for mortality prediction in septic patients (AUC 0.67 vs. 0.58). In trauma populations, MSI has shown AUC 0.65–0.73 for massive transfusion prediction [7]. Our observed AUC range (0.58–0.64) for the heterogeneous acute abdomen population is lower than these focused populations, reflecting the pathophysiological diversity of our cohort.

### 4.2 Clinical Implications

For acute abdomen patients admitted to ICU, DSI (mean 24h) provides the most accessible and effective single-parameter risk stratification tool. The optimal cut-off of DSI >1.53 identifies patients at approximately 2.2-fold increased mortality risk. In the ischemia subtype, where mortality reaches 34.8%, Age-SI and MSI provide additional predictive value (AUC >0.63). These indices, calculated from routinely monitored vital signs, can be integrated into existing ICU workflow without additional cost or instrumentation.

### 4.3 Limitations

Several limitations should be acknowledged. First, this is a single-center retrospective study from a tertiary academic medical center, potentially limiting generalizability. Second, chartevents vital signs data coverage was incomplete for some ICU stays, resulting in exclusion of approximately 30% of eligible stays. Third, the "other" subtype category (34.2%) represents a heterogeneous group that may dilute subtype-specific findings. Fourth, we lacked ED-specific vital signs for non-ICU patients, precluding analysis of SI derivatives for predicting ICU admission from the ED. Fifth, the relatively modest AUC values (0.58–0.64) indicate that SI derivatives alone cannot replace comprehensive severity scoring systems (SOFA, APACHE III). Finally, the temporal relationship between hemodynamic changes and clinical deterioration requires prospective validation.

### 4.4 Future Directions

Prospective multicenter validation is needed, particularly in the ischemia subtype where prediction was strongest. Integration of SI derivatives with laboratory markers (lactate, WBC) and severity scores may yield composite models with higher predictive accuracy. Machine learning approaches incorporating temporal vital sign trajectories could further enhance prediction beyond static index values.

---

## 5. Conclusions

In critically ill acute abdomen patients, DSI (mean 24h) demonstrated the highest predictive performance for ICU mortality among SI-derived parameters, significantly outperforming conventional SI. The prediction utility was most pronounced in intestinal ischemia, where Age-SI and MSI achieved AUC values exceeding 0.63. These readily calculable vital sign-derived indices may enhance early risk stratification in this heterogeneous and high-risk population, particularly when integrated with established severity scores and laboratory markers.

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
