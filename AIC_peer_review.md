# Annals of Intensive Care — Peer Review Report

**Manuscript**: Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV

**Review date**: 2026-07-12

**Overall recommendation**: **Major Revision**

**Confidence level**: High (reviewer verified all key statistics against the original dataset)

---

## Editor's Note

This manuscript evaluates four shock index (SI) derivatives (SI, MSI, DSI, Age-SI) for predicting in-hospital mortality in 5,728 acute abdomen ICU patients from MIMIC-IV. The topic is timely—DSI is an emerging marker (Ospina-Tascón et al., 2020, published in this journal [ref 5])—and the study is one of the first to evaluate SI derivatives specifically in acute abdomen. The statistical apparatus is extensive (ROC, NRI, IDI, DCA, RCS, CIF, bootstrap validation, 10-scenario sensitivity analysis). However, several critical issues must be addressed before the manuscript meets the standards of *Annals of Intensive Care*.

**Important context**: As of January 1, 2026, *Annals of Intensive Care* transitioned from Springer Nature to Elsevier. New submissions should be directed to https://www.editorialmanager.com/aicoj/. The Editor-in-Chief, Prof. Jean-Louis Teboul, is a co-author of the original DSI paper (Ospina-Tascón et al., 2020, ref 5). This creates both an opportunity (the editorial team is familiar with DSI) and a risk (they will hold DSI research to high standards). A conflict-of-interest declaration from the editorial team should be expected during processing.

---

## 1. Major Concerns (must resolve before resubmission)

### 1.1 Missing ICU severity scores (SOFA / APACHE II / SAPS II)

**This is the single most critical issue.** The extended baseline model includes lactate, WBC, vasopressor use, surgery, and mechanical ventilation—but does **not** include SOFA, APACHE II, SAPS II, or any standardized ICU severity score. For a journal whose core audience is intensivists, this is a fundamental gap.

- MIMIC-IV provides SOFA (hourly rolling), APSIII, SAPS II, and OASIS through the `mimic-code` concept tables (`concepts/score/sofa.sql`, `apsiii.sql`, `sapsii.sql`, `oasis.sql`).
- The extended baseline AUC (0.765) may be substantially lower than what could be achieved with SOFA or APACHE II included, which would further erode the marginal ΔAUC of 0.008 attributed to DSI.
- Without severity scores as covariates, the "incremental value of DSI beyond established ICU predictors" claim is overstated—lactate and vasopressor use are individual components, not composite severity scores.

**Action required**: Extract SOFA (24h) and/or APACHE II from MIMIC-IV concept tables, add them to the extended baseline model, and recompute all AUC/NRI/IDI/DCA analyses. If DSI still provides incremental value beyond SOFA-adjusted models, the finding would be substantially strengthened. If it does not, this should be reported transparently.

### 1.2 Temporal bias in the surgery covariate

The Methods define surgery as "any abdominal surgical procedure **during the hospitalization**." This means surgery could have occurred:
- After the 24h vital sign measurement window
- After the patient was already dying or deceased
- As a consequence of the acute abdomen that also caused death

The data confirm this bias: surgery group mortality = 19.5% vs. no-surgery = 20.9%, making surgery appear "protective" (OR=0.70). However, this likely reflects **survivorship bias**—sicker patients die before reaching the operating room, while those who survive to surgery are inherently more stable.

**Action required**: Redefine surgery as "surgery within 24h of ICU admission" or "surgery before outcome determination." Alternatively, use a time-varying covariate approach or landmark analysis. At minimum, acknowledge this temporal bias in the Discussion and report sensitivity analyses with and without surgery as a covariate.

### 1.3 ΔAUC = 0.008 with no external validation

The AUC improvement from adding DSI to the extended baseline is 0.008 (0.765→0.773). While the paper now acknowledges this is "modest," several concerns remain:

- **No external validation**: All results are from a single-center database (BIDMC) with only bootstrap internal validation (optimism ≤0.003). External validation in eICU-CRD or another MIMIC edition would substantially strengthen the claim.
- **NRI 95% CI barely excludes zero**: Reviewer-verified bootstrap 95% CI for categorical NRI = (0.012, 0.076). The lower bound is very close to zero, indicating marginal reclassification improvement.
- **DCA net benefit difference = 0.002**: At 10% threshold, the incremental net benefit of adding DSI is 0.002 (0.128 vs. 0.126). This is clinically negligible and would be invisible on a DCA curve.

