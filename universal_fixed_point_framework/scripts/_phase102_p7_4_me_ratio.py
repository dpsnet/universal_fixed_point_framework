# -*- coding: utf-8 -*-
"""
Phase 102 P7-4：m_e/M_Pl 电子比值链——轻子扇区 α=1.358 框架化
===============================================================
目标对照：m_e/M_Pl = 0.511/1.221e22 = 4.18e−23

任务：
  A. α_lepton = 1.358（paper11 §8.4 拟合值）的框架身份搜索
     候选：d_H/2（d_H = 2.7095 分形维数，框架登记量）
  B. 三扇区 α 序列体系检验（α_up = 1.945、α_down = 1.229、α_le = 1.358）
  C. m_e/m_τ = (c_1/c_3)^α 谱公式计算
  D. m_e/M_Pl 链条（谱框架 m_τ = y_τ·v/√2）
"""
import math
import json

D_H = 2.7095
SIGMA = 1.0/15.0
DLAMBDA_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72.0)
C1, C2, C3 = 0.0033, 0.0666, 0.9998
V_SP = 246.0
M_PL = 1.221e22
M_TAU_EXP = 1776.9
M_E_EXP = 0.511

def main():
    print("=" * 78)
    print("P7-4：m_e/M_Pl 电子比值链——α=1.358 框架化")
    print("=" * 78)
    print(f"[框架] d_H = {D_H}；σ = 1/15；Δλ_min = {DLAMBDA_MIN:.4f}；c = ({C1}, {C2}, {C3})")

    alpha_le = 1.358
    print(f"\n[A] α_lepton = 1.358 框架身份搜索")
    cands = [
        ("d_H/2", D_H/2.0),
        ("ln15/2", math.log(15.0)/2.0),
        ("1+1/e", 1.0+1.0/math.e),
        ("(d_H+Δλ_min)/2", (D_H+DLAMBDA_MIN)/2.0),
        ("(d_H−Δλ_min)/2", (D_H-DLAMBDA_MIN)/2.0),
    ]
    for name, v in cands:
        dev = (alpha_le/v - 1)*100
        print(f"    {name:16s} = {v:.6f}（偏差 {dev:+.2f}%{' ★' if abs(dev)<0.5 else ''}）")
    print(f"    → d_H/2 = 1.35475 为最优（偏差 +0.24%）——轻子扇区指数 = 分形维数半")

    print(f"\n[B] 三扇区 α 序列体系检验")
    a_up, a_dn, a_le = 1.945, 1.229, 1.358
    c_up = [("ln7", math.log(7.0)), ("d_H/2+0.59", D_H/2+0.59)]
    c_dn = [("d_H/2−Δλ_min", D_H/2-DLAMBDA_MIN), ("ln(3.416)", math.log(3.416))]
    print(f"    α_up = {a_up}：ln7 = {math.log(7.0):.4f}（偏差 {(a_up/math.log(7.0)-1)*100:+.2f}%）")
    print(f"    α_dn = {a_dn}：d_H/2−Δλ_min = {D_H/2-DLAMBDA_MIN:.4f}（偏差 {(a_dn/(D_H/2-DLAMBDA_MIN)-1)*100:+.2f}%）")
    print(f"    α_le = {a_le}：d_H/2 = {D_H/2:.4f}（偏差 {(a_le/(D_H/2)-1)*100:+.2f}%）")
    print(f"    → 三个 <0.31% 命中，但 ln7 与 d_H/2±Δλ_min 非统一构造——体系不统一，登记候选")

    print(f"\n[C] m_e/m_τ 谱公式（α = d_H/2 框架化）")
    alpha_fw = D_H/2.0
    ratio_fw = (C1/C3)**alpha_fw
    ratio_fit = (C1/C3)**alpha_le
    print(f"    (c_1/c_3)^(d_H/2) = ({C1/C3:.5f})^{alpha_fw:.4f} = {ratio_fw:.3e}")
    print(f"    (c_1/c_3)^1.358     = {ratio_fit:.3e}（原拟合值）")
    print(f"    实验 e/τ = 2.9e−4——框架公式偏差 ×{ratio_fw/2.9e-4:.1f}（继承 paper11 §8.4 平均偏差 ×1.37）")

    print(f"\n[D] m_e/M_Pl 链条")
    m_tau_sp = 0.01*V_SP/math.sqrt(2.0)*1000.0   # y_τ·v/√2（y_τ ≈ 0.01 谱框架）
    m_e_sp = ratio_fw*m_tau_sp
    print(f"    m_τ(谱) = y_τ·v/√2 = 0.01×246/√2 = {m_tau_sp:.0f} MeV（实验 {M_TAU_EXP}）")
    print(f"    m_e(谱) = (c_1/c_3)^(d_H/2)·m_τ = {m_e_sp:.3f} MeV（实验 {M_E_EXP}，×{m_e_sp/M_E_EXP:.1f}）")
    print(f"    m_e/M_Pl(谱) = {m_e_sp/M_PL:.2e}（实验 4.18e−23，×{m_e_sp/M_E_EXP:.1f}）")
    print(f"    → 绝对偏差 ×1.5 继承 paper11 轻子扇区预测精度（e/τ 偏差 ×1.5 已登记）")

    print(f"\n[结论]")
    print(f"    ① α_lepton 框架化：d_H/2 = 1.3548（偏差 0.24%）——轻子扇区指数 = 分形维数半（框架登记量）")
    print(f"    ② α 序列：α_down ≈ d_H/2−Δλ_min（0.31%）、α_up ≈ ln7（0.05%）——登记候选，体系不统一")
    print(f"    ③ m_e/M_Pl 链条完整（α 框架化 + m_τ 谱定），绝对偏差 ×1.5 继承 paper11 精度")
    print(f"    ④ 目标 <10% 未达——×1.5 偏差为 paper11 已知（轻子扇区 ×1.5/×2.4），登记为开放")

    result = {
        "alpha_framework": {"d_H_over_2": D_H/2, "dev": (alpha_le/(D_H/2)-1)*100},
        "alpha_sequence": {"up_ln7_dev": (1.945/math.log(7)-1)*100, "down_dH2_minus_dl_dev": (1.229/(D_H/2-DLAMBDA_MIN)-1)*100, "note": "体系不统一"},
        "m_e_over_m_tau": {"fw": ratio_fw, "fit": ratio_fit, "exp": 2.9e-4},
        "m_e_over_MPl": {"pred": m_e_sp/M_PL, "exp": M_E_EXP/M_PL, "factor": m_e_sp/M_E_EXP},
        "conclusion": "α=d_H/2 框架化（0.24%）；m_e/M_Pl 链完整但 ×1.5 偏差继承 paper11——开放",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_4_me_ratio.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
