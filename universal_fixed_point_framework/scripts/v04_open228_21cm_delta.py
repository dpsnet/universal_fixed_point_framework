# -*- coding: utf-8 -*-
# 104az-228 21cm δ 残差精确重算与数值结构分析（pyenv 3.11.8）
# 背景：f_hfs/(c·R∞) = (16/3)·α²·(m_e/m_p)·(g_p/2)·(1+δ)（104az-143/145 框架化；151 判 δ 无身份）
# 本步：1) 两种口径（实测 g_p/2 vs 框架 40217/14400）反解 δ 精确值
#       2) δ 数值结构 × 框架量（53 = 7²+2²、371 = 7×53 等素数身份候选）扫描
import numpy as np
from fractions import Fraction

# CODATA 值（记忆）
c = 299792458.0          # m/s
Rinf = 10973731.568160   # m⁻¹
alpha = 1/137.035999084
me_mp = 1/1836.15267343
f_hfs_meas = 1420405751.768  # Hz（CODATA 1420.405751768 MHz）

# 两种 g_p/2 口径
gp2_meas = 2.79284734463
gp2_frame = 40217/14400  # 2.7928472222

def f_hfs(gp2):
    return (16/3)*alpha**2*me_mp*gp2*c*Rinf

def delta(gp2):
    return f_hfs_meas/f_hfs(gp2) - 1

print("=== 1. 21cm 链两种口径反解 δ ===")
f_meas_ratio = f_hfs_meas/(c*Rinf)
print(f"f_hfs/(c·R∞) 实测 = {f_meas_ratio:.12e}")
for name, gp2 in [("实测 g_p/2", gp2_meas), ("框架 40217/14400", gp2_frame)]:
    f = f_hfs(gp2)
    d = delta(gp2)
    print(f"  {name}: f_pred = {f:.6f} Hz → δ = {d:+.10e} ({d*1e2:+.6f}%)")

print()
print("=== 2. δ 数值结构分析 ===")
d1 = delta(gp2_meas)   # 实测口径 δ（不含 g_p/2 框架偏差）
d2 = delta(gp2_frame)  # 框架口径 δ（含 g_p/2 dev 4.4e-8 残差）
for name, d in [("δ(实测口径)", d1), ("δ(框架口径)", d2)]:
    print(f"{name} = {d:.12e}")
    print(f"  ×1e2 = {d*1e2:.9f}% | ×1e4 = {d*1e4:.9f} | ×1e5 = {d*1e5:.9f} | ×1e6 = {d*1e6:.9f}")
    # 53 素因子候选：δ ≈ -53e-5? -53e-4?
    print(f"  -1/19 = {-1/19:.10e} (1/19={1/19:.10e}) | -53e-4 = {-53e-4:.10e} | -1/18.9 ≈ {d*1e2:.4f}%")

print()
print("=== 3. 框架量组合候选（观察级，需负控）===")
# δ 精确值的候选框架表达（含 53=7²+2²、371=7×53 早期登记素数身份）
print("53 = 7²+2² ?", 7*7+2*2 == 53, "（早期登记：素数 + 371=7×53 观测锚）")
print("1/190 = ?", 1/190)
print("δ1(实测) ≈ −1/1886 ?", abs(d1 - (-1/1886)), "| −1/1900 ?", abs(d1 - (-1/1900)))
# 无框架身份基线：δ 是否可写成小整数倒数的有理近似
import math
for den in [100, 500, 1000, 1900, 1886, 2000, 10000]:
    approx = -1/den
    print(f"  -1/{den} = {approx:.8e}  与 δ1 差 = {abs(d1 - approx):.3e}")
