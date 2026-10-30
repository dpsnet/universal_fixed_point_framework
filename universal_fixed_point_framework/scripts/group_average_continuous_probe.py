# -*- coding: utf-8 -*-
"""数值先证伪：离散平均涌现连续旋转对称

拟 Lean 定理逐字对齐：
  groupAverage_continuous_rotation_invariant：
    对对称 T，∀θ：rot(θ)·gA(T)·(rot θ)ᵀ = gA(T)
    ——C₄ 等变平均输出 λI（各向同性），λI 与任意旋转交换（标量中心）；
    "统计涌现"的连续侧：离散群平均 ⟹ 连续 O(2) 不变（粗粒化涌现连续对称）。

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


def rand_sym():
    A = rng.standard_normal((2, 2))
    return A + A.T


ok = True
worst = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    G = group_avg(T)
    th = rng.uniform(-10, 10)
    R = rot(th)
    lhs = R @ G @ R.T
    res = np.abs(lhs - G).max()
    worst = max(worst, res)
ok &= worst < TOL
print(f"[{'PASS' if ok else 'FAIL'}] 连续旋转不变：rotθ·gA(T)·rotθᵀ = gA(T)  残差 = {worst:.3e}")

# 复核：λI 显式（trace/2）下一致（对照 groupAverage_isotropy）
worst2 = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    G = group_avg(T)
    lam = np.trace(T) / 2
    worst2 = max(worst2, np.abs(G - lam * np.eye(2)).max())
ok &= worst2 < TOL
print(f"[{'PASS' if ok else 'FAIL'}] λI 显式对照：gA(T)=(trace/2)·I  残差 = {worst2:.3e}")

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：离散 C₄ 平均输出对连续 O(2) 旋转不变——统计涌现连续对称，机检对齐。")
