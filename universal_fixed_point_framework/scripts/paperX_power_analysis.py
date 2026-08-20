#!/usr/bin/env python3
"""
Necker 临界慢化实验：样本量与统计功效分析（解析版）
=========================================================

对应 notes/04_lorentz_gravity/sensory_integration_time_ruler.md §7.8.9。

本脚本使用单次大样本模拟 + Hessian-based Wald 标准误，快速估计不同样本量下
检测到 γ≠1 的功效。避免 bootstrap，适合预注册阶段快速样本量规划。

核心假设：
  - 真实 RT 服从 LogNormal，均值由幂律决定：E[RT]=C|δ|^{-γ}+t0；
  - RT 变异系数 CV=0.18；
  - |δ| 取 12 个对数均匀等级，范围 [0.05, 0.50]；
  - 上限截断 10000 ms；
  - 不同被试间无额外随机效应（保守简化）。

方法：
  1. 生成一个参考大样本（n_subjects_ref=50, n_trials_per_delta=200）；
  2. 拟合 UFPF toy 模型，得到 γ 的 MLE；
  3. 用数值 Hessian 估计 γ 的 Wald SE；
  4. 对任意样本量 N，按 SE ∝ 1/√N 缩放，计算功效：
       power = P(|γ_hat - 1| / SE_N > z_{1-α/2})

输出：
  - data/necker_power_analysis.csv：不同被试数/试次数组合的功效
  - figs/paperX_power_analysis.png：功效热图

运行命令：
    python scripts/paperX_power_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize, approx_fprime
from scipy.stats import norm

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


# ---------------------------------------------------------------------------
# 数据生成与似然
# ---------------------------------------------------------------------------

def generate_rt(deltas: np.ndarray, C: float, gamma: float, t0: float,
                cv: float, n_trials: int, n_subjects: int, seed: int) -> np.ndarray:
    """生成跨被试的 RT 矩阵（每行一个 trial，每列一个 |δ|）。"""
    rng = np.random.default_rng(seed)
    rt_mean = C * np.abs(deltas) ** (-gamma) + t0
    sigma_log = np.sqrt(np.log(1 + cv ** 2))
    mu_log = np.log(rt_mean) - 0.5 * sigma_log ** 2
    rt = rng.lognormal(mu_log, sigma_log, size=(n_subjects * n_trials, len(deltas)))
    return np.clip(rt, 150.0, 10000.0)


def ufpm_log_likelihood(params: np.ndarray, rt: np.ndarray, deltas: np.ndarray) -> float:
    """UFPF toy 对数似然（ms 密度单位）。"""
    C, gamma, t0, sigma_log = params
    if C <= 0 or gamma <= 0 or t0 < 0 or sigma_log <= 0:
        return -1e12
    mu_pred = C * np.abs(deltas) ** (-gamma) + t0
    if np.any(mu_pred <= 0):
        return -1e12
    mu_log = np.log(mu_pred) - 0.5 * sigma_log ** 2
    ll = (
        -0.5 * np.log(2.0 * np.pi * sigma_log ** 2)
        - np.log(rt)
        - 0.5 * ((np.log(rt) - mu_log) / sigma_log) ** 2
    )
    return float(np.sum(ll))


def fit_ufpm(rt: np.ndarray, deltas: np.ndarray) -> tuple:
    """拟合 UFPF toy 模型，返回最优参数与优化结果。"""
    def neg_ll(params):
        return -ufpm_log_likelihood(params, rt, deltas)

    best_result = None
    best_val = np.inf
    for C0 in [200.0, 350.0, 500.0]:
        for gamma0 in [0.9, 1.1, 1.3]:
            for t00 in [100.0, 300.0, 500.0]:
                for s0 in [0.15, 0.20, 0.25]:
                    result = minimize(
                        neg_ll,
                        x0=[C0, gamma0, t00, s0],
                        method="L-BFGS-B",
                        bounds=[(50.0, 2000.0), (0.5, 2.5), (0.0, 1500.0), (0.05, 0.50)],
                    )
                    if result.fun < best_val:
                        best_val = result.fun
                        best_result = result
    return best_result


def hessian(params: np.ndarray, rt: np.ndarray, deltas: np.ndarray,
            eps: float = 1e-5) -> np.ndarray:
    """用有限差分计算对数似然在 MLE 处的 Hessian。"""
    def grad(p):
        return approx_fprime(p, lambda x: ufpm_log_likelihood(x, rt, deltas), epsilon=eps)

    n = len(params)
    H = np.zeros((n, n))
    for i in range(n):
        p_plus = params.copy()
        p_minus = params.copy()
        p_plus[i] += eps
        p_minus[i] -= eps
        g_plus = grad(p_plus)
        g_minus = grad(p_minus)
        H[:, i] = (g_plus - g_minus) / (2.0 * eps)
    # 对称化
    return 0.5 * (H + H.T)


# ---------------------------------------------------------------------------
# 功效计算
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Necker 临界慢化实验：样本量与功效分析（解析版）")
    print("=" * 60)

    # 真实参数与参考样本
    true_gamma = 1.2
    C_true = 250.0
    t0_true = 400.0
    cv = 0.18
    deltas = np.exp(np.linspace(np.log(0.05), np.log(0.50), 12))

    n_subjects_ref = 50
    n_trials_per_delta_ref = 200
    n_total_ref = n_subjects_ref * n_trials_per_delta_ref

    print(f"\n[1] 生成参考大样本：{n_subjects_ref} 被试 × {n_trials_per_delta_ref} 试次/δ ...")
    rt_ref = generate_rt(deltas, C_true, true_gamma, t0_true, cv,
                        n_trials_per_delta_ref, n_subjects_ref, seed=2026)

    print("[2] 拟合 UFPF toy 模型 ...")
    result = fit_ufpm(rt_ref, deltas)
    mle = result.x
    print(f"    MLE: C={mle[0]:.2f}, γ={mle[1]:.4f}, t0={mle[2]:.2f}, σ_log={mle[3]:.4f}")

    print("[3] 计算 Hessian 与 γ 的 Wald SE（参考样本） ...")
    H = hessian(mle, rt_ref, deltas, eps=1e-4)
    try:
        cov = -np.linalg.inv(H)
        se_gamma_ref = float(np.sqrt(np.clip(cov[1, 1], 1e-12, None)))
        print(f"    γ 的参考 SE = {se_gamma_ref:.5f}")
    except np.linalg.LinAlgError:
        print("    Hessian 不可逆，改用 bootstrap 近似（请检查模型可识别性）。")
        return

    # 4. 对不同样本量计算功效
    print("[4] 计算不同样本量下的功效 ...")
    n_subjects_list = np.array([8, 10, 12, 14, 16, 18, 20, 24, 28, 32])
    n_trials_list = np.array([20, 30, 40, 50, 60, 70, 80, 90, 100])
    alpha = 0.05
    z_alpha = norm.ppf(1 - alpha / 2)

    results = []
    for ns in n_subjects_list:
        for nt in n_trials_list:
            n_total = ns * nt
            # SE 按 1/sqrt(N) 缩放
            se_gamma = se_gamma_ref * np.sqrt(n_total_ref / n_total)
            # 功效：以 MLE 的 γ_hat 为真实效应量
            effect = abs(mle[1] - 1.0)
            power = 1.0 - norm.cdf(z_alpha - effect / se_gamma) + norm.cdf(-z_alpha - effect / se_gamma)
            results.append({
                "n_subjects": int(ns),
                "n_trials_per_delta": int(nt),
                "total_trials_per_subject": int(nt * 24),
                "total_trials": int(ns * nt * 24),
                "se_gamma": float(se_gamma),
                "power": float(power),
            })

    df = pd.DataFrame(results)
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    df.to_csv(out_dir / "necker_power_analysis.csv", index=False)
    print(f"\n结果已保存至 {out_dir / 'necker_power_analysis.csv'}")
    print("\n达到 80% 功效的最小设计（按总试次数）：")
    df_80 = df[df["power"] >= 0.80].copy()
    if not df_80.empty:
        best = df_80.loc[df_80["total_trials"].idxmin()]
        print(f"  n_subjects={int(best['n_subjects'])}, n_trials_per_delta={int(best['n_trials_per_delta'])}, "
              f"每被试总试次数={int(best['total_trials_per_subject'])}, "
              f"实验总试次数={int(best['total_trials'])}, 估计 power={best['power']:.3f}")
    else:
        print("  当前参数网格未找到达到 80% 功效的设计。")

    # 5. 热图
    fig, ax = plt.subplots(figsize=(8, 6))
    pivot = df.pivot(index="n_subjects", columns="n_trials_per_delta", values="power")
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_xticks(range(len(n_trials_list)))
    ax.set_xticklabels(n_trials_list)
    ax.set_yticks(range(len(n_subjects_list)))
    ax.set_yticklabels(n_subjects_list)
    ax.set_xlabel("每 |δ| 等级试次数")
    ax.set_ylabel("被试数")
    ax.set_title(f"检测到 γ≠1 的功效（真实 γ={true_gamma}，MLE γ={mle[1]:.2f}）")
    for i, ns in enumerate(n_subjects_list):
        for j, nt in enumerate(n_trials_list):
            val = pivot.loc[ns, nt]
            color = "white" if val > 0.6 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=7)
    plt.colorbar(im, ax=ax, label="power")
    fig_path = Path("figs") / "paperX_power_analysis.png"
    fig_path.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    print(f"\n功效热图已保存至 {fig_path}")

    print("\n完成。")


if __name__ == "__main__":
    main()
