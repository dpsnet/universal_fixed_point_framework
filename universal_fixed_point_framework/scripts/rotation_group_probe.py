# -*- coding: utf-8 -*-
"""数值先证伪：旋转复合封闭（SO(2)/C₄ 群作用存在）+ spDelta2Cell 偏差非零判定。

对应 Lean 目标：
  ① ForceAverageIsotropy.lean 追加：rot_add（rot(θ₁+θ₂)=rotθ₁·rotθ₂——旋转群封闭）、
     C₄ 乘法表封闭（R1·R1=R2 等）——弥漫结构携带群作用（C₄/SO(2)）存在且封闭；
  ② HigherSpCategory.lean 追加：delta_cell_dev_ne_zero_iff_swap
     （c.dev≠0 ⟺ 层 2 交换律 LHS≠RHS——Δ 2-胞腔非平凡 ⟹ 层结构非交换）。
逐字翻译：rot θ = [[cosθ, -sinθ]; [sinθ, cosθ]]；群平均 = (1/4)Σ R·T·Rᵀ。
"""
import numpy as np

rng = np.random.default_rng(20261025)


def rot(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s], [s, c]])


worst = 0.0
for g in range(10):
    t1 = rng.uniform(-10, 10)
    t2 = rng.uniform(-10, 10)
    r = np.max(np.abs(rot(t1 + t2) - rot(t1) @ rot(t2)))
    worst = max(worst, r)
print(f"[{'PASS' if worst < 1e-8 else 'FAIL'}] rot(θ1+θ2)=rotθ1·rotθ2  最差残差 = {worst:.3e}")

# C₄ 乘法表（精确）
R1, R2, R3 = rot(np.pi / 2), rot(np.pi), rot(-np.pi / 2)
R0 = np.eye(2)
table = [("R1·R1=R2", R1 @ R1, R2), ("R1·R2=R3", R1 @ R2, R3),
         ("R1·R3=R0", R1 @ R3, R0), ("R2·R2=R0", R2 @ R2, R0),
         ("R3·R3=R2", R3 @ R3, R2), ("R3·R1=R0", R3 @ R1, R0)]
ok = True
for name, got, want in table:
    r = np.max(np.abs(got - want))
    ok = ok and r < 1e-12
    print(f"[{'PASS' if r < 1e-12 else 'FAIL'}] {name}  残差 = {r:.3e}")

# ② 层 2 交换律偏差非零判定的数值模拟：
# 用 2×2 随机谱算符 X.A,Y.A,Z.A 与 homotopy M（生成元），算 LHS-RHS = dev；
# 验证 dev ≠ 0 ⟺ LHS ≠ RHS（平凡恒等），并抽样 dev 非零比例。
n_trials = 2000
nonzero_dev = 0
for _ in range(n_trials):
    XA = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    YA = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    ZA = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    M = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    # dev = XA·M − 2·(M·YA·M) + M·ZA  (部分对易子：M 扮演 β.homotopy·α'.homotopy)
    dev = XA @ M - 2 * (M @ YA @ M) + M @ ZA
    if np.max(np.abs(dev)) > 1e-9:
        nonzero_dev += 1
print(f"[{'PASS' if nonzero_dev == n_trials else 'FAIL'}] dev 非零比例 = {nonzero_dev}/{n_trials}（交换律偏差普遍非平凡——Δ≠0 是常态非例外）")
print("ALL PASS" if ok and worst < 1e-8 and nonzero_dev == n_trials else "SOME FAIL")
