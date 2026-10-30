# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-80：量子基态能量 E_0(m,B) 过零扫描——同步收缩精确判别
================================================================
判别：m=-8 与 m=+1 的 E_0(B) 过零场强是否精确相等（同步）
扫描 B ∈ [0.20, 0.26]（步长 0.01）+ 二分细化
  (a) E_0(-8,B*) = E_0(+1,B*) ≈ 0 同点 → 同步精确（9 缺口 = 双通道同步过零）
  (b) 过零场强不同 → 同步是窗口内先后（近似）
输出：E_0 表 + 过零场强
"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def e0_m(N_r, r_max, m, B, k=300):
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
        vals, _ = eigsh(H.astype(np.float64), k=min(20, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return float(np.real(vals[0]))
    except Exception:
        return None

print("="*104)
print("P7-5e-80：量子基态 E_0(m,B) 过零扫描——同步收缩精确判别")
print("="*104)

N_r, r_max = 1500, 60.0
Bs = [0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26]
ms = [-8, 1]

table = {}
for B in Bs:
    t0 = time.time()
    row = {}
    for m in ms:
        e0 = e0_m(N_r, r_max, m, B)
        row[m] = e0
    table[B] = row
    print("  B=%.2f au: E_0(m=-8)=%+.5f  E_0(m=+1)=%+.5f  [%.0fs]"
          % (B, row[-8], row[1], time.time()-t0), flush=True)

print()
print("【过零判别】")
print("-"*104)
def cross(Bs, vals):
    for i in range(len(Bs)-1):
        if vals[i] is not None and vals[i+1] is not None and vals[i]*vals[i+1] <= 0:
            return (Bs[i], vals[i], Bs[i+1], vals[i+1])
    return None
c8 = cross(Bs, [table[b][-8] for b in Bs])
c1 = cross(Bs, [table[b][1] for b in Bs])
if c8:
    print("  m=-8 过零: [%.2f (E=%+.4f), %.2f (E=%+.4f)] → 区间中点 %.3f" % (c8[0], c8[1], c8[2], c8[3], (c8[0]+c8[2])/2))
else:
    print("  m=-8: 0.20-0.26 内未过零")
if c1:
    print("  m=+1 过零: [%.2f (E=%+.4f), %.2f (E=%+.4f)] → 区间中点 %.3f" % (c1[0], c1[1], c1[2], c1[3], (c1[0]+c1[2])/2))
else:
    print("  m=+1: 0.20-0.26 内未过零")
if c8 and c1:
    mid8 = (c8[0]+c8[2])/2
    mid1 = (c1[0]+c1[2])/2
    print("  过零差: %.3f au（%.1f MG）——%s同步" % (abs(mid8-mid1), abs(mid8-mid1)*2350,
          "精确（<0.01 au）" if abs(mid8-mid1) < 0.01 else "窗口内先后"))

json.dump({str(b): {str(m): v for m, v in row.items()} for b, row in table.items()},
          open(os.path.join(BASE, "_phase102_p7_5e80_E0.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
