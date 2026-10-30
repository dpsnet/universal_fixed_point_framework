# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-113：m=−12 同窗口 dr 外推（曲率形态第四点——先验预言检验）
================================================================
闭式 1/B*(−12) = 12/2 + 1/7 + 1/28672 = 6.142892、B* = 0.162789
窗口 = B*±2.65% 7 点。D_12 = (9−24)² = 225——继续超对合域
【先验预言（计算前写下）】
  失调 δ(12)：二次段假设（二阶差分 ≈ −1.5e-4 恒定）→ δ(12) ≈ 0.008540 + 0.000884 − 0.00015 ≈ 0.00927
  对照：线性延伸 δ(12) = 0.00990；更高阶（三阶差分非零）→ δ(12) < 0.0090
  判定：δ(12) ∈ [0.0090, 0.0096] → 二次段确认；>0.0096 → 回线性；<0.0090 → 更高阶
  ② c2 增量第 12 点：1/32 = 0.03125 保持（饱和律无域界预测）
  ③ c1 增量比：继续趋 1（1.228 → ?）
  ④ c3 二阶差分：摆动方向
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

print("P7-5e-113：m=-12 同窗口 dr 外推（曲率形态第四点——先验预言检验）", flush=True)
closed = 12.0/2.0 + 1.0/7.0 + 1.0/28672.0
Bstar_closed = 1.0/closed
print("闭式 1/B* = %.10f、B* = %.8f" % (closed, Bstar_closed), flush=True)
print("【先验预言】二次段假设 δ(12) ≈ 0.00927（二阶差分 -1.5e-4 恒定）vs 线性延伸 0.00990", flush=True)
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
        e = e0_m(N_r, 120.0, -12, float(B))
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
d_abs = abs(1.0/B_0_est - 1.0/Bstar_closed)
A12 = c1_0 * 225.0
print("", flush=True)
print("★ Richardson 二阶 B*(0) = %.8f——失调（1/B 域）= %+.5f%%（δ = %.6f）" % (B_0_est, d1B, d_abs), flush=True)
print("★ c1(0) ≈ %.8f、A_12 = c1×225 ≈ %.4f（超对合域第四点）" % (c1_0, A12), flush=True)
print("★ 先验预言检验：二次段预测 δ(12)≈0.00927 vs 实测 %.6f——线性 0.00990——更高阶 <0.0090" % d_abs, flush=True)
print("JSON 落盘……", flush=True)
json.dump({"Bstar_closed": Bstar_closed, "Bs": Bs.tolist(), "results": results,
           "B_0_est": B_0_est, "delta_1B_pct": d1B, "delta_1B_abs": d_abs, "A12": A12},
          open(os.path.join(BASE, "_phase102_p7_5e113_m12_3dr.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 OK  exit 0", flush=True)
