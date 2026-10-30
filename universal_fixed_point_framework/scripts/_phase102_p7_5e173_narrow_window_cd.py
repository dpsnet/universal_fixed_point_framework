# -*- coding: utf-8 -*-
"""
P7-5e-173: 窄窗 w=0.01 全链直接拟合——确认 C=13/128 与 D=103/5000 候选
====================================================================
172 已证：w=0.0265 的 κ·m = 三次插值截断伪影（δ_sys ∝ w⁴·m）；窄窗 w=0.01 下 κ_eff→0。
173：w=0.01 重算 m=512..1024 全链（17 点），直接拟合 delta = 1/56 + C/m + D/m² (+E/m³)，
高精度输出 C、D：
  - C ≈ −13/128 = −0.1015625 → C 双通道+窄窗三确认
  - D ≈ −103/5000 = −0.0206（用户候选 2026-10-15：103 = 2⁷−5²，分母 5⁴·2³）→ D 候选升格判别
  - 分段稳定性（m≥512/640/768/896）四档 D 是否稳定
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
    tail = 1.0/(7.0*2.0**a) if a <= 120 else 0.0
    return a/2.0 + 1.0/7.0 + tail

def Bstar_spectral(m, N=600, w=0.01):
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

print("== P7-5e-173 窄窗 w=0.01 全链直接拟合（C + D 候选判别）==", flush=True)
ms = np.arange(512, 1025, 32, dtype=float)   # 17 点
inv56 = 1.0/56.0
C13 = -13.0/128.0
Dcan = -103.0/5000.0                          # 用户候选：103 = 2^7 − 5^2，分母 5^4·2^3
Dcan_old = -47.0/2500.0                       # 122 旧候选
delta = np.empty(len(ms))
for i, m in enumerate(ms):
    cl = closed_1B(int(m))
    B = Bstar_spectral(-int(m), N=600, w=0.01)
    delta[i] = cl - 1.0/B
    print("  m=%5d  delta=%.9e" % (int(m), delta[i]), flush=True)

for name, jmax in [("3 参（1/56+C/m+D/m²）", 3), ("4 参（+E/m³）", 4)]:
    A = np.vstack([1.0/ms**j for j in range(jmax)]).T
    c, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
    resid = delta - A@c
    rms = float(np.sqrt(np.mean(resid**2)))
    Cfit = c[1]; Dfit = c[2] if jmax >= 3 else float('nan')
    print("\n%s（m≥512，17 点，w=0.01）：RMS=%.2e" % (name, rms))
    print("  C = %+.12f   13/128 = %+.12f   差 %+.6f pct" % (Cfit, C13, (Cfit-C13)/abs(C13)*100))
    print("  D = %+.12f   103/5000 = %+.12f   差 %+.4f pct" % (Dfit, Dcan, (Dfit-Dcan)/abs(Dcan)*100))
    print("  D vs 47/2500 = %+.12f：差 %+.1f pct" % (Dcan_old, (Dfit-Dcan_old)/abs(Dcan_old)*100))

print("\n== 分段稳定性（w=0.01，4 参）==")
for lo in [512, 640, 768, 896]:
    sel = ms >= lo
    A = np.vstack([1.0/ms[sel]**j for j in range(4)]).T
    c, _, _, _ = np.linalg.lstsq(A, delta[sel], rcond=None)
    resid = delta[sel] - A@c
    rms = float(np.sqrt(np.mean(resid**2)))
    print("  m>=%4d（%2d 点）C=%+.10f  D=%+.10f  RMS=%.2e   |D−103/5000|=%+.4f pct" % (
        lo, sel.sum(), c[1], c[2], rms, (c[2]-Dcan)/abs(Dcan)*100))
print("exit 0", flush=True)
