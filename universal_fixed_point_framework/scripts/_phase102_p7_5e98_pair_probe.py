# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-98：配对族检验——+2 过零场强 vs −7 闭式预言
================================================================
P7-5e-89 已确认 +1 ↔ −8 配对（1+8 = 9 = N_gen²，过零场强重合 0.237）
若配对族 {(+1,−8),(+2,−7),(+3,−6),(+4,−5)} 普遍成立——"±m 和 = N_gen²"是 B* 深层机制
−7 闭式预言：1/B*(−7) = 7/2 + 1/7 + 1/(7·2^7) = 3.643973 → B* = 0.274428
检验：+2 的数值过零 B* 是否 ≈ 0.2744（若重合——配对族确认）
"""
import json, os
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

def bisect_Bstar(m, N_r, r_max, lo, hi, iters=18):
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        e = e0_m(N_r, r_max, m, mid)
        if e > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

print("="*104)
print("P7-5e-98：配对族检验——+2 vs −7（+n ↔ −(9−n) 配对假说）")
print("="*104)

# 配对族闭式预言（统一闭式 1/B* = |m|/2 + 1/7 + 1/(7·2^|m|)）
pair_m = {2: -7, 3: -6, 4: -5, 1: -8}
print("\n★ 配对族预言（统一闭式）：")
for mplus, mneg in sorted(pair_m.items()):
    inv_neg = abs(mneg)/2.0 + 1.0/7.0 + 1.0/(7.0*2**abs(mneg))
    print("  +%d ↔ %+d：1/B*(%+d) = %.7f——B* = %.7f au"
          % (mplus, mneg, mneg, inv_neg, 1.0/inv_neg))

# +2 数值过零搜索
print("\n★ +2 数值过零场强（二分搜索）：")
for N_r, r_max in [(3000, 120)]:
    dr = r_max / N_r
    # 先探测 E_0 符号区间
    for B in [0.1, 0.2, 0.27, 0.28, 0.3, 0.4, 0.6]:
        e = e0_m(N_r, r_max, 2, B)
        print("  B=%.3f：E_0 = %+.6f" % (B, e), flush=True)
    # 二分搜索过零
    b = bisect_Bstar(2, N_r, r_max, 0.20, 0.40)
    print("\n  ★ +2 过零 B* = %.7f au（dr=%.4f）——1/B* = %.7f" % (b, dr, 1.0/b))
    inv_b = 1.0/b
    inv_neg7 = 7.0/2.0 + 1.0/7.0 + 1.0/(7.0*2**7)
    print("  vs −7 闭式 1/B* = %.7f：1/B* 域差 %+.4f%%" % (inv_neg7, (inv_b-inv_neg7)/inv_neg7*100))
    print("  vs +1 的 1/B* = 4.217857（若 +2 落在 +1 附近——配对假说不成立）")

# +3/+4 探测（若 +2 命中则继续）
print("\n★ +3/+4 过零探测（配对 −6/−5 预言）：")
inv_neg6 = 6.0/2.0 + 1.0/7.0 + 1.0/(7.0*2**6)
inv_neg5 = 5.0/2.0 + 1.0/7.0 + 1.0/(7.0*2**5)
print("  −6 闭式：B* = %.7f——−5 闭式：B* = %.7f" % (1.0/inv_neg6, 1.0/inv_neg5))
for mplus, inv_neg in [(3, inv_neg6), (4, inv_neg5)]:
    B_pred = 1.0/inv_neg
    b = bisect_Bstar(mplus, N_r, r_max, 0.10, max(0.50, B_pred*1.5))
    print("  +%d 数值 B* = %.7f vs 配对预言 %.7f——1/B* 差 %+.4f%%"
          % (mplus, b, B_pred, (1.0/b-inv_neg)/inv_neg*100), flush=True)

json.dump({"pair_closed": {str(k): 1.0/(abs(v)/2.0+1.0/7.0+1.0/(7.0*2**abs(v))) for k, v in pair_m.items()}},
          open(os.path.join(BASE, "_phase102_p7_5e98_pair_probe.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
