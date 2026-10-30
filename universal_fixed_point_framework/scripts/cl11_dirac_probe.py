# -*- coding: utf-8 -*-
"""数值先证伪：Cl(1,1) 生成元代数 + Dirac 平方（#49）

拟 Lean 定理逐字对齐：
  (a) e01_mul_e10_anticomm：e_01·e_10 = −(e_10·e_01)
  (b) cl11_commutator_generates_boost：[e_01,e_10]=2·Jprime（交换子=双曲生成元）
  (c) clifford_dirac_square：(E·e_10−p·e_01)²=(E²−p²)·1
  (d) clifford_dirac_mass_shell：E=m·coshφ、p=m·sinhφ ⟹ Dirac²=m²·1

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261026)
N_TRIALS = 500
TOL = 1e-8

e01 = np.array([[0.0, -1.0], [1.0, 0.0]])
e10 = np.array([[1.0, 0.0], [0.0, -1.0]])
Jp = np.array([[0.0, 1.0], [1.0, 0.0]])
I2 = np.eye(2)


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 反对易
worst = 0.0
worst = max(worst, np.abs(e01 @ e10 + e10 @ e01).max())
ok &= check("(a) e_01·e_10=−(e_10·e_01)", worst)

# (b) 交换子=双曲生成元
worst = 0.0
worst = max(worst, np.abs((e01 @ e10 - e10 @ e01) - 2 * Jp).max())
ok &= check("(b) [e_01,e_10]=2J'", worst)

# (c) Dirac 平方
worst = 0.0
for _ in range(N_TRIALS):
    E = rng.uniform(-10, 10)
    p = rng.uniform(-10, 10)
    D = E * e10 - p * e01
    worst = max(worst, np.abs(D @ D - (E**2 - p**2) * I2).max())
ok &= check("(c) (E·e_10−p·e_01)²=(E²−p²)·1", worst)

# (d) 质量壳 = Dirac 本征值
worst = 0.0
for _ in range(N_TRIALS):
    m = rng.uniform(0.1, 10)
    phi = rng.uniform(-2, 2)
    E = m * np.cosh(phi)
    p = m * np.sinh(phi)
    D = E * e10 - p * e01
    worst = max(worst, np.abs(D @ D - m**2 * I2).max())
ok &= check("(d) Dirac²=m²·1", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：Cl(1,1) 生成元代数+Dirac 平方全绿——时空双向量反对易、"
      + "交换子生成 boost（Δ⟹群作用时空层）、质量壳=Dirac 算符平方本征值。")
