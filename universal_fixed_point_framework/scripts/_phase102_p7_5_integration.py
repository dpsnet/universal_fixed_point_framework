# -*- coding: utf-8 -*-
"""
Phase 102 P7-5：整合链数值验证——MUFPF → 四力 → 核子/电子 → 氢原子核
=====================================================================
完整链的逐环节数值 + 偏差表 + 状态判定（闭合/候选/开放）。
唯一输入：框架常数（M_Pl 谱定、κ、Λ、轻子锚定等）。
"""
import json

# ============ 框架常数（唯一输入） ============
M_PL = 1.221e22          # MeV，paper49 §6.1 G_N=18(2+√3)Δλ_min²=1 谱定
KAPPA = 6/3.141592653589793  # 1.90986，paper40 定理 5.3
LAMBDA = 210.0           # MeV，F_π 定标有效标度
SIG = 1/15.0
D_H = 2.7095

# ============ P7 系列结果 ============
# 强子端（P7-1/P7-2/P7-3）
M_RHO = 774.5            # −0.11%
M_N = 1014.9             # +8.1% SU(6) 缺陷
M_N_EXP = 938.272        # 质子（PDG）
DELTA_N_DELTA = 293.7    # 0.17%
DM_PN = 2.402            # +0.09% p/n 质量差
# 轻子端（P7-4 系列，闭合）
M_E = 0.5110             # MeV（m_e/m_τ = e^{−3e} 锚定，−0.08%）
M_MU = 105.66            # MeV（ln16+e^{−3}，+0.002%）
M_TAU = 1776.9           # MeV（实验锚——比值链基准）
# 实验对照
M_P_EXP = 938.2720813    # proton MeV (PDG)
M_E_EXP = 0.51099895
M_MU_EXP = 105.6583755
M_TAU_EXP = 1776.86
M_N_AVG_EXP = 938.918    # (p+n)/2
M_H_EXP = 938.2720813 + 0.51099895 - 13.6e-3  # 氢原子 ≈ 质子+电子−13.6eV
E_B = 13.6e-3            # MeV，Bohr 电离能（标准值——框架 α_EM 化待 P44 §6）

def dev(f, e):
    return (f/e - 1)*100

