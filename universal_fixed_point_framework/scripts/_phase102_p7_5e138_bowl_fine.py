# -*- coding: utf-8 -*-
"""
P7-5e-138：碗底位置高精度定位——B_min/B* → 1/4 判别
================================================================
135 的 B_min/B*≈1.022（46 点 argmin 分辨率限制）——加密 + 抛物插值
P1 m=128 B 扫描 300 点（0..1.15Bc）碗底定位（抛物插值）
P2 B_min/B* vs 1/4（1.022 是分辨率还是真实偏离）
P3 E_min·|m| vs −1/4（高精度）
P4 与 135 的 46 点结果对照（加密收敛性）
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

def bowl_scan(m, npt):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    Bc = 1.0/cl
    Bs = np.linspace(0.0, 1.15*Bc, npt)
    Es = np.array([E0_at(b, m) for b in Bs])
    return Bc, Bs, Es

def bowl_fit(Bs, Es, ilo):
    """局部抛物插值碗底：取最低点附近 3 点"""
    i0 = int(np.argmin(Es))
    lo, hi = max(0, i0-1), min(len(Bs)-1, i0+1)
    x = Bs[lo:hi+1]; y = Es[lo:hi+1]
    A = np.vstack([np.ones_like(x), x, x**2]).T
    c, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    Bmin = -c[1]/(2*c[2])
    Emin = c[0] + c[1]*Bmin + c[2]*Bmin**2
    return Bmin, Emin, i0

print("=== P7-5e-138 碗底高精度定位 ===", flush=True)
for m in (-128, -256):
    Bc, Bs, Es = bowl_scan(m, 300)
    Bmin, Emin, i0 = bowl_fit(Bs, Es, None)
    # 参考 B*（135 锁定值）
    Bstar_ref = 1.0/(abs(m)/2.0 + 1.0/8.0)  # 大 m 渐近
    print("m=%3d：300 点碗底 B_min=%.7f（B*/4=%.7f，比 %.4f）、E_min=%.8f（E_min·|m|=%.6f vs −1/4）、B_min·|m|=%.6f vs 1/4（B_min≈1/(4m)? 则 B_min·m=0.25）" % (
        m, Bmin, Bstar_ref/4.0, Bmin/(Bstar_ref/4.0), Emin, Emin*abs(m), Bmin*abs(m)), flush=True)
    # 粗网格对照（46 点 argmin——135 口径）
    Bc46, Bs46, Es46 = bowl_scan(m, 46)
    i46 = int(np.argmin(Es46))
    print("  46 点对照：argmin B=%.6f（比 B*/4 %.4f）——加密后收敛判别" % (Bs46[i46], Bs46[i46]/(Bstar_ref/4.0)), flush=True)
print("exit 0", flush=True)
