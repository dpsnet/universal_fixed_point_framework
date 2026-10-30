# -*- coding: utf-8 -*-
"""
P7-5e-122b：C/D 候选的 δ 口径验证（修正对照基准）
================================================================
正确对照：120 权威 fit_3p（δ 口径，无 E 项）
  δ(m) = δ∞ + C/m + D/m²   拟合：δ∞=0.01785774、C=−0.101613、D=−0.018811
  → 正号口径 δ(m) = δ∞ − 0.101613/m − 0.018811/m²
用户候选（2026-10-14）：
  C = 127·8/10^4 = 0.1016   （127 = 2^7−1 = Mersenne M_7，7=k_max−1）
  D = 47/2500 = 0.0188      （47 = (k_max−2)·k_max−1 = 48−1）
验证路径：
  P1 候选 vs 120 fit_3p：C 差 <0.1%、D 差 <0.5%
  P2 用实测 δ = cl − 1/B*（m=33..128），拟合 δ = δ∞_free − C/m − D/m² 与候选比较
  P3 固定 C_c/D_c（1/B* 口径 +C/+D），自由 E 项：看 E 与 120 四参 E=−0.0157 是否一致
  P4 纯候选（1/B* = |m|/2 + 1/8 + 0.1016/m + 0.0188/m²）：残差 RMS 判据
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e120_spectral_m128.json"), encoding="utf-8"))
ms = np.array([abs(int(k)) for k in j["out"]], dtype=float)
invB = np.array([1.0/v["Bstar"] for v in j["out"].values()])
order = np.argsort(ms); ms = ms[order]; invB = invB[order]

# 闭式 cl = |m|/2 + 1/7 + 1/(7·2^|m|)（m=33..128，无 65 修正）
cl = ms/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**ms)
delta = cl - invB   # 实测失调（恒正，P7-5e-121）

C_c = (2.0**7 - 1)*8.0/10.0**4
D_c = 47.0/2500.0
print("候选：C_c=%.10f  D_c=%.10f" % (C_c, D_c), flush=True)

# P1：120 权威 fit_3p 对照
f3 = j["fit_3p"]
C120 = -f3["C"]; D120 = -f3["D"]   # 取反为正号口径（若 JSON 存负系数）
print("120 fit_3p（δ 口径）：δ∞=%.10f  C=%.6f  D=%.6f  RMS=%.2e" % (f3["d_inf"], f3["C"], f3["D"], f3["rms"]), flush=True)
devC = abs(C120-C_c)/C_c*100.0
devD = abs(D120-D_c)/D_c*100.0
print("P1 C 偏差 %.4f pct（判据<0.1）  D 偏差 %.4f pct（判据<0.5）" % (devC, devD), flush=True)

# P2：实测 δ 自由拟合（δ = c0 − C/m − D/m²，自由 c0,C,D）
X = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
def fit(X, y):
    c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return c, float(np.sqrt(np.mean((X@c - y)**2)))
c, rms = fit(X, delta)
print("P2 实测 δ 三参拟合：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (c[0], c[1], c[2], rms), flush=True)
devC2 = abs(c[1]-C_c)/C_c*100.0
devD2 = abs(c[2]-D_c)/D_c*100.0
print("    vs 候选：C 偏差 %.4f pct  D 偏差 %.4f pct" % (devC2, devD2), flush=True)

# P3：1/B* 口径固定 C_c/D_c，自由 E
K = 0.125
y = invB - (ms/2.0 + K + C_c/ms + D_c/ms**2)
XE = np.vstack([1.0/ms**3]).T
cE, rmsE = fit(XE, y)
print("P3 固定候选+自由 E：E=%.6f  RMS=%.2e（120 四参 E=−0.0157 对照）" % (cE[0], rmsE), flush=True)

# P4：纯候选残差（1/B* 口径，无 E）
rmsP = float(np.sqrt(np.mean(y**2)))
half = ms <= 64
rms_h = float(np.sqrt(np.mean(y[half]**2))); rms_t = float(np.sqrt(np.mean(y[~half]**2)))
print("P4 纯候选残差：RMS=%.2e（33..64=%.2e / 65..128=%.2e 漂移比=%.1f）" % (rmsP, rms_h, rms_t, rms_t/rms_h), flush=True)

print("exit 0", flush=True)
