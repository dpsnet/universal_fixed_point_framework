# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
基于试次分配方案生成模拟 Necker 立方体实验数据
=====================================================

对应 notes/04_lorentz_gravity/prereg_necker_critical_slowing.md。

输入：
  - data/necker_trial_allocation.csv（由 paperX_necker_trial_allocation.py 生成）

输出：
  - data/necker_simulated_dataset.csv：完整模拟数据集，包含 RT、选择、眼动、
    瞳孔、心血管、EEG 等字段，字段定义与 paperX_necker_experiment_data_template.py
    保持一致。
  - figs/paperX_necker_simulated_dataset.png：RT 与选择比例的概览图。

运行命令：
    python scripts/paperX_necker_simulated_dataset.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


def inject_eyetracking_pupil_noise(
    df: pd.DataFrame,
    rng: np.random.Generator,
    gaze_noise_std_deg: float = 0.50,
    gaze_drift_std_deg: float = 0.05,
    gaze_offscreen_rate: float = 0.03,
    gaze_outlier_rate: float = 0.005,
    gaze_outlier_std_deg: float = 3.0,
    pupil_noise_std_mm: float = 0.15,
    pupil_baseline_drift_mm: float = 0.10,
    pupil_dropout_rate: float = 0.05,
    pupil_partial_rate: float = 0.10,
    pupil_blink_artifact_rate: float = 0.03,
) -> pd.DataFrame:
    """
    为眼动与瞳孔数据注入真实实验风格的测量噪声与缺失。

    修改包括：
      1. 注视点仪器噪声 + 慢漂移；
      2. 随机离屏（标记 NaN）与空间离群点；
      3. 瞳孔基线被试间漂移 + 高斯测量噪声；
      4. 瞳孔完全缺失（NaN）、部分缺失（mean/peak 但 baseline 缺失）、眨眼伪迹；
      5. 根据污染程度更新 pupil_quality 与 valid/excluded 标记。

    校准说明（v0.26）：
      - gaze_outlier_rate 从 0.02 降至 0.005，gaze_outlier_std_deg 从 5.0 降至 3.0，
        使 gaze RMS 误差从约 1.23° 降至 0.7°–0.8°，更接近典型眼动仪精度 0.3°–1.0°。
    """
    df = df.copy()
    n = len(df)

    # 1. 注视点仪器噪声 + 被试内慢漂移
    # 为每个被试生成一个慢漂移偏移
    subject_ids = df["subject_id"].unique()
    drift_map = {
        sid: (rng.normal(0.0, gaze_drift_std_deg), rng.normal(0.0, gaze_drift_std_deg))
        for sid in subject_ids
    }
    dx = df["subject_id"].map(lambda s: drift_map[s][0]).to_numpy() + rng.normal(0.0, gaze_noise_std_deg, size=n)
    dy = df["subject_id"].map(lambda s: drift_map[s][1]).to_numpy() + rng.normal(0.0, gaze_noise_std_deg, size=n)
    df["gaze_x"] = df["gaze_x"].to_numpy() + dx
    df["gaze_y"] = df["gaze_y"].to_numpy() + dy

    # 2. 离屏试次：注视点超出合理范围（>3°），标记为 NaN
    offscreen_mask = rng.random(size=n) < gaze_offscreen_rate
    df.loc[offscreen_mask, "gaze_x"] = np.nan
    df.loc[offscreen_mask, "gaze_y"] = np.nan
    df.loc[offscreen_mask, "valid"] = False

    # 3. 空间离群点（少量错误校准点）
    outlier_mask = rng.random(size=n) < gaze_outlier_rate
    df.loc[outlier_mask, "gaze_x"] = rng.normal(0.0, gaze_outlier_std_deg, size=outlier_mask.sum())
    df.loc[outlier_mask, "gaze_y"] = rng.normal(0.0, gaze_outlier_std_deg, size=outlier_mask.sum())

    # 4. 眨眼/眼跳计数加入漏检与误检
    df["blinks_count"] = np.clip(df["blinks_count"] + rng.integers(-1, 2, size=n), 0, None).astype(int)
    df["saccades_count"] = np.clip(df["saccades_count"] + rng.integers(-1, 2, size=n), 0, None).astype(int)

    # 5. 瞳孔基线被试间漂移 + 测量噪声
    baseline_drift_map = {sid: rng.normal(0.0, pupil_baseline_drift_mm) for sid in subject_ids}
    b_drift = df["subject_id"].map(baseline_drift_map).to_numpy()
    df["pupil_baseline_mm"] = df["pupil_baseline_mm"].to_numpy() + b_drift + rng.normal(0.0, pupil_noise_std_mm, size=n)
    df["pupil_mean_mm"] = df["pupil_mean_mm"].to_numpy() + b_drift + rng.normal(0.0, pupil_noise_std_mm, size=n)
    df["pupil_peak_mm"] = df["pupil_peak_mm"].to_numpy() + b_drift + rng.normal(0.0, pupil_noise_std_mm, size=n)
    df["pupil_auc"] = df["pupil_auc"].to_numpy() + rng.normal(0.0, 80.0, size=n)

    # 6. 瞳孔完全缺失
    dropout_mask = rng.random(size=n) < pupil_dropout_rate
    df.loc[dropout_mask, ["pupil_baseline_mm", "pupil_mean_mm", "pupil_peak_mm", "pupil_auc"]] = np.nan
    df.loc[dropout_mask, "valid"] = False

    # 7. 部分缺失：baseline 在但 peak/mean 丢失（追踪短暂丢失）
    partial_mask = rng.random(size=n) < pupil_partial_rate
    df.loc[partial_mask, ["pupil_mean_mm", "pupil_peak_mm"]] = np.nan
    df.loc[partial_mask, "pupil_auc"] = df.loc[partial_mask, "pupil_auc"] * 0.5

    # 8. 眨眼伪迹：瞳孔直径被异常放大/缩小
    blink_mask = rng.random(size=n) < pupil_blink_artifact_rate
    df.loc[blink_mask, "pupil_mean_mm"] = df.loc[blink_mask, "pupil_baseline_mm"] * rng.uniform(0.3, 0.7, size=blink_mask.sum())
    df.loc[blink_mask, "pupil_peak_mm"] = df.loc[blink_mask, "pupil_baseline_mm"] * rng.uniform(0.3, 0.9, size=blink_mask.sum())

    # 9. 根据污染程度更新 pupil_quality
    quality = df["pupil_quality"].to_numpy().copy()
    quality[dropout_mask] = rng.uniform(0.0, 0.3, size=dropout_mask.sum())
    quality[partial_mask] *= rng.uniform(0.4, 0.8, size=partial_mask.sum())
    quality[blink_mask] *= rng.uniform(0.3, 0.7, size=blink_mask.sum())
    quality[offscreen_mask] *= rng.uniform(0.5, 0.9, size=offscreen_mask.sum())
    df["pupil_quality"] = np.clip(quality, 0.0, 1.0)

    # 10. 综合标记：低质量数据排除（pupil_quality < 0.5 或 gaze 缺失）
    exclude_mask = (df["pupil_quality"] < 0.5) | (df["gaze_x"].isna())
    df.loc[exclude_mask, "excluded"] = True
    df.loc[exclude_mask, "exclude_reason"] = "low_quality_eye_or_pupil"
    df.loc[exclude_mask, "valid"] = False

    return df


