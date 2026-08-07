# Shock Index衍生指标对急腹症患者ICU转入与院内死亡的预测价值
## ——基于MIMIC-IV v3.1的回顾性队列研究

---

## 1. 研究背景与创新点

### 1.1 现有研究缺口
- Shock Index (SI=HR/SBP) 及衍生指标（MSI=HR/MBP, DSI=HR/DBP, Age-SI）在**创伤、脓毒症**中已有大量研究
- **急腹症（acute abdomen）专项**研究几乎空白——2026版《成人急腹症诊疗急诊专家共识》明确指出早期风险分层是核心挑战
- 尚无基于MIMIC-IV的急腹症Shock Index衍生指标预测研究
- 尚无研究将SI衍生指标与急腹症**亚型**（穿孔型、梗阻型、炎症型）进行分层比较

### 1.2 本研究创新点
1. **人群创新**：首次在MIMIC-IV中聚焦急腹症急诊入院人群
2. **指标创新**：系统比较SI/MSI/DSI/Age-SI四指标，并探索**复合休克指数（Composite Shock Index, CSI）**
3. **分层创新**：按急腹症亚型（穿孔、梗阻、炎症、缺血）进行亚组分析
4. **方法创新**：多终点预测（ICU转入、院内死亡、ICU LOS>3天）+ 决策曲线分析（DCA）

---

## 2. 研究假设

- H1: SI衍生指标（MSI/DSI/Age-SI）较传统SI对急腹症ICU转入和院内死亡具有更高预测效能（AUC）
- H2: CSI（加权复合指标）较单一指标预测效能更优
- H3: 不同急腹症亚型中，各SI衍生指标的预测价值存在差异（穿孔型>梗阻型>炎症型）

---

## 3. 研究设计

### 3.1 类型
单中心回顾性队列研究（Beth Israel Deaconess Medical Center, MIMIC-IV v3.1）

### 3.2 数据来源
MIMIC-IV v3.1（2008-2023年），PostgreSQL概念表 + 原始CSV.gz

---

## 4. 研究人群

### 4.1 纳入标准
- 年龄 ≥ 18岁
- 经急诊入院（admissions.edregtime非空）
- 主诊断或前3位诊断包含急腹症ICD编码（见下表）
- 急诊入院24h内有生命体征记录（HR, SBP, DBP）

### 4.2 接除标准
- 年龄 < 18岁
- 非急诊入院
- 24h内无完整生命体征（缺少HR或SBP或DBP）
- 既往有慢性休克状态（慢性心衰NYHA IV、终末期肾病透析）
- 住院时间 < 6h（信息不充分）

### 4.3 急腹症ICD编码定义

#### ICD-10编码体系
| 亚型 | ICD-10前缀 | 代表疾病 |
|------|-----------|---------|
| 阑尾炎 | K35-K38 | 急性阑尾炎、阑尾穿孔 |
| 胆囊炎/胆道 | K80-K83 | 急性胆囊炎、胆管炎 |
| 胰腺炎 | K85-K86 | 急性胰腺炎 |
| 肠梗阻 | K56 | 肠梗阻、肠套叠 |
| 肠穿孔 | K25-K28(穿孔型), K63.1 | 胃/肠穿孔 |
| 腹膜炎 | K65 | 急性腹膜炎 |
| 肠缺血 | K55.0 | 急性肠缺血 |
| 憩室炎 | K57 | 憩室炎伴穿孔/脓肿 |
| 腹内脓肿 | K67 | 腹内脓肿 |

#### ICD-9编码对应
| 亚型 | ICD-9编码范围 |
|------|------------|
| 阑尾炎 | 540-543 |
| 胆囊炎/胆道 | 574-576 |
| 胰腺炎 | 577.0-577.1 |
| 肠梗阻 | 560 |
| 肠穿孔 | 531-534(穿孔型), 569.83 |
| 腹膜炎 | 567 |
| 肠缺血 | 557.0 |
| 憩室炎 | 562 |

### 4.4 急腹症亚型分类
- **穿孔型**：K35.2-K35.3, K25.1-K25.2, K26.1-K26.2, K27.1-K27.2, K28.1-K28.2, K63.1, K57.0, K65.0
- **梗阻型**：K56.*, K40-K46(伴梗阻), K44(嵌顿疝)
- **炎症型**：K35.0, K80.0-K80.1, K85, K57.3-K57.4, K65.1-K65.9
- **缺血型**：K55.0

---

## 5. 指标定义

### 5.1 Shock Index衍生指标
| 指标 | 公式 | 正常参考值 |
|------|------|----------|
| SI (Shock Index) | HR / SBP | 0.5-0.7 |
| MSI (Modified Shock Index) | HR / MAP | 0.7-1.0 |
| DSI (Diastolic Shock Index) | HR / DBP | 1.3-1.8 |
| Age-SI (Age-adjusted SI) | SI × (Age / 10) | 年龄依赖 |

