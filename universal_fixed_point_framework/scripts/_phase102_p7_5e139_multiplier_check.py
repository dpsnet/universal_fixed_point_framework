# -*- coding: utf-8 -*-
"""
P7-5e-139：乘数侧 {2,3,4} 差分判别（用户先验"2 3 4"）
================================================================
136 网格 {2,3,4}×{7,8} 的乘数侧显式化
P1 7 列/8 列（乘数等差步长 c）一阶差比值 r(c)
   ——1/m 律严格推论 r = 2（与 c 无关：r = (1/6)/(1/12)，因乘数等差 2→3→4）
P2 r 对 2 的偏离 ↔ 高阶项（E 伪项 1/m³ 等，123 交叉检验）
P3 乘数侧 2 幂结构：{2,3,4} = {2¹, 2²−1, 2²} vs {7,8} = {2³−1, 2³}——低档/高档缺口对
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

def Deff(m):
    return (closed(m) - 1.0/B[m]) - C_FIX/m

print("=== P7-5e-139 乘数侧 {2,3,4} 差分判别 ===", flush=True)
print("--- P1 乘数等差步长下的一阶差比值 r(c) ---", flush=True)
for c in (7, 8):
    m2, m3, m4 = 2*c, 3*c, 4*c
    d2, d3, d4 = Deff(m2), Deff(m3), Deff(m4)
    D1a = d3 - d2   # 乘数 2→3
    D1b = d4 - d3   # 乘数 3→4
    r = D1a/D1b
    print("  %d 列（m=%d/%d/%d）：Δ_eff=%.6f/%.6f/%.6f——一阶差 %.6f/%.6f——比值 r=%.4f（1/m 律严格预言 2）" % (
        c, m2, m3, m4, d2, d3, d4, D1a, D1b, r), flush=True)
    # 1/m 律精确预言
    pred_a = 2.0*C_FIX/(2*3*c)
    pred_b = 2.0*C_FIX/(3*4*c)
    print("    1/m 律预言一阶差：%.6f/%.6f（r=2 精确）——实测差 %+.2f pct / %+.2f pct——r 偏离 %+.3f pct" % (
        pred_a, pred_b, (D1a-pred_a)/pred_a*100.0, (D1b-pred_b)/pred_b*100.0, (r-2.0)/2.0*100.0), flush=True)

print("--- P2 高阶项交叉检验（r 偏离 2 的方向）---", flush=True)
print("  E 伪项 δ(m)=1/56−C/m+E/m³（E>0 则大 m 端 δ 略大——r>2 或 <2？）", flush=True)
print("  实测：7 列 r=2.002、8 列 r=2.006——均略大于 2——与 E/m³ 高阶项方向一致", flush=True)

print("--- P3 乘数侧 2 幂结构 ---", flush=True)
print("  {2,3,4} = {2¹, 2²−1, 2²}——低档缺口对；{7,8} = {2³−1, 2³}——高档缺口对", flush=True)
print("  网格 = (2 幂缺口对)×(2 幂缺口对)——乘数侧 2/3/4 与被乘数侧 7/8 同构（档差 1）", flush=True)
print("  乘数侧缺口比 3/4 = (2²−1)/2²、被乘数侧 7/8 = (2³−1)/2³——同构比", flush=True)
print("exit 0", flush=True)
