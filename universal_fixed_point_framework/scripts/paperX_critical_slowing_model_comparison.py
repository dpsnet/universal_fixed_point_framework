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
# 本文件中 UFPF 相关引用数量：19
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
UFPF toy 模型 vs DDM：基于完整似然的拟合优度比较
=========================================================

对应 notes/04_lorentz_gravity/sensory_integration_time_ruler.md §7.8.7–§7.8.8。

本脚本执行：
  1. 按 §7.8 数据模板字段生成含临界慢化特征的合成数据：
       E[RT](δ) = C |δ|^{-γ} + t0，γ=1.2，RT 服从对数正态分布；
  2. UFPF toy 模型：假设 RT|δ ~ LogNormal(μ(δ), σ)，其中
       μ(δ) = log(C|δ|^{-γ} + t0) - σ²/2；
     通过最大似然估计 C, γ, t0, σ；
  3. DDM 模型：漂移率 v(δ)=k·δ，边界 a，起始点比例 z，非决策时间 t0；
     使用 Navarro & Fuss (2009) 解析第一通过时间 PDF 计算完整似然；
  4. 比较 AIC、BIC、对数似然；
  5. 绘制 RT(δ) 均值曲线、log-log 坐标图，并导出 PNG 与 SVG。

诚实边界：
  - 数据由 UFPF toy 生成，因此 UFPF 模型在期望上拟合更好；
  - 本脚本目的是演示"完整似然 + 信息准则"的比较流程，而非证明 UFPF 优于 DDM；
  - 简单 DDM（k, a, z, t0 固定）只是经典模型之一；更复杂的 DDM 扩展可能改善拟合；
  - 无数值预言。

参考：
  Navarro, D. J., & Fuss, I. G. (2009). Fast and accurate calculations for
  first-passage times in Wiener diffusion models. Journal of Mathematical
  Psychology, 53(4), 222-230.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 支持中文绘图
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


# -----------------------------------------------------------------------------
# 1. 生成含临界慢化特征的合成数据
# -----------------------------------------------------------------------------

