# -*- coding: utf-8 -*-
"""
Phase 102 P7-5b：m_τ 绝对锚定框架搜索
========================================
目标：E_tau = ln(M_Pl/m_tau)（实验）——m_tau/M_Pl = e^(-E_tau)
M_Pl（框架谱定，paper49 §6.1）= 1.221e22 MeV
m_tau = 1776.86 MeV
E_tau = ln(1.221e22/1776.86) ≈ 43.374

搜索：E = a·c1 + b·c2（两参数）+ E = a·c1 + b·c2 + c·c3（三参数）
"""
import math
import json

M_PL = 1.221e22   # 框架谱定（paper49 G_N = 18(2+√3)Δλ_min^2 = 1）
M_TAU = 1776.86

E_TAU = math.log(M_PL/M_TAU)

C = {
    "e": math.e,
    "ln2": math.log(2),
    "ln7": math.log(7),
    "ln15": math.log(15),
    "ln16": math.log(16),
    "dH": 2.7095,
    "dl_min": (math.sqrt(6)-math.sqrt(2))/math.sqrt(72),
    "dl3": (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)*math.sqrt(2),
    "sig": 1.0/15.0,
    "e^-3": math.exp(-3),
    "sqrt2": math.sqrt(2),
    "sqrt8": math.sqrt(8),
    "kappa": 6/math.pi,
    "pi": math.pi,
    "1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "5": 5.0, "6": 6.0, "7": 7.0,
    "8": 8.0, "9": 9.0, "10": 10.0, "12": 12.0, "15": 15.0, "16": 16.0,
    "24": 24.0, "30": 30.0, "40": 40.0, "45": 45.0, "60": 60.0,
}

def dev(est, tgt):
    return (est/tgt-1)*100

def main():
    print("=" * 78)
    print("P7-5b：m_τ 绝对锚定框架搜索（E_tau = ln(M_Pl/m_tau)）")
    print("=" * 78)
    print("M_Pl = %.3e MeV（框架谱定）、m_tau = %.2f MeV" % (M_PL, M_TAU))
    print("E_tau = %.6f；候选直觉：dH×16 = %.4f（指数偏差 %+.3f%%）" % (E_TAU, C["dH"]*16, dev(C["dH"]*16, E_TAU)))

    names = list(C.keys())
    hits_2, hits_3 = [], []
    for a in range(-4, 5):
        for b in range(-4, 5):
            if a == 0 and b == 0:
                continue
            for i, n1 in enumerate(names):
                for n2 in names[i:]:
                    v = a*C[n1] + b*C[n2]
                    d = dev(v, E_TAU)
                    if abs(d) < 0.1:
                        hits_2.append((d, a, n1, b, n2, v))
    for a in range(-3, 4):
        for b in range(-3, 4):
            for c in range(-3, 4):
                if a == 0 and b == 0 and c == 0:
                    continue
                for i, n1 in enumerate(names):
                    for j, n2 in enumerate(names[i:], start=i):
                        for k, n3 in enumerate(names[j:], start=j):
                            v = a*C[n1] + b*C[n2] + c*C[n3]
                            d = dev(v, E_TAU)
                            if abs(d) < 0.05:
                                hits_3.append((d, a, n1, b, n2, c, n3, v))
    hits_2.sort(); hits_3.sort()
    print("\n两参数命中（|dev|<0.1%%）：%d 个" % len(hits_2))
    for h in hits_2[:15]:
        print("  %+0.3f%% : %d·%s %+d·%s = %.4f" % (h[0], h[1], h[2], h[3], h[4], h[5]))
    print("\n三参数命中（|dev|<0.05%%）：%d 个" % len(hits_3))
    for h in hits_3[:15]:
        print("  %+0.3f%% : %d·%s %+d·%s %+d·%s = %.4f" % (h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]))

    # 特殊候选：m_tau/M_Pl 的其他形式
    print("\n[特殊结构候选]")
    cands = {
        "dH*16": C["dH"]*16,
        "e*16": math.e*16,
        "ln16*16": math.log(16)*16,
        "dH*16-1": C["dH"]*16-1,
        "3e*16/3": 3*math.e*16/3,
        "kappa*16+16": 6/math.pi*16+16,
        "ln15*16": math.log(15)*16,
        "dH*15+dH": C["dH"]*16,
    }
    for name, v in cands.items():
        print("  %-12s = %.4f（指数偏差 %+.3f%%）" % (name, v, dev(v, E_TAU)))

    result = {
        "E_tau": E_TAU,
        "M_Pl": M_PL, "m_tau": M_TAU,
        "two_param_hits": len(hits_2), "three_param_hits": len(hits_3),
        "best_2": hits_2[0] if hits_2 else None, "best_3": hits_3[0] if hits_3 else None,
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5b_mtau_anchor.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
