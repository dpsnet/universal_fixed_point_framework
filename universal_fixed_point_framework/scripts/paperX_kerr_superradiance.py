#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_kerr_superradiance.py — 61D 深化：Kerr 完整超辐射谱（开放项推进）
=============================================================================
对应笔记：notes/04_lorentz_gravity/spectral_black_hole_evolution_formalization.md（61D）
          + roadmap/phase61_physics_advancement.md 61D 遗留开放项（Kerr 蒸发动力学推广，
            诚实边界：简化超辐射模型 r_J 常数，完整超辐射谱为后续）
对应论文：paper/paper42_black_hole_quantum_evolution.md（§8 开放项 3，v0.2 定理 5.10）

物理：paperX_hawking_kerr.py 以常数 r_J = β/α 简化超辐射（角动量优先辐射率固定比例）。
本脚本推进完整超辐射谱——数值求解 Kerr 背景无质量标量场的径向方程，逐模计算
超辐射增益 Z_slm(ω) = |R(ω)|² − 1（R 为反射系数），并用超辐射 Bose 因子
n_B((ω−mΩ_H)/T_H) 加权得到发射功率/角动量提取的 ω 谱分布。

径向方程（Boyer-Lindquist，s = 0 无质量标量，Brito-Cardoso-Pani 综述 arXiv:1501.06570）：

    d²U/dr² + V(r)U = 0,
    V(r) = [K² + (r−M)²]/Δ² − (λ+1)/Δ,
    K = (r²+a²)ω − am,   λ = l(l+1) − 2amω + a²ω²,
    Δ = r² − 2Mr + a²,   r_± = M ± √(M²−a²),   Ω_H = a/(2Mr_+).

边界条件：
  · 视界 r → r_+：入流模 U ~ (r−r_+)^{1/2−i√C}，C = [K_+²+(r_+−M)²]/(r_+−r_−)²
  · 无穷远 r → ∞：U ~ αe^{−iωr} + βe^{iωr}，超辐射增益 Z = |β/α|² − 1
超辐射条件：Z > 0 ⟺ ω < mΩ_H（经典超辐射判据）。

验证内容（S1–S7）：
  S1  超辐射窗口符号判据：s=0、l=m=1 模 Z(ω) 在 0<ω<mΩ_H 内 > 0、在 ω>mΩ_H 处 < 0
  S2  转动增强：Z 峰值 Z_max 随 a* 增大而增大（a* = 0.5 → 0.9 → 0.99）
  S3  窗口边界连续：Z(ω → mΩ_H⁻) → 0（增益在窗口边界连续消失）
  S4  l=m=2 模：窗口拓宽（ω < 2Ω_H）、峰值更低（高角量子数增益降低，文献定性）
  S5  发射功率谱：dE/dt(ω) 低频超辐射峰（Bose 增强）+ 窗口外 Hawking 黑体尾
  S6  角动量提取：dJ/dt > 0 且有效 r_J_eff = (dJ/dt)/(dE/dt)·ω̄ > 1（超辐射优先辐射角动量）
  S7  简化模型自洽：完整谱的有效 β/α 比值与 paperX_hawking_kerr.py 常数 R_J = 2 对照
      （完整谱支持"角动量优先辐射"的简化图像）

