# -*- coding: utf-8 -*-
"""
P7-5e-129：全 m 链闭式一致性检验（三数据源统一 + 中间段双曲衔接判别）
================================================================
数据源：
  A: _phase102_p7_5e_fullchain_tridiag.json（m=-1..-14，tridiag 权威）
  B: _phase102_p7_5e117_m32_scan.json（m=-15..-32，117 tridiag，Bstar0）
  C: _phase102_p7_5e124_spectral_m256.json（m=-33..-256，谱方法权威）
P1 三源统一闭式命中表：1/B* vs closed = |m|/2 + 1/7 + 1/(7·2^|m|) + [m=-1: 1/65]
P2 中间段 15..32 δ 三参拟合 vs 33..256（双曲衔接——δ∞/C 连续性）
P3 过渡区 13..14（曲率→双曲）闭合
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUTP = os.path.join(BASE, "_phase102_p7_5e129_out.txt")

lines = []
def log(s=""):
    lines.append(s)
    print(s, flush=True)

fa = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
fb = json.load(open(os.path.join(BASE, "_phase102_p7_5e117_m32_scan.json"), encoding="utf-8"))
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))

# 组装权威表：m -> Bstar
B = {}
# 源 A
if isinstance(fa, dict) and "out" in fa:
    for k, v in fa["out"].items():
        m = -int(k)
        if isinstance(v, dict):
            for bk in ("R2", "Bstar", "Bstar0", "bstar"):
                if bk in v:
                    B[m] = v[bk]; break
    log("源 A keys sample: %s" % (list(fa["out"].keys())[:3]))
elif isinstance(fa, dict):
    log("源 A top keys: %s" % list(fa.keys())[:8])
    for k, v in fa.items():
        try:
            m = -int(k)
        except Exception:
            continue
        if isinstance(v, dict):
            for bk in ("Bstar", "Bstar0", "bstar"):
                if bk in v:
                    B[m] = v[bk]; break
# 源 B
for k, v in fb["out"].items():
    m = -int(k)
    B[m] = v["Bstar0"]
# 源 C
for k, v in fc["out"].items():
    m = -int(k)
    B[m] = v["Bstar"]

ms_all = sorted(B.keys())
log("三源合并点数：%d（m 范围 %d..%d）" % (len(ms_all), ms_all[0], ms_all[-1]))

def closed(m):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    if abs(m) == 1:
        cl += 1.0/65.0
    return cl

# P1 闭式命中表
log("=== P1 闭式命中（dev = 1/B* vs closed，单位 pct）===")
bad = []
for m in ms_all:
    cl = closed(m)
    ib = 1.0/B[m]
    dev = (cl - ib)/cl*100.0
    tag = ""
    if abs(dev) > 0.16:
        tag = "  ★>0.16"
        bad.append((m, dev))
    if m in (-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 64, 128, 256):
        log("  m=%4d  dev=%+.4f pct%s" % (m, dev, tag))
log("  超 0.16 点数：%d / %d" % (len(bad), len(ms_all)))
if bad:
    log("  超差 m 列表：%s" % [m for m, _ in bad])

# P2 中间段 15..32 vs 33..256 双曲衔接
def fit3(ms, delta):
    X = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
    c, _, _, _ = np.linalg.lstsq(X, delta, rcond=None)
    rms = float(np.sqrt(np.mean((X@c-delta)**2)))
    return c[0], -c[1], -c[2], rms

log("=== P2 双曲衔接：15..32 vs 33..256 ===")
for lo, hi in [(15, 32), (33, 128), (129, 256), (33, 256), (15, 256)]:
    msk = [m for m in ms_all if lo <= m <= hi]
    ms = np.array(msk, dtype=float)
    delta = np.array([closed(m) - 1.0/B[m] for m in msk])
    d, C, D, rms = fit3(ms, delta)
    log("  %2d..%3d：δ∞=%+.8f（vs 1/56 %+.4f pct）、C=%+.6f、D=%+.6f、RMS=%.1e" % (
        lo, hi, d, (d-1/56)/(1/56)*100, C, D, rms))

# P3 过渡区 13..14
log("=== P3 过渡区 13..14 逐点 ===")
for m in (13, 14, 15):
    cl = closed(m)
    ib = 1.0/B[m]
    log("  m=%d  δ(1/B)=cl-1/B*=%.8f、closed=%.8f" % (m, cl-ib, cl))

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("exit 0")