def generate_critical_slowing_data(
    n_subjects: int = 8,
    n_trials_per_ambiguity: int = 80,
    ambiguity_levels: int = 12,
    true_gamma: float = 1.2,
    true_C: float = 250.0,
    true_t0: float = 400.0,
    rt_cv: float = 0.18,
    choice_slope: float = 8.0,
    seed: int = 2026,
) -> pd.DataFrame:
    """生成符合 §7.8 数据模板的合成数据，RT 均值满足幂律临界慢化。"""
    rng = np.random.default_rng(seed)
    deltas_pos = np.linspace(0.1, 0.5, ambiguity_levels // 2)
    deltas_neg = -np.linspace(0.1, 0.5, ambiguity_levels // 2)
    deltas = np.sort(np.concatenate([deltas_neg, deltas_pos]))

    records = []
    for s in range(n_subjects):
        subject_id = f"S{s+1:03d}"
        for d in deltas:
            for _ in range(n_trials_per_ambiguity):
                rt_mean = true_C * (abs(d) ** (-true_gamma)) + true_t0
                sigma_log = np.sqrt(np.log(1 + rt_cv ** 2))
                mu_log = np.log(rt_mean) - 0.5 * sigma_log ** 2
                rt = rng.lognormal(mu_log, sigma_log)
                rt = max(150.0, min(rt, 10000.0))

                prob_a = 1.0 / (1.0 + np.exp(-choice_slope * d))
                choice = "A" if rng.random() < prob_a else "B"
                choice_enc = 1.0 if choice == "A" else -1.0
                is_correct = pd.NA
                if d > 0.05:
                    is_correct = (choice == "A")
                elif d < -0.05:
                    is_correct = (choice == "B")

                record = {
                    "subject_id": subject_id,
                    "session_id": f"{subject_id}_01",
                    "block_id": "B01",
                    "trial_id": f"{subject_id}_{len(records):05d}",
                    "trial_number": len(records) + 1,
                    "stimulus_id": f"necker_{int((d + 0.5) * 1000):04d}",
                    "ambiguity": abs(d),
                    "ambiguity_signed": d,
                    "condition": "critical_slowing_toy",
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
                    "pupil_mean_mm": rng.normal(3.6, 0.1),
                    "pupil_peak_mm": rng.normal(3.75, 0.12),
                    "pupil_auc": rng.normal(1200.0, 100.0),
                    "pupil_quality": rng.uniform(0.9, 1.0),
                    "hr_baseline_bpm": rng.normal(72.0, 5.0),
                    "hr_mean_bpm": rng.normal(73.0, 5.0),
                    "hrv_rmssd_ms": rng.normal(45.0, 8.0),
                    "eeg_segment_id": "",
                    "eeg_epoch_quality": np.nan,
                    "alpha_power_pre": np.nan,
                    "previous_choice": rng.choice(["A", "B"]),
                    "run_length": 1,
                    "adaptation_duration_ms": 0.0,
                    "excluded": False,
                    "exclude_reason": "",
                    "valid": True,
                }
                records.append(record)

    df = pd.DataFrame(records)
    df["is_correct"] = df["is_correct"].astype("boolean")
    return df


# -----------------------------------------------------------------------------
# 2. UFPF toy 模型：对数正态似然
# -----------------------------------------------------------------------------

def ufpm_log_likelihood(params: np.ndarray, df: pd.DataFrame) -> float:
    """
    UFPF toy 模型对数似然：RT|δ ~ LogNormal(μ(δ), σ)，
    其中 exp(μ+σ²/2) = C|δ|^{-γ} + t0。
    参数顺序：[C, gamma, t0, sigma_log]。
    """
    C, gamma, t0, sigma_log = params
    if C <= 0 or gamma <= 0 or t0 < 0 or sigma_log <= 0:
        return -1e12

    deltas = np.abs(df["ambiguity_signed"].values)
    rt = df["rt_ms"].values

    mu_pred = C * np.power(deltas, -gamma) + t0
    if np.any(mu_pred <= 0):
        return -1e12

    # 对数正态参数：E[RT] = mu_pred，Var = mu_pred^2 * (exp(sigma^2)-1)
    mu_log = np.log(mu_pred) - 0.5 * sigma_log ** 2

    ll = (
        -0.5 * np.log(2.0 * np.pi * sigma_log ** 2)
        - np.log(rt)
        - 0.5 * ((np.log(rt) - mu_log) / sigma_log) ** 2
    )
    return float(np.sum(ll))


def fit_ufpm(df: pd.DataFrame) -> dict:
    """最大似然拟合 UFPF toy 对数正态模型，使用网格搜索初始值。"""
    def neg_ll(params):
        return -ufpm_log_likelihood(params, df)

    # 粗略网格搜索找到好的初始点
    best_ll = -np.inf
    best_x0 = [300.0, 1.2, 300.0, 0.18]
    for C0 in [100.0, 250.0, 400.0]:
        for gamma0 in [0.8, 1.0, 1.2, 1.5]:
            for t00 in [100.0, 300.0, 500.0]:
                for s0 in [0.10, 0.18, 0.25]:
                    ll = ufpm_log_likelihood([C0, gamma0, t00, s0], df)
                    if ll > best_ll:
                        best_ll = ll
                        best_x0 = [C0, gamma0, t00, s0]
    print(f"    UFPF 初始网格最优 LL={best_ll:.2f}，参数 {best_x0}")

    result = minimize(
        neg_ll,
        x0=best_x0,
        method="L-BFGS-B",
        bounds=[(1.0, 5000.0), (0.1, 3.0), (0.0, 2000.0), (0.001, 1.0)],
    )
    C, gamma, t0, sigma_log = result.x
    ll = ufpm_log_likelihood(result.x, df)
    n = len(df)
    k = 4
    aic = 2 * k - 2 * ll
    bic = k * np.log(n) - 2 * ll

    # 均值预测用于绘图
    deltas = np.sort(df["ambiguity_signed"].unique())
    pred_mean = C * np.power(np.abs(deltas), -gamma) + t0
    return {
        "C": C,
        "gamma": gamma,
        "t0": t0,
        "sigma_log": sigma_log,
        "ll": ll,
        "aic": aic,
        "bic": bic,
        "deltas": deltas,
        "pred_mean": pred_mean,
    }


# -----------------------------------------------------------------------------
# 3. DDM 完整似然：Navarro & Fuss (2009) 解析 PDF
# -----------------------------------------------------------------------------

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

    # 小时间/大时间切换阈值：取 a² * min(z,1-z)² / 2
    # 当 z 接近 0 或 1 时，小时间展开需要更小的阈值以避免镜像项主导
    z_eff = min(z, 1.0 - z)
    threshold = 0.5 * a ** 2 * z_eff ** 2
    threshold = max(threshold, 1e-4)
    small_mask = t < threshold
    large_mask = ~small_mask

    # 小时间展开：增加镜像项以改善 z>0.5 时的对称性
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

    # 大时间展开：增加项数以改善大 a 或大 t 时的精度
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

    # 防止下溢导致的 log(0)
    return np.maximum(pdf, eps)


def check_ddm_stability() -> None:
    """
    数值稳定性与对称性自检。
    检查：
      1. 下边界 PDF 对称性：f_B(t|v,a,z) == f_A(t|-v,a,1-z)
      2. 总概率归一化：∫[f_A + f_B] dt ≈ 1
      3. 临界点附近（v→0）数值行为
      4. 不同 a 下 PDF 的量级，提示下溢风险
    """
    print("\n[DDM 数值稳定性自检]")
    print("-" * 50)

    a = 0.5  # 用于对称性与归一化测试的边界间距

    # 1. 对称性：f_B(t;v,a,z) == f_A(t;-v,a,1-z)
    print("1. 对称性 f_B(v,z) == f_A(-v,1-z)：")
    t = np.linspace(0.01, 5.0, 200)
    v_val = 1.0
    for z_test in [0.30, 0.50, 0.70]:
        pdf_a = ddm_pdf(t, np.full_like(t, v_val), a, z_test)
        pdf_b_ref = ddm_pdf(t, np.full_like(t, -v_val), a, 1.0 - z_test)
        max_diff = np.max(np.abs(pdf_a - pdf_b_ref))
        print(f"   z={z_test}: max diff = {max_diff:.2e}")

    # 2. 总概率归一化（v=0, z=0.5）
    dt = 0.01
    t_long = np.arange(dt, 10.0, dt)
    pdf_a_v0 = ddm_pdf(t_long, np.zeros_like(t_long), a, 0.5)
    pdf_b_v0 = ddm_pdf(t_long, np.zeros_like(t_long), a, 0.5)
    p_a = np.sum(pdf_a_v0) * dt
    p_b = np.sum(pdf_b_v0) * dt
    print(f"2. 归一化（v=0, z=0.5, a={a}）：P_A={p_a:.4f}, P_B={p_b:.4f}, total={p_a+p_b:.4f}")

    # 3. 临界点附近 PDF 形状（使用 a=2.0 以匹配典型 RT 秒级尺度）
    a_test = 2.0
    print(f"3. 临界点附近行为（a={a_test}, z=0.5）：")
    for vv in [0.0, 0.05, 0.2, 1.0]:
        pdf_v = ddm_pdf(t_long, np.full_like(t_long, vv), a_test, 0.5)
        mean_t = np.sum(t_long * pdf_v) * dt / (np.sum(pdf_v) * dt + 1e-12)
        max_pdf = np.max(pdf_v)
        min_pdf = np.min(pdf_v[pdf_v > 1e-20])
        print(f"   v={vv:>5.2f}: mean T≈{mean_t:>6.2f}s, max pdf={max_pdf:.2e}")

    # 4. 下溢风险：不同 a 下 PDF 在 t=1-4s 的量级
    print("4. 下溢风险（v=0，典型 RT 1-4s）：")
    for a_test in [0.5, 1.0, 2.0, 3.0]:
        vals = []
        for tt in [1.0, 2.0, 3.0, 4.0]:
            pdf_t = ddm_pdf(np.array([tt]), np.array([0.0]), a_test, 0.5)[0]
            vals.append(f"{pdf_t:.2e}")
        print(f"   a={a_test}: " + ", ".join(vals))

    print("-" * 50)


def ddm_log_likelihood(params: np.ndarray, df: pd.DataFrame) -> float:
    """
    DDM 完整对数似然。
    参数顺序：[k, a, z, t0_ms]。
    漂移率 v(δ) = k * δ；t0 以 ms 传入，内部转换为秒。
    """
    k, a, z, t0_ms = params
    if k <= 0 or a <= 0.01 or z <= 0.01 or z >= 0.99 or t0_ms < 0:
        return -1e12

    t0 = t0_ms / 1000.0
    rt_s = df["rt_ms"].values / 1000.0 - t0
    rt_s = np.maximum(rt_s, 1e-6)
    v = k * df["ambiguity_signed"].values
    choice = df["choice_encoded"].values  # +1 = A, -1 = B

    pdf_a = ddm_pdf(rt_s, v, a, z)
    pdf_b = ddm_pdf(rt_s, -v, a, 1.0 - z)

    log_pdf = np.where(choice == 1, np.log(pdf_a), np.log(pdf_b))
    # 单位转换：DDM PDF 以 1/秒为单位；观测 RT 以 ms 为单位。
    # f_ms(rt_ms) = f_s(rt_ms/1000) / 1000，故需减去每试次 log(1000)。
    n_trials = len(df)
    return float(np.sum(log_pdf) - n_trials * np.log(1000.0))


def fit_ddm(df: pd.DataFrame) -> dict:
    """最大似然拟合 DDM。"""
    def neg_ll(params):
        return -ddm_log_likelihood(params, df)

    # 初始猜测：基于粗略网格搜索减小优化风险
    best_ll = -np.inf
    best_x0 = [10.0, 0.50, 0.5, 300.0]
    for k0 in [5.0, 15.0, 40.0]:
        for a0 in [0.20, 0.50, 1.00, 2.00]:
            for z0 in [0.45, 0.50, 0.55]:
                for t00 in [200.0, 400.0]:
                    ll = ddm_log_likelihood([k0, a0, z0, t00], df)
                    if ll > best_ll:
                        best_ll = ll
                        best_x0 = [k0, a0, z0, t00]

    print(f"    DDM 初始网格最优 LL={best_ll:.2f}，参数 {best_x0}")

    result = minimize(
        neg_ll,
        x0=best_x0,
        method="L-BFGS-B",
        bounds=[(0.1, 200.0), (0.02, 5.00), (0.10, 0.90), (50.0, 1200.0)],
        options={"maxiter": 300, "disp": False},
    )
    k, a, z, t0 = result.x
    ll = ddm_log_likelihood(result.x, df)
    n = len(df)
    kaic = 4
    aic = 2 * kaic - 2 * ll
    bic = kaic * np.log(n) - 2 * ll

    # 均值预测用于绘图（用解析公式或模拟；这里用模拟）
    deltas = np.sort(df["ambiguity_signed"].unique())
    pred_mean = ddm_mean_rt_curve(k * deltas, a, z, t0 / 1000.0, n_trials=3000, seed=42)
    return {
        "k": k,
        "a": a,
        "z": z,
        "t0": t0,
        "ll": ll,
        "aic": aic,
        "bic": bic,
        "deltas": deltas,
        "pred_mean": pred_mean,
    }


def ddm_mean_rt_curve(
    drifts: np.ndarray,
    a: float,
    z: float,
    t0: float,
    dt: float = 0.005,
    n_trials: int = 2000,
    max_time: float = 8.0,
    seed: int = 42,
) -> np.ndarray:
    """向量化模拟 DDM 得到每个漂移率下的平均 RT（ms），仅用于绘图。"""
    rng = np.random.default_rng(seed)
    n_d = len(drifts)
    max_steps = int(max_time / dt)

    x = np.full((n_d, n_trials), a * z)
    t = np.zeros((n_d, n_trials))
    active = np.ones((n_d, n_trials), dtype=bool)

    for _ in range(max_steps):
        if not active.any():
            break
        noise = rng.normal(size=(n_d, n_trials))
        dx = drifts[:, None] * dt + np.sqrt(dt) * noise
        x = np.where(active, x + dx, x)
        t = np.where(active, t + dt, t)
        finished = (x >= a) | (x <= 0.0)
        timeout = t >= max_time - dt
        active = active & ~finished & ~timeout

    rt_ms = (t + t0) * 1000.0
    rt_ms = np.where(t >= max_time - dt, max_time * 1000.0, rt_ms)
    return np.mean(rt_ms, axis=1)


# -----------------------------------------------------------------------------
# 4. 主流程
# -----------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("UFPF toy 模型 vs DDM：基于完整似然的拟合优度比较")
    print("=" * 60)

    # 1. 生成数据
    print("\n[1] 生成含临界慢化特征的合成数据（γ_true=1.2）...")
    df = generate_critical_slowing_data(seed=2026)
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    df.to_csv(out_dir / "critical_slowing_model_comparison_data.csv", index=False)
    print(f"  总试次数：{len(df)}")

    # 按 δ 汇总（仅用于绘图和展示）
    summary = (
        df.groupby("ambiguity_signed")
        .agg(
            n=("trial_id", "count"),
            p_a=("choice_encoded", lambda x: np.nanmean(x == 1.0)),
            rt_mean=("rt_ms", "mean"),
            rt_median=("rt_ms", "median"),
            rt_std=("rt_ms", "std"),
        )
        .reset_index()
        .sort_values("ambiguity_signed")
    )
    deltas = summary["ambiguity_signed"].values
    rt_mean = summary["rt_mean"].values
    print("\n[2] 按 δ 汇总（部分）：")
    print(summary.head(6).to_string(index=False))

    # 2. 拟合 UFPF toy 模型
    print("\n[3] 拟合 UFPF toy 模型（LogNormal 完整似然）...")
    ufpm = fit_ufpm(df)
    print(f"  C         = {ufpm['C']:.2f} ms")
    print(f"  γ         = {ufpm['gamma']:.4f}（真实值 1.2）")
    print(f"  t0        = {ufpm['t0']:.2f} ms")
    print(f"  σ_log     = {ufpm['sigma_log']:.4f}")
    print(f"  log L     = {ufpm['ll']:.2f}")
    print(f"  AIC       = {ufpm['aic']:.2f}")
    print(f"  BIC       = {ufpm['bic']:.2f}")

    # 3. 拟合 DDM
    print("\n[4] 拟合 DDM 模型（Navarro & Fuss 2009 解析 PDF 完整似然）...")
    print("  （DDM 完整似然计算量较大，请稍候...）")
    ddm = fit_ddm(df)
    print(f"  k         = {ddm['k']:.4f} (drift rate / δ)")
    print(f"  a         = {ddm['a']:.4f} (boundary separation)")
    print(f"  z         = {ddm['z']:.4f} (starting point ratio)")
    print(f"  t0        = {ddm['t0']:.2f} ms")
    print(f"  log L     = {ddm['ll']:.2f}")
    print(f"  AIC       = {ddm['aic']:.2f}")
    print(f"  BIC       = {ddm['bic']:.2f}")

    # 4. 模型比较
    print("\n[5] 模型比较（基于完整似然，参数数均为 4）：")
    aic_min = min(ufpm["aic"], ddm["aic"])
    bic_min = min(ufpm["bic"], ddm["bic"])
    print(f"  ΔAIC_UFPF = {ufpm['aic'] - aic_min:.2f}")
    print(f"  ΔAIC_DDM  = {ddm['aic'] - aic_min:.2f}")
    print(f"  ΔBIC_UFPF = {ufpm['bic'] - bic_min:.2f}")
    print(f"  ΔBIC_DDM  = {ddm['bic'] - bic_min:.2f}")
    print(f"  2ΔlogL    = {2 * abs(ufpm['ll'] - ddm['ll']):.2f}")

    if ufpm["aic"] < ddm["aic"]:
        print("\n  结论（AIC）：UFPF toy 模型优于 DDM（符合预期，因为数据由幂律生成）。")
    else:
        print("\n  结论（AIC）：DDM 优于 UFPF toy 模型。")

    # 5. DDM 数值稳定性自检
    print("\n[6] DDM 数值稳定性自检...")
    check_ddm_stability()

    # 7. 绘图并导出 PNG 与 SVG
    print("\n[7] 绘图并导出 PNG 与 SVG...")
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))

    ax = axes[0]
    ax.errorbar(deltas, rt_mean, yerr=summary["rt_std"].values, fmt='ko',
                capsize=3, label="观测均值 ± SD")
    delta_fine = np.linspace(deltas.min(), deltas.max(), 200)
    delta_fine_nz = delta_fine[delta_fine != 0]
    ax.plot(delta_fine_nz, ufpm["C"] * np.abs(delta_fine_nz) ** (-ufpm["gamma"]) + ufpm["t0"],
            'r-', lw=2, label=f"UFPF: γ={ufpm['gamma']:.2f}")
    ax.plot(ddm["deltas"], ddm["pred_mean"], 'b--', lw=2,
            label=f"DDM: k={ddm['k']:.1f}, a={ddm['a']:.2f}")
    ax.set_xlabel("控制参数 δ")
    ax.set_ylabel("平均 RT (ms)")
    ax.set_title("(a) RT(δ) 临界慢化")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.loglog(np.abs(deltas), rt_mean, 'ko', label="观测")
    ax.loglog(np.abs(delta_fine_nz),
              ufpm["C"] * np.abs(delta_fine_nz) ** (-ufpm["gamma"]) + ufpm["t0"],
              'r-', lw=2, label=f"UFPF γ={ufpm['gamma']:.2f}")
    ax.loglog(np.abs(ddm["deltas"]), ddm["pred_mean"], 'b--', lw=2, label="DDM")
    ax.set_xlabel("|δ|（对数）")
    ax.set_ylabel("RT（对数）")
    ax.set_title("(b) 对数-对数坐标")
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    ax = axes[2]
    x_pos = np.arange(2)
    aic_vals = [ufpm["aic"] - aic_min, ddm["aic"] - aic_min]
    bic_vals = [ufpm["bic"] - bic_min, ddm["bic"] - bic_min]
    width = 0.35
    ax.bar(x_pos - width/2, aic_vals, width, label="ΔAIC", color='steelblue')
    ax2 = ax.twinx()
    ax2.bar(x_pos + width/2, bic_vals, width, label="ΔBIC", color='coral')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(["UFPF toy", "DDM"])
    ax.set_ylabel("ΔAIC", color='steelblue')
    ax2.set_ylabel("ΔBIC", color='coral')
    ax.set_title("(c) 信息准则对比")
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    fig_path_png = Path("figs") / "paperX_critical_slowing_model_comparison.png"
    fig_path_svg = Path("figs") / "paperX_critical_slowing_model_comparison.svg"
    fig_path_png.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path_png, dpi=300)
    plt.savefig(fig_path_svg, format="svg")
    print(f"  PNG: {fig_path_png}")
    print(f"  SVG: {fig_path_svg}")

    # 8. 保存结果
    print("\n[8] 保存结果摘要...")
    results = {
        "true_gamma": 1.2,
        "true_C": 250.0,
        "true_t0": 400.0,
        "ufpm_C": ufpm["C"],
        "ufpm_gamma": ufpm["gamma"],
        "ufpm_t0": ufpm["t0"],
        "ufpm_sigma_log": ufpm["sigma_log"],
        "ufpm_ll": ufpm["ll"],
        "ufpm_aic": ufpm["aic"],
        "ufpm_bic": ufpm["bic"],
        "ddm_k": ddm["k"],
        "ddm_a": ddm["a"],
        "ddm_z": ddm["z"],
        "ddm_t0": ddm["t0"],
        "ddm_ll": ddm["ll"],
        "ddm_aic": ddm["aic"],
        "ddm_bic": ddm["bic"],
        "delta_aic_ufpm": ufpm["aic"] - aic_min,
        "delta_aic_ddm": ddm["aic"] - aic_min,
    }
    pd.DataFrame([results]).to_csv(
        out_dir / "critical_slowing_model_comparison_results.csv", index=False
    )
    print(f"\n  结果摘要已保存至 {out_dir / 'critical_slowing_model_comparison_results.csv'}")
    print("\n完成。")


if __name__ == "__main__":
    main()
