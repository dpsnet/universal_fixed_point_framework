# -*- coding: utf-8 -*-
"""数值先证伪（扩展）：换位子李代数的 LieAlgebra 双线性 + Pauli su(2) 换位子表。

对应 Lean 目标（CommutatorLieAlgebra.lean 追加）：
  commutator_add_left/right   : [A+C,B] = [A,B]+[C,B]；[A,B+C] = [A,B]+[A,C]
  commutator_smul_left/right  : [a•A,B] = a•[A,B]；[A,a•B] = a•[A,B]（lie_smul 公理）
  pauli_su2_commutator        : [σx,σy] = 2iσz 循环（Δ=[σz,σx]=2iσy 包含其中）
逐字翻译：commutator(A,B) = A@B - B@A。
"""
import numpy as np

rng = np.random.default_rng(20261025)


def comm(A, B):
    return A @ B - B @ A


worst = 0.0
ok = True
for g in range(6):
    for n in [2, 3, 4]:
        for _ in range(5):
            A = rng.standard_normal((n, n))
            B = rng.standard_normal((n, n))
            C = rng.standard_normal((n, n))
            a = rng.standard_normal()
            # 加法双线性
            r = np.max(np.abs(comm(A + C, B) - comm(A, B) - comm(C, B)))
            worst = max(worst, r)
            r = np.max(np.abs(comm(A, B + C) - comm(A, B) - comm(A, C)))
            worst = max(worst, r)
            # 标量双线性（lie_smul 两个变量）
            r = np.max(np.abs(comm(a * A, B) - a * comm(A, B)))
            worst = max(worst, r)
            r = np.max(np.abs(comm(A, a * B) - a * comm(A, B)))
            worst = max(worst, r)
ok = ok and worst < 1e-8
print(f"[{'PASS' if ok else 'FAIL'}] 换位子加法+标量双线性 最差残差 = {worst:.3e}")

# Pauli 三件套（复 2×2）
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)

triples = [("σx,σy", sx, sy, 2j * sz), ("σy,σz", sy, sz, 2j * sx), ("σz,σx", sz, sx, 2j * sy)]
for name, A, B, target in triples:
    r = np.max(np.abs(comm(A, B) - target))
    ok2 = r < 1e-12
    ok = ok and ok2
    print(f"[{'PASS' if ok2 else 'FAIL'}] [{name}] = 2i·(第三生成元)  残差 = {r:.3e}")
# 反对易三件套
for name, A, B in [("σx,σy", sx, sy), ("σy,σz", sy, sz), ("σz,σx", sz, sx)]:
    r = np.max(np.abs(A @ B + B @ A))
    ok2 = r < 1e-12
    ok = ok and ok2
    print(f"[{'PASS' if ok2 else 'FAIL'}] {{{name}}} = 0（反对易）  残差 = {r:.3e}")
# σxσy = iσz 显式
r = np.max(np.abs(sx @ sy - 1j * sz))
ok = ok and r < 1e-12
print(f"[{'PASS' if r < 1e-12 else 'FAIL'}] σxσy = iσz  残差 = {r:.3e}")
print("ALL PASS" if ok else "SOME FAIL")
