# -*- coding: utf-8 -*-
"""δ_P7 身份恒等验证（2026-10-25）

观察：δ_P7 = (E_τ−ln(16/15)/3)/16 − ln15
若 E_τ = E_τ^new = 16ln15 + (7/10)ln(16/15)，则代数上
  δ_P7 = [16ln15 + (7/10)ln1615 − ln1615/3]/16 − ln15
        = (7/10 − 1/3)·ln1615/16 = (11/30)·ln1615/16
即 δ_P7 不是独立量——它是 E_τ^new 反解口径下的代数恒等（11/30 = 7/10 − 1/3）。
此前登记的"δ_P7 vs (11/30)ln1615/16 差 0.17%"源于误用实验口径 E_τ(框架)，
E 的 ppm 级差经 /16 减 ln15 的"差值放大"在 δ 层放大到 0.17%。

本脚本：数值验证恒等 + 对比三种口径的 δ_P7。
"""
import numpy as np

ln15 = np.log(15)
ln1615 = np.log(16/15)
E_new = 16*ln15 + (7/10)*ln1615

M_Pl_fw = 1.221e22
M_Pl_pdg = 1.2209e22
m_tau = 1776.86
E_tau_fw = np.log(M_Pl_fw/m_tau)
E_tau_pdg = np.log(M_Pl_pdg/m_tau)

# 恒等验证：三路独立计算
lhs = (E_new - ln1615/3)/16 - ln15                      # 定义式（E_τ^new 反解）
rhs = (11/30)*ln1615/16                                  # 恒等候选
algebraic = (7/10 - 1/3)*ln1615/16                       # 代数展开
print("=== δ_P7 恒等验证（E_τ^new 口径） ===")
print(f"定义式 δ_P7(E_new) = {lhs:.12f}")
print(f"恒等候选 (11/30)ln1615/16 = {rhs:.12f}")
print(f"代数展开 (7/10−1/3)ln1615/16 = {algebraic:.12f}")
print(f"|定义式−恒等| = {abs(lhs-rhs):.3e}（数值零 ⟹ 代数恒等）")
print()

# 三种口径对比
d1 = (E_new - ln1615/3)/16 - ln15
d2 = (E_tau_fw - ln1615/3)/16 - ln15
d3 = (E_tau_pdg - ln1615/3)/16 - ln15
print("=== 三种口径 δ_P7 ===")
print(f"E_τ^new 口径：{d1:.9f}（= 恒等值，精确）")
print(f"E_τ(框架) 口径：{d2:.9f}（vs 恒等 差 {abs(d2-rhs)/rhs*100:.4f}%）")
print(f"E_τ(PDG)  口径：{d3:.9f}（vs 恒等 差 {abs(d3-rhs)/rhs*100:.4f}%）")
print()

# δ 放大镜效应：E 的 ppm 差 → δ 的 % 差
print("=== δ 放大镜效应（E 误差在 δ 层的放大） ===")
dE = E_new - E_tau_fw
print(f"ΔE = E_new−E(框架) = {dE:.3e}（{(dE)/E_tau_fw*1e6:+.2f} ppm）")
print(f"δ 层放大 = ΔE/16/δ = {abs(dE)/16/rhs*100:.3f}%（ppm 级 E 差 → 0.1% 级 δ 差）")
print()
print("结论：δ_P7 身份 = (11/30)·ln(16/15)/16 为 E_τ^new 反解代数恒等——")
print("      δ_P7 精确身份闭合（依赖 E_τ^new 成立）；0.17% 旧差为口径误用产物；")
print("      δ 剩余开放 = δ_α = 16259/6000−ln15（α 判别口径，独立量，无身份候选维持）。")
