# -*- coding: utf-8 -*-
"""数值先证伪：Clifford 双向量 = 旋转生成元（e01_eq_J + rotExp_eq_cos_sin_e01）

拟 Lean 定理逐字对齐：
  (a) e01_eq_J：Cℓ(0,1) 单位双向量 e_01 = !![0,-1;1,0] 恰为旋转生成元 J
      （rotExp θ = cosθ·1 + sinθ·J 中的 J；e_01²=-1 与 J²=-1 同一）。
  (b) rotExp_eq_cos_sin_e01：rotExp θ = cosθ·1 + sinθ·e_01
      ——"双向量指数生成旋转单参子群"（Cℓ(0,1) ≅ ℂ，exp 矩阵表示）。
  (c) 复核：e_01² = -1、J² = -1、rotExp(θ₁+θ₂) 指数律。

判据：残差 < 1e-12（恒等式，数值应 ~1e-16）。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-12

E01 = np.array([[0.0, -1.0], [1.0, 0.0]])   # Clifford e_01 / 旋转生成元 J
J = np.array([[0.0, -1.0], [1.0, 0.0]])


def rot_exp(th):
    return np.cos(th) * np.eye(2) + np.sin(th) * E01


def rot(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) e_01 = J（逐条目）
worst = np.abs(E01 - J).max()
ok &= check("(a) e_01 = J（矩阵同一）", worst)

# (b) rotExp θ = cosθ·1 + sinθ·e_01（与 rot 一致）
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    worst = max(worst, np.abs(rot_exp(th) - rot(th)).max())
ok &= check("(b) rotExp θ = cosθ·1 + sinθ·e_01（=rot θ）", worst)

# (c) 复核：双向量平方 -1 + 指数律（层间桥基底）
worst = max(np.abs(E01 @ E01 + np.eye(2)).max(), np.abs(J @ J + np.eye(2)).max())
ok &= check("(c) e_01² = J² = -1", worst)
worst = 0.0
for _ in range(N_TRIALS):
    th1, th2 = rng.uniform(-10, 10, 2)
    worst = max(worst, np.abs(rot_exp(th1 + th2) - rot_exp(th1) @ rot_exp(th2)).max())
ok &= check("(c') rotExp 指数律 rotExp(θ₁+θ₂)=rotExp θ₁·rotExp θ₂", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：Cℓ(0,1) 单位双向量 = 旋转生成元（同一矩阵）；指数律 ⟹ 双向量生成 SO(2) 单参子群，机检对齐。")
