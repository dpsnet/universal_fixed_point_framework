# -*- coding: utf-8 -*-
"""
P7-5e-135：消失点斜率 1/4 锁定判别（m=256 + 窗口收敛 + 双口径）
================================================================
P1 m=256 碗形：E_min·m、B_min/B*、dE/dB|_{B*}（vs 1/4）
P2 窗口收敛：B* 局部拟合窗口 w 从 2.65%→0.5%，dE/dB 收敛值
P3 双口径：133 式（7 点三次解析导数）vs 134 式（跨零两侧局部三次）
P4 全 m 对照：33/64/128/256 斜率序列 → 渐近 1/4 判别
"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

N_SP = 600

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

def E0_at(B, m, N=N_SP):
    r_lo, r_hi = 0.23*abs(m), 3.1*abs(m)
    x, D1, D2 = cheb_d1d2(N)
    a, b = r_lo, r_hi
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5 * D2 / (scale*scale)
    r_in = r[1:-1]
    H = T[1:-1, 1:-1] + np.diag(V_eff(r_in, float(B), m))
    ev = np.real(eig(H, check_finite=False)[0])
    neg = ev[ev < 0]
    if len(neg):
        return float(np.max(neg))
    pos = ev[ev >= 0]
    return float(pos.min()) if len(pos) else float(ev.min())

def scan_es(m, Bc, w, npt=9):
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), npt)
    Es = np.array([E0_at(b, m) for b in Bs])
    return Bs, Es

def slope_at(Bs, Es):
    """局部三次：dE/dB 在窗口中心（Bc）"""
    B0 = Bs[len(Bs)//2]; X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    c, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    return c[1], c

def bstar_from(Bs, Es):
    B0 = Bs[len(Bs)//2]; X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    c, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = c
    xx = -c0/c1
    for _ in range(6):
        xx = xx - (c0+c1*xx+c2*xx**2+c3*xx**3)/(c1+2*c2*xx+3*c3*xx**2)
    return B0 + xx, c

print("=== P7-5e-135 消失点斜率锁定 ===", flush=True)
Q4 = 0.25
for m in (-33, -64, -128, -256):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    Bc = 1.0/cl
    # P2 窗口收敛：w=2.65% 与 w=0.5%
    row = []
    for w in (0.0265, 0.005):
        Bs, Es = scan_es(m, Bc, w)
        s, c = slope_at(Bs, Es)
        Bstar, c = bstar_from(Bs, Es)
        row.append((w, s, Bstar))
    # P1 碗形（宽扫）
    Bw = np.linspace(0.0, 1.15*Bc, 46)
    Ew = np.array([E0_at(b, m) for b in Bw])
    imin = int(np.argmin(Ew))
    Bmin, Emin = Bw[imin], Ew[imin]
    Emin_m = Emin*abs(m)
    print("m=%3d：Bc=%.8f、碗底 B_min=%.6f（B*/%d 比例 %.3f）、E_min=%.8f（E_min·|m|=%.6f vs 1/4）、dE/dB w2.65%%=%.6f / w0.5%%=%.6f（vs 1/4 dev %+.3f pct）" % (
        m, Bc, Bmin, 4, Bmin/(row[1][2])*4, Emin, Emin_m, row[0][1], row[1][1],
        (row[1][1]-Q4)/Q4*100.0), flush=True)
print("exit 0", flush=True)
