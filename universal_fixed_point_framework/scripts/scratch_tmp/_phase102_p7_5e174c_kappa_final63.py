# -*- coding: utf-8 -*-
"""
P7-5e-174c: 真实 Newton 63 点终判——κ/D 定案 + C 确认 + D 候选判别
=================================================================
174b（负 m 正确通道，21 点）：κ≈0（172 伪影判读正确）、C=13/128（+0.012%）、
D=−0.0236（103/5000 差 −14.7%）——但 21 点 D 不稳（含 E 后爆炸）。
174c：真实 Newton m=33..1024 step 16（63 点）——统计足够，判别：
  - κ 是否 ≈0（伪影终判）
  - C 是否 = 13/128（三通道+真实提取确认）
  - D 精确值（103/5000=0.0206 vs 47/2500=0.0188 vs 新值）
"""
import numpy as np, json
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

def Bstar_true(m, N=600, w=0.0265, newton_steps=3, h_rel=1e-5):
    cl = closed_1B(m)
    Bc = 1.0/cl
    x, D1, D2 = cheb_d1d2(N)
    a, b = 0.23*abs(m), 3.1*abs(m)
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = (-0.5 * D2 / (scale*scale))[1:-1, 1:-1]
    r_in = r[1:-1]
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    Es = np.empty(7)
    for i, B in enumerate(Bs):
        H = T + np.diag(V_eff(r_in, float(B), m))
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
    B = B0 + xx
    for _ in range(newton_steps):
        h = h_rel * abs(B)
        e_p = np.real(eig(T + np.diag(V_eff(r_in, float(B+h), m)), check_finite=False)[0])
        e_m = np.real(eig(T + np.diag(V_eff(r_in, float(B-h), m)), check_finite=False)[0])
        e_0 = np.real(eig(T + np.diag(V_eff(r_in, float(B), m)), check_finite=False)[0])
        cp = e_p[(e_p > -1.0) & (e_p < 1.0)]; cm = e_m[(e_m > -1.0) & (e_m < 1.0)]
        c0v = e_0[(e_0 > -1.0) & (e_0 < 1.0)]
        if len(cp) == 0 or len(cm) == 0 or len(c0v) == 0:
            break
        de = (cp.min() - cm.min()) / (2.0*h)
        if not np.isfinite(de) or de == 0.0:
            break
        dB = -c0v.min() / de
        B = B + dB
        if abs(dB) < 1e-15*abs(B):
            break
    return B

C13 = -13.0/128.0
inv56 = 1.0/56.0

def fit(delta, ms, model):
    A = np.vstack(model(ms)).T
    c, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
    resid = delta - A@c
    return c, float(np.sqrt(np.mean(resid**2)))

print("== P7-5e-174c 真实 Newton m=33..1024 step 16（63 点）==", flush=True)
msN = np.arange(33, 1025, 16, dtype=float)
dN = np.empty(len(msN))
for i, m in enumerate(msN):
    cl = closed_1B(int(m))
    B = Bstar_true(-int(m))
    dN[i] = cl - 1.0/B
    if i % 16 == 0:
        print("  m=%5d  delta=%.9e" % (int(m), dN[i]), flush=True)

models = {
    "1+C/m+D/m²":         lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2],
    "1+C/m+D/m²+E/m³":    lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3],
    "1+C/m+D/m²+κ·m":     lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, m],
    "1+C/m+D/m²+E/m³+κ·m": lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3, m],
}
for mn, bf in models.items():
    c, rms = fit(dN, msN, bf)
    txt = "  %-22s RMS=%.2e  C=%+.10f（13/128 差 %+.5f pct）  D=%+.7f（103/5000 差 %+.2f pct）" % (
        mn, rms, c[1], (c[1]-C13)/abs(C13)*100, c[2], (c[2]+103.0/5000.0)/abs(103.0/5000.0)*100)
    if len(c) >= 4:
        txt += "  %s=%+.4e" % ("κ" if "κ" in mn else "E", c[3])
    if len(c) >= 5:
        txt += "  E=%+.4e" % c[4]
    print(txt)

print("\n== 分段稳定性（1+C/m+D/m²）==")
for lo in [128, 256, 384, 512, 640, 768, 896]:
    sel = msN >= lo
    c, rms = fit(dN[sel], msN[sel], models["1+C/m+D/m²"])
    print("  m>=%4d（%3d 点）C=%+.10f（13/128 差 %+.5f pct）  D=%+.7f（103/5000 差 %+.2f pct）  RMS=%.2e" % (
        lo, sel.sum(), c[1], (c[1]-C13)/abs(C13)*100, c[2], (c[2]+0.0206)/0.0206*100, rms))
print("exit 0", flush=True)
