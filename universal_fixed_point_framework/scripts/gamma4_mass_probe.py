# -*- coding: utf-8 -*-
"""数值先证伪：4×4 Dirac 质量方程代数层（#58，Cl(1,3) 完整签名）

D₄ = E·γ⁰ − p·γ¹（γ 矩阵用 #57 Dirac 表示，ℂ 4×4）
拟 Lean 定理：
  (a) diracOp4_sq：D₄² = (E²−p²)·1₄（Cl(1,3) 签名 Dirac 平方：
      γ⁰²=+1、γ¹²=−1、反对易项 −Ep(γ⁰γ¹+γ¹γ⁰)=0）
  (b) diracOp4_mass_shell：E=m·coshφ、p=m·sinhφ ⟹ D₄² = m²·1₄
      （4×4 质量=Dirac 算符平方本征值）
  (c) diracOp4_mass_factorization：壳上 (D₄+m·1)(m·1−D₄)=0
      （4×4 零因子分解：质量=Dirac 核 ±m，Π± 投影对的 Cl(1,3) 完整签名版）

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
I4c = np.eye(4, dtype=complex)

rng = np.random.default_rng(20261025)
N = 500
TOL = 1e-8


def D4(E, p):
    return E * g0 - p * g1


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
worst = 0.0
for _ in range(N):
    E, p = rng.uniform(-5, 5, 2)
    lhs = D4(E, p) @ D4(E, p)
    rhs = (E**2 - p**2) * I4c
    worst = max(worst, np.abs(lhs - rhs).max())
ok &= check("(a) D₄²=(E²−p²)·1（Cl(1,3) 签名 Dirac 平方）", worst)

worst = 0.0
for _ in range(N):
    m = rng.uniform(0.5, 5)
    phi = rng.uniform(-1.5, 1.5)
    E = m * np.cosh(phi)
    p = m * np.sinh(phi)
    lhs = D4(E, p) @ D4(E, p)
    rhs = (m**2) * I4c
    worst = max(worst, np.abs(lhs - rhs).max())
ok &= check("(b) 壳上 D₄²=m²·1（质量=Dirac 平方本征值）", worst)

worst = 0.0
for _ in range(N):
    m = rng.uniform(0.5, 5)
    phi = rng.uniform(-1.5, 1.5)
    E = m * np.cosh(phi)
    p = m * np.sinh(phi)
    lhs = (D4(E, p) + m * I4c) @ (m * I4c - D4(E, p))
    worst = max(worst, np.abs(lhs).max())
ok &= check("(c) 壳上 (D₄+m·1)(m·1−D₄)=0（零因子分解）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：4×4 Dirac 质量方程代数层全绿——Cl(1,3) 完整签名下 D₄²=(E²−p²)·1、"
      + "壳上 =m²·1、零因子分解成立：质量=Dirac 核 ±m 升级到 4 维标准表示，"
      + "两正交投影对的完整签名版地基。")
