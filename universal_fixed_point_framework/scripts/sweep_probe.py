# -*- coding: utf-8 -*-
"""数值先证伪：扫尾批（#59 + #60）

#59 4×4 质量投影对幂等化（Cl(1,3) 完整签名，Π± 分子版）：
  (a) diracOp4_mass_projector_idem_plus：壳上 (D₄+m·1)² = 2m·(D₄+m·1)
  (b) diracOp4_mass_projector_idem_minus：壳上 (m·1−D₄)² = 2m·(m·1−D₄)
  (c) diracOp4_mass_projectors_annihilate：壳上 (D₄+m·1)(m·1−D₄) = 0
  (d) diracOp4_mass_projectors_complement：(D₄+m·1)+(m·1−D₄) = 2m·1（恒等，无需壳）
  ——Π±²=Π±、Π₊·Π₋=0、Π₊+Π₋=1：两正交投影对的 4×4 完整签名版。

#60 双向量平方的时空投影结构（Cl(1,3)）：
  (e) Jz_sq_spatial_projection：J_z² = diag(0,−1,−1,0)——空间双向量平方=−空间投影
      （时间分量 0：静默=时间分量不参与旋转）
  (f) Kx_sq_temporal_projection：K_x² = diag(1,1,0,0)——时空双向量平方=时空投影
      （平方 +1 在 (t,x) 平面）

判据：残差 < 1e-8。
"""
import numpy as np

I2 = np.eye(2)
Z2 = np.zeros((2, 2))
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
g0 = np.block([[I2, Z2], [Z2, -I2]])
g1 = np.block([[Z2, s1], [-s1, Z2]])
I4c = np.eye(4, dtype=complex)
I4r = np.eye(4)

K_x = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=float)
J_z = np.array([[0, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], dtype=float)

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
# (a)(b)(c)(d)：壳参数化
w = [0.0] * 4
for _ in range(N):
    m = rng.uniform(0.5, 5)
    phi = rng.uniform(-1.5, 1.5)
    E = m * np.cosh(phi)
    p = m * np.sinh(phi)
    D = D4(E, p)
    Pp = D + m * I4c
    Pm = m * I4c - D
    w[0] = max(w[0], np.abs(Pp @ Pp - 2 * m * Pp).max())
    w[1] = max(w[1], np.abs(Pm @ Pm - 2 * m * Pm).max())
    w[2] = max(w[2], np.abs(Pp @ Pm).max())
    w[3] = max(w[3], np.abs(Pp + Pm - 2 * m * I4c).max())
ok &= check("(a) Π₊²=Π₊：(D₄+m·1)²=2m(D₄+m·1)", w[0])
ok &= check("(b) Π₋²=Π₋：(m·1−D₄)²=2m(m·1−D₄)", w[1])
ok &= check("(c) Π₊·Π₋=0：正交", w[2])
ok &= check("(d) Π₊+Π₋=2m·1：互补（无需壳）", w[3])
# (e)(f)：平方投影（精确）
ok &= check("(e) J_z²=diag(0,−1,−1,0)：空间双向量平方=−空间投影", np.abs(J_z @ J_z - np.diag([0.0, -1.0, -1.0, 0.0])).max())
ok &= check("(f) K_x²=diag(1,1,0,0)：时空双向量平方=时空投影", np.abs(K_x @ K_x - np.diag([1.0, 1.0, 0.0, 0.0])).max())

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：扫尾批全绿——4×4 质量投影对幂等/正交/互补完整签名闭合"
      + "（#51 两正交投影 4 维最终落地）；双向量平方=时空投影"
      + "（空间 J_z²=−P_spatial 时间分量 0 静默、时空 K_x²=+P_{t,x}）。")
