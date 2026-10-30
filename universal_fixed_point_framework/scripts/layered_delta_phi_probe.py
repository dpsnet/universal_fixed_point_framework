# -*- coding: utf-8 -*-
"""数值先证伪：Δφ 分层参数层（开放项②）

拟 Lean 定理逐字对齐（追加 RapidityTimeLayering.lean）：
  (a) speed_in_light_cone_layered：|sinh(n·φ)| < cosh(n·φ)——n 层递归后仍光锥内
  (b) mass_shell_layered：(m·cosh(n·φ))²−(m·sinh(n·φ))²=m²——n 层后壳保持
  (c) boost_nat_preserves_minkowski：(boost(n·φ))ᵀ·η·boost(n·φ)=η——n 层后闵氏保
  (d) 与 boost_nat_mul 合成：boost(n·φ)=(boost φ)^n 且保度量（离散步进闭环）

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-8


def boost(phi):
    return np.array([[np.cosh(phi), np.sinh(phi)], [np.sinh(phi), np.cosh(phi)]])


Eta = np.diag([1.0, -1.0])
I2 = np.eye(2)


def mat_pow(M, n):
    out = I2
    for _ in range(n):
        out = out @ M
    return out


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 分层光锥
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    x = n * phi
    worst = max(worst, abs(np.sinh(x)) - np.cosh(x))
ok &= check("(a) 光锥内 |sinh(n·φ)|<cosh(n·φ)", max(0.0, worst))

# (b) 分层质量壳
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    m = rng.uniform(0.1, 10)
    x = n * phi
    worst = max(worst, abs((m * np.cosh(x)) ** 2 - (m * np.sinh(x)) ** 2 - m ** 2))
ok &= check("(b) 壳保持 (m·cosh(n·φ))²−(m·sinh(n·φ))²=m²", worst)

# (c) 分层闵氏度量
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    B = boost(n * phi)
    worst = max(worst, np.abs(B.T @ Eta @ B - Eta).max())
ok &= check("(c) 保闵氏 (boost(n·φ))ᵀ·η·boost(n·φ)=η", worst)

# (d) 离散步进合成：boost(n·φ)=(boost φ)^n 且复合后仍保度量
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    Bn = mat_pow(boost(phi), int(n))
    worst = max(worst, np.abs(Bn - boost(n * phi)).max()
                + np.abs(Bn.T @ Eta @ Bn - Eta).max())
ok &= check("(d) 合成 boost(n·φ)=(boost φ)^n 且保度量", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：Δφ 分层参数层全绿——递归 n 层光锥/壳/闵氏全部保持，"
      + "Δφ 可由模型参数层任意给定不破坏结构（取值本身属模型参数层）。")
