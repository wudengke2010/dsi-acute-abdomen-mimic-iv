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
| `convert_v8_to_docx.py` | Convert manuscript to formatted DOCX |
| `Cover_Letter_WJES.md` | Cover letter for World Journal of Emergency Surgery |
| `make_strobe_wjes.py` | STROBE checklist generation script |
| `research_protocol.md` | Statistical Analysis Plan (SAP) |
| `pre_draft_reviewer_responses.md` | Anticipated reviewer responses |

## Public Data and Results

This repository publishes all **aggregate-level** results from the study (no patient-level data, per the PhysioNet Data Use Agreement):

### Published Figures (`figures_v7/`, 300 dpi, PNG + PDF)
| File | Description |
|------|-------------|
| `Fig1_Flowchart.png` | Study cohort flow diagram |
| `Fig2_ROC.png` | ROC curves with DeLong comparisons |
| `Fig3_Forest.png` | Forest plot of adjusted odds ratios |
| `FigS1–S11` | Supplementary figures (calibration, DCA, RCS, subtypes, DAG, component decomposition, nomogram, CIC) |

### Published Result Tables (CSV)
| File | Description |
|------|-------------|
| `Table_S3_Baseline_Characteristics.csv` | Baseline characteristics by DSI quartile |
| `Table_S6_Model_Coefficients.csv` | Full multivariable model coefficients |
| `Table_S7_eICU_Baseline_by_DSI_Quartile.csv` | External validation cohort baseline |
| `Table_S8_Excluded_vs_CC_Characteristics.csv` | Excluded vs complete-case comparison |
| `Table_S11_Sensitivity_Analyses_Summary.csv` | 14 sensitivity analysis scenarios |
| `table2_auc.csv`, `table3_nri_idi.csv` | AUC / NRI / IDI performance metrics |
| `table4_rcs.csv` | Restricted cubic spline dose–response |
| `table8_subgroup_auc.csv` | Subtype-specific AUCs |
| `table_bootstrap_validation.csv` | Bootstrap internal validation |
| Other `Table_S*.csv` / `table*.csv` | Additional supplementary result tables |

### Published Statistics (JSON)
| File | Description |
|------|-------------|
| `v6_revision_statistics.json` | Complete model statistics (ORs, CIs, AUCs, P values) |
| `component_decomposition_results.json` | HR vs DBP vs DSI decomposition analysis |
| `eicu_external_validation_results.json` | External validation metrics |

> **Note**: Patient-level datasets (`analysis_dataset*.csv`, `icu_vitals*.csv`, `eicu_external_validation_dataset.csv`, etc.) are **not** distributed here. The source databases (MIMIC-IV, eICU-CRD) are available from PhysioNet to credentialed researchers; the provided scripts reproduce all derived datasets end-to-end.

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
