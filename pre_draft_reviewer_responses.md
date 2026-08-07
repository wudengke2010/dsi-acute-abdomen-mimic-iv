# Pre-Draft Reviewer Response Document
## DSI Acute Abdomen Paper — Annals of Intensive Care

---

## Methodological Concerns

### Q1: Why exclude 36% of patients? Doesn't this introduce selection bias?

**Prepared response**: We acknowledge this concern and have addressed it through three complementary strategies:
1. **DAG framework** (Supplementary Figure S11): The DAG formalizes lactate/WBC measurement as a collider opened by complete-case selection, identifying collider stratification bias.
2. **Multiple imputation** on the full eligible cohort (N=8,933) produced a larger DSI effect (OR=2.65 vs 2.18), indicating the CC estimate is conservative rather than inflated.
3. **E-value analysis**: An unmeasured confounder would need an association exceeding 3.78-fold with both DSI and mortality to explain the point estimate—larger than SOFA (OR=1.16/point), lactate (OR=1.14), or CCI (OR=1.14) in our model. Such confounders are biologically implausible after SOFA adjustment.
4. **MICE sensitivity**: Alternative imputation via MICE with Rubin's rules yielded consistent results (OR=2.63), confirming stability under different missing-data assumptions.

Supplementary Table S8 details excluded patient characteristics: they had substantially lower severity (mortality 8.0% vs 19.9%), confirming that exclusion enriched the CC population with sicker patients—not the reverse.

### Q2: ΔAUC=0.005 is trivial. Is DSI clinically useful?

**Prepared response**: We acknowledge ΔAUC is below conventional clinical relevance thresholds (≥0.02), as explicitly discussed in the manuscript (citing Cook 2007 and Vickers 2008). We position DSI not as a replacement for SOFA, but as a complementary zero-cost bedside tool. Three lines of evidence support clinical utility beyond ΔAUC:
1. **Quartile gradient**: 12.1%→32.8% (2.7-fold, P=2.02×10⁻⁴⁹), replicated in eICU-CRD (2.8-fold).
2. **Category-free NRI=0.252 (P<0.001)** and **IDI=0.013 (P<0.001)**: Continuous reclassification is significant, confirming additional prognostic information.
3. **Component decomposition**: DSI outperforms isolated HR (AUC=0.571) and DBP (AUC=0.597) with DeLong P<0.001, and stratifies mortality within matched DBP/HR quintiles.

Vickers et al. (BMC Med Res Methodol 2011;11:13) argue that a single statistical test is sufficient for assessing prediction model performance—we present comprehensive evidence consistent with this principle.

### Q3: Is eICU-CRD truly an external validation? Calibration was catastrophically poor.

**Prepared response**: We transparently report both un-recalibrated (Brier 0.38–0.59, HL P<0.001) and recalibrated metrics per TRIPOD+AI guidelines. The near-ideal recalibration slope (0.952) confirms discrimination is transportable across 208 hospitals—the key validity criterion. The large intercept shift (−3.935) reflects systematic differences in SOFA computation (APS-based vs MIMIC-IV concept; median 9 vs 7) rather than model failure. We explicitly recommend local recalibration before clinical application, consistent with TRIPOD type 2b/3b validation standards.

### Q4: Why weren't Fine-Gray competing risk models used?

**Prepared response**: We acknowledge this limitation. CIF curves are descriptive only; 33.6% of hospital deaths occurred after ICU discharge, making competing risks relevant. Formal Fine-Gray subdistribution hazard modeling is listed as a priority future direction (Section 4.5, item 2).

### Q5: Why does the model include vasopressor and MV when they're non-significant after SOFA adjustment?

**Prepared response**: The DAG framework (Supplementary Figure S11) identifies vasopressor and MV as downstream mediators rather than confounders in the DSI→mortality pathway—both are consequences of the hemodynamic instability captured by SOFA. We retain them in the primary model for face validity but explicitly report their non-significance (P=0.14 and P=0.45). A parsimonious model excluding both is provided (Supplementary Table S10: AUC=0.789, DSI OR=2.22).

