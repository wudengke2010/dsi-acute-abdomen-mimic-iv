# Cover Letter

**Date:** August 7, 2026

**To:** The Editor-in-Chief, *Annals of Intensive Care*

**Re:** Submission of original research article — "Diastolic Shock Index as an Independent Predictor of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation"

---

Dear Editor,

We are pleased to submit our original research article entitled "Diastolic Shock Index as an Independent Predictor of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation" for consideration for publication in *Annals of Intensive Care*.

## Summary of the Study

This retrospective cohort study utilized MIMIC-IV v3.1 (546,028 admissions, 2008–2022) to evaluate DSI (HR/DBP) as an independent, zero-cost bedside predictor of in-hospital mortality in critically ill patients with acute abdomen, with external validation in eICU-CRD. Among 5,728 complete-case ICU stays (in-hospital mortality 19.9%), DSI maintained independent prognostic value (OR=2.18, 95% CI 1.79–2.65, P=7.59×10⁻¹⁵) after SOFA adjustment. The primary model excluded surgery to avoid survivorship bias (only 5.1% had surgery ≤24h). Adding DSI yielded AUC=0.790 vs baseline 0.785 (ΔAUC=0.005, DeLong P=0.012). We transparently acknowledge that ΔAUC is below clinical relevance thresholds (≥0.02 per Cook 2007, Vickers et al. 2011), and categorical NRI crosses zero (0.008, 95% CI −0.009 to 0.044). DSI's clinical value lies in its independent association (OR=2.18), dramatic quartile mortality gradient (12.1%→32.8%, 2.7-fold), and zero-cost bedside availability complementary to SOFA when laboratory data are pending. Component decomposition confirmed that DSI captures prognostic information unavailable from isolated HR (AUC=0.571) or DBP (AUC=0.597). External validation across 208 hospitals preserved discrimination (AUC=0.792) and replicated the quartile gradient (12.0%→33.5%), though calibration required local recalibration (intercept shift −3.935). Robustness was confirmed via an a priori DAG causal framework, E-value analysis (point estimate 3.78), Benjamini-Hochberg FDR correction, multiple imputation (N=8,933, AUC=0.822), MICE comparison, and 14 sensitivity analyses addressing nine bias categories. Analysis code is publicly available at https://github.com/wudengke2010/dsi-acute-abdomen-mimic-iv.

## Why This Study Fits *Annals of Intensive Care*

1. **Novelty — first evaluation of SI derivatives in acute abdomen ICU patients**: DSI was originally described by Ospina-Tascón et al. in *Annals of Intensive Care* (2020) for septic shock. To our knowledge, no prior study — from MIMIC-IV or any other database — has systematically evaluated SI-derived parameters (SI, MSI, DSI, Age-SI) in acute abdomen ICU patients with SOFA adjustment, component decomposition, and external validation. The broader SI-derivative literature (Jouffroy et al. in prehospital septic shock; Liu et al. in sepsis; Olaussen et al. in trauma) has not addressed this population, nor performed component decomposition or multi-center external validation.

2. **Differentiation from existing MIMIC-IV studies**: Zhang et al. (2024) developed a nomogram for intra-abdominal infection mortality using the same MIMIC-IV database, but their model relied on six laboratory variables (lactate, age, APTT, BUN, TBIL, platelets) requiring 30–60 minutes to obtain, excluded hemodynamic parameters entirely, and validated in only 149 patients (33 deaths). In contrast, our Extended+DSI model achieved virtually identical discrimination (AUC=0.790 vs 0.795) using HR and DBP — available within seconds at the bedside — and our external validation cohort (eICU-CRD, N=5,755, 1,151 deaths, 208 hospitals) was 39-fold larger. This positions DSI not as a competitor to lab-based nomograms, but as a complementary zero-cost tool for the critical first minutes of ICU admission when laboratory results are pending.

3. **Methodological innovations beyond typical database studies**: While most MIMIC-IV prediction studies report AUC and logistic regression, our study introduces several methodological advances to the acute abdomen literature: (a) a pre-specified directed acyclic graph (DAG) formalizing the causal structure, including identification of complete-case selection on lactate/WBC as a collider — a bias source not previously formalized in MIMIC-IV acute abdomen studies; (b) E-value analysis (point estimate 3.78, CI lower bound 2.98) quantifying robustness to unmeasured confounding; (c) component decomposition with matched-stratification analysis demonstrating that DSI captures prognostic information unavailable from isolated HR or DBP — extending Ospina-Tascón's finding to a new population; (d) Benjamini-Hochberg FDR correction for all DeLong comparisons; (e) two independent multiple imputation strategies (IterativeImputer + MICE with Rubin's rules) confirming DSI OR stability (2.63–2.65); and (f) 14 sensitivity analyses mapped to nine specific bias categories. Analysis code is publicly available at https://github.com/wudengke2010/dsi-acute-abdomen-mimic-iv.

4. **Clinical relevance for intensive care**: Acute abdomen requiring ICU admission carries 15–20% mortality. A zero-cost bedside tool providing immediate risk stratification before laboratory results — with externally validated discrimination across 208 hospitals (AUC=0.792) and a dramatic quartile mortality gradient (12.1%→32.8%, 2.7-fold, replicated in eICU-CRD as 12.0%→33.5%) — is of direct practical value to intensivists. We transparently acknowledge that ΔAUC (0.005) is below conventional clinical relevance thresholds (≥0.02 per Cook 2007, Vickers et al. 2011) and that categorical NRI crosses zero; we therefore position DSI as a complementary bedside tool, not a SOFA replacement.

5. **Timeliness and editorial alignment**: DSI has emerged as a research hotspot (2024–2025). Professor Teboul, Editor-in-Chief of *Annals of Intensive Care*, is a co-author of the foundational DSI paper (Ospina-Tascón et al. 2020). Our study extends that work from septic shock to acute abdomen — a population with distinct pathophysiology (splanchnic vascular compromise, perforation-induced peritonitis, mesenteric ischemia) — using causal inference methods and component decomposition that the original study did not employ.

## Important Disclosures

- This manuscript has not been published previously and is not under consideration elsewhere.
- All authors have approved the final manuscript and agree with its submission to *Annals of Intensive Care*.
- The study uses publicly available, de-identified data (MIMIC-IV v3.1, eICU-CRD v2.0). IRB approval (BIDMC, MIT) was obtained; individual consent was waived.
- The authors declare no conflicts of interest.
- This work was supported by the National Health Commission (GWJJMB202510024181), Changsha Science and Technology Bureau (kq2014242), and Hunan Provincial Natural Science Foundation (2021JJ30959). Funders had no role in study design, analysis, or publication.

We believe this study will be of significant interest to the readership of *Annals of Intensive Care* and the broader critical care community.

Sincerely,

**Dengke Wu, MD**
Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute
The Second Xiangya Hospital of Central South University
Changsha 410011, Hunan, China
Email: wudk2010@csu.edu.cn
ORCID: 0000-0003-4101-8461

**Jiqiang Liu**
Department of Emergency Medicine
The Second Xiangya Hospital of Central South University
Changsha 410011, Hunan, China
ORCID: 0009-0000-9884-3089
