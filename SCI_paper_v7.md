# Diastolic Shock Index as an Independent Predictor of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation

**Jiqiang Liu** [1]†, **Dengke Wu** [1]*

[1] Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China

† First author.

* Corresponding author: Dengke Wu, Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China. Electronic address: wudk2010@csu.edu.cn

---

## Abstract

**Background**: Shock index (SI) derivatives predict mortality in trauma and sepsis but remain unexplored in acute abdomen. We evaluated SI-derived parameters for predicting in-hospital mortality, assessing diastolic shock index (DSI) as an independent, zero-cost bedside predictor complementary to SOFA.

**Methods**: Retrospective cohort from MIMIC-IV v3.1 (2008–2022). Adult ICU patients with acute abdomen ICD codes were included; SI/MSI/DSI/Age-SI were calculated from 24-hour vital signs. Primary outcome: in-hospital mortality. The primary model excluded surgery (survivorship bias), incorporating age, sex, Charlson Comorbidity Index (CCI), lactate, WBC, vasopressor use, mechanical ventilation, and SOFA. Performance was assessed via AUC/DeLong, NRI/IDI, DCA, RCS, cumulative incidence functions, calibration, and bootstrap validation. Multiple imputation (N=8,933) and 12 sensitivity analyses were performed. External validation used eICU-CRD v2.0 (N=5,755, 208 hospitals).

**Results**: Among 5,728 complete-case ICU stays (median age 68, 56.0% male, in-hospital mortality 19.9%, SOFA 7 [4–11]), DSI was the strongest SI derivative. Extended baseline (no surgery) AUC=0.785; adding DSI yielded AUC=0.790 (ΔAUC=0.005, DeLong P=0.012). DSI was an independent predictor (OR=2.18, 95% CI 1.79–2.65, P=7.59×10⁻¹⁵). ΔAUC was below clinical relevance thresholds (≥0.02), and categorical NRI crossed zero (0.008, 95% CI −0.009 to 0.044). However, category-free NRI (0.252, P<0.001) and IDI (0.013, P<0.001) were significant, and the DSI quartile gradient was dramatic: Q1=12.1%→Q4=32.8% (2.7-fold, P=2.02×10⁻⁴⁹). Of 1,141 hospital deaths, 33.6% occurred after ICU discharge. External validation in eICU-CRD preserved discrimination (AUC=0.792, ΔAUC=0.0074, DeLong P=0.0026) and replicated the quartile gradient (12.0%→33.5%), though calibration required local recalibration (intercept shift −3.935).

**Conclusions**: DSI is an independent predictor of in-hospital mortality after SOFA adjustment, providing zero-cost bedside risk stratification with a dramatic quartile gradient. While ΔAUC is below clinical relevance thresholds and categorical NRI crosses zero, the independent OR, category-free NRI, and quartile gradient support DSI as a complementary, immediately available tool when laboratory data are pending. Prediction was most pronounced in non-surgical acute abdomen (AUC=0.826).

**Keywords**: Diastolic shock index; Acute abdomen; In-hospital mortality; SOFA; External validation

---

## Abbreviations

SI, shock index; MSI, modified shock index; DSI, diastolic shock index; Age-SI, age-adjusted shock index; HR, heart rate; SBP, systolic blood pressure; DBP, diastolic blood pressure; MAP, mean arterial pressure; SOFA, Sequential Organ Failure Assessment; CCI, Charlson Comorbidity Index; ICU, intensive care unit; LOS, length of stay; ROC, receiver operating characteristic; AUC, area under the curve; NRI, net reclassification improvement; IDI, integrated discrimination improvement; cf-NRI, category-free NRI; cat-NRI, categorical NRI; DCA, decision curve analysis; RCS, restricted cubic splines; CIF, cumulative incidence function; HL, Hosmer-Lemeshow; VIF, variance inflation factor; MV, mechanical ventilation; ED, emergency department; ICD, International Classification of Diseases; WBC, white blood cell count; MI, multiple imputation

---

## 1. Introduction

