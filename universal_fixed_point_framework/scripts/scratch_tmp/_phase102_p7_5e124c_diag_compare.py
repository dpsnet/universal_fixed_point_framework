# -*- coding: utf-8 -*-
"""P7-5e-124c：m=33 对照诊断——120 谱方法到底扫什么过零"""
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

for m in (33, 64, 128, 256):
    cl = m/2.0 + 1.0/7.0
    Bc = 1.0/cl
    # V_eff 最小值（细网格）
    rs = np.logspace(-0.5, 3.5, 300000)
    V = V_eff(rs, Bc, m)
    print("m=%4d  cl=%.6f  Bc=%.8f  V_min(Bc)=%+.6e  (B→0 渐近 −1/(2m²)=%+.3e)" % (m, cl, Bc, V.min(), -1.0/(2.0*m*m)), flush=True)
    # 谱方法：B 从 0.5Bc 到 1.5Bc 扫 9 点，最低本征值
    x, D1, D2 = cheb_d1d2(400)
    a, b = 0.23*m, 3.1*m
    r = (b-a)/2.0*x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5*D2/(scale*scale)
    r_in = r[1:-1]
    evals = []
    for Bf in np.linspace(0.5*Bc, 1.5*Bc, 9):
        H = T[1:-1,1:-1] + np.diag(V_eff(r_in, Bf, m))
        ev = np.real(eig(H, check_finite=False)[0])
        evals.append(ev.min())
    evals = np.array(evals)
    print("  最低本征值 @ B/Bc = 0.5..1.5：", flush=True)
    print("   ", "  ".join("%+.4e" % e for e in evals), flush=True)
print("exit 0", flush=True)
