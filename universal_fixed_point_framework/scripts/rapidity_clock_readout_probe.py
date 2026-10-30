# -*- coding: utf-8 -*-
"""数值先证伪：层间桥代数核心——指数律整数幂版本

拟 Lean 定理逐字对齐：
  (a) rotExp_nat_mul：rotExp((n:ℝ)·θ) = (rotExp θ)^n
      ——指数律的整数幂归纳：离散递归层 n 步复合 = 谱参数 n·θ 一步到位；
      "递归层时钟读出谱流"= rapidity 线性累积（每步 Δφ，n 步 = n·Δφ）。
  (b) rot_nat_mul（推论形态）：rot((n:ℝ)·θ) = (rot θ)^n（rotExp_eq_rot 桥）
  (c) 幂复合保正交复核：‖(rot θ)^n‖_orth 复核（自动）

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 200
TOL = 1e-8
J = np.array([[0.0, -1.0], [1.0, 0.0]])


def rot(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])


def rot_exp(th):
    return np.cos(th) * np.eye(2) + np.sin(th) * J


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 指数律整数幂：rotExp(n·θ) = (rotExp θ)^n
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    for n in range(1, 11):
        A = rot_exp(n * th)
        B = np.linalg.matrix_power(rot_exp(th), n)
        worst = max(worst, np.abs(A - B).max())
ok &= check("(a) rotExp(n·θ) = (rotExp θ)^n（n∈[1,10] 全扫）", worst)

# (b) rot 幂复合：rot(n·θ) = (rot θ)^n
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    for n in range(1, 11):
        A = rot(n * th)
        B = np.linalg.matrix_power(rot(th), n)
        worst = max(worst, np.abs(A - B).max())
ok &= check("(b) rot(n·θ) = (rot θ)^n（n∈[1,10] 全扫）", worst)

# (c) 幂保持正交 det1（自动复核：旋转幂仍是 SO(2)）
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    P = np.linalg.matrix_power(rot(th), 7)
    worst = max(worst, np.abs(P.T @ P - np.eye(2)).max())
    worst = max(worst, abs(np.linalg.det(P) - 1))
ok &= check("(c) (rot θ)^n 保正交 det1", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：指数律整数幂 = 层间桥代数核心机检对齐——递归层时钟 n 步读出 = 谱参数 n·θ "
      + "（rapidity 线性累积），rot(n·θ)=(rot θ)^n 与时间分层可加性一致。")
