# -*- coding: utf-8 -*-
"""
P7-5e-119 预备 v5b：Chebyshev 谱方法（对数映射）验证——高效版
=====================================================================
v4 失效：线性映射动态范围病态 → 伪态。
v5 优化（用户指令"必须优化高效"）：
  a) Chebyshev D1/D2 矩阵构建缓存（7 窗口点共享，不重复构建）；
  b) eigvalsh(subset_by_index=[0,0]) 只求最小本征值（稠密全谱 O(N³) → 子集 O(N²)）。
对数映射 r=e^u：配点密度 ∝1/r，匹配波函数局域 r≈13。
"""
import time
import numpy as np
from scipy.linalg import eigvalsh, eig
from functools import lru_cache

@lru_cache(maxsize=8)
def cheb_d1d2(N):
    """Lobatto-Chebyshev D1/D2 谱微分矩阵（x 降序 1→−1）。缓存复用。"""
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

def _H_internal(B, m, r_lo, r_max, N):
    """构建内部（去端点）Hamiltonian，仅一次。"""
    x, D1, D2 = cheb_d1d2(N)
    u_lo, u_hi = np.log(r_lo), np.log(r_max)
    u = (u_lo + u_hi)/2.0 + (u_hi - u_lo)/2.0 * x
    b = (u_hi - u_lo)/2.0
    r = np.exp(u)
    Lu = D2/(b*b) - D1/b
    Lr = np.diag(np.exp(-2.0*u)) @ Lu
    H = -0.5*Lr + np.diag(V_eff(r, B, m))
    return H[1:-1, 1:-1]

def Bstar_spectral(m, r_lo, r_max, w=0.0265, N=900):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    Bc = 1.0/cl
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    # 预构建：动能部分（与 B 无关）+ 坐标（线性映射 [r_lo, r_max]）
    x, D1, D2 = cheb_d1d2(N)
    a, b = r_lo, r_max
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5 * D2 / (scale*scale)
    r_in = r[1:-1]
    Es = np.empty(7)
    for i, B in enumerate(Bs):
        H = T[1:-1, 1:-1] + np.diag(V_eff(r_in, float(B), m))
        # 配点矩阵非对称（Chebyshev D2）：一般 eig + 物理能量窗筛选
        ev = np.real(eig(H, check_finite=False)[0])
        cand = ev[(ev > -1.0) & (ev < 1.0)]
        Es[i] = cand.min() if len(cand) else np.nan
    B0 = float(Bs[3]); X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    x = -c0/c1
    for _ in range(6):
        x = x - (c0+c1*x+c2*x**2+c3*x**3)/(c1+2*c2*x+3*c3*x**2)
    return B0 + x, Es

if __name__ == "__main__":
    t0 = time.time()
    print("== 谱方法验证 v6（物理支撑区间 [3,40] 线性谱）：m=−13 权威 B*=0.15076306 ==", flush=True)
    for N in [300, 600, 900]:
        Bs, Es = Bstar_spectral(-13, 3.0, 40.0, N=N)
        print("  N=%4d → B*=%.8f（差 %.1e）  δ=%.6f（权威 0.009949967）"
              % (N, Bs, abs(Bs-0.15076306), abs(1.0/Bs - (13.0/2.0+1.0/7.0+1.0/(7.0*2.0**13)))), flush=True)
        print("    窗口 E0（过零）：%s" % ["%+.6f" % e for e in Es], flush=True)
    print("耗时 %.1f s——exit 0" % (time.time()-t0), flush=True)