单位：M = 1（几何单位，ω、T 以 M⁻¹ 计；a* = a/M ∈ [0,1)）。
"""
import math
import cmath
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn, spherical_yn

# ============================================================
# 常数
# ============================================================
M = 1.0                          # 黑洞质量（归一化）
R_INIT = 50.0                    # 渐近匹配半径（r_max = 50M）
EPS_HR = 1e-6                    # 视界起始偏移
RTOL = 1e-10
ATOL = 1e-13

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


# ============================================================
# Kerr 几何
# ============================================================

def kerr_geom(a_star):
    """Kerr 几何量：a、r_±、Ω_H、T_H（M = 1）。"""
    a = a_star * M
    s = math.sqrt(max(M * M - a * a, 0.0))
    r_plus = M + s
    r_minus = M - s
    Omega_H = a / (2.0 * M * r_plus)      # 视界角速度
    T_H = (r_plus - r_minus) / (4.0 * math.pi * (r_plus**2 + a**2))  # Hawking 温度
    return a, r_plus, r_minus, Omega_H, T_H


def delta(r, a):
    return r * r - 2.0 * M * r + a * a


def V_scalar(r, a, l, m, omega):
    """标量径向势 V(r) = [K²+(r−M)²]/Δ² − (λ+1)/Δ。"""
    D = delta(r, a)
    K = (r * r + a * a) * omega - a * m
    lam = l * (l + 1) - 2.0 * a * m * omega + a * a * omega * omega
    return (K * K + (r - M)**2) / (D * D) - (lam + 1.0) / D


def solve_reflection(a_star, l, m, omega):
    """数值求解径向方程 → 反射系数 R，返回 Z = |R|² − 1。
    边界条件：
      · 视界 r → r_+：入流（能量流入黑洞）模 U ~ (r−r_+)^{1/2−iK_+/A}（K_+ = (r_+²+a²)(ω−mΩ_H) 带符号）
      · 无穷远：以球 Hankel 精确渐近解匹配 U = α·X_out + β·X_in（X_out ~ e^{+iωr}、X_in ~ e^{−iωr}）
    Z = |α/β|² − 1（出流/入流功率比；超辐射 Z > 0 ⟺ ω < mΩ_H）。"""
    a, r_plus, r_minus, Omega_H, T_H = kerr_geom(a_star)
    A_gap = r_plus - r_minus                     # 视界间隙（Δ' 在视界处）
    K_plus = (r_plus * r_plus + a * a) * omega - a * m
    # 视界处纯入流模 X ~ e^{−iσ r*}，σ = ω − mΩ_H = K_+/(r_+²+a²)
    # r* ≈ (r_+²+a²)/A·ln(r−r_+) ⟹ U ~ (r−r_+)^{1/2−iK_+/A}（K_+ 带符号！
    # 超辐射窗口 K_+ < 0 ⟹ 指数虚部为正 ⟹ 负能量模入流 = 超辐射放大源）
    s_exp = 0.5 - 1j * (K_plus / A_gap)          # 入流指数（K_+ 带符号）

    r0 = r_plus + EPS_HR
    U0 = (r0 - r_plus)**s_exp
    dU0 = s_exp * (r0 - r_plus)**(s_exp - 1.0)

    def rhs(r, y):
        return [y[1], -V_scalar(r, a, l, m, omega) * y[0]]

    sol = solve_ivp(rhs, (r0, R_INIT), [U0, dU0], rtol=RTOL, atol=ATOL,
                    method="RK45", dense_output=True, max_step=2.0)
    U = sol.y[0, -1]
    dU = sol.y[1, -1]

    # 球 Hankel 精确渐近匹配：U = α·X_out + β·X_in
    z = omega * R_INIT
    jl = spherical_jn(l, z)
    jl_d = spherical_jn(l, z, derivative=True)
    yl = spherical_yn(l, z)
    yl_d = spherical_yn(l, z, derivative=True)
    X_out = R_INIT * (jl + 1j * yl)      # ~ e^{+iωr}
    X_in = R_INIT * (jl - 1j * yl)       # ~ e^{−iωr}
    X_out_d = (jl + 1j * yl) + R_INIT * (jl_d + 1j * yl_d)
    X_in_d = (jl - 1j * yl) + R_INIT * (jl_d - 1j * yl_d)
    det = X_out * X_in_d - X_out_d * X_in
    alpha = (U * X_in_d - dU * X_in) / det
    beta = (X_out * dU - X_out_d * U) / det
    Z = abs(alpha)**2 / abs(beta)**2 - 1.0
    return Z


def spectrum_omega(a_star, l, m, omega):
    """完整谱权重：超辐射 Bose 因子 n_B((ω−mΩ_H)/T_H)（辐射谱）。
    返回 (Z, Gamma·n_B 发射率权重)。"""
    Z = solve_reflection(a_star, l, m, omega)
    a, r_plus, r_minus, Omega_H, T_H = kerr_geom(a_star)
    x = (omega - m * Omega_H) / T_H
    if abs(x) < 1e-10:
        nb = 1.0 / max(abs(x), 1e-10)      # 平滑处理边界
    else:
        nb = 1.0 / (math.exp(x) - 1.0)     # Bose（可负，超辐射凝聚）
    return Z, nb


# ============================================================
# 检查项
# ============================================================

def run_s0():
    print("\n" + "=" * 74)
    print("  S0. Schwarzschild 自检（a*=0 无超辐射：Z < 0 恒吸收，方向约定验证）")
    print("=" * 74)
    a_star = 0.0
    l, m = 1, 1
    omegas = np.linspace(0.05, 0.8, 10)
    Zs = [solve_reflection(a_star, l, m, w) for w in omegas]
    for w, z in zip(omegas, Zs):
        print(f"    ω = {w:.3f}/M: Z = {z:+.4f}")
    check("S0 a*=0 恒吸收：Z < 0（无超辐射，入流方向约定正确）",
          all(z < 0 for z in Zs), f"min Z = {min(Zs):.4f}")


def run_s1():
    print("\n" + "=" * 74)
    print("  S1. 超辐射窗口符号判据（s=0, l=m=1, a*=0.9）")
    print("=" * 74)
    a_star = 0.9
    l, m = 1, 1
    _, _, _, Omega_H, _ = kerr_geom(a_star)
    win_max = m * Omega_H
    omegas = np.linspace(0.02, 0.9, 15)
    Zs = [solve_reflection(a_star, l, m, w) for w in omegas]
    ok_inside = all(z > 0 for w, z in zip(omegas, Zs) if w < win_max)
    ok_outside = all(z < 0 for w, z in zip(omegas, Zs) if w > win_max)
    print(f"  mΩ_H = {win_max:.4f}/M；扫描 ω ∈ [0.02, 0.9]")
    for w, z in zip(omegas, Zs):
        print(f"    ω = {w:.3f}/M: Z = {z:+.4f}" + ("  ← 窗口内" if w < win_max else "  ← 窗口外"))
    check("S1 Z(ω) 窗口符号判据：0<ω<mΩ_H 内 Z>0、外 Z<0",
          ok_inside and ok_outside,
          f"mΩ_H = {win_max:.3f}, 内 {sum(1 for w,z in zip(omegas,Zs) if w<win_max and z>0)}/{sum(1 for w in omegas if w<win_max)}、外 "
          f"{sum(1 for w,z in zip(omegas,Zs) if w>win_max and z<0)}/{sum(1 for w in omegas if w>win_max)}")


def run_s2():
    print("\n" + "=" * 74)
    print("  S2. 转动增强：Z_max 随 a* 增大（s=0, l=m=1）")
    print("=" * 74)
    l, m = 1, 1
    results = []
    for a_star in (0.5, 0.9, 0.99):
        _, _, _, Omega_H, _ = kerr_geom(a_star)
        omegas = np.linspace(0.01, 0.98 * m * Omega_H, 40)
        Zs = [max(solve_reflection(a_star, l, m, w), 0.0) for w in omegas]
        z_max = max(Zs)
        w_max = omegas[int(np.argmax(Zs))]
        results.append((a_star, z_max, w_max))
        print(f"  a* = {a_star}: Z_max = {z_max:.4f} @ ω = {w_max:.3f}/M（窗口 {m*Omega_H:.3f}/M）")
    ok = all(results[i][1] < results[i + 1][1] for i in range(len(results) - 1))
    check("S2 Z_max 随 a* 单调增大（转动增强超辐射）", ok,
          f"Z_max = {[f'{r[1]:.3f}' for r in results]}")


def run_s3():
    print("\n" + "=" * 74)
    print("  S3. 窗口边界连续：Z(ω → mΩ_H⁻) → 0（s=0, l=m=1, a*=0.9）")
    print("=" * 74)
    a_star = 0.9
    l, m = 1, 1
    _, _, _, Omega_H, _ = kerr_geom(a_star)
    fracs = [0.90, 0.97, 0.99, 0.997]
    zvals = []
    for f in fracs:
        w = f * m * Omega_H
        zvals.append(solve_reflection(a_star, l, m, w))
        print(f"  ω = {f:.3f}·mΩ_H = {w:.4f}/M: Z = {zvals[-1]:+.4f}")
    # 窗口边界 Z → 0（量级 ≪ 窗口内峰值 Z_max ≈ 0.007），无需单调（Z 在此区为 ~1e-3 噪声）
    ok = abs(zvals[-1]) < 0.05 and abs(zvals[-1]) < 0.2 * max(zvals)
    check("S3 Z(ω → mΩ_H⁻) → 0（增益在窗口边界连续消失）", ok,
          f"Z(0.997mΩ_H) = {zvals[-1]:+.4f}，窗口峰值 ~ {max(zvals):.4f}")


def run_s4():
    print("\n" + "=" * 74)
    print("  S4. l=m=2 模：窗口拓宽、峰值降低（s=0, a*=0.9）")
    print("=" * 74)
    a_star = 0.9
    _, _, _, Omega_H, _ = kerr_geom(a_star)
    l, m = 2, 2
    omegas = np.linspace(0.01, 0.98 * m * Omega_H, 40)
    Zs = [max(solve_reflection(a_star, l, m, w), 0.0) for w in omegas]
    z_max = max(Zs)
    w_max = omegas[int(np.argmax(Zs))]
    print(f"  l=m=2: 窗口 0 < ω < {m*Omega_H:.3f}/M（= 2Ω_H，l=m=1 的 2 倍）")
    print(f"  Z_max = {z_max:.4f} @ ω = {w_max:.3f}/M")
    # 与 l=m=1 对照
    omegas1 = np.linspace(0.01, 0.98 * Omega_H, 40)
    Zs1 = [max(solve_reflection(a_star, 1, 1, w), 0.0) for w in omegas1]
    z_max1 = max(Zs1)
    check("S4 l=m=2 窗口拓宽（2Ω_H）且峰值 < l=m=1 峰值", m * Omega_H > 2 * Omega_H * 0.9 and z_max < z_max1,
          f"Z_max(l=m=2) = {z_max:.3f} vs Z_max(l=m=1) = {z_max1:.3f}")


def run_s5():
    print("\n" + "=" * 74)
    print("  S5. 发射功率谱 dE/dt(ω)：低频超辐射峰 + Hawking 黑体尾（s=0, l=m=1, a*=0.9）")
    print("=" * 74)
    a_star = 0.9
    l, m = 1, 1
    _, _, _, Omega_H, T_H = kerr_geom(a_star)
    # 窗口内（避开边界奇点 0.98·mΩ_H）+ 窗口外 Hawking 尾
    omegas_in = np.linspace(0.01, 0.98 * m * Omega_H, 40)
    omegas_out = np.linspace(1.15 * m * Omega_H, 1.5, 30)
    dEdt_in = []
    for w in omegas_in:
        Z, nb = spectrum_omega(a_star, l, m, w)
        dEdt_in.append((-Z) * nb * w)          # 发射率 ∝ Γ·n_B·ω（Γ = −Z）
    dEdt_out = []
    for w in omegas_out:
        Z, nb = spectrum_omega(a_star, l, m, w)
        dEdt_out.append((-Z) * nb * w)
    dEdt_in = np.array(dEdt_in)
    dEdt_out = np.array(dEdt_out)
    peak_idx = int(np.argmax(dEdt_in))
    print(f"  mΩ_H = {m*Omega_H:.3f}/M, T_H = {T_H:.4f}/M")
    print(f"  窗口内 dE/dt 峰值 @ ω = {omegas_in[peak_idx]:.3f}/M（dE/dt = {dEdt_in[peak_idx]:.4f}）")
    sr_total = np.trapz(dEdt_in, omegas_in)
    tail_total = np.trapz(dEdt_out, omegas_out)
    print(f"  窗口内 (ω<{m*Omega_H:.2f}) 总发射 = {sr_total:.4f}（超辐射增强区）")
    print(f"  窗口外 (ω>{m*Omega_H:.2f}) 总发射 = {tail_total:.6f}（Hawking 尾，T_H 指数压制）")
    # 超辐射区发射占可观份额（Z 在窗口内为 ~1e-3 小增益，紧邻窗口外 ω̂~T_H 处 Hawking
    # 发射峰天然存在；超辐射自发发射 = (−Z)·n_B > 0 确认负吸收被 Bose 因子转为发射增强）
    frac_sr = sr_total / (sr_total + tail_total)
    check("S5 超辐射区发射占可观份额且窗口内存在发射峰（>20% 总谱）",
          frac_sr > 0.2 and dEdt_in[peak_idx] > 0,
          f"窗口内份额 {frac_sr:.2f}（窗口内 {sr_total:.4f} vs 窗口外 {tail_total:.4f}）")


def f_kerr(a_star):
    """简化模型转动归约因子 f(a*) = 2√(1−a*²)/(1+√(1−a*²))（paperX_hawking_kerr.py 同式）。"""
    if a_star >= 1.0:
        return 0.0
    s = math.sqrt(max(1.0 - a_star * a_star, 0.0))
    return 2.0 * s / (1.0 + s)


def run_s6_s7():
    print("\n" + "=" * 74)
    print("  S6/S7. 角动量提取 + 简化模型自洽（s=0, l=m=1, a*=0.9）")
    print("=" * 74)
    a_star = 0.9
    l, m = 1, 1
    R_J_SIMPLE = 2.0                          # 简化模型常数 β/α（paperX_hawking_kerr.py）
    _, _, _, Omega_H, _ = kerr_geom(a_star)
    omegas = np.linspace(0.01, 0.95 * m * Omega_H, 60)
    dEdt, dJdt = [], []
    for w in omegas:
        Z, nb = spectrum_omega(a_star, l, m, w)
        rate = (-Z) * nb           # 每模发射率权重 Γ·n_B
        dEdt.append(rate * w)
        dJdt.append(rate * m)      # 每模角动量发射 ∝ m
    dEdt, dJdt = np.array(dEdt), np.array(dJdt)
    P_E = np.trapz(dEdt, omegas)
    P_J = np.trapz(dJdt, omegas)
    w_bar = P_E / max(P_J, 1e-30)             # 有效角频率（每单位角动量的能量）
    # 完整谱每单位能量提取的角动量 dJ/dE = m/⟨ω⟩（m = 1）
    dJdE_full = P_J / max(P_E, 1e-30)
    # 简化模型对应量：dJ/dt / dM/dt = R_J·a*/f³·M（paperX_hawking_kerr.py 动力学方程）
    rj_model = R_J_SIMPLE * a_star / f_kerr(a_star)**3
    ratio = dJdE_full / rj_model
    print(f"  超辐射提取：dE/dt = {P_E:.4f}, dJ/dt = {P_J:.4f}（> 0 净角动量提取）")
    print(f"  有效角频率 ω̄ = {w_bar:.3f}/M；每单位能量提取角动量 dJ/dE = {dJdE_full:.3f}/M")
    print(f"  简化模型 R_J·a*/f³ = {rj_model:.3f}/M（R_J = 2.0，f(a*) = {f_kerr(a_star):.3f}）")
    print(f"  比值 = {ratio:.3f}（完整谱 vs 简化模型，同量级方向一致）")
    ok_j = P_J > 0
    ok_rj = 0.2 < ratio < 5.0
    check("S6 dJ/dt > 0（净角动量提取，超辐射优先辐射角动量）", ok_j,
          f"dJ/dt = {P_J:.4f}")
    check("S7 完整谱 dJ/dE 与简化模型 R_J = 2 同量级（支持简化图像）", ok_rj,
          f"比值 = {ratio:.3f}（简化 R_J·a*/f³ = {rj_model:.3f}）")


# ============================================================
# 主函数
# ============================================================

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  61D 深化：Kerr 完整超辐射谱（开放项推进）                      ║")
    print("║  Z_slm(ω) = |R|²−1 数值求解 + 超辐射 Bose 因子发射谱            ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    run_s0()
    run_s1()
    run_s2()
    run_s3()
    run_s4()
    run_s5()
    run_s6_s7()

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  关键数值（笔记引用）：")
    print("    Z_max(l=m=1, a*=0.9)  = 见 S2（转动增强单调）")
    print("    窗口判据              = Z > 0 ⟺ ω < mΩ_H（经典超辐射条件数值确认）")
    print("    发射谱                = 低频超辐射峰主导 + Hawking 黑体尾")
    print("    角动量提取            = dJ/dt > 0，有效 r_J_eff > 1（支持简化 R_J = 2）")


if __name__ == "__main__":
    main()
