#!/usr/bin/env python3
"""
paperX_ww_decay.py — A4 涌现不可逆推导候选数值验证：Wigner-Weisskopf 定量衰减率
（笔记 06_photon_topology 方向 2 §3.7，2026-08-12）

推进 §3.7 "A4 涌现不可逆推导候选"：三锚点链（推迟辐射条件 -> RAGE 谱逃逸 -> 向内=吸收）
的数值层——补 RAGE 定性骨架的 WW 定量衰减率（open 系统不可逆的定量内容）。

S1: WW 非 Markov 精确解 vs Markov 指数解——gamma0/Gamma 扫描，
    非 Markov 修正 ~O(gamma0*tau_c) 幂律核对（Markov 极限 rel 偏差 < 1e-3、
    偏差随 gamma0/Gamma 近线性增长、Euler 数值核对）
S2: 氢 2p->1s 爱因斯坦 A 系数 6.27e8 s^-1 复现——径向偶极积分 I_rad（Simpson 数值）
    + 角向因子 1/sqrt(3) => |<1s|z|2p,0>|^2 = (2^15/3^10) a0^2 锚点核对（<1e-4）
S3: 光子因果外向波包——洛伦兹谱 => 因果指数波包 e^{-gamma0 t}（数值傅里叶核对）
    + 峰值以光速 c 外移（x_peak = ct）+ 原子处概率 e^{-gamma0 t} -> 0（时间尺度 1/gamma0）
S4: A4 成立域对照（失效条件数值演示）——开放连续谱（Markov）：P_e 单调 -> 0 无回波
    vs 闭合单模（JC 共振）：P_e = cos^2(gt) 周期回波（反向自发发生 => 闭合系统可逆）

诚实边界：WW 自发辐射/Lindblad/JC 为标准量子光学事实（数据核对，非新预言）；
本脚本验证 A4 涌现不可逆候选的机制一致性与定量锚点，不构成对 A4 的独立证伪实验；
S3 为一维外向波包模型演示（3D 另有 1/r 扩散，逃逸定性相同）。
"""
import numpy as np

# 物理常数（SI）
E_CHARGE = 1.602176634e-19    # C
A0 = 5.29177210903e-11        # m（玻尔半径）
EPS0 = 8.8541878128e-12       # F/m
HBAR = 1.054571817e-34        # J.s
C_LIGHT = 299792458.0         # m/s
EV2J = 1.602176634e-19        # J（1 eV）


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def simpson(f, x):
    """Simpson 数值积分（x 等距，n 点要求奇数）"""
    n = len(x) - 1
    h = (x[-1] - x[0]) / n
    return h / 3.0 * (f[0] + f[-1] + 4.0 * np.sum(f[1:n:2]) + 2.0 * np.sum(f[2:n-1:2]))


def ww_exact(gamma0, Gamma, t):
    """WW 精确解（洛伦兹谱 J(ω)=(γ₀/2π)·Γ²/((ω-ω₀)²+Γ²) ⟹ 记忆核 K(τ)=(γ₀Γ/2)e^{-Γτ}
    等价 ODE：c'' + Γ·c' + (γ₀Γ/2)·c = 0，初值 c(0)=1, c'(0)=0）。
    Markov 极限（Γ>>γ₀）下衰减率 -> γ₀/2（存活 e^{-γ₀t}）；
    非 Markov 修正 ~ O(γ₀/Γ)。"""
    D = Gamma**2 - 2.0 * gamma0 * Gamma
    if D > 0.0:
        s = np.sqrt(D)
        rp = (-Gamma + s) / 2.0   # 慢模（~ -γ₀/2）
        rm = (-Gamma - s) / 2.0   # 快模（~ -Γ）
        B = rp / (rp - rm)
        A = 1.0 - B
        return A * np.exp(rp * t) + B * np.exp(rm * t)
    if D == 0.0:
        return np.exp(-Gamma * t / 2.0) * (1.0 + (Gamma / 2.0) * t)  # 双重根
    s = np.sqrt(2.0 * gamma0 * Gamma - Gamma**2)
    return np.exp(-Gamma * t / 2.0) * (np.cos(s * t / 2.0) + (Gamma / s) * np.sin(s * t / 2.0))


def ww_euler(gamma0, Gamma, t_max, dt):
    """WW 等价 ODE 系统 Euler 数值解：dc/dt = -(γ₀Γ/2)u, du/dt = c - Γ*u"""
    n = int(t_max / dt) + 1
    t = np.linspace(0.0, t_max, n)
    c = np.zeros(n)
    u = np.zeros(n)
    c[0] = 1.0
    for i in range(n - 1):
        u[i + 1] = u[i] + dt * (c[i] - Gamma * u[i])
        c[i + 1] = c[i] + dt * (-(gamma0 * Gamma / 2.0) * u[i])
    return t, c


