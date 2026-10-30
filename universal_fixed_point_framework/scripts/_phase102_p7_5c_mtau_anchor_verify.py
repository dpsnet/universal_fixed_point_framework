# -*- coding: utf-8 -*-
"""
Phase 102 P7-5c 验证：E_tau = 16·dH + ln(16/15)/3（m_τ 锚定候选）
=================================================================
结构：m_tau/M_Pl = e^-(16·dH + ln(16/15)/3)
  16 = 2·k_max（旋量对偶，P7-4c 登记）
  dH = ln15 + δ（谱维，机器证明）
  ln(16/15) = Bott-Moran 桥量（P7-4c：ln15 = ln16 - ln(16/15)）
  /3 = N_gen = N_active（代数）

验证：① 指数偏差 ② 质量偏差 ③ M_Pl 精度敏感性 ④ dH 敏感性
"""
import math
import json

M_TAU_EXP = 1776.86
M_PL_BASE = 1.221e22      # 框架谱定（3 位有效）
LN16_15 = math.log(16/15) # Bott-Moran 桥
DH = 2.7095

def E_cand():
    return 16*DH + LN16_15/3

def main():
    Ec = E_cand()
    print("=" * 78)
    print("P7-5c 验证：E_tau = 16·dH + ln(16/15)/3")
    print("=" * 78)
    print("候选 E = 16×%.6f + %.6f/3 = %.6f" % (DH, LN16_15, Ec))

    for label, MPL in [("M_Pl = 1.221e22（框架基线）", M_PL_BASE),
                       ("M_Pl = 1.2209e22（PDG 标准）", 1.2209e22)]:
        Et = math.log(MPL/M_TAU_EXP)
        d_idx = (Ec/Et-1)*100
        m_tau_cand = MPL*math.exp(-Ec)
        d_mass = (m_tau_cand/M_TAU_EXP-1)*100
        print("  %s" % label)
        print("    E_tau(实验) = %.6f；指数偏差 %+.4f%%" % (Et, d_idx))
        print("    m_tau(候选) = %.3f MeV vs 实验 %.2f MeV；质量偏差 %+.4f%%" % (m_tau_cand, M_TAU_EXP, d_mass))

    # dH 敏感性
    print("\n[dH 敏感性]（M_Pl = 1.221e22）")
    for d in [0.0001, 0.0005, 0.001]:
        dh = DH + d
        e = 16*dh + LN16_15/3
        mt = M_PL_BASE*math.exp(-e)
        print("  dH = %.4f ± %.4f：m_tau = %.3f（偏差 %+.4f%%）" % (DH, d, mt, (mt/M_TAU_EXP-1)*100))

    # 结构分解
    print("\n[结构分解]")
    print("  E = 16·dH + ln(16/15)/3")
    print("    = 16·(ln15+δ) + ln(16/15)/3")
    print("    = 16·ln15 + 16δ + ln(16/15)/3")
    print("    = 16·(ln16 − ln(16/15)) + 16δ + ln(16/15)/3   [Bott-Moran 桥]")
    print("    = 16·ln16 − (47/3)·ln(16/15) + 16δ")
    print("    = ln(2^64) − (47/3)·ln(16/15) + 16δ           [16·ln16 = ln(16^16) = ln(2^64)]")
    print("  => m_tau/M_Pl = 2^(−64)·(16/15)^(47/3)·e^(−16δ)")
    print("  主项 16·dH（旋量对偶 × 谱维）；修正 ln(16/15)/3（桥量 ÷ 代静默 N_gen=3）")

    result = {
        "E_cand": Ec, "E_exp": math.log(M_PL_BASE/M_TAU_EXP),
        "idx_dev": (Ec/math.log(M_PL_BASE/M_TAU_EXP)-1)*100,
        "mass_dev": (M_PL_BASE*math.exp(-Ec)/M_TAU_EXP-1)*100,
        "structure": "m_tau/M_Pl = 2^(-64)·(16/15)^(47/3)·e^(-16δ)",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5c_mtau_anchor_verify.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
