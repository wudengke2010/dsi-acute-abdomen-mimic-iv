# WJES 已发表论文精读报告（4篇）

> 目的：为 DSI 急腹症论文转投 World Journal of Emergency Surgery 提供格式、结构、写作范式与引用策略参考。

---

## 一、四篇论文概览

| # | 论文 | 年份/卷期 | 设计 | 样本 | 核心结果 | 审稿周期 |
|---|------|----------|------|------|----------|----------|
| 1 | **Jung et al.** qSOFA+乳酸预测腹腔感染死亡率 | 2018; 13:14 | 单中心回顾性（韩国延世大学） | n=457，ED急诊胃肠手术的复杂性腹腔感染 | qSOFA+乳酸 AUROC 0.754 vs qSOFA 0.717 (p=0.039)；与全SOFA 0.795相当 (p=0.127) | 1/29投稿→3/5接收（**5周**） |
| 2 | **Sartelli et al.** PIPAS 研究（WSES） | 2019; 14:34 | 全球多中心观察性（153中心/56国） | n=3,137 急性腹膜炎 | PIPAS Severity Score（10变量床旁预警分）：0-1分死亡率2.9% → 7-8分86.7% | WSES旗舰研究 |
| 3 | **Koch et al.** qSOFA/SOFA/SIRS预测外科IMCU/ICU感染与死亡 | 2020; 15:63 | 单中心6年队列（德国Giessen） | n=13,780 | qSOFA在IMCU最优（AUC 0.82）；SOFA在ICU/IMCU最优（0.73）；均无法预测疑似感染 | — |
| 4 | **Park et al.** AI集成模型预测术后危重患者死亡+ prolonged ICU stay | 2025; 20:79 | 双中心回顾性（韩国）+外部验证 | n=6,029（A中心3,478/B中心2,551） | 集成模型死亡预测 AUROC 0.881（内部）/0.833（外部）；**SHAP：舒张压为关键预测因子** | 7/15投稿→9/15接收（**2个月**） |

**四篇共同主题**：床旁/简单工具在外科急腹症与危重患者中的预后价值 —— 与本文DSI定位完全同频。

---

## 二、WJES 论文结构范式（四篇一致）

### 1. 标题
- 描述性 + 设计后缀："a retrospective study" / "a WSES observational study"
- 本文标题已有 "A Retrospective Cohort Study with External Validation" ✅

### 2. 结构化摘要（Background / Methods / Results / Conclusions）
- Jung 2018 约230词；Koch 2020 约260词；Park 2025 约280词；Sartelli 2019 约280词
- 本文349词（≤350）✅，四段式结构完全一致 ✅

### 3. 关键词
- 4–6个，本文5个 ✅

### 4. 正文标题**不编号**
- 一级：Background / Methods / Results / Discussion / Conclusions
- 二级：不加数字（如 "Study population"、"Statistical analysis"、"Baseline characteristics"）
- ⚠️ 本文v8使用编号节（1./2.1/3.4/4.5），与WJES范式不同 → 建议去编号

### 5. Discussion 结构
- 开篇直接总结主要发现（无"主要发现列表"）
- 与既往文献对比段落
- **"Strengths and limitations" 独立小节**（Jung 2018 明确用此标题）
- 临床意义融合在讨论内
- 独立 Conclusions 段（3–5句，简短）
- ⚠️ 本文v8的4.5 Limitations/4.6 Future Directions 拆分偏AIC风格，可合并为 "Strengths and limitations" 一节

### 6. 背面事项顺序（Back matter，以Park 2025最新版为准）
```
Abbreviations（缩略语表）
Supplementary Information（补充材料说明+Additional file清单）
Acknowledgements
Author contributions（非 CRediT 术语，用叙述式）
Funding
Data availability
Declarations
  - Ethics approval and consent to participate
  - Consent for publication
  - Competing interests
Author details（各作者完整单位）
References
```
- ⚠️ 本文v8的Declarations子标题顺序/命名基本兼容（Data availability✅、Competing interests✅、Ethics approval✅），但顺序可在终稿排版时微调
- ⚠️ WJES用叙述式 "Author contributions"（非CRediT分项），本文现有CRediT格式也可接受

