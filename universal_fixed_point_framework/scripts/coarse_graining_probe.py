# -*- coding: utf-8 -*-
"""数值先证伪：粗粒化机制——弥漫平均（粗粒化算符）保迹

拟 Lean 定理逐字对齐（ℝ 2×2）：
  (a) ★ groupAverage_trace_eq：trace(groupAverage T) = trace(T)
      ——粗粒化（弥漫平均=幂等投影）不改变宏观读数（涌现稳定性/粗粒化守恒）
  (b) gA(T) 旋转不变（输出各向同性——粗粒化→各向同性必然，复核既有闭合）
  (c) gA(gA(T)) = gA(T)（幂等投影复核——粗粒化是投影）
  (d) 读数一致对一般随机 T 与旋转不变族 T 均成立

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


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 保迹：一般随机 T
worst = 0.0
for _ in range(N_TRIALS):
    T = rng.normal(size=(2, 2))
    worst = max(worst, abs(np.trace(gA(T)) - np.trace(T)))
ok &= check("(a) trace(gA(T)) = trace(T)（一般随机 T）", worst)

# (a2) 保迹：旋转不变族 T（AI+bJ）
worst = 0.0
for _ in range(N_TRIALS):
    a, b = rng.normal(size=2)
    T = a * np.eye(2) + b * J
    worst = max(worst, abs(np.trace(gA(T)) - np.trace(T)))
ok &= check("(a2) 保迹（旋转不变族 T）", worst)

# (b) gA(T) 旋转不变（输出各向同性）
worst = 0.0
for _ in range(N_TRIALS):
    T = rng.normal(size=(2, 2))
    th = rng.uniform(-10, 10)
    R = rot(th)
    worst = max(worst, np.abs(R @ gA(T) @ R.T - gA(T)).max())
ok &= check("(b) gA(T) 旋转不变（输出各向同性）", worst)

# (c) 幂等（粗粒化是投影）
worst = 0.0
for _ in range(N_TRIALS):
    T = rng.normal(size=(2, 2))
    worst = max(worst, np.abs(gA(gA(T)) - gA(T)).max())
ok &= check("(c) gA(gA(T)) = gA(T)（幂等投影）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：粗粒化（弥漫平均）保迹 trace(gA(T))=trace(T)（涌现稳定性）、"
      + "输出旋转不变（各向同性必然）、幂等投影——粗粒化机制代数核心，"
      + "与 groupAverage_rotation_invariant_all/groupAverage_idempotent 合流")
