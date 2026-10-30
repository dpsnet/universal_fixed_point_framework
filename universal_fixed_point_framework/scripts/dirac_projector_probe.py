# -*- coding: utf-8 -*-
"""数值先证伪：Dirac 质量投影对（#51）

拟 Lean 定理逐字对齐（D=E·e_10−p·e_01，E=m·coshφ、p=m·sinhφ，壳上 D²=m²·1）：
  (a) dirac_mass_projector_idem_plus：  (D+m·1)² = 2m·(D+m·1)   [Π₊²=Π₊ 分子版]
  (b) dirac_mass_projector_idem_minus： (m·1−D)² = 2m·(m·1−D)   [Π₋²=Π₋ 分子版；注意 Π₋=(m·1−D)/2m]
  (c) dirac_mass_projectors_annihilate： (D+m·1)(m·1−D) = 0     [Π₊Π₋=0]
  (d) dirac_mass_projectors_complement：(D+m·1)+(m·1−D) = 2m·1  [Π₊+Π₋=1]

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
worst_a = 0.0
worst_b = 0.0
worst_c = 0.0
worst_d = 0.0
for _ in range(N_TRIALS):
    m = rng.uniform(0.1, 10)
    phi = rng.uniform(-2, 2)
    E = m * np.cosh(phi)
    p = m * np.sinh(phi)
    D = E * e10 - p * e01
    Pp = D + m * I2          # Π₊ 分子
    Pm = m * I2 - D          # Π₋ 分子
    worst_a = max(worst_a, np.abs(Pp @ Pp - 2 * m * Pp).max())
    worst_b = max(worst_b, np.abs(Pm @ Pm - 2 * m * Pm).max())
    worst_c = max(worst_c, np.abs(Pp @ Pm).max())
    worst_d = max(worst_d, np.abs(Pp + Pm - 2 * m * I2).max())
ok &= check("(a) Π₊²=2m·Π₊（幂等分子版）", worst_a)
ok &= check("(b) Π₋²=2m·Π₋（幂等分子版）", worst_b)
ok &= check("(c) Π₊·Π₋=0（正交/湮灭）", worst_c)
ok &= check("(d) Π₊+Π₋=2m·1（互补）", worst_d)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：Dirac 质量投影对全绿——Π± 幂等、相互湮灭、互补覆盖 2m·1："
      + "质量壳上 Dirac 谱 ±m 的两正交互补投影（'两正交投影'在质量层的最终代数环）。")
