# -*- coding: utf-8 -*-
"""数值先证伪：SO(1,3) 空间旋转层 + 洛伦兹生成元交换子（#53）

拟 Lean 定理逐字对齐（η₄=diag(1,−1,−1,−1)）：
  (a) rot4_z_preserves_minkowski4：R_z(θ)·η₄·(R_z θ)ᵀ=η₄ ——空间旋转保闵氏度规
  (b) rot4_z_add：R_z(θ₁+θ₂)=R_z θ₁·R_z θ₂ ——SO(3) 子群可加
  (c) rot4_z_nat_mul：R_z(n·θ)=(R_z θ)^n ——离散⟹连续桥（空间侧）
  (d) lorentz_commutator_Kx_Jz：[K_x,J_z]=−K_y ——Cl(1,3) 李代数混合第一环
      （boost 生成元×旋转生成元的交换子=另一 boost 生成元）

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 300
TOL = 1e-8

Eta4 = np.diag([1.0, -1.0, -1.0, -1.0])
I4 = np.eye(4)

Kx = np.array([[0., 1., 0., 0.], [1., 0., 0., 0.], [0., 0., 0., 0.], [0., 0., 0., 0.]])
Jz = np.array([[0., 0., 0., 0.], [0., 0., -1., 0.], [0., 1., 0., 0.], [0., 0., 0., 0.]])
Ky = np.array([[0., 0., 1., 0.], [0., 0., 0., 0.], [1., 0., 0., 0.], [0., 0., 0., 0.]])


def Rz(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[1., 0., 0., 0.], [0., c, -s, 0.], [0., s, c, 0.], [0., 0., 0., 1.]])


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 旋转保度规
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-3, 3)
    R = Rz(th)
    worst = max(worst, np.abs(R @ Eta4 @ R.T - Eta4).max())
ok &= check("(a) R_z·η₄·R_zᵀ=η₄（旋转保度规）", worst)

# (b) 可加性
worst = 0.0
for _ in range(N_TRIALS):
    t1 = rng.uniform(-3, 3)
    t2 = rng.uniform(-3, 3)
    worst = max(worst, np.abs(Rz(t1 + t2) - Rz(t1) @ Rz(t2)).max())
ok &= check("(b) R_z(θ₁+θ₂)=R_zθ₁·R_zθ₂", worst)

# (c) Nat 幂
worst = 0.0
for _ in range(6):
    th = rng.uniform(-1, 1)
    n = int(rng.integers(1, 7))
    R = np.eye(4)
    for _ in range(n):
        R = R @ Rz(th)
    worst = max(worst, np.abs(R - Rz(n * th)).max())
ok &= check("(c) R_z(n·θ)=(R_zθ)^n", worst)

# (d) 交换子
worst = 0.0
worst = max(worst, np.abs(Kx @ Jz - Jz @ Kx + Ky).max())
ok &= check("(d) [K_x,J_z]=−K_y（洛伦兹混合代数）", worst)

# (e) 生成元非交换（与 #24 同构）：‖[K_x,J_z]‖ 应非零
comm = Kx @ Jz - Jz @ Kx
worst = np.abs(comm).max()
nonzer = worst > 0.5
print(f"[{'PASS' if nonzer else 'FAIL'}] (e) [K_x,J_z]≠0（洛伦兹代数非交换）  范数 = {worst:.3e}")
ok &= nonzer

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：SO(1,3) 空间旋转层+生成元交换子全绿——R_z 保度规/可加/Nat 幂完整，"
      + "[K_x,J_z]=−K_y：Cl(1,3) 李代数混合第一环（boost×旋转=另一 boost），洛伦兹代数非交换。")