**Action required**: (a) Report 95% CIs for NRI and IDI (currently absent). (b) Strongly consider adding external validation (eICU-CRD is the most accessible option). (c) Reframe the conclusion to emphasize the DSI quartile mortality gradient (12.1%→32.8%) and non-surgical subgroup AUC (0.804) as the primary findings, rather than the ΔAUC.

### 1.4 DSI quartile cutoff values not reported

The paper reports DSI quartile mortality gradients but never states the actual DSI values defining each quartile. Reviewer-verified cutoffs (CC N=5,728):

| Quartile | DSI range | N | In-hospital mortality |
|---|---|---|---|
| Q1 | < 1.279 | 1,432 | 12.1% |
| Q2 | 1.279–1.502 | 1,432 | 14.5% |
| Q3 | 1.502–1.762 | 1,432 | 20.3% |
| Q4 | > 1.762 | 1,432 | 32.8% |

**Action required**: Add these cutoff values to Table 1 and the Results text. Without them, clinicians cannot apply the risk stratification tool—the paper's primary practical contribution.

### 1.5 Complete-case analysis with 36% exclusion and no imputation sensitivity

- 3,205 of 8,933 patients (36%) were excluded, primarily for missing lactate (n=3,160).
- The paper correctly acknowledges selection bias (CC patients: vasopressor 43.6% vs. 32.3%, MV 52.5% vs. 39.9%, mortality 19.9% vs. 15.7%).
- However, no multiple imputation sensitivity analysis was performed.
- The Supplementary note justifying complete-case analysis is reasonable but insufficient for a journal that expects TRIPOD+AI compliance.

**Action required**: Perform a multiple imputation sensitivity analysis (at least 20 imputations, MICE/iterative imputation) and report whether the key findings (DSI OR, AUC, NRI) remain consistent. Even if imputation introduces its own assumptions, the comparison would demonstrate robustness.

### 1.6 KM analysis retained despite acknowledged methodological flaws

The paper states: "Because in-hospital mortality is a binary endpoint and discharge alive introduces informative censoring, these curves serve as a visual supplement." However, including a methodologically flawed analysis—even with a caveat—confuses readers and wastes figure space. The CIF analysis (Figure 9) already provides the correct competing-risk assessment.

**Action required**: Move KM curves (Figure 5) to Supplementary material or remove entirely. Replace with an additional figure of higher value (e.g., nomogram, calibration belt, or subgroup forest plot).

### 1.7 No TRIPOD+AI checklist provided

The paper cites TRIPOD+AI [ref 19] but does not include a completed TRIPOD+AI checklist as supplementary material. *Annals of Intensive Care* follows EQUATOR reporting guidelines and may require the checklist at submission. Key TRIPOD+AI items likely missing:

- **Item 10a**: Sample size justification (not provided)
- **Item 13**: Handling of missing data (present but incomplete—no imputation)
- **Item 15b**: Model specification (full regression coefficients not reported)
- **Item 16a**: Model performance with CIs (NRI/IDI lack CIs)
- **Item 22**: Model availability (no web calculator or code repository linked)

**Action required**: Complete the TRIPOD+AI checklist (27 items) and upload as Supplementary Table S4. Report full model coefficients (intercept + all β coefficients) to allow external validation. Consider depositing analysis code in a public repository (GitHub/Zenodo).

---

## 2. Moderate Concerns (should address)

### 2.1 AUC inconsistency in Section 3.4

Section 3.4 text states: "ischemia (AUC=0.780) and inflammation (AUC=0.794)." Table 3 and Section 3.11 report ischemia AUC=0.789 and inflammation AUC=0.795. Reviewer verification confirms **0.789** for ischemia (not 0.780). The text contains a typo.

**Action**: Correct "0.780" → "0.789" and "0.794" → "0.795" in Section 3.4.

### 2.2 NRI and IDI reported without 95% confidence intervals

The paper reports:
- Categorical NRI = 0.046 (no CI)
- Category-free NRI = 0.283 (no CI)
- IDI = 0.017, P = 4.88×10⁻¹³ (no CI)

Reviewer-verified bootstrap 95% CIs (500 resamples):
- Categorical NRI: **0.050 (95% CI: 0.012–0.076)**
- IDI: **0.017 (95% CI: 0.010–0.025)**

The NRI lower bound (0.012) is very close to zero, which should be explicitly discussed.

**Action**: Add 95% CIs for all NRI and IDI values in Tables 2 and 3. Discuss the marginal lower bound.

### 2.3 "Other" subtype (29.9%) is large and undescribed

