# -*- coding: utf-8 -*-
"""P7-5e-124d：直接调用 120 原函数 m=33 调试——打印 Es 数组"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache
import sys
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
# 直接内嵌 120 原函数
@lru_cache(maxsize=8)
def cheb_d1d2(N):
    x = np.cos(np.pi * np.arange(N+1) / N)
    c = np.ones(N+1); c[0] = 2.0; c[-1] = 2.0
    D1 = np.zeros((N+1, N+1))
    for k in range(N+1):
        for l in range(N+1):
            if k != l:
                D1[k, l] = c[k]/c[l] * (-1.0)**(k+l) / (x[k] - x[l])
    for k in range(1, N):
        D1[k, k] = x[k] / (2.0*(1.0 - x[k]**2))
    D1[0, 0] = -(2.0*N**2 + 1.0)/6.0
    D1[N, N] = (2.0*N**2 + 1.0)/6.0
    return x, D1, D1 @ D1

def V_eff(r, B, m):
    return (m + 0.5*B*r*r)**2/(2.0*r*r) - 1.0/r

def closed_1B(m):
    return abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))

m = 33
cl = closed_1B(m)
Bc = 1.0/cl
print("m=%d  cl=%.10f  Bc=%.10f" % (m, cl, Bc), flush=True)
x, D1, D2 = cheb_d1d2(600)
a, b = 0.23*abs(m), 3.1*abs(m)
r = (b-a)/2.0*x + (a+b)/2.0
scale = (b-a)/2.0
T = -0.5*D2/(scale*scale)
r_in = r[1:-1]
Bs = np.linspace(Bc*(1-0.0265), Bc*(1+0.0265), 7)
for i, B in enumerate(Bs):
    H = T[1:-1,1:-1] + np.diag(V_eff(r_in, float(B), m))
    ev = np.real(eig(H, check_finite=False)[0])
    cand = ev[(ev > -1.0) & (ev < 1.0)]
    print("  B[%d]=%.8f  min_ev=%.6f  cand_min=%s  n_cand=%d" % (i, B, ev.min(), (cand.min() if len(cand) else "nan"), len(cand)), flush=True)
print("exit 0", flush=True)
