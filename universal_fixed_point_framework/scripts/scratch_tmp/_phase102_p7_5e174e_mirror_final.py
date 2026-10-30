# -*- coding: utf-8 -*-
"""
P7-5e-174e: D/E 镜像结构终判——103/5000 双位置固定检验
======================================================
174d 揭示：真实 Newton 63 点全段拟合给出
  delta = 1/56 − 13/128/m − 0.02052/m² + 0.02024/m³（D≈−E≈103/5000）
候选结构：delta = 1/56 + C/m − (103/5000)(1/m² − 1/m³)
174e：固定系数检验（C=13/128、D=∓103/5000、E=±103/5000 组合），
判别镜像结构是否精确成立；w=0.0265 992 点跨通道复核。
"""
import numpy as np, json

inv56 = 1.0/56.0
C13 = 13.0/128.0
D5 = 103.0/5000.0

def rms_fixed(delta, ms, C, D, E):
    pred = inv56 + C/ms + D/ms**2 + E/ms**3
    return float(np.sqrt(np.mean((delta - pred)**2)))

def fit_free(delta, ms, ncols):
    A = np.vstack([1.0/ms**j for j in range(1, ncols+1)]).T
    A = np.hstack([np.ones((len(ms),1)), A])
    c, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
    resid = delta - A@c
    return c, float(np.sqrt(np.mean(resid**2)))

# 真实 Newton 63 点（174d 重算值已确认稳定——直接用 174d 的输出硬编码关键点不可行，需要全 63 点）
# 从 174c/174d 输出只有 4 个采样点——需要重新计算。为省时：直接用 delta 全序列（174c 脚本算出过，但没保存）。
# 方案：快速重算 63 点（~3 min 后台）——脚本自身带 Bstar_true。
print("== P7-5e-174e 镜像结构终判 ==", flush=True)
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

print("\n== 固定系数检验（真实 Newton 63 点）==")
print("  C=13/128, D=-103/5000, E=+103/5000（镜像结构） RMS=%.2e" % rms_fixed(dN, msN, -C13, -D5, +D5))
print("  C=13/128, D=-103/5000, E=0                RMS=%.2e" % rms_fixed(dN, msN, -C13, -D5, 0.0))
print("  C=13/128, D=0, E=+103/5000                RMS=%.2e" % rms_fixed(dN, msN, -C13, 0.0, +D5))
print("  C=13/128, D=-47/2500, E=+47/2500（旧候选） RMS=%.2e" % rms_fixed(dN, msN, -C13, -47.0/2500.0, 47.0/2500.0))

print("\n== C 自由、D/E 固定镜像 ==")
A = np.vstack([np.ones_like(msN), 1.0/msN]).T
rhs = dN - inv56 + D5/msN**2 - D5/msN**3
cc, _, _, _ = np.linalg.lstsq(A, rhs, rcond=None)
resid = rhs - A@cc
print("  C=%+.10f（13/128 差 %+.5f pct）  RMS=%.2e" % (cc[1], (cc[1]+C13)/C13*100, np.sqrt(np.mean(resid**2))))

print("\n== D、E 自由、C 固定镜像约束 D=-E ==")
# delta-1/56+C13/m = D*(1/m²-1/m³)
A2 = np.vstack([1.0/msN**2 - 1.0/msN**3]).T
rhs2 = dN - inv56 + C13/msN
c2, _, _, _ = np.linalg.lstsq(A2, rhs2, rcond=None)
resid2 = rhs2 - A2@c2
print("  D=%+.7f（103/5000 差 %+.2f pct）  RMS=%.2e" % (c2[0], (c2[0]+D5)/D5*100, np.sqrt(np.mean(resid2**2))))

# --- w=0.0265 992 点跨通道复核（固定模型）---
j = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e170_spectral_m1024.json", encoding='utf-8'))
out = j["out"]
m_pos = np.arange(33, 1025, dtype=float)
d_all = np.array([out[str(int(-m))]["delta"] for m in m_pos], dtype=float)
print("\n== 固定镜像结构跨通道复核（w=0.0265 992 点）==")
print("  C=13/128, D=-103/5000, E=+103/5000 全段   RMS=%.2e" % rms_fixed(d_all, m_pos, -C13, -D5, +D5))
print("  C=13/128, D=-103/5000, E=+103/5000 m>=128 RMS=%.2e" % rms_fixed(d_all[m_pos>=128], m_pos[m_pos>=128], -C13, -D5, +D5))
print("exit 0", flush=True)
