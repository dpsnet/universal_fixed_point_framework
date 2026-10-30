# -*- coding: utf-8 -*-
"""
Phase 102 P7-4e：三代轻子统一静默公式系统搜索
===============================================
搜索目标：m_e/m_tau、m_mu/m_tau 的统一公式

已知命中（P7-4b/4d）：
  m_e/m_tau = e^(-3e)（指数 8.1543，+0.01%）
  m_mu/m_tau = e^(-(ln16+e^(-3)))（指数 2.8224，-0.00%）

搜索族：
  A. 两参数族 m_i = M·s^k·(旋量倒数)^n（s = e^(-1)、旋量倒数 = 1/16 = e^(-ln16)）
     -> E = k + n·ln16，k 为框架量、n ∈ {0,1,2,3}
  B. 一般组合 E = a·c1 + b·c2（a,b 小整数、c1,c2 框架常数）
"""
import math
import json
import itertools

M_TAU = 1776.86
M_MU = 105.6584
M_E = 0.511

E_E = math.log(M_TAU/M_E)      # m_e/m_tau 指数（实验）
E_MU = math.log(M_TAU/M_MU)    # m_mu/m_tau 指数（实验）

# 框架常数表
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
    "1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "5": 5.0,
}

def dev(est, tgt):
    return (est/tgt-1)*100

def main():
    print("=" * 78)
    print("P7-4e：三代轻子统一静默公式系统搜索")
    print("=" * 78)
    print("[目标指数] E_e = %.4f（m_e/m_tau 实验）、E_mu = %.4f（m_mu/m_tau 实验）" % (E_E, E_MU))
    print("[已知命中] E_e = 3e（偏差 %+.3f%%）；E_mu = ln16+e^(-3)（偏差 %+.3f%%）" % (dev(3*math.e, E_E), dev(math.log(16)+math.exp(-3), E_MU)))

    print("\n[A] 两参数族 m_i = M·s^k·(1/16)^n（s=e^(-1)）")
    print("    E = k + n·ln16；n ∈ {0,1,2,3}；k 为框架量")
    for label, tgt in [("m_e", E_E), ("m_mu", E_MU)]:
        print("    --- %s（E = %.4f）---" % (label, tgt))
        for n in [0, 1, 2, 3]:
            k_need = tgt - n*math.log(16)
            # 找 k_need 的框架量命中（单常数）
            best = None
            for name, v in C.items():
                d = dev(v, k_need)
                if abs(d) < 1.5 and (best is None or abs(d) < abs(best[0])):
                    best = (d, name, v)
            if best:
                print("      n=%d：k_need = %.4f -> %s = %.4f（偏差 %+.3f%%）" % (n, k_need, best[1], best[2], best[0]))
            else:
                print("      n=%d：k_need = %.4f（无 <1.5%% 单框架量命中）" % (n, k_need))

    print("\n[B] 一般组合 E = a·c1 + b·c2（a,b ∈ [-3..3]，c1,c2 框架常数）")
    print("    只列 |偏差|<0.1%% 的双参数命中：")
    names = list(C.keys())
    hits_e, hits_mu = [], []
    for a in range(-3, 4):
        for b in range(-3, 4):
            for i, n1 in enumerate(names):
                for n2 in names[i:]:
                    v = a*C[n1] + b*C[n2]
                    d_e = dev(v, E_E)
                    d_mu = dev(v, E_MU)
                    if abs(d_e) < 0.1:
                        hits_e.append((d_e, a, n1, b, n2, v))
                    if abs(d_mu) < 0.1:
                        hits_mu.append((d_mu, a, n1, b, n2, v))
    hits_e.sort(); hits_mu.sort()
    print("    E_e 命中（%d 个）：" % len(hits_e))
    for h in hits_e[:10]:
        print("      %+0.3f%% : %d·%s %+d·%s = %.4f" % (h[0], h[1], h[2], h[3], h[4], h[5]))
    print("    E_mu 命中（%d 个）：" % len(hits_mu))
    for h in hits_mu[:10]:
        print("      %+0.3f%% : %d·%s %+d·%s = %.4f" % (h[0], h[1], h[2], h[3], h[4], h[5]))

    print("\n[C] 统一公式候选（同族两代同时命中）")
    # 找同时含 3e（或近似）与 ln16+e^-3 的结构：检验 m_i = M·s^{k_i}·16^{-n_i} 的参数序列
    print("    两参数族解集（n_i, k_i）：")
    print("      m_e：n=0、k=3e = %.4f（偏差 %+.3f%%）——精确命中" % (3*math.e, dev(3*math.e, E_E)))
    print("      m_mu：n=1、k=e^(-3) = %.4f（偏差 %+.3f%%）——精确命中" % (math.exp(-3), dev(math.log(16)+math.exp(-3), E_MU)))
    print("      m_tau：n=0、k=0（基准）")
    print("    参数序列：(n,k) = (0,3e)、(1,e^(-3))、(0,0)——n 无单调、k 无递推——登记开放")
    # 附加检验：k_e/k_mu 与 n 序列
    ratio_k = 3*math.e/math.exp(-3)
    print("    k_e/k_mu = %.1f（非整数）；n 序列 0->1->0 无单调——无递推规律" % ratio_k)

    result = {
        "E_e": E_E, "E_mu": E_MU,
        "known": {"3e": 3*math.e, "3e_dev": dev(3*math.e, E_E),
                  "ln16_plus_e-3": math.log(16)+math.exp(-3), "dev": dev(math.log(16)+math.exp(-3), E_MU)},
        "family_A": {
            "m_e": {"n": 0, "k": 3*math.e, "dev": dev(3*math.e, E_E)},
            "m_mu": {"n": 1, "k": math.exp(-3), "dev": dev(math.log(16)+math.exp(-3), E_MU)},
            "m_tau": {"n": 0, "k": 0},
        },
        "conclusion": "两参数族成立（m_i = M·s^k·16^(-n)，双命中 <0.01%）；参数序列无递推规律开放",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_4e_unified_silence.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
