# 论文数据来源与文献一致性核查报告

**核查日期**: 2026-07-08  
**核查范围**: SCI_paper_v3.md 全部数据声明、参考文献、方法学一致性

---

## 一、致命级问题 (P0 — 必须修正，否则无法投稿)

### 1.1 数据来源错误：MIMIC-IV总入院数

| 项目 | 论文声称 | 实际数据 | 偏差 |
|------|---------|---------|------|
| MIMIC-IV总入院数 | **431,211** | **546,028** | ❌ 差115K！ |

**原因**: 431,211来自MIMIC-IV **v2.2** (431,231)，而我们用的是v3.1。v3.0/v3.1新增了2020-2022年数据，总入院数增至546,028。论文引用了旧版本数字。

**修正**: 所有"431,211"改为"546,028"。Flowchart及Methods中的数字均需同步修改。

### 1.2 数据覆盖年份错误

| 项目 | 论文声称 | 实际数据 | 偏差 |
|------|---------|---------|------|
| 数据年份 | **2008-2023** | **2008-2022** | ❌ 错 |

**修正**: Methods 2.1中"between 2008 and 2023"改为"between 2008 and 2022"。

### 1.3 hospital_death = icu_death (数据处理错误)

| 项目 | 实际值 |
|------|--------|
| ICU死亡与住院死亡100%相等 | ❌ 不合理 |

**问题**: 数据中icu_death与hospital_death完全一致（1398/8933, 15.65%），100%匹配。在真实MIMIC-IV数据中，住院死亡率应高于ICU死亡率（部分患者ICU出院后仍在住院期间死亡）。

**原因**: process_data_v2.py中hospital_death可能被错误地直接从icu_death复制，或使用了admissions表的hospital_expire_flag但只针对ICU患者做了错误的筛选。

**修正**: 重新从admissions表正确提取hospital_expire_flag，确保住院死亡率≠ICU死亡率。

### 1.4 全数据集与complete case数据集混用

论文声称主要分析基于**5,723 complete-case ICU stays**，但论文中的描述性统计使用了**全数据集8933**的数字：

| 统计量 | 论文声称 | 全数据8933 | CC 5728 | 实际来自 |
|--------|---------|-----------|---------|---------|
| Vasopressor use | 32.3% | 32.25% ✓ | 43.61% ❌ | 全数据 |
| Mechanical ventilation | 39.9% | 39.85% ✓ | 52.50% ❌ | 全数据 |
| Surgery | 65.2% | 65.20% ✓ | 67.44% ❌ | 全数据 |
| Median WBC | 10.5 | — | 11.6 ❌ | ? |
| Mean age | 67.0 | 67.0 ✓ | 66.7 ❌ | 全数据 |

**问题**: 论文Section 3.1声称"Among 5,723 complete-case ICU stays...vasopressor use: 32.3%; mechanical ventilation: 39.9%"，但这些百分比来自全数据集而非CC。CC中vasopressor=43.61%，MV=52.50%，差异巨大（>10%）。

**原因**: 因lactate缺失导致的CC筛选偏向——有lactate数据的患者更危重（需动脉血气监测），因此vasopressor/MV使用率更高。

**修正**: 论文必须在Results 3.1中使用CC数据集的描述性统计，或在方法中说明Table 1来自全数据集而模型分析来自CC。

### 1.5 DSI quartile使用全数据集而非CC

| Quartile | 论文N | 论文死亡率 | CC实际N | CC实际死亡率 |
|----------|-------|-----------|---------|-------------|
| Q1 | 2,234 | 7.9% | 1,432 | **12.1%** |
| Q2 | 2,233 | 10.5% | 1,432 | **14.5%** |
| Q3 | 2,233 | 15.5% | 1,432 | **20.3%** |
| Q4 | 2,233 | 28.7% | 1,432 | **32.8%** |

**问题**: 论文的DSI quartile表格（Section 3.2）使用全数据8933的quartile分组和死亡率，但所有AUC/NRI/IDI分析来自CC 5728。两组的quartile cutoff不同，死亡率也不同。