The "other" subtype constitutes 29.9% of the cohort (N=1,712) but its composition is never described. Which ICD codes fall into "other"? Are these patients with nonspecific abdominal pain, post-operative complications, or mixed etiologies?

**Action**: Add a Supplementary Table listing the ICD codes and frequencies within the "other" category. Discuss whether the 29.9% proportion limits the subtype-specific conclusions.

### 2.4 Non-surgical subgroup AUC=0.804 may reflect confounding

The non-surgical subgroup (N=1,865) shows the best AUC (0.804). The paper interprets this as "DSI is particularly useful before surgical intervention." However, an alternative explanation is that the non-surgical group is enriched with patients too sick for surgery (survivorship bias), creating a more separable outcome distribution. The mortality rate (20.9%) is similar to the overall rate (19.9%), but the case mix may differ.

**Action**: Report baseline characteristics of the surgical vs. non-surgical subgroups (age, CCI, lactate, vasopressor use, subtype distribution). Discuss the survivorship bias alternative interpretation.

### 2.5 Mechanical ventilation extraction may be inaccurate

The MV indicator is derived from 4 chartevents itemids (220339, 224688, 224689, 224690). The MIMIC-IV GitHub provides a more comprehensive MV extraction algorithm (`concepts/measurement/ventilation.sql`) that includes additional itemids and handles invasive vs. non-invasive ventilation separately. The current extraction may miss ~10-15% of ventilated patients.

**Action**: Use the official MIMIC-IV ventilation concept or validate the 4-itemid approach against it. Report the sensitivity/specificity of the simplified approach if retained.

### 2.6 BP source priority may introduce confounding

The Methods state "arterial BP preferred over NIBP." Arterial line placement is itself a marker of illness severity—patients with arterial lines are typically more hemodynamically unstable. This means DSI values derived from arterial BP may be systematically different from those derived from NIBP, and the preference for arterial BP may enrich the cohort with sicker patients.

**Action**: Report the proportion of patients with arterial vs. NIBP measurements. Perform a sensitivity analysis stratified by BP source. Discuss this as a potential confounder.

### 2.7 No calibration belt / GiViTI test

The paper reports Hosmer-Lemeshow test and Brier score but not a calibration belt plot (GiViTI calibration test). Calibration belts are increasingly expected in high-impact ICU prediction model papers and provide a visual assessment of calibration across prediction ranges.

**Action**: Add a calibration belt plot (using the `calibbell` R package or Python equivalent) to complement the existing calibration plot.

### 2.8 First careunit distribution includes non-relevant ICUs

The CC cohort includes patients from:
- CCU (N=311, 5.4%)
- CVICU (N=305, 5.3%)
- Neuro SICU (N=60)
- Neuro Intermediate (N=42)

These ICU types may not be primarily managing acute abdomen. Their inclusion may dilute the specificity of the cohort.

**Action**: Report sensitivity analysis restricted to MICU/SICU/TSICU patients (excluding CCU, CVICU, Neuro). Discuss whether the inclusion of cardiac/neuro ICUs is appropriate for an acute abdomen cohort.

---

## 3. Minor Concerns (language, formatting, presentation)

### 3.1 Title

Current: "Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV"

The title implies all four SI derivatives are equally important, but the paper predominantly focuses on DSI. Consider: "Diastolic Shock Index for In-Hospital Mortality Prediction in Acute Abdomen ICU Patients: A MIMIC-IV Retrospective Cohort Study"

### 3.2 Abstract structure

- Abstract states "AUC range 0.73–0.80" but actual range is 0.736–0.804. Use precise values.
- Abstract does not report NRI/IDI 95% CIs.
- Abstract should mention the DSI quartile cutoff values for clinical utility.
- Keywords: "Cumulative incidence function" and "Sensitivity analysis" are methods, not subject keywords. Replace with "Risk stratification" and "Diastolic blood pressure."

### 3.3 Reference management

- Reference [5] (Ospina-Tascón et al., 2020) was published in *Annals of Intensive Care*—this should be highlighted in the cover letter to demonstrate topical fit.
- Reference [2] (Cervero & Laird, 1999, visceral pain) is tangential to the Introduction's point about etiological diversity. Consider replacing with a clinical review of acute abdomen outcomes.
- The paper cites 19 references, which is adequate but on the lower end for AIC. Consider adding references to recent DSI literature (Mardin et al. 2025 preprint; DSI review in Clin Crit Care 2025).

### 3.4 Figure recommendations

