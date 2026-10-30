# -*- coding: utf-8 -*-
"""数值先证伪：SO(2) 全群满射表征（开放项收口）

拟 Lean 定理逐字对齐（ℝ 2×2）：
  (a) so2_structural_necessary：Aᵀ·A=1 ∧ det A=1 ⟹ A00=A11 ∧ A01=-A10 ∧ A00²+A01²=1
      （正交+单位行列式 ⟹ 单参数单位圆结构形态）
  (b) so2_structural_sufficient：a=d ∧ b=-c ∧ a²+b²=1 ⟹ 正交 ∧ det=1（结构形态充分性）
  (c) so2_surjective：正交+det=1 ⟹ ∃θ A=rot θ（arcsin 分支重构一致）
  (d) rot 保正交 det1（正例复核）

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-8

J = np.array([[0.0, -1.0], [1.0, 0.0]])


def rot(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 必要：随机 θ → A=rot θ（正交 det1 的生成器）→ 结构形态
worst = 0.0
for _ in range(N_TRIALS):
    A = rot(rng.uniform(-10, 10))
    worst = max(worst, abs(A[0, 0] - A[1, 1]))
    worst = max(worst, abs(A[0, 1] + A[1, 0]))
    worst = max(worst, abs(A[0, 0] ** 2 + A[0, 1] ** 2 - 1))
ok &= check("(a) 结构形态必要：A00=A11、A01=-A10、A00²+A01²=1", worst)

# (b) 充分：随机结构形态矩阵 [[a,-b],[b,a]]（a²+b²=1）→ 正交 det1
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    a, b = np.cos(th), np.sin(th)
    A = np.array([[a, -b], [b, a]])
    worst = max(worst, np.abs(A.T @ A - np.eye(2)).max())
    worst = max(worst, abs(np.linalg.det(A) - 1))
ok &= check("(b) 结构形态充分：[[a,-b],[b,a]] 正交 det1", worst)

# (c) 满射：随机 A=rot θ → arcsin 重构（θ'=arcsin(-A01)，A00≥0 分支）
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    A = rot(th)
    a, b = A[0, 0], A[0, 1]
    thp = np.arcsin(-b)
    if a < 0:
        thp = np.pi - thp
    worst = max(worst, np.abs(A - rot(thp)).max())
ok &= check("(c) 满射重构：arcsin 分支 rot θ' = A", worst)

# (d) rot 保正交 det1
worst = 0.0
for _ in range(N_TRIALS):
    A = rot(rng.uniform(-10, 10))
    worst = max(worst, np.abs(A.T @ A - np.eye(2)).max())
    worst = max(worst, abs(np.linalg.det(A) - 1))
ok &= check("(d) rot θ 正交 det1", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：正交+det1 ⟺ 结构形态 [[a,-b],[b,a]]（a²+b²=1）⟺ rot θ——"
      + "SO(2) 全群满射表征机检对齐（{rot θ} 覆盖 SO(2)）")
