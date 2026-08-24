# 实验预注册文档：Necker 立方体临界慢化与 MUFPF toy 模型检验

**状态**：预注册草案 v0.1（2026-08-20）  
**对应笔记**：[`sensory_integration_time_ruler.md`](./sensory_integration_time_ruler.md) §7.8.9  
**目标**：在经典心理物理学框架内，通过 Necker 立方体双稳态知觉任务检验反应时（RT）在知觉边界附近的临界慢化是否服从幂律 $T(\delta)\sim|\delta|^{-\gamma}$，并与标准 Drift-Diffusion Model（DDM）进行模型选择比较。  
**诚实边界**：本预注册文档为 MUFPF 框架内的方法论规划，无数值预言；所有分析方案需在试点数据后修订。

---

## 1. 研究问题与假设

### 1.1 核心问题

人类在双稳态知觉（如 Necker 立方体）的决策过程中，反应时随刺激模糊度 $|\delta|$ 接近知觉边界时是否呈现幂律发散？若存在，其幂律指数 $\gamma$ 是否显著偏离标准 DDM 预测的 $\gamma_{\text{DDM}}=1$？

### 1.2 假设

- **H1（MUFPF toy 模型）**：平均 RT 满足 $E[RT|\delta]=C|\delta|^{-\gamma}+t_0$，其中 $\gamma\neq1$，且 $\gamma$ 可由底层谱维度 $d_s$ 通过 $\gamma=2/d_s$ 解释。
- **H0（标准 DDM）**：临界点附近 RT 发散指数为固定值 $\gamma=1$；若 DDM 扩展（非线性漂移、时变边界、有色噪声）可拟合数据，则 H1 的解释力被削弱。
- **H2（中性/不可区分）**：数据噪声过大或 RT 截断严重，无法可靠区分幂律指数与 1。

### 1.3 研究类型

- 实验类型：实验室行为实验，可选同步记录瞳孔、EEG/MEG。
- 设计：被试内设计，$|\delta|$ 为自变量，RT 为因变量。

---

## 2. 被试

### 2.1 纳入标准

- 年龄 18–35 岁；
- 视力或矫正视力正常；
- 无已知前庭/神经疾病影响知觉或反应时；
- 首次参与此类双稳态实验（避免练习效应污染）。

### 2.2 排除标准

- 在练习阶段（见 §4.3）正确率 < 60% 或平均 RT 异常（> 5000 ms）；
- 超过 20% 试次超时或按键错误；
- 自我报告无法理解任务。

### 2.3 样本量

#### 2.3.1 基于 toy 模拟的初步估计

使用 [`scripts/paperX_power_analysis.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_power_analysis.py) 进行解析功效分析（假设真实 $\gamma=1.2$，CV=0.18，$|\delta|\in[0.05,0.50]$，12 个对数均匀等级，10000 ms 上限截断）。结果：

| 参数 | 数值 |
|:--|:--|
| 参考大样本 MLE | $\hat\gamma=1.17$，SE=0.0026（n=50，200 trials/δ） |
| 达到 80% 功效的最小设计（按总试次数） | 8 被试 × 20 trials/δ = 3840 总试次 |

#### 2.3.2 实际招募目标

上述估计基于强简化假设（无被试间随机效应、模型正确设定、无额外混淆变量），实际实验应采用更保守样本量：

- **目标样本量**：N = 24 名有效被试；
- **每被试试次数**：约 480 试次（20 trials/δ × 12 |δ| 等级 × 2 符号方向）；
- **总数据量**：约 11520 试次；
- **预留脱落**：招募 28–30 人，按 §2.2 排除后保留 ≥24 人。

选择 N=24 的理由：
1. 覆盖个体差异和练习效应；
2. 允许分层贝叶斯/混合效应模型中的被试级随机斜率；
3. 为 EEG/MEG 子分析（若进行）提供足够的 trial 数量。

---

## 3. 实验材料

### 3.1 刺激

- **Necker 立方体**：标准线框立方体，大小约 6° 视角；
- **模糊度参数 δ**：通过改变两个深度解释线索的相对强度实现，例如：
  - 遮挡线索（线条粗细/透明度差异）；
  - 透视线索（近大远小程度）；
  - 亮度/阴影偏向。
- **δ 操作化**：$\delta=0$ 表示完全中性（50/50 双稳态）；$|\delta|>0$ 表示偏向某一知觉解释；$\delta>0$ 偏向解释 A，$\delta<0$ 偏向解释 B。
- **δ 等级**：使用脚本 [`paperX_necker_trial_allocation.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_trial_allocation.py) 生成对数均匀分布的 12 个 |δ| 等级：

