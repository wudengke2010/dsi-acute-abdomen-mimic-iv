# Cover Letter

**Date:** August 22, 2026

**To:** The Editor-in-Chief, *World Journal of Emergency Surgery*

**Re:** Submission of original research article — "Diastolic Shock Index as an Independent Predictor of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation"

---

Dear Editor,

We are pleased to submit our original research article entitled "Diastolic Shock Index as an Independent Predictor of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation" for consideration for publication in *World Journal of Emergency Surgery*.

## Summary of the Study

This retrospective cohort study utilized MIMIC-IV v3.1 (546,028 admissions, 2008–2022) to evaluate the diastolic shock index (DSI = HR/DBP) as an independent, zero-cost bedside predictor of in-hospital mortality in critically ill patients with acute abdomen, with external validation in eICU-CRD (208 hospitals, N=5,755). Among 5,728 complete-case ICU stays (in-hospital mortality 19.9%), DSI maintained independent prognostic value (OR=2.18, 95% CI 1.79–2.65, P=7.59×10⁻¹⁵) after SOFA adjustment. Component decomposition confirmed that DSI captures prognostic information unavailable from isolated HR (AUC=0.571) or DBP (AUC=0.597): within matched DBP or HR quintiles, DSI tertile consistently stratified mortality. The DSI quartile mortality gradient was dramatic (12.1%→32.8%, 2.7-fold) and closely replicated externally (12.0%→33.5%). Robustness was confirmed via a pre-specified DAG causal framework, E-value analysis (point estimate 3.78), Benjamini-Hochberg FDR correction, multiple imputation (N=8,933, AUC=0.822), and 14 sensitivity analyses addressing nine bias categories. Analysis code is publicly available at https://github.com/wudengke2010/dsi-acute-abdomen-mimic-iv.

## Why This Study Fits *World Journal of Emergency Surgery*

1. **Acute abdomen is the core readership of WJES**: Acute abdomen requiring ICU admission carries 15–20% mortality, and early risk stratification is central to emergency surgery decision-making — triage intensity, timing of surgical source control, and postoperative monitoring. Our study addresses precisely this decision point: DSI is computed from HR and DBP within seconds of ED or ICU admission, before laboratory results return, offering immediate risk stratification when surgical decisions must be made under time pressure.

2. **First systematic evaluation of shock index derivatives in acute abdomen ICU patients**: The SI-derivative literature (Ospina-Tascón et al. in septic shock; Jouffroy et al. prehospital; Liu et al. in sepsis; Olaussen et al. in trauma) has never systematically addressed acute abdomen — a population with unique pathophysiological diversity (perforation-induced peritonitis, mesenteric ischemia, obstruction, inflammation) that emergency surgeons manage daily. To our knowledge, this is the first study to compare SI, MSI, DSI, and Age-SI in this population with SOFA adjustment, component decomposition, and multi-center external validation.

3. **Relevance to emergency surgery practice**: The subtype-specific findings speak directly to emergency surgical decision-making: DSI performed best in mesenteric ischemia (mortality 40.5%, AUC=0.807) — the most time-critical abdominal emergency — and in non-surgical acute abdomen (AUC=0.826), where identifying patients who need urgent surgical evaluation versus conservative management is the central clinical question. Additionally, 33.6% of hospital deaths occurred after ICU discharge, implicating DSI-guided monitoring intensity beyond the ICU.

4. **Methodological rigor beyond typical database studies**: Our study introduces advances relevant to WJES readers: (a) a pre-specified directed acyclic graph (DAG) identifying complete-case selection on lactate/WBC as a collider; (b) E-value analysis quantifying robustness to unmeasured confounding; (c) component decomposition with matched-stratification analysis; (d) Benjamini-Hochberg FDR correction; (e) two independent multiple imputation strategies; and (f) 14 sensitivity analyses mapped to nine bias categories, including explicit handling of the survivorship bias inherent in "surgery during hospitalization" covariates — a caution directly applicable to future emergency surgery prediction studies. Reporting follows STROBE and TRIPOD+AI guidelines; checklists are provided.

5. **Externally validated, generalizable, and transparent**: Discrimination was preserved across 208 US hospitals (AUC=0.792), and we transparently report that calibration requires local recalibration (intercept shift −3.935). We also transparently acknowledge that ΔAUC (0.005) is below conventional clinical relevance thresholds and position DSI as a complementary bedside tool, not a SOFA replacement. All analysis code is publicly available.

We believe this study will be of significant interest to the readership of *World Journal of Emergency Surgery* — emergency surgeons, acute care surgeons, and intensivists managing abdominal emergencies.

## Important Disclosures

- This manuscript has not been published previously and is not under consideration elsewhere.
- All authors have approved the final manuscript and agree with its submission to *World Journal of Emergency Surgery*.
- The study uses publicly available, de-identified data (MIMIC-IV v3.1, eICU-CRD v2.0). IRB approval (BIDMC, MIT) was obtained; individual consent was waived.
- The authors declare no competing interests.
- This work was supported by the National Health Commission (GWJJMB202510024181), Changsha Science and Technology Bureau (kq2014242), and Hunan Provincial Natural Science Foundation (2021JJ30959). Funders had no role in study design, analysis, or publication.

Sincerely,

**Dengke Wu, MD, PhD** (Corresponding Author)
Department of Emergency Medicine, Second Xiangya Hospital, Central South University
Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University
139 Renmin Middle Road, Changsha 410011, Hunan, China
Email: wudk2010@csu.edu.cn
ORCID: 0000-0003-4101-8461

**Yuzhong Cai, MD** (First Author)
Department of Emergency Medicine
Second Xiangya Hospital of Central South University
Changsha 410011, Hunan, China
Email: caiyuzhong@csu.edu.cn
ORCID: 0009-0004-3425-3898

**Jiqiang Liu, MD**
Department of Emergency Medicine
Second Xiangya Hospital of Central South University
Changsha 410011, Hunan, China
ORCID: 0009-0000-9884-3089
