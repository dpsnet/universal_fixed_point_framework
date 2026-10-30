# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-107b：m=−6 续跑——仅 dr=0.0025 档（N_r=48000）
================================================================
前 3 档（dr=0.02/0.01/0.005）已由 107 脚本完成并输出至 p107_out.txt。
本脚本补最重的 dr=0.0025 档（7 点 × ~10-20 min ≈ 1.5-2.5 h），JSON 落盘，
供合并脚本做三阶 Richardson（与 m=−5 严格可比）。
e0_m 带降级重试（tol/maxiter 递进）。
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

print("P7-5e-107b：m=−6 续跑 dr=0.0025 档（N_r=48000，7 点）", flush=True)

Bstar_closed = 1.0 / (3.0 + 1.0/7.0 + 1.0/448.0)
w = 0.0265
Bs = np.linspace(Bstar_closed*(1-w), Bstar_closed*(1+w), 7)
dr = 0.0025
N_r = int(round(120.0 / dr))
Es = []
for i, B in enumerate(Bs):
    t0 = time.time()
    e = e0_m(N_r, 120.0, -6, float(B))
    Es.append(e)
    print("  B=%.5f（%d/7）：E0 = %+.10f（%.1fs）" % (B, i+1, e, time.time()-t0), flush=True)
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
print("dr=0.0025：c1 = %+.9f、c2 = %+.9f、c3 = %+.9f、B* = %.8f、RMS = %.2e"
      % (c1, c2, c3, Bcross, rms), flush=True)

json.dump({"dr": dr, "c1": float(c1), "c2": float(c2), "c3": float(c3),
           "B*": float(Bcross), "rms": rms, "Es": Es.tolist(), "Bs": Bs.tolist()},
          open(os.path.join(BASE, "_phase102_p7_5e107_m6_dr0025.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0", flush=True)
