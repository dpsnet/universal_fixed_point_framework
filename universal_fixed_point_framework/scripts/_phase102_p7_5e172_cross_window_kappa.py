# -*- coding: utf-8 -*-
"""
P7-5e-172: 交叉窗口判别——κ·m 尾项是真实结构还是三次插值窗口伪影
================================================================
170 基线：w = ±2.65%（7 点三次插值 + Newton 求根），κ = 2.447e-9 来自 delta 拟合。
判别：w ∈ {0.010, 0.020, 0.0265, 0.040, 0.050} 重算 m = 512/1024 的 B*。
- κ_eff 随 w 稳定（散布 << 自身）→ κ 真实结构
- κ_eff 随 w 大幅变化（~50%+）→ 提取链（窗口/插值）伪影
分辨率：delta 的 N 收敛精度 ~9e-10（170 收敛测试）；κ·m 在 m=1024 效应 2.5e-6 —— 可分辨。
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
    tail = 1.0/(7.0*2.0**a) if a <= 120 else 0.0   # m>120: 尾 < 1e-36 截断（2^1024 溢出）
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

print("== P7-5e-172 交叉窗口判别（κ·m 尾项：真实 vs 窗口伪影）==", flush=True)
ms = [512, 1024]
ws = [0.010, 0.020, 0.0265, 0.040, 0.050]
C13 = -13.0/128.0
D   = -0.020597
inv56 = 1.0/56.0

for m in ms:
    cl = closed_1B(m)
    pred = inv56 + C13/m + D/m**2          # 171b 统一结构（无 κ 项）
    rows = []
    for w in ws:
        B = Bstar_spectral(-m, N=600, w=w)
        delta = cl - 1.0/B                 # 带符号 delta（171b 口径，恒正）
        kapp = (delta - pred)/m            # κ 投影
        rows.append((w, B, delta, kapp))
        print("  m=%5d w=%5.3f  B*=%.12f  delta=%.6e  κ_eff=%+.3e" % (m, w, B, delta, kapp), flush=True)
    kapps = np.array([r[3] for r in rows])
    print("  → m=%5d：κ_eff 均值 %+.3e，散布 %.2e（相对 %.1f%%）" % (
        m, kapps.mean(), kapps.std(), 100.0*kapps.std()/abs(kapps.mean())), flush=True)
print("判据：散布 < 20% → κ 真实结构（窗口不变）；散布 > 50% → 提取链窗口伪影", flush=True)
print("exit 0", flush=True)
