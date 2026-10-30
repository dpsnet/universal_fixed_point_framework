# -*- coding: utf-8 -*-
"""
P7-5e-175c: 41/2000 候选完整判别（静默单元家族）+ 分段稳定性（修正 delta 切片）
===============================================================================
175b 发现：固定 C=13/128、镜像母体下 D=-41/2000 RMS=3.93e-9 优于 -103/5000 的 9.80e-9（2.5 倍）。
且 103/5000 - 41/2000 = 1/10000 = n_max^-4（n_max=10=k_max+2）精确。
本步按用户方法论（候选必须过分段稳定性关）完整判别：
  1. 41/2000 vs 103/5000 镜像结构（D=-c、E=+c）零自由 RMS + 分段稳定性
  2. D 单侧（E 自由）判别：41/2000 vs 103/5000 的 D 值
  3. E 单侧（D 自由）判别
  4. D=-E 约束自由拟合下 D 精确值对照两候选
  5. 残差形复核：固定镜像后残差是否还有 1/m^4 结构（两种 D 候选）
"""
import numpy as np, json, os

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "_phase102_p7_5e175_delta63.json")) as f:
    d = json.load(f)
ms = np.array(d["m"]); delta = np.array(d["delta"])
n = len(ms)
C13 = -13.0/128.0
inv56 = 1.0/56.0

def rms_of(dv, basev):
    return float(np.sqrt(np.mean((dv - basev)**2)))

def fit(dv, ms_, cols):
    A = np.vstack(cols(ms_)).T
    c, _, _, _ = np.linalg.lstsq(A, dv, rcond=None)
    resid = dv - A@c
    return c, float(np.sqrt(np.mean(resid**2)))

mA = lambda m: (1.0/m**2 - 1.0/m**3)   # 镜像母体
c41 = 41.0/2000.0
c103 = 103.0/5000.0

print("== P7-5e-175c 41/2000 vs 103/5000 完整判别（%d 点 m=33..%d）==" % (n, int(ms[-1])), flush=True)

print("\n-- 1. 零自由镜像结构 RMS（C=13/128, D=-c, E=+c）--")
print("   c=41/2000 : RMS=%.3e" % rms_of(delta, inv56 + C13/ms + (-c41)*mA(ms)))
print("   c=103/5000: RMS=%.3e" % rms_of(delta, inv56 + C13/ms + (-c103)*mA(ms)))

print("\n-- 2. 分段稳定性（镜像零自由，m>=lo 段）--")
for lo in [33, 129, 257, 513]:
    sel = ms >= lo
    r41 = rms_of(delta[sel], inv56 + C13/ms[sel] + (-c41)*mA(ms[sel]))
    r103 = rms_of(delta[sel], inv56 + C13/ms[sel] + (-c103)*mA(ms[sel]))
    print("   m>=%4d（%3d 点）41/2000 RMS=%.3e | 103/5000 RMS=%.3e | 比=%.2f" %
          (lo, int(sel.sum()), r41, r103, r41/r103))

print("\n-- 3. D 单侧判别（固定 C=13/128、E 自由）--")
for dn, dv in [("41/2000", c41), ("103/5000", c103)]:
    c, rms = fit(delta, ms, lambda m, dv=dv: [np.ones_like(m), 1.0/m, dv*(1.0/m**2 - 1.0/m**3), 1.0/m**3])
    # cols: [1, 1/m, c*(1/m^2-1/m^3), E/m^3]——c 固定后 E 自由
    print("   固定D=-%-8s（E 自由）: C=%+.10f  E=%+.7f  RMS=%.3e" % (dn, c[1], c[3], rms))

print("\n-- 4. D=-E 约束自由（C 固定 13/128）--")
c, rms = fit(delta, ms, lambda m: [np.ones_like(m), 1.0/m, (1.0/m**2 - 1.0/m**3)])
print("   C 固定时镜像系数 D 约束拟合: D=%+.7f（41/2000 差 %+.3f pct, 103/5000 差 %+.3f pct） RMS=%.3e" % (
    c[2], (c[2]+c41)/c41*100, (c[2]+c103)/c103*100, rms))

print("\n-- 5. 固定镜像后残差形（1/m^4 泄漏判别）--")
for dn, dv in [("41/2000", c41), ("103/5000", c103)]:
    resid = delta - (inv56 + C13/ms + (-dv)*mA(ms))
    cf, rms = fit(resid, ms, lambda m: [1.0/m**4])
    print("   c=%-9s 固定镜像残差拟合 F/m^4: F=%+.7f  RMS=%.3e" % (dn, cf[0], rms))

print("\n-- 6. 全自由四参复核（对照 174c）--")
c, rms = fit(delta, ms, lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3])
print("   自由: C=%+.10f  D=%+.7f  E=%+.7f  RMS=%.3e" % (c[1], c[2], c[3], rms))
print("   D 与 41/2000 差 %+.3f pct；与 103/5000 差 %+.3f pct" %
      ((c[2]+c41)/c41*100, (c[2]+c103)/c103*100))
print("   E 与 41/2000 差 %+.3f pct；与 103/5000 差 %+.3f pct" %
      ((c[3]-c41)/c41*100, (c[3]-c103)/c103*100))
print("exit 0", flush=True)
