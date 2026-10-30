# -*- coding: utf-8 -*-
"""
P7-5e-148：C 精确判别——0.1016 vs 13/128（5-6 位精度）
================================================================
144：δ_1/8×m → 0.1016（4 位）；147：h(2) 外推 = 7/64 → C = h(2) − 1/128 = 13/128 = 0.1015625。
两候选差 3.7e-5——需 5-6 位精度判别。
P1 m=128/256 加密过零（±0.5% 窗口 300 点 + 三次插值）→ 1/B* 6-7 位
P2 C = (δ_1/8×m) 两点外推消 D/m → 5-6 位 C
P3 判别：0.1016 / 13/128 / (2^10−8)/10⁴=0.1016 / 其他框架候选
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

def x0_cubic(xa, ya, xb, yb, xc, yc, xd, yd):
    # 四点三次插值过零
    A = np.vstack([np.ones(4), [xa, xb, xc, xd], [xa**2, xb**2, xc**2, xd**2],
                   [xa**3, xb**3, xc**3, xd**3]]).T
    cc, _, _, _ = np.linalg.lstsq(A, [ya, yb, yc, yd], rcond=None)
    # 三次求根（0.8..2.5 区间）
    roots = np.roots([cc[3], cc[2], cc[1], cc[0]])
    real = [r.real for r in roots if abs(r.imag) < 1e-10 and 0.5 <= r.real <= 3.0]
    if not real:
        return None
    return min(real, key=lambda v: abs(v - xb))

print("=== P7-5e-148 C 精确判别 ===", flush=True)
ms = [-128, -256]
npt = 300
invBs = {}
for m in ms:
    cl = abs(m)/2.0 + 1.0/8.0
    Bc = 1.0/cl
    # 粗扫定位
    Bs = np.linspace(0.0, 1.15*Bc, 50)
    Es = np.array([E0_at(b, m) for b in Bs])
    x = Bs*abs(m); y = Es*abs(m)
    idx = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    i = idx[-1]
    b_lo = Bs[max(0, i-1)]; b_hi = Bs[min(len(Bs)-1, i+1)]
    # 加密 ±0.5%
    Bf = np.linspace(0.995*b_lo, 1.005*b_hi, npt)
    Ef = np.array([E0_at(b, m) for b in Bf])
    xf = Bf*abs(m); yf = Ef*abs(m)
    idx2 = np.where((yf[:-1] < 0) & (yf[1:] >= 0))[0]
    j = idx2[-1]
    if 1 <= j <= len(xf)-3:
        x0 = x0_cubic(xf[j-1], yf[j-1], xf[j], yf[j], xf[j+1], yf[j+1], xf[j+2], yf[j+2])
    else:
        x0 = xf[j] - yf[j]*(xf[j+1]-xf[j])/(yf[j+1]-yf[j])
    invB = abs(m)/x0
    invBs[m] = (invB, x0)
    d18 = invB - cl
    print("  m=%4d：x0=%.10f、1/B*=%.10f、δ_1/8=%.10f、δ_1/8×m=%.8f" % (
        m, x0, invB, d18, d18*abs(m)), flush=True)

print("--- P2 两点外推 C（消 D/m：C = (m₂δ₂ − m₁δ₁)/(m₂−m₁)）---", flush=True)
m1, m2 = abs(ms[0]), abs(ms[1])
d1 = invBs[ms[0]][0] - (m1/2.0 + 1.0/8.0)
d2 = invBs[ms[1]][0] - (m2/2.0 + 1.0/8.0)
C_ext = (m2*d2 - m1*d1) / (m2 - m1)
print("  C（外推）= %.8f" % C_ext, flush=True)
# 用单点 m2 加 D 估计：若 C=13/128，D 应 = (d2*256 − C)*256
D_est = (d2*m2 - 13.0/128.0)*m2
print("  若 C=13/128：D 应 = %.6f（vs 120 的 D≈0.0179）" % D_est, flush=True)

print("--- P3 候选判别 ---", flush=True)
cands = {
    "0.1016 = 127·8/10⁴": 0.1016,
    "13/128 = 0.1015625": 13.0/128.0,
    "(2^10−8)/10⁴": 0.1016,
    "7/64−1/128": 13.0/128.0,
    "0.1015625 = 13·2^-7": 13.0/128.0,
    "0.101604 = 65/640": 65.0/640.0,
}
for name, v in cands.items():
    print("  %s：差 %+.8f（%+.4f%%）" % (name, C_ext-v, (C_ext/v-1)*100), flush=True)
print("exit 0", flush=True)
