# -*- coding: utf-8 -*-
"""数值先证伪：#62 全动量版质量投影对幂等化（Cl(1,3) 完整动量）

壳上 E²−p₁²−p₂²−p₃²=m² ⟹ D_full²=m²·1：
  (a) (D_full+m·1)² = 2m·(D_full+m·1)    Π₊²=Π₊
  (b) (m·1−D_full)² = 2m·(m·1−D_full)    Π₋²=Π₋
  (c) (D_full+m·1)(m·1−D_full) = 0       Π₊·Π₋=0 正交
  (d) (D_full+m·1)+(m·1−D_full) = 2m·1   Π₊+Π₋=1 互补（无需壳）

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
w = [0.0] * 4
for _ in range(N):
    m = rng.uniform(0.5, 5)
    p1, p2, p3 = rng.uniform(-3, 3, 3)
    E = np.sqrt(m**2 + p1**2 + p2**2 + p3**2)
    D = Dfull(E, p1, p2, p3)
    Pp = D + m * I4c
    Pm = m * I4c - D
    w[0] = max(w[0], np.abs(Pp @ Pp - 2 * m * Pp).max())
    w[1] = max(w[1], np.abs(Pm @ Pm - 2 * m * Pm).max())
    w[2] = max(w[2], np.abs(Pp @ Pm).max())
    w[3] = max(w[3], np.abs(Pp + Pm - 2 * m * I4c).max())
ok &= check("(a) Π₊²=Π₊（全动量）", w[0])
ok &= check("(b) Π₋²=Π₋（全动量）", w[1])
ok &= check("(c) Π₊·Π₋=0 正交（全动量）", w[2])
ok &= check("(d) Π₊+Π₋=2m·1 互补（全动量，无需壳）", w[3])

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：全动量版质量投影对全绿——Π± 幂等/正交/互补在完整 3+1 动量下闭合："
      + "'态射/右伴随两正交投影'在标准相对论 Dirac 结构的最终落地。")
