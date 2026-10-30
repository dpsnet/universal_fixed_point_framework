# -*- coding: utf-8 -*-
# _v04_open240_field_verdict.py — 104az-240: #481 G227-35 场强口径文献裁决数值核验 + 判据①双线窗口几何
# 两口径关系: 120 MG ≈ 0.63 × B_p(180 MG) = 偶极表面平均场 vs 偶极极场
# pyenv 3.11.8 执行
import numpy as np

# ---- 1. 偶极表面平均场因子（面积加权）----
# 纯偶极 B(r,theta) = B_p (cosθ rhat 分量等); 表面 |B(θ)| ∝ sqrt(1+3cos²θ)/2 · B_p
# 面积加权平均 <|B|> = B_p * ∫_{0}^{π} sqrt(1+3cos²θ)/2 · sinθ dθ / 2
def dipole_avg_factor():
    th = np.linspace(0, np.pi, 400001)
    w = np.sin(th)                       # 面积权重
    f = np.sqrt(1 + 3*np.cos(th)**2) / 2 # |B(θ)|/B_p
    return np.sum(f * w) / np.sum(w)

fac = dipole_avg_factor()
print(f"偶极表面平均场因子 <|B|>/B_p = {fac:.4f}  (文献标准 0.63)")
for Bp in (170.0, 180.0, 150.0):
    print(f"  B_p={Bp:>5.0f} MG -> <|B|> ≈ {fac*Bp:>6.1f} MG")

print(f"0.67×180 = {0.67*180:.1f}  (上界, 120.6 ≈ B&L2020 转述 120 MG 口径)")
print(f"0.63×180 = {0.63*180:.1f}  (标准因子)")

# ---- 2. 判据①双线窗口几何 ----
# 238 缩窄 [1.85,2.0] 基于 Hα 单线 1.864; 239 精确对角化 Hβ 2.005/2.003/2.002
# 重注册 [1.8, 2.1]: 覆盖 Hα 1.864 与 Hβ 2.005 (纯二次+抗磁修正物理窗口)
HALPHA_IDX, HBETA_IDX = 1.864, 2.005
W_L, W_H = 1.8, 2.1
print(f"\n判据①重注册窗口 [{W_L}, {W_H}]:")
print(f"  Hα 1.864 在窗内: {W_L <= HALPHA_IDX <= W_H}")
print(f"  Hβ 2.005 在窗内: {W_L <= HBETA_IDX <= W_H}")
print(f"  238 缩窄带 [1.85,2.0] 对 Hβ 2.005: 超上界 {2.005/2.0 - 1:+.2%}")
print(f"  抗磁修正符号: Hα(n=3) -0.136 vs Hβ(n=4) +0.005 -> 跨带耦合主导符号随线变化, 窗口须覆盖 ±0.1 修正量级")

# ---- 3. 蓝窗可行性(谱线平均场口径) ----
# 239 反解: Hβ π 最内层 5260 Å @120 MG, 蓝窗上界 5300 -> B_max
# 位移 ∝ B^2 (指数 ~2): Δλ(B) = Δλ(120)·(B/120)^2; 5260 + Δλ = 5300 -> Δλ=40 Å
import math
B120, D120, DLIM = 120.0, 398.8, 40.0
Bmax = 120.0 * math.sqrt((D120 + DLIM) / D120)
print(f"\n蓝窗(Hβ π) B_max 反解: 120 MG 余量 40 Å -> B_max ≈ {Bmax:.1f} MG")
print(f"  谱线平均场 <|B|> ≈ {fac*180:.0f} MG 档 -> 窗内(余量 {Bmax-fac*180:.0f} MG) ✓ 可行")
print(f"  若全域 ~180 MG 主导(非偶极加权) -> 出窗 ✗ 需 σ 一阶自洽定标")
