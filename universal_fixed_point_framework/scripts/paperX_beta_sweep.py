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
# 本文件中 UFPF 相关引用数量：2
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
UFPF 多通道竞争：β（精度）扫描对比实验
=======================================

展示 §4.7 中 softmax 通道权重

    w_i(β) = exp(β·ε_i) / Σ_j exp(β·ε_j)

随精度参数 β 的变化曲线。β 对应预测编码中的 precision：
  - β → 0：熵正则主导，权重趋于均匀（低精度/高不确定性）；
  - β → ∞：预测误差主导，权重趋于 winner-take-all（高精度/低不确定性）。

本脚本固定三组典型预测误差向量，扫描 β ∈ [1e-2, 1e2]，绘制权重曲线，
验证 softmax 权重是 §4.7 变分自由能泛函的唯一极小点。

参考：
  - notes/04_lorentz_gravity/sensory_integration_time_ruler.md §4.7
  - scripts/paperX_multichannel_sensory_time_ruler.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


def softmax_weights(infos: np.ndarray, beta: float) -> np.ndarray:
    """计算 softmax 通道权重。"""
    infos = np.asarray(infos)
    max_info = np.max(infos)
    scaled = beta * (infos - max_info)
    exp = np.exp(scaled)
    return exp / (np.sum(exp) + 1e-30)


def variational_free_energy(weights: np.ndarray,
                            infos: np.ndarray,
                            beta: float) -> float:
    """
    变分自由能 F(w) = -Σ w_i·ε_i + (1/β)·Σ w_i·log w_i。
    """
    weights = np.asarray(weights)
    infos = np.asarray(infos)
    mask = weights > 1e-15
    entropy_term = 0.0
    if np.any(mask):
        entropy_term = (1.0 / beta) * np.sum(weights[mask] * np.log(weights[mask]))
    return -np.sum(weights * infos) + entropy_term


def beta_sweep(infos: np.ndarray,
               beta_range: np.ndarray) -> np.ndarray:
    """
    对给定预测误差向量 infos，扫描 beta，返回权重矩阵 weights[beta_idx, channel_idx]。
    """
    weights = []
    for beta in beta_range:
        w = softmax_weights(infos, beta)
        weights.append(w)
    return np.array(weights)


def plot_beta_sweep(scenarios: List[Tuple[str, np.ndarray]],
                    beta_range: np.ndarray,
                    save_path: str = 'figs/paperX_beta_sweep.png'):
    """绘制多组场景下的 β-权重曲线。"""
    out_dir = os.path.dirname(save_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    n = len(scenarios)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4), sharey=True)
    if n == 1:
        axes = [axes]

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for idx, (title, infos) in enumerate(scenarios):
        weights = beta_sweep(infos, beta_range)
        ax = axes[idx]
        for i in range(len(infos)):
            ax.plot(beta_range, weights[:, i], lw=2.5, color=colors[i % len(colors)],
                    label=f'通道 {i}: $\\varepsilon={infos[i]:.2f}$')
        ax.set_xscale('log')
        ax.set_xlabel('精度参数 $\\beta$')
        ax.set_ylabel('竞争权重 $w_i$')
        ax.set_title(title)
        ax.set_ylim([-0.05, 1.05])
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        # 标注低β/高β极限
        ax.axvline(x=0.1, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=10.0, color='gray', linestyle='--', alpha=0.5)
        ax.text(0.08, 0.95, '低精度\n均匀', transform=ax.get_xaxis_transform(),
                fontsize=9, ha='right', va='top', color='gray')
        ax.text(12.0, 0.95, '高精度\nWinner-take-all', transform=ax.get_xaxis_transform(),
                fontsize=9, ha='left', va='top', color='gray')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"  图已保存至 {save_path}")
    return fig


def verify_minimum(scenarios: List[Tuple[str, np.ndarray]],
                   beta_test: List[float]) -> None:
    """验证 softmax 权重最小化变分自由能。"""
    print("\n=== 变分自由能最小化验证 ===")
    for title, infos in scenarios:
        print(f"\n场景：{title}，预测误差 {infos}")
        for beta in beta_test:
            w_soft = softmax_weights(infos, beta)
            F_soft = variational_free_energy(w_soft, infos, beta)
            # 均匀权重
            w_uniform = np.ones(len(infos)) / len(infos)
            F_uniform = variational_free_energy(w_uniform, infos, beta)
            # 随机权重：随机扰动 softmax
            rng = np.random.default_rng(42)
            w_pert = w_soft + 0.1 * rng.random(len(infos))
            w_pert = w_pert / np.sum(w_pert)
            F_pert = variational_free_energy(w_pert, infos, beta)
            print(f"  β={beta:6.2f}  softmax F={F_soft:8.4f}  "
                  f"uniform F={F_uniform:8.4f}  perturbed F={F_pert:8.4f}  "
                  f"softmax 最优？{F_soft < min(F_uniform, F_pert)}")


def main():
    print("UFPF β 扫描对比实验\n" + "=" * 40)

    # 三组典型预测误差场景
    scenarios = [
        ("场景 A：单通道主导", np.array([2.0, 0.3, 0.2])),
        ("场景 B：双通道竞争", np.array([1.5, 1.4, 0.3])),
        ("场景 C：三通道均衡", np.array([1.0, 0.9, 0.8])),
    ]

    beta_range = np.logspace(-2, 2, 200)
    plot_beta_sweep(scenarios, beta_range)
    verify_minimum(scenarios, beta_test=[0.1, 1.0, 10.0])
    print("\n完成。")


if __name__ == '__main__':
    main()
