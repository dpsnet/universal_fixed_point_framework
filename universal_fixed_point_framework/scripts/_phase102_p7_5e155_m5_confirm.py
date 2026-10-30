# -*- coding: utf-8 -*-
"""
P7-5e-155：m=5 位点独立确认（谱方法通道——独立于 tridiag）
149/151 观察：δ_cl 在 m=5 有 3 倍跳跃（4.4e-4→1.36e-3），δ_cl/pred 突跳 0.317→0.676。
用 Chebyshev 谱方法（N=800，142 范式）重算 m=-5 的 B* 高精度：
若谱方法 B* 与 tridiag 一致 → m=5 跳跃真实（物理结构位点 2²+1² 候选）
若不一致 → 数据伪影（tridiag 通道问题）
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

def x0_cubic(xa, ya, xb, yb, xc, yc, xd, yd):
    A = np.vstack([np.ones(4), [xa, xb, xc, xd], [xa**2, xb**2, xc**2, xd**2],
                   [xa**3, xb**3, xc**3, xd**3]]).T
    cc, _, _, _ = np.linalg.lstsq(A, [ya, yb, yc, yd], rcond=None)
    roots = np.roots([cc[3], cc[2], cc[1], cc[0]])
    real = [r.real for r in roots if abs(r.imag) < 1e-10 and 0.5 <= r.real <= 3.0]
    if not real:
        return None
    return min(real, key=lambda v: abs(v - xb))

print("=== P7-5e-155 m=5 位点独立确认 ===", flush=True)
m = -5
cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
Bc = 1.0/cl
print("闭式 1/B* = %.9f（Bc = %.9f）" % (cl, Bc), flush=True)
# 粗扫
Bs = np.linspace(0.0, 1.3*Bc, 60)
Es = np.array([E0_at(b, m) for b in Bs])
x = Bs*abs(m); y = Es*abs(m)
idx = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
i = idx[-1]
b_lo = Bs[max(0, i-1)]; b_hi = Bs[min(len(Bs)-1, i+1)]
# 加密 ±0.5%
Bf = np.linspace(0.995*b_lo, 1.005*b_hi, 120)
Ef = np.array([E0_at(b, m) for b in Bf])
xf = Bf*abs(m); yf = Ef*abs(m)
idx2 = np.where((yf[:-1] < 0) & (yf[1:] >= 0))[0]
j = idx2[-1]
x0 = x0_cubic(xf[j-1], yf[j-1], xf[j], yf[j], xf[j+1], yf[j+1], xf[j+2], yf[j+2])
invB = abs(m)/x0
delta_cl = cl - invB
geom = 1.0/(7.0*2.0**abs(m))
print("谱方法：x0=%.10f、1/B*=%.10f、δ_cl=%+.3e、1/(7·2^m)=%.3e、δ_cl/geom=%.3f" % (
    x0, invB, delta_cl, geom, delta_cl/geom), flush=True)
print("tridiag（151）：1/B*=2.645963518、δ_cl=+1.358e-3、δ_cl/geom=0.304", flush=True)
print("谱方法 vs tridiag：差 = %.3e" % (invB - 2.645963518), flush=True)
# 相对 1/B*（闭式）的相对误差
print("闭式相对误差：谱 %.5f%% vs tridiag %.5f%%" % (
    abs(delta_cl)/cl*100, abs(1.358e-3)/cl*100), flush=True)
print("exit 0", flush=True)
