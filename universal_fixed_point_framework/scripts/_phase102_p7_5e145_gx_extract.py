# -*- coding: utf-8 -*-
"""
P7-5e-145：g(x) 数值提取——E_0·|m| 的 1/m 修正系数形态
================================================================
142 锁定 f(x) = x/2 − sqrt(x/2)（渐近）。真实 E_0·|m| = f(x) + g(x)/m + ...
144 锁定 C = g(2) = 0.1016（过零处 1/m 修正）。
谐振子变分给出 g(x) = −1/8（常数，符号相反）——需数值提取真实 g(x)：
P1 中区逐点 E_0·|m| − f(x)，×m → g(x)（m=33/64/128 三档塌缩检验）
P2 g(x) 形态判别（常数 / √x / 线性 / 反比）
P3 g(2) 值 vs C = 0.1016 与 −1/8
"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

N_SP = 800

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

def f_model(x):
    return 0.5*x - np.sqrt(0.5*x)

print("=== P7-5e-145 g(x) 数值提取 ===", flush=True)
ms = [-33, -64, -128]
xs = np.linspace(0.35, 2.6, 24)
gs = {}
for m in ms:
    cl = abs(m)/2.0 + 1.0/8.0
    Bc = 1.0/cl
    Bs = xs / abs(m)   # x = B*|m| → B = x/|m|
    Es = np.array([E0_at(b, m) for b in Bs])
    y = Es*abs(m)
    g = (y - f_model(xs)) * abs(m)
    gs[m] = g
    print("m=%4d：24 点完成" % m, flush=True)

print("--- P1/P2 g(x) 三档对比（塌缩检验）---", flush=True)
hdr = "  x     " + "".join("g(m=%4d)" % abs(m) for m in ms)
print(hdr, flush=True)
for k in range(len(xs)):
    row = "%.4f  " % xs[k] + "  ".join("%9.6f" % gs[m][k] for m in ms)
    print(row, flush=True)
# g(2) 插值
g2 = {}
for m in ms:
    g2[m] = float(np.interp(2.0, xs, gs[m]))
    print("  g(2)（m=%4d）= %.6f（vs C=0.1016、−1/8=−0.125）" % (abs(m), g2[m]), flush=True)

print("--- P3 形态判别 ---", flush=True)
# 尝试 g(x) = a + b*sqrt(x)、a + b*x、a/x + b 拟合（用 m=128 最精确档）
g = gs[-128]
A1 = np.vstack([np.ones_like(xs), np.sqrt(xs)]).T
c1, _, _, _ = np.linalg.lstsq(A1, g, rcond=None)
r1 = np.sum((g - A1@c1)**2)
A2 = np.vstack([np.ones_like(xs), xs]).T
c2, _, _, _ = np.linalg.lstsq(A2, g, rcond=None)
r2 = np.sum((g - A2@c2)**2)
A3 = np.vstack([np.ones_like(xs), 1.0/xs]).T
c3, _, _, _ = np.linalg.lstsq(A3, g, rcond=None)
r3 = np.sum((g - A3@c3)**2)
A4 = np.vstack([np.ones_like(xs), np.sqrt(xs), xs]).T
c4, _, _, _ = np.linalg.lstsq(A4, g, rcond=None)
r4 = np.sum((g - A4@c4)**2)
print("  a+b√x：a=%.5f b=%.5f 残差 %.3e" % (c1[0], c1[1], r1), flush=True)
print("  a+b·x：a=%.5f b=%.5f 残差 %.3e" % (c2[0], c2[1], r2), flush=True)
print("  a+b/x：a=%.5f b=%.5f 残差 %.3e" % (c3[0], c3[1], r3), flush=True)
print("  a+b√x+cx：a=%.5f b=%.5f c=%.5f 残差 %.3e" % (c4[0], c4[1], c4[2], r4), flush=True)
print("exit 0", flush=True)
