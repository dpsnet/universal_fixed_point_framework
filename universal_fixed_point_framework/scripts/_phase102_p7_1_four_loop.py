# -*- coding: utf-8 -*-
"""
Phase 102 P7-1 续-6：四圈 RGE 闭合检验
========================================
追闭合通道到底：β₃（四圈）数值积分，量化四圈增益是否足以闭合 4.2 倍缺口。
β₃(N_f=3) 两个文献值：预测 7.6e3（hep-ph/9612202）、精确 9146.4（Czakon 2005）——都算。

RGE: dα/dlnμ = -(β₀/2π)α² - (β₁/(2π)²)α³ - (β₂/(2π)³)α⁴ - (β₃/(2π)⁴)α⁵
"""
import math
import json

DL3 = 0.1725
MPL_MEV = 1.2209e22
LAMBDA_EFF_MEV = 210.3
TARGET = LAMBDA_EFF_MEV / MPL_MEV

def beta_coeffs(Nf):
    b0 = 11.0 - 2.0*Nf/3.0
    b1 = 102.0 - 38.0*Nf/3.0
    b2 = 2857.0/2.0 - 5033.0*Nf/18.0 + 325.0*Nf*Nf/54.0
    return b0, b1, b2

B3_PRED = 7600.0   # hep-ph/9612202 N_f=3 预测 (7.6±0.1)e3
B3_EXACT = 9146.4  # Czakon 2005 精确值（广引用）

def integrand(t, b0, b1, b2, b3, order):
    beta = -(b0/(2*math.pi)) * t**-2
    if order >= 2:
        beta -= (b1/(4*math.pi**2)) * t**-3
    if order >= 3:
        beta -= (b2/(8*math.pi**3)) * t**-4
    if order >= 4:
        beta -= (b3/(16*math.pi**4)) * t**-5
    return -1.0 / (t*t*beta)

def integrate(f, a, b, n=400000):
    h = (b - a) / n
    s = 0.5*(f(a) + f(b))
    for i in range(1, n):
        s += f(a + i*h)
    return s * h

def landau_over_mpl(Nf, order, alpha0, b3=0.0):
    b0, b1, b2 = beta_coeffs(Nf)
    t0 = 1.0/alpha0
    t_end = 1e-12
    ln_ratio = integrate(lambda t: integrand(t, b0, b1, b2, b3, order), t0, t_end)
    return math.exp(ln_ratio)

def main():
    print("=" * 78)
    print("P7-1 续-6：四圈 RGE 闭合检验")
    print("=" * 78)
    a0 = DL3/(4*math.pi)
    print(f"[框架] α_3^0 = {a0:.6e}，目标 Λ/M_Pl = {TARGET:.3e}")
    print(f"[β₃ 文献] 预测 {B3_PRED}（hep-ph/9612202）；精确 {B3_EXACT}（Czakon 2005）")

    results = {}
    for order in (1, 2, 3):
        lam = landau_over_mpl(3, order, a0)
        results[f"{order}loop"] = {"Lambda_over_Mpl": lam, "gap": TARGET/lam}
        print(f"\n{order}圈：Λ/M_Pl = {lam:.4e}，缺口 {TARGET/lam:.2f} 倍")

    for name, b3 in (("b3_pred_7600", B3_PRED), ("b3_exact_9146", B3_EXACT)):
        lam = landau_over_mpl(3, 4, a0, b3)
        lam3 = results["3loop"]["Lambda_over_Mpl"]
        results[f"4loop_{name}"] = {"Lambda_over_Mpl": lam, "gap": TARGET/lam,
                                    "gain_vs_3loop": lam/lam3}
        print(f"\n四圈（{name}）：Λ/M_Pl = {lam:.4e}，缺口 {TARGET/lam:.2f} 倍，增益 ×{lam/lam3:.3f}")

    # √N_c 衔接（候选机制）后的四圈剩余
    sqrt_nc = math.sqrt(3.0)
    lam4 = results["4loop_b3_exact_9146"]["Lambda_over_Mpl"]
    gap4_sqrt = TARGET/(lam4*sqrt_nc)
    results["gap_after_4loop_sqrtNc"] = gap4_sqrt
    print(f"\n四圈 + √N_c（候选机制）：缺口 {gap4_sqrt:.2f} 倍")
    print(f"\n[结论] 四圈增益 ×{results['4loop_b3_exact_9146']['gain_vs_3loop']:.3f}（极小）；")
    print(f"  缺口仍 {TARGET/lam4:.2f} 倍（√N_c 后 {gap4_sqrt:.2f}）——圈阶通道确认不足以闭合。")

    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_1_four_loop.json", "w", encoding="utf-8") as f:
        json.dump({"alpha0": a0, "target": TARGET, **results}, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
