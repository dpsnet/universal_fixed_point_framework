# -*- coding: utf-8 -*-
"""
P7-5e-124a 修正：m=−256 谱方法收敛测试（负 m——离心项过零势阱）
================================================================
120 全链为负 m（m=−33..−128）：V_eff 中 (m+½Br²)² 在 r=√(2|m|/B) 过零
  → 势阱由 −1/r 主导（深度 ~ −1/√(2|m|/B)），束缚态 E_0(B) 过零 → B*
m=−256：r_lo=58.88、r_hi=793.6；Bc=1/128.1429≈0.0078038
  势阱中心 r≈256、深度 V≈−1/256≈−0.0039（极浅——N=600 分辨率 1.22 需 ~20+ 格点覆盖）
先验登记：
  P1 m=−256 的 B* 在 N=600/900/1200 逐位一致（差 <1e-12）→ N=600 可继续
  P2 若 N=600 不收敛（差 >1e-10）→ 换 N=900
对照锚：双曲外推 1/B*(256) ≈ 128.125 + 0.1016/256 + 0.0188/256² ≈ 128.12540
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
    return abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))

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

m = -256
print("== P7-5e-124a：m=−256 收敛测试（负 m，N=600/900/1200）==", flush=True)
# 势阱检查
cl = closed_1B(m); Bc = 1.0/cl
rs = np.linspace(0.01*abs(m), 3.1*abs(m), 500000)
V = V_eff(rs, Bc, m)
print("  势阱：V_min=%.6e @ r=%.2f（B=Bc，负 m 离心过零势阱）" % (V.min(), rs[np.argmin(V)]), flush=True)
vals = {}
for N in (600, 900, 1200):
    B = Bstar_spectral(m, N=N)
    vals[N] = B
    print("  N=%4d  B*=%.12f  1/B*=%.8f" % (N, B, 1.0/B), flush=True)
d1 = abs(vals[600]-vals[900]); d2 = abs(vals[600]-vals[1200])
print("  |N600−N900| = %.2e    |N600−N1200| = %.2e" % (d1, d2), flush=True)
anchor = 128.125 + 0.1016/256.0 + 0.0188/(256.0**2)
print("  双曲外推锚：1/B*(256) ≈ %.8f" % anchor, flush=True)
dev = (1.0/vals[600]-anchor)/anchor*100
print("  N=600 vs 双曲锚偏差：%+.6f pct" % dev, flush=True)
ok = d1 < 1e-12 and d2 < 1e-12
print("  收敛判定：%s" % ("通过——N=600 可用" if ok else "★ 未通过——需 N=900 全链"), flush=True)
print("exit 0", flush=True)
