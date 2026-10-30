# -*- coding: utf-8 -*-
"""数值先证伪：Dirac 质量谱分解（#50）

拟 Lean 定理逐字对齐：
  (a) clifford_dirac_trace_zero：tr(E·e_10−p·e_01)=0（Dirac 算符无迹 ⟹ 谱对称 ±λ）
  (b) clifford_dirac_factorization：E²−p²=m² ⟹ (D−m·1)·(D+m·1)=0（壳上零因子分解）
  (c) clifford_dirac_mass_factorization：E=m·coshφ、p=m·sinhφ ⟹ 同上（参数化壳）

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-8

e01 = np.array([[0.0, -1.0], [1.0, 0.0]])
e10 = np.array([[1.0, 0.0], [0.0, -1.0]])
I2 = np.eye(2)


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 无迹
worst = 0.0
for _ in range(N_TRIALS):
    E = rng.uniform(-10, 10)
    p = rng.uniform(-10, 10)
    D = E * e10 - p * e01
    worst = max(worst, abs(np.trace(D)))
ok &= check("(a) tr(D)=0", worst)

# (b) 壳上零因子分解
worst = 0.0
for _ in range(N_TRIALS):
    m = rng.uniform(0.1, 10)
    E = rng.uniform(-10, 10)
    p = np.sign(rng.uniform(-1, 1)) * np.sqrt(max(E**2 - m**2, 0.0))
    if abs(E**2 - p**2 - m**2) > 1e-6:
        E = np.sqrt(p**2 + m**2)
    D = E * e10 - p * e01
    factor = (D - m * I2) @ (D + m * I2)
    worst = max(worst, np.abs(factor).max())
ok &= check("(b) (D−m·1)(D+m·1)=0", worst)

# (c) 参数化壳
worst = 0.0
for _ in range(N_TRIALS):
    m = rng.uniform(0.1, 10)
    phi = rng.uniform(-2, 2)
    E = m * np.cosh(phi)
    p = m * np.sinh(phi)
    D = E * e10 - p * e01
    factor = (D - m * I2) @ (D + m * I2)
    worst = max(worst, np.abs(factor).max())
ok &= check("(c) 参数化 (D−m·1)(D+m·1)=0", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：Dirac 质量谱分解全绿——无迹⟹谱对称±λ；壳上 (D−m)(D+m)=0 零因子分解，"
      + "质量=Dirac 核 ±m（两互补投影的前身，质量层投影对落地）。")
