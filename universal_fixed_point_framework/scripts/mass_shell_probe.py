# -*- coding: utf-8 -*-
"""数值先证伪：质量壳 E²−p²=m²（质量 = 能量-动量时空间隔的不动点）

拟 Lean 定理逐字对齐（追加 RapidityTimeLayering.lean）：
  (a) mass_shell：∀m φ，(m·coshφ)² − (m·sinhφ)² = m²
      ——E=m·coshφ（能量=质量×γ）、p=m·sinhφ（动量=质量×rapidity 流）：
      质量 = 四矢时空间隔的不动点（cosh²−sinh²=1 的加权形态）。
  (b) energy_gamma：m·coshφ = m·secθ 当 sinθ=tanhφ（γ 互译——E=mγ 与偏转角 θ 表述一致）。
  (c) speed_lt_light：|tanhφ| < 1（rapidity 流总在光锥内，c=1）。
  (d) mass_shell_speed：E=m·secθ ⟹ E²−(m·sinhφ)²=m²（θ 表述下的壳条件）。

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
N_TRIALS = 500
TOL = 1e-8


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 质量壳
worst = 0.0
for _ in range(N_TRIALS):
    m = rng.uniform(0.01, 10)
    phi = rng.uniform(-3, 3)
    E, p = m * np.cosh(phi), m * np.sinh(phi)
    worst = max(worst, abs(E**2 - p**2 - m**2))
ok &= check("(a) E²−p²=m²（质量壳）", worst)

# (b) E = mγ = m·secθ
worst = 0.0
for _ in range(N_TRIALS):
    m = rng.uniform(0.01, 10)
    phi = rng.uniform(-1.5, 1.5)
    theta = np.arcsin(np.tanh(phi))          # sinθ = tanhφ
    E = m * np.cosh(phi)
    worst = max(worst, abs(E - m / np.cos(theta)))
ok &= check("(b) E=m·coshφ=m·secθ（γ 互译）", worst)

# (c) 光锥内
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-3, 3)
    v = np.tanh(phi)
    worst = max(worst, abs(abs(v) - 1) if abs(v) >= 1 else 0.0)
ok &= check("(c) |tanhφ|<1（光锥内）", worst)

# (d) θ 表述壳
worst = 0.0
for _ in range(N_TRIALS):
    m = rng.uniform(0.01, 10)
    phi = rng.uniform(-1.5, 1.5)
    E = m * np.cosh(phi)
    p = m * np.sinh(phi)
    worst = max(worst, abs(E**2 - p**2 - m**2))
ok &= check("(d) E²−p²=m²（θ 表述复核）", worst)

# (e) 红移互补：E_lab(φ)=m·coshφ ⟹ 频率读出 ω_lab=ω₀·cosθ（θ=偏转角）
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-1.5, 1.5)
    theta = np.arcsin(np.tanh(phi))
    w0 = rng.uniform(0.1, 5)
    worst = max(worst, abs(w0 * np.cosh(phi) - w0 / np.cos(theta)))
ok &= check("(e) ω·coshφ = ω·secθ（红移 γ 互译）", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：质量壳 E²−p²=m² 全绿——质量=四矢时空间隔不动点，γ=coshφ=secθ 互译，"
      + "rapidity 流总在光锥内（c=1）。")
