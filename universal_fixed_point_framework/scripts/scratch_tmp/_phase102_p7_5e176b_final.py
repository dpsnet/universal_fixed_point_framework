# -*- coding: utf-8 -*-
"""P7-5e-176b: 176 收尾细化
1. m>=33 段（避开过渡带）固定候选后 F/m^4 拟合 → 与 175c 的 -1/32 协调
2. m=257..512 vs 513+ 分段细化：确认"反转"是否判别力耗尽（噪声）
3. 判别力论证：两候选模型差 (1/10^4)(1/m^2-1/m^3) vs 提取噪声随 m 演化
"""
import numpy as np, json, os

base = os.path.dirname(os.path.abspath(__file__))
def load(name):
    with open(os.path.join(base, name)) as f:
        d = json.load(f)
    return np.array(d["m"]), np.array(d["delta"])

msL, dL = load("_phase102_p7_5e176_delta_lowm.json")
msH, dH = load("_phase102_p7_5e175_delta63.json")
ms = np.concatenate([msL, msH]); dv = np.concatenate([dL, dH])

C13 = -13.0/128.0; inv56 = 1.0/56.0
c41 = 41.0/2000.0; c103 = 103.0/5000.0
mA = lambda m: 1.0/m**2 - 1.0/m**3
fit = lambda dv, ms, cols: np.linalg.lstsq(np.vstack(cols(ms)).T, dv, rcond=None)[0]
rms = lambda r: float(np.sqrt(np.mean(r**2)))

print("== P7-5e-176b 收尾细化 ==")

# 1. m>=33 段 F/m^4（避开 17..32 过渡带）
print("\n-- 1. F/m^4 判别（m=33..128 段，固定候选）--")
sel = (ms >= 33) & (ms < 129)
for tag, c in [("41/2000", c41), ("103/5000", c103)]:
    resid = dv[sel] - (inv56 + C13/ms[sel] + (-c)*mA(ms[sel]))
    F = fit(resid, ms[sel], lambda m: [1.0/m**4])[0]
    print("   c=%-8s F=%+.7f（1/32=%+.7f, 差 %+.2f pct）RMS=%.3e" %
          (tag, F, -1.0/32.0, (F+1.0/32.0)/(1.0/32.0)*100, rms(resid)))

# 2. m=257..512 vs 513+ 细化（用 175 json）
print("\n-- 2. 大 m 段细化（两候选 RMS 比；<1=41 优）--")
for lo, hi in [(257, 513), (513, 10**6), (257, 10**6)]:
    s = (ms >= lo) & (ms < hi)
    if s.sum() == 0: continue
    r41 = rms(dv[s] - (inv56 + C13/ms[s] + (-c41)*mA(ms[s])))
    r103 = rms(dv[s] - (inv56 + C13/ms[s] + (-c103)*mA(ms[s])))
    print("   m=%4d..%-5d（%3d 点）41 RMS=%.3e | 103 RMS=%.3e | 比=%.3f" %
          (lo, hi-1 if hi < 10**6 else hi, int(s.sum()), r41, r103, r41/r103))

# 3. 判别力论证：模型差 vs 噪声
print("\n-- 3. 判别力：两候选模型差 (1/10^4)(1/m^2-1/m^3) vs 段噪声 --")
for mref in [33, 65, 129, 257, 513, 769]:
    moddiff = (1.0/1e4)*mA(mref)
    s = (ms >= mref) & (ms < mref*2 if mref*2 > mref else mref+1)
    # 段噪声：41 固定后残差 RMS 作为噪声估计（m>=33 全段）
    s2 = (ms >= 33) & (ms < 10**6)
    noise = rms(dv[s2] - (inv56 + C13/ms[s2] + (-c41)*mA(ms[s2])))
    print("   m=%4d: 模型差=%.2e | 提取噪声~%.2e | 信噪比=%.2f %s" %
          (mref, moddiff, noise, moddiff/noise,
           "可判别" if moddiff > 3*noise else "判别力耗尽"))

# 4. 过渡带确认：m=17..32 结构残差量级（对渐近展开）
print("\n-- 4. m=17..32 过渡带残差（41 固定）——确认不可并入渐近 --")
s = ms <= 32
resid = dv[s] - (inv56 + C13/ms[s] + (-c41)*mA(ms[s]))
for m, r in zip(ms[s], resid):
    print("   m=%4d  r=%+.2e" % (int(m), r))

# 5. D 终值（m>=33 四参）与候选距离
print("\n-- 5. D/E 终值（m>=33, 110 点自由四参）--")
sel = ms >= 33
c = fit(dv[sel], ms[sel], lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3])
print("   C=%+.9f  D=%+.7f（41 距 %+.2f pct, 103 距 %+.2f pct）  E=%+.7f  RMS=%.3e" %
      (c[1], c[2], (c[2]+c41)/c41*100, (c[2]+c103)/c103*100, c[3],
       rms(dv[sel] - (np.vstack([np.ones_like(ms[sel]), 1.0/ms[sel], 1.0/ms[sel]**2, 1.0/ms[sel]**3]).T @ c))))
print("exit 0", flush=True)
