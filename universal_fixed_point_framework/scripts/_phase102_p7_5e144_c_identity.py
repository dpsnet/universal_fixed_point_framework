# -*- coding: utf-8 -*-
"""
P7-5e-144：C/D 精确提取——加密过零扫描 + 二次插值
================================================================
142 的 1/B* 用 150 点线性插值——δ_1/8 尾部疑似数值噪声主导
（δ_1/8 × m^0.63 非简单幂律）。本步：
P1 聚焦 B* 附近加密网格（200 点，Bc 的 ±2%）+ 二次插值 → 高精度 1/B*
P2 δ_cl(m) = (|m|/2+1/7) − 1/B* 拟合 1/56 − C/m − D/m²（最小二乘）
P3 C 对比候选 127·8/10⁴ = 0.1016（升格/证伪判别）
P4 高阶残差（e/m³ 项重要性）
"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

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

def x0_from_bracket(xa, ya, xb, yb, xc, yc):
    # 二次插值过零（三邻近点）
    A = np.vstack([np.ones(3), [xa, xb, xc], [xa**2, xb**2, xc**2]]).T
    cc, _, _, _ = np.linalg.lstsq(A, [ya, yb, yc], rcond=None)
    disc = cc[1]**2 - 4*cc[2]*cc[0]
    if disc < 0 or abs(cc[2]) < 1e-30:
        return None
    s1 = (-cc[1] + np.sqrt(disc)) / (2*cc[2])
    s2 = (-cc[1] - np.sqrt(disc)) / (2*cc[2])
    cand = [v for v in (s1, s2) if xa <= v <= xc]
    if not cand:
        return None
    return min(cand, key=lambda v: abs(v - xb))

print("=== P7-5e-144 C/D 精确提取 ===", flush=True)
ms = [-33, -64, -128, -256]
npt = 200
invBs = {}
for m in ms:
    cl = abs(m)/2.0 + 1.0/8.0
    Bc = 1.0/cl
    # 聚焦 B* 附近：先粗扫定位，再加密
    Bs = np.linspace(0.0, 1.15*Bc, 60)
    Es = np.array([E0_at(b, m) for b in Bs])
    x = Bs*abs(m); y = Es*abs(m)
    idx = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    i = idx[-1]
    b_lo = Bs[max(0, i-1)]; b_hi = Bs[min(len(Bs)-1, i+1)]
    # 加密 ±5% 窗口
    Bf = np.linspace(0.95*b_lo, 1.05*b_hi, npt)
    Ef = np.array([E0_at(b, m) for b in Bf])
    xf = Bf*abs(m); yf = Ef*abs(m)
    idx2 = np.where((yf[:-1] < 0) & (yf[1:] >= 0))[0]
    j = idx2[-1]
    if j >= 1 and j <= len(xf)-2:
        x0 = x0_from_bracket(xf[j-1], yf[j-1], xf[j], yf[j], xf[j+1], yf[j+1])
    else:
        # 线性
        x0 = xf[j] - yf[j]*(xf[j+1]-xf[j])/(yf[j+1]-yf[j])
    invB = abs(m)/x0
    invBs[m] = (invB, x0, cl)
    print("  m=%4d：x0=%.8f（B*·|m|）、1/B*=%.8f、|m|/2+1/8=%.8f、差=%.6f" % (
        m, x0, invB, cl, invB-cl), flush=True)

print("--- P2/P3 C/D 拟合（δ_cl = 1/56 − C/m − D/m²）---", flush=True)
M = np.array([abs(m) for m in ms])
dcl = np.array([(abs(m)/2.0+1.0/7.0) - invBs[m][0] for m in ms])
# 双参拟合 C, D
A = np.vstack([1.0/M, 1.0/M**2]).T
cc, res, _, _ = np.linalg.lstsq(A, dcl, rcond=None)
print("  双参（C,D）：C=%.8f（候选 127·8/10⁴=0.1016，偏差 %+.5f%%）、D=%.8f" % (
    cc[0], (cc[0]/0.1016-1)*100, cc[1]), flush=True)
pred = 1.0/56.0 - cc[0]/M - cc[1]/M**2
for k, m in enumerate(ms):
    print("    m=%4d：δ_cl 实测 %.6f vs 双参预测 %.6f（残差 %+.6f）" % (
        m, dcl[k], pred[k], dcl[k]-pred[k]), flush=True)
# 三参（加 e/m³）
A3 = np.vstack([1.0/M, 1.0/M**2, 1.0/M**3]).T
c3, _, _, _ = np.linalg.lstsq(A3, dcl, rcond=None)
print("  三参（C,D,e）：C=%.8f、D=%.8f、e=%.8f" % tuple(c3), flush=True)
pred3 = 1.0/56.0 - c3[0]/M - c3[1]/M**2 - c3[2]/M**3
for k, m in enumerate(ms):
    print("    m=%4d：δ_cl 实测 %.6f vs 三参预测 %.6f（残差 %+.6f）" % (
        m, dcl[k], pred3[k], dcl[k]-pred3[k]), flush=True)
# C 固定候选 0.1016 检验
resid_fixed = np.sum((dcl - (1.0/56.0 - 0.1016/M))**2)
resid_free = np.sum((dcl - pred)**2)
print("  C=0.1016 固定残差平方 %.3e vs 双参自由 %.3e（比值 %.2f）" % (
    resid_fixed, resid_free, resid_fixed/max(resid_free, 1e-30)), flush=True)
print("exit 0", flush=True)
