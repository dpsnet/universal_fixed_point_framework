# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-87：闭式解析来源判别——谐振子近似（V_min + ω/2 = 0）
================================================================
P7-5e-85/86 闭式实锤：1/B* = |m|/2 + 1/7（高 |m| 7/7 <0.16% + 3 次先验命中）
物理图景（P7-5e-78 已证 V_min 恒负）：负 m 过零 = 零点能主导
推导检验：2D 氢径向有效势 V(r) = m²/(2r²) + mB/2 + B²r²/8 − 1/r（质量 1）
  过零条件（谐振子近似）：V_min + ω/2 = 0，ω = √(V''(r*))——基态零点能
判别：(a) B_harm ≈ B* 量子全 m 命中 → 谐振子近似 = 闭式机制来源（内生推导）
      (b) 高 |m| 命中、低 |m| 偏离 → 修正 = 非谐振修正（修正项来源可攻）
      (c) 全不命中 → 零点能图景有误
"""
import json, os, time
import numpy as np
from scipy.optimize import brentq
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def V(r, m, B):
    return m*m/(2*r*r) + m*B/2 + B*B*r*r/8 - 1.0/r

def Vprime(r, m, B):
    return -m*m/(r**3) + B*B*r/4 + 1.0/(r*r)

def Vdprime(r, m, B):
    return 3*m*m/(r**4) + B*B/4 + 2.0/(r**3)

def e_harm(m, B):
    """谐振子近似基态能量：V_min + ω/2——V'(r)=0 唯一根（f(r)=B²r⁴/4+r=m² 单调增）"""
    try:
        rstar = brentq(lambda r: Vprime(r, m, B), 0.01, max(abs(m)*abs(m) + 5.0, 20.0))
    except Exception:
        return None, None
    vmin = V(rstar, m, B)
    w = np.sqrt(max(Vdprime(rstar, m, B), 1e-12))
    return vmin + w/2, (rstar, vmin, w)

def bisect_harm(m, lo, hi, iters=16):
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        e, _ = e_harm(m, mid)
        if e is None:
            return None
        if e > 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)

print("="*104)
print("P7-5e-87：闭式解析来源判别——谐振子近似（V_min + ω/2 = 0）")
print("="*104)

quantum = {-11: 0.177487, -10: 0.194733, -9: 0.215692, -8: 0.24168,
           -7: 0.27475, -6: 0.31825, -5: 0.37796, -4: 0.46488,
           -3: 0.60237, -2: 0.84884}

hits = 0
total = 0
for m in sorted(quantum, reverse=True):
    bh = bisect_harm(m, 0.05, 2.0)
    if bh is None:
        print("  m=%+d: 谐振子近似无解" % m)
        continue
    q = quantum[m]
    total += 1
    diff = (bh - q)/q*100
    hit = abs(diff) < 2.0
    hits += hit
    print("  m=%+d: 谐振子 B_harm=%.5f vs 量子 B*=%.5f——差 %+.2f%% %s"
          % (m, bh, q, diff, "★命中" if hit else "✗"), flush=True)

print()
print("  命中 %d/%d（<2%% 容差）——%s" % (hits, total,
    "谐振子近似 = 闭式机制来源" if hits == total else
    "高 |m| 命中/低 |m| 偏离——非谐振修正" if hits >= total*0.6 else "零点能图景有误"))

# 高 |m| 单独统计
print()
print("【高 |m|（≥5）单独统计】")
high_hits = 0; high_total = 0
for m in [-11, -10, -9, -8, -7, -6, -5]:
    bh = bisect_harm(m, 0.05, 2.0)
    q = quantum[m]
    diff = abs((bh-q)/q*100)
    high_total += 1
    high_hits += diff < 1.0
    print("  m=%+d: 差 %.3f%%" % (m, diff))
print("  高 |m| 命中 %d/%d（<1%%）" % (high_hits, high_total))

json.dump({"quantum": {str(k): v for k, v in quantum.items()},
           "harmonic": {str(m): bisect_harm(m, 0.05, 2.0) for m in quantum}},
          open(os.path.join(BASE, "_phase102_p7_5e87_harmonic.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
