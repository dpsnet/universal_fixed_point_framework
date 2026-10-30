# -*- coding: utf-8 -*-
"""
Phase 102 P7-1 续：三圈 RGE 精确闭合
======================================
目标：以标准理论 β 函数系数（MS-bar，纯理论非实验参数）数值积分 RGE，
求两圈/三圈 Landau 极点 Λ_2/Λ_3，量化圈阶修正因子，检验剩余 4.0 倍缺口
是否由三圈 + √N_c 衔接闭合。

β 系数（标准 QCD MS-bar，理论值）：
  β_0 = 11 - 2N_f/3
  β_1 = 102 - 38N_f/3
  β_2 = 2857/2 - 5033N_f/18 + 325N_f^2/54

RGE: dα/dlnμ = β(α) = -(β_0/2π)α² - (β_1/(2π)²)α³ - (β_2/(2π)³)α⁴
Landau 极点：从 α(M_Pl)=α_3^(0) 积分到 α→∞。

变量替换 t=1/α 消除发散：∫ dα/β(α) 从 α_0 到 ∞ = -∫ dt/(t²·β(1/t)) 从 1/α_0 到 0。
"""
import math
import json

# 框架常数
DL3 = 0.1725
MPL_MEV = 1.2209e22
LAMBDA_EFF_MEV = 210.3  # 对照（不进推导链）
TARGET = LAMBDA_EFF_MEV / MPL_MEV

# Z-链（Paper XI §1.5）
Z_PROD = 3.67 * 2.12 * 1.44

# 标准 QCD MS-bar β 系数（纯理论）
def beta_coeffs(Nf):
    b0 = 11.0 - 2.0*Nf/3.0
    b1 = 102.0 - 38.0*Nf/3.0
    b2 = 2857.0/2.0 - 5033.0*Nf/18.0 + 325.0*Nf*Nf/54.0
    return b0, b1, b2

def integrand(t, b0, b1, b2, order):
    """t = 1/α。dα/β(α) 变换后：-dt/(t²·β(1/t))。β(1/t) = -(b0/2π)t^-2 - (b1/4π²)t^-3 - (b2/8π³)t^-4"""
    if order == 1:
        beta = -(b0/(2*math.pi)) * t**-2
    elif order == 2:
        beta = -(b0/(2*math.pi)) * t**-2 - (b1/(4*math.pi**2)) * t**-3
    else:
        beta = -(b0/(2*math.pi)) * t**-2 - (b1/(4*math.pi**2)) * t**-3 - (b2/(8*math.pi**3)) * t**-4
    return -1.0 / (t*t*beta)   # = dα/β 在 α=1/t 处

def integrate(f, a, b, n=200000):
    """梯形积分（t 空间从 a→b）"""
    h = (b - a) / n
    s = 0.5*(f(a) + f(b))
    for i in range(1, n):
        s += f(a + i*h)
    return s * h

def landau_over_mpl(Nf, order, alpha0):
    b0, b1, b2 = beta_coeffs(Nf)
    t0 = 1.0 / alpha0
    t_end = 1e-12  # α→∞
    # ∫ dα/β(α) 从 α_0 到 ∞ = ∫_{-t}^{0}（t=1/α 从 t_0 到 0）：
    # 用 integrate(f, a=t0, b=t_end) 即 ∫_{t0}^{t_end}，β<0 使结果为正的 -2π/(b0·α0)
    ln_ratio = integrate(lambda t: integrand(t, b0, b1, b2, order), t0, t_end)
    return math.exp(ln_ratio)  # Λ/M_Pl

def main():
    print("=" * 78)
    print("P7-1 续：三圈 RGE 精确闭合（N_f=3 轻味通道）")
    print("=" * 78)
    a0 = DL3 / (4*math.pi)
    b0, b1, b2 = beta_coeffs(3)
    print(f"\n[框架常数] α_3^(0) = {a0:.6e}")
    print(f"[理论 β 系数 N_f=3] β_0={b0:.4f}  β_1={b1:.4f}  β_2={b2:.4f}")
    print(f"[对照目标] Λ/M_Pl = {TARGET:.3e}")

    print("\n--- 圈阶推进（Landau 极点数值积分） ---")
    print(f"{'圈阶':<8}{'Λ/M_Pl':<14}{'与目标比':<12}{'缺口(倍)':<12}{'累计修正'}")
    lam_prev = None
    for order in (1, 2, 3):
        lam = landau_over_mpl(3, order, a0)
        gap = TARGET / lam
        factor = 1.0 if lam_prev is None else lam/lam_prev
        lam_prev = lam
        print(f"{order:<8}{lam:<14.3e}{gap:<12.1f}{gap:,.1f}     ×{factor:.3f}")

    lam1 = landau_over_mpl(3, 1, a0)
    lam3 = landau_over_mpl(3, 3, a0)
    lam_z3 = lam3 * Z_PROD
    print(f"\n--- 三圈 + Z-链 + √N_c 联合闭合检验 ---")
    sqrt_nc = math.sqrt(3.0)
    print(f"三圈裸值: {lam3:.3e}；×Z-链({Z_PROD:.2f}): {lam_z3:.3e}")
    print(f"×√N_c({sqrt_nc:.4f}): {lam_z3*sqrt_nc:.3e}；目标 {TARGET:.3e}")
    gap_final = TARGET / (lam_z3 * sqrt_nc)
    print(f"最终缺口: {gap_final:.3f} 倍")

    print("\n--- √N_c 衔接机制论证（框架内） ---")
    print("F_π 谱公式（paper40 L190）：F_π = √N_c·Λ·(Δλ_3/4πΔλ_min)·C_QCD")
    print("  → Λ_eff = F_π/(√N_c·(Δλ_3/4πΔλ_min)·C_QCD)")
    print("Landau 极点（定理 4.1）：Λ_pert = M_Pl·exp(-8π²/(b_0·Δλ_3))")
    print("衔接比 ξ = Λ_eff/Λ_pert = 1.726 ≈ √N_c = 1.732（paper40 已登记，偏差 0.3%）")
    print("机制候选：")
    print("  ① 色因子对偶：Landau 极点指数含 N_c（b_0=11-2N_f/3 的 -2N_f/3 项来自色-味圈）")
    print("     F_π 定标含 √N_c——同一色自由度在指数（极点位置）与定标（凝聚归一）中的对偶表现")
    print("  ② 谱静默四层：Z-链本身编码 N_c 相关的静默层级（Paper XI §1.5）")
    print("  ③ 严格化路径：把 ξ=√N_c 提升为定理需 N_c 在两类公式中的出现做显式追踪")

    result = {
        "alpha0": a0,
        "beta_coeffs_Nf3": {"b0": b0, "b1": b1, "b2": b2},
        "landau": {"1loop": lam1, "2loop": landau_over_mpl(3,2,a0), "3loop": lam3},
        "z_chain": Z_PROD,
        "sqrt_nc": sqrt_nc,
        "gap_after_3loop_z_sqrtNc": gap_final,
        "target": TARGET,
        "note": "理论 β 系数 + 框架常数；对照值不进推导链",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_1_three_loop.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
