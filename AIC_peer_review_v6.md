# Annals of Intensive Care — Peer Review Report

**Manuscript**: Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV

**Authors**: Jiqiang Liu, Dengke Wu

**Date**: 2026-07-20

**Reviewer**: Simulated AIC Reviewer (Critical Care / Hemodynamic Monitoring specialist)

---

## Overall Assessment

This manuscript presents a comprehensive evaluation of shock index-derived parameters (SI, MSI, DSI, Age-SI) for predicting in-hospital mortality in acute abdomen ICU patients, with derivation from MIMIC-IV and external validation in eICU-CRD. The study addresses a clinically relevant question, employs a multi-layered statistical framework, and includes both internal (bootstrap) and external (eICU) validation. However, several critical methodological concerns substantially limit the strength of the conclusions, particularly regarding the claimed incremental value of DSI beyond SOFA.

**Recommendation**: Major Revision

**Confidence**: High (90%)

---

## Major Concerns (8 items, must be addressed)

### P0-1: ΔAUC=0.005 — Statistically Significant but Clinically Negligible

The core claim of this paper is that DSI provides "incremental value" beyond an extended baseline already containing SOFA. However:

- **ΔAUC=0.005** (0.787→0.792) in the derivation cohort and **ΔAUC=0.0074** in eICU are statistically significant (DeLong P=0.012 and 0.0026) but fall well below the widely accepted threshold for clinical relevance (ΔAUC≥0.02–0.03 per Cook 2007, BMJ 335:641; Vickers 2008, Med Decis Making 28:525).
- The **categorical NRI=0.008 (CI: −0.009 to 0.044) crosses zero**, meaning DSI does not meaningfully reclassify patients across clinically relevant risk thresholds (10%/30%). This is the most clinically interpretable reclassification metric, and it fails.
- The authors pivot to **category-free NRI (0.252) and IDI (0.013)** as evidence of "additional prognostic information." However, cf-NRI lacks established clinical interpretation thresholds — a cf-NRI of 0.252 could represent noise-level improvements in individual risk predictions that never cross decision thresholds. IDI=0.013 translates to a 1.3% improvement in average sensitivity minus average specificity, which is trivially small.
- The Discussion section's assertion that "DSI provides additional continuous prognostic information" is technically correct but clinically misleading. A marker that improves continuous risk prediction without shifting clinical decisions is of questionable utility.
- **Recommended action**: (a) Acknowledge upfront that ΔAUC is below clinical relevance thresholds; (b) Remove or substantially soften language claiming "incremental value" in the Abstract and Conclusions; (c) Reframe the contribution as DSI being an *independent* predictor (OR=2.27) that provides *zero-cost bedside risk stratification* complementary to SOFA, rather than claiming it *adds* predictive value to an already comprehensive model; (d) Cite Cook 2007 and Vickers 2008 on ΔAUC clinical relevance thresholds.

### P0-2: Selection Bias from Complete-Case Analysis — Double Selection Effect

The 36% exclusion rate (8,933→5,728, primarily lactate non-availability at 64.6% coverage) introduces **selection bias toward more severely ill patients** (vasopressor use 43.6% vs 32.3%, MV 52.5% vs 39.9%, mortality 19.9% vs 15.7%). This bias has two critical implications:

1. **Derivation model bias**: The model is trained on a cohort enriched for severity, where both DSI and SOFA are more extreme. This inflates apparent ORs and AUCs relative to the full population.
2. **External validation compounding**: eICU also required complete lactate/WBC (CC rate 32.6%, 17,576→5,755), creating the same selection bias. "Validation" of a severity-enriched model in another severity-enriched cohort does not demonstrate generalizability to the full acute abdomen ICU population.

While multiple imputation (MI) on N=8,933 yielded AUC=0.822 and DSI OR=2.65, the authors note these are "higher estimates suggesting complete-case analysis was conservative." This interpretation is problematic: MI estimates being higher likely reflects the same selection bias amplified by imputation from a severity-enriched CC distribution, not that CC analysis is "conservative."