### Q6: How was multiplicity addressed in multiple DeLong comparisons?

**Prepared response**: Benjamini-Hochberg FDR correction [38] was applied to all DeLong comparisons at the 5% threshold. All significant comparisons before correction remained significant after correction, as reported in Sections 3.3 and 3.4.

### Q7: Is the "Other" subtype (29.9%) a threat to validity?

**Prepared response**: The "Other" subgroup contains complications alongside primary ICD codes (detailed in Supplementary Table S5). Sensitivity analysis excluding "Other" preserved results (AUC=0.786–0.788, DSI OR=2.15–2.22), confirming this heterogeneity does not drive the primary findings.

### Q8: Isn't 37.3% missingness too high for MI?

**Prepared response**: We used 5 imputations with MICE/Rubin's rules for the primary MI analysis. The MI results (OR=2.65) are directionally consistent with CC analysis (OR=2.18), and alternative MICE with Rubin's rules produced similar results (OR=2.63). E-value analysis (3.78) further supports robustness. Graham et al. (Prev Sci 2007) showed that MI with 5 imputations remains valid at 50% missingness when the imputation model is correctly specified. We acknowledge the limitation and present both CC and MI results transparently.

---

## Reporting and Transparency

### Q9: Where is the analysis code?

**Prepared response**: Analysis code is publicly available at https://github.com/wudengke2010/DSI-acute-abdomen.

### Q10: How was AI used in this study?

**Prepared response**: Per TRIPOD+AI guidelines, AI was used only for language polishing and manuscript editing. All data extraction, statistical analyses, figure generation, and scientific interpretation were performed independently by the authors. This is explicitly declared in the Declarations section.

---

## Clinical and Pathophysiological Concerns

### Q11: Is DSI dimensionally meaningful? (following Dalmau 2020)

**Prepared response**: Following Dalmau [12], we acknowledge the dimensional concern and empirically address it through component decomposition analysis. Within matched DBP quintiles, DSI tertile consistently stratified mortality (e.g., DBP Q3: 12.0%→18.8%→32.5%), confirming the ratio captures prognostic information unavailable from either component alone. This mirrors the key finding of Ospina-Tascón et al. [6] in septic shock.

### Q12: Why study acute abdomen specifically? Is this just another SI study?

**Prepared response**: Acute abdomen represents a distinct pathophysiological entity from trauma and sepsis: splanchnic vascular compromise, perforation-induced peritonitis, and mesenteric ischemia create unique hemodynamic perturbations. No prior SI-derivative study has examined this population, performed component decomposition within matched vital sign quintiles, or externally validated across 208 hospitals. Our subtype analysis (ischemia AUC=0.807, mortality 40.5%) suggests particular utility in this high-risk subgroup.

### Q13: Why not use LASSO for variable selection (like Zhang 2025)?

**Prepared response**: We adopted a clinically pre-specified approach for interpretability, consistent with TRIPOD recommendations favoring pre-specification over data-driven selection. Zhang et al. [35] used LASSO to select 6 laboratory variables; their model (AUC=0.795) requires 30–60 minutes for laboratory results. Our model (AUC=0.790) uses DSI—available within seconds from routine vitals—plus pre-specified covariates. The trade-off between variable selection methods (LASSO vs. pre-specification) is discussed in Section 4.5, item 4.

---

## Data and Generalizability

### Q14: Is single-center derivation sufficient?

**Prepared response**: Derivation is single-center (BIDMC), but external validation across 208 eICU-CRD hospitals preserved discrimination (AUC=0.792) and replicated the DSI quartile gradient (2.8-fold). Prospective multicenter validation is listed as a future direction.

### Q15: Are results generalizable to non-US settings?

**Prepared response**: We acknowledge the geographic limitation. The eICU-CRD validation covers 208 US hospitals. Non-US validation is listed as a future direction (Section 4.5, item 5). However, the physiological principles underlying DSI (Windkessel effect, compensatory tachycardia, vasomotor tone loss) are universal, supporting potential transportability.