**影响**: 7.9%→28.7%的梯度声称来自8933全数据，但CC中为12.1%→32.8%。两者都是显著的梯度，但数值不一致。

**修正**: 统一使用CC 5728的数据生成DSI quartile表格，或明确说明quartile表格来自全数据集描述而模型来自CC。

### 1.6 Complete case样本量偏差

| 项目 | 论文 | 实际 | 偏差 |
|------|------|------|------|
| Complete cases | 5,723 | **5,728** | +5 |

**原因**: 可能是comprehensive_analysis.py中WBC清洗（去除>100值）导致5行差异。

**修正**: 重新核实exact CC样本量，统一使用一致数字。

---

## 二、参考文献严重错误 (P0 — 必须修正)

### 2.1 引用[2]: 虚构文献

**论文声称**: Cervero F, Laird JM. Understanding the signaling mechanisms of visceral pain: from basic science to clinical applications. Curr Opin Pharmacol. 2023;23:1-7.

**实际情况**: Cervero & Laird发表的是"Understanding the signaling and transmission of visceral nociceptive events"在**J Neurobiol 2004;60(1-3):10-18**，非Curr Opin Pharmacol 2023。Fernando Cervero已于2015年去世，不可能有2023年新作。

**状态**: ❌ **标题、期刊、年份、卷号页码全部错误，疑似虚构**

### 2.2 引用[5]: 无法验证的DSI起源文献

**论文声称**: Rau CS, Wu SC, Chien PC, et al. Diastolic shock index is more sensitive than shock index in identifying hemorrhage: a retrospective cohort study. Am J Emerg Med. 2024;42:15-21.

**实际情况**: 多轮搜索未找到此文献。DSI (HR/DBP)实际上最早由**Ospina-Tascon et al.**在2020年系统研究（Ann Intensive Care 2020;10:41, DOI:10.1186/s13613-020-00658-8）。

**状态**: ❌ **可能虚构/无法验证。DSI起源归因错误。**

### 2.3 引用[4]: 期刊和年份错误

**论文声称**: Liu YC, Su HY, Lee CT, et al. Modified shock index is more sensitive than shock index in septic patients. Am J Emerg Med. 2023;41:75-80.

**实际情况**: Liu YC的休克指数sepsis论文发表在**J Emerg Med (JEM-Journal)** 2024年2月，DOI:10.1016/j.jemermed.2023.10.017，标题为"Relationship between shock index, modified shock index, and age shock index and 28-day mortality among patients with prehospital septic shock"。期刊缩写不同（Am J Emerg Med ≠ J Emerg Med），年份不同（2023→2024），标题也不完全匹配。

**状态**: ❌ **期刊、年份、标题均有偏差**

### 2.4 引用[6]: 无法验证

**论文声称**: King RW, Plewa MC, Buderer NMF, et al. Shock index as a predictor of mortality in elderly trauma patients. J Emerg Med. 2020;58(4):575-582.

**实际情况**: 多轮搜索未找到此文献。J Emerg Med 2020年58卷4期的内容无法确认包含此文。

**状态**: ❌ **可能虚构/需要更精确验证**

### 2.5 引用[11]: 年份和卷号错误

**论文声称**: Steyerberg EW, Vergouwe Y. Towards better clinical prediction models: seven steps for development and an ABCD for validation. Eur Heart J. 2025;36(2):215-228.

**实际情况**: 实际发表在**Eur Heart J 2014;35(29):1925-1931**, DOI:10.1093/eurheartj/ehu207。

**状态**: ❌ **年份错（2025→2014），卷号错（36→35），页码错**

### 2.6 引用[13]: 标题和年份错误

**论文声称**: Desquilbet L, Mariotti F. Flexible regression models for restricted cubic splines in epidemiologic studies. Am J Epidemiol. 2017;186(2):225-233.

**实际情况**: 实际标题为"Dose-response analyses using restricted cubic spline functions in **public health** research"，发表在**Am J Epidemiol 2010;172(12):1377-1385**（初版）或2017年勘误版。DOI:10.1093/aje/kwx029是正确的，但原文是2010年发表。

