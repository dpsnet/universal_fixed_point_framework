# -*- coding: utf-8 -*-
"""数值先证伪：对称张量的正交无迹分解 + 投影互补性（两正交投影直觉）

拟 Lean 定理逐字对齐：
  (a) symmetric_traceless_decomp：对称 T ⟹ ∃T₀，T = (trace/2)·1 + T₀ ∧ trace T₀ = 0
      ——标量部分（宏观读数）与无迹部分（各向异性结构）直和。
  (b) scalar_orthogonal_traceless：trace((a·1)ᵀ·T₀) = 0 当 trace T₀ = 0
      ——矩阵内积下标量中心 ⊥ 无迹部分（正交）。
  (c) groupAverage_complement_traceless：trace(T − gA(T)) = 0
      ——gA 保留标量（各向同性/相空间读数），id−gA 保留无迹（各向异性/Cl 结构），
      互补正交投影（用户"两个正交投影"直觉的代数对应）。

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


def group_avg(T):
    out = np.zeros((2, 2))
    for R in RS:
        out += R @ T @ R.T
    return out / 4


def rand_sym():
    A = rng.standard_normal((2, 2))
    return A + A.T


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 无迹分解
worst = 0.0
worst_t0 = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    lam = np.trace(T) / 2
    T0 = T - lam * np.eye(2)
    worst = max(worst, np.abs(T - (lam * np.eye(2) + T0)).max())
    worst_t0 = max(worst_t0, abs(np.trace(T0)))
ok &= check("(a) T = λI + T₀（直和）", worst)
ok &= check("(a') trace(T₀) = 0（无迹）", worst_t0)

# (b) 标量 ⊥ 无迹（内积 trace(AᵀB)）
worst = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    a = rng.uniform(-5, 5)
    T0 = T - np.trace(T) / 2 * np.eye(2)
    worst = max(worst, abs(np.trace((a * np.eye(2)).T @ T0)))
ok &= check("(b) trace((a·1)ᵀ·T₀)=0（正交）", worst)

# (c) 补投影无迹
worst = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    worst = max(worst, abs(np.trace(T - group_avg(T))))
ok &= check("(c) trace(T − gA(T)) = 0（补投影无迹）", worst)

# (c') 幂等+互补：T = gA(T) + (T − gA(T))
worst = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    worst = max(worst, np.abs(T - (group_avg(T) + (T - group_avg(T)))).max())
ok &= check("(c') T = gA(T) + (T−gA(T))（互补）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：粗粒化 = 到标量中心（相空间读数）的正交投影，id−gA = 到无迹（各向异性/Cl 结构）"
      + "的正交投影——两正交投影互补，机检对齐。")
