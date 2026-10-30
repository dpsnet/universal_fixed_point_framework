# -*- coding: utf-8 -*-
"""
P7-5e-174d: E（1/m³）项真伪判别 + D=103/5000 跨通道复核
=====================================================
174c 63 点真实 Newton：+E/m³ 模型 C=13/128（+0.00015%）、D=−0.02052（103/5000 +0.37%）、
E=+0.0202≈−D。判别 E 是否真实（加 F/m⁴ 看 E/D 漂移），并 w=0.0265 992 点并排复核。
"""
import numpy as np, json

C13 = -13.0/128.0
inv56 = 1.0/56.0

def fit(delta, ms, model):
    A = np.vstack(model(ms)).T
    c, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
    resid = delta - A@c
    return c, float(np.sqrt(np.mean(resid**2)))

models = {
    "1+C/m+D/m²":           lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2],
    "1+C/m+D/m²+E/m³":      lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3],
    "1+C/m+D/m²+E/m³+F/m⁴": lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3, 1.0/m**4],
    "1+C/m+D/m²+E/m³+F/m⁴+G/m⁵": lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3, 1.0/m**4, 1.0/m**5],
}

def report(name, delta, ms):
    print("\n== %s（%d 点）==" % (name, len(ms)))
    for mn, bf in models.items():
        c, rms = fit(delta, ms, bf)
        txt = "  %-24s RMS=%.2e  C=%+.10f（13/128 差 %+.5f pct）  D=%+.7f（103/5000 差 %+.2f pct）" % (
            mn, rms, c[1], (c[1]-C13)/abs(C13)*100, c[2], (c[2]+0.0206)/0.0206*100)
        if len(c) >= 4:
            txt += "  E=%+.5f" % c[3]
        if len(c) >= 5:
            txt += "  F=%+.4f" % c[4]
        if len(c) >= 6:
            txt += "  G=%+.3f" % c[5]
        print(txt)

# --- 真实 Newton 63 点（174c 输出已算，重算成本 ~3 分钟；直接复用硬编码关键点 + 重算剩余？不，直接重算太慢，从 174c 输出取——需要全部 63 点。这里重算 63 点（后台 ~3 min）--->
print("== 重算真实 Newton 63 点 ==", flush=True)
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

msN = np.arange(33, 1025, 16, dtype=float)
dN = np.empty(len(msN))
for i, m in enumerate(msN):
    cl = closed_1B(int(m))
    B = Bstar_true(-int(m))
    dN[i] = cl - 1.0/B
    if i % 16 == 0:
        print("  m=%5d  delta=%.9e" % (int(m), dN[i]), flush=True)

report("真实 Newton 全段", dN, msN)
report("真实 Newton m>=128", dN[msN>=128], msN[msN>=128])

# --- w=0.0265 992 点（170 JSON，int 键）---
j = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e170_spectral_m1024.json", encoding='utf-8'))
out = j["out"]
m_pos = np.arange(33, 1025, dtype=float)
d_all = np.array([out[str(int(-m))]["delta"] for m in m_pos], dtype=float)
report("w=0.0265 全链", d_all, m_pos)
report("w=0.0265 m>=128", d_all[m_pos>=128], m_pos[m_pos>=128])
report("w=0.0265 m>=512", d_all[m_pos>=512], m_pos[m_pos>=512])
print("exit 0", flush=True)
