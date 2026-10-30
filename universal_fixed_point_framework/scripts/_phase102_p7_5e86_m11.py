# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-86：m=-11 第三次先验检验 + 通道数预测闭式化
================================================================
P7-5e-85 闭式升格：1/B*(m) = |m|/2 + 1/7（高 |m| 6/6 <0.16% + 2 次先验命中）
第三次先验：m=-11 → 1/B* = 5.5+1/7 = 5.642857 → B* = 0.177215 au（416.5 MG）
附带：用闭式预测通道数 N_neg(B) = floor(2(1/B − 1/7)) + 修正——检验通道数观测
低 |m| 修正登记：m=-2 实测 0.84884 vs 闭式 0.875（−3.0%）
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
print("P7-5e-86：m=-11 第三次先验检验（闭式 1/B* = |m|/2 + 1/7）")
print("="*104)

pred = 1.0 / (11.0 / 2 + 1.0 / 7)
print("m=-11：闭式预言 B* = 1/(11/2+1/7) = %.6f au（%.1f MG）" % (pred, pred*2350))
bs = {}
for rmax in [60, 80, 100]:
    b = bisect_bstar(-11, rmax, 0.10, 0.22)
    bs[rmax] = b
    print("  r_max=%d: B* = %.6f au（%.1f MG）——差 %.4f（%.2f%%）%s"
          % (rmax, b, b*2350, b-pred, (b-pred)/pred*100,
             "★★命中" if abs(b-pred)/pred < 0.01 else "✗"))
print("  r_max 稳定性：%s" % ("稳定" if max(bs.values())-min(bs.values()) < 1e-3 else "不稳定"), flush=True)

print()
print("【通道数闭式预测】（负 m 存活数 = max{|m|: B*(m) > B}，用闭式 B* = 1/(|m|/2+1/7)）")
print("-"*104)
obs = {0.25: 8, 0.30: 7, 0.35: 6, 0.40: 5, 0.50: 4, 0.65: 3, 0.85: 2, 1.30: 2}
for B in sorted(obs):
    # 闭式预测：|m| < 2(1/B − 1/7) 的负 m 存活
    n_closed = max(0, int(np.floor(2.0*(1.0/B - 1.0/7.0))))
    # 用实测过零的精确预测（P7-5e-83/85 数据）
    n_exact = sum(1 for m in range(-1, -12, -1) if 1.0/(abs(m)/2+1/7) > B or True)
    print("  B=%.2f：观测通道 %d vs 闭式预测 %d %s" % (B, obs[B], n_closed, "✓" if obs[B]==n_closed else "✗"))

json.dump({"m-11_pred": pred, "m-11_rmax": {str(k): v for k, v in bs.items()}},
          open(os.path.join(BASE, "_phase102_p7_5e86_m11.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
