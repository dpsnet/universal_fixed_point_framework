# 预注册附录：Necker 立方体临界慢化模拟数据质量报告

**生成日期**：2026-08-20  
**对应预注册文档**：[`prereg_necker_critical_slowing.md`](./prereg_necker_critical_slowing.md)  
**数据来源**：[`data/necker_simulated_dataset.csv`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/data/necker_simulated_dataset.csv)  
**生成脚本**：
- [`scripts/paperX_necker_simulated_dataset.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_simulated_dataset.py)
- [`scripts/paperX_necker_data_cleaning_analysis.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_data_cleaning_analysis.py)
- [`scripts/paperX_necker_noise_distribution_check.py`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_necker_noise_distribution_check.py)

**说明**：本报告基于含噪声的模拟数据，用于验证预注册阶段的数据清洗流程、字段完整性、测量误差统计规律，以及在典型排除率下关键模型参数估计的稳健性。所有数值均为 toy 模拟结果，不代表真实被试数据。

---

## 1. 数据集概览

| 项目 | 数值 |
|:--|:--|
| 被试数 | 24 |
| |δ| 等级数 | 12 |
| 符号方向 | 2（正 δ / 负 δ） |
| 原始总试次 | 115,200 |
| 字段数 | 39 |
| 数据格式 | CSV（UTF-8，表头见 §4） |

---

## 2. 数据字段清单（39 个）

| 类别 | 字段名 |
|:--|:--|
| 试次结构 | `subject_id`, `session_id`, `block_id`, `trial_id`, `trial_number`, `stimulus_id` |
| 刺激 | `ambiguity`, `ambiguity_signed`, `condition` |
| 时间 | `timestamp_onset`, `timestamp_offset` |
| 行为 | `choice`, `choice_encoded`, `rt_ms`, `is_correct`, `timed_out`, `response_device` |
| 眼动 | `gaze_x`, `gaze_y`, `fixation_duration_ms`, `blinks_count`, `saccades_count` |
| 瞳孔 | `pupil_baseline_mm`, `pupil_mean_mm`, `pupil_peak_mm`, `pupil_auc`, `pupil_quality` |
| 心血管 | `hr_baseline_bpm`, `hr_mean_bpm`, `hrv_rmssd_ms` |
| EEG 元数据 | `eeg_segment_id`, `eeg_epoch_quality`, `alpha_power_pre` |
| 混淆控制 | `previous_choice`, `run_length`, `adaptation_duration_ms` |
| 质控 | `excluded`, `exclude_reason`, `valid` |

---

## 3. 噪声注入策略

模拟数据在生成后经过 `inject_eyetracking_pupil_noise()` 模块处理，注入的测量误差类型包括：

1. **注视点仪器噪声**：每试次高斯噪声（σ = 0.5°）；
2. **被试内慢漂移**：每个被试独立的 x/y 慢漂移（σ = 0.05°）；
3. **离屏试次**：gaze_x/y 标记为 NaN（目标率 3%）；
4. **空间离群点**：少量 gaze 值被替换为大幅度随机数（目标率 2%）；
5. **眨眼/眼跳漏检误检**：计数 ±1 抖动；
6. **瞳孔基线漂移**：被试间基线偏移（σ = 0.10 mm）；
7. **瞳孔高斯测量噪声**（σ = 0.15 mm）；
8. **瞳孔完全缺失**：全部瞳孔字段 NaN（目标率 5%）；
9. **瞳孔部分缺失**：mean/peak NaN，AUC 折半（目标率 10%）；
10. **眨眼伪迹**：瞳孔直径异常压低（目标率 3%）；
11. **质量评分动态更新**：根据污染程度调整 `pupil_quality`；
12. **综合排除**：`pupil_quality < 0.5` 或 gaze 缺失的试次标记 `excluded=True`。

---

## 4. 数据质量统计

### 4.1 原始数据与清洗结果

| 指标 | 数值 |
|:--|:--|
| 原始总试次 | 115,200 |
| 清洗后有效试次 | 101,113 |
| 保留率 | 87.77% |
| 综合排除率 | 12.23% |

### 4.2 眼动噪声分布

| 指标 | 数值 | 典型真实范围 | 评估 |
|:--|:--|:--|:--|
| 有效注视点样本 | 111,878 | — | — |
| gaze_x 均值 | -0.019° | ≈ 0° | 符合 |
| gaze_y 均值 | 0.015° | ≈ 0° | 符合 |
| gaze_x 标准差 | 0.872° | 0.3°–1.0° | 略高 |
| gaze_y 标准差 | 0.872° | 0.3°–1.0° | 略高 |
| RMS 误差 | 1.234° | 0.3°–1.0° | 略高 |
| 离屏率 | 2.88% | 2%–10% | 符合 |
| 离群点率（\|gaze\| > 3°） | 1.13% | 1%–3% | 符合 |

**说明**：gaze 标准差与 RMS 误差略高于典型眼动仪精度（0.3°–1.0°），主要因为注入了 2% 的空间离群点。若用于真实实验校准，可降低 `gaze_outlier_rate` 至 0.5%–1%。

### 4.3 瞳孔噪声分布

