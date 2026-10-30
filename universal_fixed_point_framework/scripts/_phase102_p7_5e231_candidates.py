# -*- coding: utf-8 -*-
"""
P7-5e-231：ε/D/E 解析候选搜索（230c 打靶全链口径）
====================================================================
目标值（230c 打靶全链）：
  ε：+0.215e-6（33..129 单参，RMS 8.4e-8）~ +2.0e-6（512..1024）窗口漂移真实；
      低 m 段 +0.2~0.4e-6 最可信（模型近乎完美）。
  D：−0.019848（33..129 三参）→ |D|≈0.01985（vs 41/2000=0.0205 偏 −3.2%）
  E：+0.012134（33..129 两参，−37.8% vs 39/2000）~ +0.009158（33..256）
候选池：框架常数 {2,7,8,13,41,56,65,128,252,256,512} 组合、p/q 小整数、1/(k·2^n)。
先验：P1 命中 <0.5% → 候选登记升格；P2 仅候选级 → 维持登记；P3 无干净命中 → 确认 ε/D/E 需先解高 m 段残留结构。
"""
import json, os
import numpy as np
from fractions import Fraction

TARGET_EPS = 0.215e-6      # 低 m 段（最可信）
TARGET_EPS_RANGE = (0.1e-6, 3.0e-6)
TARGET_D = 0.019848        # |D| 33..129 三参
TARGET_D_RANGE = (0.0195, 0.0206)
TARGET_E = 0.012134        # E 33..129 两参
TARGET_E_RANGE = (0.008, 0.014)

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def scan(name, target, rng, forms, max_q=2000, max_n=24):
    best = []
    for form in forms:
        if form == "pq":
            for q in range(1, max_q+1):
                for p in range(1, q*5):
                    v = p/float(q)
                    if rng[0] <= v <= rng[1]:
                        dev = (v-target)/target*100
                        if abs(dev) < 3.0:
                            best.append((abs(dev), v, "%d/%d" % (p, q), dev))
        elif form == "k2n":
            for k in [1, 2, 3, 5, 7, 8, 13, 17, 41, 56, 65]:
                for n in range(1, max_n+1):
                    v = k/(2.0**n)
                    if rng[0] <= v <= rng[1]:
                        dev = (v-target)/target*100
                        if abs(dev) < 3.0:
                            best.append((abs(dev), v, "%d/2^%d" % (k, n), dev))
        elif form == "1k2n":
            for k in [1, 2, 3, 5, 7, 8, 13, 17, 41, 56, 65, 128, 252]:
                for n in range(0, max_n+1):
                    v = 1.0/(k*2.0**n)
                    if rng[0] <= v <= rng[1]:
                        dev = (v-target)/target*100
                        if abs(dev) < 3.0:
                            best.append((abs(dev), v, "1/(%d·2^%d)" % (k, n), dev))
    best.sort(key=lambda x: x[0])
    print("== %s（目标 %.6g，范围 %.4g~%.4g）==" % (name, target, rng[0], rng[1]), flush=True)
    for d, v, lab, dev in best[:8]:
        print("  %-16s = %.8g  dev %+.3f pct" % (lab, v, dev), flush=True)
    return best

if __name__ == "__main__":
    print("== P7-5e-231：ε/D/E 解析候选搜索（打靶全链口径）==", flush=True)
    scan("ε（低 m 段）", TARGET_EPS, TARGET_EPS_RANGE, ["pq", "k2n", "1k2n"])
    print("", flush=True)
    scan("D（|D| 33..129）", TARGET_D, TARGET_D_RANGE, ["pq", "1k2n"], max_q=4000)
    print("", flush=True)
    scan("E（33..129 两参）", TARGET_E, TARGET_E_RANGE, ["pq", "1k2n"], max_q=4000)

    # ε 全窗登记（不搜索，仅记录）
    print("", flush=True)
    print("== ε 窗口登记（打靶，230c）==", flush=True)
    for lab, v in [("33..129", 0.215e-6), ("33..1024", 0.961e-6), ("128..1024", 1.430e-6), ("512..1024", 1.998e-6)]:
        print("  [%s] ε=%+.3e" % (lab, v), flush=True)

    json.dump({"note": "eps/D/E analytic candidate search (shoot full-chain 230c)", 
               "targets": {"eps_lowm": TARGET_EPS, "D": TARGET_D, "E": TARGET_E}},
              open(os.path.join(BASE, "_phase102_p7_5e231_candidates.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
