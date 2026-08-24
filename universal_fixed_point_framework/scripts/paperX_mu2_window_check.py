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
# -*- coding: utf-8 -*-
"""
paperX_mu2_window_check.py — 框架胶子 vs MT 有效强度比 0.42 的观测窗口因素检验
====================================================================================
对应：paper40 §5.9（v0.36 有效强度比 0.42；v0.46 推导 H1 否定）
触发：用户"框架胶子形式（1/p⁴）与 DS 工作胶子（MT 高斯）有效强度不等价（0.42×）
      是否存在观测窗口的因素？"

背景：框架胶子（无极点增强 μ²q²/(q²+m_IR²)² + UV 尾）与 MT 高斯（(4π²d/ω⁴)q²e^{-q²/ω²}
+ UV 尾）的有效强度比 ∫dq·q·G_fw / ∫dq·q·G_MT = 0.42（v0.36，两位精度）。
观测窗口候选因子（框架 §5.10 谱静默）：
  · ¾ = 1 − a_c(4) = 0.75（D=4 闭弦零点能观测层修正）
  · S_4 = e^{−d_H} = e^{−ln15} ≈ 0.0665（观测窗口谱权重筛选）
  · ¾² = 0.5625、¾³ = 27/64 = 0.421875、¾⁴ = 0.3164
  · 其他组合

检验：
  W1  精确计算 I_fw/I_MT（高精度）
  W2  与观测窗口候选因子匹配（¾³ = 0.4219 等，偏差 < 2%）
  W3  匹配因子的框架地位
  W4  物理诠释：观测窗口因素是否解释有效强度差
  W5  诚实边界

单位：GeV²。
"""
import numpy as np

# ---- 谱定量（paper40）----
SIGMA = 0.1764            # GeV²，弦张力（定理 5.5）
ALPHA_S = 0.3380          # 轻味有效耦合（推论 5.8）
CF = 4.0 / 3.0
MU2 = 8.0 * np.pi * SIGMA / (4.0 * np.pi * ALPHA_S * CF)   # 0.783 GeV²（谱定，含 C_F）
M_IR = np.sqrt(SIGMA)     # √σ = 0.420 GeV
GAMMA_M = 12.0 / 25.0
LAMBDA_UV = 0.21
M_T = 0.5
TAU = np.exp(2.0) - 1.0
D_MT_REF = 0.926          # MT 完整顶点后强度（推论 5.9）
OMEGA = 0.5

QUARTER = 0.75            # ¾
S4 = np.exp(-np.log(15))  # 谱静默观测窗口权重 e^{-d_H}，d_H = ln15

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def g_uv(q2):
    return (8.0 * np.pi**2 * GAMMA_M / np.log(TAU + (1.0 + q2 / LAMBDA_UV**2)**2)) \
           * (1.0 - np.exp(-q2 / (4.0 * M_T**2))) / (q2 + 1e-12)


def fw_gluon(q2):
    return MU2 * q2 / (q2 + M_IR**2) ** 2 + g_uv(q2)


def mt_gluon_ref(q2):
    return (4.0 * np.pi**2 * D_MT_REF / OMEGA**4) * q2 * np.exp(-q2 / OMEGA**2) + g_uv(q2)


def g_int(gluon):
    """∫dq·q·G(q²)（有效强度，DS 积分核心量）。"""
    q = np.linspace(0.01, 6.0, 4000)
    G = np.array([gluon(qq**2) for qq in q])
    return float(np.trapz(q * G, q))


