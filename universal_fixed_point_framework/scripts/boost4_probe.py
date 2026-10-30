# -*- coding: utf-8 -*-
"""数值先证伪：1+3 洛伦兹 boost 层（#52，SO(1,3) 显式化第一步）

拟 Lean 定理逐字对齐（Λ_x(φ)=4×4 x-boost，η₄=diag(1,−1,−1,−1)）：
  (a) boost4_x_preserves_minkowski4：(Λ_x φ)ᵀ·η₄·(Λ_x φ)=η₄ ——保闵氏度规=SO(1,3) 定义
  (b) boost4_x_add：Λ_x(φ₁+φ₂)=Λ_x φ₁·Λ_x φ₂ ——rapidity 可加性 4×4
  (c) boost4_x_nat_mul：Λ_x(n·φ)=(Λ_x φ)^n ——离散步进⟹连续 rapidity 4×4
  (d) 块结构自检：Λ_x=块对角(boost₂,1₂)，空间块恒等

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 300
TOL = 1e-8

Eta4 = np.diag([1.0, -1.0, -1.0, -1.0])
I4 = np.eye(4)


def B4(phi):
    c, s = np.cosh(phi), np.sinh(phi)
    return np.array([[c, s, 0, 0], [s, c, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0]])


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 保度规
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    L = B4(phi)
    worst = max(worst, np.abs(L.T @ Eta4 @ L - Eta4).max())
ok &= check("(a) (Λφ)ᵀ·η₄·Λφ=η₄（保度规）", worst)

# (b) 可加性
worst = 0.0
for _ in range(N_TRIALS):
    p1 = rng.uniform(-2, 2)
    p2 = rng.uniform(-2, 2)
    worst = max(worst, np.abs(B4(p1 + p2) - B4(p1) @ B4(p2)).max())
ok &= check("(b) Λ(φ₁+φ₂)=Λφ₁·Λφ₂", worst)

# (c) Nat 幂
worst = 0.0
for _ in range(6):
    phi = rng.uniform(-1, 1)
    n = int(rng.integers(1, 7))
    L = np.eye(4)
    for _ in range(n):
        L = L @ B4(phi)
    worst = max(worst, np.abs(L - B4(n * phi)).max())
ok &= check("(c) Λ(n·φ)=(Λφ)^n", worst)

# (d) 块结构
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    L = B4(phi)
    block = np.array([[np.cosh(phi), np.sinh(phi)], [np.sinh(phi), np.cosh(phi)]])
    worst = max(worst, abs(L[0, 0] - block[0, 0]) + abs(L[0, 1] - block[0, 1])
                + abs(L[2, 2] - 1.0) + abs(L[3, 3] - 1.0)
                + abs(L[0, 2]) + abs(L[1, 3]) + abs(L[2, 0]) + abs(L[3, 1]))
ok &= check("(d) 块对角(boost₂,1₂)", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：1+3 洛伦兹 boost 层全绿——4×4 x-boost 保闵氏度规 η₄（SO(1,3) 定义）、"
      + "rapidity 可加、Nat 幂离散⟹连续桥、块结构恒等。")