| 等级 | abs(δ) | 预期 RT（ms，γ=1.2） | 每符号方向试次数（adaptive_rt 策略） |
|:--:|:--:|:--:|:--:|
| 1 | 0.0500 | 9503 | 522 |
| 2 | 0.0616 | 7481 | 411 |
| 3 | 0.0760 | 5908 | 324 |
| 4 | 0.0937 | 4684 | 257 |
| 5 | 0.1155 | 3733 | 205 |
| 6 | 0.1424 | 2993 | 165 |
| 7 | 0.1756 | 2417 | 133 |
| 8 | 0.2164 | 1969 | 107 |
| 9 | 0.2668 | 1620 | 88 |
| 10 | 0.3290 | 1349 | 73 |
| 11 | 0.4056 | 1138 | 62 |
| 12 | 0.5000 | 974 | 53 |

*注：试次数分配采用 adaptive_rt 策略，使临界点获得更多试次以准确估计分布尾部。*

### 3.2 设备

- 显示器：刷新率 ≥120 Hz，固定观看距离 60 cm；
- 反应键：标准键盘或按键盒，左右键对应两种知觉解释；
- 可选设备：眼动仪（注视监控）、瞳孔仪、EEG/MEG 采集系统。

---

## 4. 实验流程

### 4.1 试次结构

1. **注视点**：500 ms；
2. **刺激呈现**：最多 10000 ms（见 §5 截断策略），被试按键后消失；
3. **反馈/间隔**：500 ms 空屏（不提供正确性反馈，仅用于 ITI）；
4. 被试需尽快且准确地报告看到哪一种知觉解释（A 或 B）。

### 4.2 试次顺序

- 每个 block 包含所有 δ 等级的伪随机序列，避免连续相同 δ；
- 正负 δ 随机穿插；
- 每 120 试次安排一次短暂休息；
- 总实验分 4 个 session，每个 session 约 120 试次。

### 4.3 练习阶段

- 正式实验前 24 练习试次（每个 |δ| 等级 1 正 1 负）；
- 仅用于熟悉任务，数据不进入主分析；
- 若练习阶段正确率 < 60% 或超时率 > 30%，排除该被试。

---

## 5. 数据收集与截断处理策略

### 5.1 收集变量

| 变量 | 类型 | 说明 |
|:--|:--|:--|
| subject_id | 分类 | 被试编号 |
| session/block/trial | 整数 | 实验结构 |
| ambiguity_signed | 连续 | 带符号模糊度 δ |
| ambiguity | 连续 | \|δ\| |
| choice | 分类 | A / B |
| choice_encoded | 整数 | A=+1, B=-1 |
| rt_ms | 连续 | 反应时（ms） |
| timed_out | 布尔 | 是否超时 |
| response_device | 分类 | 键盘/按键盒 |
| gaze_x/y（可选） | 连续 | 注视点坐标 |
| pupil_baseline/peak（可选） | 连续 | 瞳孔直径 |
| eeg_segment_id（可选） | 字符串 | EEG epoch 标识 |