注：MAP = (2×DBP + SBP) / 3

### 5.2 复合休克指数（CSI）——本研究创新指标
CSI = w₁×SI + w₂×MSI + w₃×DSI + w₄×Age_SI_normalized

权重通过Logistic回归系数标准化获得。

### 5.3 指标采集时间窗
- **急诊24h内首次生命体征**（ED首测值）
- **急诊24h内最大值**（worst值，反映恶化趋势）
- **急诊24h内均值**

---

## 6. 结局定义

### 6.1 主要结局
1. **ICU转入**：admissions.hadm_id 在 icustays 中存在记录
2. **院内死亡**：admissions.hospital_expire_flag = 1

### 6.2 次要结局
1. **ICU住院时长 > 3天**
2. **30天死亡**：patients.dod - admissions.admittime ≤ 30天
3. **急诊到ICU转入时间**：icustays.intime - admissions.edregtime

---

## 7. 协变量

| 类别 | 变量 | 来源 |
|------|------|------|
| 人口学 | 年龄、性别、种族、保险类型 | patients + admissions |
| 入院特征 | admission_type, admission_location | admissions |
| 合并症 | Charlson合并症指数（CCI） | diagnoses_icd → 计算 |
| 生命体征 | 体温、呼吸频率、SpO2、GCS | chartevents |
| 实验室 | WBC, lactate, creatinine, CRP | labevents |
| 疾病严重度 | SOFA评分(首日) | mimic-code concepts |
| 急腹症亚型 | 穿孔/梗阻/炎症/缺血 | ICD编码分类 |

---

## 8. 统计方法

### 8.1 描述性统计
- 连续变量：正态→mean±SD, 非正态→median(IQR)；组间比较t检验/Mann-Whitney U
- 分类变量：n(%)；组间比较χ²/Fisher精确检验

### 8.2 预测效能比较
- 各指标对各结局的ROC曲线及AUC值
- AUC两两比较：DeLong检验
- 最佳截断值：Youden指数

### 8.3 多因素分析
- Logistic回归：逐步纳入SI衍生指标+协变量
- 校准度：Hosmer-Lemeshow检验 + 校准曲线
- 区分度：AUC + NRI + IDI

### 8.4 亚组分析
- 按急腹症亚型（穿孔/梗阻/炎症/缺血）
- 按年龄分层（<60, 60-75, >75）
- 按性别

### 8.5 敏感性分析
- 仅ICD-10编码人群（排除ICD-9编码可能的分类误差）
- 仅主诊断急腹症（排除次要诊断纳入的偏倚）
- 不同时间窗指标（首测值 vs worst值 vs 均值）

### 8.6 临床决策价值
- 决策曲线分析（DCA）
- 临床净收益（Net Benefit）曲线

---

## 9. 样本量估算
预期ICU转入率约30-40%，院内死亡率约5-10%。
基于AUC从0.65提升至0.75的检验效能（α=0.05, β=0.20），
需要约400-600例ICU转入事件，总样本约1000-2000例。
MIMIC-IV急腹症急诊入院预计可达数千例，充分满足需求。

---

## 10. 论文结构

### Title
**Shock Index-Derived Parameters as Predictors of ICU Admission and In-Hospital Mortality in Emergency Department Patients with Acute Abdomen: A Retrospective Cohort Study from MIMIC-IV**

### Sections
1. Abstract (structured: Background, Methods, Results, Conclusion)
2. Introduction
3. Methods (Study design, Population, Variables, Outcomes, Statistical analysis)
4. Results (Baseline characteristics, SI-derived indices distribution, Predictive performance, Multivariable analysis, Subgroup analysis, Sensitivity analysis, DCA)
5. Discussion
6. Conclusion
7. Limitations
8. Declarations (Ethics, Funding, Conflicts)

---

## 11. 技术路线

```
Step 1: 数据提取（Python pandas → CSV.gz）
  ├── 急腹症人群筛选（ICD编码 + ED入院）
  ├── 生命体征提取（chartevents → HR/SBP/DBP/MAP）
  ├── 结局判定（ICU转入 + 院内死亡）
  └── 协变量提取（人口学 + 合并症 + 实验室）

Step 2: 指标计算与清洗
  ├── SI/MSI/DSI/Age-SI计算
  ├── CSI指标构建
  ├── 异常值处理与缺失值分析
  └── 急腹症亚型分类

Step 3: 统计分析（Python → statsmodels/scikit-learn）
  ├── 描述性统计
  ├── 单因素分析 + ROC/AUC
  ├── 多因素Logistic回归
  ├── 亚组分析 + 敏感性分析
  └── DCA分析

Step 4: 论文撰写 + 表格/图表制作
```
