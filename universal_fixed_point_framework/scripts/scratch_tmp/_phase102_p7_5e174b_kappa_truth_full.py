# -*- coding: utf-8 -*-
"""
P7-5e-174b: κ·m 真实结构终判 + D 身份判别（真实 Newton 全段 + w=0.0265 全链并排）
================================================================================
174 关键发现（真实 Newton 17 点，含常数+κ 模型）：
  C = −0.101656（13/128 差 −0.092%）、D ≈ +0.00016（≈0！）、κ = +2.378e-9、RMS 9.2e-10
→ κ·m 真实（非 172 判读的伪影）；但 D ≈ 0 与 171b（w=0.0265 992 点）的 D = −0.0206 冲突！
174b：真实 Newton 扩展到 m=384..1024（21 点）重算，与 w=0.0265 992 点并排拟合，
判别：D 是真实（≈103/5000？）还是 w=0.0265 提取伪影投影（真实 Newton 下 D→0）？
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
        e_plus = np.real(eig(T + np.diag(V_eff(r_in, float(B+h), m)), check_finite=False)[0])
        e_minus = np.real(eig(T + np.diag(V_eff(r_in, float(B-h), m)), check_finite=False)[0])
        cand_p = e_plus[(e_plus > -1.0) & (e_plus < 1.0)]
        cand_m = e_minus[(e_minus > -1.0) & (e_minus < 1.0)]
        e0 = np.real(eig(T + np.diag(V_eff(r_in, float(B), m)), check_finite=False)[0])
        e0 = e0[(e0 > -1.0) & (e0 < 1.0)].min()
        de = (cand_p.min() - cand_m.min()) / (2.0*h)
        if not np.isfinite(de) or de == 0.0:
            break
        dB = -e0 / de
        B = B + dB
        if abs(dB) < 1e-15*abs(B):
            break
    return B

C13 = -13.0/128.0
Dcan = -103.0/5000.0
inv56 = 1.0/56.0

def fit(delta, ms, model):
    A = np.vstack(model(ms)).T
    c, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
    resid = delta - A@c
    return c, float(np.sqrt(np.mean(resid**2)))

models = {
    "1+C/m+D/m²":        lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2],
    "1+C/m+D/m²+κ·m":    lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, m],
    "1+C/m+D/m²+E/m³+κ·m": lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3, m],
}

def report(name, delta, ms):
    print("\n== %s（%d 点）==" % (name, len(ms)))
    for mn, bf in models.items():
        c, rms = fit(delta, ms, bf)
        txt = "  %-24s RMS=%.2e  C=%+.9f（13/128 差 %+.4f pct）  D=%+.7f（103/5000 差 %+.2f pct）" % (
            mn, rms, c[1], (c[1]-C13)/abs(C13)*100, c[2], (c[2]-Dcan)/abs(Dcan)*100)
        if len(c) >= 4 and mn != "1+C/m+D/m²":
            txt += "  κ=%+.3e" % c[3]
        if len(c) >= 5:
            txt += "  E=%+.4f" % c[4]
        print(txt)

# --- 真实 Newton：m=384..1024 step 32（21 点）---
print("== 真实 Newton 重算（m=384..1024 step 32，21 点）==", flush=True)
msN = np.arange(384, 1025, 32, dtype=float)
dN = np.empty(len(msN))
for i, m in enumerate(msN):
    cl = closed_1B(int(m))
    B = Bstar_true(-int(m))
    dN[i] = cl - 1.0/B
    print("  m=%5d  delta=%.9e" % (int(m), dN[i]), flush=True)
report("真实 Newton", dN, msN)

# --- w=0.0265 全链（170 JSON）---
j = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e170_spectral_m1024.json", encoding='utf-8'))
out = j["out"]
m_pos = np.arange(33, 1025, dtype=float)
d_all = np.array([out[str(-m)]["delta"] for m in m_pos], dtype=float)   # 键是负 m 字符串
report("w=0.0265 全链", d_all, m_pos)
report("w=0.0265 m>=512", d_all[m_pos >= 512], m_pos[m_pos >= 512])

# --- 三通道 κ/D 对比 ---
print("\n== 模型 1+C/m+D/m²+κ·m 三通道对比 ==")
for name, delta, ms in [("真实 Newton(21p)", dN, msN), ("w=0.0265 全链(992p)", d_all, m_pos), ("w=0.0265 m>=512", d_all[m_pos>=512], m_pos[m_pos>=512])]:
    c, rms = fit(delta, ms, models["1+C/m+D/m²+κ·m"])
    print("  %-20s C=%+.9f  D=%+.7f  κ=%+.4e  RMS=%.2e" % (name, c[1], c[2], c[3], rms))
print("exit 0", flush=True)
