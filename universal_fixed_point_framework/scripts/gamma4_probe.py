# -*- coding: utf-8 -*-
"""数值先证伪：4×4 Dirac γ 矩阵层（#57，Cl(1,3) 标准表示）

Dirac 表示（ℂ 4×4）：γ⁰=diag(1,1,−1,−1)、γⁱ=[[0,σⁱ],[−σⁱ,0]]
拟 Lean 定理：
  (a) gamma0_sq：γ⁰² = 1（时间生成元平方 +1）
  (b) gamma1_sq：γ¹² = −1（空间生成元平方 −1）
  (c) gamma0_gamma1_anticomm：γ⁰·γ¹+γ¹·γ⁰ = 0（时空反对易）
  (d) gamma1_gamma2_anticomm：γ¹·γ²+γ²·γ¹ = 0（空间间反对易）
  (e) 完整 Clifford 关系：γᵃγᵇ+γᵇγᵃ = 2·ηᵃᵇ（6 对全表，η=diag(1,−1,−1,−1)）

判据：残差 < 1e-8。
"""
import numpy as np

I2 = np.eye(2)
Z2 = np.zeros((2, 2))
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)

g0 = np.block([[I2, Z2], [Z2, -I2]])
g1 = np.block([[Z2, s1], [-s1, Z2]])
g2 = np.block([[Z2, s2], [-s2, Z2]])
g3 = np.block([[Z2, s3], [-s3, Z2]])
G = [g0, g1, g2, g3]
Eta = np.diag([1.0, -1.0, -1.0, -1.0])
I4c = np.eye(4, dtype=complex)


def check(name, resid):
    ok = resid < 1e-8
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
ok &= check("(a) γ⁰²=1", np.abs(g0 @ g0 - I4c).max())
ok &= check("(b) γ¹²=−1", np.abs(g1 @ g1 + I4c).max())
ok &= check("(c) γ⁰γ¹+γ¹γ⁰=0", np.abs(g0 @ g1 + g1 @ g0).max())
ok &= check("(d) γ¹γ²+γ²γ¹=0", np.abs(g1 @ g2 + g2 @ g1).max())
# (e) 完整 Clifford 表
worst = 0.0
for a in range(4):
    for b in range(4):
        lhs = G[a] @ G[b] + G[b] @ G[a]
        rhs = 2 * Eta[a, b] * I4c
        worst = max(worst, np.abs(lhs - rhs).max())
ok &= check("(e) γᵃγᵇ+γᵇγᵃ=2ηᵃᵇ（6 对全表）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：4×4 Dirac γ 矩阵层全绿——γ⁰²=+1（时间）、γⁱ²=−1（空间）、"
      + "时空/空间反对易、完整 Clifford 关系 γᵃγᵇ+γᵇγᵃ=2ηᵃᵇ：Cl(1,3) 标准表示机检。")