Acute abdomen—severe abdominal pain of sudden onset requiring urgent evaluation—remains one of the most challenging presentations in emergency medicine [1]. Early risk stratification is critical, as outcomes vary dramatically across etiologies [1,2].

The shock index (SI=HR/SBP), first described by Allgöwer and Burri [3], has inspired derivatives: modified shock index (MSI=HR/MAP) [4], diastolic shock index (DSI=HR/DBP) [5], and age-adjusted shock index (Age-SI=SI×Age/10) [6]. These predict mortality in trauma [7] and sepsis [8], but have never been systematically evaluated in acute abdomen—a population with pathophysiological diversity including inflammation-driven vasodilation, mechanical obstruction, perforation-induced peritonitis, and ischemia.

Previous SI-derivative studies relied on AUC comparisons without evaluating independent predictive value beyond established ICU predictors, nor assessing robustness via bootstrap validation, sensitivity analyses, or competing risks. The TRIPOD+AI guidelines [9] emphasize that prediction models must demonstrate clinical benefit via NRI/IDI/DCA [10] and undergo external validation. This study was reported per STROBE [11] and TRIPOD+AI guidelines [9].

We aimed to: (1) compare SI, MSI, DSI, and Age-SI for in-hospital mortality prediction; (2) evaluate DSI as an independent predictor beyond SOFA-adjusted covariates; (3) assess robustness via bootstrap, MI, and 12 sensitivity analyses; (4) externally validate in eICU-CRD; and (5) determine subtype-specific performance.

---

## 2. Methods

### 2.1 Data Sources and Study Design

This retrospective cohort study utilized MIMIC-IV v3.1 [12] (Beth Israel Deaconess Medical Center, Boston, 2008–2022; 546,028 admissions). External validation used eICU-CRD v2.0 [13] (208 US hospitals, 2014–2015). Both accessed via PhysioNet with required training. IRB approval (BIDMC, MIT) was obtained; individual consent waived for de-identified data.

### 2.2 Study Population (Figure 1)

**Inclusion**: age ≥18; ICU admission via ED; acute abdomen ICD-9/10 codes (Supplementary Table S1); complete vital signs (HR, SBP, DBP) within 24h. **Exclusion**: missing extended covariates (lactate, WBC). From 546,028 admissions, 5,728 complete cases (CC) were analyzed. The 3,205 excluded patients had substantially lower severity (mortality 8.0% vs 19.9%, vasopressor 12% vs 43.6%, MV 17% vs 52.5%), reflecting selection bias toward patients receiving arterial blood gas monitoring (Supplementary Table S8). MI (N=8,933) addressed this bias.

Acute abdomen subtypes based on ICD: perforation, ischemia, obstruction, inflammation, and other (29.9%, N=1,712, containing complications alongside primary codes; Supplementary Table S5). Priority: perforation > ischemia > obstruction > inflammation > other.

### 2.3 Variables and Analysis

**SI derivatives** (24h vital signs): SI=HR/SBP, MSI=HR/MAP, DSI=HR/DBP, Age-SI=SI×Age/10. BP priority: arterial > non-invasive > manual. **Primary outcome**: in-hospital mortality (hospital_expire_flag); **secondary**: ICU mortality.

**Primary extended baseline** (without surgery): age, sex, CCI [14], lactate, WBC, vasopressor use, MV, SOFA [15]. Surgery was excluded because "surgery during hospitalization" (67.4%) introduces survivorship bias: only 5.1% had surgery ≤24h from ICU admission, confirming most procedures occurred after surviving the acute crisis (surgery_24h OR=0.88, P=0.46). A model including surgery is reported as an alternative (Supplementary Table S9). A parsimonious model (without vasopressor and MV) is also reported (Supplementary Table S10), since these covariates were non-significant after SOFA adjustment (P=0.14 and 0.45 respectively).

