# SCI论文图片质量检查报告

## 检查范围
- 论文: `SCI_paper_v4_corrected.md`
- 图片: `shock_index_abdomen/figures/` 目录下10张图片 (Fig1-Fig10)
- 检查维度: 布局合理性、内容完整性、重叠/覆盖、显示清晰度、标注合理性、文字与图片内容重叠、科学正确性

---

## 总体结论

**10张图中，9张存在P0级致命问题（必须重新生成），1张存在P1级严重问题。**

主要问题类别:
1. **数据/结局错误**: 8张图仍在使用旧数据 (`icu_death` / 旧分析集)，而非修正后的 `hospital_expire_flag` (in-hospital mortality)。
2. **标题/标注错误**: 6张图标题仍为"ICU Mortality" / "ICU Survival" / "ICU Death"，与论文primary outcome (in-hospital mortality) 不一致。
3. **科学计算错误**: Fig9 CIF计算错误，Y轴超出100%；Fig4 RCS曲线实际为平线，无法支持论文结论。
4. **内容缺失**: Fig1 Flowchart缺少从8,933到5,728 complete cases的最后一步。
5. **多重共线性导致可视化失败**: Fig7 Forest Plot因同时纳入4个高度共线的SI衍生指标，OR尺度严重扭曲，可读性差。
6. **关键亚型缺失**: Fig8 Subgroup ROC缺少inflammation和ischemia两个关键亚型。
7. **版面设计问题**: 颜色辨识度低、图例过小、比例失调。

---

## 逐图检查结果

### 🔴 Fig1: Patient Selection Flowchart

**文件**: `figures/Fig1_Flowchart.png` (3000×4200 px)

**P0问题**:
- **内容不完整**: 流程图只展示到 "Complete vital signs data (SBP, HR, DBP within 24h) n = 8,933"，缺少从8,933到5,728 complete cases的最后一步排除框（因缺少lactate/WBC等扩展协变量被排除的3,205例）。
- 这与论文Figure 1 legend和Methods 2.2中描述的"5,728 had complete data for extended covariates"直接矛盾。

**P1问题**:
- 图片尺寸偏高 (3000×4200)，在论文单栏排版中可能过大；建议调整为宽度≤8 inches (~2400 px at 300 dpi)。
- 排除框文字偏小 (fontsize 8)，在缩印后可能难以阅读。

**建议**: 添加第六个box: "Complete cases for extended covariates\nn = 5,728"，以及对应的exclusion box: "Excluded: Missing extended covariates\nn = 3,205"。

---

### 🔴 Fig2: ROC Curves: SI-Derived Metrics for ICU Mortality Prediction

**文件**: `figures/Fig2_ROC.png` (2099×2107 px)

**P0问题**:
1. **标题错误**: 标题为"ICU Mortality Prediction"，但论文primary outcome是 **in-hospital mortality**。
2. **数据错误**: 该图基于旧的 `analysis_dataset.csv` 和 `icu_death` 计算。图中AUC (Baseline=0.648, SI=0.695, MSI=0.691, DSI=0.692, Age-SI=0.694, Full=0.709) 与修正后数据不一致。
3. 修正后basic baseline AUC应为0.626，basic+DSI约为0.692（需重新计算确认）。

**P2问题**:
- 图例位置在右下，不遮挡曲线；曲线颜色区分度良好。
- X/Y轴标签清晰。

**建议**: 使用 `analysis_dataset_corrected.csv` 和 `hospital_expire_flag` 重新计算并绘图；标题改为 "ROC Curves: SI-Derived Metrics for In-Hospital Mortality Prediction"。

---

### 🔴 Fig3: Decision Curve Analysis: SI-Derived Metrics for ICU Mortality Prediction

**文件**: `figures/Fig3_DCA.png` (2160×1645 px)

**P0问题**:
1. **标题错误**: 同样为"ICU Mortality Prediction"。
2. **数据错误**: 基于旧数据/旧结局。Net benefit曲线是在icu_death=13.7%的基线患病率下计算，与in-hospital mortality (19.9%) 不一致。

**P1问题**:
- 阈值范围0-50%合理，但Treat All曲线在约15%后降至0以下，Net benefit范围-0.05到0.20合理。
- 图例清晰。

**建议**: 基于修正数据重新计算DCA；标题改为 "Decision Curve Analysis: SI-Derived Metrics for In-Hospital Mortality Prediction"。

---

### 🔴 Fig4: RCS: SI → ICU Mortality 等

**文件**: `figures/Fig4_RCS.png` (3569×2970 px)

**P0问题**:
1. **标题错误**: 所有4个子图标题均为"ICU Mortality"。
2. **数据错误**: 基于旧结局 `icu_death` (患病率13.7%)，参考红线在0.137左右；修正后应为19.9%。
3. **曲线实际为平线**: Y轴范围仅0.130-0.144，曲线几乎水平，无法显示任何剂量-反应关系。这与论文Results 3.7中声称的"Significant overall associations (P_overall<10⁻³⁸) without nonlinear threshold effects"严重不符。读者无法从图中看到任何关系。
4. **Y轴范围过窄**: 即使存在真实效应，0.130-0.144的范围也会使曲线看起来平坦。应扩展Y轴范围（如0-0.40）以展示相对变化。

