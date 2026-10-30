# -*- coding: utf-8 -*-
"""
Phase 102 P7-5a：α_v = 1.883 与 y_τ = 0.01 框架身份系统搜索
============================================================
目标 1：α_v = 1.883（paper11 L398 Higgs VEV 指数，v = m_t·c_1^{α_v−α_t}）
目标 2：Δ = α_t − α_v = 0.06197（等价搜索目标，ln(v/m_t) = (α_t−α_v)·ln(1/c_1)）
目标 3：ln(100) = 4.6052（y_τ = 0.01 = e^{−ln100} 的指数候选）

搜索：E = a·c1 + b·c2（两参数）+ E = a·c1 + b·c2 + c·c3（三参数）
       a,b ∈ [-3..3]；c ∈ [-2..2]；框架常数表
"""
import math
import json
import itertools

TARGETS = {
    "alpha_v_1.883": 1.883,
    "Delta_alpha_t-alpha_v_0.06197": 0.06197,
    "ln100_4.6052": math.log(100),
}

# 框架常数表（Phase 102 登记 + paper11 相关）
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
    "alpha_u_ln7": math.log(7),
    "alpha_d": math.log(15)/2 - (math.sqrt(6)-math.sqrt(2))/math.sqrt(72),
    "alpha_l": math.log(15)/2,
    "1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "5": 5.0,
}

def dev(est, tgt):
    return (est/tgt-1)*100

def search(target_name, tgt, max_dev=0.1):
    names = list(C.keys())
    hits_2, hits_3 = [], []
    # 两参数
    for a in range(-3, 4):
        for b in range(-3, 4):
            if a == 0 and b == 0:
                continue
            for i, n1 in enumerate(names):
                for n2 in names[i:]:
                    v = a*C[n1] + b*C[n2]
                    d = dev(v, tgt)
                    if abs(d) < max_dev:
                        hits_2.append((d, a, n1, b, n2, v))
    # 三参数（限制系数范围避免爆炸）
    for a in range(-2, 3):
        for b in range(-2, 3):
            for c in range(-2, 3):
                if a == 0 and b == 0 and c == 0:
                    continue
                for i, n1 in enumerate(names):
                    for j, n2 in enumerate(names[i:], start=i):
                        for k, n3 in enumerate(names[j:], start=j):
                            v = a*C[n1] + b*C[n2] + c*C[n3]
                            d = dev(v, tgt)
                            if abs(d) < max_dev*0.5:  # 三参数更严
                                hits_3.append((d, a, n1, b, n2, c, n3, v))
    hits_2.sort(); hits_3.sort()
    print("\n[%s] 目标 = %.4f" % (target_name, tgt))
    print("  两参数命中（|dev|<%.1f%%）：%d 个" % (max_dev, len(hits_2)))
    for h in hits_2[:12]:
        print("    %+0.3f%% : %d·%s %+d·%s = %.4f" % (h[0], h[1], h[2], h[3], h[4], h[5]))
    print("  三参数命中（|dev|<%.1f%%）：%d 个" % (max_dev*0.5, len(hits_3)))
    for h in hits_3[:12]:
        print("    %+0.3f%% : %d·%s %+d·%s %+d·%s = %.4f" % (h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]))
    return hits_2, hits_3

def main():
    print("=" * 78)
    print("P7-5a：α_v = 1.883 与 y_τ = 0.01 框架身份搜索")
    print("=" * 78)
    all_hits = {}
    for name, tgt in TARGETS.items():
        h2, h3 = search(name, tgt)
        all_hits[name] = {"two_param": len(h2), "three_param": len(h3),
                          "best_2": h2[0] if h2 else None, "best_3": h3[0] if h3 else None}

    print("\n" + "=" * 78)
    print("[身份判定]")
    print("  y_τ = 0.01：paper11 全库无出处（轻子扇区仅质量比框架 L394，无绝对质量预言）")
    print("  -> y_τ = 0.01 为实验反推近似（√2·m_τ/v = 0.010217 -> 0.01），m_τ 谱定 = 平凡循环（确认）")
    print("  α_v = 1.883：搜索命中见上——有 <0.1%% 命中则登记候选，无则开放")

    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5a_alpha_v_y_tau.json", "w", encoding="utf-8") as f:
        json.dump({"targets": {k: {"two_param_count": v["two_param"], "three_param_count": v["three_param"],
                                   "best_2": v["best_2"], "best_3": v["best_3"]} for k, v in all_hits.items()},
                   "y_tau_judgment": "y_τ = 0.01 无 paper11 出处 = 实验反推近似（0.010217），m_τ 谱定平凡循环"},
                  f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
