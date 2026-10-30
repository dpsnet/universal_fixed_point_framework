# -*- coding: utf-8 -*-
"""
P7-5e-123：E（1/m³ 项）框架身份候选验证
================================================================
背景：双曲渐近 δ(m) = 1/56 − C/m − D/m² − E/m³（δ 口径；1/B* 口径 +E）。
  C = 127·8/10^4 = 0.1016（P7-5e-122 候选命中 +0.0125%）
  D = 47/2500 = 0.0188（P7-5e-122 候选命中 +0.0600%）
  E：120 四参拟合 E = −0.015707（δ 口径系数）
候选（2026-10-14 直觉 + 框架量筛选）：
  E_c1 = 1/64 = 0.015625 —— 1/k_max² = 2^−6 = (k_max−1)/k_max · δ∞ = 7/8 · 1/56（同值）
  E_c2 = 47/3000 = 0.0156667 —— D · (k_max−3)/(k_max−2) = (47/2500)·(5/6)
先验登记（计算前）：
  P1 确认 E 拟合值 ≈ 0.015707（自由四参，δ 口径，m=33..128）
  P2 E_c1=1/64 vs 拟合：差 <1%（预期 0.5% 级）
  P3 固定 E=E_c1 三参拟合（δ∞、C、D 自由）：RMS 与自由四参同级（~1e-8），
     且 δ∞/C/D 漂移 <0.1%——E 候选与其余系数自洽
  P4 对照 E_c2=47/3000 vs 拟合：差 <1%（预期 0.26% 级）
数据源：scripts\_phase102_p7_5e120_spectral_m128.json（谱方法全链 96 点，m=33..128）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e120_spectral_m128.json"), encoding="utf-8"))
ms = np.array([abs(int(k)) for k in j["out"]], dtype=float)
invB = np.array([1.0/v["Bstar"] for v in j["out"].values()])
order = np.argsort(ms); ms = ms[order]; invB = invB[order]

cl = ms/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**ms)
delta = cl - invB

def fit(X, y):
    c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return c, float(np.sqrt(np.mean((X@c - y)**2)))

# 自由四参（δ 口径：δ = c0 + c1/m + c2/m² + c3/m³）
X4 = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2, 1.0/ms**3]).T
c4, rms4 = fit(X4, delta)
E_fit = -c4[3]  # 正号口径
print("自由四参（δ 口径）：δ∞=%.8f  C=%.6f  D=%.6f  E=%.6f  RMS=%.2e" % (c4[0], -c4[1], -c4[2], E_fit, rms4), flush=True)

E_c1 = 1.0/64.0
E_c2 = 47.0/3000.0
print("候选：E_c1 = 1/64 = %.10f（1/k_max² = 2^−6 = (7/8)δ∞）  E_c2 = 47/3000 = %.10f（D·5/6）" % (E_c1, E_c2), flush=True)

# P1/P2/P4：偏差
dev1 = abs(E_fit-E_c1)/E_fit*100.0
dev2 = abs(E_fit-E_c2)/E_fit*100.0
print("P1 E 拟合确认：%.6f（120 四参 −0.015707 对照）" % E_fit, flush=True)
print("P2 E_c1=1/64 偏差：%.4f pct（判据<1）" % dev1, flush=True)
print("P4 E_c2=47/3000 偏差：%.4f pct（判据<1）" % dev2, flush=True)

# P3：固定 E=E_c1，自由 δ∞/C/D（δ 口径 δ = c0 + c1/m + c2/m² + E_c1/m³）
X3f = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
yf = delta - E_c1/ms**3
c3f, rms3f = fit(X3f, yf)
print("P3 固定 E=1/64 三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (c3f[0], -c3f[1], -c3f[2], rms3f), flush=True)
dev_dinf = abs(c3f[0]-1.0/56.0)/(1.0/56.0)*100.0
dev_C = abs(-c3f[1]-0.1016)/0.1016*100.0
dev_D = abs(-c3f[2]-0.0188)/0.0188*100.0
print("    固定 E 后：δ∞ vs 1/56 偏差 %.4f pct、C vs 0.1016 偏差 %.4f pct、D vs 0.0188 偏差 %.4f pct" % (dev_dinf, dev_C, dev_D), flush=True)

# 对照：固定 E=E_c2 三参
yf2 = delta - E_c2/ms**3
c3g, rms3g = fit(X3f, yf2)
print("对照 固定 E=47/3000：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (c3g[0], -c3g[1], -c3g[2], rms3g), flush=True)

# P5：分段 E 稳定性检验（33..64 vs 65..128）——E 真实项 vs 低阶投影判别
for lo, hi, tag in [(33, 64, "33..64"), (65, 128, "65..128")]:
    msk = (ms >= lo) & (ms <= hi)
    c4s, rms4s = fit(X4[msk], delta[msk])
    print("分段 %s 四参：δ∞=%.8f  C=%.6f  D=%.6f  E=%.6f  RMS=%.2e" % (tag, c4s[0], -c4s[1], -c4s[2], -c4s[3], rms4s), flush=True)

print("exit 0", flush=True)