完整字段模板见 [`scripts/paperX_necker_experiment_data_template.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_experiment_data_template.py)。

### 5.2 截断策略

#### 5.2.1 上限截断（右截断）

- **截断值**：10000 ms。
- **理由**：允许被试有足够时间完成极困难试次，同时控制总实验时长。
- **处理方法**：
  1. 主分析报告截断比例；
  2. 在 MUFPF 似然中显式引入右截断校正（log-normal 右截断似然）：
     $$\mathcal{L}_{\text{censored}} = \mathbb{1}_{RT<RT_{\max}}\log f(RT) + \mathbb{1}_{RT=RT_{\max}}\log(1-F(RT_{\max}))$$
  3. 若截断比例 > 10%（尤其在小 |δ| 等级），则考虑提高截断值或调整 δ 范围。

#### 5.2.2 下限截断（过快反应）

- **截断值**：200 ms。
- **排除条件**：RT < 200 ms 的试次被视为按键抖动或预期反应，予以排除。
- 若某被试此类试次 > 5%，报告并考虑排除该被试。

#### 5.2.3 中间值处理

- RT ∈ [200, 10000] ms 的试次进入主分析；
- 对 RT 取对数后建模，以降低右偏影响。

---

## 6. 统计模型与检验计划

### 6.1 MUFPF toy 模型

假设 RT|δ 服从对数正态分布，其均值由幂律决定：

$$E[RT|\delta] = C|\delta|^{-\gamma} + t_0,$$
$$\log(RT|\delta) \sim \mathcal{N}\left(\log(C|\delta|^{-\gamma}+t_0) - \frac{\sigma^2}{2},\; \sigma^2\right).$$

参数：$\theta_{\text{MUFPF}}=(C,\gamma,t_0,\sigma)$，k=4。

拟合方法：最大似然估计（L-BFGS-B），多起点网格搜索避免局部最优。

### 6.2 标准 DDM

使用标准 Wiener 扩散模型：

- 漂移率 $v(\delta)=k\cdot\delta$；
- 边界间距 $a$；
- 起始点比例 $z$（通常固定为 0.5）；
- 非决策时间 $t_0$。

参数：$\theta_{\text{DDM}}=(k,a,z,t_0)$，k=4。

拟合方法：Navarro & Fuss (2009) 解析第一通过时间 PDF，最大似然估计。**注意**：DDM PDF 单位为 1/秒，观测 RT 单位为 ms，比较前必须统一密度测度：

$$f_{\text{ms}}(t_{\text{ms}}) = \frac{1}{1000} f_s\!\left(\frac{t_{\text{ms}}}{1000}\right).$$

### 6.3 模型比较

- **信息准则**：AIC、BIC；
- **主指标**：ΔAIC = AIC_model - min(AIC)；
- **判读标准**（Burnham & Anderson, 2002）：
  - ΔAIC ≤ 2：模型有竞争力；
  - 4 ≤ ΔAIC ≤ 7：较弱支持；
  - ΔAIC > 10：基本排除。
- **参数显著性**：对 γ 进行 bootstrap 置信区间（n_bootstrap=1000）或 Wald 区间估计；若 95% CI 不包含 1，则认为显著偏离 DDM 预测。

### 6.4 替代模型（敏感性分析）

若标准 DDM 与 MUFPF toy 无法区分，则拟合以下扩展模型：

| 模型 | 额外自由度 | 用途 |
|:--|:--|:--|
| DDM + 非线性漂移 $v(\delta)=k\delta + q\delta^3$ | 1 | 检验幂律是否可由漂移非线性解释 |
| DDM + 时变边界 $a(\delta)=a_0 + a_1|\delta|$ | 1 | 检验边界随 δ 变化是否解释慢化 |
| DDM + 有色噪声 | 1–2 | 检验非马尔可夫噪声是否产生伪幂律 |

### 6.5 多层次结构

由于数据为被试内设计，最终分析采用分层贝叶斯或混合效应扩展：

$$\gamma_i \sim \mathcal{N}(\mu_\gamma, \tau_\gamma^2),$$

其中 $i$ 为被试索引。若被试级 γ 分布的 95% 可信区间不包含 1，支持 H1。

---

## 7. 独立估计谱维度 $d_s$（可选的神经验证）

### 7.1 目标

若同时采集 EEG/MEG/LFP，尝试从神经信号中独立估计谱维度 $d_s$，并验证行为学 γ 与 $2/d_s$ 的一致性。

### 7.2 候选方法

| 方法 | 神经信号 | 具体操作 | 与 $d_s$ 的关系 | 典型文献 |
|:--|:--|:--|:--|:--|
| **PSD 斜率法** | EEG/MEG/LFP 单通道或多通道 | 估计功率谱 $S(f)\sim f^{-\beta}$；在 $10^{-1}$–$10^2$ Hz 频段拟合 β | 对扩散型过程，形式类比 $d_s\approx 2(3-\beta)$；需假设信号由分数阶布朗运动生成 | Heneghan & McDarby (2000); Bullmore et al. (2001) |
| **特征值累积法** | 多通道协方差矩阵或图 Laplacian | 构建通道间相关矩阵/图 Laplacian，计算特征值累积分布 $N(\lambda)\sim\lambda^{d_s/2}$ | 直接对应图/流形上的谱维度定义 | Burioni & Cassi (2005); de Nigris et al. (2017) |
| **返回概率法** | 神经源重构时间序列 | 定义随机游走在有效网络上的返回概率 $P(t)\sim t^{-d_s/2}$ | 随机游走在谱维度 $d_s$ 网络上的返回概率标度 | Burioni & Cassi (2005); Riascos & Mateos (2014) |
| **多尺度熵/DFA** | EEG 全局场功率或单通道 | 估计 Hurst 指数 $H$ 或标度指数 α | 分数阶布朗运动的谱维度形式类比：$d_s\approx 2/(2H-1)$（对 $H>0.5$） | Costa et al. (2005); Peng et al. (1994) |

### 7.3 诚实边界

- 上述关系均为**形式类比**，不是 MUFPF 严格数学定理；
- MUFPF 的 $d_s$ 是针对 Rec/Sp 谱对象的抽象量，神经数据上的 $d_s$ 估计需要额外映射假设；
- 若独立估计的 $d_s$ 与行为 γ 不一致，**不能**直接否定 MUFPF toy 模型，只能说明当前映射假设不成立；
- 本部分为探索性分析，不纳入主要假设检验。

---

## 8. 预注册分析与实际分析的偏差计划

### 8.1 必须预注册的内容

1. 主要假设 H1/H0/H2；
2. δ 等级、试次数分配、截断值；
3. 纳入/排除标准；
4. 主模型（MUFPF toy）和竞争模型（DDM）；
5. 模型比较指标（AIC/BIC）和显著性标准；
6. 计划样本量及其依据。

### 8.2 可允许的探索性分析

- 扩展 DDM 模型比较；
- EEG/MEG 频谱分析（若采集）；
- 瞳孔/眼动协变量分析；
- 不同 δ 间距（线性 vs 对数）的稳健性检验。

### 8.3 偏离处理

若实际数据质量迫使改变截断值或排除标准，将在最终报告中明确说明并报告敏感性分析。

---

## 9. 可重复性

- 所有分析代码将存放于 `scripts/` 目录；
- 数据使用 [`paperX_necker_experiment_data_template.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_experiment_data_template.py) 定义字段；
- 试次分配由 [`paperX_necker_trial_allocation.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_trial_allocation.py) 生成；
- 功效分析由 [`paperX_power_analysis.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_power_analysis.py) 生成；
- 最终分析脚本将随论文/报告一并公开。