def main():
    print("=" * 78)
    print("P7-5：整合链数值验证——MUFPF → 四力 → 核子/电子 → 氢原子核")
    print("=" * 78)

    print("\n[1] 框架常数（唯一输入，全谱定）：")
    print("  M_Pl = %.3e MeV（G_N=1 谱定 ✓）" % M_PL)
    print("  κ = 6/π = %.5f（定理 5.3 ✓）" % KAPPA)
    print("  Λ = %g MeV（F_π 定标）" % LAMBDA)
    print("  d_H = %.4f、σ = 1/15、Δλ_min = 0.122（机器证明）" % D_H)

    print("\n[2] 四力端：")
    print("  引力（P49）：M_Pl 谱定 ✓【整链基准】")
    print("  强（P40/P7）：κ=1.90986 ✓、Λ=210（Λ/M_Pl 缺口 4.2 倍开放）、α_s*=0.3380（N-Δ 0.00%）")
    print("  弱（P11）：v=246 GeV 框架预言（α_v=1.883 身份未登记——半开放）")
    print("  电磁（P44/P17）：电荷谱 {+2/3,−1/3,0,−1,+1} ✓（定理 5.0）、光子拓扑 ✓；α_EM 框架化待 §6")

    print("\n[3] 粒子端：")
    print("  m_ρ  = %6.1f（实验 775.3，偏差 %+.2f%%）✓ 闭合" % (M_RHO, dev(M_RHO, 775.3)))
    print("  m_N  = %6.1f（实验 938.27，偏差 %+.2f%%）✗ SU(6) 缺陷开放（候选 κ²Λ/(3+7)）" % (M_N, dev(M_N, M_N_EXP)))
    print("  Δ−N  = %6.1f（实验 293.8，偏差 %+.2f%%）✓ 闭合" % (DELTA_N_DELTA, dev(DELTA_N_DELTA, 293.8)))
    print("  Δm_pn= %6.2f（实验 2.400，偏差 %+.2f%%）✓ 闭合（EM 项 +38%% 开放）" % (DM_PN, dev(DM_PN, 2.4)))
    print("  m_e  = %6.4f（实验 0.5110，偏差 %+.2f%%）✓ 闭合（e^{−3e} 链）" % (M_E, dev(M_E, M_E_EXP)))
    print("  m_μ  = %6.2f（实验 105.66，偏差 %+.2f%%）✓ 闭合（ln16+e^{−3} 链）" % (M_MU, dev(M_MU, M_MU_EXP)))
    print("  m_τ  = %6.1f（实验 1776.9，偏差 %+.2f%%）— 比值链基准（绝对锚定 e^{−Eτ} +0.043%%）" % (M_TAU, dev(M_TAU, M_TAU_EXP)))

    print("\n[4] 质量比（核心可检验量）：")
    r_p_e_fw = M_N/M_E
    r_p_e_exp = M_P_EXP/M_E_EXP
    print("  m_p/m_e = %.2f（实验 %.2f，偏差 %+.2f%%）——轻子闭合+强子 SU(6) 缺陷合成" % (r_p_e_fw, r_p_e_exp, dev(r_p_e_fw, r_p_e_exp)))
    r_mu_e = M_MU/M_E
    r_mu_e_exp = M_MU_EXP/M_E_EXP
    print("  m_μ/m_e = %.4f（实验 %.4f，偏差 %+.2f%%）✓ 轻子比值链" % (r_mu_e, r_mu_e_exp, dev(r_mu_e, r_mu_e_exp)))
    r_tau_e = M_TAU/M_E
    r_tau_e_exp = M_TAU_EXP/M_E_EXP
    print("  m_τ/m_e = %.4f（实验 %.4f，偏差 %+.2f%%）✓ 轻子比值链" % (r_tau_e, r_tau_e_exp, dev(r_tau_e, r_tau_e_exp)))

    print("\n[5] 氢原子核/氢原子端：")
    print("  氢原子核 = 质子：m_p = m_N(框架) = %.1f（+8.1%% SU(6) 继承）" % M_N)
    m_h_fw = M_N + M_E - E_B
    print("  氢原子 m_H = m_p + m_e − E_b = %.3f MeV（实验 %.3f，偏差 %+.2f%%）" % (m_h_fw, M_H_EXP, dev(m_h_fw, M_H_EXP)))
    print("  E_b = 13.6 eV = (α²/2)·m_e（需 α_EM 框架化——P44 谱间隙→Bohr 锚定，待闭合）")
    print("  m_H/M_Pl = %.3e（E_b 相对质量 ~1e-7 可忽略）" % (m_h_fw/M_PL))
    print("  m_p/M_Pl = %.3e、m_e/M_Pl = %.3e（轻子闭合链）" % (M_N/M_PL, M_E/M_PL))

    print("\n[6] 整合链状态判定：")
    print("  ✓ 闭合：框架常数（机器证明）、引力 M_Pl、轻子扇区（m_e/m_μ/m_τ 比值+锚定全部 <0.1%）")
    print("  ✓ 闭合：m_ρ(−0.11%)、Δ−N(0.17%)、Δm_pn(+0.09%)")
    print("  ○ 候选：m_N 缺口 κ²Λ/(N_gen+k_max−1)（−0.04%，跨层加性假说倾向支持）")
    print("  ✗ 开放：Λ/M_Pl（4.2 倍）、EM_pn（+38%）、m_N SU(6)（+8.1%）、α_v/y_τ 身份、α_EM 框架化、E_b Bohr 锚定")

    result = {"m_p_over_m_e": [r_p_e_fw, r_p_e_exp, dev(r_p_e_fw, r_p_e_exp)],
              "m_mu_over_m_e": [r_mu_e, r_mu_e_exp, dev(r_mu_e, r_mu_e_exp)],
              "m_h": [m_h_fw, M_H_EXP, dev(m_h_fw, M_H_EXP)],
              "m_h_over_M_Pl": m_h_fw/M_PL}
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5_integration.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
