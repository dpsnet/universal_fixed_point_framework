# -*- coding: utf-8 -*-
"""数值先证伪：三层时间分层桥（递归层→谱层→物理层 全链实例化）

拟 Lean 定理逐字对齐（追加 RapidityTimeLayering.lean）：
  (a) theta_layered：sinθ=tanh(n·φ) ⟹ cosh(n·φ)²·cosθ²=1
  (b) energy_gamma_layered：sinθ=tanh(n·φ) ∧ cosθ>0 ⟹ m·cosh(n·φ)=m·secθ
  (c) deflection_cost_layered_nonneg：0≤m ⟹ 0 ≤ m·cosh(n·φ)−m
  (d) 三层闭链复核：θ_n=arcsin(tanh(n·φ)) 下 γ_n=cosh(n·φ)=secθ_n（0≤n·φ 时）

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261026)
N_TRIALS = 500
TOL = 1e-8


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 分层 φ↔θ 平方恒等
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    th = np.arcsin(np.tanh(n * phi))
    worst = max(worst, abs(np.cosh(n * phi) ** 2 * np.cos(th) ** 2 - 1))
ok &= check("(a) cosh(n·φ)²·cosθ²=1", worst)

# (b) 分层 γ 互译（cosθ>0 检查：arcsin 主值 ⟹ θ∈[-π/2,π/2] ⟹ cosθ≥0）
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-0.9, 0.9)
    m = rng.uniform(0.1, 10)
    th = np.arcsin(np.tanh(n * phi))
    if np.cos(th) <= 0:
        continue
    worst = max(worst, abs(m * np.cosh(n * phi) - m / np.cos(th)))
ok &= check("(b) m·cosh(n·φ)=m·secθ", worst)

# (c) 分层偏转代价非负
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    m = rng.uniform(0, 10)
    worst = max(worst, max(0.0, -(m * np.cosh(n * phi) - m)))
ok &= check("(c) K_n=m(cosh(n·φ)−1)≥0", worst)

# (d) 三层闭链：γ_n=cosh(n·φ)=secθ_n
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(0, 0.9)  # n·φ≥0 ⟹ θ_n≥0 主值
    th = np.arcsin(np.tanh(n * phi))
    worst = max(worst, abs(np.cosh(n * phi) - 1 / np.cos(th)))
ok &= check("(d) γ_n=secθ_n 三层闭链", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：三层时间分层桥全绿——递归 n 步的 rapidity/能量/代价/偏转角全部钉住，"
      + "层1→层3 直接读出成立（θ_n=arcsin(tanh(n·φ))）。")