**Recommended action**: (a) Report baseline characteristics of the excluded 3,205 patients alongside the CC cohort (Table 1 or supplementary), enabling readers to assess bias magnitude; (b) Present MI results as the primary analysis (not "sensitivity"), given that MI addresses the selection bias that CC cannot; (c) Discuss the double-selection-bias concern in the eICU validation; (d) If possible, perform MI on eICU full dataset (N=17,576) to assess whether CC validation is also biased.

### P0-3: SOFA Computation Heterogeneity Between MIMIC-IV and eICU

The paper states that eICU SOFA was "computed from APACHE APS variables" rather than the identical MIMIC-IV concept definition. The eICU median SOFA (9 [7-12]) is notably higher than MIMIC-IV (7 [4-11]), a 2-point median difference. This discrepancy likely reflects:

- **Methodological heterogeneity**: APACHE APS-based SOFA computation is not identical to MIMIC-IV concept-based SOFA (different GCS mapping, different PaO₂/FiO₂ estimation, different creatinine windows).
- **Missing components**: eICU SOFA lacked platelets (replaced by hematocrit) and bilirubin (from APS). These substitutions change component scores.
- This undermines the claim in §2.8 that the validation used "identical methodology" and "the same component-based approach."

The 2-point SOFA difference directly affects model performance because SOFA (OR=1.163/point) is the dominant predictor. A systematic 2-point shift alters baseline predictions substantially, which explains the very large recalibration intercept shift (−3.935).

**Recommended action**: (a) Remove the claim of "identical methodology" — explicitly acknowledge methodological differences; (b) Report eICU SOFA component-level distributions (respiration, coagulation, liver, cardiovascular, CNS, renal) alongside MIMIC-IV components to enable comparison; (c) Discuss whether the SOFA heterogeneity limits the interpretation of "external validation" — is this truly validating the same model, or testing a model with a systematically different SOFA input?

### P0-4: Surgery Covariate — Fundamental Survivorship Bias Not Adequately Addressed

The surgery covariate ("any abdominal surgical procedure during the hospitalization") is defined at 67.4% prevalence. The paper acknowledges temporal bias and performs a sensitivity analysis redefining surgery as ≤24h from ICU admission (5.1% prevalence). However:

- **The 67.4% vs 5.1% discrepancy** reveals that the vast majority of "surgical" patients had procedures well after ICU admission, often after surviving the acute crisis. This confirms survivorship bias: patients who survive long enough to undergo surgery are inherently selected.
- The protective OR=0.68 for surgery is therefore almost entirely an artifact of survivorship, not a true protective effect.
- Including a survivorship-biased variable in the extended baseline model inflates its apparent performance (AUC 0.787) because the model learns "surgery = survival," which is reverse causation.
- The sensitivity analysis (surgery ≤24h, AUC=0.790) uses only 5.1% surgical prevalence, which is unrealistic for acute abdomen and may not adequately capture the confounding.

**Recommended action**: (a) Remove surgery from the extended baseline model entirely, as it represents reverse causation; (b) Re-compute AUC/NRI/IDI without surgery and report whether DSI's incremental value changes; (c) Alternatively, define surgery strictly as "procedure within 48h of ICU admission" (a clinically meaningful window for emergency surgery) and use this as the primary definition; (d) If surgery is retained, add a dedicated paragraph in Limitations explaining survivorship bias and its quantitative impact.

### P0-5: "Other" Subtype Contamination — ICD Code Selection Too Broad

The "Other" subtype (29.9%, n=1,712) contains conditions that are not primary acute abdomen diagnoses. Table S5 reveals the top ICD-10 codes include:
- D62 (Acute posthemorrhagic anemia, n=495) — a complication, not a primary acute abdomen diagnosis
- N179 (AKI unspecified, n=410) — a complication of critical illness
- E872 (Acidosis, n=376) — a metabolic complication
- R6521 (Severe sepsis with septic shock, n=277) — a systemic syndrome
- A419 (Sepsis unspecified, n=245) — not acute abdomen

