# -*- coding: utf-8 -*-
"""数值先证伪：李群连续层指认 + 各向同性⟹交织反向（开放项收口）

拟 Lean 定理逐字对齐（ℝ 2×2）：
  (a) J² = -1（J=[[0,-1],[1,0]] 反交换生成元）
  (b) rotExp θ := cosθ·1 + sinθ·J = rot θ（线性组合=旋转矩阵——exp 形态指认）
  (c) 指数律 rotExp(θ₁+θ₂) = rotExp θ₁ · rotExp θ₂（SO(2) 连续层；数学上即 cos/sin 加法公式）
  (d) J 与旋转交换：J·rot θ = rot θ·J（中心元素——旋转群作用的核心代数）
  (e) 各向同性⟹交织反向：λI·B = B·λI 对任意 B（λI 与一切交换）

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


def rotExp(th):
    return np.cos(th) * np.eye(2) + np.sin(th) * J


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) J² = -1
d = np.abs(J @ J + np.eye(2)).max()
ok &= check("(a) J·J = -I", d)

# (b) rotExp = rot
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    worst = max(worst, np.abs(rotExp(th) - rot(th)).max())
ok &= check("(b) rotExp=cosθ·I+sinθ·J = rot θ", worst)

# (c) 指数律 rotExp(θ₁+θ₂) = rotExp θ₁·rotExp θ₂
worst = 0.0
for _ in range(N_TRIALS):
    t1, t2 = rng.uniform(-10, 10, size=2)
    worst = max(worst, np.abs(rotExp(t1 + t2) - rotExp(t1) @ rotExp(t2)).max())
ok &= check("(c) 指数律 rotExp(θ₁+θ₂)=rotExp θ₁·rotExp θ₂", worst)

# (d) J 与旋转交换
worst = 0.0
for _ in range(N_TRIALS):
    th = rng.uniform(-10, 10)
    worst = max(worst, np.abs(J @ rot(th) - rot(th) @ J).max())
ok &= check("(d) J·rot θ = rot θ·J", worst)

# (e) 各向同性⟹交织反向：λI·B = B·λI
worst = 0.0
for _ in range(N_TRIALS):
    lam = rng.normal()
    B = rng.normal(size=(2, 2))
    worst = max(worst, np.abs(lam * B - B * lam).max())
ok &= check("(e) λI·B = B·λI（任意 B）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：J²=-1 反交换生成元、(b) rotExp=rot 线性组合（exp 形态）、(c) 指数律（SO(2) 连续层）、"
      + "(d) J 中心交换、(e) 各向同性 λI 与一切交织——李群连续层指认 + 各向同性⟹交织反向")
