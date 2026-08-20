#!/usr/bin/env python3
"""
Necker 临界慢化实验：样本量与统计功效分析
================================================

对应 notes/04_lorentz_gravity/sensory_integration_time_ruler.md §7.8.9。

本脚本通过模拟估计：在给定被试数、每 δ 试次数、真实 γ 等条件下，
UFPF toy 模型能否以 80% 功效检测到 γ 显著偏离 1（即拒绝标准 DDM 的 γ=1 预测）。

假设：
  - 真实 RT 服从 LogNormal，均值由幂律决定：E[RT]=C|δ|^{-γ}+t0；
  - RT 变异系数 CV=0.18；
  - |δ| 取 12 个对数均匀等级，范围 [0.05, 0.50]；
  - 上限截断 10000 ms（保守估计）。

输出：
  - data/necker_power_analysis.csv：各参数组合的功效、γ 平均估计、偏差
  - figs/paperX_power_analysis.png：功效热图

运行命令：
    python scripts/paperX_power_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


def generate_rt(deltas: np.ndarray, C: float, gamma: float, t0: float,
                cv: float, n_trials: int, seed: int) -> np.ndarray:
    """为给定 δ 数组生成 n_trials 个 RT（ms）。"""
    rng = np.random.default_rng(seed)
    rt_mean = C * np.abs(deltas) ** (-gamma) + t0
    sigma_log = np.sqrt(np.log(1 + cv ** 2))
    mu_log = np.log(rt_mean) - 0.5 * sigma_log ** 2
    rt = rng.lognormal(mu_log, sigma_log, size=(n_trials, len(deltas)))
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


def fit_ufpm(rt: np.ndarray, deltas: np.ndarray) -> tuple[float, ...]:
    """拟合 UFPF toy 模型，返回 (C, gamma, t0, sigma_log)。"""
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
    return tuple(best_result.x)


def bootstrap_gamma_ci(
    rt: np.ndarray,
    deltas: np.ndarray,
    n_bootstrap: int = 200,
    seed: int = 42,
    ci: float = 0.95,
) -> tuple[float, float]:
    """用 bootstrap 估计 γ 的置信区间。"""
    rng = np.random.default_rng(seed)
    n_trials = rt.shape[0]
    gammas = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n_trials, size=n_trials)
        rt_boot = rt[idx, :]
        _, gamma, _, _ = fit_ufpm(rt_boot, deltas)
        gammas.append(gamma)
    gammas = np.array(gammas)
    alpha = (1 - ci) / 2
    return float(np.percentile(gammas, 100 * alpha)), float(np.percentile(gammas, 100 * (1 - alpha)))


def estimate_power(
    n_subjects: int,
    n_trials_per_delta: int,
    true_gamma: float = 1.2,
    C: float = 250.0,
    t0: float = 400.0,
    cv: float = 0.18,
    n_simulations: int = 100,
    seed_offset: int = 0,
) -> dict:
    """
    估计在 n_subjects、n_trials_per_delta 下的功效。
    功效 = 检测到 γ 的 95% CI 不包含 1 的比例。
    为节省计算，每个被试的 δ 等级相同，跨被试汇总后 bootstrap。
    """
    rng = np.random.default_rng(2026 + seed_offset)
    deltas = np.exp(np.linspace(np.log(0.05), np.log(0.50), 12))

    detections = 0
    gamma_estimates = []
    for sim in range(n_simulations):
        # 汇总所有被试的 RT
        all_rt = []
        for s in range(n_subjects):
            rt = generate_rt(deltas, C, true_gamma, t0, cv, n_trials_per_delta,
                            seed=rng.integers(0, 1_000_000))
            all_rt.append(rt)
        rt_all = np.vstack(all_rt)

        _, gamma_hat, _, _ = fit_ufpm(rt_all, deltas)
        gamma_estimates.append(gamma_hat)

        # bootstrap CI（为速度仅做 100 次）
        lo, hi = bootstrap_gamma_ci(rt_all, deltas, n_bootstrap=100, seed=rng.integers(0, 1_000_000))
        if lo > 1.0 or hi < 1.0:
            detections += 1

    return {
        "power": detections / n_simulations,
        "gamma_mean": float(np.mean(gamma_estimates)),
        "gamma_std": float(np.std(gamma_estimates)),
        "gamma_median": float(np.median(gamma_estimates)),
    }


def main():
    print("=" * 60)
    print("Necker 临界慢化实验：样本量与功效分析")
    print("=" * 60)
    print("（注意：为控制计算时间，模拟次数较少，结果仅供参考）\n")

    # 参数网格
    n_subjects_list = [5, 8, 12, 16, 20]
    n_trials_list = [20, 40, 60, 80, 100]

    results = []
    for n_subjects in n_subjects_list:
        for n_trials in n_trials_list:
            print(f"计算：n_subjects={n_subjects}, n_trials_per_delta={n_trials} ...")
            res = estimate_power(
                n_subjects=n_subjects,
                n_trials_per_delta=n_trials,
                true_gamma=1.2,
                C=250.0,
                t0=400.0,
                cv=0.18,
                n_simulations=50,  # 小样本模拟以控制时间
                seed_offset=n_subjects * 1000 + n_trials,
            )
            results.append({
                "n_subjects": n_subjects,
                "n_trials_per_delta": n_trials,
                "total_trials_per_subject": n_trials * 24,  # 12 |δ| × 2 sign
                **res,
            })

    df = pd.DataFrame(results)
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    df.to_csv(out_dir / "necker_power_analysis.csv", index=False)
    print(f"\n结果已保存至 {out_dir / 'necker_power_analysis.csv'}")
    print("\n部分结果：")
    print(df.head(10).to_string(index=False))

    # 找出达到 80% 功效的最小总试次数
    df_80 = df[df["power"] >= 0.80].copy()
    if not df_80.empty:
        df_80["total_trials"] = df_80["n_subjects"] * df_80["total_trials_per_subject"]
        best = df_80.loc[df_80["total_trials"].idxmin()]
        print(f"\n达到 80% 功效的最小设计：")
        print(f"  n_subjects={int(best['n_subjects'])}, n_trials_per_delta={int(best['n_trials_per_delta'])}, "
              f"每被试总试次数={int(best['total_trials_per_subject'])}, 总试次数={int(best['total_trials'])}")
    else:
        print("\n当前参数网格未找到达到 80% 功效的设计。")

    # 热图
    fig, ax = plt.subplots(figsize=(7, 5))
    pivot = df.pivot(index="n_subjects", columns="n_trials_per_delta", values="power")
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_xticks(range(len(n_trials_list)))
    ax.set_xticklabels(n_trials_list)
    ax.set_yticks(range(len(n_subjects_list)))
    ax.set_yticklabels(n_subjects_list)
    ax.set_xlabel("每 δ 等级试次数")
    ax.set_ylabel("被试数")
    ax.set_title("检测到 γ≠1 的功效（真实 γ=1.2）")
    for i, ns in enumerate(n_subjects_list):
        for j, nt in enumerate(n_trials_list):
            val = pivot.loc[ns, nt]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color="black", fontsize=8)
    plt.colorbar(im, ax=ax, label="power")
    fig_path = Path("figs") / "paperX_power_analysis.png"
    fig_path.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    print(f"\n功效热图已保存至 {fig_path}")


if __name__ == "__main__":
    main()
