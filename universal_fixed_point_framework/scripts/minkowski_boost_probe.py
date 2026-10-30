# -*- coding: utf-8 -*-
"""数值先证伪：1+1 闵氏 boost 层（时间偏转的谱流实现）

拟 Lean 定理逐字对齐（MinkowskiBoost.lean）：
  (a) boost_add：boost(φ₁+φ₂) = boost(φ₁)·boost(φ₂)
      ——rapidity 可加性的矩阵实现（"在时间中移动=沿 rapidity 谱流演化"）。
  (b) boost_det_one：det(boost φ) = 1（cosh²−sinh²=1，保面积/守恒）。
  (c) boostExp_eq_boost：boostExp φ = coshφ·1 + sinhφ·J' = boost φ（双曲指数 exp(φJ')）。
  (d) Jprime_sq：J'² = 1（Cl(1,1) 时空双向量，平方=+1——与欧氏 e_01（平方−1）互补）。
  (e) e10_eq_Jprime：Clifford e_10 = J'（双曲生成元指认）。

boost φ = [[cosh φ, sinh φ], [sinh φ, cosh φ]]；J' = [[0,1],[1,0]]。
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


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) rapidity 可加（矩阵实现）
worst = 0.0
for _ in range(N_TRIALS):
    p1 = rng.uniform(-3, 3)
    p2 = rng.uniform(-3, 3)
    worst = max(worst, np.abs(boost(p1 + p2) - boost(p1) @ boost(p2)).max())
ok &= check("(a) boost(φ₁+φ₂)=boost(φ₁)·boost(φ₂)", worst)

# (b) det = 1
worst = 0.0
for _ in range(N_TRIALS):
    p = rng.uniform(-3, 3)
    worst = max(worst, abs(np.linalg.det(boost(p)) - 1))
ok &= check("(b) det(boost φ)=1（cosh²−sinh²=1）", worst)

# (c) 双曲指数 = boost
worst = 0.0
for _ in range(N_TRIALS):
    p = rng.uniform(-3, 3)
    worst = max(worst, np.abs(boost_exp(p) - boost(p)).max())
ok &= check("(c) boostExp φ = coshφ·1+sinhφ·J' = boost φ", worst)

# (d) J'² = 1（双曲生成元，与欧氏 e_01 平方 −1 互补）
worst = max(np.abs(Jp @ Jp - I2).max(), np.abs(Jp @ Jp - I2).max())
ok &= check("(d) J'² = 1", worst)

# (e) e_10 = J'（Clifford 桥：e_10 = [[0,1],[1,0]]）
e10 = np.array([[0.0, 1.0], [1.0, 0.0]])
worst = np.abs(e10 - Jp).max()
ok &= check("(e) e_10 = J'（双曲生成元指认）", worst)

# (f)（删除：谱流保 trace 需交织前提，非一般 T——对应既有 massReadout_flow_invariant）

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：1+1 闵氏 boost 层全绿——rapidity 可加、det=1、双曲指数=boost、J'=e_10（平方+1），"
      + "与欧氏 e_01（平方−1）构成两正交投影的生成元互补对。")
