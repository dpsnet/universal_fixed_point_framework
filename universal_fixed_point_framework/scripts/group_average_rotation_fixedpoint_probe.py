# -*- coding: utf-8 -*-
"""数值先证伪：等变平均在旋转群元上=恒等（Karcher 表述第一步）+ rot det=1

拟 Lean 定理逐字对齐：
  (a) groupAverage_preserves_rotation：groupAverage(rot φ) = rot φ
      ——SO(2) 阿贝尔（共轭 R(θ)·R(φ)·R(θ)ᵀ = R(φ)）⟹ C₄ 平均对旋转群元自平均不动；
      Karcher/几何平均在阿贝尔群元上平凡=恒等，等变平均对旋转结构自动保正交。
  (b) rot_det_eq_one：det(rot θ) = 1（#31 描述 (d) 复核句）。

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-8

R0 = np.eye(2)
R1 = np.array([[0.0, -1.0], [1.0, 0.0]])
R2 = -np.eye(2)
R3 = np.array([[0.0, 1.0], [-1.0, 0.0]])
RS = [R0, R1, R2, R3]


def rot(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])


def group_avg(T):
    out = np.zeros((2, 2))
    for R in RS:
        out += R @ T @ R.T
    return out / 4


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 群元恒等：随机 φ → groupAverage(rot φ) = rot φ
worst = 0.0
for _ in range(N_TRIALS):
    ph = rng.uniform(-10, 10)
    T = rot(ph)
    worst = max(worst, np.abs(group_avg(T) - T).max())
    # 保正交复核：平均结果正交
    worst = max(worst, np.abs(group_avg(T).T @ group_avg(T) - np.eye(2)).max())
ok &= check("(a) 群元恒等：groupAverage(rot φ)=rot φ + 自动保正交", worst)

# (b) rot det=1
worst = 0.0
for _ in range(N_TRIALS):
    A = rot(rng.uniform(-10, 10))
    worst = max(worst, abs(np.linalg.det(A) - 1))
ok &= check("(b) rot θ det=1", worst)

# (c) 反射元湮灭：T = rot(θ)·F（F=diag(1,-1)，det=-1）→ groupAverage(T)=0
#     F 与 C₄ 旋转反交换型共轭 ⟹ 四份 R·T·Rᵀ 自抵消（手性在粗粒化下湮灭）
Fm = np.array([[1.0, 0.0], [0.0, -1.0]])
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    T = rot(th) @ Fm
    worst = max(worst, np.abs(group_avg(T)).max())
    # 逐项自抵消复核：Σ R·T·Rᵀ 的范数（先于 1/4）
ok &= check("(c) 反射元湮灭：groupAverage(rot θ·F)=0（手性粗粒化湮灭）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：SO(2) 阿贝尔 ⟹ 等变平均在群元上恒等（Karcher 表述第一步机检对齐），"
      + "群元上自动保正交；det(rot θ)=1 复核。")
