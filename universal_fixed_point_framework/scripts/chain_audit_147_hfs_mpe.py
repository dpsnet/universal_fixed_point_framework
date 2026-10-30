# -*- coding: utf-8 -*-
"""
chain_audit_147_hfs_mpe.py — 待办4+5 联动：
A) 21cm δ 残差精算 + 框架身份搜索（g_p/2 用锁定级 40217/14400）
B) m_p/m_e 小数部 0.1527 修正搜索
"""
import math, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ============ A) 21cm 链路 ============
print("========== A) 21cm 超精细分裂链路 ==========")
f_hfs = 1420405751.7667      # Hz CODATA 2022
c = 299792458.0              # m/s
Rinf = 10973731.568160       # m^-1
alpha = 1/137.035999084      # CODATA 2022
me_mp = 1/1836.15267343      # m_e/m_p
gp2_obs = 2.79284734463      # CODATA g_p/2
gp2_frame = 40217/14400      # 框架锁定表达

obs_ratio = f_hfs / (c * Rinf)
print(f"观测 f_hfs/(c·R∞) = {obs_ratio:.12e}")

for name, gp2 in [("观测 g_p/2", gp2_obs), ("框架 40217/14400", gp2_frame)]:
    K = 16/3
    fw = K * alpha**2 * me_mp * gp2
    delta = (obs_ratio / fw - 1) * 100
    print(f"{name}: 框架值 = {fw:.12e}  观测偏差 δ = {delta:+.5f}%")

# 用框架 g_p/2 精算 δ
fw = (16/3) * alpha**2 * me_mp * gp2_frame
delta = obs_ratio / fw - 1
print(f"\nδ（框架 g_p/2）= {delta:.9e} = {delta*100:+.5f}%")

# δ 框架身份搜索：−σ²、−α/π·1/2 已排除；搜索 1/D 与 σ 幂组合（δ 为负，用 |δ| 比较）
print("\nδ 候选（1/D 与 σ 组合，目标 |δ| = {:.3e}）：".format(abs(delta)))
cands = []
for D in range(1800, 2001):
    v = 1/D
    dev = (abs(v)/abs(delta) - 1)*100
    if abs(dev) < 0.5:
        cands.append((abs(dev), D, v, dev))
cands.sort()
for ad, D, v, d in cands[:8]:
    print(f"  1/{D} = {v:.6e}  dev vs |δ| {d:+.4f}%")
if not cands:
    print("  1/D 家族无 <0.5% 命中")

# 组合搜索：-σ²·r、-σ³·r、α/π 修正
sig = 1/15
combos = []
for r_num in [2,3,4,5,7,8,16,25,49,64]:
    for r_den in [1,2,3,4,5,7,8,16,25,49,64]:
        r = r_num/r_den
        for base_name, base in [("σ²", sig**2), ("σ³", sig**3), ("σ", sig), ("α/π", alpha/math.pi)]:
            v = base * r
            dev = (v/delta - 1)*100
            if abs(dev) < 1.5:
                combos.append((abs(dev), f"{base_name}·{r_num}/{r_den}", v, dev))
combos.sort()
print("\nσ 幂/απ×框架比组合：")
for ad, name, v, d in combos[:15]:
    print(f"  {name} = {v:.6e}  dev {d:+.4f}%")

# ============ B) m_p/m_e 小数部 ============
print("\n\n========== B) m_p/m_e = 1836.15267343 小数部修正 ==========")
mpme = 1836.15267343
main = 3*7*8*11 - 3*4   # 1836 主结构
frac = mpme - main      # 0.15267343
print(f"主结构 1836 = 3·7·8·11−3·4；小数部 = {frac:.10f}")

# 平滑分母搜索小数部
smooth = set()
for i2 in range(15):
    for i3 in range(10):
        for i5 in range(6):
            for i7 in range(5):
                n = 2**i2 * 3**i3 * 5**i5 * 7**i7
                if 0 < n <= 4000:
                    smooth.add(n)
best = []
for b in sorted(smooth):
    a = round(frac * b)
    v = a/b
    err = abs(v - frac)
    best.append((err, a, b, v))
best.sort()
print(f"\n小数部最优平滑有理近似（7-平滑分母≤4000）：")
for err, a, b, v in best[:10]:
    print(f"  {a}/{b} = {v:.10f}  err={err:.3e}  dev={(v/frac-1)*100:+.5f}%")

# 框架量组合候选
print("\n小数部框架量候选：")
fc = []
for num in [3,4,5,7,8,9,11,13,15,16,21,25,49]:
    for den in [45,64,72,90,96,100,120,128,144,150,160,180,192,200,216,224,225,240,250,256,270,288,300,320,336,360,375,384,400,448,450,480,512,576,600,625,640,675,700,720,768,800,864,900,960,1000,1024,1125,1152,1200,1250,1280,1440,1500,1600,1728,1800,1920,2000,2048,2160,2250,2304,2400,2500,2560,2700,2880,3000,3072,3200,3375,3456,3600,3750,3840,4000]:
        v = num/den
        dev = (v/frac - 1)*100
        if abs(dev) < 1:
            fc.append((abs(dev), f"{num}/{den}", v, dev))
fc.sort()
for ad, name, v, d in fc[:15]:
    print(f"  {name} = {v:.8f}  dev {d:+.4f}%")
