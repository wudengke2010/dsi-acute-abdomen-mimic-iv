# 四篇外刊论文对v8质量提升建议

## 论文概要

| # | 论文 | 期刊 | 年份 | 人群 | N | 结局 | 核心方法 | 核心结果 |
|---|------|------|------|------|---|------|----------|----------|
| 1 | Althunayyan — SI/MSI脓毒症筛查 | JIPH (IF~3.0) | 2019 | ED发热患者 | 274 | 脓毒症/28天死亡 | SI/MSI cut-off敏感性/特异性 | MSI≥1 Se=90%脓毒症; 仅5例死亡 |
| 2 | Zhang — 腹腔脓毒症预测模型 | BMJ Open (IF~3.5) | 2025 | IAS ICU(MIMIC-IV+eICU) | 1,300/149 | 住院死亡 | LASSO→nomogram→DCA+CIC | AUC=0.795/0.846; SOFA AUC=0.622 |
| 3 | Luo — 腹腔感染ICU死亡风险 | Frontiers Med (IF~4.0) | 2022 | IAI ICU(中国单中心) | 476 | 28天死亡 | Cox回归→SOFA+慢性病+血球压积 | SOFA HR=1.285; 慢性病HR=3.14 |
| 4 | Jeon — SI/DSI脓毒症休克预测 | AJEM (IF~2.7) | 2024 | ED脓毒症(韩国) | 1,267 | 脓毒症休克进展 | SI+DSI PCA tertile→aOR | DSI AUC=0.717; SI AUC=0.707(P=0.14) |

---

## 引用价值评估

### ⭐⭐⭐ 必须引用(2篇)

#### 1. Zhang 2025 BMJ Open — 腹腔脓毒症预测模型
**引用理由**:
- **同疾病领域**: intra-abdominal sepsis/infection → 与v8急腹症直接重叠
- **同数据库**: MIMIC-IV + eICU → 与v8完全相同的双数据库来源
- **同结局**: in-hospital mortality → 与v8 primary outcome一致
- **直接竞争模型**: Zhang的nomogram(AUC=0.795) vs v8的Extended+DSI(AUC=0.790) → 方法对比必须在Discussion中
- **关键差异**: Zhang不包含血流动力学变量(无BP/SI/DSI), 而v8以DSI为核心 → 这是v8的独特价值点
- **方法学启示**: LASSO变量选择、nomogram可视化、CIC → v8缺少这三项
- **eICU验证对比**: Zhang eICU N=149(33死) vs v8 eICU N=5,755(1,151死) → v8验证远为更强

**引用位置**: §4.2 Comparison with Previous Studies

**建议引用文本**:
> Zhang et al. [ref] developed a nomogram for IAS in-hospital mortality using LASSO-selected variables (lactate, age, APTT, BUN, TBIL, platelets; AUC=0.795) from the same MIMIC-IV database. Their model excluded hemodynamic parameters, relying solely on laboratory markers and age. In contrast, DSI provides zero-cost bedside risk stratification from routine vitals—available within seconds, before laboratory results. Notably, their eICU validation cohort (N=149, 33 deaths) was substantially smaller than ours (N=5,755, 1,151 deaths), limiting calibration assessment.

#### 2. Jeon 2024 AJEM — DSI/SI脓毒症休克预测
**引用理由**:
- **直接DSI研究**: 使用DSI预测脓毒症休克进展 → 与v8核心指标完全相同
- **ED triage场景**: DSI在ED可用 → 强化v8"zero-cost bedside tool"定位
- **关键发现**: DSI AUC=0.717, SI AUC=0.707(DeLong P=0.14, **无显著差异**) → v8应坦诚承认此nuance
- **PCA tertile分类**: Jeon用PCA合并SI+DSI → 创新方法，v8可提及作为替代
- **升压药关联**: DSI tertile与升压药剂量/时间显著相关 → 支持v8的"血流动力学严重程度标志"论述
- **地域多样性**: 韩国ED数据 → 增加v8地域覆盖面

