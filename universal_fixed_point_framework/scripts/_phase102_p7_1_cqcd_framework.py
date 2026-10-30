# -*- coding: utf-8 -*-
"""
Phase 102 P7-1 续-3：C_QCD 框架内起源检验（用户洞察驱动）
=============================================================
用户洞察：C_QCD ≈ 2² − ξ₂/3。

本轮澄清 + 验证：
  A. 上一轮脚本 D 段的 C_QCD_required=3.88 是"√N_c 配 Λ_pert"的混合搭配错误值；
     正确组合 B（N_c 配 Λ_pert）应反推 C_QCD ≈ 2.24 ≈ 2.25。
  B. 检验用户公式：2² − ξ₂/3 = 3.8785 vs 混合伪值 3.8800（0.04% 吻合——巧合分解？）
  C. ★ 真正框架量候选：C_QCD = (N_c/2)² = (3/2)² = 2.25（精确）——检验组合 A/B 复现 F_π
"""
import math
import json

Nc = 3
DLMIN = 0.122
DL3 = 0.1725
K = DL3 / (4*math.pi*DLMIN)          # Δλ_3/4πΔλ_min
LAMBDA_EFF = 210.3                    # MeV
LAMBDA_PERT_1L = 121.8                # MeV（单圈跨味）
LAMBDA_PERT_2L = 577.0                # MeV（两圈 pole）
F_PI_EXP = 92.1                       # MeV（实验对照）

def main():
    print("=" * 78)
    print("C_QCD 框架内起源检验")
    print("=" * 78)

    xi = LAMBDA_EFF / LAMBDA_PERT_1L
    xi2 = LAMBDA_EFF / LAMBDA_PERT_2L
    print(f"\n[A] 澄清：上一轮 C_QCD_required=3.88 的来源")
    c_mixed = F_PI_EXP / (math.sqrt(Nc) * K * LAMBDA_PERT_1L)
    print(f"    混合搭配（√N_c·Λ_pert）：C = {c_mixed:.4f} ← 错误（√N_c 应配 Λ_eff 或 N_c 配 Λ_pert）")
    c_correct_B = F_PI_EXP / (Nc * K * LAMBDA_PERT_1L)
    print(f"    正确组合 B（N_c·Λ_pert）：C = {c_correct_B:.4f}（≈ paper40 的 2.25，偏差 {(c_correct_B/2.25-1)*100:.2f}%）")

    print(f"\n[B] 用户公式检验：2² − ξ₂/3")
    user_val = 4.0 - xi2/3.0
    print(f"    ξ₂ = Λ_eff/Λ_pert2 = {LAMBDA_EFF}/{LAMBDA_PERT_2L} = {xi2:.4f}")
    print(f"    2² − ξ₂/3 = 4 − {xi2/3:.6f} = {user_val:.4f} vs 混合伪值 {c_mixed:.4f}")
    print(f"    吻合偏差 {(user_val/c_mixed-1)*100:.4f}%")
    print(f"    注：ξ₂/3 = {xi2/3:.5f} ≈ Δλ_min = {DLMIN}（偏差 {(xi2/3/DLMIN-1)*100:.2f}%）——")
    print(f"    该巧合使用户公式≈4−Δλ_min=3.878；但 3.88 本身是错误混合值，此吻合为巧合分解")

    print(f"\n[C] ★ 真正框架量候选：C_QCD = (N_c/2)² = ({Nc}/2)² = {(Nc/2.0)**2}")
    c_fw = (Nc/2.0)**2
    print(f"    与 paper40 登记 C_QCD=2.25 偏差 {(c_fw/2.25-1)*100:.4f}%（精确）")
    print(f"\n    组合 A（paper40，√N_c·Λ_eff）：")
    fpi_A = math.sqrt(Nc) * LAMBDA_EFF * K * c_fw
    print(f"      F_π = √N_c·Λ_eff·K·C = {fpi_A:.2f} MeV（实验 92.1，偏差 {(fpi_A/F_PI_EXP-1)*100:.2f}%）")
    print(f"    组合 B（N_c·Λ_pert）：")
    fpi_B = Nc * LAMBDA_PERT_1L * K * c_fw
    print(f"      F_π = N_c·Λ_pert·K·C = {fpi_B:.2f} MeV（实验 92.1，偏差 {(fpi_B/F_PI_EXP-1)*100:.2f}%）")
    print(f"    两组合在 C_QCD=(N_c/2)² 下同时复现 F_π≈92 MeV——ξ=√N_c 等价性的干净数值验证")

    print(f"\n[D] 结论")
    print(f"    ① C_QCD 从'复核自由量'升级为'框架内代数量 (N_c/2)²'——精确零偏差")
    print(f"    ② 用户公式 2²−ξ₂/3 与伪值吻合为巧合（ξ₂/3≈Δλ_min 偏差 0.4%）；")
    print(f"       但用户'C_QCD 应有框架内起源'的直觉正确，正确起源是 (N_c/2)² 而非 4−Δλ_min")
    print(f"    ③ 组合 A/B 在 C_QCD=(N_c/2)² 下自洽（92.2/92.5 MeV）——P7-1 的 √N_c 衔接机制加强")

    result = {
        "c_mixed_error": c_mixed,
        "c_correct_B": c_correct_B,
        "user_formula": user_val,
        "xi2": xi2,
        "xi2_over_3_vs_dlmin": {"xi2_3": xi2/3.0, "dlmin": DLMIN, "dev": xi2/3.0/DLMIN-1},
        "C_QCD_framework": c_fw,
        "C_QCD_paper40": 2.25,
        "Fpi_A": fpi_A, "Fpi_B": fpi_B, "Fpi_exp": F_PI_EXP,
        "conclusion": "C_QCD=(N_c/2)² 精确框架量；用户 2²−ξ₂/3 为巧合分解（ξ₂/3≈Δλ_min）；组合 A/B 自洽",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_1_cqcd_framework.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