### 7. 参考文献（Springer Basic风格）
- 编号制；作者 ≤6全列或 "et al."；期刊缩写；年;卷(期):页码
- 本文40条格式接近 ✅（含DOI，Springer接受）

### 8. 方法学金标准表述
- Koch 2020 明确写 "methods and results are presented in accordance with the STROBE guidelines" → 本文已有STROBE清单 ✅，建议在Methods加一句同样表述

---

## 三、关键发现：对本文的直接支撑

### Park 2025 的 SHAP 分析发现**舒张压（diastolic blood pressure）是术后危重患者死亡的关键预测因子之一** —— 
这是对 DSI（HR/DBP）病理生理学前提的**独立、近期、WJES自家期刊**的佐证：
- 建议引用在 Discussion §4.2（病理生理学依据）或 §4.3（与既往研究对比）
- 表述要点：机器学习可解释性分析独立确认DBP的预后权重，间接支持以DBP为分母的DSI价值

### Sartelli 2019 PIPAS 是急腹症/腹膜炎床旁评分的标杆：
- PIPAS需10个变量（含SpO2、血小板、乳酸），DSI仅需2个生命体征
- 建议在Introduction/Discussion对比："PIPAS validated a 10-variable bedside score for acute peritonitis; whether an even simpler vital-sign ratio performs comparably in the broader acute abdomen population remains unknown" —— 正是本文填补的空白

### Jung 2018 同域研究、体量对比悬殊：
- 单中心457例 vs 本文MIMIC-IV 5,728 + eICU 208医院外部验证
- qSOFA+乳酸思路（简单指标增强）与DSI思路平行，Introduction可引用

### Koch 2020 提供"简单评分性能场景依赖"的证据：
- qSOFA在IMCU好、ICU差 → 支持"分层场景需要不同工具"的论证，可用于Discussion

---

## 四、对本文v8的具体修改建议（按优先级）

| 优先级 | 修改项 | 工作量 |
|--------|--------|--------|
| ★★★ | **新增4条WJES引用**（Jung/Sartelli/Koch/Park，编号41–44），分别嵌入Introduction与Discussion §4.2/§4.3 | 小（~120词增量） |
| ★★★ | **Discussion引入Park 2025 SHAP-DBP佐证**（一句即可，强化病理生理学论证） | 小 |
| ★★☆ | **章节去编号**：1. Introduction→Background；2.1→直接小节名；4.5+4.6合并为"Strengths and limitations" | 中 |
| ★★☆ | Methods加一句 STROBE 依照声明（仿Koch 2020） | 极小 |
| ★☆☆ | Back matter顺序按WJES范式微调 | 小 |
| — | 摘要349词/关键词5个/表格嵌入 ✅ 无需改动 | — |
| — | Cover Letter WJES版已就绪 ✅ | — |

**引用格式（Springer Basic）：**
41. Jung YT, Jeon J, Park JY, et al. Addition of lactic acid levels improves the accuracy of quick sequential organ failure assessment in predicting mortality in surgical patients with complicated intra-abdominal infections: a retrospective study. World J Emerg Surg. 2018;13:14.
42. Sartelli M, Abu-Zidan FM, Labricciosa FM, et al. Physiological parameters for Prognosis in Abdominal Sepsis (PIPAS) Study: a WSES observational study. World J Emerg Surg. 2019;14:34.
43. Koch C, Edinger F, Fischer T, et al. Comparison of qSOFA score, SOFA score, and SIRS criteria for the prediction of infection and mortality among surgical intermediate and intensive care patients. World J Emerg Surg. 2020;15:63.
44. Park DJ, Baik SM, Hong KS, et al. Development and external validation of an artificial intelligence model for predicting mortality and prolonged ICU stay in postoperative critically ill patients: a retrospective study. World J Emerg Surg. 2025;20:79.

---

## 五、审稿速度与定位判断

- Jung 2018：投稿到接收 **5周**；Park 2025：**2个月** —— WJES流程快
- 四篇均为"简单工具+外科/腹腔感染人群"录用先例 → 本文（双数据库+外部验证+14项敏感性分析）证据强度高于其中3篇
- 定位话术：**比PIPAS更简单（2 vs 10变量）、比Jung样本大20倍+外部验证、比AI模型更可解释且零成本**