These represent **secondary diagnoses and complications** rather than acute abdomen etiologies. Including them inflates the cohort with patients whose primary admission reason may have been sepsis, hemorrhage, or renal failure, with an incidental acute abdomen code. This dilutes the pathophysiological rationale for SI-derivative utility in *acute abdomen* specifically.

**Recommended action**: (a) Restrict the cohort to patients whose *primary* ICD diagnosis (first-listed) is an acute abdomen code, not secondary/complication codes; (b) Report how many patients would be excluded by this restriction; (c) If the full cohort is retained, add an explicit limitation that 29.9% "Other" patients may not have acute abdomen as their primary pathology; (d) Provide a sensitivity analysis excluding the "Other" subtype.

### P0-6: Recalibration Magnitude — Large Intercept Shift Questions "Validation" Claim

The logistic recalibration intercept shift is −3.935 for the extended+DSI model (slope=0.952). An intercept shift of this magnitude means the MIMIC-IV model predicts baseline risks that are fundamentally different from eICU. While recalibration is expected per TRIPOD, this specific magnitude raises concerns:

- The raw (un-recalibrated) Brier scores were 0.383–0.588 (HL P<0.001), indicating catastrophically poor calibration. Only after recalibration did Brier reach 0.126 and HL P=0.266.
- This means the MIMIC-IV model cannot be directly applied to any new setting without recalibration — it does not provide portable absolute risk estimates.
- The recalibration slope (0.952) is close to 1.0, which is reassuring for discrimination transportability, but the intercept shift means clinicians in a new hospital would need to recalibrate the model using local data before it provides useful absolute risk predictions.

The paper's Discussion states "adequate recalibrated calibration" — this phrasing obscures the fact that *without* recalibration, the model fails completely in a new setting.

**Recommended action**: (a) Report un-recalibrated performance explicitly in Table 8 alongside recalibrated metrics; (b) Add a sentence: "The large recalibration intercept shift (−3.935) indicates that while model discrimination is transportable, absolute risk predictions require local recalibration before clinical deployment"; (c) Discuss this limitation under the eICU validation findings, not buried in Methods; (d) Consider whether the title's claim of "external validation" should be tempered to "external validation with recalibration."

### P0-7: Figure-File Numbering Mismatch — Submission Risk

The paper text references figures as:
- Figure 1 (Flowchart), Figure 2 (ROC), Figure 3 (DCA), Figure 4 (RCS), Figure 5 (Calibration), Figure 6 (Forest), Figure 7 (Subgroup ROC), Figure 8 (CIF), Figure 9 (ROC extended)

But the actual files in the `figures/` directory are named:
- Fig5_KM, Fig6_Calibration, Fig7_Forest, Fig8_Subgroup_ROC, Fig9_CIF, Fig10_ROC_extended

This is a **+1 offset mismatch** from Fig5 onward, plus Fig5_KM is actually KM curves (now moved to Supplementary Fig S2 in the paper). At submission, Elsevier Editorial Manager requires figure numbers to match the manuscript text. Uploading Fig6_Calibration.pdf as "Figure 6" when the paper calls it "Figure 5" will cause editorial confusion.

**Recommended action**: Rename all figure files to match paper numbering: Fig1_Flowchart, Fig2_ROC, Fig3_DCA, Fig4_RCS, Fig5_Calibration, Fig6_Forest, Fig7_Subgroup_ROC, Fig8_CIF, Fig9_ROC_extended. Remove Fig5_KM from the main figures directory (it is now Fig S2).

### P0-8: TRIPOD+AI Checklist Outdated — Inconsistency with Updated Paper

Table S4 (TRIPOD+AI checklist) contains two entries that contradict the updated paper:
- **Item 11**: States "no external validation" — but the paper now includes eICU external validation (§3.12, Table 8). This must be updated to "External validation in eICU-CRD (N=5,755, 208 hospitals)".
- **Item 21**: States "no external validation" in limitations — but Limitations §4.4(1) now reads "though externally validated in the multi-center eICU-CRD."

These inconsistencies undermine TRIPOD+AI compliance claims.

**Recommended action**: Update Table S4 items 11 and 21 to reflect the eICU external validation. Also verify all other TRIPOD items against the current paper text.

