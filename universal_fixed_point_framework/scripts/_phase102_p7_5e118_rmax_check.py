# -*- coding: utf-8 -*-
"""P7-5e-118 预备：r_max 校验（m=33/64/128）——大 |m| 势阱 r_min≈|m|，需按 m 放大"""
import time, json, os
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
w = 0.0265

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

print("== r_max 校验（dr=0.01 单档 B* 对比，r_min≈|m| 假设）==", flush=True)
t0 = time.time()
for m, rms_pairs in [(-33, [120.0, 240.0, 360.0]),
                     (-64, [240.0, 480.0, 640.0]),
                     (-128, [512.0, 1024.0, 1536.0])]:
    print("m=%4d 闭式 B*=%.8f：" % (m, 1.0/closed_1B(m)), flush=True)
    vals = {}
    for rm in rms_pairs:
        vals[rm] = Bstar_1dr(m, rm, 0.01)
        print("  r_max=%.0f → B*=%.8f（%.1f s）" % (rm, vals[rm], time.time()-t0), flush=True)
    d12 = abs(vals[rms_pairs[0]]-vals[rms_pairs[1]])
    d23 = abs(vals[rms_pairs[1]]-vals[rms_pairs[2]])
    print("  r1 vs r2 差 %.2e；r2 vs r3 差 %.2e —— %s" % (
        d12, d23,
        "最小档不足" if d12 > 1e-7 else ("中等档充足（末差 %.2e）" % d23)), flush=True)

print("", flush=True)
print("耗时 %.1f s——exit 0" % (time.time()-t0), flush=True)