---

## 10. 局限性与诚实边界

- 本预注册基于 MUFPF toy 模型合成数据，真实数据可能不满足对数正态假设；
- 功效分析假设无被试间随机效应，实际所需样本量可能更大；
- 10000 ms 截断可能压缩 γ 估计；
- DDM 扩展模型可能也能拟合 γ≠1 数据，MUFPF 解释需通过 ΔAIC 和独立 $d_s$ 估计竞争；
- 本研究不检验 MUFPF 的量子/谱效应（生物尺度不可观测，见 [`sensory_integration_time_ruler.md`](./sensory_integration_time_ruler.md) §7.3）。

---

## 11. 附录 A：数据质量报告（模拟验证）

### A.1 目的与数据来源

本附录基于含噪声的模拟数据，验证预注册阶段的数据清洗流程、字段完整性、测量误差统计规律，以及在典型排除率下关键模型参数估计的稳健性。

- **生成脚本**：[`scripts/paperX_necker_simulated_dataset.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_simulated_dataset.py)（含噪声注入）、[`scripts/paperX_necker_data_cleaning_analysis.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_data_cleaning_analysis.py)（清洗+建模）、[`scripts/paperX_necker_noise_distribution_check.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_noise_distribution_check.py)（分布检查）
- **完整独立报告**：[`notes/04_lorentz_gravity/prereg_necker_data_quality_report.md`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/notes/04_lorentz_gravity/prereg_necker_data_quality_report.md)

### A.2 噪声注入参数（v0.26 校准后）

| 参数 | 默认值 | 说明 |
|:--|:--:|:--|
| `gaze_noise_std_deg` | 0.50° | 注视点仪器噪声 |
| `gaze_drift_std_deg` | 0.05° | 被试内慢漂移 |
| `gaze_offscreen_rate` | 0.03 | 离屏试次比例 |
| `gaze_outlier_rate` | **0.005** | 空间离群点比例（校准后从 0.02 降低） |
| `gaze_outlier_std_deg` | **3.0°** | 离群点标准差（校准后从 5.0° 降低） |
| `pupil_noise_std_mm` | 0.15 mm | 瞳孔测量噪声 |
| `pupil_baseline_drift_mm` | 0.10 mm | 被试间基线漂移 |
| `pupil_dropout_rate` | 0.05 | 完全缺失比例 |
| `pupil_partial_rate` | 0.10 | 部分缺失比例 |
| `pupil_blink_artifact_rate` | 0.03 | 眨眼伪迹比例 |

### A.3 数据质量统计

#### A.3.1 原始与清洗后数据

| 指标 | 数值 |
|:--|:--|
| 被试数 | 24 |
| 原始总试次 | 115,200 |
| 清洗后有效试次 | 101,117 |
| 保留率 | **87.78%** |
| 综合排除率 | **12.22%** |

#### A.3.2 眼动噪声分布

| 指标 | 数值 | 典型真实范围 | 评估 |
|:--|:--|:--|:--|
| gaze_x 标准差 | 0.544° | 0.3°–1.0° | 符合 |
| gaze_y 标准差 | 0.540° | 0.3°–1.0° | 符合 |
| **RMS 误差** | **0.767°** | **0.3°–1.0°** | **符合** |
| 离屏率 | 2.93% | 2%–10% | 符合 |
| 离群点率（\|gaze\| > 3°） | 0.17% | 1%–3% | 偏低 |

#### A.3.3 瞳孔噪声分布

| 指标 | 数值 | 典型真实范围 | 评估 |
|:--|:--|:--|:--|
| 瞳孔基线标准差 | 0.195 mm | 0.1–0.4 mm | 符合 |
| 瞳孔平均直径标准差 | 0.397 mm | 0.1–0.5 mm | 符合 |
| 完全缺失率 | 14.07% | 5%–20% | 符合 |
| 部分缺失率 | 9.12% | 5%–15% | 符合 |
| 眨眼伪迹率 | 1.48% | 1%–5% | 符合 |
| pupil_quality < 0.5 比例 | 9.89% | 5%–15% | 符合 |

### A.4 清洗后模型拟合结果

#### A.4.1 MUFPF toy 模型

| 参数 | 估计值 | 真实值 | 偏差 |
|:--|:--|:--|:--|
| C | 288.88 ms | 250.00 ms | +15.6% |
| **γ** | **1.1440** | **1.2000** | **-4.7%** |
| t0 | 319.43 ms | 400.00 ms | -20.1% |
| σ_log | 0.1680 | 0.1786 | -5.9% |

#### A.4.2 标准 DDM 模型（10,000 试次子样本）

| 参数 | 估计值 |
|:--|:--|
| k | 0.0010 |
| a | 4.5876 |
| z | 0.5041 |
| t0 | 230.04 ms |

#### A.4.3 模型比较（同一子样本）

| 模型 | log L | AIC | BIC |
|:--|:--|:--|:--|
| MUFPF toy | -80,535.10 | 161,078.21 | 161,107.05 |
| 标准 DDM | -101,188.23 | 202,384.45 | 202,413.29 |
| ΔAIC（DDM − MUFPF） | — | **+41,306.24** | **+41,306.24** |

### A.5 附录结论

- 在 12.22% 综合排除率下，关键参数 γ 估计稳健（偏差 < 5%）；
- 校准后 gaze RMS 误差降至 0.767°，进入典型眼动仪精度范围；
- 瞳孔缺失/伪迹率均落在真实实验常见范围内；
- MUFPF toy 在由其生成的数据上显著优于标准 DDM，符合预期；
- 本附录为 toy 模拟验证，真实实验需根据试点数据重新校准噪声参数。

---

## 12. 参考文献

- Burnham, K. P., & Anderson, D. R. (2002). *Model selection and multimodal inference: A practical information-theoretic approach* (2nd ed.). Springer.
- Navarro, D. J., & Fuss, I. G. (2009). Fast and accurate calculations for first-passage times in Wiener diffusion models. *Journal of Mathematical Psychology*, 53(4), 222–230.
- Ratcliff, R., & McKoon, G. (2008). The diffusion decision model: Theory and data for two-choice decision tasks. *Neural Computation*, 20(4), 873–922.
- Burioni, R., & Cassi, D. (2005). Random walks on graphs: ideas, techniques and results. *Journal of Physics A: Mathematical and General*, 38(8), R45–R78.

---

**版本记录**  
- v0.1（2026-08-20）：初始预注册草案，含研究问题、样本量、实验流程、截断策略、统计模型与模型比较计划。
- v0.2（2026-08-20）：新增附录 A（数据质量报告模拟验证），整合校准后的噪声注入参数、质量统计与模型拟合结果；对应 `scripts/paperX_necker_simulated_dataset.py` v0.26 校准（`gaze_outlier_rate` 0.02→0.005，`gaze_outlier_std_deg` 5.0°→3.0°）。