**Statistical methods**: Multivariable logistic regression at three levels (basic, extended, extended+DSI). ROC/AUC with DeLong comparisons [16]. VIF for multicollinearity (all <3.0; maximum SOFA=2.42). NRI: categorical (<10%, 10–30%, >30% risk strata) and category-free [10]; IDI [10]. DCA [17]. RCS (4 knots) [18]. Cumulative incidence functions for competing risks [19]; formal Fine-Gray models were not implemented (CIF curves are descriptive only). Calibration: HL test, Brier score. Bootstrap validation (200 resamples; optimism=0.002). Sensitivity analyses (12 scenarios, Supplementary Table S11). MI: 5 imputations on N=8,933.

### 2.4 External Validation

MIMIC-IV models were applied to eICU-CRD without retraining (TRIPOD type 2b/3b). **Methodological note**: eICU SOFA was computed from APACHE APS variables rather than identical MIMIC-IV concept definitions; platelets were unavailable (hematocrit substituted). This heterogeneity is reflected in higher eICU median SOFA (9 [7–12] vs MIMIC-IV 7 [4–11]). Both un-recalibrated and recalibrated (logistic intercept/slope adjustment) metrics are reported per TRIPOD+AI [9]. Performance: AUC/DeLong, cf-NRI/IDI, DSI quartile gradient (derivation cutoffs applied; eICU quartile sizes unequal: Q1=1,294, Q4=1,677). All analyses: Python 3.13 (pandas, scipy, statsmodels, DuckDB).

---

## 3. Results

### 3.1 Baseline Characteristics (Table 1)

Among 5,728 CC ICU stays: median age 68 [57–79], 56.0% male, in-hospital mortality 19.9% (1,141 deaths; 33.6% after ICU discharge). SOFA 7 [4–11]; significantly higher in non-survivors (11 [8–15] vs 6 [4–10]). Vasopressor use 43.6%; MV 52.5%; lactate 2.0 [1.3–3.2] mmol/L; CCI 3 [1–5]. Subtypes: inflammation (37.5%), other (29.9%), obstruction (20.6%), ischemia (6.2%), perforation (5.8%).

### 3.2 DSI Quartile Mortality Gradient (Table 1)

DSI (mean 24h) quartiles demonstrated a dramatic gradient (χ²=229, P=2.02×10⁻⁴⁹): Q1<1.279 (12.1%), Q2 1.279–1.502 (14.5%), Q3 1.502–1.762 (20.3%), Q4>1.762 (32.8%)—a 2.7-fold increase. Higher quartiles had progressively higher lactate, vasopressor use, and MV rates.

### 3.3 Primary Model Results (Table 2)

**Table 2, Panel A (MIMIC-IV)**: Extended baseline (no surgery) AUC=0.785 [0.769–0.801]; adding DSI: AUC=0.790 [0.775–0.805], ΔAUC=0.005 (DeLong P=0.012). DSI: OR=2.18 [1.79–2.65], P=7.59×10⁻¹⁵; SOFA: OR=1.16 [1.13–1.19], P<10⁻³⁶; lactate: OR=1.14 [1.11–1.17]; CCI: OR=1.14 [1.11–1.16]. Vasopressor (P=0.14), MV (P=0.45), gender (P=0.08), and WBC (P=0.07) were non-significant after SOFA adjustment. ΔAUC=0.005 was below clinical relevance thresholds (≥0.02 per Cook [20] and Vickers [21]); categorical NRI (0.008, CI −0.009 to 0.044) crossed zero. Category-free NRI (0.252, CI 0.183–0.331) and IDI (0.013, CI 0.007–0.020) were significant, confirming additional continuous prognostic information. VIF all <3.0; bootstrap optimism=0.002. Full coefficients: Supplementary Table S6; Forest plot: Figure 3; ROC curves: Figure 2.

**Table 2, Panel B (eICU-CRD)**: N=5,755 (208 hospitals), mortality 20.0%, SOFA 9 [7–12]. Extended baseline AUC=0.785; Extended+DSI AUC=0.792; ΔAUC=0.0074 (DeLong P=0.0026). Un-recalibrated: Brier=0.38–0.59, HL P<0.001 (catastrophically poor). After logistic recalibration (intercept −3.935, slope 0.952): Brier=0.126, HL P=0.266. cf-NRI=0.277, IDI=0.014. DSI quartile gradient: Q1=12.0%→Q4=33.5% (2.8-fold). The large intercept shift indicates discrimination is transportable (slope near 1.0), but absolute risk estimates require local recalibration.

