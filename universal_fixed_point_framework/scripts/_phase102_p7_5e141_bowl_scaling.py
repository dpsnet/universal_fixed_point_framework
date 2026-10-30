# -*- coding: utf-8 -*-
"""
P7-5e-141：碗形普适标度塌缩判别
================================================================
134/135/138：E_min·|m|→−1/4、B_min=B*/4、过零斜率→1/4 均与 m 无关——
  碗形是否普适标度曲线 E_0(B)·|m| = f(B·|m|)？
P1 m=33/64/128 全程碗形（0..1.15Bc 120 点）
P2 塌缩检验：E_0(B)·|m| vs B·|m| 三点是否重合（残差）
P3 标度函数特征：过零斜率（vs B·|m| 轴）、碗底位置/深度
"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

N_SP = 500

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

print("=== P7-5e-141 碗形普适标度塌缩 ===", flush=True)
ms = [-33, -64, -128]
npt = 120
res = {}
for m in ms:
    cl = abs(m)/2.0 + 1.0/8.0  # 大 m 渐近闭式（1/k_max 截距）
    Bc = 1.0/cl
    Bs = np.linspace(0.0, 1.15*Bc, npt)
    Es = np.array([E0_at(b, m) for b in Bs])
    res[m] = (Bs, Es)
    print("m=%3d：碗形 120 点完成" % m, flush=True)

# P1 标度量
print("--- P1 标度量（E_0·|m| vs B·|m|）---", flush=True)
for m in ms:
    Bs, Es = res[m]
    x = Bs*abs(m)
    y = Es*abs(m)
    # 过零
    idx = np.where(np.sign(y[:-1]) != np.sign(y[1:]))[0]
    x0 = None
    if len(idx):
        i = idx[0]
        x0 = x[i] - y[i]*(x[i+1]-x[i])/(y[i+1]-y[i])
    # 碗底（抛物插值）
    i0 = int(np.argmin(y))
    lo, hi = max(0, i0-1), min(len(x)-1, i0+1)
    xx = x[lo:hi+1]; yy = y[lo:hi+1]
    A = np.vstack([np.ones_like(xx), xx, xx**2]).T
    cc, _, _, _ = np.linalg.lstsq(A, yy, rcond=None)
    xmin = -cc[1]/(2*cc[2]); ymin = cc[0]+cc[1]*xmin+cc[2]*xmin**2
    # 过零斜率（y 对 x 轴）
    i = idx[0]
    dy = y[i+1]-y[i]; dx = x[i+1]-x[i]
    slope = dy/dx
    print("  m=%3d：过零 x=%.6f（理论 2+1/4=2.25 渐近）、碗底 (x_min=%.5f, y_min=%.6f)、过零斜率 %.4f" % (
        m, x0, xmin, ymin, slope), flush=True)

print("--- P2 塌缩残差（三点 vs 均值）---", flush=True)
# 取公共 x 网格比较
import numpy as np
x_all = np.linspace(0.4, 2.6, 60)
ys = {}
for m in ms:
    Bs, Es = res[m]
    x = Bs*abs(m); y = Es*abs(m)
    ys[m] = np.interp(x_all, x, y)
mean = np.mean(list(ys.values()), axis=0)
for m in ms:
    dev = np.max(np.abs(ys[m]-mean))
    rel = dev/max(abs(mean).max(), 1e-9)
    print("  m=%3d：最大塌缩残差 %.6f（相对 %.2f pct）" % (m, dev, rel*100.0), flush=True)
print("  三点均值曲线特征：过零斜率、碗底——若残差 <1e-3 级 → 普适标度成立", flush=True)
print("exit 0", flush=True)
