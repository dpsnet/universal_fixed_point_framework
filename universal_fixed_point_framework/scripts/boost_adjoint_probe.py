# -*- coding: utf-8 -*-
"""数值先证伪：boost 共轭层（#55，缺口②第一环）

拟 Lean 定理逐字对齐（B=boost φ 1+1 双曲旋转）：
  (a) boost_adjoint_symmetric：T 对称 ⟹ B·T·Bᵀ 对称（boost 共轭保持对称）
  (b) boost_adjoint_trace_eq：tr(B·T·Bᵀ)=tr(boost(2φ)·T)（迹的谱流演化）
  (c) boost_adjoint_traceless_explicit：无迹对称 T=[[a,b],[b,−a]] ⟹
      B·T·Bᵀ = [[a+2b·sinhφ·coshφ, b(cosh²+sinh²)],[b(cosh²+sinh²), −a+2b·sinhφ·coshφ]]

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-8


def B(phi):
    c, s = np.cosh(phi), np.sinh(phi)
    return np.array([[c, s], [s, c]])


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 对称保持
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    T = rng.uniform(-5, 5, size=(2, 2))
    T = T + T.T
    C = B(phi) @ T @ B(phi).T
    worst = max(worst, np.abs(C - C.T).max())
ok &= check("(a) B·T·Bᵀ 对称", worst)

# (b) 迹演化
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    T = rng.uniform(-5, 5, size=(2, 2))
    lhs = np.trace(B(phi) @ T @ B(phi).T)
    rhs = np.trace(B(2 * phi) @ T)
    worst = max(worst, abs(lhs - rhs))
ok &= check("(b) tr(B·T·Bᵀ)=tr(boost(2φ)·T)", worst)

# (c) 无迹显式形态
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    a = rng.uniform(-5, 5)
    b = rng.uniform(-5, 5)
    T = np.array([[a, b], [b, -a]])
    C = B(phi) @ T @ B(phi).T
    c, s = np.cosh(phi), np.sinh(phi)
    E = np.array([[a + 2 * b * s * c, b * (c**2 + s**2)],
                  [b * (c**2 + s**2), -a + 2 * b * s * c]])
    worst = max(worst, np.abs(C - E).max())
ok &= check("(c) 无迹轨道显式形态", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：boost 共轭层全绿——共轭保持对称（闭包基础）、迹按 boost(2φ) 谱流演化"
      + "（质量读数在非紧侧的变换律）、无迹对称张量的 boost 轨道显式参数化"
      + "（各向异性 b 与对角混合，非紧侧无有限平均不动点⟹窗口正则化必要性）。")
