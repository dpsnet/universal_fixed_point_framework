# -*- coding: utf-8 -*-
"""数值探索：d_H 与 Δφ=ln2 链的衔接（#68，数值内生层）

背景：Δφ=ln2 链已锁死（#64-66：4 步翻倍 ⟹ 2⁴=16 态 ⟹ 15=16−1 非标量层）。
d_H（静默分层框架常数，判别值 16259/6000≈2.709833）此前观察到与 ln15≈2.708050
差 0.066%。本探索检验 d_H 是否可由 Δφ 链组合内生（衔接候选），或保持判别值。

检验项目：
  E1  d_H vs ln15（非标量层 15）精确性
  E2  d_H vs ln16（全态 16）及 ln16−ln(16/15)=ln15 恒等
  E3  若 d_H=ln15：路径 A 目标 24(ln15+3) vs α⁻¹
  E4  若 d_H=ln15：静默窗口 e^{−d_H}=1/15（全锁定权重）
  E5  组合候选：d_H = ln15 + ε，ε 是否与已知锚（谱隙/Δφ/双向量数）成比
"""
import numpy as np

d_H = 16259 / 6000
ln15 = np.log(15)
ln16 = np.log(16)
gap = (np.sqrt(3) - 1) / 6
alpha_inv = 137.035999084

print("=== E1/E2：d_H 与 ln15/ln16 ===")
print(f"d_H          = {d_H:.10f}")
print(f"ln15         = {ln15:.10f}   d_H−ln15 = {d_H-ln15:.2e} 相对 {abs(d_H-ln15)/ln15*100:.4f}%")
print(f"ln16         = {ln16:.10f}   d_H−ln16 = {d_H-ln16:.4f}")
print(f"ln16−ln(16/15)= {ln16 - np.log(16/15):.10f}（恒等 = ln15）")
print()

print("=== E3：路径 A 目标若 d_H=ln15 ===")
print(f"24(d_H+3)     = {24*(d_H+3):.6f}（判别值口径，命中 α⁻¹）")
print(f"24(ln15+3)    = {24*(ln15+3):.6f}   vs α⁻¹={alpha_inv:.6f}：差 {24*(ln15+3)-alpha_inv:+.4f}（{abs(24*(ln15+3)-alpha_inv)/alpha_inv*100:.4f}%）")
print()

print("=== E4：静默窗口 ===")
print(f"e^{{−d_H}}      = {np.exp(-d_H):.6f} = 1/{np.exp(d_H):.4f}   vs 1/15={1/15:.6f}（差 {abs(np.exp(-d_H)-1/15)/(1/15)*100:.3f}%）")
print()

print("=== E5：ε = d_H−ln15 与已知锚的比值 ===")
eps = d_H - ln15
print(f"ε             = {eps:.8f}")
print(f"ε/Δλ_min      = {eps/gap:.4f}  (谱隙)   → 若 ε=Δλ_min/68.5 无意义")
print(f"ε/ln(16/15)   = {eps/np.log(16/15):.4f}  (修正项) → ≈1/36.2")
print(f"ε/Δφ         = {eps/np.log(2):.4f}  (翻倍步)")
print(f"36·ε          = {36*eps:.6f}  (若 ε=ln(16/15)/36?)")
print(f"ln(16/15)/36  = {np.log(16/15)/36:.8f}")
print(f"→ ε 与 ln(16/15)/36 差 {abs(eps-np.log(16/15)/36)/np.log(16/15)*100:.2f}%")
print()

print("=== 结论 ===")
print("E1-E4：d_H 与 ln15 差 0.066%（非精确恒等）；d_H=ln15 假说下路径 A 目标差 0.031%。")
print("E5：ε=d_H−ln15 与 ln(16/15)/36 差 ~0.5%（36=6²，双向量数 6 的平方）——接近但非精确。")
print("→ 无精确恒等。判定：d_H 保持判别值 16259/6000；'d_H≈ln15（非标量层衔接）'")
print("  登记为观察（方向咬合级接近），不立为精确链——避免凑数。")
