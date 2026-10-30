# -*- coding: utf-8 -*-
"""数值先证伪：矩阵换位子的李代数骨架（Jacobi 恒等式 + 反对称）。

对应 Lean 目标：CommutatorLieAlgebra.lean
  jacobi_identity : [A,[B,C]] + [B,[C,A]] + [C,[A,B]] = 0
  anticommutative : [B,A] = -[A,B]
逐字翻译：commutator(A,B) = A@B - B@A。
"""
import numpy as np


def comm(A, B):
    return A @ B - B @ A


def jacobi_residue(A, B, C):
    return comm(A, comm(B, C)) + comm(B, comm(C, A)) + comm(C, comm(A, B))


def check_group(name, dims, n_groups=6, tol=1e-8):
    worst = 0.0
    for g in range(n_groups):
        for n in dims:
            for _ in range(5):
                A = np.random.randn(n, n)
                B = np.random.randn(n, n)
                C = np.random.randn(n, n)
                r = np.max(np.abs(jacobi_residue(A, B, C)))
                worst = max(worst, r)
                if r > tol:
                    return False, r, (A, B, C)
                # 反对称
                r2 = np.max(np.abs(comm(B, A) + comm(A, B)))
                worst = max(worst, r2)
                if r2 > tol:
                    return False, r2, (A, B)
    return True, worst, None


rng = np.random.default_rng(20261025)

ok, worst, bad = check_group("实矩阵 Jacobi", [2, 3, 4], 6, 1e-8)
print(f"[{'PASS' if ok else 'FAIL'}] 实矩阵 Jacobi + 反对称 最差残差 = {worst:.3e}")

# 复矩阵
def comm_c(A, B):
    return A @ B - B @ A

worst_c = 0.0
for g in range(6):
    for n in [2, 3]:
        for _ in range(5):
            A = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
            B = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
            C = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
            r = np.max(np.abs(comm_c(A, comm_c(B, C)) + comm_c(B, comm_c(C, A)) + comm_c(C, comm_c(A, B))))
            worst_c = max(worst_c, r)
print(f"[{'PASS' if worst_c < 1e-8 else 'FAIL'}] 复矩阵 Jacobi 最差残差 = {worst_c:.3e}")

# Pauli 层专项：sigma_z/sigma_x 换位子 = 2i sigma_y（su(2) 生成元结构）
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
comm_zx = comm_c(sz, sx)
target = 2j * sy
print(f"[{'PASS' if np.max(np.abs(comm_zx - target)) < 1e-12 else 'FAIL'}] [σz,σx] = 2iσy  残差 = {np.max(np.abs(comm_zx - target)):.3e}")
# 反对易 {σz,σx} = 0
anti = sz @ sx + sx @ sz
print(f"[{'PASS' if np.max(np.abs(anti)) < 1e-12 else 'FAIL'}] {{σz,σx}} = 0  残差 = {np.max(np.abs(anti)):.3e}")
# 非交换（Δ≠0 的前提）
print(f"[{'PASS' if np.max(np.abs(comm_zx)) > 1e-8 else 'FAIL'}] [σz,σx] ≠ 0（Δ 非平凡）")
