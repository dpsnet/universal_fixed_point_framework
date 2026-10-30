# -*- coding: utf-8 -*-
"""数值先证伪：4×4 Dirac 完整动量版本（#61，Cl(1,3) 全动量）

D₄_full = γ⁰E − γ¹p₁ − γ²p₂ − γ³p₃（γ 矩阵 #57 Dirac 表示，ℂ 4×4）
拟 Lean 定理：
  (a) diracOp4full_sq：D_full² = (E²−p₁²−p₂²−p₃²)·1
      （完整 Clifford 关系：γ⁰²=+1、γⁱ²=−1、全交叉反对易消零）
  (b) diracOp4full_mass_shell：E²−p₁²−p₂²−p₃²=m² ⟹ D_full² = m²·1
      （相对论色散关系 E²=p²+m² 的 Dirac 算符表述）
  (c) diracOp4full_mass_factorization：壳上 (D_full+m·1)(m·1−D_full)=0
      （零因子分解：质量=Dirac 核 ±m 的全动量版）

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
I4c = np.eye(4, dtype=complex)

rng = np.random.default_rng(20261026)
N = 500
TOL = 1e-8


def Dfull(E, p1, p2, p3):
    return E * g0 - p1 * g1 - p2 * g2 - p3 * g3


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
worst = 0.0
for _ in range(N):
    E, p1, p2, p3 = rng.uniform(-5, 5, 4)
    lhs = Dfull(E, p1, p2, p3) @ Dfull(E, p1, p2, p3)
    rhs = (E**2 - p1**2 - p2**2 - p3**2) * I4c
    worst = max(worst, np.abs(lhs - rhs).max())
ok &= check("(a) D_full²=(E²−p₁²−p₂²−p₃²)·1（全动量 Dirac 平方）", worst)

worst = 0.0
for _ in range(N):
    m = rng.uniform(0.5, 5)
    p1, p2, p3 = rng.uniform(-3, 3, 3)
    E = np.sqrt(m**2 + p1**2 + p2**2 + p3**2)
    lhs = Dfull(E, p1, p2, p3) @ Dfull(E, p1, p2, p3)
    rhs = (m**2) * I4c
    worst = max(worst, np.abs(lhs - rhs).max())
ok &= check("(b) 壳上 D_full²=m²·1（相对论色散 E²=p²+m²）", worst)

worst = 0.0
for _ in range(N):
    m = rng.uniform(0.5, 5)
    p1, p2, p3 = rng.uniform(-3, 3, 3)
    E = np.sqrt(m**2 + p1**2 + p2**2 + p3**2)
    lhs = (Dfull(E, p1, p2, p3) + m * I4c) @ (m * I4c - Dfull(E, p1, p2, p3))
    worst = max(worst, np.abs(lhs).max())
ok &= check("(c) 壳上 (D_full+m·1)(m·1−D_full)=0（零因子分解）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：4×4 Dirac 完整动量版本全绿——γ⁰E−Σγⁱpᵢ 平方 = E²−p² 标量、"
      + "壳上 =m²·1（相对论色散 E²=p²+m² 的 Dirac 表述）、零因子分解成立："
      + "质量壳 = Dirac 算符零空间的全动量 Cl(1,3) 机检。")
