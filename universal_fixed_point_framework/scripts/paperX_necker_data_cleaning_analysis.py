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
# 本文件中 UFPF 相关引用数量：9
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
含噪声 Necker 模拟数据的清洗、建模与稳健性分析
=====================================================

对应 notes/04_lorentz_gravity/prereg_necker_critical_slowing.md。

输入：
  - data/necker_simulated_dataset.csv

输出：
  - data/necker_cleaned_analysis_results.csv：清洗后按被试-δ 汇总数据
  - data/necker_cleaning_model_comparison.csv：UFPF toy vs DDM 拟合结果
  - figs/paperX_necker_cleaning_analysis.png：清洗前后 RT 曲线与模型拟合图

运行命令：
    python scripts/paperX_necker_data_cleaning_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


# ===========================================================================
# 数据清洗
# ===========================================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    应用预注册 §5 的清洗规则：
      - excluded=False
      - 200 <= RT <= 10000 ms
      - pupil_quality >= 0.5
      - gaze_x/y 非 NaN
    """
    mask = (
        (~df["excluded"])
        & (df["rt_ms"] >= 200.0)
        & (df["rt_ms"] <= 10000.0)
        & (df["pupil_quality"] >= 0.5)
        & (~df["gaze_x"].isna())
        & (~df["gaze_y"].isna())
    )
    return df[mask].copy()


def summarize_by_subject_delta(df: pd.DataFrame) -> pd.DataFrame:
    """按被试和 δ 汇总平均 RT、选择比例等。"""
    summary = (
        df.groupby(["subject_id", "ambiguity_signed"])
        .agg(
            n=("trial_id", "count"),
            rt_mean=("rt_ms", "mean"),
            rt_median=("rt_ms", "median"),
            rt_std=("rt_ms", "std"),
            rt_log_mean=("rt_ms", lambda x: np.log(x).mean()),
            rt_log_std=("rt_ms", lambda x: np.log(x).std()),
            p_a=("choice_encoded", lambda x: (x == 1.0).mean()),
            ambiguity=("ambiguity", "first"),
        )
        .reset_index()
    )
    return summary


def collapse_across_subjects(summary: pd.DataFrame) -> pd.DataFrame:
    """跨被试平均（固定效应聚合）。"""
    agg = (
        summary.groupby("ambiguity_signed")
        .agg(
            n_subjects=("subject_id", "nunique"),
            n_trials=("n", "sum"),
            rt_mean=("rt_mean", "mean"),
            rt_std=("rt_mean", "std"),
            rt_sem=("rt_mean", lambda x: x.std() / np.sqrt(len(x))),
            p_a=("p_a", "mean"),
            ambiguity=("ambiguity", "first"),
        )
        .reset_index()
    )
    return agg


# ===========================================================================
# UFPF toy 模型
# ===========================================================================

def ufpm_log_likelihood(params: np.ndarray, rt: np.ndarray, deltas: np.ndarray) -> float:
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


def fit_ufpm(rt: np.ndarray, deltas: np.ndarray):
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


# ===========================================================================
# DDM（Navarro & Fuss 2009 解析 PDF）
# ===========================================================================

def ddm_pdf(t: np.ndarray, v: np.ndarray, a: float, z: float, eps: float = 1e-20) -> np.ndarray:
    """
    简单 DDM 第一通过时间 PDF（上边界 A）。
    参数：
        t : 决策时间数组（秒），必须 > 0
        v : 漂移率数组（1/秒），与 t 同形状
        a : 边界间距（证据单位）
        z : 起始点比例，0<z<1，起始位置 = a*z
    返回：
        f_A(t | v, a, z)
    下边界 PDF 可通过 f_B(t) = f_A(t | -v, a, 1-z) 获得。
    """
    t = np.asarray(t, dtype=float)
    v = np.asarray(v, dtype=float)
    pdf = np.zeros_like(t, dtype=float)

    z_eff = min(z, 1.0 - z)
    threshold = 0.5 * a ** 2 * z_eff ** 2
    threshold = max(threshold, 1e-4)
    small_mask = t < threshold
    large_mask = ~small_mask

    if small_mask.any():
        ts = t[small_mask]
        vs = v[small_mask]
        s = np.zeros_like(ts)
        for k in range(-20, 21):
            ak = a * z + 2 * k * a
            s += (z + 2 * k) * np.exp(-(ak ** 2) / (2.0 * ts))
        pdf[small_mask] = (
            a / np.sqrt(2.0 * np.pi * ts ** 3)
            * np.exp(-vs * a * z - 0.5 * vs ** 2 * ts)
            * s
        )

    if large_mask.any():
        tl = t[large_mask]
        vl = v[large_mask]
        s = np.zeros_like(tl)
        for k in range(1, 50):
            s += k * np.sin(k * np.pi * z) * np.exp(-(k ** 2) * (np.pi ** 2) * tl / (2.0 * a ** 2))
        pdf[large_mask] = (
            np.pi / (a ** 2)
            * np.exp(-vl * a * z - 0.5 * vl ** 2 * tl)
            * s
        )

    return np.maximum(pdf, eps)


def ddm_log_likelihood(params: np.ndarray, rt_ms: np.ndarray, delta: np.ndarray, choices: np.ndarray) -> float:
    """
    DDM 完整对数似然。
    参数顺序：[k, a, z, t0_ms]。
    漂移率 v(δ) = k * δ；t0 以 ms 传入，内部转换为秒。
    """
    k, a, z, t0_ms = params
    if k <= 0 or a <= 0.01 or z <= 0.01 or z >= 0.99 or t0_ms < 0:
        return -1e12

    t0 = t0_ms / 1000.0
    rt_s = rt_ms / 1000.0 - t0
    rt_s = np.maximum(rt_s, 1e-6)
    v = k * delta
    choice = choices  # +1 = A, -1 = B

    pdf_a = ddm_pdf(rt_s, v, a, z)
    pdf_b = ddm_pdf(rt_s, -v, a, 1.0 - z)

    log_pdf = np.where(choice == 1, np.log(pdf_a), np.log(pdf_b))
    # 单位转换：DDM PDF 以 1/秒为单位；观测 RT 以 ms 为单位。
    n_trials = len(rt_ms)
    return float(np.sum(log_pdf) - n_trials * np.log(1000.0))


def fit_ddm(rt_ms: np.ndarray, delta: np.ndarray, choices: np.ndarray, seed: int = 2026, max_n: int = 10000):
    """
    对 DDM 进行子采样拟合以控制计算时间。
    max_n：用于拟合的最大试次数（随机子采样）。
    """
    rng = np.random.default_rng(seed)
    n = len(rt_ms)
    if n > max_n:
        idx = rng.choice(n, size=max_n, replace=False)
        rt_ms = rt_ms[idx]
        delta = delta[idx]
        choices = choices[idx]

    def neg_ll(params):
        return -ddm_log_likelihood(params, rt_ms, delta, choices)

    best_result = None
    best_val = np.inf
    for k0 in [0.02, 0.05, 0.10, 0.20]:
        for a0 in [1.5, 2.5, 3.5]:
            for z0 in [0.5]:
                for t00 in [300.0, 400.0, 500.0]:
                    result = minimize(
                        neg_ll,
                        x0=[k0, a0, z0, t00],
                        method="L-BFGS-B",
                        bounds=[(0.001, 2.0), (0.5, 5.0), (0.45, 0.55), (100.0, 800.0)],
                    )
                    if result.fun < best_val:
                        best_val = result.fun
                        best_result = result
    return best_result


# ===========================================================================
# 主流程
# ===========================================================================

def main():
    print("=" * 60)
    print("含噪声 Necker 模拟数据：清洗、建模与稳健性分析")
    print("=" * 60)

    data_path = Path("data") / "necker_simulated_dataset.csv"
    if not data_path.exists():
        print(f"错误：未找到 {data_path}")
        return

    df = pd.read_csv(data_path, low_memory=False)
    print(f"\n原始数据：{len(df)} 试次")

    df_clean = clean_data(df)
    print(f"清洗后数据：{len(df_clean)} 试次（保留率 {len(df_clean)/len(df)*100:.2f}%）")
    print(f"排除原因分布：")
    excluded = df[df["excluded"]]
    print(f"  excluded=True：{len(excluded)} ({len(excluded)/len(df)*100:.2f}%)")

    # 按被试-δ 汇总
    sub_summary = summarize_by_subject_delta(df_clean)
    agg = collapse_across_subjects(sub_summary)

    print(f"\n清洗后 δ 等级数：{agg['ambiguity_signed'].nunique()}")
    print(f"每 δ 平均被试数：{agg['n_subjects'].mean():.1f}")

    # 统一模型比较子样本，避免 AIC/BIC 因样本量不同而失真
    rng_cmp = np.random.default_rng(2026)
    cmp_n = 10000
    cmp_idx = rng_cmp.choice(len(df_clean), size=cmp_n, replace=False)
    rt_cmp = df_clean.iloc[cmp_idx]["rt_ms"].to_numpy()
    delta_cmp = df_clean.iloc[cmp_idx]["ambiguity_signed"].to_numpy()
    choices_cmp = df_clean.iloc[cmp_idx]["choice_encoded"].to_numpy()

    # UFPF 拟合：使用完整清洗数据估计参数，但在统一子样本上评估似然
    rt_vec = df_clean["rt_ms"].to_numpy()
    delta_vec = df_clean["ambiguity_signed"].to_numpy()
    ufpm_result = fit_ufpm(rt_vec, delta_vec)
    C_hat, gamma_hat, t0_hat, sigma_hat = ufpm_result.x
    logL_ufpm_full = -ufpm_result.fun
    # 统一子样本上的对数似然
    logL_ufpm = ufpm_log_likelihood(ufpm_result.x, rt_cmp, delta_cmp)
    k_ufpm = 4
    aic_ufpm = 2 * k_ufpm - 2 * logL_ufpm
    bic_ufpm = k_ufpm * np.log(cmp_n) - 2 * logL_ufpm

    print("\n[UFPF toy 模型拟合结果]")
    print(f"  C = {C_hat:.2f} ms（真实 250.00）")
    print(f"  γ = {gamma_hat:.4f}（真实 1.2000）")
    print(f"  t0 = {t0_hat:.2f} ms（真实 400.00）")
    print(f"  σ_log = {sigma_hat:.4f}（真实约 {np.sqrt(np.log(1+0.18**2)):.4f}）")
    print(f"  全样本 log L = {logL_ufpm_full:.2f}")
    print(f"  比较子样本 log L = {logL_ufpm:.2f}, AIC = {aic_ufpm:.2f}, BIC = {bic_ufpm:.2f}")

    # DDM 拟合（在统一子样本上）
    ddm_result = fit_ddm(rt_cmp, delta_cmp, choices_cmp)
    k_hat, a_hat, z_hat, t0_ddm = ddm_result.x
    logL_ddm = -ddm_result.fun
    aic_ddm = 2 * 4 - 2 * logL_ddm
    bic_ddm = 4 * np.log(cmp_n) - 2 * logL_ddm

    print("\n[标准 DDM 拟合结果]")
    print(f"  k = {k_hat:.4f}")
    print(f"  a = {a_hat:.4f}")
    print(f"  z = {z_hat:.4f}")
    print(f"  t0 = {t0_ddm:.2f} ms")
    print(f"  log L = {logL_ddm:.2f}, AIC = {aic_ddm:.2f}, BIC = {bic_ddm:.2f}")

    delta_aic = aic_ddm - aic_ufpm
    print(f"\n[模型比较]")
    print(f"  ΔAIC = AIC_DDM - AIC_UFPF = {delta_aic:.2f}")
    print(f"  ΔBIC = {bic_ddm - bic_ufpm:.2f}")

    # 保存汇总结果
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    agg.to_csv(out_dir / "necker_cleaned_analysis_results.csv", index=False)
    pd.DataFrame({
        "model": ["UFPF_toy", "DDM"],
        "C_or_k": [C_hat, k_hat],
        "gamma_or_a": [gamma_hat, a_hat],
        "t0_ms": [t0_hat, t0_ddm],
        "sigma_or_z": [sigma_hat, z_hat],
        "logL": [logL_ufpm, logL_ddm],
        "AIC": [aic_ufpm, aic_ddm],
        "BIC": [bic_ufpm, bic_ddm],
    }).to_csv(out_dir / "necker_cleaning_model_comparison.csv", index=False)

    print(f"\n结果已保存至：")
    print(f"  {out_dir / 'necker_cleaned_analysis_results.csv'}")
    print(f"  {out_dir / 'necker_cleaning_model_comparison.csv'}")

    # 绘图
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    ax = axes[0]
    abs_delta = agg["ambiguity_signed"].abs()
    ax.errorbar(abs_delta, agg["rt_mean"], yerr=agg["rt_sem"], fmt='o', capsize=3, label="清洗后数据", color='steelblue')

    d_fine = np.linspace(abs_delta.min(), abs_delta.max(), 200)
    rt_pred = C_hat * d_fine ** (-gamma_hat) + t0_hat
    ax.plot(d_fine, rt_pred, 'r--', lw=2, label=f"UFPF 拟合 γ={gamma_hat:.3f}")
    ax.plot(d_fine, 250 * d_fine ** (-1.2) + 400, 'k:', lw=1.5, label="真实生成曲线")
    ax.set_xlabel("|δ|")
    ax.set_ylabel("平均 RT (ms)")
    ax.set_title("清洗后数据与 UFPF 拟合")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.bar(["UFPF toy", "DDM"], [aic_ufpm, aic_ddm], color=['steelblue', 'coral'])
    ax.set_ylabel("AIC")
    ax.set_title("模型比较（AIC 越低越好）")
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    fig_path = Path("figs") / "paperX_necker_cleaning_analysis.png"
    fig_path.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    print(f"\n分析图已保存至 {fig_path}")


if __name__ == "__main__":
    main()