**P1问题**:
- 4子图2×2布局合理，但子图间距和标题字体偏小。
- 阴影置信区间可见但范围极小。

**建议**: 
- 重新拟合RCS模型，使用 `hospital_expire_flag`。
- 检查样条函数实现是否正确；如有必要改用scikit-learn的SplineTransformer或patsy的rcs。
- 设置合理Y轴范围（如0-0.40或0.05-0.50）。
- 标题改为 "RCS: {metric} → In-Hospital Mortality"。

---

### 🔴 Fig5: KM Curve: DSI Quartiles → ICU Survival

**文件**: `figures/Fig5_KM.png` (3570×2970 px)

**P0问题**:
1. **标题错误**: 所有子图标题为"ICU Survival"，但结局应为in-hospital mortality（住院期间生存）。若使用ICU survival，则与论文primary outcome不一致；若应改为hospital survival，需重新计算。
2. **数据错误**: 基于旧结局。当前KM曲线显示的是ICU存活曲线，其基线患病率约13.7%，分层效果较in-hospital mortality更弱。

**P2问题**:
- 2×2布局合理，曲线颜色区分度好。
- Log-rank P值标签清晰，不重叠。
- 图例位置合理。

**建议**: 使用 `hospital_expire_flag` 重新计算住院生存曲线；标题改为 "KM Curve: DSI Quartiles → Hospital Survival" 等；或直接使用"In-Hospital Survival"。

---

### 🟡 Fig6: Calibration plots for all models

**文件**: `figures/Fig6_Calibration.png` (4181×2370 px)

**P1问题**:
1. **数据错误**: 基于旧结局。但校准图本身视觉尚可，6子图（2×3）布局合理，尺寸14×8 inches较宽（4181×2370 px），在双栏排版下可能较好。
2. **颜色区分度差**: 所有模型使用深灰/黑色调，难以快速区分不同模型。建议为每个模型分配不同颜色。
3. **标题中无结局信息**: 虽然标题未写ICU，但应明确为"In-Hospital Mortality"。

**P2问题**:
- X/Y轴标签清晰，刻度合理（0-0.40）。
- Brier score和HL P值标注在每个子图标题中，不重叠。

**建议**: 使用修正数据重新生成，为每个模型使用不同颜色，标题明确in-hospital mortality。

---

### 🔴 Fig7: Forest Plot: Multivariate Logistic Regression (Full Model)

**文件**: `figures/Fig7_Forest.png` (2970×1769 px)

**P0问题**:
1. **多重共线性导致可视化崩溃**: 同时纳入SI_mean, MSI_mean, DSI_mean, Age_SI_mean四个高度相关变量（r>0.85），造成系数符号反转和巨大OR值（SI_mean OR=25.87, DSI_mean OR=18.79, MSI_mean OR=0.017）。这种模型在临床预测论文中不宜作为森林图展示，会被审稿人质疑。
2. **X轴尺度严重扭曲**: 因SI_mean OR=25.87且CI上限达246.7，X轴被拉伸到0-200+，导致其他变量（Age OR=1.0, Male OR=1.09）的点几乎重合在左侧，误差棒几乎不可见。
3. **可读性差**: 标签文字在右侧远端，需要读者视线大幅移动。

**P1问题**:
- 配色方案简单，但变量排序不够直观（建议按OR大小排序或按临床重要性分组）。

**建议**:
- **最佳方案**: 用 Extended + DSI 模型（主模型）替换Full Model，展示各协变量（Age, Male, CCI, Lactate, WBC, Vasopressor, Surgery, MV, DSI_mean）的OR。
- 或从主论文中移除Fig7，改为Table 7；将原图放入Supplementary。
- 对数尺度X轴（log OR）可减少尺度问题。

---

### 🟡 Fig8: Subgroup ROC curves by acute abdomen subtype

**文件**: `figures/Fig8_Subgroup_ROC.png` (4770×1170 px)

**P1问题**:
1. **关键亚型缺失**: 图中只显示 perforation, obstruction, other 三个亚型，缺少 **inflammation** 和 **ischemia**。论文Results 3.11重点讨论的是ischemia (n=353, mortality 40.5%) 和 perforation (n=334)，inflammation也有37.5%的样本。缺少这两个亚型使图无法支撑论文讨论。
2. **图片比例过宽**: 4770×1170 px (约4:1)，在论文单栏中会被压缩得很小，在双栏中也会显得狭长。建议改为2×3或3×2布局。
3. **图例文字过小**: 每个子图图例字体小，在印刷后可能难以辨认。
4. **颜色辨识度**: 在 obstruction 等面板中，橙色和蓝色曲线较接近，难以区分。