**引用位置**: §4.2 Comparison with Previous Studies + §4.1 Pathophysiology(升压药关联)

**建议引用文本**:
> Jeon et al. [ref] evaluated DSI for predicting septic shock progression at ED triage (N=1,267, Korea), reporting DSI AUC=0.717 vs SI AUC=0.707 (DeLong P=0.14, non-significant). While DSI and SI showed similar discrimination for shock prediction, DSI tertile stratification correlated with vasopressor dose and time to initiation—supporting the hemodynamic severity interpretation central to our acute abdomen findings. The ED triage context further validates DSI's zero-cost bedside applicability.

### ⭐⭐ 建议引用(1篇)

#### 3. Luo 2022 Frontiers — 腹腔感染ICU死亡风险因素
**引用理由**:
- **中国单中心IAI数据**: 提供v8缺乏的中国真实世界数据
- **SOFA验证**: HR=1.285 → 与v8 SOFA OR=1.16一致(不同方法/人群但方向一致)
- **慢性病影响**: HR=3.14 → 支持v8的CCI OR=1.14
- **死亡梯度**: 3.5%→7.6%→30.9%(感染→脓毒症→休克) → 与v8 DSI梯度12.1%→32.8%概念对应
- **血球压积**: HR=1.099 → v8未纳入此变量，可讨论
- **治疗趋势**: 后4年死亡率下降(20.3%→12.9%) → 与v8 MIMIC-IV时间跨度(2008-2022)相关

**引用位置**: §4.2 Comparison + §4.4 Limitations(缺乏微生物学数据)

**建议引用文本**:
> Luo et al. [ref] identified SOFA (HR=1.285) and underlying chronic diseases (HR=3.14) as independent risk factors for 28-day mortality in Chinese ICU IAI patients (N=476), consistent with our findings. Their single-center Chinese data complement our US-derived MIMIC-IV/eICU results, though geographic and practice-pattern differences limit direct comparison.

### ⭐ 有限价值(1篇)

#### 4. Althunayyan 2019 JIPH — SI/MSI脓毒症筛查
**引用理由有限**:
- 样量极小(N=274, 仅5例死亡) → 统计可靠性不足
- 聚焦脓毒症筛查(Se/Sp/NPV/PPV)而非死亡率预测 → 与v8目标不同
- MSI为主(SI为辅)，无DSI → 与v8核心指标不符
- **唯一价值**: 提示SI derivatives在ED triage的筛查角色

**是否引用**: 可在§4.2简要提及，但非必须。如引用，强调其ED triage筛查定位(与v8的ICU死亡率预测定位不同)

---

## P0级质量提升建议(5项)

### P0-1: 添加Nomogram临床决策支持工具 ⭐⭐⭐ 最高优先级

**缺口**: v8仅提供DSI quartile阈值(Q1<1.279, Q4>1.762)作为临床参考，缺乏可视化决策工具。Zhang 2025 BMJ Open提供完整的nomogram(lactate+age+APTT+BUN+TBIL+platelets)，可直接计算个体死亡概率。

**改进方案**:
1. 创建Extended+DSI模型nomogram(年龄+CCI+lactate+WBC+vasopressor+MV+SOFA+DSI → 个体死亡概率)
2. 同时创建简化版nomogram(age+DSI+SOFA+lactate → 快速 bedside估算)
3. 在Results §3.4后新增"§3.4a Clinical Application: Nomogram"
4. 添加FigS9(Nomogram图)至补充材料
5. 在Discussion §4.3 Clinical Implications中讨论nomogram的应用场景

**AIC限制**: 展示项≤5(当前已5), nomogram需作为FigS9(补充材料), 不计入主文展示项

**参考文献影响**: 引用Zhang 2025 [ref] 的nomogram方法作为模板; +1篇参考文献→35篇

