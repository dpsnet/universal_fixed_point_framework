# -*- coding: utf-8 -*-
"""
P7-5e-142：普适曲线解析形式验证——f(x) = x/2 − sqrt(x/2)
================================================================
141 发现碗形普适标度 E_0(B)·|m| = f(B·|m|)。势阱标度分析（离心-抗磁平衡）给出
解析候选 f(x) = x/2 − sqrt(x/2)——四个特征量全是代数推论：
  碗底位置 f'(x)=0 → x=1/2；碗底深度 f(1/2)=−1/4
  过零 f(x)=0 → x=2；过零斜率 f'(2)=+1/4
P1 高精度碗形（N=800，150 点）m=33/64/128/256
P2 f(x) 模型残差（碗底+过零区）
P3 过零位置 B*·|m| vs 2（修正 2−1/(2m) 检验）
P4 E_0(0)·|m| m 依赖量化（极低 B 区）
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

print("=== P7-5e-142 普适曲线解析形式验证 ===", flush=True)
ms = [-33, -64, -128, -256]
npt = 150
res = {}
for m in ms:
    cl = abs(m)/2.0 + 1.0/8.0
    Bc = 1.0/cl
    Bs = np.linspace(0.0, 1.15*Bc, npt)
    Es = np.array([E0_at(b, m) for b in Bs])
    res[m] = (Bs, Es)
    print("m=%4d：碗形 %d 点完成（N=800）" % (m, npt), flush=True)

print("--- P1 标度量（修正过零检测：负→正过零 = B*）---", flush=True)
for m in ms:
    Bs, Es = res[m]
    x = Bs*abs(m)
    y = Es*abs(m)
    idx = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    i = idx[-1]
    x0 = x[i] - y[i]*(x[i+1]-x[i])/(y[i+1]-y[i])
    slope = (y[i+1]-y[i])/(x[i+1]-x[i])
    i0 = int(np.argmin(y))
    lo, hi = max(0, i0-1), min(len(x)-1, i0+1)
    xx = x[lo:hi+1]; yy = y[lo:hi+1]
    A = np.vstack([np.ones_like(xx), xx, xx**2]).T
    cc, _, _, _ = np.linalg.lstsq(A, yy, rcond=None)
    xmin = -cc[1]/(2*cc[2]); ymin = cc[0]+cc[1]*xmin+cc[2]*xmin**2
    # f 模型残差
    ferr = np.max(np.abs(y - f_model(x)))  # 全曲线最大
    ferr_mid = np.max(np.abs(y[(x>0.35)&(x<2.6)] - f_model(x[(x>0.35)&(x<2.6)])))
    e0m = y[0]
    print("  m=%4d：过零 x0=%.6f（vs 2、修正 2−1/(2m)=%.6f）、斜率 %.4f（vs 1/4）" % (
        m, x0, 2.0-1.0/(2.0*abs(m)), slope), flush=True)
    print("        碗底 (%.5f, %.6f)（vs (0.5, −0.25)）；全曲线残差 %.6f；中区残差 %.6f；E_0(0)·|m|=%.5f" % (
        xmin, ymin, ferr, ferr_mid, e0m), flush=True)

print("--- P3 过零位置修正检验 ---", flush=True)
for m in ms:
    Bs, Es = res[m]
    x = Bs*abs(m); y = Es*abs(m)
    idx = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    i = idx[-1]
    x0 = x[i] - y[i]*(x[i+1]-x[i])/(y[i+1]-y[i])
    print("  m=%4d：B*·|m| = %.6f；2−1/(2m) = %.6f；差 = %+.6f；1/B* = %.8f vs |m|/2+1/8 = %.8f" % (
        m, x0, 2.0-1.0/(2.0*abs(m)), x0-(2.0-1.0/(2.0*abs(m))),
        abs(m)/x0, abs(m)/2.0+1.0/8.0), flush=True)

print("--- P4 E_0(0)·|m| 序列（m 依赖）---", flush=True)
for m in ms:
    Bs, Es = res[m]
    print("  m=%4d：E_0(0)=%.6f、E_0(0)·|m|=%.5f" % (m, Es[0], Es[0]*abs(m)), flush=True)
print("exit 0", flush=True)
