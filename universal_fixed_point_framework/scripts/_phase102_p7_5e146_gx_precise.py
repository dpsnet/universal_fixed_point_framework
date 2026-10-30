# -*- coding: utf-8 -*-
"""
P7-5e-146：g(x) 精确形态——两档 Richardson 外推 + 系数身份判别
================================================================
145 提取 g(x) 含 h(x)/m 残差（三档差 ~0.002）。本步：
P1 三档（33/64/128）40 点中区 g(x)，两档外推 → g_∞(x)（消 1/m 残差）
P2 g_∞(x) = a + b√x + c·x 精确拟合（残差 + 系数）
P3 √x 系数身份判别：0.09=3²/10² / 1/(4√2)=0.0884 / √2/16=0.0884 / (√2+1)/16
P4 g_∞(2) 精确值 vs 1/8
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

print("=== P7-5e-146 g(x) 精确形态 ===", flush=True)
ms = [-33, -64, -128]
xs = np.linspace(0.5, 2.6, 40)
gs = {}
for m in ms:
    Bs = xs / abs(m)
    Es = np.array([E0_at(b, m) for b in Bs])
    y = Es*abs(m)
    gs[m] = (y - f_model(xs)) * abs(m)
    print("m=%4d：40 点完成" % abs(m), flush=True)

print("--- P1 两档外推 g_∞(x) ---", flush=True)
# Richardson：g(m) = g_inf + h/m → 用 (33,64) 与 (64,128) 两对分别外推
g_64 = (64.0*gs[-64] - 33.0*gs[-33]) / (64.0 - 33.0)
g_128 = (128.0*gs[-128] - 64.0*gs[-64]) / (128.0 - 64.0)
print("  外推对 (33,64) vs (64,128) 一致性（应近似相等，残差 = h₂/m² 级）：", flush=True)
print("  最大差 = %.3e" % np.max(np.abs(g_64 - g_128)), flush=True)

print("--- P2 g_∞(x) = a + b√x + c·x 拟合（用 (64,128) 档）---", flush=True)
A = np.vstack([np.ones_like(xs), np.sqrt(xs), xs]).T
c3, _, _, _ = np.linalg.lstsq(A, g_128, rcond=None)
r3 = np.sum((g_128 - A@c3)**2)
print("  a=%.8f（vs −1/8=−0.125）、b=%.8f、c=%.8f（vs 1/16=0.0625）、残差 %.3e" % (
    c3[0], c3[1], c3[2], r3), flush=True)

print("--- P3 系数身份判别 ---", flush=True)
cands = {
    "0.09=3²/10²": 0.09,
    "1/(4√2)=0.088388": 1.0/(4.0*np.sqrt(2)),
    "√2/16=0.088388": np.sqrt(2.0)/16.0,
    "(√2+1)/16=0.1509": (np.sqrt(2.0)+1.0)/16.0,
    "0.089=89/1000": 0.089,
    "1/(√2·8)=0.08839": 1.0/(np.sqrt(2.0)*8.0),
    "9/100.4≈0.08964": 0.08964,
}
for name, v in cands.items():
    print("  b=%s：差 %+.6f（%+.2f%%）" % (name, c3[1]-v, (c3[1]/v-1)*100), flush=True)
# c 身份
print("  c vs 1/16=0.0625：差 %+.6f（%+.3f%%）" % (c3[2]-0.0625, (c3[2]/0.0625-1)*100), flush=True)
print("  c vs 1/15=0.06667：差 %+.6f" % (c3[2]-1.0/15.0), flush=True)

print("--- P4 g_∞(2) vs 1/8 ---", flush=True)
g2_128 = float(np.interp(2.0, xs, g_128))
g2_64 = float(np.interp(2.0, xs, g_64))
print("  g_∞(2)（64 档外推）= %.8f、g_∞(2)（128 档）= %.8f、vs 1/8=0.125（差 %+.6f）" % (
    g2_64, g2_128, g2_128-0.125), flush=True)
print("exit 0", flush=True)
