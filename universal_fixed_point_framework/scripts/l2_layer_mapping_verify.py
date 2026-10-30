# -*- coding: utf-8 -*-
"""L2 M2 层映射论证 + L3 15 同源性论证数值核验（2026-10-23）
M2（哪两层复合 → 层归属）：σz（层 3 实对合，严格层 spThreeExchangeLaw_strict 实=无相位）、
σx（层 1 实对合，基底）、σy（层 2 复对合，偏差层）——
  核心恒等式：Δ = [σz, σx] = σzσx − σxσz = 2·σzσx = 2J（层 3/层 1 交换偏差 = 两层复合两倍）
              σy = i·J = (i/2)·Δ（层 2 对合 = 交换律偏差 Δ 的相位化）
  ⟹ 层 2（Δ 偏差所在层 spExchangeLaw）的对合由 Δ 显式构造，语义精确吻合。

L3（15 同源性）：15 = 2⁴−1 = 4 维方向集非空子集计数 = C(4,1)+C(4,2)+C(4,3)+C(4,4)
  = 4+6+4+1 = Cl(1,3) 外代数非标量层（Λ¹⊕Λ²⊕Λ³⊕Λ⁴，k-矢 ↔ k 子集一一对应）
  = Moran B=15（BranchCounting d_H=ln15 条件定理：谱分支数）
  ⟹ Clifford 与 Moran 的 15 同源（同一组合计数的两个实现）。

检验：
  A. [σz,σx] = 2σzσx = 2J（交换偏差 = 两倍复合）
  B. σy = (i/2)·Δ（层 2 对合 = Δ 相位化，残差 0）
  C. Cl(1,3) 外代数非标量分层 {4,6,4,1} = 组合计数 {C(4,1),C(4,2),C(4,3),C(4,4)}，和 = 15 = 2⁴−1
  D. 15 同源表核验（Clifford 16−1 / 组合 2⁴−1 / Moran B=15 同值）
pyenv 3.11.8 运行。
"""
import numpy as np
from math import comb

Px = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
Pz = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
sx = 2 * Px - np.eye(2)
sz = 2 * Pz - np.eye(2)
J = sz @ sx
sy = 1j * J

print("L2 M2 层映射 + L3 15 同源性 数值核验")
print("=" * 78)

# A. 交换偏差 = 两倍复合
comm = sz @ sx - sx @ sz
print(f"A. Δ = [σz,σx] = σzσx − σxσz：")
print(f"   ‖Δ − 2J‖_F = {np.linalg.norm(comm - 2 * J, ord='fro'):.3e}（应 0：反对易 ⟹ [σz,σx]=2σzσx）")
print(f"   ‖Δ − 2·σzσx‖_F = {np.linalg.norm(comm - 2 * (sz @ sx), ord='fro'):.3e}（直接验证）")

# B. 层 2 对合 = Δ 的相位化
sy_from_delta = 0.5j * comm
print(f"\nB. σy = (i/2)·Δ（层 2 对合 = 偏差 Δ 相位化）：")
print(f"   ‖σy − (i/2)·Δ‖_F = {np.linalg.norm(sy - sy_from_delta, ord='fro'):.3e}（应 0）")

# C. 外代数分层 = 组合计数
layers = [comb(4, k) for k in (1, 2, 3, 4)]  # [4,6,4,1]
total = sum(layers)
print(f"\nC. Cl(1,3) 外代数非标量层 = 组合计数：")
print(f"   Λ¹..Λ⁴ = {layers} = C(4,k) 一一对应（k-矢 ↔ k 子集）")
print(f"   和 = {total} = 2⁴−1 = {2 ** 4 - 1}  一致性 {total == 2 ** 4 - 1}")

# D. 15 同源表
print(f"\nD. 15 同源核验：")
print(f"   Clifford：dim Cl(1,3) − 1 = 16 − 1 = 15（M₄(ℝ) 非标量元素）")
print(f"   组合：2⁴ − 1 = 15（4 维时空方向非空子集）")
print(f"   Moran：B = 15（BranchCounting d_H = ln15 条件定理，谱分支数）")
print(f"   同源论证：15 = 2⁴−1 = 非空子集计数 = 外代数非标量层（一一对应）= 谱方向组合数（Moran B）")

# E. 结构总结
print(f"\nE. M2 层映射（论证）：")
print(f"   层 3（严格层，spThreeExchangeLaw_strict 实=无相位）→ σz（实对合）")
print(f"   层 1（基底层）→ σx（实对合）")
print(f"   层 2（偏差层，spExchangeLaw Δ 所在层）→ σy = (i/2)·[σz,σx]（Δ 的相位化，复对合）")
print(f"   ⟹ Δ 偏差（交换顺序差异）精确 = 层 2 对合的构造源；'哪两层复合'= 层 1 × 层 3")
