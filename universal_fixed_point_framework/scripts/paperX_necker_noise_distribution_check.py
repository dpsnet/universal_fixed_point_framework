#!/usr/bin/env python3
"""
Necker 模拟数据：眼动与瞳孔噪声分布特征检查
===================================================

对应 notes/04_lorentz_gravity/prereg_necker_critical_slowing.md。

输入：
  - data/necker_simulated_dataset.csv

输出：
  - data/necker_noise_distribution_check.csv：各噪声类型的统计摘要
  - figs/paperX_necker_noise_distribution.png：噪声分布可视化

运行命令：
    python scripts/paperX_necker_noise_distribution_check.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


def check_gaze_distribution(df: pd.DataFrame) -> dict:
    """检查注视点分布与典型眼动仪精度对比。"""
    valid_gaze = df.dropna(subset=["gaze_x", "gaze_y"])
    rms = np.sqrt((valid_gaze["gaze_x"]**2 + valid_gaze["gaze_y"]**2).mean())
    std_x = valid_gaze["gaze_x"].std()
    std_y = valid_gaze["gaze_y"].std()
    offscreen_rate = df["gaze_x"].isna().mean()
    outlier_rate = (valid_gaze["gaze_x"].abs() > 3.0).mean()
    return {
        "n_valid": len(valid_gaze),
        "mean_x": valid_gaze["gaze_x"].mean(),
        "mean_y": valid_gaze["gaze_y"].mean(),
        "std_x": std_x,
        "std_y": std_y,
        "rms_error_deg": rms,
        "offscreen_rate": offscreen_rate,
        "outlier_rate_gt3deg": outlier_rate,
    }


def check_pupil_distribution(df: pd.DataFrame) -> dict:
    """检查瞳孔测量值分布与典型瞳孔仪精度对比。"""
    baseline = df["pupil_baseline_mm"]
    mean = df["pupil_mean_mm"]
    peak = df["pupil_peak_mm"]

    stats = {
        "baseline_mean": baseline.mean(),
        "baseline_std": baseline.std(),
        "mean_pupil_diameter_mm": mean.mean(),
        "peak_pupil_diameter_mm": peak.mean(),
        "mean_std": mean.std(),
        "peak_std": peak.std(),
        "complete_dropout_rate": mean.isna().mean(),
        "partial_missing_rate": ((~baseline.isna()) & mean.isna()).mean(),
        "blink_artifact_rate": (mean / baseline < 0.5).mean(),
        "quality_mean": df["pupil_quality"].mean(),
        "quality_lt_0.5_rate": (df["pupil_quality"] < 0.5).mean(),
    }
    return stats


def compare_to_real_world(checks: dict) -> pd.DataFrame:
    """与真实实验中常见的眼动/瞳孔测量误差范围做对比。"""
    rows = [
        {
            "指标": "注视点 RMS 误差",
            "模拟值": f"{checks['gaze']['rms_error_deg']:.3f}°",
            "典型真实范围": "0.3°–1.0°",
            "结论": "符合" if 0.3 <= checks['gaze']['rms_error_deg'] <= 1.0 else "偏低/偏高",
        },
        {
            "指标": "gaze 离屏率",
            "模拟值": f"{checks['gaze']['offscreen_rate']*100:.2f}%",
            "典型真实范围": "2%–10%",
            "结论": "符合" if 0.02 <= checks['gaze']['offscreen_rate'] <= 0.10 else "偏低/偏高",
        },
        {
            "指标": "瞳孔完全缺失率",
            "模拟值": f"{checks['pupil']['complete_dropout_rate']*100:.2f}%",
            "典型真实范围": "5%–20%",
            "结论": "符合" if 0.05 <= checks['pupil']['complete_dropout_rate'] <= 0.20 else "偏低/偏高",
        },
        {
            "指标": "瞳孔部分缺失率",
            "模拟值": f"{checks['pupil']['partial_missing_rate']*100:.2f}%",
            "典型真实范围": "5%–15%",
            "结论": "符合" if 0.05 <= checks['pupil']['partial_missing_rate'] <= 0.15 else "偏低/偏高",
        },
        {
            "指标": "眨眼伪迹率",
            "模拟值": f"{checks['pupil']['blink_artifact_rate']*100:.2f}%",
            "典型真实范围": "1%–5%",
            "结论": "符合" if 0.01 <= checks['pupil']['blink_artifact_rate'] <= 0.05 else "偏低/偏高",
        },
        {
            "指标": "瞳孔质量 < 0.5 比例",
            "模拟值": f"{checks['pupil']['quality_lt_0.5_rate']*100:.2f}%",
            "典型真实范围": "5%–15%",
            "结论": "符合" if 0.05 <= checks['pupil']['quality_lt_0.5_rate'] <= 0.15 else "偏低/偏高",
        },
        {
            "指标": "综合排除率",
            "模拟值": f"{checks['overall_exclusion_rate']*100:.2f}%",
            "典型真实范围": "10%–25%",
            "结论": "符合" if 0.10 <= checks['overall_exclusion_rate'] <= 0.25 else "偏低/偏高",
        },
    ]
    return pd.DataFrame(rows)


def main():
    print("=" * 60)
    print("Necker 模拟数据：眼动与瞳孔噪声分布特征检查")
    print("=" * 60)

    data_path = Path("data") / "necker_simulated_dataset.csv"
    if not data_path.exists():
        print(f"错误：未找到 {data_path}")
        return

    df = pd.read_csv(data_path, low_memory=False)
    print(f"\n加载数据：{len(df)} 试次")

    checks = {
        "gaze": check_gaze_distribution(df),
        "pupil": check_pupil_distribution(df),
        "overall_exclusion_rate": df["excluded"].mean(),
    }

    print("\n[眼动噪声分布]")
    for k, v in checks["gaze"].items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")

    print("\n[瞳孔噪声分布]")
    for k, v in checks["pupil"].items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")

    print(f"\n[综合排除率] {checks['overall_exclusion_rate']*100:.2f}%")

    comparison = compare_to_real_world(checks)
    print("\n[与真实实验测量误差范围对比]")
    print(comparison.to_string(index=False))

    # 保存统计摘要
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    comparison.to_csv(out_dir / "necker_noise_distribution_check.csv", index=False)
    print(f"\n噪声分布检查摘要已保存至 {out_dir / 'necker_noise_distribution_check.csv'}")

    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))

    valid_gaze = df.dropna(subset=["gaze_x", "gaze_y"])
    ax = axes[0, 0]
    ax.hist2d(valid_gaze["gaze_x"], valid_gaze["gaze_y"], bins=50, cmap="Blues")
    ax.set_xlabel("gaze_x (deg)")
    ax.set_ylabel("gaze_y (deg)")
    ax.set_title("注视点 2D 分布")
    ax.set_aspect("equal")

    ax = axes[0, 1]
    ax.hist(valid_gaze["gaze_x"], bins=80, color="steelblue", edgecolor="k", alpha=0.7)
    ax.axvline(0, color="red", linestyle="--")
    ax.set_xlabel("gaze_x (deg)")
    ax.set_ylabel("频数")
    ax.set_title("gaze_x 边缘分布")

    ax = axes[0, 2]
    ax.hist(valid_gaze["gaze_y"], bins=80, color="steelblue", edgecolor="k", alpha=0.7)
    ax.axvline(0, color="red", linestyle="--")
    ax.set_xlabel("gaze_y (deg)")
    ax.set_ylabel("频数")
    ax.set_title("gaze_y 边缘分布")

    ax = axes[1, 0]
    valid_pupil = df.dropna(subset=["pupil_baseline_mm"])
    ax.hist(valid_pupil["pupil_baseline_mm"], bins=80, color="coral", edgecolor="k", alpha=0.7)
    ax.set_xlabel("pupil_baseline_mm")
    ax.set_ylabel("频数")
    ax.set_title("瞳孔基线直径分布")

    ax = axes[1, 1]
    valid_mean = df.dropna(subset=["pupil_mean_mm"])
    ax.hist(valid_mean["pupil_mean_mm"], bins=80, color="coral", edgecolor="k", alpha=0.7)
    ax.set_xlabel("pupil_mean_mm")
    ax.set_ylabel("频数")
    ax.set_title("瞳孔平均直径分布")

    ax = axes[1, 2]
    ax.hist(df["pupil_quality"], bins=50, color="green", edgecolor="k", alpha=0.7)
    ax.axvline(0.5, color="red", linestyle="--", label="quality=0.5")
    ax.set_xlabel("pupil_quality")
    ax.set_ylabel("频数")
    ax.set_title("瞳孔质量评分分布")
    ax.legend()

    plt.tight_layout()
    fig_path = Path("figs") / "paperX_necker_noise_distribution.png"
    fig_path.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    print(f"噪声分布图已保存至 {fig_path}")


if __name__ == "__main__":
    main()