### P0-2: 添加Clinical Impact Curves (CIC) ⭐⭐⭐ 高优先级

**缺口**: v8目前仅有DCA曲线(FigS4), 缺乏CIC。Zhang 2025 BMJ Open同时提供DCA+CIC。CIC显示"每100人中被分类为高风险"与"其中真实阳性"的数量对比——比DCA的"net benefit"更直观，临床决策者更易理解。

**改进方案**:
1. 生成CIC曲线(red=high-risk classified, blue=true positives)在不同风险阈值
2. 将CIC与现有DCA合并为补充材料FigS4(或替换现有DCA)
3. 在Results §3.5 Sensitivity item (8) 中添加CIC描述

**参考文献影响**: 无需新增引用; 仅方法学改进

### P0-3: Discussion中对比Zhang 2025 IAS模型 ⭐⭐⭐ 高优先级

**缺口**: v8 §4.2 Comparison仅讨论Ospina-Tascón(脓毒症休克DSI)和Jouffroy/Liu/Olaussen(SI derivatives综述)，未提及同疾病领域+同数据库的竞争模型。Zhang 2025使用MIMIC-IV+eICU开发IAS预测模型，是v8最直接的方法学对比参照。

**改进方案**:
在§4.2末段新增对比段落:
- Zhang的LASSO选择6变量(无血流动力学) vs v8的预指定+DSI
- Zhang nomogram AUC=0.795 vs v8 Extended+DSI AUC=0.790 → 几乎相同但DSI提供即时性
- Zhang eICU N=149(33死) vs v8 eICU N=5,755(1,151死) → v8验证远更强
- 关键差异: Zhang需要6项实验室结果(APTT/BUN/TBIL/platelets需30-60分钟) vs DSI秒级可用
- 这强化v8的"complementary bedside tool when labs are pending"定位

**参考文献影响**: +1篇(Zhang 2025 BMJ Open) → 35篇

### P0-4: Discussion中讨论Jeon 2024 DSI/SI nuance ⭐⭐ 高优先级

**缺口**: v8定位DSI为"strongest SI derivative"，但Jeon 2024发现DSI vs SI DeLong P=0.14(无显著差异)。v8应坦诚承认这一nuance: DSI在脓毒症休克预测中与SI鉴别力相似，但在急性腹部死亡率预测和组分拆解分析中DSI有独特贡献(matched-stratification)。

**改进方案**:
在§4.2 Comparison中新增段落:
- Jeon DSI AUC=0.717 vs SI AUC=0.707(P=0.14) → DSI/SI鉴别力在休克预测中相似
- 但v8组分拆解显示DSI > HR(0.571)和DBP(0.597), 而SI = HR/SBP(SBP非Windkessel核心变量)
- DBP比SBP更早反映血管张力丧失(§4.1 Windkessel论述)
- Jeon的升压药剂量关联支持DSI的血流动力学严重程度解读
- DSI+SI PCA tertile(Jeon方法) → 未来方向

**参考文献影响**: +1篇(Jeon 2024 AJEM) → 36篇

### P0-5: 讨论LASSO变量选择作为替代方法 ⭐⭐ 中高优先级

**缺口**: v8使用临床预指定协变量(age/sex/CCI/lactate/WBC/vasopressor/MV/SOFA)，未讨论数据驱动的变量选择方法。Zhang 2025使用LASSO+10-fold CV选择最优变量集。两种方法各有优势:v8预指定保证临床可解释性和跨数据集一致性; LASSO可能发现非预期预测因子但依赖特定数据集特征。

**改进方案**:
在§4.4 Limitations末或§4.5 Future Directions中添加:
- 预指定vs LASSO变量选择的方法学差异
- 预指定优势:临床可解释性、跨中心一致性、不依赖数据集特异性
- LASSO优势:客观性、可能发现非预期因子、更简约模型
- 当前预指定方法在SOFA调整后vasopressor(P=0.14)/MV(P=0.45)不显著 → LASSO可能剔除这些变量
- 未来: LASSO/RF变量选择作为补充验证