### 3.4 Sensitivity Analyses (Supplementary Table S11)

DSI's independent predictive value was robust across 12 analyses (OR range 2.15–2.65, all P<10⁻¹¹). Key findings: (1) Including surgery increased AUC by only 0.002 (baseline 0.785→0.787); surgery appeared protective (OR=0.68) but likely reflects survivorship bias; surgery_24h (OR=0.88, P=0.46) was non-significant. (2) Excluding "Other" subtype (N=4,016): AUC=0.786–0.788, DSI OR=2.15–2.22. (3) Parsimonious model (without vasopressor/MV): AUC=0.789, DSI OR=2.22, ΔAUC=0.005—confirming redundant covariates do not affect DSI's value. (4) Non-surgical subgroup: AUC=0.826 (best performance). (5) MI (N=8,933): AUC=0.822, DSI OR=2.65, addressing selection bias with higher estimates. (6) RCS: all P_overall<0.001, P_nonlinear>0.05 (Supplementary Figure S3). (7) DCA: modest incremental net benefit (Supplementary Figure S4). (8) Calibration: Extended+DSI HL P=0.691, Brier=0.126 (Supplementary Figure S5). (9) Subtype-specific AUC: inflammation 0.819, obstruction 0.749, perforation 0.766, ischemia 0.807 (Supplementary Figure S6). (10) CIF curves confirmed progressive risk across quartiles (Supplementary Figure S7).

---

## 4. Discussion

This study provides the first comprehensive evaluation of SI-derived parameters in acute abdomen ICU patients, with SOFA adjustment, bootstrap validation, MI, 12 sensitivity analyses, competing risk framework, external validation in 208 hospitals, and STROBE/TRIPOD+AI-compliant reporting.

**First**, DSI is an independent predictor after SOFA adjustment (OR=2.18, P=7.59×10⁻¹⁵). However, ΔAUC=0.005 is below clinical relevance thresholds (≥0.02) [20,21], and categorical NRI crossing zero means DSI does not reclassify patients across the 10%/30% risk strata beyond a model already containing SOFA and lactate. This is expected when a marker refines continuous prediction without shifting categorical thresholds [21]. We position DSI not as a SOFA replacement, but as a **complementary zero-cost bedside tool** providing independent risk information from routinely monitored HR and DBP—available without laboratory turnaround time. DSI's clinical value lies in immediate risk stratification when SOFA components (platelets, bilirubin, PaO₂, vasopressor doses) are pending.

**Second**, the DSI quartile gradient (12.1%→32.8%, 2.7-fold) provides clinically actionable thresholds (Q1<1.279, Q4>1.762). Higher quartiles had progressively higher lactate, vasopressor, and MV rates, confirming DSI as an integrative hemodynamic severity marker.

**Third**, 33.6% of hospital deaths occurred after ICU discharge, justifying in-hospital mortality as the primary endpoint and suggesting DSI could guide post-ICU monitoring intensity.

**Fourth**, surgery was excluded from the primary model due to survivorship bias: 67.4% "during hospitalization" vs 5.1% ≤24h, with surgery_24h non-significant (P=0.46). Including surgery increased baseline AUC by only 0.002, confirming its minimal and biased contribution. This bias affects any model including "surgery during hospitalization" as a covariate—a caution for future ICU prediction studies.

**Fifth**, external validation in eICU-CRD (208 hospitals) preserved discrimination (AUC=0.792, ΔAUC=0.0074) and replicated the quartile gradient (12.0%→33.5%). However, direct application yielded catastrophically poor calibration (Brier 0.38–0.59), requiring logistic recalibration (intercept −3.935, slope 0.952). The near-ideal slope confirms discrimination transportability, but the large intercept shift means MIMIC-IV-derived absolute risk estimates cannot be directly applied to new settings without local recalibration. Additionally, eICU SOFA computation differed from MIMIC-IV (APACHE APS-based, median 9 vs 7; hematocrit substituted for platelets), and eICU data (2014–2015) represents an older practice era.

