# -*- coding: utf-8 -*-
"""
P7-5e-125：D_tail（129..256 段）框架身份候选验证——用户代数观察
================================================================
用户：0.0057 = ((8−1)·8+1)/((8+2)²·(8+2)²) = 57/10000
  D_tail（124 输出 129..256 三参）：−0.005731（正号 0.005731）
先验登记（计算前）：
  P1 D_tail vs 57/10⁴：偏差 <1%（预期 +0.54%——段内拟合精度受限）
  P2 固定 D=57/10⁴ 三参拟合 129..256 段：δ∞/C 漂移 <0.1%（自洽）
  P3 家族对照：D_head=47/2500（(k_max−2)k_max−1）、D_tail=57/10⁴（(k_max−1)k_max+1）、
     65=k_max²+1（m=−1 修正）——"k_max 家族 ±1"三成员；57−47=10=n_max
数据源：scripts\_phase102_p7_5e124_spectral_m256.json（129..256 段逐点）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))
out = j["out"]
ms = np.array([abs(int(k)) for k in out if -257 < int(k) <= -129], dtype=float)
invB = np.array([1.0/out[k]["Bstar"] for k in out if -257 < int(k) <= -129])
order = np.argsort(ms); ms = ms[order]; invB = invB[order]
cl = ms/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**ms)
delta = cl - invB

def fit(X, y):
    c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return c, float(np.sqrt(np.mean((X@c - y)**2)))

# 129..256 段三参（复算 124）
X3 = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
c3, rms3 = fit(X3, delta)
D_tail = -c3[2]
print("129..256 段三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (c3[0], -c3[1], D_tail, rms3), flush=True)

D_c = 57.0/10000.0
print("候选：D_tail = 57/10^4 = %.10f（57 = (k_max−1)·k_max + 1 = 7·8+1）" % D_c, flush=True)
dev = abs(D_tail-D_c)/D_tail*100
print("P1 D_tail vs 57/10^4 偏差：%+.4f pct（判据<1）→ %s" % (dev, "过" if dev < 1 else "未过"), flush=True)

# P2 固定 D=57/10^4 三参（δ∞、C 自由）
X2f = np.vstack([np.ones_like(ms), 1.0/ms]).T
yf = delta - D_c/ms**2
c2f, rms2f = fit(X2f, yf)
dev_dinf = abs(c2f[0]-1.0/56.0)/(1.0/56.0)*100
dev_C = abs(-c2f[1]-0.1016)/0.1016*100
print("P2 固定 D=57/10^4：δ∞=%.8f（vs 1/56 %+.4f pct）  C=%.6f（vs 0.1016 %+.4f pct）  RMS=%.2e" % (
    c2f[0], dev_dinf, -c2f[1], dev_C, rms2f), flush=True)
print("   → δ∞ 漂移 %s（<0.1）/ C 漂移 %s（<0.1）" % (
    "过" if dev_dinf < 0.1 else "★ 未过", "过" if dev_C < 0.1 else "★ 未过"), flush=True)

# P3 家族对照
print("", flush=True)
print("P3 k_max 家族 ±1 成员：", flush=True)
fam = [("65", 65, "k_max²+1 = 8²+1（m=−1 修正，P7-5e-95e/98）"),
       ("57", 57, "(k_max−1)k_max+1 = 7·8+1（D_tail，129..256 段）"),
       ("47", 47, "(k_max−2)k_max−1 = 6·8−1（D_head，33..128 段）")]
for name, v, desc in fam:
    print("  %s = %d：%s" % (name, v, desc), flush=True)
print("  57−47 = 10 = n_max = k_max+2（框架量再现）", flush=True)
print("  分母：D_head 2500 = (k_max−3)²·(k_max+2)² = 5²·10²；D_tail 10000 = (k_max+2)⁴ = 10⁴", flush=True)
print("exit 0", flush=True)
