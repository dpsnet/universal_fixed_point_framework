#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_hawking_kerr.py — 61D 深化：Kerr 蒸发动力学推广（Schwarzschild → 转动黑洞）
=============================================================================
对应笔记：notes/04_lorentz_gravity/spectral_black_hole_evolution_formalization.md（61D）
          + roadmap/phase61_physics_advancement.md 61D 遗留开放项（Kerr 蒸发动力学推广）
对应论文：paper/paper42_black_hole_quantum_evolution.md（§8 开放项 3，v0.2）

物理：paper42 覆盖 Schwarzschild（a=0）蒸发动力学。本脚本推广到 Kerr（转动）：
  Kerr 视界：r_± = M ± √(M²−a²)，a = J/M 为角动量参数，a* = a/M = J/M² ∈ [0,1)
  Kerr 温度（标准 Bekenstein-Hawking 形状）：T_Kerr ∝ (r_+ − r_−)/(r_+² + a²)
  谱框架推广：以 Schwarzschild 谱温度 T_S = Δλ_min/(2πM) 为基准，归约因子
    f(a*) = T_Kerr/T_S = 2√(1−a*²)/(1+√(1−a*²)) ∈ (0,1]
    a*=0 → f=1（Schwarzschild 极限）；a*→1 → f→0（极端 Kerr 冷却，蒸发终止）
  蒸发动力学（质量 + 角动量耦合，超辐射优先辐射角动量）：
    dM/dt = −α·f(a*)⁴/M²   （Stefan-Boltzmann：功率 ∝ T⁴）
    dJ/dt = −β·a*·f(a*)/M  （超辐射：角动量优先辐射，β/α = r_J > 1）

验证内容（K1–K6）：
  K1  Kerr 温度归约：T_Kerr(M, a=0) = Δλ_min/(2πM)（Schwarzschild 谱极限）
  K2  转动降温：T_Kerr 随 a* 递减（a*₁ < a*₂ → T₁ > T₂）
  K3  极端冷却：a* → 1 时 T_Kerr → 0（极端黑洞蒸发终止）
  K4  蒸发寿命延长：t_evap(a*₀) ≥ t_evap(0)（f ≤ 1 数学保证，转动显著延长）
  K5  演化方向：a*(t) 递减（超辐射优先辐射角动量，Kerr → Schwarzschild）
  K6  谱判据定标自洽：f(a*) ∈ (0,1]（转动不增温）

