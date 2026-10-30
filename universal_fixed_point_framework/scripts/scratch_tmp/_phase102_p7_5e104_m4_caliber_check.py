# -*- coding: utf-8 -*-
"""m=-4 口径复验：用历史脚本同口径（窗口 [0.455,0.475] ±2.2%、4 档 dr、Richardson 三阶）
但求解器换 tridiag——验证 m=-4 全链偏差（-7.3%）是否纯粹是口径差异而非数值问题。
"""
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

r_max = 120.0
m = -4
Bstar_closed = 112.0 / 241.0
Bs = np.linspace(0.455, 0.475, 7)
drs = [0.02, 0.01, 0.005, 0.0025]

def solve(N_r, B):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    return float(eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0])

results = {}
for dr in drs:
    N_r = int(round(r_max / dr))
    Es = np.array([solve(N_r, float(B)) for B in Bs])
    B0 = 0.465
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
    print("dr=%.4f：c1=%+.9f c2=%+.9f c3=%+.9f B*=%.8f RMS=%.2e" % (dr, c1, c2, c3, Bcross, rms), flush=True)

def rich(vals):
    v1 = [(4*vals[i+1]-vals[i])/3.0 for i in range(3)]
    v2 = [(16*v1[i+1]-v1[i])/15.0 for i in range(2)]
    v3 = (64*v2[1]-v2[0])/63.0
    return v1, v2, v3

Br = [results[d]["B*"] for d in drs]
_, _, B_0 = rich(Br)
d_abs = 1.0/B_0 - 1.0/Bstar_closed
d_pct = d_abs/(1.0/Bstar_closed)*100
print("", flush=True)
print("Richardson 三阶 B*(0)=%.8f  1/B*(0)=%.8f  闭式 1/B*=%.8f" % (B_0, 1.0/B_0, 1.0/Bstar_closed), flush=True)
print("δ(1/B) 带符号 = %+.8f（%.4f pct）" % (d_abs, d_pct), flush=True)
print("历史定案：δ_abs = 0.000473（判别脚本登记）；全链统一口径 = 0.000438（±2.65%/3档/二阶）", flush=True)
print("→ %s" % ("复现历史值——差异=口径差异（窗口±2.2% + 三阶外推），非数值错误" 
      if abs(abs(d_abs) - 0.000473) < 5e-6 else "未复现——需进一步诊断"), flush=True)
