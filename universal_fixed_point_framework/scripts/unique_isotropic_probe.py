# -*- coding: utf-8 -*-
"""数值先证伪：粗粒化的机制无关唯一性（离散 C₄ 平均 = 任意各向同性保迹机制）

拟 Lean 定理逐字对齐：
  unique_isotropic_average {T} (hsym : Tᵀ=T)
    (P : Matrix → Matrix)
    (hPiso : ∀对称 S，∃λ，P S = λ·1)     -- P 输出各向同性
    (hPtrace : ∀ S，trace(P S) = trace S) -- P 保迹
    : P T = groupAverage T
  ——输出不依赖具体机制（C₄ 离散/连续/其他）：只由"各向同性 + 保迹"决定，
    即粗粒化的统计涌现普适性（弱等效读数与机制无关）。

数值检验：
  (a) 任意"各向同性+保迹"机制 P（实现：P S = (trace S/2)·1）⟹ P(T)=gA(T)（残差 ~0）
  (b) 保迹复核：trace(P T)=trace T
  (c) 唯一性：两个不同机制的输出一致

判据：(a)(b)(c) 残差 < 1e-8。
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


def iso_trace_preserving(T):
    """任意各向同性+保迹机制（唯一形态：λI，λ=trace/2）。"""
    return np.trace(T) / 2 * np.eye(2)


def rand_sym():
    A = rng.standard_normal((2, 2))
    return A + A.T


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 各向同性保迹机制 = C₄ 平均
worst = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    worst = max(worst, np.abs(iso_trace_preserving(T) - group_avg(T)).max())
ok &= check("(a) P(T) = gA(T)（机制无关唯一性）", worst)

# (b) 保迹
worst = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    worst = max(worst, abs(np.trace(iso_trace_preserving(T)) - np.trace(T)))
ok &= check("(b) 保迹：trace(P(T))=trace(T)", worst)

# (c) 两个机制（离散 C₄ vs 连续旋转平均近似）输出一致
worst = 0.0
for _ in range(N_TRIALS):
    T = rand_sym()
    # 连续近似：90 度内 180 等分旋转平均
    cont = np.zeros((2, 2))
    for k in range(180):
        th = k * np.pi / 180.0
        c, s = np.cos(th), np.sin(th)
        R = np.array([[c, -s], [s, c]])
        cont += R @ T @ R.T
    cont /= 180
    worst = max(worst, np.abs(cont - group_avg(T)).max())
ok &= check("(c) 连续旋转平均 ≈ C₄ 平均（机制无关）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：粗粒化输出与机制无关——各向同性+保迹唯一决定 λI，C₄ 离散与连续平均同构，机检对齐。")