- **Figure 5 (KM)**: Remove or move to Supplementary (see Major Concern 1.6).
- **Figure 6 (Calibration)**: Add calibration belt overlay.
- **Figure 7 (Forest plot)**: Good. Consider adding a nomogram figure for clinical application.
- **Figure 8 (Subgroup ROC)**: Consider adding sample size and mortality rate as annotations in each panel.
- **Figure 10**: Consider replacing with a clinical impact curve or nomogram.

### 3.5 Table formatting

- Table 1 should be a proper baseline characteristics table (overall + by DSI quartile), not the current mixed mortality/covariate format. Table S3 appears to serve this purpose but should be in the main text for AIC.
- All tables should report 95% CIs for AUCs, ORs, NRI, and IDI.
- Add a row for DSI quartile cutoff values in Table 1.

### 3.6 Data availability

The paper states "Code available on request from the corresponding author." AIC (Elsevier) encourages open data and code. Consider depositing analysis code on GitHub/Zenodo with a DOI link. MIMIC-IV data is already publicly available (PhysioNet).

### 3.7 Funding and declarations

- The funding wording is now polished. Verify that the grant numbers are correct at submission.
- Add a "Role of the funder" statement: "The funders had no role in study design, data collection, analysis, interpretation, or manuscript writing."
- Consider adding a CRediT (Contributor Roles Taxonomy) statement, which Elsevier journals prefer.

### 3.8 Statistical reporting conventions

- "P<10⁻³⁸" and "P=2.02×10⁻⁴⁹" should be reported as "P<0.001" per convention, unless the exact value is clinically meaningful.
- "χ² P=2.02×10⁻⁴⁹" for the DSI quartile gradient should use Cochran-Armitage trend test, not plain χ², since the quartiles are ordered.
- Report all P-values to 3 decimal places or use scientific notation consistently.

---

## 4. Reviewer-Verified Data Summary

The following key statistics were independently verified against the original dataset (`analysis_dataset_corrected.csv`, CC N=5,728):

| Metric | Paper value | Reviewer-verified | Match? |
|---|---|---|---|
| CC sample size | 5,728 | 5,728 | ✅ |
| In-hospital mortality | 19.9% (1,141) | 19.9% (1,141) | ✅ |
| Extended baseline AUC | 0.765 | 0.7647 | ✅ |
| Extended+DSI AUC | 0.773 | 0.7731 | ✅ |
| ΔAUC | 0.008 | 0.0084 | ✅ |
| DSI OR | 2.53 (2.08–3.07) | 2.523 (2.078–3.064) | ✅ |
| DSI P-value | <10⁻¹³ | 9.25×10⁻²¹ | ✅ (conservative) |
| Category-free NRI | 0.283 | 0.2831 | ✅ |
| Categorical NRI (10%/30%) | 0.046 | 0.0496 | ⚠️ Slight difference |
| NRI 95% CI | Not reported | (0.012, 0.076) | ❌ Missing |
| IDI | 0.017 | 0.0165 | ✅ |
| IDI 95% CI | Not reported | (0.010, 0.025) | ❌ Missing |
| IDI P-value | 4.88×10⁻¹³ | — | Not independently verified |
| DSI Q1 cutoff | Not reported | 1.279 | ❌ Missing |
| DSI Q2 cutoff | Not reported | 1.502 | ❌ Missing |
| DSI Q3 cutoff | Not reported | 1.762 | ❌ Missing |
| Ischemia AUC (text) | 0.780 | 0.789 | ❌ Typo |
| Ischemia AUC (table) | 0.789 | 0.789 | ✅ |
| SOFA/APACHE in dataset | Not used | Available in MIMIC-IV | ❌ Critical gap |
| Surgery timing | "During hospitalization" | Temporal bias confirmed | ❌ Methodological flaw |

---

## 5. Strengths of the Manuscript

To balance the critique, the following strengths should be acknowledged:

1. **Novel population**: First systematic evaluation of SI derivatives in acute abdomen ICU patients—a genuine knowledge gap.
2. **Large sample**: 5,728 CC patients is substantially larger than comparable DSI studies (Mardin 2025: 598; sepsis comparison: 135).
3. **Comprehensive statistical framework**: ROC + NRI + IDI + DCA + RCS + CIF + bootstrap + 10-scenario sensitivity is thorough.
4. **Honest reporting**: The paper now transparently acknowledges the modest ΔAUC, selection bias, and lack of Fine-Gray modeling.
5. **Clinical relevance**: DSI is a zero-cost, bedside-calculable metric from routine vitals—no additional equipment or laboratory tests needed.
6. **Post-ICU death insight**: The finding that 33.6% of hospital deaths occur after ICU discharge is clinically important and underreported in the literature.
7. **Non-surgical subgroup**: AUC=0.804 is a clinically meaningful finding that suggests DSI's greatest utility may be in pre-decision risk stratification.
8. **STROBE compliance**: Reported following STROBE guidelines with a completed checklist.