**P2问题**:
- 标题简洁清晰。
- 各子图均有参考对角线。

**建议**: 重新生成包含5个亚型的子图（2行3列，最后一格留空或合并图例），调整图例大小和颜色对比度。

---

### 🔴 Fig9: Cumulative Incidence Function: ICU Death by DSI Quartile

**文件**: `figures/Fig9_CIF.png` (2400×1800 px)

**P0问题**:
1. **标题错误**: 应为 "Cumulative Incidence of In-Hospital Death" 而非 ICU Death。
2. **Y轴超出100%**: 图中Q4曲线在30天时达到约115%，这在科学上不可能。Cumulative incidence function must be bounded [0, 1] (0-100%)。这是CIF计算代码的bug：直接累加 `1/n_at_risk` 而没有乘以overall survival product。
3. **数据错误**: 基于旧结局 `icu_death`。

**P1问题**:
- 颜色渐变合理（Q1深蓝到Q4深红）。
- 步进曲线样式可接受，但线条过于粗糙（阶梯过多），可平滑处理。

**建议**:
- 修正CIF计算: `CIF(t) = Σ_{t_j ≤ t} (d_j / n_j) × S(t_j-)`，其中 S 为overall survival Kaplan-Meier product。
- 将Y轴上限设为100%。
- 使用 `hospital_expire_flag` 重新计算，并将competing event定义为discharge alive。
- 标题改为 "Cumulative Incidence of In-Hospital Death by DSI Quartile"。

---

### 🔴 Fig10: ROC Curves: Extended Models for ICU Mortality Prediction

**文件**: `figures/Fig10_ROC_extended.png` (2400×1800 px)

**P0问题**:
1. **标题错误**: "ICU Mortality Prediction" 应改为 "In-Hospital Mortality Prediction"。
2. **数据错误**: 虽然AUC值 (0.626, 0.765, 0.773, 0.777) 与修正后数值接近，但图仍由旧脚本生成，不能确保完全匹配修正后的bootstrap optimism-corrected值。

**P2问题**:
- 4条曲线颜色区分度好，图例清晰。
- 布局合理。

**建议**: 使用修正数据和修正后的模型重新生成，标题改为in-hospital mortality。

---

## 关键根因分析

1. **脚本数据源未更新**: `advanced_statistical_analysis.py` 读取 `analysis_dataset.csv`（旧数据），`comprehensive_analysis.py` 读取 `analysis_dataset_extended.csv`（旧数据，含错误的 `icu_death`/`hospital_death`）。修正后的数据集 `analysis_dataset_corrected.csv` 没有被任何作图脚本使用。
2. **结局变量未统一**: 所有脚本以 `icu_death` 为结局，而非修正后的 `hospital_expire_flag`。
3. **CIF算法错误**: `comprehensive_analysis.py` 第421-425行的CIF实现遗漏了overall survival product，导致累积发病率可超过100%。
4. **多重共线性未处理**: Fig7的Full Model同时纳入4个高度相关的SI衍生指标，这是森林图崩溃的根本原因。

---

## 优先级修复清单

| 优先级 | 图号 | 问题 | 修复方式 |
|--------|------|------|----------|
| P0 | Fig1 | 缺少complete cases最后一步 | 添加box和exclusion |
| P0 | Fig2 | 标题/数据错误 | 使用修正数据重新生成 |
| P0 | Fig3 | 标题/数据错误 | 使用修正数据重新生成 |
| P0 | Fig4 | RCS平线/数据错误 | 修正数据、调整Y轴、检查样条实现 |
| P0 | Fig5 | 标题/数据错误 | 使用hospital_expire_flag重新生成 |
| P0 | Fig7 | 多重共线性/尺度崩溃 | 改为Extended+DSI模型森林图 |
| P0 | Fig9 | Y轴>100%/数据错误 | 修正CIF计算、重绘 |
| P0 | Fig10 | 标题/数据错误 | 使用修正数据重新生成 |
| P1 | Fig6 | 数据/颜色错误 | 使用修正数据、改用不同颜色 |
| P1 | Fig8 | 缺少亚型/比例过宽 | 增加亚型、改为2×3布局 |

---

## 建议操作

**必须重新生成全部10张图**，建议编写新的统一作图脚本 `generate_figures_corrected.py`，以 `analysis_dataset_corrected.csv` 为输入，使用 `hospital_expire_flag` 为primary outcome，并修正上述所有P0/P1问题。

**完成后验证**:
- 所有标题包含 "In-Hospital Mortality" 或 "Hospital" 字样，不含 "ICU Mortality"。
- Fig1包含n=5,728的最终complete cases box。
- Fig4 RCS曲线显示明显的单调上升趋势，Y轴范围合理。
- Fig7 Forest Plot使用Extended+DSI模型，X轴尺度在0.1-50之间（或log scale）。
- Fig9 CIF Y轴上限为100%。
- Fig8包含5个亚型（inflammation, obstruction, perforation, ischemia, other）。
