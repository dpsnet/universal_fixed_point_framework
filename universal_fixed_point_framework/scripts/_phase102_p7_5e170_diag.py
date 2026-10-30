# -*- coding: utf-8 -*-
"""
P7-5e-170 诊断：δ∞ 偏差身份（去 abs）+ C_m 正确口径重算
======================================================
170 主脚本两点存疑：
  A) worker 的 delta 用了 abs()——若 delta 全负则无害，但需带符号确认
  B) C_m 用了 160 的错误口径 clp=|m|/2+9/56（164 审计确认 Cm_seq 错误）
     正确口径：Cm_seq_fixed = (1/B* − (|m|/2+1/8))·m
"""
import json, numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
d = json.load(open(BASE + r"\_phase102_p7_5e170_spectral_m1024.json", encoding="utf-8"))
out = d["out"]
inv56 = 1.0/56.0

def closed(m):
    a = abs(m)
    tail = 1.0/(7.0*2.0**a) if a <= 120 else 0.0
    return a/2.0 + 1.0/7.0 + tail

# A) 带符号 delta 的多窗口拟合
print("== A) 带符号 delta = 1/B* − 闭式（去 abs）==", flush=True)
signed = {}
for m in range(-33, -1025, -1):
    signed[m] = 1.0/out[str(m)]["Bstar"] - closed(m)
for m in [-33, -64, -128, -256, -512, -1024]:
    print("  m=%5d：signed delta = %+.8f（abs 值 %+.8f）" % (m, signed[m], abs(signed[m])), flush=True)
# 符号检查
neg = sum(1 for m in signed if signed[m] < 0)
print("  符号统计：%d/992 负 → %s" % (neg, "全部负——abs 无害" if neg == 992 else "★ 混合符号——abs 破坏拟合"), flush=True)

print("\n== δ∞ 多窗口（带符号 delta，2-5 参）==", flush=True)
for lo in [128, 256, 384, 512, 768, 900]:
    ms_ = np.arange(lo, 1025, dtype=float)
    ds_ = np.array([signed[m] for m in range(-lo, -1025, -1)])
    best = None
    for k in range(2, 6):
        A = np.vstack([1.0/ms_**j for j in range(k)]).T
        c, _, _, _ = np.linalg.lstsq(A, ds_, rcond=None)
        r = float(np.sqrt(np.mean((A@c - ds_)**2)))
        if best is None or r < best[1]:
            best = (c, r, k)
    c, r, k = best
    print("  m≥%4d（%d 点，%d 参）：δ∞_fit = %.10f  vs 1/56 差 %+.4f pct（abs %.2e）RMS=%.1e" %
          (lo, len(ms_), k, c[0], (c[0]-inv56)/inv56*100, abs(c[0]-inv56), r), flush=True)

# B) Cm_seq_fixed 正确口径
print("\n== B) Cm_seq_fixed 口径：C_m = (1/B* − (|m|/2+1/8))·m ==", flush=True)
vals = {}
for m in [256, 384, 512, 768, 1024]:
    invB = 1.0/out[str(-m)]["Bstar"]
    vals[m] = (invB - (m/2.0 + 1.0/8.0)) * m
    print("  C_m(m=%4d) = %.10f（13/128 = 0.10156250，差 %+.6f pct）" % (m, vals[m], (vals[m]-13.0/128.0)/(13.0/128.0)*100), flush=True)
c13 = 13.0/128.0
Cr1 = 2.0*vals[1024] - vals[512]
Cr2 = 1024.0/(1024.0-768.0)*vals[1024] - 768.0/(1024.0-768.0)*vals[768]
print("  Richardson (512,1024)：C = %.10f（13/128 差 %+.6f pct）" % (Cr1, (Cr1-c13)/c13*100), flush=True)
print("  Richardson (768,1024)：C = %.10f（13/128 差 %+.6f pct）" % (Cr2, (Cr2-c13)/c13*100), flush=True)

# C) C_m 序列趋势（C_m = C + D/m + E/m²... → 拟合 C 真值）
print("\n== C) C_m 序列幂律外推 ==", flush=True)
ms_ = np.array([256.0, 384.0, 512.0, 768.0, 1024.0])
cmv = np.array([vals[m] for m in [256, 384, 512, 768, 1024]])
for k in range(2, 5):
    A = np.vstack([1.0/ms_**j for j in range(k)]).T
    c, _, _, _ = np.linalg.lstsq(A, cmv, rcond=None)
    r = float(np.sqrt(np.mean((A@c - cmv)**2)))
    print("  %d 参 C_m 拟合：C∞ = %.10f（13/128 差 %+.6f pct）RMS=%.1e" % (k, c[0], (c[0]-c13)/c13*100, r), flush=True)
print("exit 0", flush=True)
