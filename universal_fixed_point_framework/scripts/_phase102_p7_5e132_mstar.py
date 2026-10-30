# -*- coding: utf-8 -*-
"""
P7-5e-132：过渡尺度 m* 判别——缺口→满格通道倒数转换的定位
==========================================================
Δ_eff(m) = δ(m) − c/m（扣 1/m 项后的截距差部分）：小 m → 0（缺口域 1/7），大 m → 1/56（满格域 1/8）
P1 三源全链 Δ_eff 序列（2..256）
P2 半高点（1/112）定位 m*
P3 候选对照：2(k_max−1)=14、k_max²/2=32、k_max(k_max−1)/2=28、3(k_max−1)=21、k_max+7=15、2^3+4=12
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUTP = os.path.join(BASE, "_phase102_p7_5e132_out.txt")

lines = []
def log(s=""):
    lines.append(s)
    print(s, flush=True)

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

ms_all = sorted(B.keys())  # 1..256
log("数据源合并点数：%d（m=1..%d）" % (len(ms_all), ms_all[-1]))

C_FIX = 0.1016  # 127·8/10⁴ 候选固定（b 口径五参 c=0.101562，两者微差不敏感）
D56 = 1.0/56.0

log("=== P1 全链 Δ_eff(m) = δ(m) − C/m（δ=cl−1/B*，C=%.4f）===")
rows = []
for m in ms_all:
    delta = closed(m) - 1.0/B[m]
    De = delta - C_FIX/m
    rows.append((m, delta, De))
    if m in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,24,28,32,40,48,64,96,128,192,256):
        log("  m=%3d：δ=%+.7f、Δ_eff=%+.7f（1/56=%.7f）" % (m, delta, De, D56))

log("=== P2 半高点定位（Δ_eff 首次达 1/112=%.7f）===" % (D56/2))
half = D56/2
prev = None
for m, delta, De in rows:
    if De >= half and prev is None:
        log("  首个达半高点：m=%d（Δ_eff=%.7f）——过渡中心 m*≈%d（前一点 m=%d Δ_eff=%.7f）" % (m, De, m, m-1, prev))
        break
    prev = De

log("=== P3 候选对照 ===")
cands = {
    "2(k_max-1)=14": 14, "k_max^2/2=32": 32, "k_max(k_max-1)/2=28": 28,
    "3(k_max-1)=21": 21, "k_max+7=15": 15, "2^3+4=12": 12, "2^4-1=15": 15,
}
# 找各候选点的 Δ_eff 与 1/56 的接近度（过渡带内）
for name, mc in cands.items():
    if mc not in B:
        log("  %s：m=%d 无数据" % (name, mc))
        continue
    delta = closed(mc) - 1.0/B[mc]
    De = delta - C_FIX/mc
    log("  %s（m=%d）：Δ_eff=%.6f、1/56 占比 %.1f pct、半高 1/112 占比 %.1f pct" % (
        name, mc, De, De/D56*100.0, De/(D56/2)*100.0))

log("exit 0")
with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
