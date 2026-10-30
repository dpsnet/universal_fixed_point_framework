# -*- coding: utf-8 -*-
"""
P7-5e-175b: 镜像母体固定检验（符号修正版，读 175 json）
=======================================================
174e 报告固定镜像（C=13/128, D=-103/5000, E=+103/5000）RMS=9.8e-9。
175 第 1 部分符号 bug（+D 而非 -D）作废。本步：
  1. 复现 174e 固定镜像 RMS（应 = 9.8e-9）
  2. 零自由参数母体对照：镜像(A) vs 1/(m(m+1))(B) vs 1/(m^2-1)(C)
  3. D 候选对照：103/5000 vs 41/2000 vs 47/2500 vs 13/625（均取 - 号）
  4. 分段稳定性：固定结构在 m>=64 / 128 / 256 / 512 的 RMS 是否稳定
"""
import numpy as np, json, os

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "_phase102_p7_5e175_delta63.json")) as f:
    d = json.load(f)
ms = np.array(d["m"]); delta = np.array(d["delta"])

C13 = -13.0/128.0
inv56 = 1.0/56.0

def rms_of(basev):
    return float(np.sqrt(np.mean((delta - basev)**2)))

print("== P7-5e-175b 固定检验（符号修正）==")
print("  63 点 m=33..1024 step16, delta 同 175 json", flush=True)

# 1. 复现 174e
mA = lambda m: (1.0/m**2 - 1.0/m**3)
mB = lambda m: 1.0/(m*(m+1.0))
mC = lambda m: 1.0/(m*m - 1.0)

print("\n-- 1. 固定 C=13/128、D=-103/5000（174e 复现）--")
print("   镜像 (1/m^2-1/m^3): RMS=%.3e（174e 报 9.8e-9）" %
      rms_of(inv56 + C13/ms + (-103.0/5000.0)*mA(ms)))
print("   1/(m(m+1)):         RMS=%.3e" %
      rms_of(inv56 + C13/ms + (-103.0/5000.0)*mB(ms)))
print("   1/(m^2-1):          RMS=%.3e" %
      rms_of(inv56 + C13/ms + (-103.0/5000.0)*mC(ms)))

print("\n-- 2. D 候选零自由对照（母体=镜像，174e 口径）--")
Dcand = {"103/5000": 103.0/5000.0, "41/2000": 41.0/2000.0,
         "47/2500": 47.0/2500.0, "13/625": 13.0/625.0,
         "53/2575": 53.0/2575.0, "1/48.54": 1.0/48.54}
for dn, dv in Dcand.items():
    print("   D=%-9s RMS=%.3e" % (dn, rms_of(inv56 + C13/ms + (-dv)*mA(ms))))

print("\n-- 3. 母体=1/(m(m+1))，D 候选零自由对照 --")
for dn, dv in Dcand.items():
    print("   D=%-9s RMS=%.3e" % (dn, rms_of(inv56 + C13/ms + (-dv)*mB(ms))))

print("\n-- 4. 分段稳定性（固定 C=13/128、D=-103/5000、镜像）--")
for lo in [33, 64, 128, 256, 512, 768]:
    sel = ms >= lo
    print("   m>=%4d（%3d 点）RMS=%.3e" % (lo, int(sel.sum()),
          rms_of(inv56 + C13/ms[sel] + (-103.0/5000.0)*mA(ms[sel]))))
print("\n-- 5. 分段稳定性（母体=1/(m(m+1))）--")
for lo in [33, 64, 128, 256, 512, 768]:
    sel = ms >= lo
    print("   m>=%4d（%3d 点）RMS=%.3e" % (lo, int(sel.sum()),
          rms_of(inv56 + C13/ms[sel] + (-103.0/5000.0)*mB(ms[sel]))))
print("exit 0", flush=True)
