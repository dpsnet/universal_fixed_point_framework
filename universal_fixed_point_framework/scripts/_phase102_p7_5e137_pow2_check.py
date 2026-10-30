# -*- coding: utf-8 -*-
"""
P7-5e-137：2 幂点减半规律检验（136 先验延伸）
================================================================
136 登记：32=2⁵ 呼应 1/32=2^{−5}——"能否延伸到 m=64/128/256（2 幂点）"
P1 m=2^k（k=1..8）Δ_eff 占比与补占比（1−占比）
P2 补占比减半比：m 倍增是否精确减半
P3 减半 vs 2C/m 恒等关系澄清（Δ_eff=δ−C/m 定义代换 vs 独立结构）
P4 C 身份 2 幂结构对照（2C=0.2032？）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
fa = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
fb = json.load(open(os.path.join(BASE, "_phase102_p7_5e117_m32_scan.json"), encoding="utf-8"))
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))

B = {}
for k, v in fa["out"].items():
    B[-int(k)] = v["R2"]
for k, v in fb["out"].items():
    B[-int(k)] = v["Bstar0"]
for k, v in fc["out"].items():
    B[-int(k)] = v["Bstar"]

def closed(m):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    if abs(m) == 1:
        cl += 1.0/65.0
    return cl

C_FIX = 0.1016
D56 = 1.0/56.0

def Deff(m):
    return (closed(m) - 1.0/B[m]) - C_FIX/m

print("=== P7-5e-137 2 幂点减半规律 ===", flush=True)
print("--- P1 2^k 点占比/补占比 ---", flush=True)
ms = [2, 4, 8, 16, 32, 64, 128, 256]
ratios = []
for m in ms:
    d = Deff(m)
    r = d/D56
    ratios.append(r)
    print("  m=%3d（2^%d）：Δ_eff=%.6f、占比 %5.2f pct、补占比 %5.2f pct" % (m, int(np.log2(m)), d, r*100.0, (1-r)*100.0), flush=True)

print("--- P2 补占比减半比（m 倍增）---", flush=True)
for i in range(1, len(ms)):
    r_prev, r_cur = 1-ratios[i-1], 1-ratios[i]
    print("  %d→%d：补占比 %.4f→%.4f——比值 %.4f（精确减半 = 0.5000）" % (ms[i-1], ms[i], r_prev, r_cur, r_cur/r_prev), flush=True)

print("--- P3 恒等澄清：1−Δ_eff/D56 vs 2C/(m·D56) ---", flush=True)
for m in ms:
    pred = 2.0*C_FIX/(m*D56)
    obs = 1.0 - Deff(m)/D56
    print("  m=%3d：实测补占比 %.6f vs 2C/(m·D56)=%.6f——差 %+.3f pct" % (m, obs, pred, (obs-pred)/pred*100.0), flush=True)

print("--- P4 C 的 2 幂结构对照 ---", flush=True)
print("  2C = %.6f——候选：0.2032 = 2032/10⁴；2C·10⁴ = %.1f" % (2*C_FIX, 2*C_FIX*1e4), flush=True)
print("  127·8·2 = 2032 = 2⁴·127 = 2⁴·(2⁷−1)——2C = Mersenne·2⁴/10⁴" , flush=True)
print("  1/32 = 0.03125 的补占比对应 m=32：2C/(32·D56) = %.6f vs 1−0.643=%.6f" % (2*C_FIX/(32*D56), 1-ratios[4]), flush=True)
print("exit 0", flush=True)
