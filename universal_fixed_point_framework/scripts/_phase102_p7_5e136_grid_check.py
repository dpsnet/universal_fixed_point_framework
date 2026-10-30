# -*- coding: utf-8 -*-
"""
P7-5e-136：用户先验判别——21/28/32 = 3·7/4·7/4·8 网格结构检验
================================================================
用户观察（先验）：21/28/32 = 3·7、4·7、4·8——3=2²−1、4=2²、7=2³−1、8=2³ 全 2 幂组合
——被乘数 7→8 = 缺口域→满格域通道数跨乘；乘数 3→4 = (2²−1)→2²
P1 6 点网格 {2,3,4}×{7,8} = {14,16,21,24,28,32} 的 Δ_eff 与 1/56 占比
P2 可分离性判别：占比(m)=Δ_eff/D56 是否可分解 f(a·c)=g(a)h(c)（乘积律）？
P3 网格点 vs 1/m 幂律残差（132 的 1/56−Δ_eff≈2C/m 在网格点是否精确）
P4 框架解读：过渡带窗口标度 = k_max 家族乘积阶梯？
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
HALF = D56/2

def Deff(m):
    return (closed(m) - 1.0/B[m]) - C_FIX/m

print("=== P7-5e-136 网格结构检验 ===", flush=True)
grid = {"2x7=14": 14, "3x7=21": 21, "4x7=28": 28, "2x8=16": 16, "3x8=24": 24, "4x8=32": 32}
print("--- P1 6 点网格 Δ_eff / 占比 ---", flush=True)
rows = {}
for name, m in grid.items():
    d = Deff(m)
    rows[m] = d
    print("  %-7s m=%2d：Δ_eff=%.6f、1/56 占比 %5.1f pct、半高 1/112 占比 %5.1f pct" % (
        name, m, d, d/D56*100.0, d/HALF*100.0), flush=True)

print("--- P2 可分离性判别（占比是否 = g(a)·h(c)）---", flush=True)
pct = {m: rows[m]/D56 for m in rows}
# 7 列（c=7）：a=2,3,4 → 14,21,28；8 列（c=8）：16,24,32
c7 = [pct[14], pct[21], pct[28]]
c8 = [pct[16], pct[24], pct[32]]
r7 = [c8[i]/c7[i] for i in range(3)]
print("  7 列占比：14/21/28 = %.3f/%.3f/%.3f；8 列：16/24/32 = %.3f/%.3f/%.3f" % (c7[0], c7[1], c7[2], c8[0], c8[1], c8[2]), flush=True)
print("  列间比 r=8列/7列：%.3f/%.3f/%.3f——若可分离应三值相等" % (r7[0], r7[1], r7[2]), flush=True)
print("  行间比（乘数+1）：21/14=%.3f、28/21=%.3f、24/16=%.3f、32/24=%.3f——若可分离同乘数行间比应相等" % (
    pct[21]/pct[14], pct[28]/pct[21], pct[24]/pct[16], pct[32]/pct[24]), flush=True)

print("--- P3 网格点 vs 1/m 幂律残差（1/56−Δ_eff vs 2C/m）---", flush=True)
for name, m in grid.items():
    resid = D56 - rows[m]
    pred = 2.0*C_FIX/m
    print("  m=%2d：1/56−Δ_eff=%.6f vs 2C/m=%.6f——差 %+.2f pct" % (m, resid, pred, (resid-pred)/pred*100.0), flush=True)

print("--- P4 框架对照 ---", flush=True)
print("  21 = N_gen·(k_max−1) = 3·7；28 = 2²·(k_max−1)；32 = 2²·k_max = k_max²/2 = 2⁵", flush=True)
print("  56 = 7·8 = (k_max−1)·k_max 因子系 {1,2,4,7,8,14,28,56}——21 非因子（3·7 跨乘）", flush=True)
print("  32 = 2⁵ 呼应 121 的 1/32 = 2^{−(k_max−3)} 二进制倒数家族（c2 饱和项）", flush=True)
print("exit 0", flush=True)
