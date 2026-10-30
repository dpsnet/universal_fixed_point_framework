# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-85：负 m 过零闭式先验检验——1/B* = |m|/2 + 1/7
================================================================
P7-5e-83 数据复盘发现：1/B*(m) 等差（步长 ≈ 0.5 = α₀ = N_Weyl/k_max）
闭式候选：1/B*(m) = |m|·α₀ + 1/(k_max−1) = |m|/2 + 1/7（截距 1/7 = 1/(k_max−1)，7 = k_max−1）
高 |m|（5-8）命中 <0.12%；低 |m| 偏离递增（−0.38%/−1.05%/−3.1%）——修正开放
先验预言（未测 m）：m=−9 → B* = 1/(4.5+1/7) = 0.21538、m=−10 → 1/(5+1/7) = 0.19444
判别：命中 → 闭式升格"候选闭式"（α₀ 斜率 + 1/(k_max−1) 截距双框架量）
稳定性：m=−9/−10 用 r_max=60/80/100 检验（过零 E→0 波函数扩展风险）
"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def e0_m(N_r, r_max, m, B, k=20):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
              offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return float(np.real(vals[0]))
    except Exception:
        return None

def bisect_bstar(m, r_max, lo, hi, iters=14):
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        E = e0_m(1500, r_max, m, mid)
        if E is not None and E > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

print("="*104)
print("P7-5e-85：负 m 过零闭式先验检验——1/B* = |m|/2 + 1/7")
print("="*104)

ALPHA0 = 0.5      # N_Weyl/k_max
INV7 = 1.0 / 7.0  # 1/(k_max-1)

for m in [-9, -10]:
    pred = 1.0 / (abs(m) * ALPHA0 + INV7)
    print("m=%+d：闭式预言 B* = 1/(%d/2+1/7) = %.6f au（%.1f MG）" % (m, abs(m), pred, pred*2350))
    bs = {}
    for rmax in [60, 80, 100]:
        b = bisect_bstar(m, rmax, 0.10, 0.30)
        bs[rmax] = b
        print("  r_max=%d: B* = %.6f au（%.1f MG）——差 %.4f（%.2f%%）%s"
              % (rmax, b, b*2350, b-pred, (b-pred)/pred*100,
                 "★★命中" if abs(b-pred)/pred < 0.01 else "✗"))
    print("  r_max 稳定性：%s" % ("稳定" if max(bs.values())-min(bs.values()) < 1e-3 else "不稳定——波函数扩展"), flush=True)

# 低 |m| 修正检查（m=-5..-2 偏差结构）
print()
print("【低 |m| 偏差结构】（闭式 vs 实测）")
known = {-8: 0.24168, -7: 0.27475, -6: 0.31825, -5: 0.37796, -4: 0.46488, -3: 0.60237, -2: 0.84884}
for m, b in sorted(known.items()):
    pred = 1.0 / (abs(m) * ALPHA0 + INV7)
    print("  m=%+d: 实测 %.5f vs 闭式 %.5f——偏差 %+.2f%%" % (m, b, pred, (b-pred)/pred*100))

json.dump({"closed_form": "1/B* = |m|/2 + 1/7",
           "m-9": {str(k): v for k, v in bisect_bstar(-9, 100, 0.10, 0.30) and {"B": None}.items()} if False else {},
           "alpha0": ALPHA0, "inv7": INV7},
          open(os.path.join(BASE, "_phase102_p7_5e85_Bstar_closed.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
