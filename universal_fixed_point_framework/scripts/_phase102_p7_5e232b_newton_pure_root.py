# -*- coding: utf-8 -*-
"""
P7-5e-232b：三次拟合残差判别——高精度求根通道（Newton 细化）vs 三次拟合根
====================================================================
232 发现：高 m 段残差 r ∝ ~2.5-2.9e-9·m 线性（两求解器系数差 20%）。
判别实验：B* 的求根方式不同→线性残差是否变化：
  a) 三次拟合根（230c/227 现有 Bstar_spectral）——三次拟合外推
  b) Newton 细化（在三次拟合根上，对 N=1200 特征值 E(B) 做中心差分求根）
     ——收敛到 N=1200 数值系统的真实根（175 的机制，但 N=1200 离散化误差小）
先验：P1 Newton 细化版高 m 段 δ 相对三次拟合版变化 ~2.9e-9·m（线性）→ 三次拟合是来源；
  P2 变化 <20% → 线性残差独立于求根方式（物理/闭式结构）；
  P3 变化无规律 → 数值噪声。
"""
import time, json, os
import numpy as np
from scipy.linalg import eig

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
W = 0.0265
N_SP = 1200
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0
EPS_W = 0.215e-6

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
    am = abs(m)
    tiny = 1.0/(7.0*2.0**am) if am <= 1000 else 0.0
    return am/2.0 + 1.0/7.0 + tiny

def Bstar_spectral(m, N=N_SP, w=W):
    cl = closed_1B(m)
    Bc = 1.0/cl
    r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
    x, D1, D2 = cheb_d1d2(N)
    a, b = r_lo, r_hi
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5 * D2 / (scale*scale)
    r_in = r[1:-1]
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    Es = np.empty(7)
    for i, B in enumerate(Bs):
        H = T[1:-1, 1:-1] + np.diag(V_eff(r_in, float(B), m))
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
    return B0 + xx

def E0_at(B, m, N=N_SP):
    cl = closed_1B(m)
    Bc = 1.0/cl
    r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
    x, D1, D2 = cheb_d1d2(N)
    a, b = r_lo, r_hi
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5 * D2 / (scale*scale)
    r_in = r[1:-1]
    H = T[1:-1, 1:-1] + np.diag(V_eff(r_in, float(B), m))
    ev = np.real(eig(H, check_finite=False)[0])
    cand = ev[(ev > -1.0) & (ev < 1.0)]
    return cand.min() if len(cand) else np.nan

def Bstar_newton(m, N=N_SP, newton_steps=3, h_rel=1e-5):
    """三次拟合根 + 对 N 谱特征值 E(B) 的 Newton 细化（收敛到 N 系统的真实根）"""
    B = Bstar_spectral(m, N=N)
    for _ in range(newton_steps):
        h = h_rel * abs(B)
        e_p = E0_at(B+h, m, N); e_m = E0_at(B-h, m, N); e_0 = E0_at(B, m, N)
        de = (e_p - e_m) / (2.0*h)
        if not np.isfinite(de) or de == 0.0:
            break
        dB = -e_0 / de
        B = B + dB
        if abs(dB) < 1e-14*abs(B):
            break
    return B

if __name__ == "__main__":
    t0 = time.time()
    print("== P7-5e-232b：三次拟合残差判别（Newton 细化 vs 三次拟合根）==", flush=True)
    ms_test = [33, 129, 256, 512, 513, 640, 768, 896, 1024]
    print("  m     | δ(三次拟合)  | δ(Newton)     | Δδ          | 模型残差 r(Newton)", flush=True)
    for m in ms_test:
        Bc = Bstar_spectral(-m)
        Bn = Bstar_newton(-m)
        cl = closed_1B(m)
        dc = cl - 1.0/Bc
        dn = cl - 1.0/Bn
        mod = INV56 + EPS_W - C13/m - D41/m**2 + E39/m**3
        print("  %4d | %.10f | %.10f | %+.2e | %+.2e" % (m, dc, dn, dn-dc, dn-mod), flush=True)

    print("", flush=True)
    print("== 高 m 段（512..1024）Newton 版残差线性拟合 ==", flush=True)
    msf = np.array([m for m in ms_test if 512 <= m <= 1024], dtype=float)
    rn = []
    for m in ms_test:
        if 512 <= m <= 1024:
            Bn = Bstar_newton(-m)
            dn = closed_1B(m) - 1.0/Bn
            mod = INV56 + EPS_W - C13/m - D41/m**2 + E39/m**3
            rn.append(dn - mod)
    rn = np.array(rn)
    X = np.vstack([np.ones_like(msf), msf]).T
    c = np.linalg.lstsq(X, rn, rcond=None)[0]
    rms = np.sqrt(np.mean((X@c - rn)**2))
    print("  残差 = %+.3e + %+.3e·m（RMS %.2e）" % (c[0], c[1], rms), flush=True)
    print("  vs 三次拟合版线性系数（打靶 2.93e-9 / N=1200 2.45e-9）", flush=True)

    json.dump({"base": "Newton refinement on N=1200 eigenvalues (pure-root channel)",
               "ms": ms_test, "runtime_s": time.time()-t0},
              open(os.path.join(BASE, "_phase102_p7_5e232b_newton_pure_root.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
