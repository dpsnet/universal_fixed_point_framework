# -*- coding: utf-8 -*-
"""
P7-5e-122：C/D 系数框架身份候选验证（用户代数观察 2026-10-14）
================================================================
用户候选（精确代数）：
  C = (2^(k_max−1)−1)·k_max/(k_max+2)^4 = 127·8/10^4 = 0.1016
      127 = Mersenne M_7 = 2^7−1（7 = k_max−1）
  D = ((k_max−2)·k_max−1)/((k_max−3)^2·(k_max+2)^2) = 47/(25·100) = 47/2500 = 0.0188
      47 = 6·8−1 = 48−1（(k_max−2)·k_max − 1）
口径：1/B* = |m|/2 + 1/8 + C/m + D/m² + ...（C、D 正系数；δ 口径为 −C、−D）
对照拟合值（1/B* 口径）：
  120 三参：C=0.101613、D=0.018811（δ 拟合取反）
  121 固定 K=1/8 两参：C=0.101537、D=0.020893（两参缺 1/m³ 项，D 偏移）
先验登记（计算前）：
  P1 C 候选 0.1016 与自由拟合差 < 0.1%（预期 0.013% 级）
  P2 D 候选 0.0188 与三参拟合差 < 0.5%（预期 0.058% 级）
  P3 固定 C_c/D_c 候选值拟合（自由 E）：RMS 与自由三参同级（~1e-8），E≈−0.0157 残留
  P4 纯候选检验（C_c、D_c 固定，无拟合）：残差 RMS ≤ 2e-7 且无系统漂移
数据源：scripts\_phase102_p7_5e120_spectral_m128.json（谱方法全链 96 点）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e120_spectral_m128.json"), encoding="utf-8"))
ms = np.array([abs(int(k)) for k in j["out"]], dtype=float)
invB = np.array([1.0/v["Bstar"] for v in j["out"].values()])
# 确保按 m 升序
order = np.argsort(ms); ms = ms[order]; invB = invB[order]

C_c = (2.0**7 - 1)*8.0/10.0**4   # 127*8/10000
D_c = ((8.0-2)*8.0 - 1.0)/((8.0-3)**2*(8.0+2)**2)  # 47/2500
print("候选精确值：C_c = 127*8/10^4 = %.10f    D_c = 47/2500 = %.10f" % (C_c, D_c), flush=True)

K = 0.125  # 1/8 = 1/k_max（P7-5e-121 锁定）

# 自由两参（对照 121）
def fit(X, y):
    c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return c, float(np.sqrt(np.mean((X@c - y)**2)))

X2 = np.vstack([1.0/ms, 1.0/ms**2]).T
y2 = invB - (ms/2.0 + K)
c2, rms2 = fit(X2, y2)
print("自由两参：C=%.6f  D=%.6f  RMS=%.2e" % (c2[0], c2[1], rms2), flush=True)

X3 = np.vstack([1.0/ms, 1.0/ms**2, 1.0/ms**3]).T
c3, rms3 = fit(X3, y2)
print("自由三参：C=%.6f  D=%.6f  E=%.6f  RMS=%.2e" % (c3[0], c3[1], c3[2], rms3), flush=True)

# P1/P2：候选 vs 自由三参
devC = abs(c3[0]-C_c)/C_c*100.0
devD = abs(c3[1]-D_c)/D_c*100.0
print("P1 C 偏差：|0.101613−0.1016|/0.1016 = %.4f pct（判据 <0.1）" % devC, flush=True)
print("P2 D 偏差：|0.018811−0.0188|/0.0188 = %.4f pct（判据 <0.5）" % devD, flush=True)

# P3：固定 C_c/D_c，自由 E
XE = np.vstack([1.0/ms**3]).T
yE = y2 - (C_c/ms + D_c/ms**2)
cE, rmsE = fit(XE, yE)
print("P3 固定候选+自由 E：E=%.6f  RMS=%.2e（120 四参 E=−0.015707 对照）" % (cE[0], rmsE), flush=True)

# P4：纯候选检验（C_c、D_c、E=0 全固定）
resid = y2 - (C_c/ms + D_c/ms**2)
rmsP = float(np.sqrt(np.mean(resid**2)))
half = ms <= 64
rms_h = float(np.sqrt(np.mean(resid[half]**2)))
rms_t = float(np.sqrt(np.mean(resid[~half]**2)))
print("P4 纯候选残差：RMS=%.2e（分段 33..64=%.2e / 65..128=%.2e 漂移比=%.1f）" % (rmsP, rms_h, rms_t, rms_t/rms_h), flush=True)

# 附加：候选+E 组合 RMS（C_c、D_c、E=自由）
print("综合判定：", flush=True)
p1_ok = devC < 0.1; p2_ok = devD < 0.5; p4_ok = rmsP <= 2e-7
print("  P1 %s（%.4f pct）  P2 %s（%.4f pct）  P4 %s（RMS %.1e）" % ("通过" if p1_ok else "未过", devC, "通过" if p2_ok else "未过", devD, "通过" if p4_ok else "未过", rmsP), flush=True)
print("exit 0", flush=True)
