# -*- coding: utf-8 -*-
"""
P7-5e-126a：D_tail=57/10⁴ 分段稳定性检验（方法论关——123 确立的候选规则）
================================================================
129..256 段拆两子段：129..192 vs 193..256——两子段三参 D 是否均 ~0.0057
  P1a 两子段 D 偏差 <10%（对 0.0057）→ 57/10⁴ 分段支持
  P1b 两子段 D 互相偏差 <20% → 段内 D 稳定
数据源：scripts\_phase102_p7_5e124_spectral_m256.json
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))
out = j["out"]

def seg_fit(lo, hi):
    ms = np.array([abs(int(k)) for k in out if lo <= -int(k) <= hi], dtype=float)
    invB = np.array([1.0/out[k]["Bstar"] for k in out if lo <= -int(k) <= hi])
    order = np.argsort(ms); ms = ms[order]; invB = invB[order]
    cl = ms/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**ms)
    delta = cl - invB
    X3 = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
    c3, _, _, _ = np.linalg.lstsq(X3, delta, rcond=None)
    rms = float(np.sqrt(np.mean((X3@c3-delta)**2)))
    return c3[0], -c3[1], -c3[2], rms

d1, C1, D1, r1 = seg_fit(129, 192)
d2, C2, D2, r2 = seg_fit(193, 256)
print("129..192 三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (d1, C1, D1, r1), flush=True)
print("193..256 三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (d2, C2, D2, r2), flush=True)
dev1 = abs(D1-0.0057)/0.0057*100
dev2 = abs(D2-0.0057)/0.0057*100
print("P1a 子段 D vs 57/10⁴：129..192 %+.4f pct、193..256 %+.4f pct（判据<10）→ %s" % (
    dev1, dev2, "过" if dev1 < 10 and dev2 < 10 else "★ 未过"), flush=True)
dev12 = abs(D1-D2)/D2*100
print("P1b 子段 D 互差：%+.4f pct（判据<20）→ %s" % (dev12, "过" if dev12 < 20 else "★ 未过"), flush=True)
# δ∞/C 子段稳定性对照
print("δ∞ 子段差：%+.4f pct；C 子段差：%+.4f pct" % (abs(d1-d2)/d2*100, abs(C1-C2)/C2*100), flush=True)
print("exit 0", flush=True)
