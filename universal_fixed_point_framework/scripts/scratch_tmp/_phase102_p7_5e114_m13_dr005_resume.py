# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-114 续算：dr=0.005 剩余 5 点（应用切换后任务中断恢复）
================================================================
背景：主脚本三档运行时应用切换——后台任务终止。dr=0.02/0.01 已全 7 点完成
（B*=0.15076424 / 0.15076335），dr=0.005 仅完成 2/7 点。
本脚本：跳过已完成 2 点（E0 硬编码），只算剩余 5 点 → 拟合 7 点三次多项式
求 B*(dr=0.005) → 落盘 JSON。Richardson 三档合并留待用户确认后补。
"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def e0_m(N_r, r_max, m, B, k=12):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
              offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    for tol, maxiter in [(1e-9, 50000), (1e-8, 100000), (1e-7, 150000)]:
        try:
            vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                            which='SA', maxiter=maxiter, tol=tol)
            return float(np.real(vals[0]))
        except Exception:
            continue
    raise RuntimeError("eigsh 全部降级失败：N_r=%d m=%d B=%.6f" % (N_r, m, B))

print("P7-5e-114 续算：dr=0.005 剩余 5 点（中断恢复）", flush=True)
closed = 13.0/2.0 + 1.0/7.0 + 1.0/57344.0
Bstar_closed = 1.0/closed
w = 0.0265
Bs = np.linspace(Bstar_closed*(1-w), Bstar_closed*(1+w), 7)

# 已完成 2 点（p114_out.txt 实测）
E_done = {0: -0.0010666016, 1: -0.0007317494}  # B=0.14655, 0.14788

dr = 0.005
N_r = int(round(120.0 / dr))
Es = []
for i, B in enumerate(Bs):
    if i in E_done:
        e = E_done[i]
        print("  dr=%.4f B=%.5f（%d/7）：E0 = %+.10f（跳过——已算）" % (dr, B, i+1, e), flush=True)
    else:
        t0 = time.time()
        e = e0_m(N_r, 120.0, -13, float(B))
        print("  dr=%.4f B=%.5f（%d/7）：E0 = %+.10f（%.1fs）" % (dr, B, i+1, e, time.time()-t0), flush=True)
    Es.append(e)
Es = np.array(Es)
B0 = float(Bs[len(Bs)//2])
X = Bs - B0
A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
c0, c1, c2, c3 = coef
x = -c0/c1
for _ in range(6):
    e = c0 + c1*x + c2*x**2 + c3*x**3
    de = c1 + 2*c2*x + 3*c3*x**2
    x = x - e/de
Bcross = B0 + x
rms = float(np.sqrt(np.mean((A@coef-Es)**2)))
print("", flush=True)
print("dr=0.005（7 点全）：c1 = %+.9f、c2 = %+.9f、c3 = %+.9f、B* = %.8f、RMS = %.2e"
      % (c1, c2, c3, Bcross, rms), flush=True)
print("三档 B*：{0.02}=0.15076424 {0.01}=0.15076335 {0.005}=%.8f——JSON 落盘（Richardson 待用户确认）" % Bcross, flush=True)
json.dump({"Bstar_closed": Bstar_closed, "Bs": Bs.tolist(),
           "Bstar_002": 0.15076424, "Bstar_001": 0.15076335, "Bstar_0005": float(Bcross),
           "c1_0005": float(c1), "c2_0005": float(c2), "c3_0005": float(c3), "rms_0005": rms},
          open(os.path.join(BASE, "_phase102_p7_5e114_m13_3dr.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 OK  exit 0", flush=True)