**状态**: ❌ **标题错，年份错（2017→2010），卷号错（186→172）**

---

## 三、严重问题 (P1 — 强烈建议修正)

### 3.1 亚型分布数据不一致

| 亚型 | 论文 | 全数据8933 | CC 5728 |
|------|------|-----------|---------|
| Inflammation | 41.6% | 39.8% ❌ | 37.5% ❌ |
| Other | 34.2% | 32.7% ❌ | 29.9% ❌ |
| Obstruction | 17.2% | 18.2% ❌ | 20.6% ❌ |
| Perforation | 3.9% | 4.7% ❌ | 5.8% ❌ |
| Ischemia | 3.2% | 4.7% ❌ | 6.2% ❌ |

**论文声称**: "Subtype distribution: inflammation (41.6%), other (34.2%), obstruction (17.2%), perforation (3.9%), ischemia (3.2%)"

**问题**: 无论全数据还是CC，都不完全匹配论文数字。论文中的百分比似乎介于两者之间，可能是手工编辑时引入的错误。

### 3.2 缺血亚型死亡率使用全数据而非CC

**论文声称**: Ischemia mortality 39.5%
- 全数据: 39.5% ✓
- CC: 40.5% ❌

**论文声称**: Perforation mortality 27.9%
- 全数据: 27.9% ✓
- CC: 28.1% ❌

**问题**: 论文Results中交替使用全数据和CC的死亡率，未明确标注数据来源。

### 3.3 DSI quartile中lactate/vasopressor/surgery值与CC不符

| Quartile | 论文Lac | CC Lac | 论文Vaso | CC Vaso | 论文Surg | CC Surg |
|----------|--------|--------|----------|---------|----------|---------|
| Q1 | 1.5 | **1.7** ❌ | 16.8% | **27.6%** ❌ | 57.5% | **60.5%** ❌ |
| Q2 | 1.8 | **1.9** | 22.5% | **39.2%** ❌ | 62.0% | **64.7%** |
| Q3 | 2.1 | **2.0** | 33.1% | **47.3%** ❌ | 67.3% | **70.5%** ❌ |
| Q4 | 3.2 | **2.6** ❌ | 56.9% | **60.3%** | 72.7% | **74.1%** |

**问题**: Vasopressor差异最大（Q2: 22.5% vs 39.2%，差16.7个百分点）。论文使用全数据集8933的quartile统计，但这些患者中部分没有lactate/vasopressor数据，导致百分比偏低。

### 3.4 论文声称CC死亡率19.9% (n=1,139)

- CC实际: 5,728 × 19.92% = **1,141 deaths**
- 论文声称: 5,723 × 19.9% = **1,139 deaths**
- 差异: 2 deaths, 5 patients

### 3.5 年龄IQR

| 项目 | 论文 | 全数据 | CC |
|------|------|--------|-----|
| Age IQR | 57-79 | 57-80 ❌ | ? |

---

## 四、已验证正确的数据 ✓

| 统计量 | 论文 | 实际 | 状态 |
|--------|------|------|------|
| Acute abdomen ICD匹配 | 72,676 | 72,676 | ✓ |
| CC ICU死亡率 | 19.9% | 19.92% | ✓ (四舍五入) |
| CC男性比例 | 56.1% | 56.0% | ✓ (近似) |
| CC lactate median | 2.0 | 2.0 | ✓ |
| Extended baseline AUC | 0.765 | 0.7649 | ✓ |
| Extended+DSI AUC | 0.773 | 0.7732 | ✓ |
| Extended+all SI AUC | 0.777 | 0.7767 | ✓ |
| DSI NRI | 0.038 | 0.0382 | ✓ |
| DSI IDI | 0.017 | 0.0166 | ✓ (近似) |
| IDI P | <10⁻¹³ | 4.19×10⁻¹³ | ✓ |
| Bootstrap optimism ≤0.003 | ≤0.003 | 0.001-0.003 | ✓ |
| Sensitivity: Non-surgical N | 1,865 | 1,865 | ✓ |
| Sensitivity: Non-surgical AUC | 0.804 | 0.804 | ✓ |
| Sensitivity: Ischemia N | 418 | 418 | ✓ (全数据) |

