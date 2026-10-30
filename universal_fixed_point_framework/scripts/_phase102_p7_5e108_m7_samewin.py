# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-108：m=−7 同窗口 dr 外推（前 3 档——D 层对合镜像检验）
================================================================
闭式 1/B*(−7) = 7/2 + 1/7 + 1/896 = 3.643973214、B* = 0.27443
窗口 = B*±2.65% 7 点。D_7 = (9−14)² = 25（与 m=−2 同档——对合 m↦9−m 镜像点）
判别：
  ① 失调段 2 增长律：m=−6 −0.085%——若比值 1.67 延续 → −0.14% 级；线性 → −0.10% 级
  ② A_7 镜像：A_7 = c1×25——若对合成立 ≈ 6.5（A_2=7.006×c1 演化比值）
  ③ 失调是否回落（镜像点行为）——对合 vs 失效域
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

print("P7-5e-108：m=−7 同窗口 dr 外推（前 3 档——对合镜像检验）", flush=True)
closed = 7.0/2.0 + 1.0/7.0 + 1.0/896.0
Bstar_closed = 1.0/closed
print("闭式 1/B* = %.10f、B* = %.8f" % (closed, Bstar_closed), flush=True)
w = 0.0265
Bs = np.linspace(Bstar_closed*(1-w), Bstar_closed*(1+w), 7)
print("B 窗口 = [%.5f, %.5f] 7 点" % (Bs[0], Bs[-1]), flush=True)

drs = [0.02, 0.01, 0.005]
results = {}
for dr in drs:
    N_r = int(round(120.0 / dr))
    Es = []
    for i, B in enumerate(Bs):
        t0 = time.time()
        e = e0_m(N_r, 120.0, -7, float(B))
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

drs_sorted = sorted(drs, reverse=True)
vals = [results[d]["B*"] for d in drs_sorted]
v1 = [(4*vals[i+1]-vals[i])/3.0 for i in range(2)]
v2 = (16*v1[1]-v1[0])/15.0
B_0_est = v2
c1_0 = (16*(4*results[0.01]["c1"]-results[0.02]["c1"])/3.0 - (4*results[0.005]["c1"]-results[0.01]["c1"])/3.0)/15.0
d1B = (1.0/B_0_est - 1.0/Bstar_closed)/(1.0/Bstar_closed)*100
A7 = c1_0 * 25.0
print("\n★ Richardson 二阶 B*(0) = %.8f——失调（1/B 域）= %+.5f%%" % (B_0_est, d1B), flush=True)
print("★ c1(0) ≈ %.8f、A_7 = c1×25 ≈ %.4f（镜像预测 ~6.5，A_2=7.006）" % (c1_0, A7), flush=True)
print("★ 失调七点：m=−2 +0.0167%、m=−3 +0.0210%、m=−4 +0.0204%、m=−5 −0.0512%、m=−6 −0.0854%、m=−7 %+.5f%%" % d1B, flush=True)
print("★ 判别：段 2 比值（m=−7/m=−6）= %.3f（比值 1.67 延续 = 段 2 指数律；≈1.16 = 线性律）" % (abs(d1B)/0.0854,), flush=True)

json.dump({"Bstar_closed": Bstar_closed, "Bs": Bs.tolist(), "results": results,
           "B_0_est": B_0_est, "delta_1B_pct": d1B, "A7": A7},
          open(os.path.join(BASE, "_phase102_p7_5e108_m7_3dr.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0", flush=True)
