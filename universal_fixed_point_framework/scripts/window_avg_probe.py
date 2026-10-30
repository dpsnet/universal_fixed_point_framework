# -*- coding: utf-8 -*-
"""数值先证伪：窗口 boost 平均定理（#56，缺口②收口）

3 点对称窗口平均：Avg_φ(T)=(1/3)[B(−φ)·T·B(−φ)ᵀ + T + B(φ)·T·B(φ)ᵀ]
拟 Lean 定理：
  (a) boost_window3_avg_traceless_form：无迹对称 T=[[a,b],[b,−a]] ⟹
      Avg = [[a, b(1+2(coshφ²+sinhφ²))/3],[b(1+2(coshφ²+sinhφ²))/3, −a]]
      ——窗口平均保持无迹对称形态（对角不动、非对角同号缩放）
  (b) boost_window3_avg_diag_fixed：Avg 00 = a、Avg 11 = −a（对角分量不动）
  (c) boost_window3_avg_scale_factor_ge_one：缩放因子 (1+2cosh(2φ))/3 ≥ 1
      ——不消灭各向异性（与旋转平均相反：非紧侧窗口平均放大非对角）

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-8


def B(phi):
    c, s = np.cosh(phi), np.sinh(phi)
    return np.array([[c, s], [s, c]])


def Avg(phi, T):
    return (B(-phi) @ T @ B(-phi).T + T + B(phi) @ T @ B(phi).T) / 3.0


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 形态定理
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    a = rng.uniform(-5, 5)
    b = rng.uniform(-5, 5)
    T = np.array([[a, b], [b, -a]])
    c, s = np.cosh(phi), np.sinh(phi)
    E = np.array([[a, b * (1 + 2 * (c**2 + s**2)) / 3.0],
                  [b * (1 + 2 * (c**2 + s**2)) / 3.0, -a]])
    worst = max(worst, np.abs(Avg(phi, T) - E).max())
ok &= check("(a) 窗口平均保持无迹对称形态", worst)

# (b) 对角不动
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    a = rng.uniform(-5, 5)
    b = rng.uniform(-5, 5)
    T = np.array([[a, b], [b, -a]])
    A = Avg(phi, T)
    worst = max(worst, abs(A[0, 0] - a) + abs(A[1, 1] + a))
ok &= check("(b) 对角分量不动 (Avg₀₀=a, Avg₁₁=−a)", worst)

# (c) 缩放因子 ≥1
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    f = (1 + 2 * np.cosh(2 * phi)) / 3.0
    if f < 1 - 1e-12:
        worst = max(worst, 1 - f)
ok &= check("(c) 缩放因子 (1+2cosh2φ)/3 ≥ 1", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：窗口 boost 平均定理全绿——3 点对称窗口平均保持无迹对称形态"
      + "（对角不动、非对角同号缩放），缩放因子≥1 不消灭各向异性："
      + "非紧侧等变平均只能在有限窗口发生（静默窗口机制），与旋转平均互补。")
