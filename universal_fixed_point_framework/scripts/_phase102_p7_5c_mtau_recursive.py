# -*- coding: utf-8 -*-
"""
Phase 102 P7-5c：基于 dH 的递归展开族搜索（m_τ 锚定）
========================================================
目标：E_tau = ln(M_Pl/m_tau) = 43.3739（M_Pl = 1.221e22 框架谱定、m_tau = 1776.86）

递归展开族：
  A. 幂次展开：E = a·dH^k（a ∈ 1..24、k ∈ 1..4）
  B. ln15 塔：E = n·ln15（n ∈ 1..24）——15 = 2^k_max−1 对偶分支
  C. 2 幂系数：E = 2^a·dH（a ∈ 0..5）——16 = 2^4 = 2k_max 旋量对偶
  D. dH 幂组合：E = a·dH + b·dH^2
  E. 对偶塔递归：m_tau/M_Pl ≈ 15^{−n}（n 整数扫描）
"""
import math
import json

M_PL = 1.221e22
M_TAU = 1776.86
E_TAU = math.log(M_PL/M_TAU)
RATIO = M_PL/M_TAU

LN15 = math.log(15)
DH = 2.7095
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
SIG = 1.0/15.0

def dev(est, tgt):
    return (est/tgt-1)*100

def mass_dev(e_est):
    return (math.exp(e_est)/RATIO-1)*100

def main():
    print("=" * 78)
    print("P7-5c：基于 dH 的递归展开族搜索")
    print("=" * 78)
    print("E_tau = %.6f（目标）、M_Pl/m_tau = %.4e" % (E_TAU, RATIO))
    print("dH = %.4f（= ln15 + δ，δ = %.6f）、ln15 = %.6f" % (DH, DH-LN15, LN15))

    print("\n[A] 幂次展开 E = a·dH^k：")
    best_a = []
    for k in range(1, 5):
        for a in range(1, 25):
            v = a*(DH**k)
            d = dev(v, E_TAU)
            if abs(d) < 2.0:
                best_a.append((d, k, a, v))
    best_a.sort()
    for d, k, a, v in best_a[:8]:
        print("  %+0.3f%%（指数）: %d·dH^%d = %.4f；质量偏差 %+.2f%%" % (d, a, k, v, mass_dev(v)))

    print("\n[B] ln15 塔 E = n·ln15：")
    for n in range(1, 25):
        v = n*LN15
        d = dev(v, E_TAU)
        if abs(d) < 2.0:
            print("  %+0.3f%%（指数）: %d·ln15 = %.4f（= ln(15^%d)）；质量偏差 %+.2f%%" % (d, n, v, n, mass_dev(v)))

    print("\n[C] 2 幂系数 E = 2^a·dH：")
    for a in range(0, 6):
        v = (2**a)*DH
        d = dev(v, E_TAU)
        print("  2^%d·dH = %.4f（指数偏差 %+.3f%%；质量偏差 %+.2f%%）" % (a, v, d, mass_dev(v)))

    print("\n[D] dH 幂组合 E = a·dH + b·dH^2：")
    for a in range(-4, 5):
        for b in range(-3, 4):
            v = a*DH + b*(DH**2)
            d = dev(v, E_TAU)
            if abs(d) < 1.0:
                print("  %+0.3f%%（指数）: %d·dH %+d·dH^2 = %.4f" % (d, a, b, v))

    print("\n[E] 对偶塔递归 m_tau/M_Pl ≈ 15^(-n)：")
    for n in range(10, 21):
        v = 15**n
        d = (RATIO/v-1)*100
        print("  15^%d = %.4e（比值偏差 %+.2f%%）" % (n, v, d))

    print("\n[F] 递归候选：E = 16·dH 的修正项")
    delta = E_TAU - 16*DH
    print("  E_tau - 16·dH = %.6f" % delta)
    cands = {"delta/2": delta/2, "e^-3*0.44": math.exp(-3)*0.44, "DL_MIN/5.57": DL_MIN/5.57,
             "SIG*0.33": SIG*0.33, "delta*15": delta*15, "ln(16/15)": math.log(16/15),
             "ln(16/15)*0.34": math.log(16/15)*0.34}
    for name, v in cands.items():
        print("  %-18s = %.6f" % (name, v))
    print("  注：ln(16/15) = %.6f（Bott-Moran 桥量）" % math.log(16/15))

    result = {"E_tau": E_TAU, "ratio": RATIO,
              "best_A": best_a[0] if best_a else None,
              "sixteen_dH_dev": dev(16*DH, E_TAU), "sixteen_dH_mass_dev": mass_dev(16*DH),
              "fifteen_power_16_dev": (RATIO/(15**16)-1)*100,
              "E_minus_16dH": delta}
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5c_mtau_recursive.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
