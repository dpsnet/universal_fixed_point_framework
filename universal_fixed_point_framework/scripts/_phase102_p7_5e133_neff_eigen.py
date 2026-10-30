# -*- coding: utf-8 -*-
"""
P7-5e-133：N_eff 本征态提取——E_0(B) 磁线性项 + B* 处基态波函数形态
==================================================================
机制候选：1/B* = |m|/2 + 1/8 ⟺ E_0(B) = −E_bind + μ_eff·B（μ_eff = |m|/2 + 1/8）
P1 μ_eff 判别：E_0(B) 在 B* 附近的线性斜率 vs |m|/2+1/8（m=33/64/128）
P2 E_bind 判别：B→0 外推 E_0(0)（束缚能）vs 1（自然单位库仑标度）
P3 ψ(r) 形态：B* 处基态波函数峰值/宽度/节点数（磁长度标度对照）
"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

N_SP = 600
W = 0.0265

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

def scan(m, N=N_SP, w=W):
    """返回 Bs、Es、psi(r 网格, 基态)、r 网格"""
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    Bc = 1.0/cl
    r_lo, r_hi = 0.23*abs(m), 3.1*abs(m)
    x, D1, D2 = cheb_d1d2(N)
    a, b = r_lo, r_hi
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5 * D2 / (scale*scale)
    r_in = r[1:-1]
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    Es = np.empty(7); psis = []
    for i, B in enumerate(Bs):
        H = T[1:-1, 1:-1] + np.diag(V_eff(r_in, float(B), m))
        ev, evec = eig(H, check_finite=False)
        evr = np.real(ev)
        cand = evr[(evr > -1.0) & (evr < 1.0)]
        if len(cand):
            i0 = int(np.argmin(evr[(evr > -1.0) & (evr < 1.0)]))
            # 找全局最小正/负候选索引
            mask = (evr > -1.0) & (evr < 1.0)
            idx = np.where(mask)[0]
            jmin = idx[np.argmin(evr[idx])]
            Es[i] = evr[jmin]
            psis.append(evec[:, jmin])
        else:
            Es[i] = np.nan; psis.append(None)
    return Bs, Es, psis, r_in

def analyze(m):
    Bs, Es, psis, r = scan(m)
    # B* 过零（三次拟合）
    B0 = float(Bs[3]); X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    xx = -c0/c1
    for _ in range(6):
        xx = xx - (c0+c1*xx+c2*xx**2+c3*xx**3)/(c1+2*c2*xx+3*c3*xx**2)
    Bstar = B0 + xx
    # dE/dB 在 B*（三次导数解析）
    dEdB = c1 + 2*c2*xx + 3*c3*xx**2
    mu_pred = abs(m)/2.0 + 1.0/8.0
    # E_bind：B=0 外推（用低 B 端两点线性外推不可靠——用三次多项式在 B=0 估值，但 B 范围不含 0：
    # 改用 E_0(B) 的三次拟合在 X=-B0 处估值（外推误差大，标注）
    E_bind_ext = c0 + c1*(-B0) + c2*(-B0)**2 + c3*(-B0)**3
    # ψ 在 B*=中心 B（Bs[3]）——用 Bc 处 psi（第 4 点）
    psi = psis[3]
    rho = psi**2
    r_peak = r[np.argmax(rho)]
    # 宽度：二阶矩
    norm = np.trapezoid(rho, r)
    mean_r = np.trapezoid(r*rho, r)/norm
    var_r = np.trapezoid((r-mean_r)**2*rho, r)/norm
    width = np.sqrt(var_r)
    # 节点数
    signs = np.sign(psi)
    nodes = int(np.sum(signs[1:]*signs[:-1] < 0))
    l_B = 1.0/np.sqrt(Bstar)
    rho_at_peak = rho.max()*norm
    return dict(m=m, Bstar=Bstar, dEdB=float(dEdB), mu_pred=mu_pred,
                dEdB_dev_pct=(dEdB-mu_pred)/mu_pred*100.0,
                E_bind_ext=float(E_bind_ext),
                r_peak=float(r_peak), width=float(width), nodes=nodes,
                l_B=float(l_B), r_peak_lB=float(r_peak/l_B), width_lB=float(width/l_B))

print("=== P7-5e-133 N_eff 本征态提取 ===", flush=True)
for m in (-33, -64, -128):
    res = analyze(m)
    print("m=%3d：B*=%.8f、dE/dB=%.8f（预测 |m|/2+1/8=%.8f，dev %+.6f pct）、E_bind(外推)=%.6f、r_peak=%.4f（%.2f l_B）、宽度=%.4f（%.2f l_B）、节点=%d" % (
        res["m"], res["Bstar"], res["dEdB"], res["mu_pred"], res["dEdB_dev_pct"],
        res["E_bind_ext"], res["r_peak"], res["r_peak_lB"], res["width"], res["width_lB"], res["nodes"]), flush=True)
print("exit 0", flush=True)
