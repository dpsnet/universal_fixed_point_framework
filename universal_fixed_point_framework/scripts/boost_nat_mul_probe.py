# -*- coding: utf-8 -*-
"""数值先证伪：1+1 离散⟹连续桥（n 步 = rapidity 线性累积 n·φ）

拟 Lean 定理逐字对齐（追加 MinkowskiBoost.lean）：
  (a) boostExp_nat_mul：boostExp(n·φ) = (boostExp φ)^n
      ——递归层时钟 n 步 = 谱参数 n·φ 一步到位（#34 rotExp_nat_mul 的双曲镜像：
      "每次递归=时间递进一层"在 1+1 时间偏转层的代数实现）。
  (b) boost_nat_mul：boost(n·φ) = (boost φ)^n（旋转形态时钟步进⟷谱参数线性累积）。
  (c) 合成：boostExp(n·φ)=boost(n·φ)=（boost φ）^n（三形态一致）。

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-8


def boost(phi):
    return np.array([[np.cosh(phi), np.sinh(phi)], [np.sinh(phi), np.cosh(phi)]])


Jp = np.array([[0.0, 1.0], [1.0, 0.0]])
I2 = np.eye(2)


def boost_exp(phi):
    return np.cosh(phi) * I2 + np.sinh(phi) * Jp


def mat_pow(M, n):
    out = np.eye(2)
    for _ in range(n):
        out = out @ M
    return out


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 指数整数幂（n≤6、|φ|≤1 控制 mat_pow 浮点累积；解析恒等式精确）
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    worst = max(worst, np.abs(boost_exp(n * phi) - mat_pow(boost_exp(phi), int(n))).max())
ok &= check("(a) boostExp(n·φ)=(boostExp φ)^n", worst)

# (b) 旋转形态
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    worst = max(worst, np.abs(boost(n * phi) - mat_pow(boost(phi), int(n))).max())
ok &= check("(b) boost(n·φ)=(boost φ)^n", worst)

# (c) 三形态一致
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 12)
    phi = rng.uniform(-2, 2)
    worst = max(worst, np.abs(boost_exp(n * phi) - boost(n * phi)).max())
ok &= check("(c) boostExp(n·φ)=boost(n·φ)", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：1+1 离散⟹连续桥全绿——递归层 n 步 = rapidity 线性累积 n·φ，"
      + "指数形态/旋转形态/合成三一致，与欧氏 rotExp_nat_mul（#34）构成双曲镜像。")
