# Annals of Intensive Care — Peer Review Report (v5 Revised)

**Manuscript**: Shock Index-Derived Parameters as Predictors of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV

**Review date**: 2026-07-12 (second review, v5 revised)

**Overall recommendation**: **Minor Revision**

**Confidence level**: High (reviewer independently verified key statistics against revised dataset)

---

## Editor's Note

This is the second review of this manuscript. The authors have made substantial revisions in response to the initial review, most notably adding SOFA scores to the extended baseline model (the single most critical deficiency in v4), performing multiple imputation, providing TRIPOD+AI and supplementary tables, and adding bootstrap confidence intervals for NRI/IDI. These changes have materially improved the manuscript.

However, the inclusion of SOFA has revealed an important finding: the categorical NRI confidence interval now includes zero (−0.009 to 0.044), meaning DSI does not significantly improve risk reclassification at clinically meaningful thresholds (10%/30%) beyond a SOFA-enhanced model. The authors honestly report this, which is commendable. The category-free NRI and IDI remain significant, and DSI's adjusted OR (2.27, P=4.53×10⁻¹⁶) is highly significant, but the clinical utility argument has been weakened. This, combined with several formatting/reference issues that must be resolved, supports a recommendation of Minor Revision.

**Context reminder**: AIC Editor-in-Chief Prof. Jean-Louis Teboul is a co-author of the original DSI paper (ref 5, Ospina-Tascón et al. 2020, published in this journal). The editorial team will be familiar with DSI but will hold DSI research to high standards.

---

## 1. Assessment of v4→v5 Revisions

### 1.1 P0 Issues from First Review — Resolution Status

| # | v4 Issue | v5 Status | Assessment |
|---|---|---|---|
| 1 | Missing SOFA/APACHE II | ✅ SOFA added (median 7 [IQR 4-11], OR=1.163/point) | Resolved. APACHE II not added but SOFA is sufficient. |
| 2 | Surgery temporal bias | ⚠️ Sensitivity analysis done (≤24h, 5.1% vs 67.4%), but main model still uses "during hospitalization" | Partially resolved. See P0-1 below. |
| 3 | DSI quartile cutoffs unreported | ✅ Reported: Q1<1.279, Q2 1.279-1.502, Q3 1.502-1.762, Q4>1.762 | Resolved. |
| 4 | NRI/IDI without 95% CIs | ✅ Bootstrap CIs added (1000 resamples) | Resolved. Reveals categorical NRI crosses zero. |
| 5 | Ischemia AUC typo (0.780) | ✅ Corrected (now 0.807 with SOFA) | Resolved. |
| 6 | TRIPOD+AI checklist missing | ✅ 27-item checklist provided (Table S4) | Resolved. Model coefficients reported (Table S6). |
| 7 | No external validation | ❌ Not performed | Acknowledged as limitation. Acceptable for minor revision. |
| 8 | Multiple imputation | ✅ Performed (5 imputations, N=8,933) | Partially resolved. See P1-1 below (only 5 imputations). |

### 1.2 P1 Issues from First Review — Resolution Status

| # | v4 Issue | v5 Status |
|---|---|---|
| 9 | KM moved to supplementary | ✅ Now Figure S2 |
| 10 | "Other" subtype ICD composition | ✅ Table S5 (30 ICD-10 codes) |
| 12 | Surgical vs non-surgical baseline | ⚠️ AUCs reported but baseline characteristics not compared |
| 14 | MICU/SICU/TSICU sensitivity | ✅ AUC=0.800 |
| 15 | BP source sensitivity | ❌ Not done; acknowledged as limitation |
| — | Calibration belt | ❌ Not added |
| — | MV extraction validation | ❌ Not done |

---

## 2. New Issues Identified in v5

### P0 — Must Resolve Before Acceptance

#### P0-1. Figure numbering is comprehensively inconsistent

**This is the most visible problem in v5.** When the KM figure was moved to supplementary, the figure legends were renumbered (Fig 5→Calibration, Fig 6→Forest, etc.), but the in-text references were NOT updated. The result is a systematic mismatch:

| Content | In-text reference | Figure legend | Actual file |
|---|---|---|---|
| Flow diagram | Figure 1 | Figure 1 | Fig1_Flowchart |
| ROC (basic vs extended) | Figure 2 | Figure 2 | Fig2_ROC |
| DCA | Figure 3 | Figure 3 | Fig3_DCA |
| RCS | Figure 4 | Figure 4 | Fig4_RCS |
| KM (now supplementary) | Figure S2 | — | Fig5_KM (still in main dir) |
| Calibration | **Figure 6** ❌ | **Figure 5** | Fig6_Calibration |
| Forest plot | **Figure 7** ❌ | **Figure 6** | Fig7_Forest |
| Subgroup ROC | **Figure 8** ❌ | **Figure 7** | Fig8_Subgroup_ROC |
| CIF | **Figure 9** ❌ | **Figure 8** | Fig9_CIF |
| ROC (extended comparison) | **Figure 10** ❌ | **Figure 9** | Fig10_ROC_extended |

Specifically:
- Section 3.3 references "Figure 10" but no Figure 10 legend exists
- Section 3.9 references "Figure 6" for calibration, but legend says Figure 5
- Section 3.10 references "Figure 7" for forest plot, but legend says Figure 6
- Section 3.11 references "Figure 8" for subgroup, but legend says Figure 7
- Section 3.2 and 3.10 reference "Figure 9" for CIF, but legend says Figure 8
- "Figure 5" is never referenced in the text body

**Action required**: Renumber all in-text figure references to match the legends (Figures 1-9). Move Fig5_KM.png to a supplementary directory. Remove the "Figure 10" reference (it should be Figure 9 per the legend). Ensure actual file names match.

#### P0-2. Figures have not been regenerated with SOFA-adjusted data

All figure files in `figures_publication/` were generated for v4 (pre-SOFA). The v5 paper reports SOFA-adjusted AUCs (e.g., extended baseline 0.787, extended+DSI 0.792, ischemia 0.807, non-surgical 0.826), but the figures likely still display v4 values (0.765, 0.773, 0.789, 0.804 respectively). This creates a data-figure mismatch.

**Action required**: Regenerate all figures using the v5 SOFA-adjusted analysis results. Specifically:
- **Fig2 (ROC)**: AUC values must show 0.635/0.787/0.792/0.796 (not 0.626/0.765/0.773/0.777)
- **Fig6 (Forest plot)**: Must include SOFA (OR=1.163) and show updated DSI OR=2.27 (not 2.53); vasopressor and MV should show non-significant CIs
- **Fig7 (Subgroup ROC)**: AUCs must reflect SOFA-adjusted values (inflammation 0.819, obstruction 0.749, perforation 0.766, ischemia 0.807, other 0.808)
- **Fig8 (CIF)**: Verify curves reflect the same CC 5,728 cohort
- **Fig9 (ROC extended)**: Must show SOFA-adjusted AUCs

#### P0-3. Duplicate and incomplete references

- **Ref 8 and Ref 22 are identical**: Both cite "Liu YC, et al. PLoS One. 2024;19(3):e0298617" — the same paper appears twice with slightly different wording.
- **Ref 21**: "Mardin FK, et al. Diastolic shock index as a predictor of mortality in ICU patients. 2025. [Preprint]" — missing preprint server, DOI, and complete author list.
- **Ref 23**: "[DSI in infectious critical illness — conference abstract, 2026.]" — completely incomplete. No authors, no journal, no abstract number. This is not a citable reference.
- **Ref 15** (Fine & Gray 1999): Cited for CIF methodology, but the paper explicitly states "a formal Fine-Gray subdistribution hazard model was not fitted." The citation is used for the conceptual framework, which is acceptable, but the text should clarify that Fine & Gray's method was referenced but not implemented.

**Action required**: (a) Merge refs 8 and 22 into a single reference and renumber. (b) Complete ref 21 with preprint server and DOI. (c) Either complete ref 23 with full citation details or remove it. (d) Renumber all in-text citations accordingly.

---

### P1 — Should Resolve

#### P1-1. Multiple imputation uses only 5 imputations

The previous review recommended "at least 20 imputations." The v5 uses only 5. While this provides a proof of concept, 5 imputations yield wider confidence intervals and less stable pooled estimates than the standard recommendation of 20+.

