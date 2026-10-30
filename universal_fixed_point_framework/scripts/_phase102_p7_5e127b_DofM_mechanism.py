# -*- coding: utf-8 -*-
"""
P7-5e-127b：D_eff(m) 机制判别——D 漂移是否 = E/m³ 高阶项
======================================================
P1b D_eff vs 1/m 线性拟合（5 窗口）：高线性度（R²>0.99）= D 漂移源于 E/m³ 项
P2b C_eff vs 1/m 线性拟合：C 漂移与 D 漂移是否同源（基相关传递）
P3b 残差结构再检：全链三参残差 vs 1/m³ 相关性（corr 高 = 残差即 E/m³）
数据源：124 权威 JSON
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))
out = j["out"]

def get_data(lo, hi):
    ms = np.array([abs(int(k)) for k in out if lo <= -int(k) <= hi], dtype=float)
    invB = np.array([1.0/out[k]["Bstar"] for k in out if lo <= -int(k) <= hi])
    order = np.argsort(ms); ms = ms[order]; invB = invB[order]
    cl = ms/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**ms)
    return ms, cl - invB

def fit3(ms, delta):
    X = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
    c, _, _, _ = np.linalg.lstsq(X, delta, rcond=None)
    return c[0], -c[1], -c[2]

# P1b/P2b：窗口拟合 D_eff、C_eff vs 窗口中心 1/m
starts = list(range(129, 256-48+1, 16))
mc, Ds, Cs = [], [], []
for s in starts:
    ms, delta = get_data(s, s+47)
    d, C, D = fit3(ms, delta)
    mc.append(np.mean(ms)); Ds.append(D); Cs.append(C)
mc = np.array(mc); Ds = np.array(Ds); Cs = np.array(Cs)
inv_m = 1.0/mc

def linfit(x, y):
    X = np.vstack([np.ones_like(x), x]).T
    c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X@c
    ss_tot = np.sum((y-np.mean(y))**2)
    r2 = 1.0 - np.sum(resid**2)/ss_tot
    return c[1], c[0], r2  # slope, intercept, R2

print("=== P1b D_eff vs 1/m 线性拟合（窗口中心）===", flush=True)
E, D_true, r2 = linfit(inv_m, Ds)
print("  D_eff(m) = D_true + E/m：D_true=%+.6f、E=%+.3f、R²=%.6f" % (D_true, E, r2), flush=True)
print("  → E>0 且 R² 高 = D 漂移源于 E/m³ 高阶项（δ 中 E/m³ 贡献）", flush=True)

print("=== P2b C_eff vs 1/m 线性拟合 ===", flush=True)
Ec, C_true, r2c = linfit(inv_m, Cs)
print("  C_eff(m) = C_true + Ec/m：C_true=%+.6f、Ec=%+.4f、R²=%.6f" % (C_true, Ec, r2c), flush=True)

print("=== P3b 全链三参残差 vs 1/m³ 相关性 ===", flush=True)
ms, delta = get_data(33, 256)
X = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
c, _, _, _ = np.linalg.lstsq(X, delta, rcond=None)
res = delta - X@c
corr = np.corrcoef(res, 1.0/ms**3)[0,1]
print("  corr(残差, 1/m³) = %+.3f（|corr|>0.9 = 残差即 E/m³ 结构）" % corr, flush=True)
# 残差/m³ 有效 E 值（分段）
for lo, hi in [(33,128),(129,192),(193,256)]:
    msk = (ms>=lo)&(ms<=hi)
    E_eff = np.mean(res[msk]*ms[msk]**3)
    print("  段 %d..%d：E_eff = 残差×m³ 均值 = %+.3f（跨段稳定 = E 真存在；发散 = 非纯 E/m³）" % (lo, hi, E_eff), flush=True)
print("exit 0", flush=True)