**参考文献影响**: 通过Zhang 2025引用间接覆盖; 无需新增

---

## P1级质量提升建议(5项)

### P1-1: 补充DSI阈值诊断性能(Se/Sp/PPV/NPV)

**缺口**: v8报告AUC/OR/NRI/IDI，但未报告DSI在临床阈值点的诊断性能。Althunayyan(JIPH)和Jeon(AJEM)均报告了SI/MSI/DSI在各cut-off的Se/Sp/PPV/NPV。对于"zero-cost bedside tool"定位，阈值性能比AUC更实用。

**改进方案**:
1. 计算DSI在以下阈值的Se/Sp/PPV/NPV: 1.0, 1.279(Q1/Q2), 1.502(Q2/Q3), 1.762(Q3/Q4), 2.0
2. 结果加入Table S3(DSI quartile baseline特征)或新Table S12
3. 在Results §3.2简要提及最优Youden指数阈值

**AIC限制**: 补充材料表格不计入展示项限制

### P1-2: 讨论血球压积/凝血作为潜在附加预测因子

**缺口**: Luo 2022发现血球压积(HR=1.099)为独立预测因子; Zhang 2025发现APTT/platelets为独立预测因子(凝血功能障碍)。v8未纳入血球压积或凝血指标。

**改进方案**:
在§4.5 Future Directions或§4.4 Limitations中提及:
- Luo(Frontiers)和Zhang(BMJ Open)发现血球压积/APTT/platelets为IAI独立预测因子
- v8的Extended baseline含WBC但无Hct/APTT/platelets
- 未来: 将凝血和血球压积纳入模型可能提升预测力(Zhang AUC=0.795含platelets/APTT)
- 但v8聚焦即时可用性(Hct/APTT需实验室结果), 与DSI的秒级可用定位不同

### P1-3: 引用Luo 2022 Frontiers中国IAI数据

**改进方案**: 在§4.2 Comparison新增1-2句:
- Luo et al.在中国单中心IAI(N=476)验证SOFA(HR=1.285)和慢性病(HR=3.14)为独立预测因子
- 与v8的SOFA OR=1.16和CCI OR=1.14方向一致
- 中国数据补充v8的US数据局限

**参考文献影响**: +1篇(Luo 2022 Frontiers) → 37篇

### P1-4: 承认缺乏微生物学数据

**缺口**: Luo 2022和Zhang 2025均报告病原学分布(E. coli/Klebsiella/Enterococcus/Candida)。v8完全缺乏微生物学数据(MIMIC-IV微生物学数据提取复杂，且ICD代码不包含病原学信息)。

**改进方案**:
在§4.4 Limitations item (1)中添加:
- v8缺乏病原学数据(微生物培养/耐药模式), Luo [ref]和Zhang [ref]显示Enterococcus和真菌感染与IAI死亡独立相关
- 未来: 整合病原学数据可能提升亚型特异性预测

### P1-5: 讨论DSI vs SI差异的上下文依赖性

**缺口**: Jeon发现DSI vs SI P=0.14(脓毒症休克预测)，v8发现DSI为"strongest" SI derivative。差异可能取决于:
- 预测目标(休克进展vs死亡率)
- 人群(脓毒症vs急性腹部)
- 时间窗口(ED triage单次vs ICU 24h mean)

**改进方案**: 在§4.2 Comparison中明确指出DSI/SI鉴别力差异是上下文依赖的，v8急性腹部ICU场景下DSI通过组分拆解展示了独特贡献(§3.3 matched-stratification)，这在脓毒症休克ED triage场景中未被Jeon评估。

---

## P2级质量提升建议(3项)

### P2-1: 提及时间趋势分析

