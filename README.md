# dsi-acute-abdomen-mimic-iv

**Diastolic Shock Index as an Independent Predictor of In-Hospital Mortality in Critically Ill Patients with Acute Abdomen: A Retrospective Cohort Study with External Validation**

Jiqiang Liu†, Dengke Wu\*

Department of Emergency Medicine, and Emergency Medicine and Difficult Diseases Institute, The Second Xiangya Hospital of Central South University, Changsha 410011, Hunan, China

---

## Overview

This repository contains the analysis code for evaluating Diastolic Shock Index (DSI = HR/DBP) as a bedside predictor of in-hospital mortality in ICU patients with acute abdomen, using MIMIC-IV v3.1 and eICU-CRD v2.0 databases.

## Data Sources

- **MIMIC-IV v3.1** (2008–2022): Primary derivation cohort
- **eICU-CRD v2.0** (208 US hospitals): External validation cohort

Both datasets are available via PhysioNet:
- [MIMIC-IV](https://physionet.org/content/mimiciv/)
- [eICU-CRD](https://physionet.org/content/eicu-crd/)

## Repository Structure

### Data Extraction
| Script | Description |
|--------|-------------|
| `extract_vitals.py` | Extract vital signs (HR, SBP, DBP, MAP) from chartevents |
| `extract_vitals_full.py` | Full vital signs extraction with chunked processing |
| `extract_sofa.py` | Compute SOFA scores from MIMIC-IV concept tables |
| `extract_extended_covariates.py` | Extract lab values, vasopressor, surgery, ventilation |
| `process_data.py` | Merge all data, compute SI derivatives, classify subtypes |
| `process_data_v2.py` | Updated processing pipeline with full vitals |

### Primary Analysis
| Script | Description |
|--------|-------------|
| `statistical_analysis.py` | Core logistic regression, AUC, DeLong tests |
| `comprehensive_analysis.py` | Extended models, bootstrap, sensitivity analyses |
| `advanced_statistical_analysis.py` | NRI/IDI, RCS, KM, calibration, subgroup ROC |
| `correction_analysis.py` | Corrected analyses after data verification |
| `recompute_models.py` | Full model recomputation with multiple imputation |
| `compute_v6_stats.py` | v6 revision statistics |
| `compute_all_stats.py` | Comprehensive statistics summary |

### Supplementary Analyses
| Script | Description |
|--------|-------------|
| `component_decomposition.py` | DSI component (HR vs DBP) decomposition |
| `eicu_external_validation.py` | eICU-CRD external validation pipeline |
| `generate_dag_evalue.py` | DAG causal diagram + E-value sensitivity analysis |
| `generate_nomogram_cic.py` | Nomogram + Clinical Impact Curve |
| `mice_comparison.py` | Comparison of 3 imputation strategies (IterativeImputer, MICE, Median) |
| `generate_figS8.py` | Supplementary heatmap figures (DBP/HR × DSI) |
| `generate_table_s3.py` | Supplementary table generation |

### Figure Generation
| Script | Description |
|--------|-------------|
| `generate_figures_publication.py` | Publication-quality figures (v4/v5) |
| `generate_figures_corrected.py` | Corrected figures (v6) |
| `generate_figures_sci.py` | SCI-style figures (v7) |
| `generate_figures_v7.py` | Final v7 figures |

### Manuscript & Submission
| File | Description |
|------|-------------|
| `SCI_paper_v8.md` | Final manuscript (Markdown source) |
| `convert_v8_to_docx.py` | Convert manuscript to AIC-formatted DOCX |
| `Cover_Letter_AIC.md` | Cover letter for Annals of Intensive Care |
| `research_protocol.md` | Statistical Analysis Plan (SAP) |
| `pre_draft_reviewer_responses.md` | Anticipated reviewer responses |
| `submission_checklist_v8.md` | AIC submission checklist |

## Key Results

- **Primary cohort**: N=5,728 CC (MIMIC-IV), in-hospital mortality 19.9%
- **DSI independent OR**: 2.18 (95% CI 1.79–2.65, P=7.59×10⁻¹⁵)
- **Quartile mortality gradient**: 12.1% → 32.8% (2.7-fold)
- **External validation** (eICU): AUC=0.792, replicated gradient 12.0% → 33.5%

## Requirements

```
python >= 3.10
duckdb, pandas, numpy, scipy, scikit-learn, statsmodels, lifelines, matplotlib
```

## Citation

If you use this code, please cite the corresponding paper.

## License

MIT License

## Contact

Dengke Wu: wudk2010@csu.edu.cn