| 指标 | 数值 | 典型真实范围 | 评估 |
|:--|:--|:--|:--|
| 瞳孔基线均值 | 3.501 mm | 2–5 mm | 符合 |
| 瞳孔基线标准差 | 0.221 mm | 0.1–0.4 mm | 符合 |
| 瞳孔平均直径均值 | 3.537 mm | 2–5 mm | 符合 |
| 瞳孔峰值直径均值 | 3.695 mm | 2–6 mm | 符合 |
| 完全缺失率 | 14.09% | 5%–20% | 符合 |
| 部分缺失率 | 9.13% | 5%–15% | 符合 |
| 眨眼伪迹率 | 1.49% | 1%–5% | 符合 |
| 平均 pupil_quality | 0.853 | 0.7–0.95 | 符合 |
| pupil_quality < 0.5 比例 | 9.93% | 5%–15% | 符合 |

---

## 5. 清洗规则

根据预注册文档 §5.2，清洗规则如下：

```python
mask = (
    (~df["excluded"])                      # 未被噪声模块标记为排除
    & (df["rt_ms"] >= 200.0)               # 下限截断：过快反应
    & (df["rt_ms"] <= 10000.0)             # 上限截断：超时
    & (df["pupil_quality"] >= 0.5)         # 瞳孔质量合格
    & (~df["gaze_x"].isna())               # 注视点有效
    & (~df["gaze_y"].isna())               # 注视点有效
)
```

---

## 6. 清洗后模型拟合结果

### 6.1 UFPF toy 模型

在清洗后的 101,113 试次上拟合 UFPF toy 幂律模型：

| 参数 | 估计值 | 真实值 | 偏差 |
|:--|:--|:--|:--|
| C | 288.54 ms | 250.00 ms | +15.4% |
| γ | 1.1445 | 1.2000 | -4.6% |
| t0 | 320.13 ms | 400.00 ms | -20.0% |
| σ_log | 0.1680 | 0.1786 | -5.9% |

**评估**：
- γ 估计较为稳健（偏差 < 5%），是模型中最关键的临界慢化指数；
- C 与 t0 存在系统性偏移，可能由 10000 ms 上限截断和噪声排除导致；
- 在真实实验中，应通过试点数据重新校准 C 与 t0 的先验范围。

### 6.2 标准 DDM 模型

在统一的 10,000 试次子样本上拟合标准 DDM：

| 参数 | 估计值 |
|:--|:--|
| k | 0.0010 |
| a | 4.5980 |
| z | 0.4976 |
| t0 | 234.08 ms |

### 6.3 模型比较

| 模型 | 比较子样本 log L | AIC | BIC |
|:--|:--|:--|:--|
| UFPF toy | -80,582.39 | 161,172.79 | 161,201.63 |
| 标准 DDM | -101,222.17 | 202,452.34 | 202,481.18 |
| ΔAIC（DDM − UFPF） | — | +41,279.55 | +41,279.55 |

**结论**：在由 UFPF toy 生成的含噪声数据上，UFPF toy 模型显著优于标准 DDM（ΔAIC > 10,000）。这一结果符合预期，因为数据本身由 UFPF toy 生成；本报告目的是验证清洗/比较流程在 12.23% 排除率下仍能稳健恢复 γ，而非证明 UFPF 优于 DDM。

---

## 7. 数据导出标准

清洗后的数据以 CSV 格式导出，字段与原始数据一致，额外保留 `excluded` 与 `exclude_reason` 以便审计。

导出文件：
- 完整含噪声模拟数据：[`data/necker_simulated_dataset.csv`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/data/necker_simulated_dataset.csv)
- 清洗后按被试-δ 汇总：[`data/necker_cleaned_analysis_results.csv`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/data/necker_cleaned_analysis_results.csv)
- 模型比较结果：[`data/necker_cleaning_model_comparison.csv`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/data/necker_cleaning_model_comparison.csv)
- 噪声分布检查摘要：[`data/necker_noise_distribution_check.csv`](file:///e:/workspace/hyper-resolution/universal_fixed_point_framework/data/necker_noise_distribution_check.csv)

---

## 8. 局限性与诚实边界

1. **模拟数据不代表真实被试**：RT、眼动、瞳孔均由参数化模型生成，真实实验中的被试间差异、练习效应、疲劳效应未完全模拟；
2. **gaze RMS 略高**：当前参数下 gaze RMS 为 1.23°，略高于典型眼动仪精度，可通过降低 `gaze_outlier_rate` 校准；
3. **UFPF toy 生成偏差**：C 与 t0 估计存在系统性偏移，提示真实实验需要试点阶段重新估计参数先验；
4. **DDM 仅使用标准形式**：未拟合非线性漂移、时变边界、有色噪声等扩展模型，因此 ΔAIC 可能夸大 UFPF toy 的优势；
5. **子样本比较**：DDM 在 10,000 试次子样本上拟合，UFPF toy 在 101,113 试次上估计参数但在同一子样本上评估似然，AIC/BIC 基于同一子样本量计算，具有可比性；
6. **无数值预言**：本报告为方法论验证，不声称真实 Necker 实验将观察到 γ ≠ 1。

---

## 9. 关键脚本运行命令

```bash
# 生成含噪声模拟数据
python scripts/paperX_necker_simulated_dataset.py

# 数据清洗、建模与稳健性分析
python scripts/paperX_necker_data_cleaning_analysis.py

# 噪声分布特征检查
python scripts/paperX_necker_noise_distribution_check.py
```

---

**版本**：v0.1（2026-08-20）
