# -*- coding: utf-8 -*-
"""
P7-5e-134：E_0(B) 全程碗形扫描——消失点斜率 1/4 判别 + 碗形结构提取
=====================================================================
P7-5e-133 发现：dE_0/dB|_{B*} ≈ 1/4（与 m 无关）——E_0(B) 碗形（Larmor 线性降 + B²r²/8 曲率升）
P1 E_0(B) 全程扫描（B=0..1.15B*，40 点）：碗形形态
P2 极小值 (B_min, E_min) 定位 + E_0(0)（B=0 束缚能）
P3 B* 过零斜率精确判别（局部三次）：vs 1/4=2/k_max=α₀/2
P4 m=33/64/128 对照
"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

N_SP = 600

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
    """B 处的基态束缚能（最低负本征值，若无则最近 0 的本征值）"""
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
        return float(np.max(neg))  # 束缚态（最低负）
    # 无束缚：取最低正（连续谱底）
    pos = ev[ev >= 0]
    return float(pos.min()) if len(pos) else float(ev.min())

def analyze(m):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    Bc = 1.0/cl
    Bs = np.linspace(0.0, 1.15*Bc, 46)
    Es = np.array([E0_at(b, m) for b in Bs])
    # E0(0)：B 最小点（>0 但接近 0）
    E0_0 = Es[0] if Bs[0] == 0 else None
    # 极小值（碗底）
    imin = int(np.argmin(Es))
    Bmin, Emin = Bs[imin], Es[imin]
    # 过零：E_0(B*) 用线性插值最近 0 的两点
    i0 = np.argmin(np.abs(Es))
    # 找 E 跨 0
    idx = np.where(Es[:-1]*Es[1:] <= 0)[0]
    Bstar = None; slope = None
    for i in idx:
        if Es[i] < 0 and Es[i+1] > 0 and Bs[i] > Bmin:
            Bstar = Bs[i] - Es[i]*(Bs[i+1]-Bs[i])/(Es[i+1]-Es[i])
            # 局部斜率：用 Bstar 两侧各 2 点三次拟合
            jm = max(0, i-2); jp = min(len(Bs)-1, i+3)
            X = Bs[jm:jp+1]; Y = Es[jm:jp+1]
            A = np.vstack([np.ones_like(X), X-X.mean(), (X-X.mean())**2]).T
            c, _, _, _ = np.linalg.lstsq(A, Y, rcond=None)
            slope = c[1]
            break
    return dict(m=m, Bc=Bc, Bs=Bs, Es=Es, E0_0=E0_0, Bmin=float(Bmin), Emin=float(Emin),
                Bstar=float(Bstar) if Bstar else None, slope=float(slope) if slope is not None else None,
                n_bind=len(Bs[Es < 0]))

print("=== P7-5e-134 E_0(B) 全程碗形扫描 ===", flush=True)
for m in (-33, -64, -128):
    res = analyze(m)
    print("m=%3d：Bc=%.6f、E_0(0)=%.6f、碗底 (B_min=%.6f, E_min=%.6f)、B*=%.6f、dE/dB|_{B*}=%.6f（1/4=0.2500，dev %+.3f pct）、束缚区宽度=%.2f pct" % (
        res["m"], res["Bc"], res["E0_0"], res["Bmin"], res["Emin"], res["Bstar"],
        res["slope"], (res["slope"]-0.25)/0.25*100.0, 100.0*res["n_bind"]/len(res["Bs"])), flush=True)
    # 碗形关键点输出
    E = res["Es"]; B = res["Bs"]
    print("   E_0(B) 采样：B=0: %.4f、0.25Bc: %.4f、0.5Bc: %.4f、0.75Bc: %.4f、Bc: %.4f、1.15Bc: %.4f" % (
        E[0], E[np.argmin(np.abs(B-0.25*res["Bc"]))], E[np.argmin(np.abs(B-0.5*res["Bc"]))],
        E[np.argmin(np.abs(B-0.75*res["Bc"]))], E[np.argmin(np.abs(B-res["Bc"]))], E[-1]), flush=True)
print("exit 0", flush=True)
