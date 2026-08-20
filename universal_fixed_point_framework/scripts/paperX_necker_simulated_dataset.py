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


def generate_trial_records(
    allocation: pd.DataFrame,
    n_subjects: int = 24,
    true_gamma: float = 1.2,
    true_C: float = 250.0,
    true_t0: float = 400.0,
    rt_cv: float = 0.18,
    choice_slope: float = 8.0,
    seed: int = 2026,
) -> pd.DataFrame:
    """
    根据试次分配表生成模拟实验数据。

    参数：
      n_subjects: 被试数
      true_gamma, true_C, true_t0: 幂律 RT 参数
      rt_cv: RT 对数正态变异系数
      choice_slope: 选择概率 sigmoid 斜率
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
