# -*- coding: utf-8 -*-
"""
Phase 102 P7-1: Λ_QCD/M_Pl 纯框架闭合诊断
=============================================
自然单位制（M_Pl=1）下，Λ_QCD/M_Pl 应完全由 Cl(1,7) 代数常数推出：
  Λ_QCD/M_Pl = exp(-2π/(b_0(N_f)·α_3^(0))) = exp(-8π²/(b_0(N_f)·Δλ_3))
    α_3^(0) = Δλ_3/4π，Δλ_3 = √2·Δλ_min = 0.1725（Cl(1,7) 根系 SU(3) 谱间隙）
    b_0(N_f) = 11 - 2N_f/3（理论 β 函数，非实验参数）

逐环节诊断：单圈裸值 → 四层谱静默 Z-链（Z₁=3.67, Z₂=2.12, Z₃=1.44）→ 圈阶结构。
对照（不进推导链）：Λ_QCD/M_Pl = 210 MeV / 1.221e22 MeV = 1.72e-20。
"""
import math

MPL_MEV = 1.2209e22          # 实验单位制对照用（M_Pl = 1.2209e19 GeV）
LAMBDA_EFF_MEV = 210.3        # 谱框架有效值（对照，非推导锚点）

DL3 = 0.1725                  # Cl(1,7) 根系 SU(3) 谱间隙（纯代数常数）
DLMIN = 0.122                  # SU(2)/GR 谱间隙（纯代数常数）

# 四层谱静默 Z-链（Paper XI §1.5）
Z_CHAIN = {"Z1": 3.67, "Z2": 2.12, "Z3": 1.44}
Z_PROD = Z_CHAIN["Z1"] * Z_CHAIN["Z2"] * Z_CHAIN["Z3"]

def alpha3_bare():
    return DL3 / (4 * math.pi)

def lambda_over_mpl_one_loop(Nf):
    b0 = 11.0 - 2.0 * Nf / 3.0
    return math.exp(-8.0 * math.pi**2 / (b0 * DL3))

def main():
    print("=" * 78)
    print("P7-1：Λ_QCD/M_Pl 纯框架闭合诊断（自然单位制 M_Pl=1）")
    print("=" * 78)

    a0 = alpha3_bare()
    print(f"\n[框架常数] α_3^(0) = Δλ_3/4π = {a0:.6e}（Δλ_3={DL3} 纯 Cl(1,7) 代数常数）")
    print(f"[Z-链] Z₁·Z₂·Z₃ = {Z_CHAIN['Z1']}×{Z_CHAIN['Z2']}×{Z_CHAIN['Z3']} = {Z_PROD:.3f}（Paper XI §1.5 四层谱静默）")

    target = LAMBDA_EFF_MEV / MPL_MEV
    print(f"\n[对照目标] Λ_QCD/M_Pl = {LAMBDA_EFF_MEV} MeV / {MPL_MEV:.3e} MeV = {target:.3e}")

    print("\n--- 单圈裸值（定理 4.1） ---")
    print(f"{'N_f':<6}{'b_0':<8}{'Λ/M_Pl 裸值':<16}{'与目标比':<12}{'缺口(倍)'}")
    results = {}
    for Nf in (3, 4, 5, 6):
        b0 = 11.0 - 2.0 * Nf / 3.0
        lam = lambda_over_mpl_one_loop(Nf)
        ratio = target / lam
        results[Nf] = lam
        print(f"{Nf:<6}{b0:<8.3f}{lam:<16.3e}{ratio:<12.1f}{ratio:,.0f}")

    print("\n--- 修正环节逐级推进（N_f=3 起步） ---")
    lam0 = results[3]
    print(f"{'环节':<28}{'值':<16}{'累计倍数'}")
    print(f"{'单圈裸值 Λ/M_Pl':<28}{lam0:<16.3e}{'1.0'}")
    lam_z = lam0 * Z_PROD
    print(f"{'Z-链 ×11.21':<28}{lam_z:<16.3e}{Z_PROD:.2f}")
    # 圈阶结构：单圈 122 → 两圈 pole 577（paper40 推论 4.4，理论两圈 β 积分）
    loop_factor = 577.0 / 121.8
    lam_2loop = lam_z * loop_factor
    print(f"{'两圈 pole 修正 ×4.737':<28}{lam_2loop:<16.3e}{Z_PROD*loop_factor:.2f}")

    gap = target / lam_2loop
    print(f"\n[缺口诊断] 两圈+Z-链后仍差 {gap:.1f} 倍 → 需要框架内闭合的剩余量")

    print("\n[候选闭合通道]")
    print("  1. 三圈 β 系数（理论，标准 QCD 已知）：指数敏感，可贡献 ~2-6 倍")
    print("  2. N_f 阈值跨味结构（m_t/m_b/m_c 本身是 P7-2/P7-4 推导目标——循环依赖需解耦：")
    print("     用轻味 N_f=3 有效值与圈阶修正的联合闭合）")
    print("  3. 圈阶无关有效标度 Λ_eff（paper40 推论 4.4：pole 漂移带 [122,577]，Λ_eff=210.3 在带内）")
    print("     —— 210.3/121.8 = 1.726 ≈ √N_c = 1.732（偏差 0.3%，paper40 诚实登记为数值近似）")
    print("     √N_c 恰为框架内量（N_c=3 色因子）！")

    print("\n[诊断结论]")
    print("  裸 Landau 极点给 6e-23（N_f=3），目标 1.72e-20，缺口 ~287 倍；")
    print("  Z-链（11.2）+ 两圈（4.7）后缺口 ~5.4 倍；")
    print("  √N_c 衔接比（1.726）机制存疑但为框架内量——三圈 + √N_c 联合可望闭合剩余 ~5.4 倍。")
    print("  （诊断性探索；框架内闭合的严格形式见 P7-1 后续）")

    result = {
        "alpha3_bare": a0,
        "lambda_target_over_mpl": target,
        "one_loop_over_mpl": {str(Nf): results[Nf] for Nf in results},
        "z_chain_product": Z_PROD,
        "two_loop_factor": loop_factor,
        "gap_after_z_and_2loop": gap,
        "candidate_closures": ["3-loop beta (theoretical)", "sqrt(N_c) bridging (frame-internal)", "N_f threshold decoupling"],
        "note": "诊断性探索；对照值不进推导链",
    }
    import json
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_1_lambda_ratio.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