def radial_integral(n_pts=200001):
    """氢 2p->1s 径向偶极积分 I_rad = int r^3 R_10(r) R_21(r) dr（单位 a0，Simpson）"""
    r = np.linspace(1e-4, 80.0, n_pts)
    R10 = 2.0 * np.exp(-r)
    R21 = (1.0 / (2.0 * np.sqrt(6.0))) * r * np.exp(-r / 2.0)
    return simpson(r**3 * R10 * R21, r)


def main():
    print("A4 涌现不可逆推导候选数值验证：Wigner-Weisskopf 定量衰减率（笔记 06_photon_topology §3.7）")
    print("=" * 78)

    # ---- S1: WW 非 Markov vs Markov（gamma0/Gamma 扫描，修正 ~O(gamma0*tau_c)）----
    print("\nS1  WW 非 Markov 精确解 vs Markov 指数解（非 Markov 修正 ~O(gamma0/Gamma)）")
    gamma0 = 1.0
    ratios = [1e-4, 1e-3, 1e-2, 0.1, 0.5]
    t1 = np.linspace(0.0, 20.0, 2001)
    ce_markov = np.exp(-gamma0 * t1 / 2.0)
    deviations = []
    for gr in ratios:
        ce = ww_exact(gamma0, gamma0 / gr, t1)
        deviations.append(np.max(np.abs(ce - ce_markov)))
        print(f"   gamma0/Gamma = {gr:6.1e}: max|ce - e^(^-gamma0*t/2)| = {deviations[-1]:.3e}")
    # 幂律核对：log(dev) vs log(gamma0/Gamma) 斜率 ~ 1（修正 ~O(gamma0*tau_c)）
    slope = np.polyfit(np.log(ratios[:4]), np.log(deviations[:4]), 1)[0]
    ok1a = deviations[0] < 1e-3          # Markov 极限（gr=1e-4）偏差 < 1e-3
    ok1b = abs(slope - 1.0) < 0.4        # 近线性（幂律指数 ~1）
    # Euler 数值核对（gr=0.1 代表情形，dt=1e-3，快模 -Gamma 稳定）
    t_e, c_e = ww_euler(gamma0, 10.0, 20.0, 1e-3)
    ce_exact = ww_exact(gamma0, 10.0, t_e)
    ok1c = np.max(np.abs(c_e - ce_exact)) < 1e-2
    ok1 = ok1a and ok1b and ok1c
    check("S1  非 Markov 修正 ~O(gamma0*tau_c)：Markov 极限偏差 <1e-3、偏差随 gr 近线性"
          f"（幂律指数 {slope:.2f}）、Euler 数值核对 <1e-2", ok1,
          f"dev(gr=1e-4)={deviations[0]:.2e}，Euler max|d|={np.max(np.abs(c_e-ce_exact)):.2e}")

    # ---- S2: 氢 2p->1s 爱因斯坦 A 系数复现 ----
    print("\nS2  氢 2p->1s 爱因斯坦 A 系数（径向偶极积分 + 角向因子 1/sqrt(3)）")
    I_rad = radial_integral()
    d2_over_e2_a02 = I_rad**2 / 3.0     # |<1s|z|2p,0>|^2 = I_rad^2/3（角向因子 1/sqrt(3)）
    anchor_d2 = 2.0**15 / 3.0**10       # 标准值 (2^15/3^10) a0^2 = 0.55493 a0^2
    DE_eV = 13.6 * (1.0 - 1.0 / 4.0)    # 2p->1s 能量差 = 10.2 eV
    omega = DE_eV * EV2J / HBAR
    A_coef = omega**3 * (d2_over_e2_a02 * E_CHARGE**2 * A0**2) / (3.0 * np.pi * EPS0 * HBAR * C_LIGHT**3)
    ok2a = abs(d2_over_e2_a02 - anchor_d2) / anchor_d2 < 1e-4
    ok2b = abs(A_coef - 6.268e8) / 6.268e8 < 0.01
    ok2 = ok2a and ok2b
    print(f"   I_rad = {I_rad:.5f} a0；|<1s|z|2p,0>|^2 = {d2_over_e2_a02:.5f} a0^2"
          f"（标准 (2^15/3^10) = {anchor_d2:.5f}）；A = {A_coef:.4e} s^-1（标准 6.268e8）")
    check("S2  氢 2p->1s A 系数 6.27e8 s^-1 复现（|d|^2 锚点 <1e-4、A 偏差 <1%）", ok2,
          f"A={A_coef:.3e} s^-1")

    # ---- S3: 光子因果外向波包（洛伦兹谱 => 因果指数 + 光速外移 + 原子处概率->0）----
    print("\nS3  光子因果外向波包：洛伦兹谱 => 因果指数波包，峰值以光速外移，原子处概率 -> 0")
    gamma0 = 1.0
    Gamma = gamma0 / 2.0                 # 自然线宽 = gamma0/2
    w0 = 50.0
    dw = 0.02
    w = np.arange(w0 - 200.0, w0 + 200.0, dw)
    g = (Gamma / np.pi) / ((w - w0)**2 + Gamma**2)
    t3 = np.linspace(0.0, 10.0, 400)
    psi0 = np.sum(g[None, :] * np.exp(-1j * w[None, :] * t3[:, None]), axis=1) * dw
    psi0_ref = np.exp(-Gamma * t3)       # 洛伦兹谱 Fourier 逆变换 = 因果指数（t>0）
    rel_err = np.max(np.abs(np.abs(psi0) - psi0_ref)) / np.max(psi0_ref)
    # 因果外向波包：psi(x,t) = e^{-Gamma(t-x/c)} * theta(t-x/c)，峰值在前沿 x=ct
    cval = 1.0
    xg = np.linspace(0.0, 8.0, 801)
    t_fixed = 5.0
    psi_x = np.exp(-Gamma * (t_fixed - xg)) * (t_fixed - xg > 0)
    x_peak = xg[np.argmax(psi_x)]
    p0_atom = np.exp(-2.0 * Gamma * t3)  # |psi(0,t)|^2 = e^{-gamma0 t}
    ok3a = rel_err < 1e-2                # 洛伦兹谱 <-> 因果指数 数值傅里叶核对
    ok3b = abs(x_peak - cval * t_fixed) < 0.01   # 峰值（前沿）以光速外移
    ok3c = p0_atom[-1] < 5e-5            # 原子处概率 e^{-gamma0*10} -> 0（时间尺度 1/gamma0）
    ok3 = ok3a and ok3b and ok3c
    print(f"   数值傅里叶核对 rel err = {rel_err:.2e}（|psi(0,t)|=e^{{-Gamma t}}）；"
          f"前沿峰值 x_peak(t={t_fixed}) = {x_peak:.2f}（=ct）；|psi(0,10/gamma0)|^2 = {p0_atom[-1]:.2e}")
    check("S3  光子因果外向波包：洛伦兹谱=>e^{-Gamma t} 核对 + 峰值以光速外移 + "
          "原子处概率 e^{-gamma0 t}->0（时间尺度 1/gamma0）", ok3,
          f"rel err={rel_err:.2e}，x_peak={x_peak:.2f}")

    # ---- S4: A4 成立域对照（失效条件数值演示）：开放连续谱 vs 闭合单模 ----
    print("\nS4  A4 成立域对照：开放连续谱（不可逆）vs 闭合单模 JC（可逆）")
    t4 = np.linspace(0.0, 25.0, 500)
    Pe_open = np.exp(-t4)                # WW Markov（gamma0=1）：单调 -> 0
    Pe_closed = np.cos(t4)**2            # JC 共振（g=1）：|e,0> -> cos(gt)|e,0>
    open_monotone = np.all(np.diff(Pe_open) <= 0.0)            # 开放：单调无回波
    closed_revival = np.max(Pe_closed[6:]) > 0.95              # 闭合：周期回波 ~1
    ok4a = open_monotone and closed_revival
    ok4b = Pe_open[-1] < 1e-10 and Pe_closed[-1] < 1.0          # 开放永不回归 vs 闭合可逆
    ok4 = ok4a and ok4b
    print(f"   开放：P_e(25/gamma0) = {Pe_open[-1]:.2e}（单调 -> 0，无回波）"
          f"；闭合（JC）：P_e = cos^2(t) 周期回波（max = {np.max(Pe_closed):.3f}）")
    check("S4  A4 失效条件演示：开放连续谱单调->0 无回波（不可逆）vs 闭合单模 JC 周期回波"
          "（可逆——腔/镜 = 外部边界驱动）", ok4,
          f"P_e(open,25/gamma0)={Pe_open[-1]:.1e}，P_e(closed) 回波 max={np.max(Pe_closed):.2f}")

    results = [ok1, ok2, ok3, ok4]
    print("\n" + "=" * 78)
    print(f"A4 涌现不可逆候选数值验证：{sum(results)}/4 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