Luo 2022比较4年时段(2011-2014 vs 2015-2018)显示死亡率下降(20.3%→12.9%), 与优化抗生素策略和限制液体平衡相关。v8数据跨度2008-2022, 可在Limitations提及未分析时间趋势对DSI预测力的影响。

### P2-2: 提及PCA-based风险分类

Jeon使用PCA合并SI+DSI为单一风险维度(tertile分类)。v8的quartile分类基于DSI alone。PCA方法可能更优(利用SI+DSI的95.74%共同方差), 可在Future Directions中提及。

### P2-3: 简要引用Althunayyan 2019 JIPH

仅在§4.2末段以1句提及SI/MSI在ED triage的筛查价值(与v8的ICU死亡率预测定位区分), 不作重点讨论。

---

## 引用数量影响

| 项目 | 当前v8 | P0建议后 | P1建议后 | AIC限制 |
|------|--------|----------|----------|---------|
| 参考文献 | 34 | **36** | **37** | ≤40 ✅ |
| 正文 | 3,499词 | ~3,600词 | ~3,650词 | ≤4,000 ✅ |
| 主展示项 | 5 | 5(不变) | 5(不变) | ≤5 ✅ |
| 补充表 | S1-S8+FigS1-S8 | +S9-S12 | +S12 | 无限制 ✅ |

### 新增参考文献清单

| 编号 | 论文 | 引用优先级 |
|------|------|-----------|
| [35] | Zhang J, Chen Y, Zhao C, et al. Development and validation of a prediction model for in-hospital mortality in patients with intra-abdominal sepsis: a dual-database study using MIMIC-IV and eICU databases. BMJ Open. 2025;15:e102971. | P0-3 ⭐⭐⭐ |
| [36] | Jeon Y, Kim S, Ahn S, et al. Predicting septic shock in patients with sepsis at emergency department triage using systolic and diastolic shock index. Am J Emerg Med. 2024;78:196-201. | P0-4 ⭐⭐⭐ |
| [37] | Luo X, Li L, Ou S, et al. Risk Factors for Mortality in Abdominal Infection Patients in ICU: A Retrospective Study From 2011 to 2018. Front Med. 2022;9:839284. | P1-3 ⭐⭐ |

---

## v8与4篇论文的核心对比表

| 特征 | v8 (我们的论文) | Zhang 2025 BMJ Open | Jeon 2024 AJEM | Luo 2022 Frontiers | Althunayyan 2019 JIPH |
|------|-----------------|---------------------|----------------|---------------------|----------------------|
| 疾病 | 急腹症(全亚型) | 腹腔脓毒症(IAS) | 脓毒症(ED) | 腹腔感染(IAI) | 发热→脓毒症 |
| 数据库 | MIMIC-IV+eICU | MIMIC-IV+eICU | 韩国单中心 | 中国单中心 | 沙特单中心 |
| 样量 | 5,728/5,755 | 1,300/149 | 1,267 | 476 | 274 |
| 死亡率 | 19.9%/20.0% | 20.3%/22.2% | — | 16.0%(28天) | 1.8%(28天) |
| 核心指标 | DSI | nomogram(6变量) | SI+DSI PCA | SOFA+慢性病 | SI+MSI |
| 变量选择 | 预指定 | LASSO | PCA tertile | Cox stepwise | cut-off |
| Best AUC | 0.790 | 0.795/0.846 | 0.717 | —(Cox) | 0.913(筛查) |
| 组分拆解 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 外部验证 | ✅(208医院) | ✅(N=149) | ❌ | ❌ | ❌ |
| Nomogram | ❌→应添加 | ✅ | ❌ | ❌ | ❌ |
| CIC | ❌→应添加 | ✅ | ❌ | ❌ | ❌ |
| DCA | ✅ | ✅ | ❌ | ❌ | ❌ |
| 病原学 | ❌ | 部分 | ❌ | ✅ | ❌ |
| Se/Sp/NPV/PPV | ❌→应添加 | ❌ | ❌ | ❌ | ✅ |
