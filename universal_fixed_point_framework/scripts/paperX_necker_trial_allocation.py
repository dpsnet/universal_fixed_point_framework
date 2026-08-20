#!/usr/bin/env python3
"""
Necker 立方体临界慢化实验：临界点附近密集采样试次分配方案
==================================================================

对应 notes/04_lorentz_gravity/sensory_integration_time_ruler.md §7.8.9。

本脚本为 |δ|∈[0.05, 0.50] 区间自动生成试次分配方案，核心思想：
  - 临界点（小 |δ|）附近 RT 变化最剧烈，需要更多试次以准确估计分布尾部；
  - 远离临界点（大 |δ|）RT 变化平缓，可适当减少试次；
  - 提供多种分配策略：线性、对数、反比、自适应（基于预期 RT 方差）。

输出：
  - data/necker_trial_allocation.csv：各 δ 等级的试次数、累计试次、预期 RT、建议呈现顺序
  - 终端摘要

运行命令：
    python scripts/paperX_necker_trial_allocation.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


def generate_delta_levels(
    n_levels: int = 12,
    delta_min: float = 0.05,
    delta_max: float = 0.50,
    spacing: str = "log",
) -> np.ndarray:
    """
    生成 |δ| 等级。

    spacing 选项：
      - linear: 线性均匀分布
      - log: 对数均匀分布（默认，小 |δ| 更密集）
      - inverse: 反比分布（临界点最密）
    """
    if spacing == "linear":
        return np.linspace(delta_min, delta_max, n_levels)
    elif spacing == "log":
        return np.exp(np.linspace(np.log(delta_min), np.log(delta_max), n_levels))
    elif spacing == "inverse":
        # 反比变换：1/δ 线性，再取倒数
        inv = np.linspace(1.0 / delta_max, 1.0 / delta_min, n_levels)
        return 1.0 / inv
    else:
        raise ValueError(f"Unknown spacing: {spacing}")


def allocate_trials(
    deltas: np.ndarray,
    total_trials: int,
    strategy: str = "adaptive_rt",
    gamma: float = 1.2,
    C: float = 250.0,
    t0: float = 400.0,
) -> np.ndarray:
    """
    根据策略分配总试次数到各 δ 等级。

    strategy 选项：
      - uniform: 各等级平均分配
      - inverse_delta: 试次数 ∝ 1/|δ|，临界点更多
      - inverse_delta_sq: 试次数 ∝ 1/|δ|²
      - adaptive_rt: 试次数 ∝ 预期 RT 的方差（基于幂律模型）
    """
    deltas = np.asarray(deltas)
    if strategy == "uniform":
        weights = np.ones_like(deltas)
    elif strategy == "inverse_delta":
        weights = 1.0 / deltas
    elif strategy == "inverse_delta_sq":
        weights = 1.0 / deltas ** 2
    elif strategy == "adaptive_rt":
        # 预期 RT 均值
        rt_mean = C * deltas ** (-gamma) + t0
        # 以 RT 均值作为不确定度代理（临界点 RT 大、方差大）
        weights = rt_mean
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    # 归一化并分配整数试次数
    proportions = weights / weights.sum()
    trials = np.floor(proportions * total_trials).astype(int)

    # 处理剩余试次（由于 floor 造成的差值）
    remainder = total_trials - int(trials.sum())
    if remainder > 0:
        # 将剩余试次分配给权重最大的 remainder 个等级
        idx = np.argsort(weights)[-remainder:]
        trials[idx] += 1

    return trials


def build_allocation_table(
    deltas: np.ndarray,
    trials: np.ndarray,
    gamma: float = 1.2,
    C: float = 250.0,
    t0: float = 400.0,
) -> pd.DataFrame:
    """构建包含预期 RT 和呈现顺序建议的分配表。"""
    rt_expected = C * deltas ** (-gamma) + t0
    cumulative = np.cumsum(trials)

    # 建议呈现顺序：按 |δ| 从大到小穿插，避免长时间相邻呈现相近模糊度
    # 生成 block 内伪随机顺序索引
    rng = np.random.default_rng(2026)
    order = np.arange(len(deltas))
    rng.shuffle(order)

    df = pd.DataFrame({
        "abs_delta": np.round(deltas, 4),
        "delta_signed_neg": np.round(-deltas, 4),
        "delta_signed_pos": np.round(deltas, 4),
        "n_trials_per_sign": trials,
        "n_total_signed": trials * 2,  # 正负 δ 各一份
        "cumulative_total": cumulative * 2,
        "expected_rt_ms": np.round(rt_expected, 1),
        "presentation_block_order": order + 1,
    })
    return df


def main():
    parser = argparse.ArgumentParser(description="Necker 临界慢化试次分配")
    parser.add_argument("--n_levels", type=int, default=12, help="|δ| 等级数")
    parser.add_argument("--total_trials", type=int, default=2400, help="每符号方向总试次数（正负 δ 合计翻倍）")
    parser.add_argument("--spacing", type=str, default="log", choices=["linear", "log", "inverse"])
    parser.add_argument("--strategy", type=str, default="adaptive_rt",
                        choices=["uniform", "inverse_delta", "inverse_delta_sq", "adaptive_rt"])
    parser.add_argument("--gamma", type=float, default=1.2)
    parser.add_argument("--C", type=float, default=250.0)
    parser.add_argument("--t0", type=float, default=400.0)
    args = parser.parse_args()

    print("=" * 60)
    print("Necker 临界慢化实验：试次分配方案")
    print("=" * 60)
    print(f"参数：n_levels={args.n_levels}, total_trials_per_sign={args.total_trials}, "
          f"spacing={args.spacing}, strategy={args.strategy}")
    print(f"幂律参考：γ={args.gamma}, C={args.C} ms, t0={args.t0} ms\n")

    deltas = generate_delta_levels(args.n_levels, 0.05, 0.50, args.spacing)
    trials = allocate_trials(deltas, args.total_trials, args.strategy,
                           args.gamma, args.C, args.t0)
    df = build_allocation_table(deltas, trials, args.gamma, args.C, args.t0)

    print(df.to_string(index=False))
    print(f"\n每符号方向总试次数：{df['n_trials_per_sign'].sum()}")
    print(f"含正负 δ 总试次数：{df['n_total_signed'].sum()}")

    # 保存
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "necker_trial_allocation.csv"
    df.to_csv(out_path, index=False)
    print(f"\n分配表已保存至 {out_path}")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    ax = axes[0]
    ax.bar(df["abs_delta"], df["n_trials_per_sign"], width=0.015, color='steelblue', edgecolor='k')
    ax.set_xlabel("|δ|")
    ax.set_ylabel("每符号方向试次数")
    ax.set_title(f"试次分配策略：{args.strategy}")
    ax.grid(True, alpha=0.3, axis='y')

    ax = axes[1]
    ax.plot(df["abs_delta"], df["expected_rt_ms"], 'ro-', label="预期 RT")
    ax.set_xlabel("|δ|")
    ax.set_ylabel("预期 RT (ms)")
    ax.set_title("幂律预期 RT 参考")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    fig_path = Path("figs") / "paperX_necker_trial_allocation.png"
    fig_path.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    print(f"可视化已保存至 {fig_path}")


if __name__ == "__main__":
    main()
