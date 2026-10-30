# -*- coding: utf-8 -*-
"""
P7-5e-128：α₀=1/2 主斜率精确性判别（用户"系数是否 m 的函数"先验延续到主斜率）
============================================================================
P1 全链（33..256）自由 a 拟合 1/B* = a·m + b + c/m + d/m²——a vs 1/2 偏差 + 固定/自由 RMS 对照
P2 滑动窗口 a_eff(m) 形态：常数=α₀ 精确 1/2；平滑漂移=α₀(m) 依赖
P3 ε 上限：δ∞ 锁定（子段差 0.0027%）+ 残差 |max| 隐含的斜率精度约束
数据源：_phase102_p7_5e124_spectral_m256.json
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
    return ms, invB

# P1 全链自由 a 四参
print("=== P1 全链 33..256：自由 a 四参拟合 ===", flush=True)
ms, invB = get_data(33, 256)
X4 = np.vstack([ms, np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
c4, _, _, _ = np.linalg.lstsq(X4, invB, rcond=None)
r4 = invB - X4@c4
rms4 = float(np.sqrt(np.mean(r4**2)))
# 固定 a=1/2：残差 = invB - (m/2 + b + c/m + d/m²)
cl = ms/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**ms)
delta = cl - invB
X3 = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
c3, _, _, _ = np.linalg.lstsq(X3, delta, rcond=None)
r3 = delta - X3@c3
rms3 = float(np.sqrt(np.mean(r3**2)))
print("  自由 a=%+.9f（vs 1/2 偏差 %+.4e pct）；b=%+.9f、c=%+.6f、d=%+.6f、RMS=%.2e" % (
    c4[0], (c4[0]-0.5)/0.5*100, c4[1], -c4[2], -c4[3], rms4), flush=True)
print("  固定 a=1/2 三参 RMS=%.2e（δ 口径）" % rms3, flush=True)
print("  自由 a 改善比 = %.1fx（>10x = ε 真实；<3x = 斜率精确 1/2）" % (rms3/rms4), flush=True)
cond = np.linalg.cond(X4)
print("  四参设计矩阵条件数 = %.1e" % cond, flush=True)

# P2 滑动窗口 a_eff
print("=== P2 滑动窗口 a_eff（33..256，窗 48 步 16）===", flush=True)
starts = list(range(33, 256-48+1, 16))
a_s, mc_s = [], []
for s in starts:
    msw, ib = get_data(s, s+47)
    X = np.vstack([msw, np.ones_like(msw), 1.0/msw, 1.0/msw**2]).T
    c, _, _, _ = np.linalg.lstsq(X, ib, rcond=None)
    a_s.append(c[0]); mc_s.append(np.mean(msw))
    print("  m=%d..%d  a_eff=%+.7f（偏差 %+.2e pct vs 1/2）" % (s, s+47, c[0], (c[0]-0.5)/0.5*100), flush=True)
print("  a_eff 序列 = %s" % ("、".join("%+.6f" % a for a in a_s)), flush=True)
if len(a_s) >= 3:
    print("  a_eff 极差 = %.2e（~0 = α₀ 精确常数；大 = α₀(m) 依赖）" % (max(a_s)-min(a_s)), flush=True)
    # 线性趋势检验
    X = np.vstack([np.ones_like(np.array(mc_s)), np.array(mc_s)]).T
    c, _, _, _ = np.linalg.lstsq(X, np.array(a_s), rcond=None)
    print("  a_eff vs m 线性斜率 = %+.2e（|斜率|>1e-7 = 漂移；~0 = 常数）" % c[1], flush=True)

# P3 ε 上限（残差隐含约束）
print("=== P3 ε 上限（δ∞ 锁定 + 残差隐含约束）===", flush=True)
eps_bound = 9.25e-8/33.0
print("  残差 |max|=9.25e-8 在 m=33 → |ε| ≲ %.2e（斜率偏离 1/2 的上限）" % eps_bound, flush=True)
print("  δ∞ 锁定子段差 0.0027% → 独立交叉约束 ε·256 ≲ 1.7e-6·?（见拟合）", flush=True)
print("exit 0", flush=True)
