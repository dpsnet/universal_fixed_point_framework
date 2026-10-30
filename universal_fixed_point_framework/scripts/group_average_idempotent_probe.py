# -*- coding: utf-8 -*-
"""数值先证伪：强制平均的投影性质（§7.6① 三项形式化待证之第 2 项前哨）

目标命题族（与 Lean groupAverage = (1/4)Σ R_i·T·R_iᵀ 逐字对齐）：
  (a) 幂等性  groupAverage(groupAverage(T)) = groupAverage(T)   ——预期残差 0（群平均投影性质）
  (b) 保正交  T·Tᵀ=I ⟹ groupAverage(T) 正交                     ——预期残差非零（欧氏平均不保正交，
       Karcher/谱测度平均必要性的数值反证证据）
  (c) 保对称  Tᵀ=T ⟹ (groupAverage(T))ᵀ = groupAverage(T)      ——预期残差 0（共轭平均保对称）

判据：|残差|max 容差 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N = 500


def R0():
    return np.array([[1.0, 0.0], [0.0, 1.0]])


def R1():
    c, s = np.cos(np.pi / 2), np.sin(np.pi / 2)
    return np.array([[c, -s], [s, c]])


def R2():
    c, s = np.cos(np.pi), np.sin(np.pi)
    return np.array([[c, -s], [s, c]])


def R3():
    c, s = np.cos(-np.pi / 2), np.sin(-np.pi / 2)
    return np.array([[c, -s], [s, c]])


RS = [R0(), R1(), R2(), R3()]


def group_avg(M):
    return sum(R @ M @ R.T for R in RS) / 4.0


# (a) 幂等性
worst_idem = 0.0
idem_ok = True
for _ in range(N):
    M = rng.normal(size=(2, 2))
    w = np.abs(group_avg(group_avg(M)) - group_avg(M)).max()
    worst_idem = max(worst_idem, w)
    if w > 1e-8:
        idem_ok = False
print(f"[{'PASS' if idem_ok else 'FAIL'}] 幂等性 groupAverage²=groupAverage  最差残差 = {worst_idem:.3e}")

# (b) 保正交（预期证伪：欧氏平均不保正交）
worst_orth = 0.0
orth_ok = True
for _ in range(N):
    A = rng.normal(size=(2, 2))
    Q, _ = np.linalg.qr(A)
    M = group_avg(Q)
    w = np.abs(M @ M.T - np.eye(2)).max()
    worst_orth = max(worst_orth, w)
    if w > 1e-8:
        orth_ok = False
print(f"[{'PASS' if orth_ok else 'FAIL'}] 保正交（欧氏平均）  最差残差 = {worst_orth:.3e}"
      + ("  → 预期非零：欧氏平均不保正交，Karcher/谱测度平均必要" if not orth_ok else "  → 意外：欧氏平均保正交"))

# (c) 保对称
worst_sym = 0.0
sym_ok = True
for _ in range(N):
    A = rng.normal(size=(2, 2))
    S = (A + A.T) / 2.0
    M = group_avg(S)
    w = np.abs(M - M.T).max()
    worst_sym = max(worst_sym, w)
    if w > 1e-8:
        sym_ok = False
print(f"[{'PASS' if sym_ok else 'FAIL'}] 保对称 groupAverage(T)ᵀ=groupAverage(T)  最差残差 = {worst_sym:.3e}")

ok = idem_ok and sym_ok and (not orth_ok)
print("ALL PASS" if ok else "SOME FAIL")
print(f"摘要：幂等 {worst_idem:.2e}（=0 投影）、保正交 {worst_orth:.2e}（≠0 反证）、保对称 {worst_sym:.2e}（=0 保持）")
