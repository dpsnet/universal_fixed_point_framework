# -*- coding: utf-8 -*-
"""
P7-5e-147：h(x) 提取——E_0·|m| 的 1/m² 修正系数（C 的真正来源）
================================================================
E_0·|m| = f(x) + g_∞(x)/m + h(x)/m² + ...
146 锁定 g_∞(x) = -1/8 + sqrt(x/2)/8 + x/16（机器精度）。
145 推导：C = h(2) - 3/256 → h(2) ≈ 0.1016 + 0.011719 ≈ 0.11332。
P1 三档（64/128/256）h(x) 提取（用 146 精确 g_∞ 代入）
P2 h(x) 形态判别（常数 / 线性 / √x / 组合）
P3 h(2) vs 0.11332 检验 + C 闭环验证
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

def g_inf(x):
    return -0.125 + np.sqrt(0.5*x)/8.0 + x/16.0

print("=== P7-5e-147 h(x) 提取 ===", flush=True)
ms = [-64, -128, -256]
xs = np.linspace(0.5, 2.6, 32)
hs = {}
for m in ms:
    Bs = xs / abs(m)
    Es = np.array([E0_at(b, m) for b in Bs])
    y = Es*abs(m)
    h = (y - f_model(xs) - g_inf(xs)/abs(m)) * abs(m)**2
    hs[m] = h
    print("m=%4d：32 点完成" % abs(m), flush=True)

print("--- P1 h(x) 三档对比（应近似一致，残差 = i(x)/m 级）---", flush=True)
for k in range(0, len(xs), 4):
    row = "x=%.4f: " % xs[k] + "  ".join("h=%9.6f" % hs[m][k] for m in ms)
    print(row, flush=True)

print("--- P2 形态判别（用 m=256 档）---", flush=True)
h = hs[-256]
A1 = np.vstack([np.ones_like(xs), xs]).T
c1, _, _, _ = np.linalg.lstsq(A1, h, rcond=None)
r1 = np.sum((h - A1@c1)**2)
A2 = np.vstack([np.ones_like(xs), np.sqrt(xs), xs]).T
c2, _, _, _ = np.linalg.lstsq(A2, h, rcond=None)
r2 = np.sum((h - A2@c2)**2)
A3 = np.vstack([np.ones_like(xs), np.sqrt(xs)]).T
c3, _, _, _ = np.linalg.lstsq(A3, h, rcond=None)
r3 = np.sum((h - A3@c3)**2)
print("  a+bx：a=%.6f b=%.6f 残差 %.3e" % (c1[0], c1[1], r1), flush=True)
print("  a+b√x+cx：a=%.6f b=%.6f c=%.6f 残差 %.3e" % (c2[0], c2[1], c2[2], r2), flush=True)
print("  a+b√x：a=%.6f b=%.6f 残差 %.3e" % (c3[0], c3[1], r3), flush=True)

print("--- P3 h(2) vs 0.11332 + C 闭环 ---", flush=True)
for m in ms:
    h2 = float(np.interp(2.0, xs, hs[m]))
    print("  h(2)（m=%4d）= %.6f（vs 0.11332 预测）；C_闭环 = h(2) − 3/256 = %.6f（vs 0.1016）" % (
        abs(m), h2, h2 - 3.0/256.0), flush=True)
print("exit 0", flush=True)