**Action**: Either increase to ≥20 imputations or justify why 5 is sufficient (e.g., cite Rubin's rule showing diminishing returns beyond 5 when missingness is moderate). Report the pooled DSI OR with 95% CI from MI (currently only point estimates are given: AUC=0.822, OR=2.65).

#### P1-2. Three covariates lost statistical significance after SOFA adjustment — not discussed

From Table S6 (model coefficients):

| Variable | OR | 95% CI | P-value | Status |
|---|---|---|---|---|
| Gender (M vs F) | 0.869 | 0.749-1.009 | 0.066 | ❌ Not significant |
| Vasopressor use | 1.133 | 0.948-1.353 | 0.169 | ❌ Not significant |
| Mechanical ventilation | 1.117 | 0.917-1.362 | 0.272 | ❌ Not significant |
| WBC | 1.006 | 1.000-1.012 | 0.049 | ⚠️ Barely significant |

The paper does not discuss why vasopressor use and MV lost significance after SOFA adjustment. This is expected: SOFA's cardiovascular component (MAP + vasopressor doses) and respiratory component (PaO₂/FiO₂ + ventilation) absorb variance from these binary indicators. This should be explicitly discussed as it has implications for model parsimony and multicollinearity.

**Action**: Add a paragraph in Section 3.10 or Discussion noting that vasopressor use and MV became non-significant after SOFA adjustment, likely because SOFA's organ-specific components capture overlapping information. Consider whether these variables should be retained in the final model.

#### P1-3. Main analysis still uses the temporally biased surgery definition

Section 2.6 defines surgery as "any abdominal surgical procedure during the hospitalization" — the definition flagged in the first review as having temporal bias. The ≤24h redefinition is only a sensitivity analysis. Since the sensitivity analysis shows consistent results (AUC=0.790 vs 0.792, DSI OR=2.19 vs 2.27), and only 5.1% of patients had surgery ≤24h (vs 67.4% during hospitalization), the broad definition captures mostly post-ICU-admission surgeries.

**Action**: Either (a) make the ≤24h definition the primary analysis and the broad definition the sensitivity analysis, or (b) explicitly state in the Methods that the broad definition is retained as primary because the sensitivity analysis confirms robustness, and the broad definition captures the full surgical burden which is clinically relevant for risk stratification.

#### P1-4. "Other" subtype ICD composition reveals misclassification concern

Table S5 shows the top 30 ICD-10 codes in the "Other" subtype (N=1,712, 29.9% of cohort). However, many of these are comorbidities rather than acute abdomen diagnoses:
- D62 (Acute posthemorrhagic anemia) — a consequence, not a diagnosis
- E785 (Hyperlipidemia), I10 (Hypertension), I2510 (Atherosclerotic heart disease) — comorbidities
- N179 (AKI), E872 (Acidosis), R6521 (Severe sepsis with septic shock) — complications
- Z66 (DNR status), Z515 (Palliative care) — care limitations

This suggests the "Other" category may include patients whose **primary** acute abdomen ICD code was not captured by the 4 subtype definitions, but who have various secondary diagnoses. The 29.9% proportion is large enough to affect the overall results.

**Action**: Clarify in the Methods that subtype classification was based on the primary admission diagnosis. Report what percentage of "Other" patients had secondary ICD codes matching the 4 subtypes (i.e., were they truly "other" or just misclassified by priority ordering?). Discuss whether the "Other" subgroup's AUC (0.808) is interpretable given this heterogeneity.

#### P1-5. DCA net benefit difference is clinically negligible

Section 3.6 reports: "At 10% threshold probability, the extended+DSI model yielded a net benefit of 0.128, compared with 0.126 for the extended baseline alone—a modest incremental benefit of 0.002."

A net benefit difference of 0.002 means 2 additional true positives per 1,000 patients at the cost of additional false positives — this is clinically invisible and should not be presented as supporting clinical utility.

**Action**: Reframe the DCA discussion. State that the DCA shows the extended baseline (with SOFA) already provides excellent net benefit, and DSI's addition does not meaningfully improve it at any threshold. The DCA's role is to confirm that adding DSI does not harm calibration, not to demonstrate incremental benefit. This is honest and actually strengthens the paper's credibility.

#### P1-6. Tables lack formal numbering and captions

The paper references "Table 1" through "Table 8" in section headers, but the tables themselves are embedded markdown tables without explicit "Table X:" captions. For journal submission, each table needs a numbered caption above or below the table.

**Action**: Add formal table captions (e.g., "Table 1. DSI quartile mortality gradient and baseline characteristics" etc.) to all tables.

---

### P2 — Polish

#### P2-1. Abstract precision

- "AUC range 0.75-0.83" → should be "0.749-0.826" for precision
- "12 scenarios" — the table lists 13 rows; clarify that the primary analysis (DSI mean 24h) is excluded from the count
- Consider mentioning in the abstract that the categorical NRI CI includes zero, as this is a key finding that affects interpretation

#### P2-2. Title

The title still implies all four SI derivatives are equally important ("Shock Index-Derived Parameters as Predictors..."), but the paper overwhelmingly focuses on DSI. Consider: "Diastolic Shock Index for In-Hospital Mortality Prediction in Acute Abdomen ICU Patients: A MIMIC-IV Retrospective Cohort Study"

#### P2-3. Statistical reporting

- "P=2.02×10⁻⁴⁹" for the DSI quartile gradient should use Cochran-Armitage trend test (for ordered categories) rather than plain χ², since quartiles are ordinal. The χ² test ignores the ordering.
- "P<10⁻³⁸" should be "P<0.001" per convention
- Report P-values consistently — some use scientific notation, others use "<0.001"

#### P2-4. Reference 15 (Fine & Gray)

The paper cites Fine & Gray (1999) for CIF methodology but explicitly states "a formal Fine-Gray subdistribution hazard model was not fitted." Clarify in the text that the CIF was estimated using the Aalen-Johansen estimator (which is the non-parametric equivalent) rather than the Fine-Gray regression model.

#### P2-5. Code availability

"Code available on request from the corresponding author" — AIC (Elsevier) encourages open data and code. Consider depositing on GitHub/Zenodo with a DOI.

#### P2-6. Surgical vs non-surgical baseline comparison

The first review asked for baseline characteristics of surgical vs non-surgical subgroups. The v5 reports AUCs and mortality for each group but does not provide a table comparing their baseline characteristics (age, CCI, lactate, vasopressor use, subtype distribution). This comparison is needed to interpret the non-surgical AUC=0.826 finding.

---

## 3. Reviewer-Verified Data Summary (v5)

| Metric | Paper value (v5) | Reviewer-verified | Match? |
|---|---|---|---|
| CC sample size | 5,728 | 5,728 | ✅ |
| In-hospital mortality | 19.9% (1,141) | 19.9% (1,141) | ✅ |
| SOFA median [IQR] | 7 [4-11] | 7.0 [4-11] | ✅ |
| Extended+SOFA AUC | 0.787 | 0.7867 | ✅ |
| Extended+SOFA+DSI AUC | 0.792 | 0.7920 | ✅ |
| ΔAUC | 0.005 | 0.0053 | ✅ |
| DSI OR | 2.27 (1.86-2.76) | 2.266 (1.860-2.760) | ✅ |
| DSI P-value | 4.53×10⁻¹⁶ | 4.53e-16 | ✅ |
| SOFA OR | 1.163 (1.136-1.190) | 1.163 (1.136-1.190) | ✅ |
| SOFA P-value | 1.66×10⁻³⁶ | 1.66e-36 | ✅ |
| Categorical NRI | 0.008 (−0.009, 0.044) | 0.0080 (−0.0093, 0.0435) | ✅ |
| Category-free NRI | 0.252 (0.183, 0.331) | 0.2520 (0.1827, 0.3310) | ✅ |
| IDI | 0.013 (0.007, 0.020) | 0.0128 (0.0072, 0.0198) | ✅ |
| Bootstrap optimism | 0.002 | 0.0020 | ✅ |
| Optimism-corrected AUC | 0.788 | 0.7882 | ✅ |
| MI AUC | 0.822 | 0.8224 | ✅ |
| MI DSI OR | 2.65 | 2.653 | ✅ |
| Surgery ≤24h AUC | 0.790 | 0.7902 | ✅ |
| Surgery ≤24h DSI OR | 2.19 | 2.191 | ✅ |
| DSI Q1 cutoff | 1.279 | 1.279 | ✅ |
| DSI Q2 cutoff | 1.502 | 1.502 | ✅ |
| DSI Q3 cutoff | 1.762 | 1.762 | ✅ |
| DSI Q1 mortality | 12.1% | 12.1% | ✅ |
| DSI Q4 mortality | 32.8% | 32.8% | ✅ |
| Non-surgical AUC | 0.826 | 0.826 | ✅ |
| Ischemia AUC | 0.807 | 0.807 | ✅ |
| MICU/SICU/TSICU AUC | 0.800 | 0.800 | ✅ |
| Gender P-value | Not reported | 0.066 | ❌ (should be reported) |
| Vasopressor P-value | Not reported | 0.169 | ❌ (should be reported) |
| MV P-value | Not reported | 0.272 | ❌ (should be reported) |

**Data integrity**: All key statistics verified. The revised dataset is internally consistent. No data fabrication or inconsistency detected.

---

## 4. Assessment of Key Scientific Concerns

### 4.1 The Categorical NRI Crossing Zero

This is the most important scientific issue in v5. With SOFA in the model:
- Categorical NRI = 0.008, 95% CI (−0.009, 0.044) — **crosses zero**
- Category-free NRI = 0.252, 95% CI (0.183, 0.331) — significant
- IDI = 0.013, 95% CI (0.007, 0.020) — significant

**Interpretation**: DSI changes individual predicted probabilities (category-free NRI and IDI significant) but does not reliably move patients across the 10%/30% risk strata (categorical NRI not significant). This means:
- DSI refines continuous risk estimation but does not change clinical risk category assignments
- The clinical decision impact is limited — clinicians using risk categories would make the same decisions with or without DSI

**The authors handle this well**: They transparently report it, discuss it in the Discussion (Section 4, First paragraph), and reframe DSI as a "complementary rather than replacement tool." The conclusion appropriately leads with DSI's independent predictive value (OR=2.27) rather than the ΔAUC.

**Reviewer's assessment**: The honest reporting is a strength. However, the abstract should more prominently acknowledge this limitation. Currently, the abstract states the categorical NRI CI includes zero, but it is buried in a long Results paragraph. Consider adding a sentence to the Conclusions: "The categorical NRI confidence interval included zero, indicating that DSI does not significantly improve risk category reclassification beyond the SOFA-enhanced model."

### 4.2 ΔAUC = 0.005 — Clinical Significance

The ΔAUC of 0.005 (from 0.787 to 0.792) is below the commonly cited threshold of 0.01 for clinically meaningful improvement. Combined with:
- DCA net benefit difference = 0.002 (clinically negligible)
- Categorical NRI crossing zero

The incremental value of DSI beyond SOFA is statistically present (significant OR, category-free NRI, IDI) but clinically marginal at the population level. The paper's argument rests on:
1. DSI is zero-cost and instantly available (no lab turnaround)
2. The quartile gradient (12.1%→32.8%) is clinically striking
3. Non-surgical subgroup AUC=0.826 is the strongest finding
4. MI confirms robustness

This is a reasonable argument, but the paper should more clearly acknowledge that DSI's incremental value over SOFA is modest and its primary utility may be in settings where SOFA is not yet available (e.g., ED triage, pre-ICU assessment).

### 4.3 Non-Surgical Subgroup AUC=0.826

This remains the paper's strongest finding. The interpretation that "DSI is most useful before surgical intervention alters hemodynamics" is plausible, but the alternative explanation (survivorship bias — non-surgical patients are too sick for surgery, creating more separable outcomes) has not been fully addressed. A baseline characteristics comparison table is needed.

### 4.4 Post-ICU Deaths (33.6%)

The finding that 383 of 1,141 in-hospital deaths (33.6%) occurred after ICU discharge is a clinically important observation. This supports the choice of in-hospital mortality as the primary endpoint and highlights an underrecognized population. This is a genuine contribution to the literature.

---

## 5. Strengths of the v5 Manuscript

1. **SOFA adjustment**: The most critical gap from v4 has been addressed. SOFA is now the strongest single predictor (OR=1.163/point), and DSI remains independently significant.
2. **Honest reporting**: The categorical NRI crossing zero is transparently reported and discussed. This scientific integrity is commendable and will be appreciated by reviewers.
3. **Comprehensive sensitivity analyses**: 12 scenarios including MI, surgery timing, ICU type restriction, and subtype-specific models.
4. **TRIPOD+AI compliance**: 27-item checklist with full model coefficients (Table S6) enables external validation.
5. **Multiple imputation**: Confirms CC analysis is conservative (MI AUC=0.822 vs CC 0.792).
6. **Large sample**: 5,728 CC patients — 10× larger than any prior DSI study.
7. **Novel population**: First evaluation of SI derivatives in acute abdomen ICU patients.
8. **Zero-cost tool**: DSI requires only HR and DBP — no laboratory tests or scoring algorithms.

---

## 6. Prioritized Action Items

### Must do (P0 — acceptance blockers)

| # | Action | Effort | Impact |
|---|---|---|---|
| 1 | Fix figure numbering: renumber all in-text references to match legends (1-9); remove "Figure 10" reference; move KM file to supplementary | Low | 🔴 Critical |
| 2 | Regenerate all figures with SOFA-adjusted data (AUCs, ORs, forest plot with SOFA row) | Medium | 🔴 Critical |
| 3 | Fix references: merge duplicate refs 8/22; complete refs 21 and 23 or remove; renumber all citations | Low | 🔴 Critical |

### Should do (P1 — quality improvements)

| # | Action | Effort | Impact |
|---|---|---|---|
| 4 | Discuss why vasopressor/MV lost significance after SOFA adjustment; report all P-values in Table S6 text | Low | 🟡 Important |
| 5 | Increase MI to ≥20 imputations or justify 5; report pooled DSI OR with 95% CI from MI | Medium | 🟡 Important |
| 6 | Add surgical vs non-surgical baseline characteristics table | Low | 🟡 Important |
| 7 | Reframe DCA discussion (net benefit diff=0.002 is negligible, not "modest") | Low | 🟡 Important |
| 8 | Clarify "Other" subtype classification (primary vs secondary ICD codes) | Low | 🟡 Important |
| 9 | Add formal table captions (Table 1-8) | Low | 🟡 Important |
| 10 | Consider making ≤24h surgery the primary definition | Medium | 🟡 Important |

### Nice to have (P2 — polish)

| # | Action | Effort | Impact |
|---|---|---|---|
| 11 | Refine title to focus on DSI | Trivial | 🟢 Polish |
| 12 | Use Cochran-Armitage trend test for ordered quartile gradient | Low | 🟢 Polish |
| 13 | Clarify CIF was Aalen-Johansen estimator, not Fine-Gray regression | Trivial | 🟢 Polish |
| 14 | Deposit code on GitHub/Zenodo | Low | 🟢 Polish |
| 15 | Add calibration belt plot | Low | 🟢 Polish |
| 16 | Report abstract AUC range as 0.749-0.826 | Trivial | 🟢 Polish |

---

## 7. Final Recommendation

**Minor Revision.**

The v5 manuscript has addressed the critical deficiencies identified in the first review (SOFA, NRI CIs, TRIPOD+AI, MI, DSI cutoffs). The core scientific content is sound: DSI is an independent predictor of in-hospital mortality after SOFA adjustment (OR=2.27, P=4.53×10⁻¹⁶), with a dramatic quartile gradient, robust sensitivity analyses, and honest reporting of the categorical NRI's non-significance.

The remaining issues are primarily formatting (figure numbering chaos, reference errors) and discussion enhancements (non-significant covariates, DCA reframing, non-surgical subgroup baseline comparison). These are fixable within 1-2 weeks without requiring new data extraction.

**The one substantive concern** is that the categorical NRI crossing zero weakens the clinical utility argument. The authors should ensure the paper does not overstate DSI's incremental value beyond SOFA. The current framing as "a complementary zero-cost bedside tool" is appropriate, but the abstract conclusions could be more measured.

**Estimated revision timeline**: 1-2 weeks (figure regeneration + reference cleanup + discussion additions).

**Submission logistics**: Submit to https://www.editorialmanager.com/aicoj/ (Elsevier, effective Jan 2026). Cover letter should highlight: (1) first DSI evaluation in acute abdomen; (2) SOFA-adjusted independent prediction; (3) 5,728-patient sample; (4) zero-cost bedside tool; (5) post-ICU death finding (33.6%). Reference [5] (Ospina-Tascón et al. 2020) was published in AIC — demonstrate topical alignment.

---

*Review prepared for: Jiqiang Liu (First Author) and Dengke Wu (Corresponding Author), Department of Emergency Medicine, The Second Xiangya Hospital of Central South University.*
