# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-88：WKB 过零条件判别——∫√(-2V)dr = π/2
================================================================
P7-5e-87：谐振子近似系统性低估 7-50%（非谐振修正主导）——图景确认、近似不足
WKB 基态量子化（E=0 过零）：∫₀^r_out √(-2V(r)) dr = π/2（r_out = V=0 转折点）
判别：B_wkb(m) vs 量子 B*(m)——命中 → WKB = 闭式机制来源（截距 1/7 获身份）
     不中 → 解析来源仍开放（登记）
"""
import json, os, time
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def V(r, m, B):
    return m*m/(2*r*r) + m*B/2 + B*B*r*r/8 - 1.0/r

def wkb_s(m, B):
    """WKB 作用量 S = ∫√(-2V)dr（V<0 区）——E=0 基态"""
    # 找 V(r)=0 根（V(小) = m²/2r² → +∞ 正；V(大) = B²r²/8 → +∞ 正——中间 V<0）
    # V'=0 唯一极小 r*——V(r*)<0 时 V<0 区间存在：根在 (0, r*) 与 (r*, ∞)
    try:
        rstar = brentq(lambda r: -m*m/(r**3) + B*B*r/4 + 1.0/(r*r), 1e-6, max(abs(m)*abs(m)+5, 20))
    except Exception:
        return None
    if V(rstar, m, B) >= 0:
        return None  # 无 V<0 区（势阱消失）
    try:
        r1 = brentq(lambda r: V(r, m, B), 1e-6, rstar)
        r2 = brentq(lambda r: V(r, m, B), rstar, max(rstar*10, 100))
    except Exception:
        return None
    integrand = lambda r: np.sqrt(max(-2.0*V(r, m, B), 0.0))
    s, _ = quad(integrand, r1, r2, limit=200)
    return s

def bisect_wkb(m, lo, hi, iters=16):
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        s = wkb_s(m, mid)
        if s is None:
            return None
        if s < np.pi/2:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)

print("="*104)
print("P7-5e-88：WKB 过零条件判别——∫√(-2V)dr = π/2")
print("="*104)

quantum = {-11: 0.177487, -10: 0.194733, -9: 0.215692, -8: 0.24168,
           -7: 0.27475, -6: 0.31825, -5: 0.37796, -4: 0.46488,
           -3: 0.60237, -2: 0.84884}
closed = {m: 1.0/(abs(m)/2.0 + 1.0/7.0) for m in quantum}

hits = 0; total = 0
for m in sorted(quantum, reverse=True):
    bw = bisect_wkb(m, 0.05, 2.0)
    if bw is None:
        print("  m=%+d: WKB 无解" % m)
        continue
    q = quantum[m]; total += 1
    diff = (bw - q)/q*100
    hit = abs(diff) < 2.0
    hits += hit
    print("  m=%+d: WKB B_wkb=%.5f vs 量子 B*=%.5f——差 %+.2f%% %s"
          % (m, bw, q, diff, "★命中" if hit else "✗"), flush=True)

print()
print("  命中 %d/%d（<2%%）——%s" % (hits, total,
    "WKB = 闭式机制来源" if hits == total else
    "部分命中" if hits >= total*0.6 else "WKB 亦不足——解析来源开放"))

json.dump({"quantum": {str(k): v for k, v in quantum.items()}},
          open(os.path.join(BASE, "_phase102_p7_5e88_wkb.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
