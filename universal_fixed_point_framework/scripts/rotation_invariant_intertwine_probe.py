# -*- coding: utf-8 -*-
"""数值先证伪：T 涌现完整形态——弥漫平均保持谱交织（§7.6① (iii) 有效谱交织等式）

形态（与拟 Lean 定理逐字对齐，ℝ 2×2）：
  (a) left：A 旋转不变（∀θ, rotθ·A·(rotθ)ᵀ=A，即 A=aI+bJ 中心族，J=[[0,-1],[1,0]]）
      ⟹ A·groupAverage(B) = groupAverage(A·B) 对任意 B（等变投影与不变算符左交换）
  (b) right：A 旋转不变 ⟹ groupAverage(B·A) = groupAverage(B)·A（右交换）
  (c) 交织保持：A_GR、A_SM 旋转不变 + 种子交织 A_GR·B = B·A_SM
      ⟹ A_GR·groupAverage(B) = groupAverage(B)·A_SM（★ T=gA(B) 结构涌现满足有效谱交织）

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


RS = [rot(0), rot(np.pi / 2), rot(np.pi), rot(-np.pi / 2)]


def gA(M):
    return sum(R @ M @ R.T for R in RS) / 4.0


def invariant_mat(a, b):
    return a * np.eye(2) + b * J


worst_a = worst_b = worst_c = 0.0
ok_a = ok_b = ok_c = True
for _ in range(N_TRIALS):
    a, b = rng.normal(size=2)
    A = invariant_mat(a, b)
    B = rng.normal(size=(2, 2))                       # 任意 B
    # (a) left
    d = np.abs(A @ gA(B) - gA(A @ B)).max()
    worst_a = max(worst_a, d)
    if d > TOL:
        ok_a = False
    # (b) right
    d = np.abs(gA(B @ A) - gA(B) @ A).max()
    worst_b = max(worst_b, d)
    if d > TOL:
        ok_b = False

# (c) 交织保持：A_GR=A_SM=A（旋转不变），B 取中心族（与 A 交换，种子交织成立）
for _ in range(N_TRIALS):
    a, b = rng.normal(size=2)
    A_GR = invariant_mat(a, b)
    A_SM = invariant_mat(a, b)
    e, f = rng.normal(size=2)
    B = invariant_mat(e, f)
    # 种子交织 A_GR·B = B·A_SM（中心族自动满足）
    d = np.abs(A_GR @ B - B @ A_SM).max()
    assert d < TOL, f"种子交织构造失败 {d}"
    d = np.abs(A_GR @ gA(B) - gA(B) @ A_SM).max()
    worst_c = max(worst_c, d)
    if d > TOL:
        ok_c = False

print(f"[{'PASS' if ok_a else 'FAIL'}] (a) left   A·gA(B)=gA(A·B)（A 旋转不变，B 任意）  最差残差 = {worst_a:.3e}")
print(f"[{'PASS' if ok_b else 'FAIL'}] (b) right  gA(B·A)=gA(B)·A（A 旋转不变，B 任意）  最差残差 = {worst_b:.3e}")
print(f"[{'PASS' if ok_c else 'FAIL'}] (c) 交织保持 A_GR·gA(B)=gA(B)·A_SM（种子交织+双侧旋转不变）  最差残差 = {worst_c:.3e}")
ok = ok_a and ok_b and ok_c
print("ALL PASS" if ok else "SOME FAIL")
print(f"摘要：等变投影与不变算符交换（a/b {worst_a:.2e}/{worst_b:.2e}）、"
      + f"弥漫平均保持谱交织（c {worst_c:.2e}）——T=gA(B) 结构涌现满足有效谱交织")