---

## 6. Prioritized Action Items

### Must do before submission (P0 — critical for acceptance)

| # | Action | Effort | Impact |
|---|---|---|---|
| 1 | Extract SOFA/APACHE II from MIMIC-IV; add to extended baseline; recompute all analyses | High | 🔴 Critical |
| 2 | Redefine surgery timing (≤24h or before outcome); rerun models | Medium | 🔴 Critical |
| 3 | Report DSI quartile cutoff values (1.279, 1.502, 1.762) | Low | 🔴 Critical |
| 4 | Add 95% CIs for NRI and IDI | Low | 🔴 Critical |
| 5 | Fix ischemia AUC typo (0.780→0.789) in Section 3.4 | Trivial | 🔴 Critical |
| 6 | Complete TRIPOD+AI checklist; upload as supplementary | Medium | 🔴 Critical |
| 7 | External validation (eICU-CRD) — strongly recommended | High | 🟡 Strongly recommended |

### Should do before submission (P1 — important for quality)

| # | Action | Effort | Impact |
|---|---|---|---|
| 8 | Multiple imputation sensitivity analysis | Medium | 🟡 Important |
| 9 | Move KM curves to Supplementary; replace with nomogram | Low | 🟡 Important |
| 10 | Describe "other" subtype composition | Low | 🟡 Important |
| 11 | Add calibration belt plot | Low | 🟡 Important |
| 12 | Report surgical vs. non-surgical baseline characteristics | Low | 🟡 Important |
| 13 | Validate MV extraction against official MIMIC-IV algorithm | Medium | 🟡 Important |
| 14 | Sensitivity analysis: MICU/SICU only (exclude CCU/CVICU/Neuro) | Low | 🟡 Important |
| 15 | Report BP source (arterial vs. NIBP) distribution; sensitivity analysis | Low | 🟡 Important |

### Nice to have (P2 — polish)

| # | Action | Effort | Impact |
|---|---|---|---|
| 16 | Refine title to focus on DSI | Trivial | 🟢 Polish |
| 17 | Update keywords (remove methods terms) | Trivial | 🟢 Polish |
| 18 | Add CRediT statement | Trivial | 🟢 Polish |
| 19 | Deposit code on GitHub/Zenodo | Low | 🟢 Polish |
| 20 | Add "Role of funder" statement | Trivial | 🟢 Polish |
| 21 | Use Cochran-Armitage trend test for ordered quartiles | Low | 🟢 Polish |
| 22 | Add recent DSI literature references (2025) | Low | 🟢 Polish |

---

## 7. Final Recommendation

**Major Revision.**

The study addresses a relevant clinical question with a large sample and comprehensive methodology. However, the absence of ICU severity scores (SOFA/APACHE II) as covariates is a fundamental methodological gap that will be immediately flagged by AIC reviewers and editors. The temporal bias in the surgery covariate further undermines the multivariable model. The ΔAUC of 0.008, while honestly reported, requires stronger support (external validation, NRI with CIs) to justify publication in a top-tier intensive care journal.

**Estimated revision timeline**: 2–4 weeks for P0 items (SOFA extraction + surgery redefinition + NRI CIs + TRIPOD checklist) if data extraction is straightforward. External validation (eICU-CRD) would add 2–3 weeks but would substantially improve acceptance probability.

**Submission logistics**: Submit to https://www.editorialmanager.com/aicoj/ (Elsevier system, effective Jan 2026). Include cover letter highlighting that ref [5] (Ospina-Tascón et al. 2020) was published in AIC, demonstrating topical alignment. Expect a fast initial decision (AIC median: 7 days to first decision).

**Cover letter strategy**: Emphasize (1) first evaluation of SI derivatives in acute abdomen; (2) 5,728-patient sample, 10× larger than any prior DSI study; (3) DSI as a zero-cost bedside tool; (4) the post-ICU death finding (33.6%); (5) non-surgical subgroup AUC=0.804. Do NOT emphasize ΔAUC=0.008 as a primary finding.

---

*Review prepared for: Jiqiang Liu (First Author) and Dengke Wu (Corresponding Author), Department of Emergency Medicine, The Second Xiangya Hospital of Central South University.*
