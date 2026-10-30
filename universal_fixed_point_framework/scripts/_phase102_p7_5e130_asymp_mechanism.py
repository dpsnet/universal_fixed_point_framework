# -*- coding: utf-8 -*-
"""
P7-5e-130：渐近截距机制攻点——高阶项剥离判别
==================================================
P1 三参 vs 四参：33..256 δ = δ∞ − C/m − D/m² (+E/m³)，看 δ∞ 是否收敛到 1/56
P2 分段四参：33..128 / 129..256 / 15..256，δ∞ 稳定性
P3 b 口径对照：1/B* = a·m + b + c/m + d/m² (+e/m³)，b vs 1/8
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUTP = os.path.join(BASE, "_phase102_p7_5e130_out.txt")

lines = []
def log(s=""):
    lines.append(s)
    print(s, flush=True)

fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))
fb = json.load(open(os.path.join(BASE, "_phase102_p7_5e117_m32_scan.json"), encoding="utf-8"))

B = {}
for k, v in fc["out"].items():
    B[-int(k)] = v["Bstar"]
for k, v in fb["out"].items():
    B[-int(k)] = v["Bstar0"]

ms_all = sorted(B.keys())

def closed(m):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    if abs(m) == 1:
        cl += 1.0/65.0
    return cl

def fit(ms, delta, npar):
    """delta = c0 + c1/m + c2/m^2 (+ c3/m^3)，返回 (δ∞, C=-c1, D=-c2, E=-c3, RMS)"""
    X = np.vstack([np.ones_like(ms)] + [1.0/ms**p for p in range(1, npar)]).T
    c, _, _, _ = np.linalg.lstsq(X, delta, rcond=None)
    rms = float(np.sqrt(np.mean((X @ c - delta)**2)))
    return (c[0], -c[1], -c[2], -c[3] if npar >= 4 else 0.0, rms)

def d56():
    return 1.0/56.0

def show(tag, lo, hi, npar, delta_mode="delta"):
    msk = [m for m in ms_all if lo <= m <= hi]
    ms = np.array(msk, dtype=float)
    if delta_mode == "delta":
        delta = np.array([closed(m) - 1.0/B[m] for m in msk])
    else:
        delta = np.array([1.0/B[m] - abs(m)/2.0 for m in msk])
        # 1/B* - |m|/2 = b + c/m + d/m^2 ... 但 1/B* 含 1/7+1/(7·2^|m|)+δ → delta 语义不同，此处仅对照
    d, C, D, E, rms = fit(ms, delta, npar)
    dev = (d - d56())/d56()*100.0
    log("  %s %2d..%3d npar=%d：δ∞=%+.10f（vs 1/56 %+.6f pct）、C=%+.8f、D=%+.8f%s、RMS=%.1e" % (
        tag, lo, hi, npar, d, dev, C, D, ("、E=%+.6f" % E) if npar >= 4 else "", rms))

log("=== P1 三参 vs 四参（δ 口径，δ=δ∞−C/m−D/m²(−E/m³)）===")
show("P1", 33, 256, 3)
show("P1", 33, 256, 4)
log("=== P2 分段四参 ===")
show("P2", 33, 128, 4)
show("P2", 129, 256, 4)
show("P2", 15, 256, 4)
log("=== P3 b 口径：1/B* = a·m + b + c/m + d/m²（33..256，直接拟合）===")
msk = [m for m in ms_all if 33 <= m <= 256]
ms = np.array(msk, dtype=float)
ib = np.array([1.0/B[m] for m in msk])
X4 = np.vstack([ms, np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
c4, _, _, _ = np.linalg.lstsq(X4, ib, rcond=None)
rms4 = float(np.sqrt(np.mean((X4 @ c4 - ib)**2)))
log("  四参 a=%+.10f（vs 1/2 %+.4f pct）、b=%+.10f（vs 1/8 %+.6f pct）、c=%+.8f、d=%+.8f、RMS=%.1e" % (
    c4[0], (c4[0]-0.5)/0.5*100.0, c4[1], (c4[1]-0.125)/0.125*100.0, c4[2], c4[3], rms4))
X5 = np.vstack([ms, np.ones_like(ms), 1.0/ms, 1.0/ms**2, 1.0/ms**3]).T
c5, _, _, _ = np.linalg.lstsq(X5, ib, rcond=None)
rms5 = float(np.sqrt(np.mean((X5 @ c5 - ib)**2)))
log("  五参 a=%+.10f、b=%+.10f（vs 1/8 %+.6f pct）、c=%+.8f、d=%+.8f、e=%+.6f、RMS=%.1e" % (
    c5[0], c5[1], (c5[1]-0.125)/0.125*100.0, c5[2], c5[3], c5[4], rms5))
log("  b 口径说明：1/B* − |m|/2 = b + c/m + ... 与 δ 口径关系：b = 1/7+1/(7·2^|m|) 部分 ≈ 1/7（m 大）−δ → 这里直接对比数值")
log("exit 0")

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
