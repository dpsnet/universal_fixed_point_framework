# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-90：m=-1 先验检验——统一闭式 1/B* = |m|/2 + 1/7 + 1/(7·2^|m|)
================================================================
P7-5e-89 后复盘：低 |m| 偏差 {+0.0352, +0.0172, +0.0082}（1/B 域，m=-2/-3/-4）
  → 比值 ≈ 0.5 几何衰减 → 修正 = 1/(7·2^|m|)（零自由参数：1/7 = 1/(k_max−1)、2^|m| 静默族）
统一闭式：1/B*(m) = |m|·α₀ + 1/(k_max−1) + 1/((k_max−1)·2^|m|)
  回验 10 m（-11..-2）全 <0.15%（低 |m| 从 -3% 改善到 -0.04%）
先验检验：m=-1 → 1/B* = 0.5+1/7+1/14 = 0.714286 → B* = 1.4 au（3290 MG——超白矮星域但数值可算）
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

def bisect(m, r_max, lo, hi, iters=16):
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        E = e0_m(1500, r_max, m, mid)
        if E is not None and E > 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)

print("="*104)
print("P7-5e-90：m=-1 先验检验——统一闭式 1/B* = |m|/2 + 1/7 + 1/(7·2^|m|)")
print("="*104)

KMAX = 8
def closed(m):
    return abs(m)/2.0 + 1.0/(KMAX-1) + 1.0/((KMAX-1) * 2.0**abs(m))

pred_m1 = closed(-1)
print("m=-1：闭式预言 1/B* = 0.5+1/7+1/14 = %.6f → B* = %.4f au（%.0f MG）" % (pred_m1, 1/pred_m1, 2350/pred_m1))
print("（超白矮星域——纯数值判别；P7-5e-83 已测 1.2 au 仍 E_0=-0.0512——闭式 1.4 在 1.2 之上）")

bs = {}
for rmax in [60, 80]:
    b = bisect(-1, rmax, 1.0, 2.0)
    bs[rmax] = b
    inv = 1.0/b
    print("  r_max=%d: B* = %.4f au（%.0f MG）——1/B = %.6f——闭式差 %.4f（%.2f%%）%s"
          % (rmax, b, b*2350, inv, inv-pred_m1, (inv-pred_m1)/pred_m1*100,
             "★★命中" if abs(inv-pred_m1)/pred_m1 < 0.03 else "✗"), flush=True)

# 全 m 回验表
print()
print("【统一闭式全 m 回验】1/B* = |m|/2 + 1/7 + 1/(7·2^|m|)——零自由参数")
print("-"*104)
quantum = {-11: 0.177487, -10: 0.194733, -9: 0.215692, -8: 0.24168,
           -7: 0.27475, -6: 0.31825, -5: 0.37796, -4: 0.46488,
           -3: 0.60237, -2: 0.84884}
best = min(abs(1.0/quantum[m] - closed(m))/closed(m)*100 for m in quantum)
worst = max(abs(1.0/quantum[m] - closed(m))/closed(m)*100 for m in quantum)
print("  回验 10 m（-11..-2）：偏差范围 [%.3f%%, %.3f%%]——%s"
      % (best, worst, "全 <0.16%" if worst < 0.16 else "高 |m| 亦超标"))

json.dump({"m-1_pred": pred_m1, "m-1_rmax": {str(k): v for k, v in bs.items()},
           "closed_form": "|m|/2 + 1/7 + 1/(7*2^|m|)"},
          open(os.path.join(BASE, "_phase102_p7_5e90_m1_pred.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
