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

1. **Novelty**: First systematic evaluation of DSI — originally described by Ospina-Tascón et al. in *Annals of Intensive Care* (2020) for septic shock — in acute abdomen ICU patients. Component decomposition extends the principle that DSI outperforms isolated HR or DBP to a new population.

2. **Clinical relevance for intensive care**: Acute abdomen requiring ICU admission carries 15–20% mortality. A zero-cost bedside tool providing immediate risk stratification before laboratory results is of direct practical value to intensivists.

3. **Methodological rigor**: STROBE and TRIPOD+AI-compliant; DAG-based causal framework with E-value sensitivity analysis; primary model excludes surgery to avoid survivorship bias; transparent disclosure of ΔAUC below clinical thresholds and categorical NRI crossing zero; Benjamini-Hochberg FDR correction for multiplicity; bootstrap validation, DeLong testing, VIF diagnostics, NRI/IDI, DCA, RCS, CIF; two multiple imputation strategies (IterativeImputer + MICE); 14 sensitivity analyses across nine bias categories; external validation with both un-recalibrated and recalibrated metrics; analysis code publicly available.

4. **Timeliness**: DSI has emerged as a research hotspot (2024–2025), with multiple publications in critical care journals. Our study extends this evidence with causal inference methods and component decomposition to a previously unexamined population.

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
ORCID: 0009-0008-1363-9621

**Jiqiang Liu**
Department of Emergency Medicine
The Second Xiangya Hospital of Central South University
Changsha 410011, Hunan, China
ORCID: 0009-0000-9884-3089