def generate_trial_records(
    allocation: pd.DataFrame,
    n_subjects: int = 24,
    true_gamma: float = 1.2,
    true_C: float = 250.0,
    true_t0: float = 400.0,
    rt_cv: float = 0.18,
    choice_slope: float = 8.0,
    seed: int = 2026,
    # 眼动/瞳孔测量噪声参数
    gaze_noise_std_deg: float = 0.50,
    gaze_drift_std_deg: float = 0.05,
    gaze_offscreen_rate: float = 0.03,
    gaze_outlier_rate: float = 0.005,
    gaze_outlier_std_deg: float = 3.0,
    pupil_noise_std_mm: float = 0.15,
    pupil_baseline_drift_mm: float = 0.10,
    pupil_dropout_rate: float = 0.05,
    pupil_partial_rate: float = 0.10,
    pupil_blink_artifact_rate: float = 0.03,
) -> pd.DataFrame:
    """
    根据试次分配表生成模拟实验数据。

    参数：
      n_subjects: 被试数
      true_gamma, true_C, true_t0: 幂律 RT 参数
      rt_cv: RT 对数正态变异系数
      choice_slope: 选择概率 sigmoid 斜率
      gaze_noise_std_deg: 注视点仪器噪声标准差（度）
      gaze_drift_std_deg: 慢漂移标准差（度）
      gaze_offscreen_rate: 离屏试次比例
      gaze_outlier_rate: 离群点比例（已校准至 0.005）
      gaze_outlier_std_deg: 离群点标准差（度，已校准至 3.0）
      pupil_noise_std_mm: 瞳孔直径测量噪声（mm）
      pupil_baseline_drift_mm: 被试间基线漂移（mm）
      pupil_dropout_rate: 完全缺失比例
      pupil_partial_rate: 部分时段缺失比例
      pupil_blink_artifact_rate: 眨眼伪迹比例
    """
    rng = np.random.default_rng(seed)
    records = []
    trial_counter_global = 0

    for subj_idx in range(n_subjects):
        subject_id = f"S{subj_idx+1:03d}"

        for _, row in allocation.iterrows():
            abs_delta = row["abs_delta"]
            n_trials = int(row["n_trials_per_sign"])

            for sign in [-1.0, 1.0]:
                delta_signed = sign * abs_delta

                # 幂律 RT 均值
                rt_mean = true_C * (abs_delta ** (-true_gamma)) + true_t0
                sigma_log = np.sqrt(np.log(1 + rt_cv ** 2))
                mu_log = np.log(rt_mean) - 0.5 * sigma_log ** 2

                # 选择概率
                prob_a = 1.0 / (1.0 + np.exp(-choice_slope * delta_signed))

                for t in range(n_trials):
                    rt = rng.lognormal(mu_log, sigma_log)
                    rt = max(150.0, min(rt, 10000.0))

                    choice = "A" if rng.random() < prob_a else "B"
                    choice_enc = 1.0 if choice == "A" else -1.0

                    is_correct = pd.NA
                    if delta_signed > 0.05:
                        is_correct = (choice == "A")
                    elif delta_signed < -0.05:
                        is_correct = (choice == "B")

                    block_id = f"B{((trial_counter_global // 120) % 4) + 1:02d}"
                    session_id = f"SE{((trial_counter_global // 480) % 4) + 1:02d}"

                    record = {
                        "subject_id": subject_id,
                        "session_id": f"{subject_id}_{session_id}",
                        "block_id": block_id,
                        "trial_id": f"{subject_id}_{trial_counter_global:05d}",
                        "trial_number": trial_counter_global + 1,
                        "stimulus_id": f"necker_{int((abs_delta + 0.5) * 1000):04d}_{'pos' if sign > 0 else 'neg'}",
                        "ambiguity": abs_delta,
                        "ambiguity_signed": delta_signed,
                        "condition": "necker_critical_slowing_simulation",
                        "timestamp_onset": pd.Timestamp.now(),
                        "timestamp_offset": pd.Timestamp.now() + pd.Timedelta(milliseconds=float(rt)),
                        "choice": choice,
                        "choice_encoded": choice_enc,
                        "rt_ms": float(rt),
                        "is_correct": is_correct,
                        "timed_out": False,
                        "response_device": "keyboard",
                        "gaze_x": rng.normal(0.0, 0.01),
                        "gaze_y": rng.normal(0.0, 0.01),
                        "fixation_duration_ms": float(rt),
                        "blinks_count": rng.integers(0, 2),
                        "saccades_count": rng.integers(0, 2),
                        "pupil_baseline_mm": rng.normal(3.5, 0.1),
                        "pupil_mean_mm": rng.normal(3.6 + 0.02 * (rt / rt_mean - 1.0), 0.1),
                        "pupil_peak_mm": rng.normal(3.75 + 0.03 * (rt / rt_mean - 1.0), 0.12),
                        "pupil_auc": rng.normal(1200.0 + 50.0 * (rt / rt_mean - 1.0), 100.0),
                        "pupil_quality": rng.uniform(0.9, 1.0),
                        "hr_baseline_bpm": rng.normal(72.0, 5.0),
                        "hr_mean_bpm": rng.normal(73.0 + 0.5 * (rt / rt_mean - 1.0), 5.0),
                        "hrv_rmssd_ms": rng.normal(45.0, 8.0),
                        "eeg_segment_id": f"{subject_id}_seg{(trial_counter_global // 40):04d}",
                        "eeg_epoch_quality": rng.uniform(0.85, 1.0),
                        "alpha_power_pre": rng.lognormal(2.5, 0.3),
                        "previous_choice": rng.choice(["A", "B"]),
                        "run_length": rng.integers(1, 4),
                        "adaptation_duration_ms": 0.0,
                        "excluded": False,
                        "exclude_reason": "",
                        "valid": True,
                    }
                    records.append(record)
                    trial_counter_global += 1

    df = pd.DataFrame(records)
    df["is_correct"] = df["is_correct"].astype("boolean")

    # 注入眼动与瞳孔测量噪声
    df = inject_eyetracking_pupil_noise(
        df,
        rng,
        gaze_noise_std_deg=gaze_noise_std_deg,
        gaze_drift_std_deg=gaze_drift_std_deg,
        gaze_offscreen_rate=gaze_offscreen_rate,
        gaze_outlier_rate=gaze_outlier_rate,
        gaze_outlier_std_deg=gaze_outlier_std_deg,
        pupil_noise_std_mm=pupil_noise_std_mm,
        pupil_baseline_drift_mm=pupil_baseline_drift_mm,
        pupil_dropout_rate=pupil_dropout_rate,
        pupil_partial_rate=pupil_partial_rate,
        pupil_blink_artifact_rate=pupil_blink_artifact_rate,
    )
    return df