### 已验证正确的参考文献 ✓

| 编号 | 文献 | 状态 |
|------|------|------|
| [3] | Allgöwer & Burri 1967 DMW | ✓ |
| [9] | Johnson AEW MIMIC-IV Sci Data 2023 | ✓ |
| [10] | Charlson CCI J Chronic Dis 1987 | ✓ |
| [14] | von Elm STROBE Lancet 2007 | ✓ |
| [15] | Fine & Gray JASA 1999 | ✓ |
| [16] | DeLong Biometrics 1988 | ✓ |
| [17] | Pencina NRI Stat Med 2008 | ✓ |
| [18] | Hou MSI Front Cardiovasc Med 2022 | ✓ |
| [12] | Vickers DCA Med Decis Making 2006 | ✓ |

---

## 五、方法论一致性检查

### 5.1 NRI计算方法

论文声称NRI使用"risk categories <5%, 5-15%, >15%" [17]，但comprehensive_analysis.py中实际使用threshold=0.5（50%）进行二分类NRI计算。**❌ 方法描述与实际计算不一致**

**修正**: (a) 改用3-category NRI (5%/15%阈值) 重新计算，或(b) 将论文方法描述改为"binary NRI at 50% threshold"。

### 5.2 Fine-Gray竞争风险

论文声称"Fine-Gray subdistribution hazard model"，但comprehensive_analysis.py实际使用**logistic regression approximation**。代码注释明确说"For proper Fine-Gray, we need lifelines; use multivariable logistic as proxy"。

**状态**: 论文Limitations 4.4(4)已承认这一局限，但Results 3.10中"Fine-Gray subdistribution hazard approximation"的OR=5.34来自logistic回归而非真正的Fine-Gray模型。**需在Results中明确标注"approximation"**。

### 5.3 36%排除率声明

论文Limitations称"36% exclusion rate for incomplete extended covariates"。实际: (8933-5728)/8933 = **36.0%** ✓。但论文说5,723而非5,728。

---

## 六、修正建议优先级排序

### P0 (必须立即修正，否则无法投稿)

1. **修正MIMIC-IV总入院数**: 431,211 → 546,028
2. **修正数据年份**: 2008-2023 → 2008-2022
3. **修正hospital_death**: 重新从admissions表提取，确保≠icu_death
4. **修正参考文献[2]**: 替换为真实文献或删除
5. **修正参考文献[5]**: 替换为Ospina-Tascon 2020或删除Rau CS虚构文献
6. **修正参考文献[11]**: 2025→2014, 36(2)→35(29), 215-228→1925-1931
7. **修正参考文献[13]**: 标题修正, 2017→2010, 186→172
8. **统一数据来源**: 决定使用CC 5728还是全数据8933，所有表格使用同一数据集

### P1 (强烈建议修正)

9. **修正参考文献[4]**: 核实真实Liu YC论文的准确标题/期刊/年份
10. **验证参考文献[6]**: 确认King RW文献是否存在
11. **修正CC样本量**: 5,723 → 5,728 (或重新统一)
12. **修正DSI quartile表格**: 使用CC数据而非全数据
13. **修正vasopressor/MV/surgery百分比**: 使用CC而非全数据
14. **修正亚型分布**: 使用一致数据集的准确百分比
15. **修正NRI方法描述**: 与实际计算方法一致
16. **修正WBC median**: 10.5 → 11.6 (CC) 或确认全数据值

### P2 (建议改进)

17. **明确标注数据来源**: 每个表格标注N来自CC还是全数据
18. **补充selection bias讨论**: lactate缺失导致CC偏向更危重患者
19. **年龄IQR**: 核实57-79 vs 57-80
20. **添加lactate覆盖率**: CC中100% (by design)，但全数据64.6%
