# -*- coding: utf-8 -*-
"""
P7-5e-120 预备：谱方法全链（m=33..128）档位收敛测试
======================================================
119 验证形态：线性映射 [r_lo, r_hi] = [0.23|m|, 3.1|m|]（m=13 时 = [3,40]，N=300/600/900 逐位一致）。
本测试：m=33/64/128 × N=600/900/1200——确认大 m 同构缩放下的档位（动态范围相同 13.5）。
判定：N=900 与 N=1200 逐位一致（差 <1e-7 级）→ 全链用 N=900（效能优先）。
"""
import time
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

def Bstar_spectral(m, N=900, w=0.0265):
    """区间 [0.23|m|, 3.1|m|]（119 同构缩放）。返回 B*、7 点 E0 窗口。"""
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
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
    return B0 + xx, Es

if __name__ == "__main__":
    t0 = time.time()
    print("== 谱方法全链档位收敛测试：m=33/64/128 × N=600/900/1200 ==", flush=True)
    for m in [-33, -64, -128]:
        cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
        prev = None
        for N in [600, 900, 1200]:
            Bs, Es = Bstar_spectral(m, N=N)
            d = abs(1.0/Bs - cl)
            diff = "" if prev is None else "  与 N=%.0f 差 %.1e" % (prev[0], abs(Bs-prev[1]))
            print("  m=%4d  N=%4d → B*=%.8f  1/B*=%.8f  δ=%.7f%s" % (m, N, Bs, 1.0/Bs, d, diff), flush=True)
            prev = (N, Bs)
    print("耗时 %.1f s——exit 0" % (time.time()-t0), flush=True)
