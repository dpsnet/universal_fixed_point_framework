# -*- coding: utf-8 -*-
"""d_H 四候选殊途同归裁决数值核验（开放项① 合流：ln15 路径 + 三候选矩阵）

候选：
  C-A 16259/6000=(2^14−2^7+3)/6000  α+m_τ 双观测链最优
  C-B 65/24=(k_max/N_gen)(1+1/k_max²)   框架内自洽（双谱隙点最近）
  C-C √(22/3)                            已排除（−0.056% 且无身份）
  C-D ln15=2.708050    Moran 方程 B·r^d=1（B=15 分支计数、r=e⁻¹）——内生链全机检

判据：
  K1 内生链完整性（B 的来源：Sp 分支计数 vs Clifford 非标量层 15=16−1）
  K2 α 链命中 24(d+3)
  K3 双谱隙自洽点 d_H*=2.708258（104az-152）
  K4 m_τ 链（跨链最优）
"""
import numpy as np

a_inv = 137.035999084
cA = 16259/6000
cB = 65/24
cC = np.sqrt(22/3)
cD = np.log(15)
d_star = 2.708258
ln16_15 = np.log(16/15)

print("=== 四候选 ===")
for name, v in [("A 16259/6000", cA), ("B 65/24", cB), ("C √(22/3)", cC), ("D ln15", cD)]:
    print(f"{name} = {v:.9f}")

print()
print("=== K1：B=15 的双内生锚 ===")
print("  锚1：Sp 4-范畴分支计数 B=15（BranchCounting.lean B_eq_15 机检）")
print("  锚2：Cl(1,3) 非标量层 15=16−1（MinkowskiBoost.lean cl13_non_scalar_word_count 机检，Δφ=ln2 链）")
print("  → 15 双锚同指：分支计数层与 Clifford 计数层独立收敛同一结构数")

print()
print("=== K2：α 链命中 24(d+3) vs α⁻¹ ===")
for name, v in [("A 16259/6000", cA), ("B 65/24", cB), ("C √(22/3)", cC), ("D ln15", cD)]:
    val = 24*(v+3)
    rel = abs(val - a_inv)/a_inv*100
    print(f"  24({name:>11}+3) = {val:.9f}  相对差 {rel:.4f}%")

print()
print("=== K3：双谱隙自洽点 d_H*=2.708258 ===")
for name, v in [("A 16259/6000", cA), ("B 65/24", cB), ("D ln15", cD)]:
    print(f"  {name:>11} 差 {abs(v-d_star)/d_star*100:.4f}%")

print()
print("=== K4：m_τ 链（跨链） ===")
print("  A 为 α+m_τ 双观测链 1e-6% 级（104az-152 已裁决）；D 无 m_τ 表达（未合流）")

print()
print("=== 修正 ε：判别值与内生主项的差 ===")
epsA = cA - cD
print(f"  ε_A = 16259/6000 − ln15 = {epsA:.9f}")
print(f"  ε_A vs ln(16/15)/36 = {ln16_15/36:.9f}：差 {abs(epsA-ln16_15/36)/(ln16_15/36)*100:.2f}%")
print(f"  16259 = 2^14−2^7+3 = 128·127+3（127=2^7−1 梅森素数）")
print(f"  6000 = 2^4·3·5^3（5=3-4-5 勾股斜边=Δφ 链一步速度分母）")

print()
print("=== 判据汇总 ===")
print("  A：K2 α 命中 7e-9（王者）、K4 双观测链最优；K1 无机制（反解有理化）；K3 差 0.058%")
print("  B：K2 137 整数（0.026%）、K3 0.003%（最接近双谱隙点）；K1 机制半开放")
print("  C：已排除（104az-152）")
print("  D：K1 三锚闭环（分支计数+Moran+Clifford 非标量 15）；K2 0.0312%；K3 0.0077%")
