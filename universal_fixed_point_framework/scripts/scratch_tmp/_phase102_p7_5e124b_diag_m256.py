# -*- coding: utf-8 -*-
"""P7-5e-124b：m=256 nan 诊断——势阱深度 + 谱方法最低本征值"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

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

m = 256
cl = m/2.0 + 1.0/7.0
Bc = 1.0/cl
print("m=%d  cl(1/B*)=%.6f  Bc=%.8f" % (m, cl, Bc), flush=True)

# 1) 细网格扫描 V_eff 最小值（r 从 0.5 到 2000 对数网格）
rs = np.logspace(-0.3, 3.4, 200000)
V = V_eff(rs, Bc, m)
imin = np.argmin(V)
print("V_eff 最小值：V_min=%.6e @ r=%.3f（B=Bc）" % (V[imin], rs[imin]), flush=True)
# B 扫描看势阱深度随 B 变化
for Bf in [0.5*Bc, 0.8*Bc, Bc, 1.2*Bc, 2.0*Bc]:
    Vb = V_eff(rs, Bf, m)
    print("  B=%.3e: V_min=%.6e" % (Bf, Vb.min()), flush=True)

# 2) 谱方法最低本征值（N=600）
x, D1, D2 = cheb_d1d2(600)
a, b = 0.23*m, 3.1*m
r = (b-a)/2.0*x + (a+b)/2.0
scale = (b-a)/2.0
T = -0.5*D2/(scale*scale)
r_in = r[1:-1]
for Bf in [0.5*Bc, 0.8*Bc, Bc]:
    H = T[1:-1,1:-1] + np.diag(V_eff(r_in, Bf, m))
    ev = np.real(eig(H, check_finite=False)[0])
    ev.sort()
    print("  N=600 B=%.3e: 最低3本征值 = %.6e, %.6e, %.6e" % (Bf, ev[0], ev[1], ev[2]), flush=True)
print("exit 0", flush=True)
