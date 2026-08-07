# P0 问题根因分析报告

**日期**: 2026-07-15
**分析对象**: SCI_paper_v5_revised.md 第三轮AIC审稿发现的8项P0问题
**方法**: 逐项追溯原始数据文件、分析脚本、论文版本演变

---

## 文件时间线

| 时间 | 文件 | 事件 |
|---|---|---|
| 07-07 20:25 | analysis_dataset.csv | 原始数据集(N=8,933, 无extended covariates) |
| 07-07 20:48 | table4-8_*.csv | advanced_statistical_analysis.py生成5个表格CSV |
| 07-07 22:41 | SCI_paper_v3.md | v3论文(基于原始数据) |
| 07-08 12:10 | analysis_dataset_corrected.csv | 修正后全数据集(N=8,933, 含extended covariates) |
| 07-12 20:12 | SCI_paper_v4_corrected.md | v4论文(修正hospital_expire_flag) |
| 07-12 20:15 | generate_figures_publication.py | v4图片生成脚本(含SVG) |
| 07-12 20:16 | figures/*.svg, *v4*.png | v4图片生成(10个SVG+12个PNG/PDF) |
| 07-12 20:18 | Table_S3_Baseline_Characteristics.csv | Table S3生成(**SOFA尚不存在**) |
| 07-12 20:57 | extract_sofa.py 运行 | SOFA提取(39分钟后) |
| 07-12 21:03 | analysis_dataset_with_sofa.csv | 含SOFA的数据集 |
| 07-12 21:08 | analysis_dataset_revised.csv | 最终CC数据集(N=5,728, 含SOFA) |
| 07-12 21:08 | revised_analysis_summary.csv | 全部分析结果汇总 |
| 07-12 21:59 | SCI_paper_v5_revised.md | v5论文(添加SOFA调整) |
| 07-12 22:04 | figures/*v5*.png | v5图片生成(仅PNG+PDF, 无SVG) |

---

## P0-1: 正文baseline statistics与数据集不一致

### 问题
| 指标 | 论文§3.1 (line 111) | CC数据集实际值 | Table S3值 |
|---|---|---|---|
| ICU LOS | 2.1 [1.2-4.4] | **2.7 [1.5-5.8]** | 2.7 [1.5-5.8] ✅ |
| Lactate IQR | 1.3-3.4 | **1.3-3.2** | 1.3-3.2 ✅ |
| WBC IQR | 8.2-16.2 | **7.5-16.9** | 7.5-16.9 ✅ |
| CCI IQR | 2-5 | **1-5** | 1.0-5.0 ✅ |

### 根因: **版本叠加未同步 — 正文统计量来自全数据集(N=8,933)而非CC(N=5,728)**

追溯发现：
1. **ICU LOS 2.1[1.2-4.4]**: 精确匹配 `analysis_dataset_corrected.csv`（N=8,933全数据集）的 `los.median()=2.1, IQR=1.2-4.4`。CC数据集(N=5,728)的ICU LOS为2.7[1.5-5.8]。**正文误用了全数据集的LOS值。**

2. **Lactate IQR上界3.4**: CC数据集和全数据集都是1.3-3.2。3.4不匹配任何已知数据集版本，可能来自更早的中间计算（v2/v1时代的analysis_dataset_extended.csv已无法直接验证，因该文件不含lactate列名或已被覆盖）。

3. **WBC IQR 8.2-16.2**: CC数据集是7.5-16.9，全数据集是7.1-15.4。8.2-16.2不匹配任何已知版本，同样可能来自中间计算。

4. **CCI IQR下界2**: CC数据集是1-5。原始 `table1_baseline.csv`(N=7,004)显示survived组CCI=2.0[1.0-4.0]、died组=4.0[2.0-7.0]。**可能误取了survived组的IQR下界2而非overall的1。**

5. v3论文(07-07)的§3.1使用的是v1数据(N=5,723)，当时的统计量来自 `table1_baseline.csv`(N=7,004)。v4论文(07-12 20:12)修正了样本量(5,723→5,728)和结局(hospital_expire_flag)，但**§3.1的baseline统计量直接从v3复制**，未用CC数据集重新计算。

6. Table S3由 `generate_table_s3.py` 于20:18生成，正确读取了CC数据集(`analysis_dataset_corrected.csv` dropna后N=5,728)，所以Table S3值正确。**但正文§3.1从未与Table S3同步。**

### 结论
**核心原因：论文文本在不同版本间复制粘贴时，baseline statistics始终沿用旧值（来自全数据集或更早的中间数据集），未根据最终CC数据集(N=5,728)重新计算并更新。Table S3虽然正确，但正文从未与之对齐。**

---

## P0-2: Basic baseline AUC 0.635 vs 0.626

### 问题
论文§3.3 (line 132, 136) 写 AUC=0.635，但实际计算值=0.626。

### 根因: **v5修改时混入了SI-only模型的AUC值**

验证发现：
| 模型定义 | AUC |
|---|---|
| Age+Sex+CCI (论文定义的basic baseline) | **0.6260** ✅ |
| SI_mean only (recompute_models.py中的"Basic"定义) | **0.6347** ≈ 0.635 ❌ |
| DSI_mean only | 0.6437 |
| Age+Sex only | 0.5590 |
| CCI only | 0.6190 |

**关键发现**: SI-only模型的AUC=0.6347，四舍五入后=0.635，与论文中的错误值完全匹配。

版本追溯：
- v3论文(07-07): AUC=**0.626** ✅
- v4论文(07-12 20:12): AUC=**0.626** ✅
- v5论文(07-12 21:59): AUC=**0.635** ❌ (新引入的错误)

`recompute_models.py` 第50-51行定义的"Basic (SI)"模型为 `X_basic = cc[['SI_mean']]`（仅含SI_mean一个变量），这不是论文定义的"basic baseline (age+sex+CCI)"。v5在修改§3.3添加SOFA内容时，可能参考了 `recompute_models.py` 的输出，误将SI-only的AUC(0.635)当作basic baseline的AUC写入论文。

### 结论
**核心原因：recompute_models.py中"Basic"模型的定义(X=SI_mean only)与论文中"basic baseline"的定义(age+sex+CCI)不一致。v5修改时误用了脚本中SI-only模型的AUC值0.635，而非正确的age+sex+CCI模型的AUC值0.626。**

---

## P0-3: §3.8 Figure引用错误 (Figure 9 → Figure 8)

### 问题
论文§3.8 (line 194): "cumulative incidence functions (Section 3.2, Figure 9)"，但CIF实际是Figure 8。

### 根因: **v5重新编号时部分交叉引用遗漏**

v4→v5的图表重编号映射：
| v4编号 | 内容 | v5编号 |
|---|---|---|
| Fig 5 | KM曲线 | → Fig S2 (移至补充材料) |
| Fig 6 | 校准图 | → Fig 5 |
| Fig 7 | 森林图 | → Fig 6 |
| Fig 8 | 亚组ROC | → Fig 7 |
| Fig 9 | CIF | → Fig 8 |
| Fig 10 | ROC extended | → Fig 9 |

通过v4/v5 diff对比确认：
- §3.10 (line 204): "cumulative incidence functions (**Figure 8**)" — ✅ 已正确更新
- §3.8 (line 194): "cumulative incidence functions (Section 3.2, **Figure 9**)" — ❌ 遗漏

v4中CIF是Figure 9，§3.8的引用在v4中是正确的。v5将CIF从Fig9改为Fig8，但§3.8的这处引用未同步更新。

### 结论
**核心原因：v5从10图缩减为9图时，对CIF的引用进行了部分更新(§3.10已改)，但遗漏了§3.8中的一处引用。这是手动编辑交叉引用时的典型遗漏错误。**

---

## P0-4: Tables 4-8完全缺失

### 问题
§3.7-3.11的section标题引用Table 4-8，但正文中从未展示这些表格。

### 根因: **分析脚本生成了CSV但从未整合进论文**

文件追溯：
- `table4_rcs.csv` — 由 `advanced_statistical_analysis.py` 于07-07 20:48生成
- `table5_km_logrank.csv` — 同上
- `table6_calibration.csv` — 同上
- `table7_forest.csv` — 同上
- `table8_subgroup_auc.csv` — 同上

这5个CSV文件均存在且包含数据，但其内容从未被格式化为markdown表格整合进论文正文。v3/v4/v5三个版本的论文都在section标题中引用了"Table 4"-"Table 8"，但从未展示表格内容。

注意：这些CSV使用的是**原始v1数据集**(N=5,723, 无SOFA)，其中：
- `table7_forest.csv`: 4个SI指标同时入模(严重多重共线性)，DSI OR=18.79 — 与v5论文的Extended+DSI模型(OR=2.27)完全不同
- `table8_subgroup_auc.csv`: 单变量DSI-only AUC(如perforation=0.616) — 与v5论文的Extended+SOFA+DSI AUC(如perforation=0.766)完全不同
- `table5_km_logrank.csv`: DSI χ²=47.27 — 与论文中的χ²=71.2不同(后者用修正数据集重算)

### 结论
**核心原因：分析脚本生成的中间CSV从未被整合进论文。且这些CSV基于原始v1数据集，即使整合也需用修正后的CC数据集重新计算。三个论文版本均未解决此问题。**

---

## P0-5: Table S3缺少SOFA行

### 问题
补充材料描述Table S3为"including SOFA scores"，但表中无SOFA行。

### 根因: **时间顺序错误 — Table S3在SOFA提取之前生成**

时间线：
1. 20:18 — `generate_table_s3.py` 运行，生成 `Table_S3_Baseline_Characteristics.csv`
2. 20:57 — `extract_sofa.py` 运行，提取SOFA分数（39分钟后）
3. 21:08 — `analysis_dataset_revised.csv` 生成（含SOFA列）

`generate_table_s3.py` 第3行读取的是 `analysis_dataset_corrected.csv`，该文件**没有SOFA列**。脚本中也没有添加SOFA行的代码。因此Table S3生成时根本无法包含SOFA。

v5论文修改时，将Table S3的描述文本改为"including SOFA scores"(line 270)，但**未重新运行 `generate_table_s3.py`** 来更新实际表格内容。

### 结论
**核心原因：SOFA提取(extract_sofa.py, 20:57)晚于Table S3生成(generate_table_s3.py, 20:18)39分钟。v5论文只修改了描述文本，未重新运行脚本更新表格内容。**

---

## P0-6: v4图片残留 + 无v5 SVG

### 问题
figures/目录中有12个v4 PNG/PDF + 10个v4 SVG文件未清理；v5未生成SVG矢量图。

### 根因: **文件名不冲突导致旧文件未被覆盖 + v5脚本未调用savefig('.svg')**

v4与v5的文件命名对照：
| v4文件名 | v5文件名 | 冲突? |
|---|---|---|
| Fig5_KM.png/pdf/svg | Fig5_Calibration.png/pdf | ❌ 不冲突 |
| Fig6_Calibration.png/pdf/svg | Fig6_Forest.png/pdf | ❌ 不冲突 |
| Fig7_Forest.png/pdf/svg | Fig7_Subgroup_ROC.png/pdf | ❌ 不冲突 |
| Fig8_Subgroup_ROC.png/pdf/svg | Fig8_CIF.png/pdf | ❌ 不冲突 |
| Fig9_CIF.png/pdf/svg | Fig9_ROC_extended.png/pdf | ❌ 不冲突 |
| Fig10_ROC_extended.png/pdf/svg | (无对应) | ❌ 不冲突 |
| Fig1-4_*.svg | (无v5 SVG) | — |

由于v4和v5使用了不同的文件名（v4: Fig5_KM, v5: Fig5_Calibration），v5的 `savefig()` 不会覆盖v4文件，导致v4文件残留。

v5脚本 `generate_figures_v5.py` 的所有 `savefig()` 调用（如line 147-148）只写了 `.png` 和 `.pdf`，没有 `.svg`。而v4脚本 `generate_figures_publication.py` 额外生成了SVG。

### 结论
**核心原因：(1) v5重编号导致文件名变化，旧v4文件不会被同名覆盖而残留；(2) v5脚本的savefig调用缺少'.svg'格式，未生成矢量图。**

---

## P0-7: 无DeLong P值

### 问题
Methods §2.7 (line 83) 声明"With DeLong method comparisons"，但Results从未报告DeLong P值。

### 根因: **方法声明与代码实现脱节**

代码审查：
- `recompute_models.py`: 仅使用 `roc_auc_score()` 计算AUC点估计值，通过bootstrap计算NRI/IDI的95% CI，**未实现DeLong检验**
- `generate_figures_v5.py`: 同样仅计算AUC值，无DeLong实现
- 项目中**没有任何脚本实现DeLong Z-test**

论文Methods中引用了DeLong 1988年原文(ref 16)并声明使用该方法，但实际分析从未执行该检验。ΔAUC=0.005是否具有统计学显著性至今未知。

### 结论
**核心原因：Methods中声明了DeLong检验但分析脚本从未实现该检验。这是一个"方法学声明与实际分析脱节"的问题——论文写了好方法但代码没跟上。**

---

## P0-8: 无VIF/共线性诊断

### 问题
SOFA的心血管组件包含vasopressor剂量和MAP，模型同时纳入vasopressor_use(binary)和mechanical_ventilation——存在结构性共线性风险，但从未进行VIF诊断。

### 根因: **分析计划中从未包含VIF**

代码审查：
- `recompute_models.py`: 无VIF计算
- `generate_figures_v5.py`: 无VIF计算
- 论文全文: 无"VIF"、"collinearity"、"variance inflation"等关键词

Table S6模型系数显示：vasopressor_use在SOFA调整后P=0.169不显著，MV的P=0.272不显著。这可能是共线性导致的标准误膨胀，但未被诊断。

`recompute_models.py` 第55-56行定义的Extended模型同时包含：
- `vasopressor_use` (binary, 24h内任何血管活性药物使用)
- `sofa` (其中心血管组件直接使用vasopressor剂量+MAP)
- `mechanical_ventilation` (binary, 24h内任何呼吸机使用)

SOFA的呼吸组件使用PaO2/FiO2比值，与MV存在间接关联（MV影响FiO2），但不是严格的数学嵌套关系。

### 结论
**核心原因：分析设计阶段未规划VIF诊断。SOFA与vasopressor_use之间的结构性共线性（SOFA心血管组件直接使用vasopressor剂量）从未被评估。这是一个缺失的分析步骤，而非"有但没报告"。**

---

## 总结：根因分类

| 根因类型 | 涉及P0 | 本质 |
|---|---|---|
| **版本叠加未同步** | P0-1, P0-3 | 论文在不同版本间复制粘贴时，部分数值/引用未更新 |
| **脚本与论文定义不一致** | P0-2 | recompute_models.py中"Basic"定义≠论文"basic baseline"定义 |
| **生成但未整合** | P0-4 | CSV文件存在但从未格式化进论文 |
| **时间顺序错误** | P0-5 | Table S3在SOFA提取之前生成，未补运行 |
| **文件管理疏漏** | P0-6 | 旧文件名不冲突未被覆盖 + 新脚本缺SVG输出 |
| **方法声明未实现** | P0-7 | Methods写了DeLong但代码从未实现 |
| **分析计划缺失** | P0-8 | 从未规划VIF诊断 |

**根本原因模式**: 8项P0问题中，5项(P0-1/2/3/4/5)与**多版本迭代中的同步遗漏**直接相关——每次修改论文时只关注当前修改点，未对全文进行系统性的数据一致性核对。2项(P0-6/7)与**脚本与论文的脱节**有关。1项(P0-8)是**分析计划遗漏**。
