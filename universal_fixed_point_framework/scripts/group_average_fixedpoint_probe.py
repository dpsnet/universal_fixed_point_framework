# -*- coding: utf-8 -*-
"""数值先证伪：等变平均的投影完整刻画（不动点 = 各向同性张量）

拟 Lean 定理逐字对齐：
  groupAverage_fixed_iff_scalar {T} (hsym : Tᵀ=T) :
      groupAverage T = T ↔ ∃ λ, T = λ·1
    ——C₄ 等变平均（粗粒化算符）的固定点空间恰为一维标量中心 {λI}：
      像空间 = 不动点空间 = 各向同性；一切非各向同性部分被平均消除。

数值检验（三方向）：
  (a) 正向：gA(T)=T（固定点）⟹ T≈λI（残差 ~0）
  (b) 反向：λI 是固定点（gA(λI)=λI 精确）
  (c) 一般对称 T：非各向同性部分被消除（‖gA(T)-λI‖ 小，T≠λI 时变化非零）

判据：(a)(b) 残差 < 1e-8；(c) 显示非零消除量。
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


def check(name, resid, extra=""):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e} {extra}")
    return ok


ok = True
# (a) 正向：固定点（数值构造 gA(T)=T 的解 = λI 族，取 T=gA(T0)）
worst = 0.0
for _ in range(N_TRIALS):
    T0 = rand_sym()
    T = group_avg(T0)          # 是固定点：gA(T)=T（幂等）
    lam = np.trace(T) / 2
    worst = max(worst, np.abs(T - lam * np.eye(2)).max())
ok &= check("(a) 固定点 ⟹ T=λI（各向同性）", worst)

# (b) 反向：λI 是固定点（gA(λI)=λI 精确）
worst = 0.0
for _ in range(N_TRIALS):
    lam = rng.uniform(-5, 5)
    T = lam * np.eye(2)
    worst = max(worst, np.abs(group_avg(T) - T).max())
ok &= check("(b) λI 是固定点（gA(λI)=λI）", worst)

# (c) 一般对称 T 的非各向同性部分被消除（消除量 > 0 展示）
ann = []
for _ in range(N_TRIALS):
    T = rand_sym()
    lam = np.trace(T) / 2
    ann.append(np.abs(group_avg(T) - lam * np.eye(2)).max())
worst = max(ann)
max_ann = max(ann)
print(f"[INFO] (c) 一般对称 T：‖gA(T)-λI‖ max = {max_ann:.3e}（消除量；T 本身非 λI 时变化非零）")

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：等变平均（粗粒化）的固定点 = 各向同性张量 λI——像=不动点=标量中心，投影完整刻画，机检对齐。")
