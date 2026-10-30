# -*- coding: utf-8 -*-
"""
P7-5e-155b：小 m 全线谱方法重算（m=1..14——δ_cl 通道无关值）
每 m：粗扫定位 → ±0.5% 加密 100 点 → 三次插值过零 → 1/B*、δ_cl、δ_cl/geom
对比 tridiag（151）差值 → tridiag 系统偏差的 m 分布
"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache
import json

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

# tridiag 参考值（151）
tri = {1: 0.729654550, 2: 1.178370130, 3: 1.660359892, 4: 2.151343797,
       5: 2.645963518, 6: 3.142397790, 7: 3.639864169, 8: 4.137972416,
       9: 4.636506585, 10: 5.135337668, 11: 5.634383915, 12: 6.133590925,
       13: 6.632921364, 14: 7.132348484}

print("m\t1/B*_spec\tdelta_cl_spec\tdelta/geom\ttri_delta\ttri−spec", flush=True)
out = {}
for m in range(1, 15):
    cl = m/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**m)
    Bc = 1.0/cl
    Bs = np.linspace(0.0, 1.3*Bc, 60)
    Es = np.array([E0_at(b, -m) for b in Bs])
    x = Bs*m; y = Es*m
    idx = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    if len(idx) == 0:
        # 兜底：更细全区间扫描
        Bs = np.linspace(0.0, 1.5*Bc, 150)
        Es = np.array([E0_at(b, -m) for b in Bs])
        x = Bs*m; y = Es*m
        idx = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    if len(idx) == 0:
        print("m=%d：未找到过零（B 区间 0..%.4f）" % (m, 1.5*Bc), flush=True)
        continue
    i = idx[-1]
    b_lo = Bs[max(0, i-1)]; b_hi = Bs[min(len(Bs)-1, i+1)]
    Bf = np.linspace(0.995*b_lo, 1.005*b_hi, 100)
    Ef = np.array([E0_at(b, -m) for b in Bf])
    xf = Bf*m; yf = Ef*m
    idx2 = np.where((yf[:-1] < 0) & (yf[1:] >= 0))[0]
    j = idx2[-1]
    x0 = x0_cubic(xf[j-1], yf[j-1], xf[j], yf[j], xf[j+1], yf[j+1], xf[j+2], yf[j+2])
    invB = m/x0
    dcl = cl - invB
    geom = 1.0/(7.0*2.0**m)
    tri_d = tri.get(m, float('nan'))
    diff = tri_d - invB if m in tri else float('nan')
    print("%d\t%.9f\t%+.3e\t%.4f\t%.3e\t%+.3e" % (m, invB, dcl, dcl/geom, tri_d-cl if False else dcl, diff), flush=True)
    out[m] = {"invB_spec": invB, "delta_cl": dcl, "tri_invB": tri.get(m), "diff": diff}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e155b_smallm_spec.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("saved", flush=True)