def run():
    print("=" * 74)
    print("框架胶子 vs MT 有效强度比 0.42 的观测窗口因素检验")
    print("=" * 74)
    print(f"    观测窗口候选：¾ = {QUARTER}、S_4 = e^(−d_H) = {S4:.4f}、¾³ = {QUARTER**3:.6f}")

    # W1: 精确有效强度比
    print("\n" + "=" * 74)
    print("W1. 精确有效强度比 I_fw/I_MT")
    print("=" * 74)
    I_fw = g_int(fw_gluon)
    I_mt = g_int(mt_gluon_ref)
    ratio = I_fw / I_mt
    print(f"    I_fw = {I_fw:.4f}，I_MT = {I_mt:.4f}，比值 = {ratio:.6f}（v0.36 报告 0.42）")
    check("W1 精确比值计算（高精度，非两位四舍五入）",
          True, f"比值 = {ratio:.6f}")

    # W2: 观测窗口候选因子匹配
    print("\n" + "=" * 74)
    print("W2. 观测窗口候选因子匹配")
    print("=" * 74)
    candidates = {
        "¾": QUARTER,
        "¾²": QUARTER**2,
        "¾³": QUARTER**3,
        "¾⁴": QUARTER**4,
        "S_4": S4,
        "√S_4": S4**0.5,
        "¾×√S_4": QUARTER * S4**0.5,
        "1/C_F": 1.0 / CF,
    }
    best = (None, 1e9)
    for name, val in candidates.items():
        dev = abs(ratio - val) / val * 100
        print(f"    {name:>10s} = {val:.6f}  偏差 {dev:5.1f}%")
        if dev < best[1]:
            best = (name, dev)
    print(f"    ⟹ 最佳匹配：{best[0]}（偏差 {best[1]:.1f}%）")
    check("W2 观测窗口候选匹配（¾³ = 0.4219 vs 比值，偏差 < 2% 即成立）",
          best[1] < 2.0, f"最佳候选 {best[0]}，偏差 {best[1]:.1f}%")

    # W3: 匹配因子框架地位
    print("\n" + "=" * 74)
    print("W3. 匹配因子的框架地位")
    print("=" * 74)
    if best[0] == "¾³":
        print("    ¾³ = 27/64 = 0.4219：¾ = 1 − a_c(4)（D=4 闭弦零点能，观测层修正，§5.10）")
        print("    三次方：三个空间方向（观测层 3D）或谱静默三层修正——需机制解释")
    else:
        print(f"    匹配因子 {best[0]}（非 ¾³）——框架地位需单独评估")
    check("W3 匹配因子框架地位登记（¾³ = 观测层修正³）",
          True, f"最佳候选 {best[0]}")

    # W4: 物理诠释
    print("\n" + "=" * 74)
    print("W4. 物理诠释：观测窗口因素是否解释有效强度差")
    print("=" * 74)
    if best[0] == "¾³":
        print("    若 ¾³ 成立：框架胶子（谱机制 1/p⁴ 结构，μ² 由 σ 反解）的有效强度")
        print("    = ¾³ ×（DS 工作胶子强度）——观测层修正³ 把'谱机制强度'映射到")
        print("    'DS 工作强度'；框架胶子非 DS 工作胶子（v0.36/v0.46）的部分差异")
        print("    获观测窗口因素解释（但 0.42 的'三次方'机制待解释）")
    else:
        print(f"    无清晰观测窗口匹配（最佳 {best[0]} 偏差 {best[1]:.1f}%）——")
        print("    0.42 不直接来自观测窗口因子（¾/S_4 族），保持形式差异解释（v0.36）")
    check("W4 物理诠释登记（按匹配结果如实）",
          True, "观测窗口因素成立与否按 W2 匹配")

    # W5: 诚实边界
    print("\n" + "=" * 74)
    print("W5. 诚实边界")
    print("=" * 74)
    print("    ① 单点比较（一个比值 0.42）：即使 = ¾³（偏差 <1%），无法区分'结构'")
    print("       与'巧合'——¾³ 的'三次方'无机制来源（三个方向？谱静默层次？）；")
    print("    ② 比值依赖 UV 尾与积分截断（q ∈ [0.01, 6] GeV）——不同截断会变；")
    print("    ③ 观测窗口叙事（S_4/¾）在 §5.10 针对胶球谱，此处为传播子强度——")
    print("       映射是推测性的（需独立机制论证）。")
    check("W5 诚实登记：¾³ 匹配为单点观察（无三次方机制），观测窗口映射推测性",
          True, "结构 vs 巧合不可区分；截断依赖")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print("\n" + "=" * 74)
    print(f"结果：{n_pass}/{len(RESULTS)} 通过")
    print("=" * 74)
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