谱间隙：Δλ_min = (√6−√2)/√72 ≈ 0.1221（与 paperX_hawking_spectrum.py 一致）。
"""
import math
import numpy as np
from scipy.integrate import solve_ivp

# ============================================================
# 常数
# ============================================================
DELTA_LAMBDA_MIN = (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)  # ≈ 0.1221
ALPHA = 1e-4        # 蒸发率标度（与 paperX_hawking_spectrum.py 一致）
R_J = 2.0           # 超辐射角动量辐射率 β/α（角动量优先辐射）

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def t_schwarz(M):
    """Schwarzschild 谱温度：T_S = Δλ_min/(2πM)。"""
    return DELTA_LAMBDA_MIN / (2 * math.pi * M)


def f_kerr(a_star):
    """转动归约因子：f(a*) = T_Kerr/T_S = 2√(1−a*²)/(1+√(1−a*²)) ∈ (0,1]。"""
    if a_star >= 1.0:
        return 0.0
    s = math.sqrt(max(1.0 - a_star * a_star, 0.0))
    return 2.0 * s / (1.0 + s)


def t_kerr(M, a_star):
    """Kerr 谱温度：T_Kerr = T_S·f(a*)。"""
    return t_schwarz(M) * f_kerr(a_star)


def evaporate(M0, a_star0, alpha=ALPHA, r_j=R_J, t_max=2e8, M_end=0.01):
    """蒸发动力学数值积分（欧拉/solve_ivp）。
    返回 (t 网格, M(t), a*(t))。终止：M → M_end·M0 或 t_max。"""
    def rhs(t, y):
        M, J = y
        a_star = min(J / (M * M), 0.999999)
        f = f_kerr(a_star)
        dM = -alpha * f**4 / (M * M)
        dJ = -r_j * alpha * a_star * f / M
        return [dM, dJ]

    def stop(t, y):
        return y[0] - M_end * M0
    stop.direction = -1

    sol = solve_ivp(rhs, [0.0, t_max], [M0, a_star0 * M0 * M0],
                    events=stop, rtol=1e-9, atol=1e-12, max_step=1e4)
    return sol.t, sol.y[0], sol.y[1] / sol.y[0]**2


def run_k1_k2_k3():
    print("\n" + "=" * 74)
    print("  K1/K2/K3. Kerr 谱温度：归约 + 转动降温 + 极端冷却")
    print("=" * 74)
    M = 2.0
    T_S = t_schwarz(M)
    T0 = t_kerr(M, 0.0)
    print(f"  Schwarzschild 谱温度 T_S({M}) = {T_S:.4f}")
    print(f"  T_Kerr(M, a*=0) = {T0:.4f}（归约因子 f(0) = {f_kerr(0.0):.3f}）")
    check("K1 Kerr 温度归约：T_Kerr(a*=0) = Δλ_min/(2πM)", abs(T0 - T_S) < 1e-12,
          f"f(0) = {f_kerr(0.0):.3f}")
    # 转动降温
    vals = [(a, t_kerr(M, a)) for a in (0.0, 0.3, 0.6, 0.9)]
    mono = all(vals[i][1] > vals[i+1][1] for i in range(len(vals)-1))
    print(f"  T_Kerr 随 a*：{[f'{a}: {t:.4f}' for a, t in vals]}")
    check("K2 转动降温：T_Kerr 随 a* 单调递减", mono,
          f"({vals[0][1]:.4f} → {vals[-1][1]:.4f})")
    # 极端冷却（渐近趋零验证：a* → 1 时 f → 0 单调）
    ext_ks = (3, 5, 7, 9)
    ext_vals = [(1 - 10**(-k), f_kerr(1 - 10**(-k))) for k in ext_ks]
    T_ext = t_kerr(M, ext_vals[-1][0])
    ratio = T_ext / T_S
    print(f"  极端渐近 f(a*)：{[f'1−1e-{k}: {f:.2e}' for k, (_, f) in zip(ext_ks, ext_vals)]}")
    print(f"  极端极限 T_Kerr(a*→1)/T_S = {ratio:.2e}（极端 Kerr 冷却）")
    check("K3 极端冷却：a* → 1 时 T_Kerr/T_S < 1e-3（蒸发终止）", ratio < 1e-3,
          f"比值 = {ratio:.2e}")


def run_k4():
    print("\n" + "=" * 74)
    print("  K4. 蒸发寿命延长：转动黑洞蒸发更慢")
    print("=" * 74)
    M0 = 10.0
    t_evap_list = []
    for a0 in (0.0, 0.3, 0.6, 0.9):
        t, M, a_star = evaporate(M0, a0)
        t_evap = t[-1] if len(t) else float('nan')
        t_evap_list.append((a0, t_evap))
        print(f"  a*₀ = {a0:.1f}: t_evap = {t_evap:.3e}")
    # f ≤ 1 数学保证 t_evap(a*₀) ≥ t_evap(0)
    t0 = t_evap_list[0][1]
    ok_all = all(ti >= t0 - 1e-6 for _, ti in t_evap_list)
    t09 = t_evap_list[-1][1]
    print(f"  t_evap(0) = {t0:.3e}，t_evap(0.9) = {t09:.3e}（延长 {t09/t0:.2f}×）")
    check("K4 蒸发寿命延长：t_evap(a*₀) ≥ t_evap(0)（f ≤ 1 数学保证）", ok_all,
          f"t_evap(0.9)/t_evap(0) = {t09/t0:.2f}")


def run_k5():
    print("\n" + "=" * 74)
    print("  K5. 演化方向：超辐射优先辐射角动量 → a*(t) 递减")
    print("=" * 74)
    M0 = 10.0
    t, M, a_star = evaporate(M0, 0.9)
    # 抽样检查 a* 单调递减
    idx = np.linspace(0, len(a_star) - 1, 6).astype(int)
    samples = [(t[i], a_star[i]) for i in idx]
    mono_dec = all(samples[i][1] >= samples[i+1][1] for i in range(len(samples)-1))
    print(f"  a*(t) 轨迹：{[f't={t:.1e}: a*={a:.3f}' for t, a in samples]}")
    final = a_star[-1]
    check("K5 a*(t) 单调递减（Kerr → Schwarzschild 演化方向）", mono_dec,
          f"a*(0)={samples[0][1]:.3f} → a*(t_evap)={final:.3f}")


def run_k6():
    print("\n" + "=" * 74)
    print("  K6. 谱判据定标自洽：f(a*) ∈ (0,1]（转动不增温）")
    print("=" * 74)
    ok = all(0.0 < f_kerr(a) <= 1.0 for a in np.linspace(0.0, 0.999, 100))
    print(f"  f(a*) ∈ (0,1] for a* ∈ [0, 1)：扫描 100 点全部满足")
    check("K6 转动归约因子 ∈ (0,1]（T_Kerr ≤ T_S，谱间隙定标自洽）", ok,
          "f ∈ (0,1]")


# ============================================================
# 主函数
# ============================================================

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  61D 深化：Kerr 蒸发动力学推广（Schwarzschild → 转动黑洞）     ║")
    print("║  谱温度归约 + 转动降温 + 极端冷却 + 超辐射角动量优先辐射       ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    run_k1_k2_k3()
    run_k4()
    run_k5()
    run_k6()

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  关键数值（笔记引用）：")
    M0 = 10.0
    t0, _, _ = evaporate(M0, 0.0)
    t9, _, _ = evaporate(M0, 0.9)
    print(f"    f(a*)            = 2√(1−a*²)/(1+√(1−a*²)) ∈ (0,1]")
    print(f"    T_Kerr(a*→1)/T_S = 0（极端 Kerr 冷却）")
    print(f"    t_evap(0)/t_evap(0.9) = {t0[-1]:.3e} / {t9[-1]:.3e}"
          f"（延长 {t9[-1]/t0[-1]:.2f}×）")


if __name__ == "__main__":
    main()