**Pathophysiological rationale**: DSI captures HR-to-diastolic pressure relationships. In acute abdomen, progressive vasodilation and splanchnic compromise first manifest as diastolic pressure decline—loss of peripheral vascular tone before systolic compensatory mechanisms fail—making DSI more sensitive to early deterioration than SI (HR/SBP) [5].

**Clinical implications**: DSI provides: (1) independent predictive value (OR=2.18); (2) dramatic quartile gradient; (3) zero-cost from routine vitals; (4) validated discrimination across 208 hospitals. It complements but does not replace SOFA-based categorical risk classifications. In ischemia (mortality 40.5%, AUC=0.807) and non-surgical acute abdomen (AUC=0.826), DSI may be particularly useful.

### 4.1 Limitations

(1) Single-center retrospective derivation, though externally validated in 208 hospitals; (2) Selection bias: 36% exclusion (primarily lactate) enriched CC with more severe patients (mortality 19.9% vs 8.0% in excluded); MI (N=8,933) addressed this; eICU validation also used CC (32.6% rate); (3) ΔAUC below clinical thresholds; categorical NRI crossing zero; DSI is positioned as a complementary bedside tool, not a SOFA replacement; (4) Surgery survivorship bias addressed by removal from primary model; (5) "Other" subtype heterogeneity (29.9%); sensitivity excluding it preserved results; (6) No Fine-Gray subdistribution hazard models; CIF curves are descriptive; (7) eICU SOFA heterogeneity (APS-based vs MIMIC-IV concept; median 9 vs 7); hematocrit substituted for platelets; (8) Large recalibration intercept shift (−3.935) means absolute risk predictions require local recalibration; discrimination (slope 0.952) is transportable; (9) eICU data (2014–2015) represents older practice era; (10) WBC borderline (P=0.07); vasopressor and MV non-significant after SOFA adjustment (absorbed by SOFA components); (11) Only two authors; statistical expertise was guided by TRIPOD+AI guidelines and established biostatistical references [9,16,20,21].

### 4.2 Future Directions

Prospective multicenter validation with standardized SOFA; Fine-Gray modeling; DSI trajectory analysis; integration with machine learning; non-US population validation.

---

## 5. Conclusions

DSI is an independent predictor of in-hospital mortality in acute abdomen after SOFA adjustment (OR=2.18, 95% CI 1.79–2.65), providing zero-cost bedside risk stratification with a dramatic quartile gradient (2.7-fold). While ΔAUC=0.005 is below clinical relevance thresholds and categorical NRI crosses zero, the independent OR, category-free NRI, and quartile gradient support DSI as a complementary, immediately available risk-stratification tool when laboratory data are pending. External validation in eICU-CRD (208 hospitals) confirmed discrimination transportability and replicated the quartile gradient, though calibration required local recalibration. Prediction was most pronounced in non-surgical acute abdomen (AUC=0.826).

---

## Supplementary Materials

**Table S1**: ICD-9/10 codes for acute abdomen identification and subtype classification.
**Table S2**: STROBE checklist (completed).
**Table S3**: Baseline characteristics (N=5,728) by DSI quartile.
**Table S4**: TRIPOD+AI checklist (27 items) [9].
**Table S5**: ICD code composition of "Other" subtype (N=1,712).
**Table S6**: Full model coefficients (primary model without surgery + DSI).
**Table S7**: eICU-CRD baseline characteristics (N=5,755) by DSI quartile.
**Table S8**: Excluded (N=3,205) vs CC (N=5,728) patient characteristics.
**Table S9**: Alternative model (with surgery) coefficients and performance.
**Table S10**: Parsimonious model (without vasopressor/MV) performance.
**Table S11**: Sensitivity analyses summary (12 scenarios).
**Figure S1**: Calibration plots for basic baseline models.
**Figure S2**: Kaplan-Meier curves by DSI quartile.
**Figure S3**: RCS dose-response curves for SI, MSI, DSI, Age-SI.
**Figure S4**: DCA net benefit across threshold probabilities.
**Figure S5**: Calibration plots (4 model levels).
**Figure S6**: Subgroup ROC curves by subtype.
**Figure S7**: Cumulative incidence functions by DSI quartile.

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

