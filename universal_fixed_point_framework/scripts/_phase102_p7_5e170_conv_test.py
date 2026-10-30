# -*- coding: utf-8 -*-
"""
P7-5e-170 前置：m=1024 收敛测试——N=600 vs 900 vs 1200
=====================================================
164 已证 m≤512 时 N=600 饱和（vs N=1200 差 1e-12 级）。
m=1024 区间 [235.5, 3174.4] 更大——保险验证 N=600 仍收敛。
判据：三档 B* 逐位一致（差 < 1e-10 级）→ N=600 可用于全链。
"""
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

def closed_1B(m):
    a = abs(m)
    tail = 1.0/(7.0*2.0**a) if a <= 120 else 0.0   # m≥120 时尾巴 <1e-36 可忽略；m=1024 时 2^m 溢出浮点
    return a/2.0 + 1.0/7.0 + tail

def Bstar_spectral(m, N=600, w=0.0265):
    cl = closed_1B(m)
    Bc = 1.0/cl
    r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
    x, D1, D2 = cheb_d1d2(N)
    a, b = r_lo, r_hi
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5 * D2 / (scale*scale)
    r_in = r[1:-1]
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    Es = np.empty(7)
    for i, B in enumerate(Bs):
        H = T[1:-1, 1:-1] + np.diag(V_eff(r_in, float(B), m))
        ev = np.real(eig(H, check_finite=False)[0])
        cand = ev[(ev > -1.0) & (ev < 1.0)]
        Es[i] = cand.min() if len(cand) else np.nan
    B0 = float(Bs[3]); X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    xx = -c0/c1
    for _ in range(6):
        xx = xx - (c0+c1*xx+c2*xx**2+c3*xx**3)/(c1+2*c2*xx+3*c3*xx**2)
    return B0 + xx

print("== P7-5e-170 前置：m=1024 收敛测试 ==", flush=True)
res = {}
for N in [600, 900, 1200]:
    B = Bstar_spectral(-1024, N=N)
    res[N] = B
    print("  N=%4d：B* = %.12f（delta = %.3e）" % (N, B, abs(1.0/B - closed_1B(1024))), flush=True)
d1 = abs(res[600]-res[1200])
d2 = abs(res[900]-res[1200])
print("  |N600−N1200| = %.2e；|N900−N1200| = %.2e" % (d1, d2), flush=True)
print("  判据：<1e-10 → N=600 饱和可用", flush=True)
print("  结论：%s" % ("N=600 饱和——全链 m=1024 可用" if max(d1, d2) < 1e-10 else "★ N=600 未饱和——需升 N"), flush=True)
print("exit 0", flush=True)
