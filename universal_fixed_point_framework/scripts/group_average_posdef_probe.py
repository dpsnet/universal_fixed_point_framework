# -*- coding: utf-8 -*-
"""数值先证伪：粗粒化保正定 + 各向同性质量读数为正

拟 Lean 定理逐字对齐：
  (a) groupAverage_preserves_posdef：T 对称正定 ⟹ groupAverage(T) 正定
      ——C₄ 共轭保正定（正交共轭）+ 正组合闭包；粗粒化保持能量/质量谱正性。
  (b) groupAverage_posdef_isotropy_pos：T 正定 ⟹ ∃λ>0, groupAverage(T)=λI
      ——各向同性（旋转不变⟹λI）+ 保正定 + 保迹（trace>0 ⟹ λ=trace/2>0）；
      宏观质量读数为正。
  (c) 保迹复核：trace(gA(T))=trace(T)。

判据：(a)(c) 残差 < 1e-8；(b) min λ > 0。
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


def rand_pd():
    B = rng.standard_normal((2, 2))
    T = B @ B.T + 1.0 * np.eye(2)   # 对称正定
    return T


def check(name, resid, ref=None):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}" +
          (f"（ref={ref:.3e}）" if ref is not None else ""))
    return ok


ok = True
# (a) 保正定：T 正定 ⟹ gA(T) 正定（min vᵀgA(T)v over 单位向量扫角）
worst = 0.0
lam_min = 1e9
for _ in range(N_TRIALS):
    T = rand_pd()
    G = group_avg(T)
    # 最小特征值（正定 ⟺ 对称 + 特征值>0）
    ev = np.linalg.eigvalsh((G + G.T) / 2)
    lam_min = min(lam_min, ev.min())
    worst = max(worst, np.abs(G - G.T).max())   # 对称性残差
ok &= check("(a) 保正定：groupAverage(T) 对称正定（min λ>0）", worst)
print(f"     (a) min eig(gA(T)) = {lam_min:.6e} (>0 ✓)" if lam_min > 0 else "     (a) min eig ≤ 0 ✗")

# (b) 各向同性 + λ>0：gA(T) ≈ λI，λ = trace(T)/2 > 0
worst = 0.0
lam_pos = 1e9
for _ in range(N_TRIALS):
    T = rand_pd()
    G = group_avg(T)
    lam = np.trace(T) / 2
    worst = max(worst, np.abs(G - lam * np.eye(2)).max())
    lam_pos = min(lam_pos, lam)
ok &= check("(b) 各向同性输出：groupAverage(T)=λI，λ=trace(T)/2", worst)
print(f"     (b) min λ = {lam_pos:.6e} (>0 ✓)" if lam_pos > 0 else "     (b) min λ ≤ 0 ✗")

# (c) 保迹复核
worst = 0.0
for _ in range(N_TRIALS):
    T = rand_pd()
    worst = max(worst, abs(np.trace(group_avg(T)) - np.trace(T)))
ok &= check("(c) 保迹：trace(gA(T))=trace(T)", worst)

print("ALL PASS" if ok and lam_min > 0 and lam_pos > 0 else "SOME FAIL")
print("摘要：粗粒化保正定 + 各向同性 ⟹ λI 且 λ=trace/2>0——宏观质量读数为正，机检对齐。")
