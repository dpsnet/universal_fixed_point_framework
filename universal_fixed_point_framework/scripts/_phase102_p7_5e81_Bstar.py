# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-81：过零场强二分细化——框架量身份锁定
================================================================
m=+1 过零 ∈ [0.23, 0.24]、m=-8 过零 ∈ [0.24, 0.25]（P7-5e-80）
二分 12 次 → B* 精度 ~2.4e-5 au——对照框架量分数：
  49/200=0.245（静默单元 49 场强域复现）、47/200=0.235、6/25=0.24（2N_gen/25）、
  12/50=0.24、B_0/100=0.01 间距（配置基数²）
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

def bisect(m, lo, hi, n=12):
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        e = e0_m(1500, 60.0, m, mid)
        if e is None:
            return None
        if e > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

print("="*104)
print("P7-5e-81：过零场强二分细化——框架量身份锁定")
print("="*104)

t0 = time.time()
B1 = bisect(1, 0.23, 0.24, 12)
B8 = bisect(-8, 0.24, 0.25, 12)
print("  m=+1 过零 B* = %.5f au（%.1f MG）" % (B1, B1*2350))
print("  m=-8 过零 B* = %.5f au（%.1f MG）" % (B8, B8*2350))
print("  间距 Δ = %.5f au（%.1f MG）——B_0/100 = 0.0100（配置基数²）对照" % (abs(B8-B1), abs(B8-B1)*2350))
print("  用时 %.0fs" % (time.time()-t0))

print()
print("【框架量身份对照】")
print("-"*104)
cands = {
    "49/200 静默单元": 49/200, "47/200": 47/200, "6/25=2N_gen/25": 6/25,
    "9/40=N_gen²/(5·4)": 9/40, "10/40=配置基数/20": 10/40,
    "B0/2=1/2": 0.5, "B0/4=1/4": 0.25, "3/10=N_gen/10": 0.3,
}
for name, v in cands.items():
    d1 = abs(B1 - v)
    d8 = abs(B8 - v)
    mark1 = "★★" if d1 < 5e-4 else ""
    mark8 = "★★" if d8 < 5e-4 else ""
    print("  %s = %.5f——m=+1 差 %.5f %s | m=-8 差 %.5f %s" % (name, v, d1, mark1, d8, mark8))

json.dump({"m+1": B1, "m-8": B8, "spacing": abs(B8-B1)},
          open(os.path.join(BASE, "_phase102_p7_5e81_Bstar.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
