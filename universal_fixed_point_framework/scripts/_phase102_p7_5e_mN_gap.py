# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e：m_N 缺口（SU(6) 缺陷 76.63 MeV）与胶子/π 量关系搜索
====================================================================
目标：gap = m_N(框架 1014.9) − m_N(实验 938.272) = 76.628 MeV
搜索：
  A. gap/Λ（无量纲 0.36490）的框架常数组合
  B. gap 的 MeV 级组合（κΛ、Δ_hf、m_pi、m_ud 等）
  C. 特殊结构候选：κ²Λ/10、3Δλ_min·Λ、π 云关联
"""
import math
import json

GAP = 1014.9 - 938.272   # m_N 缺口
LAMBDA = 210.0           # 框架有效标度
KAPPA = 6/math.pi        # κ = 1.909859（paper40 定理 5.3：κ = (N_c/π)(Δλ3/Δλmin)² = 6/π）
M_PI = 130.0             # 框架预言（定理 5.1 树级 GOR）
M_UD = 3.45              # 流质量
D_HF = 195.8             # paper40 超精细
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
DL3 = DL_MIN*math.sqrt(2)
SIG = 1.0/15.0

def dev(est, tgt):
    return (est/tgt-1)*100

def main():
    print("=" * 78)
    print("P7-5e：m_N 缺口与胶子/π 量关系搜索")
    print("=" * 78)
    print("gap = %.3f MeV、gap/Λ = %.5f" % (GAP, GAP/LAMBDA))
    print("κ = 6/π = %.6f、κΛ = %.1f、m_π = %.1f、Δ_hf = %.1f" % (KAPPA, KAPPA*LAMBDA, M_PI, D_HF))

    print("\n[A] gap/Λ = %.5f 的框架组合：" % (GAP/LAMBDA))
    C = {
        "kappa": KAPPA, "kappa^2": KAPPA**2, "kappa^3": KAPPA**3,
        "dl_min": DL_MIN, "dl3": DL3, "sig": SIG, "e^-3": math.exp(-3),
        "ln16/15": math.log(16/15), "ln2": math.log(2), "ln7": math.log(7),
        "ln15": math.log(15), "ln16": math.log(16), "dH": 2.7095,
        "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3), "sqrt8": math.sqrt(8),
        "pi": math.pi, "pi^2": math.pi**2, "e": math.e, "kappa/10": KAPPA/10,
    }
    names = list(C.keys())
    hits = []
    for a in range(-4, 5):
        for b in range(-4, 5):
            if a == 0 and b == 0:
                continue
            for i, n1 in enumerate(names):
                for n2 in names[i:]:
                    v = a*C[n1] + b*C[n2]
                    d = dev(v, GAP/LAMBDA)
                    if abs(d) < 0.5:
                        hits.append((d, a, n1, b, n2, v))
    hits.sort()
    print("  命中（|dev|<0.5%%）：%d 个" % len(hits))
    for h in hits[:12]:
        print("    %+0.3f%% : %d·%s %+d·%s = %.5f" % (h[0], h[1], h[2], h[3], h[4], h[5]))

    print("\n[B] 特殊结构候选（gap = %.3f MeV）：" % GAP)
    cands = {
        "kappa^2*Lambda/10": KAPPA**2*LAMBDA/10,
        "3*dl_min*Lambda": 3*DL_MIN*LAMBDA,
        "kappa*Lambda*kappa/10": KAPPA*LAMBDA*KAPPA/10,
        "kappa*Lambda*(1-2*sig/3)": KAPPA*LAMBDA*(1-2*SIG/3),
        "m_pi*0.589": M_PI*(GAP/M_PI),
        "d_hf/2.556": D_HF/2.556,
        "kappa*Lambda/5.233": KAPPA*LAMBDA/5.233,
        "m_ud*22.21": M_UD*(GAP/M_UD),
        "Lambda/5.753": LAMBDA/5.753,
        "kappa^2*Lambda/9.76": KAPPA**2*LAMBDA/9.76,
    }
    for name, v in cands.items():
        d = dev(v, GAP)
        print("  %-28s = %.3f（偏差 %+.3f%%）" % (name, v, d))

    print("\n[C] 直接关系检验：")
    print("  gap/Λ = %.5f vs κ²/10 = %.5f（偏差 %+.3f%%）" % (GAP/LAMBDA, KAPPA**2/10, dev(KAPPA**2/10, GAP/LAMBDA)))
    print("  gap/Λ = %.5f vs 3Δλ_min = %.5f（偏差 %+.3f%%）" % (GAP/LAMBDA, 3*DL_MIN, dev(3*DL_MIN, GAP/LAMBDA)))
    print("  gap/m_π = %.4f" % (GAP/M_PI))
    print("  gap/κΛ = %.5f vs κ/10 = %.5f（偏差 %+.3f%%）" % (GAP/(KAPPA*LAMBDA), KAPPA/10, dev(KAPPA/10, GAP/(KAPPA*LAMBDA))))

    result = {"gap": GAP, "gap_over_lambda": GAP/LAMBDA,
              "kappa2_over_10": KAPPA**2/10, "kappa2_over_10_dev": dev(KAPPA**2/10, GAP/LAMBDA),
              "three_dlmin_dev": dev(3*DL_MIN, GAP/LAMBDA)}
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e_mN_gap.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
