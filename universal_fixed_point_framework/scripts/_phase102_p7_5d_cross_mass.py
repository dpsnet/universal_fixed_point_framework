# -*- coding: utf-8 -*-
"""
Phase 102 P7-5d：递归结构跨质量检验（m_τ/m_N/m_e 锚定一致性）
================================================================
递归候选（P7-5c 命中）：E_τ = 16·dH + ln(16/15)/3（质量偏差 +0.043% 达标）
检验：同一递归结构（旋量塔×桥修正）是否适用于 m_N、m_e 的锚定

目标指数：
  E_x = ln(M_Pl/m_x)（M_Pl = 1.221e22 框架谱定）
  E_tau = ln(1.221e22/1776.86) = 43.37394
  E_N   = ln(1.221e22/938.272) = ?
  E_e   = ln(1.221e22/0.511)   = ?

检验：
  A. 直接适配：E_x = a·dH + b·ln(16/15)/3（a ∈ 1..20、b ∈ -10..10）
  B. 一般组合：E_x = a·c1 + b·c2（c1,c2 框架常数）
  C. 特殊结构：16·ln16−ln√2、16·ln15+ln2、E_τ+3e（m_e 继承）等
  D. 体系判定：递归结构跨质量普遍性
"""
import math
import json

M_PL = 1.221e22
M_TAU = 1776.86
M_N = 938.272
M_E = 0.511

E_TAU = math.log(M_PL/M_TAU)
E_N = math.log(M_PL/M_N)
E_E = math.log(M_PL/M_E)

LN16_15 = math.log(16/15)
DH = 2.7095
LN15 = math.log(15)
LN16 = math.log(16)
LN2 = math.log(2)
LN_SQRT2 = 0.5*math.log(2)

def mass_dev(e_est, e_exp):
    """候选质量 vs 实验质量的偏差（%）"""
    return (math.exp(e_est)/math.exp(e_exp)-1)*100

def idx_dev(e_est, e_exp):
    return (e_est/e_exp-1)*100

def main():
    print("=" * 78)
    print("P7-5d：递归结构跨质量检验（m_τ/m_N/m_e 锚定）")
    print("=" * 78)
    print("E_tau = %.6f、E_N = %.6f、E_e = %.6f" % (E_TAU, E_N, E_E))
    print("递归候选 E_tau = 16·dH + ln(16/15)/3 = %.6f（质量 %+.4f%%）" % (16*DH+LN16_15/3, mass_dev(16*DH+LN16_15/3, E_TAU)))

    print("\n[A] 直接适配 E_x = a·dH + b·ln(16/15)/3（质量偏差 <2%% 列出）：")
    for label, Et in [("m_N", E_N), ("m_e", E_E)]:
        print("  --- %s（E = %.4f）---" % (label, Et))
        hits = []
        for a in range(1, 21):
            for b in range(-10, 11):
                v = a*DH + b*LN16_15/3
                d = mass_dev(v, Et)
                if abs(d) < 2.0:
                    hits.append((abs(d), d, a, b, v))
        hits.sort()
        for h in hits[:6]:
            print("    质量 %+0.3f%% : %d·dH %+d·(ln(16/15)/3) = %.4f" % (h[1], h[2], h[3], h[4]))

    print("\n[B] 特殊结构候选（质量偏差）：")
    specials = {
        "m_N 16·ln16−ln√2": 16*LN16 - LN_SQRT2,
        "m_N 16·ln15+ln2": 16*LN15 + LN2,
        "m_N 16·dH+ln2": 16*DH + LN2,
        "m_N 17·dH": 17*DH,
        "m_e 继承 E_tau+3e": 16*DH + LN16_15/3 + 3*math.e,
        "m_e 19·dH": 19*DH,
    }
    for name, v in specials.items():
        if "m_N" in name:
            Et = E_N
        else:
            Et = E_E
        print("  %-22s = %.6f：质量 %+.4f%%（指数 %+.4f%%）" % (name, v, mass_dev(v, Et), idx_dev(v, Et)))

    print("\n[C] 体系判定：")
    # m_tau
    d_tau = mass_dev(16*DH+LN16_15/3, E_TAU)
    # m_e 继承
    d_e = mass_dev(16*DH+LN16_15/3+3*math.e, E_E)
    # m_N 直接适配最优
    print("  m_tau（递归候选 16·dH+桥/3）：质量 %+.4f%%" % d_tau)
    print("  m_e（继承 E_tau+3e = 旋量塔+桥/3+3e）：质量 %+.4f%%" % d_e)
    print("  m_N（直接适配）：最优候选 16·ln16−ln√2 质量 %+.4f%%、16·ln15+ln2 质量 %+.4f%%——均超 0.1%% 标准" % (
        mass_dev(16*LN16-LN_SQRT2, E_N), mass_dev(16*LN15+LN2, E_N)))
    print("  → 轻子扇区（τ 锚定 + e 继承）递归结构闭合（<0.1%）；强子扇区 m_N 走独立链（P7-2 Λ→Δ_dress→m_N，+8.1% SU(6) 缺陷）——旋量塔族适用于轻子锚定，强子为另一族")
    print("  → 体系判定：部分闭合——轻子绝对锚定闭合（τ/e），强子端独立链 + 缺口登记")

    result = {
        "E_tau": E_TAU, "E_N": E_N, "E_e": E_E,
        "tau_cand": {"E": 16*DH+LN16_15/3, "mass_dev": d_tau},
        "e_inherit": {"E": 16*DH+LN16_15/3+3*math.e, "mass_dev": d_e},
        "N_direct_best": {"16ln16-ln2_2": mass_dev(16*LN16-LN_SQRT2, E_N),
                          "16ln15+ln2": mass_dev(16*LN15+LN2, E_N)},
        "judgment": "轻子扇区闭合（τ +0.043%、e 继承 +0.04%）；m_N 直接适配不达标（强子独立链 P7-2）——部分闭合",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5d_cross_mass.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
