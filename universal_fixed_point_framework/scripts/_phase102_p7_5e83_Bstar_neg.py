# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-83：负 m 量子过零场强序列扫描——"台阶 = 过零投影"判别
================================================================
先验预测（台阶投影假说）：B*(m) = 台阶场强
  m=-7 → 0.25（10/40）、m=-6 → 0.30（12/40）、m=-5 → 0.35（14/40）、
  m=-4 → 0.40（16/40）、m=-3 → 0.50（20/40）、m=-2 → 0.70（28/40）、m=-1 → 0.90（36/40）
m=-8 已知例外（0.24168 ≠ 0.25——但最接近 0.24=2N_gen/25）
判别：(a) 全命中 → 台阶 = 量子过零投影（强闭合）
      (b) 部分命中 → 修正；(c) 全不命中 → 台阶另有来源
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

print("="*104)
print("P7-5e-83：负 m 量子过零场强序列——'台阶 = 过零投影'判别")
print("="*104)

ms = [-7, -6, -5, -4, -3, -2, -1]
Bstar = {}
for m in ms:
    # 粗扫找过零区间（从 0.24 起步进 0.03——上限 1.2 覆盖 m=-1）
    lo, hi = None, None
    prev_B, prev_E = 0.24, e0_m(1500, 60.0, m, 0.24)
    for B in np.arange(0.27, 1.23, 0.03):
        E = e0_m(1500, 60.0, m, B)
        if E is None:
            break
        if prev_E is not None and prev_E * E <= 0:
            lo, hi = prev_B, B
            break
        prev_B, prev_E = B, E
    if lo is None:
        # 未找到——检查末点
        print("  m=%+d: 0.24-1.2 au 内未过零（E_0 仍 %+.4f）" % (m, prev_E), flush=True)
        Bstar[m] = None
        continue
    # 二分细化 12 次
    for _ in range(12):
        mid = 0.5 * (lo + hi)
        E = e0_m(1500, 60.0, m, mid)
        if E is not None and E > 0:
            hi = mid
        else:
            lo = mid
    Bstar[m] = 0.5 * (lo + hi)
    print("  m=%+d: B* = %.5f au（%.1f MG）" % (m, Bstar[m], Bstar[m]*2350), flush=True)

print()
print("【台阶投影判别】")
print("-"*104)
steps = {-7: 0.25, -6: 0.30, -5: 0.35, -4: 0.40, -3: 0.50, -2: 0.70, -1: 0.90}
hits = 0
for m in ms:
    bs = Bstar.get(m)
    if bs is None:
        print("  m=%+d: 无过零——台阶 %.2f 不适用" % (m, steps[m]))
        continue
    diff = abs(bs - steps[m])
    hit = diff < 0.015
    hits += hit
    print("  m=%+d: B*=%.5f vs 台阶 %.2f——差 %.4f %s" % (m, bs, steps[m], diff, "★★命中" if hit else "✗")
)
print()
print("  命中 %d/7——%s" % (hits, "台阶 = 过零投影（强闭合）" if hits == 7 else "部分命中——需修正" if hits >= 3 else "不成立——台阶另有来源"))

json.dump({str(m): (bs if bs is not None else None) for m, bs in Bstar.items()},
          open(os.path.join(BASE, "_phase102_p7_5e83_Bstar_neg.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
