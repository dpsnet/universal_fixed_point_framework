# -*- coding: utf-8 -*-
"""
P7-5e-131：渐近截距 1/8 机制判别——b_eff 滑动窗口稳定性（方法论规则 3）
=================================================================
P1 五参 b_eff 滑动窗口（窗 96 步 32，33..256）：b_eff 是否稳定 1/8（±1e-8 级）
P2 a_eff 同窗：维持 1/2？
P3 e_eff 同窗：e 是否稳定（稳定=有身份候选；漂移=段投影）
P4 常数身份双关（漂移形态 vs 阶跃）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUTP = os.path.join(BASE, "_phase102_p7_5e131_out.txt")

lines = []
def log(s=""):
    lines.append(s)
    print(s, flush=True)

fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))
B = {-(int(k)): v["Bstar"] for k, v in fc["out"].items()}
ms_all = sorted(B.keys())  # 33..256，224 点

def fit5(ms, ib):
    X = np.vstack([ms, np.ones_like(ms), 1.0/ms, 1.0/ms**2, 1.0/ms**3]).T
    c, _, _, _ = np.linalg.lstsq(X, ib, rcond=None)
    rms = float(np.sqrt(np.mean((X @ c - ib)**2)))
    return c, rms

def pct(v, ref):
    return (v - ref)/ref*100.0

log("=== P1/P2/P3 五参滑动窗口（窗 96 步 32，33..256）===")
ws, steps = 96, 32
starts = list(range(33, 33 + 224 - ws + 1, steps))
rows = []
for s in starts:
    e = s + ws - 1
    msk = [m for m in ms_all if s <= m <= e]
    ms = np.array(msk, dtype=float)
    ib = np.array([1.0/B[m] for m in msk])
    c, rms = fit5(ms, ib)
    rows.append((s, e, c, rms))
    log("  窗 %3d..%3d：a=%+.10f（1/2 %+.3e pct）、b=%+.10f（1/8 %+.3e pct）、c=%+.8f、d=%+.8f、e=%+.6f、RMS=%.1e" % (
        s, e, c[0], pct(c[0], 0.5), c[1], pct(c[1], 0.125), c[2], c[3], c[4], rms))

log("=== P4 漂移形态判别 ===")
bs = [r[2][1] for r in rows]
as_ = [r[2][0] for r in rows]
es = [r[2][4] for r in rows]
log("  b_eff 序列：%s" % ("、".join("%+.9f" % v for v in bs)))
log("  b_eff 极差=%.2e、vs m 斜率（线性回归）=%+.3e" % (max(bs)-min(bs), np.polyfit(np.arange(len(bs)), bs, 1)[0]))
log("  a_eff 极差=%.2e、斜率=%+.3e" % (max(as_)-min(as_), np.polyfit(np.arange(len(as_)), as_, 1)[0]))
log("  e_eff 序列：%s" % ("、".join("%+.5f" % v for v in es)))
log("  e_eff 极差=%.3f、斜率=%+.3f" % (max(es)-min(es), np.polyfit(np.arange(len(es)), es, 1)[0]))
log("  b_eff 与 1/8 最大偏移：%+.3e（相对 %+.4f pct）" % (max([abs(v-0.125) for v in bs]), pct(max([abs(v-0.125) for v in bs]), 0.125)))
log("exit 0")

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
