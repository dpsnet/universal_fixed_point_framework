# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-89：m=+1 过零高精度验证 + 9 窗口配对闭式
================================================================
发现（复盘 P7-5e-81 的 m=+1 过零 0.23708）：
  1/B*(+1) = 4.2180 ≈ k_max/2 + 1/(k_max−1) + N_gen/(k_max·(k_max−N_gen))
           = 4 + 1/7 + 3/40 = 4.217857（差 0.0025%）
  结构：+1 的"等效 |m|" = k_max = 8（镜像反转）——+1 ↔ −8 配对（1+8=9=N_gen²）
  9 窗口（P7-5e-82）机制闭式化：+1 过零 ≈ −8 闭式过零 + 3/40（1/B 域）
验证：m=+1 过零二分加深（18 次）+ r_max 稳定性——确认 1/B* 精确值
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

def bisect(m, r_max, lo, hi, iters=18):
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        E = e0_m(1500, r_max, m, mid)
        if E is not None and E > 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)

print("="*104)
print("P7-5e-89：m=+1 过零高精度验证 + 9 窗口配对闭式")
print("="*104)

KMAX, NGEN = 8, 3
closed_m1 = KMAX/2 + 1.0/(KMAX-1) + NGEN/(KMAX*(KMAX-NGEN))  # 4 + 1/7 + 3/40
pred_B = 1.0/closed_m1
print("闭式：1/B*(+1) = k_max/2 + 1/(k_max−1) + N_gen/(k_max·(k_max−N_gen))")
print("     = 4 + 1/7 + 3/40 = %.6f → B* = %.6f au（%.1f MG）" % (closed_m1, pred_B, pred_B*2350))

bs = {}
for rmax in [60, 80, 100]:
    b = bisect(1, rmax, 0.20, 0.26)
    bs[rmax] = b
    inv = 1.0/b
    print("  r_max=%d: B* = %.6f au（%.1f MG）——1/B = %.6f——闭式差 %.4f（%.2f%%）%s"
          % (rmax, b, b*2350, inv, inv-closed_m1, (inv-closed_m1)/closed_m1*100,
             "★★命中" if abs(inv-closed_m1)/closed_m1 < 0.005 else "✗"))
print("  r_max 稳定性：%s" % ("稳定" if max(bs.values())-min(bs.values()) < 1e-4 else "不稳定"), flush=True)

print()
print("【配对结构】+1 ↔ −8：|m| 和 = 9 = N_gen²")
print("  1/B*(+1) = %s + 3/40（正侧镜像——等效 |m| = k_max）" % "4+1/7")
print("  1/B*(−8) = 4+1/7（负 m 闭式 |m|=k_max）——间距 3/40 = N_gen/(k_max·(k_max−N_gen))")
print("  B 域间距：Δ(1/B) = 3/40 = 0.075 ↔ ΔB ≈ 0.075×B² ≈ 0.075×0.239² ≈ 0.0043 au ≈ 10.1 MG")
print("  （实测窗口宽 0.0046 au = 10.8 MG——差 6.5%——二阶项）")

json.dump({"closed_m1": closed_m1, "m1_rmax": {str(k): v for k, v in bs.items()}},
          open(os.path.join(BASE, "_phase102_p7_5e89_m1_pair.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