---

## Minor Concerns (11 items, recommended improvements)

### P1-1: Only Two Authors — Expertise Concern

A study of this complexity (MIMIC-IV data extraction, eICU validation, competing risk analysis, RCS, bootstrap validation, NRI/IDI, DCA) typically requires a multidisciplinary team. Having only two authors (one emergency physician, one corresponding author) may raise concerns about:
- Statistical expertise: No identified biostatistician co-author
- Intensivist perspective: No ICU specialist co-author despite studying ICU patients
- Data science expertise: Complex DuckDB/MIMIC-IV data pipeline

While not a reason for rejection, AIC reviewers may question whether all analyses were performed with appropriate expertise. The CRediT statement (JL: "Software, Formal analysis") suggests one author did all computational work.

**Suggested**: Consider inviting a biostatistician or intensivist as co-author, or at minimum, add an explicit Acknowledgments section crediting statistical consultation.

### P1-2: Reference 22 — Conference Abstract Not Peer-Reviewed

Reference [22] (Mirani HG, "Diastolic shock index as an early failure-to-normalize marker...") is cited as a "Conference abstract" presented at "Infectious Diseases Congress 2026, Birmingham, UK." Conference abstracts are not peer-reviewed and may not be citable per AIC editorial policy. Additionally, this references a 2026 conference — the manuscript was submitted in 2026, raising questions about the abstract's availability.

**Suggested**: Remove or replace with a peer-reviewed source. If retained, verify the abstract is publicly accessible and provide a DOI or URL.

### P1-3: WBC P=0.050 — Borderline Significance

WBC (OR=1.006, 95% CI 1.000–1.012, P=0.050) is borderline significant at the conventional 0.05 threshold. The 95% CI lower bound is exactly 1.000, suggesting WBC may not be a reliable predictor. Including borderline predictors in the extended baseline may inflate model complexity without meaningful contribution.

**Suggested**: Discuss whether WBC should be retained, and report the model performance without WBC as a sensitivity analysis.

### P1-4: Vasopressor/MV/Gender Non-Significant in Final Model

