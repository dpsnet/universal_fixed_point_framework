# -*- coding: utf-8 -*-
"""
P7-5e-175: D/E 镜像结构母体判别
=================================
174e 锁定 δ(m) = 1/56 - 13/128/m - (103/5000)(1/m^2 - 1/m^3) + O(1/m^4)。
本步判别镜像 (1/m^2 - 1/m^3) 的展开母体：
  (A) (1/m^2 - 1/m^3) 自身是基本对象（截断展开，1/m^4 独立）
  (B) 1/(m(m+1)) = 1/m^2 - 1/m^3 + 1/m^4 - ...（望远镜差分母体，1/m^4 系数 = +D）
  (C) 1/(m^2-1) = 1/m^2 + 1/m^4 + ...（偶次展开，应无 E 项，预期被排除）
判别手段：
  1. 固定 C=13/128 下各母体固定 D 检验 RMS（103/5000 vs 41/2000 候选对照）
  2. 自由拟合各母体的 C/D 与 RMS
  3. +F/m^4 后 F 值判别：F≈0 → 母体精确；F≈+D → (B) 展开泄漏；(A) 独立项
  4. 残差形：r(m)=δ-1/56+13/128/m，r*m^3 vs m 线性拟合（(A): 严格直线截距+D斜率-D；
     (B): 带 -D/(m+1) 修正的可检曲率）
输出 63 点数据到 json 供后续复用。
"""
import numpy as np, json, os
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

def fit(delta, ms, cols):
    A = np.vstack(cols(ms)).T
    c, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
    resid = delta - A@c
    return c, float(np.sqrt(np.mean(resid**2)))

def fixed_rms(delta, ms, base):
    resid = delta - base
    return float(np.sqrt(np.mean(resid**2)))

print("== P7-5e-175 真实 Newton 63 点（m=33..1024 step 16）镜像母体判别 ==", flush=True)
msN = np.arange(33, 1025, 16, dtype=float)
dN = np.empty(len(msN))
for i, m in enumerate(msN):
    cl = closed_1B(int(m))
    B = Bstar_true(-int(m))
    dN[i] = cl - 1.0/B
    if i % 16 == 0:
        print("  m=%5d  delta=%.9e" % (int(m), dN[i]), flush=True)

out = {"m": msN.tolist(), "delta": dN.tolist(),
       "script": "_phase102_p7_5e175_mirror_mother.py"}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "_phase102_p7_5e175_delta63.json"), "w") as f:
    json.dump(out, f)
print("  saved _phase102_p7_5e175_delta63.json", flush=True)

# ---- 1. 固定 C=13/128 检验（零自由参数）----
print("\n-- 1. 固定 C=13/128，母体 × D 候选 RMS --")
Dcand = {"103/5000": 103.0/5000.0, "41/2000": 41.0/2000.0, "47/2500": 47.0/2500.0, "13/625": 13.0/625.0}
mothers = {
    "(1/m^2-1/m^3)": lambda m: (1.0/m**2 - 1.0/m**3),
    "1/(m(m+1))":    lambda m: 1.0/(m*(m+1.0)),
    "1/(m^2-1)":     lambda m: 1.0/(m*m - 1.0),
}
for mn, mf in mothers.items():
    for dn, dv in Dcand.items():
        base = inv56 + C13/msN + dv*mf(msN)
        rms = fixed_rms(dN, msN, base)
        print("   母体=%-12s D=%s  RMS=%.3e" % (mn, dn, rms))

# ---- 2. 自由拟合各母体 ----
print("\n-- 2. 自由拟合（C、D 自由）--")
cols_map = {
    "(1/m^2-1/m^3)": lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2 - 1.0/m**3],
    "1/(m(m+1))":    lambda m: [np.ones_like(m), 1.0/m, 1.0/(m*(m+1.0))],
    "1/(m^2-1)":     lambda m: [np.ones_like(m), 1.0/m, 1.0/(m*m - 1.0)],
}
for mn, cf in cols_map.items():
    c, rms = fit(dN, msN, cf)
    print("   母体=%-12s RMS=%.3e  C=%+.10f（13/128 差 %+.4f pct）  D=%+.7f（103/5000 差 %+.2f pct）" % (
        mn, rms, c[1], (c[1]-C13)/abs(C13)*100, c[2], (c[2]+0.0206)/0.0206*100))

# ---- 3. +F/m^4 判别 ----
print("\n-- 3. 高阶 1/m^4 判别 --")
c, rms = fit(dN, msN, lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3, 1.0/m**4])
print("   自由 5 参: RMS=%.3e  C=%+.10f  D=%+.7f  E=%+.7f  F=%+.7f" % (
    rms, c[1], c[2], c[3], c[4]))
print("   (B)预言 F=+D=+0.0206；(A)截断 F 独立")
c, rms = fit(dN, msN, lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2 - 1.0/m**3, 1.0/m**4])
print("   固定镜像+自由F: RMS=%.3e  C=%+.10f  D=%+.7f  F=%+.7f" % (rms, c[1], c[2], c[3]))
c, rms = fit(dN, msN, lambda m: [np.ones_like(m), 1.0/m, 1.0/(m*(m+1.0)), 1.0/m**4])
print("   固定1/(m(m+1))+自由F: RMS=%.3e  C=%+.10f  D=%+.7f  F=%+.7f" % (rms, c[1], c[2], c[3]))

# ---- 4. 残差形判别 ----
print("\n-- 4. 残差形：r(m)=δ-1/56+13/128/m，r*m^3 vs m --")
r = dN - inv56 - C13/msN
ym = r * msN**3
c, rms = fit(ym, msN, lambda m: [np.ones_like(m), m, 1.0/m])
print("   r*m^3 = a + b*m + g/m: a=%+.8f  b=%+.8f  g=%+.8f  RMS=%.3e" % (c[0], c[1], c[2], rms))
print("   (A)预言 a=+D=+0.0206, b=-D=-0.0206, g=0；(B)预言额外 -D/(m+1)~-D/m 曲率 g≈-D")
# 线性（无曲率）对照
c, rms = fit(ym, msN, lambda m: [np.ones_like(m), m])
print("   无曲率拟合: a=%+.8f  b=%+.8f  RMS=%.3e" % (c[0], c[1], rms))
print("exit 0", flush=True)
