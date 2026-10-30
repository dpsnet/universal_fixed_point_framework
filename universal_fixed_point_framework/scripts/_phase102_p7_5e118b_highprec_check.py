# -*- coding: utf-8 -*-
"""
P7-5e-118b：尾部数值噪声判别——m=123/128 高精度档复核
======================================================
118 主脚本尾部（m≥100）偏差 ±3~5% 且相邻点跳动 1e-3 级（物理不可能）
→ 怀疑 Richardson 二阶数值噪声，非物理变换。
本脚本：dr={0.005, 0.0025} 两档 Richardson 二阶复核 m=123/128（+ 对照 m=80/33），
与双曲预测对比：收敛到双曲 → 数值噪声确认（双曲持续）；稳定偏离 → 真变换。
"""
import time, json, os
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
w = 0.0265
D_INF, C_HYP = 0.017895, 0.103317

def closed_1B(m):
    return abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))

def solve(N_r, r_max, B, m):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    return float(eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0])

def Bstar_1dr(m, r_max, dr):
    cl = closed_1B(m); Bc = 1.0/cl
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    N_r = int(round(r_max / dr))
    Es = np.array([solve(N_r, r_max, float(B), m) for B in Bs])
    B0 = float(Bs[3]); X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    x = -c0/c1
    for _ in range(6):
        x = x - (c0+c1*x+c2*x**2+c3*x**3)/(c1+2*c2*x+3*c3*x**2)
    return B0 + x

print("== 高精度复核（dr=0.005/0.0025 两档 Richardson 二阶）==", flush=True)
t0 = time.time()
for m in [-33, -80, -123, -128]:
    r_max = max(120.0, 4.0*abs(m))
    cl = closed_1B(m)
    B5  = Bstar_1dr(m, r_max, 0.005)
    B25 = Bstar_1dr(m, r_max, 0.0025)
    R2 = (4*B25 - B5)/3.0
    delta = abs(1.0/R2 - cl)
    pred = D_INF - C_HYP/abs(m)
    dev = (delta-pred)/pred*100
    print("m=%4d  r_max=%.0f  B*(0.005)=%.8f  B*(0.0025)=%.8f  R2=%.8f  δ=%.7f  双曲=%.6f  偏差=%+.2f pct"
          % (m, r_max, B5, B25, R2, delta, pred, dev), flush=True)
    print("        主脚本 δ(0.005/0.01/0.02 二阶)：%s" % (
        "需对比 JSON" ), flush=True)
print("耗时 %.0f s" % (time.time()-t0), flush=True)
print("exit 0", flush=True)
