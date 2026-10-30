# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-107：m=−6 同窗口 dr 外推（前 3 档判别——边界：回带 or 继续偏离）
================================================================
闭式 1/B*(−6) = 3 + 1/7 + 1/448 = 3.145089286、B* = 1/3.145089286 = 0.31795659
B 窗口 = B*±2.65% = [0.30953, 0.32638] 7 点（同 m=−5 相对窗口宽度）
前 3 档 dr = 0.02/0.01/0.005（N_r = 6000/12000/24000），三阶 Richardson 判别失调方向。
判别：失调回带 ~+0.02% → m=−5 孤立边界点；失调继续偏离 → |m|≥5 系统性失效域。
e0_m 带降级重试（tol/maxiter 递进 1e-9/5e4 → 1e-8/1e5 → 1e-7/1.5e5）。
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

print("P7-5e-107：m=−6 同窗口 dr 外推（前 3 档判别）", flush=True)
print("闭式 1/B* = 3+1/7+1/448 = %.10f、B* = %.8f" % (3+1/7+1/448, 1/(3+1/7+1/448)), flush=True)

Bstar_closed = 1.0 / (3.0 + 1.0/7.0 + 1.0/448.0)
# 窗口：B*±2.65%（同 m=−5 相对宽度）
w = 0.0265
Bs = np.linspace(Bstar_closed*(1-w), Bstar_closed*(1+w), 7)
print("B 窗口 = [%.5f, %.5f] 7 点（B*=%.8f）" % (Bs[0], Bs[-1], Bstar_closed), flush=True)

drs = [0.02, 0.01, 0.005]
results = {}
for dr in drs:
    N_r = int(round(120.0 / dr))
    Es = []
    for i, B in enumerate(Bs):
        t0 = time.time()
        e = e0_m(N_r, 120.0, -6, float(B))
        Es.append(e)
        print("  dr=%.4f B=%.5f（%d/7）：E0 = %+.10f（%.1fs）" % (dr, B, i+1, e, time.time()-t0), flush=True)
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
    results[dr] = {"c1": float(c1), "c2": float(c2), "c3": float(c3), "B*": float(Bcross), "rms": rms}
    print("dr=%.4f：c1 = %+.9f、c2 = %+.9f、c3 = %+.9f、B* = %.8f、RMS = %.2e"
          % (dr, c1, c2, c3, Bcross, rms), flush=True)

# 三阶 Richardson（3 档 → 2 级 Richardson，比 4 档少一级——判别方向足够）
drs_sorted = sorted(drs, reverse=True)
vals = [results[d]["B*"] for d in drs_sorted]
v1 = [(4*vals[i+1]-vals[i])/3.0 for i in range(2)]
v2 = (16*v1[1]-v1[0])/15.0
B_0_est = v2
d1B = (1.0/B_0_est - 1.0/Bstar_closed)/(1.0/Bstar_closed)*100
print("\n★ Richardson 二阶（3 档）B*(0) 估计 = %.8f" % B_0_est, flush=True)
print("★ 失调（1/B 域）m=−6 = %+.5f%%（前三点带：m=−2 +0.0167%、m=−3 +0.0210%、m=−4 +0.0204%；m=−5 −0.0512%）" % d1B, flush=True)
print("★ 判别：回带（>−0.02%）→ m=−5 孤立边界点；继续偏离（≤−0.04%）→ |m|≥5 失效域", flush=True)

json.dump({"Bstar_closed": Bstar_closed, "Bs": Bs.tolist(), "results": results,
           "B_0_est": B_0_est, "delta_1B_pct": d1B},
          open(os.path.join(BASE, "_phase102_p7_5e107_m6_3dr.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0", flush=True)