**CRediT**: Jiqiang Liu: Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Software, Validation, Visualization, Writing – original draft. Dengke Wu: Conceptualization, Funding acquisition, Methodology, Project administration, Resources, Supervision, Writing – review & editing.

**AI use declaration**: During the preparation of this manuscript, the authors used a large language model for language polishing and manuscript editing only. All data extraction, statistical analyses, figure generation, and scientific interpretation were performed independently by the authors. After using the tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.

**Acknowledgments**: We thank the MIMIC-IV and eICU-CRD teams for open access to clinical databases.

**Data availability**: MIMIC-IV v3.1 at https://physionet.org/content/mimiciv/3.1/. eICU-CRD v2.0 at https://physionet.org/content/eicu-crd/2.0/. Analysis code available on request from the corresponding author.

---

## References

1. Flum DR. Acute abdomen. In: Sabiston Textbook of Surgery. 21st ed. Elsevier; 2022.
2. Cervero F, Laird JM. Visceral pain. Lancet. 1999;353(9170):2145-2148.
3. Allgöwer M, Burri C. Schockindex. Deutsche Med Wochenschr. 1967;92(43):1947-1950.
4. Jouffroy R, Gille S, Gilbert B, et al. Shock index derivatives and 28-day mortality in prehospital septic shock. J Emerg Med. 2024;66(2):144-153.
5. Ospina-Tascón GA, Teboul JL, Hernandez G, et al. Diastolic shock index and clinical outcomes in septic shock. Ann Intensive Care. 2020;10:41.
6. Kim SY, Hong KJ, Shin SD, et al. Validation of shock indices for predicting geriatric trauma mortality. J Korean Med Sci. 2016;31(12):2026-2032.
7. Olaussen A, Peterson G, Synnot A, et al. Shock index and mortality in trauma: systematic review. Crit Care. 2023;27:88.
8. Liu YC, Lee CT, Su HY, et al. Shock indices and in-hospital mortality in sepsis. PLoS One. 2024;19(3):e0298617.
9. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement. BMJ. 2024;385:e078378.
10. Pencina MJ, D'Agostino RB, et al. Evaluating added predictive ability. Stat Med. 2008;27(2):157-172.
11. von Elm E, Altman DG, Egger M, et al. STROBE statement. Lancet. 2007;370(9596):1453-1457.
12. Johnson AEW, Bulgarelli L, Pollard TJ, et al. MIMIC-IV. Sci Data. 2023;10:1.
13. Pollard TJ, Johnson AEW, Raffa JD, et al. eICU-CRD. Sci Data. 2018;5:180175.
14. Charlson ME, Pompei P, Ales KL, MacKenzie CR. Comorbidity classification. J Chronic Dis. 1987;40(5):373-383.
15. Vincent JL, Moreno R, Takala J, et al. SOFA score. Intensive Care Med. 1996;22(7):707-710.
16. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing AUCs. Biometrics. 1988;44(3):837-845.
17. Vickers AJ, Elkin EB. Decision curve analysis. Med Decis Making. 2006;26(6):565-574.
18. Desquilbet L, Mariotti F. Dose-response via RCS. Am J Epidemiol. 2010;172(12):1377-1385.
19. Fine JP, Gray RJ. Proportional hazards model for competing risks. J Am Stat Assoc. 1999;94(446):496-509.
20. Cook NR. Use and misuse of the receiver operating characteristic curve in risk prediction. Circulation. 2007;115(7):928-935.
21. Vickers AJ, Cronin AM, Begg CB. One statistical test is sufficient for assessing prediction model performance. Med Decis Making. 2008;28(5):525-529.