Three extended baseline covariates are non-significant in the final model: vasopressor use (P=0.169), mechanical ventilation (P=0.272), gender (P=0.066). While SOFA absorbs much of their predictive information (SOFA's cardiovascular component includes vasopressor doses; respiratory component includes MV), their inclusion as separate binary variables alongside SOFA creates redundancy without independent contribution. This supports the VIF finding (SOFA VIF=2.42) but raises the question of whether a parsimonious model without these three variables would perform similarly.

**Suggested**: Report a parsimonious model (Extended minus vasopressor, MV, gender) alongside the full model, and assess whether DSI's incremental value changes in the parsimonious version.

### P1-5: eICU Temporal Gap (2014-2015 vs 2008-2022)

MIMIC-IV covers 2008–2022 (14 years), while eICU-CRD covers only 2014–2015 (2 years). The 10+ year temporal gap means:
- ICU practices evolved significantly between 2014 and 2022 (e.g., vasopressor choices, ventilation strategies, sepsis bundles)
- eICU represents an older practice era, potentially limiting the relevance of validation results to current ICU practice
- The paper does not discuss this temporal mismatch

**Suggested**: Add a Discussion sentence acknowledging the temporal gap and its implications for contemporary applicability.

### P1-6: No Formal Fine-Gray Subdistribution Hazard Model

The paper states (§4.4, limitation 4): "Although cumulative incidence functions account for the competing risk of discharge, a formal Fine-Gray subdistribution hazard model was not fitted." CIF curves are descriptive; they do not provide hazard ratios or quantitative effect estimates under competing risks. For a study that emphasizes competing risk methodology, this gap is notable.

**Suggested**: Either implement Fine-Gray models for DSI quartiles (available in Python via `lifelines` or R via `cmprsk`), or prominently acknowledge that the competing risk analysis is limited to descriptive CIF curves without regression modeling.

### P1-7: Abstract Length — Exceeds Typical AIC Limit

The Abstract is approximately 400 words (Background+Methods+Results+External validation+Conclusions). AIC typically limits abstracts to 250–300 words for Research Articles. The added "External validation" paragraph pushes it well beyond this.

**Suggested**: Condense the Abstract to ≤300 words. Consider merging the external validation results into the Results paragraph rather than adding a separate section.

### P1-8: Title Does Not Reflect eICU Validation

The title reads "A Retrospective Cohort Study from MIMIC-IV" but the paper now includes eICU external validation as a major component (§3.12, Table 8, 8th Discussion finding). The title should reflect this.

**Suggested**: Consider: "Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation" or similar.

### P1-9: DSI Quartile N Unequal in eICU

In MIMIC-IV, quartile sizes are equal (1,432 each), but in eICU they are unequal: Q1=1,294, Q2=1,289, Q3=1,495, Q4=1,677. This occurs because the derivation cohort quartile cutoffs were applied to a different DSI distribution. Q4 has 383 more patients than Q1, which amplifies the apparent mortality gradient (more high-risk patients concentrated in Q4). The Q1→Q4 fold difference is stated as 2.8-fold (12.0%→33.5%), but this comparison is between unequal groups.

**Suggested**: Report eICU DSI distribution statistics (median, IQR) alongside MIMIC-IV, and note that unequal quartile sizes in the validation cohort may amplify the gradient comparison.

### P1-10: STROBE Item 15a — "ICU death 13.7%" vs Paper "13.2%"

Table S2 (STROBE checklist) Item 15a states "ICU death 13.7%" but the paper (§3.1, Table S3) reports "ICU mortality 13.2% (758/5,728)". This inconsistency suggests the STROBE checklist was not updated to match the final paper.

**Suggested**: Update Table S2 Item 15a to match the paper (13.2%).

### P1-11: Supplementary Materials Incomplete for eICU

The submission checklist mentions "Table S1-S6" and "Fig S1-S2" in supplementary materials, but the paper now has Table S7 (eICU baseline by DSI quartile). Supplementary_Materials_AIC.docx may not include Table S7.

**Suggested**: Verify Supplementary_Materials_AIC.docx includes Table S7 and any eICU-specific figures.

---

## Strengths

1. **Comprehensive methodological framework**: Bootstrap validation, MI, RCS, CIF, NRI/IDI, DCA — this is one of the most thorough SI-derivative evaluations in the literature.
2. **External validation**: eICU-CRD (208 hospitals) is a genuine strength, and the discrimination transportability (AUC=0.792 preserved) is remarkable.
3. **DSI quartile mortality gradient**: 12.1%→32.8% (2.7-fold) is dramatic and clinically intuitive, closely replicated in eICU (12.0%→33.5%).
4. **DSI OR=2.27 after SOFA adjustment**: This is a robust independent association, even if ΔAUC is small.
5. **Post-ICU deaths highlight**: 33.6% of hospital deaths occurring after ICU discharge is an important clinical observation that justifies in-hospital mortality as the primary endpoint.
6. **TRIPOD+AI compliance**: Full model coefficients reported (Table S6), enabling external validation.
7. **Pathophysiological rationale**: The Discussion provides a plausible mechanistic explanation for DSI's superiority (diastolic perfusion pressure sensitivity in early hemodynamic deterioration).
8. **STROBE compliance**: Checklist provided (Table S2).

---

## Summary Table

| # | Severity | Issue | Key Impact | Recommended Action |
|---|---|---|---|---|
| P0-1 | **Critical** | ΔAUC=0.005 clinically negligible; cat-NRI crosses zero | Core claim of "incremental value" overstated | Reframe as independent predictor; acknowledge ΔAUC below relevance threshold; cite Cook/Vickers |
| P0-2 | **Critical** | Double selection bias (CC in derivation + CC in validation) | Model built on severity-enriched cohort; validation in equally biased cohort | Report excluded patient characteristics; present MI as primary; discuss double bias |
| P0-3 | **Major** | SOFA computation heterogeneity (MIMIC-IV vs eICU) | "Identical methodology" claim false; SOFA 2-point shift affects model fundamentally | Remove "identical methodology" claim; report component-level SOFA; discuss heterogeneity |
| P0-4 | **Major** | Surgery survivorship bias (67.4% prevalence, OR=0.68) | Reverse causation inflates extended baseline AUC | Remove surgery or redefine as ≤48h; re-compute without surgery |
| P0-5 | **Major** | "Other" subtype contaminated with complications | 29.9% may not have acute abdomen as primary diagnosis | Restrict to primary ICD; sensitivity excluding "Other" |
| P0-6 | **Major** | Recalibration intercept −3.935 (raw Brier 0.38–0.59) | Model not portable without local recalibration | Report un-recalibrated in Table 8; discuss recalibration necessity |
| P0-7 | **Major** | Figure-file numbering mismatch | Submission confusion; editorial rejection risk | Rename files to match paper numbering |
| P0-8 | **Major** | TRIPOD+AI checklist outdated (items 11, 21) | Compliance claim undermined | Update Table S4 items 11, 21 |
| P1-1 | Minor | Only 2 authors | Expertise concern | Add biostatistician/intensivist |
| P1-2 | Minor | Ref 22 conference abstract | Not peer-reviewed | Remove or replace |
| P1-3 | Minor | WBC P=0.050 borderline | Unreliable predictor | Sensitivity without WBC |
| P1-4 | Minor | Vasopressor/MV/gender non-significant | Redundant with SOFA | Parsimonious model sensitivity |
| P1-5 | Minor | eICU temporal gap (2014-2015) | Practice evolution | Discuss in Limitations |
| P1-6 | Minor | No Fine-Gray model | CIF only descriptive | Implement or acknowledge |
| P1-7 | Minor | Abstract >300 words | Exceeds AIC limit | Condense to ≤300 |
| P1-8 | Minor | Title doesn't reflect eICU validation | Misleading | Update title |
| P1-9 | Minor | eICU quartile N unequal | Gradient comparison unequal groups | Report DSI distribution |
| P1-10 | Minor | STROBE 15a: 13.7% vs 13.2% | Checklist outdated | Update Table S2 |
| P1-11 | Minor | Supp materials may lack Table S7 | Incomplete submission | Verify and update |

---

## Decision

**Major Revision** — The study addresses an important clinical question with a strong methodological framework, but the core conclusion (DSI provides "incremental value beyond SOFA") is overstated relative to the evidence (ΔAUC=0.005, categorical NRI crossing zero, recalibration-dependent validation). The selection bias and surgery survivorship bias further limit confidence. The external validation in eICU is a genuine strength, but methodological heterogeneity (SOFA computation, recalibration magnitude) must be transparently disclosed.

If the authors can: (1) reframe the contribution around DSI's independent predictive value (OR=2.27) and zero-cost bedside utility rather than "incremental AUC"; (2) address the selection and survivorship biases; (3) fix the technical inconsistencies (figure numbering, TRIPOD checklist, STROBE checklist); and (4) transparently disclose the limitations of the eICU validation (SOFA heterogeneity, recalibration necessity) — the manuscript would meet AIC publication standards.

---

## Questions for Authors

1. What is the AUC of the extended baseline model *without surgery*? Does DSI's incremental value change when this reverse-causation variable is removed?
2. What are the baseline characteristics of the 3,205 excluded patients (missing lactate/WBC)? How different are they from the CC cohort?
3. Can the authors report eICU SOFA component-level scores to enable comparison with MIMIC-IV SOFA components?
4. What would the ΔAUC be if surgery is removed from the extended baseline? This is critical for assessing whether the "incremental" claim is robust.
5. Have the authors considered presenting MI (N=8,933) as the primary analysis rather than CC (N=5,728), given the selection bias?
6. Why was surgery defined as "during hospitalization" rather than "within 24-48h of ICU admission" in the primary model? The sensitivity analysis shows this definition is problematic.
7. How many patients in the "Other" subtype had acute abdomen as their *primary* (first-listed) ICD diagnosis vs. a secondary diagnosis?

---

*End of Review Report*