def main():
    print("=" * 60)
    print("基于试次分配方案生成模拟 Necker 立方体实验数据")
    print("=" * 60)

    alloc_path = Path("data") / "necker_trial_allocation.csv"
    if not alloc_path.exists():
        print(f"错误：未找到 {alloc_path}，请先运行 scripts/paperX_necker_trial_allocation.py")
        return

    allocation = pd.read_csv(alloc_path)
    print(f"\n已读取试次分配表：{len(allocation)} 个 |δ| 等级")
    print(f"每符号方向总试次数：{allocation['n_trials_per_sign'].sum()}")

    n_subjects = 24
    df = generate_trial_records(allocation, n_subjects=n_subjects, seed=2026)

    print(f"\n生成数据集：{n_subjects} 被试，{len(df)} 总试次")
    print(f"字段数：{len(df.columns)}")

    # 数据验证
    print("\n数据验证：")
    print(f"  RT 范围：[{df['rt_ms'].min():.1f}, {df['rt_ms'].max():.1f}] ms")
    print(f"  超时试次数：{df['timed_out'].sum()}")
    print(f"  选择 A 比例：{(df['choice'] == 'A').mean():.3f}")
    print(f"  有效试次数：{df['valid'].sum()}")

    # 眼动/瞳孔噪声注入统计
    print("\n眼动/瞳孔噪声注入统计：")
    print(f"  gaze_x NaN 比例：{df['gaze_x'].isna().mean()*100:.2f}%")
    print(f"  gaze 离群点比例（|gaze|>3°）：{(df['gaze_x'].abs() > 3.0).mean()*100:.2f}%")
    print(f"  瞳孔完全缺失比例：{df['pupil_mean_mm'].isna().mean()*100:.2f}%")
    print(f"  瞳孔部分缺失比例（baseline 在但 mean NaN）：{((~df['pupil_baseline_mm'].isna()) & df['pupil_mean_mm'].isna()).mean()*100:.2f}%")
    print(f"  眨眼伪迹比例（mean/baseline < 0.5）：{(df['pupil_mean_mm'] / df['pupil_baseline_mm'] < 0.5).mean()*100:.2f}%")
    print(f"  pupil_quality < 0.5 比例：{(df['pupil_quality'] < 0.5).mean()*100:.2f}%")
    print(f"  综合排除比例（excluded=True）：{df['excluded'].mean()*100:.2f}%")

    # 保存
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "necker_simulated_dataset.csv"
    df.to_csv(out_csv, index=False)
    print(f"\n模拟数据已保存至 {out_csv}")

    # 按 δ 汇总
    summary = (
        df.groupby("ambiguity_signed")
        .agg(
            n=("trial_id", "count"),
            p_a=("choice_encoded", lambda x: (x == 1.0).mean()),
            rt_mean=("rt_ms", "mean"),
            rt_median=("rt_ms", "median"),
            rt_std=("rt_ms", "std"),
        )
        .reset_index()
        .sort_values("ambiguity_signed")
    )
    print("\n按 δ 汇总（部分）：")
    print(summary.head(8).to_string(index=False))

    # 绘图
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    ax = axes[0]
    ax.errorbar(
        summary["ambiguity_signed"].abs(),
        summary["rt_mean"],
        yerr=summary["rt_std"],
        fmt='o',
        capsize=3,
        color='steelblue',
        ecolor='gray',
    )
    abs_deltas = summary["ambiguity_signed"].abs().values
    expected = 250.0 * abs_deltas ** (-1.2) + 400.0
    ax.plot(abs_deltas, expected, 'r--', lw=2, label="真实幂律 E[RT]")
    ax.set_xlabel("|δ|")
    ax.set_ylabel("平均 RT (ms)")
    ax.set_title("模拟 RT 随 |δ| 的变化")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.plot(summary["ambiguity_signed"], summary["p_a"], 'go-', lw=2, markersize=6)
    ax.axhline(0.5, color='gray', linestyle='--')
    ax.set_xlabel("δ")
    ax.set_ylabel("选择 A 比例")
    ax.set_title("模拟选择比例随 δ 的变化")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    fig_path = Path("figs") / "paperX_necker_simulated_dataset.png"
    fig_path.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    print(f"\n概览图已保存至 {fig_path}")


if __name__ == "__main__":
    main()
