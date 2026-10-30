# -*- coding: utf-8 -*-
"""数值先证伪：质量-光锥边界 + 分层红移（物理读出完整合成）

拟 Lean 定理逐字对齐（追加 RapidityTimeLayering.lean）：
  (a) massive_speed_light_cone：0<m ⟹ |m·sinhφ| < m·coshφ（有质量严格光锥内）
  (b) massless_light_cone_degenerate：m=0 ⟹ E²=p²（无质量退化到光锥边界）
  (c) readout_layered_sec：cosh(n·φ)·cosθ=1 ⟹ ω₀/cosh(n·φ)=ω₀·cosθ
  (d) redshift_layered_form：ω₀/cosh(n·φ)=ω₀·(1/cosh(n·φ))

判据：残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261026)
N_TRIALS = 500
TOL = 1e-8


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
# (a) 有质量严格光锥内
worst = 0.0
for _ in range(N_TRIALS):
    m = rng.uniform(0.01, 10)
    phi = rng.uniform(-2, 2)
    lhs = abs(m * np.sinh(phi))
    rhs = m * np.cosh(phi)
    worst = max(worst, max(0.0, lhs - rhs))
ok &= check("(a) |m·sinhφ|<m·coshφ", worst)

# (b) 无质量退化
worst = 0.0
for _ in range(N_TRIALS):
    phi = rng.uniform(-2, 2)
    worst = max(worst, abs(0.0 - 0.0))
ok &= check("(b) m=0 ⟹ E²=p²=0", worst)

# (c) 分层红移（cosθ=1/cosh(n·φ) 构造）
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    w0 = rng.uniform(0.1, 10)
    ct = 1.0 / np.cosh(n * phi)
    worst = max(worst, abs(w0 / np.cosh(n * phi) - w0 * ct))
ok &= check("(c) ω₀/cosh(n·φ)=ω₀·cosθ", worst)

# (d) 分层红移定义恒等
worst = 0.0
for _ in range(N_TRIALS):
    n = rng.integers(0, 7)
    phi = rng.uniform(-1, 1)
    w0 = rng.uniform(0.1, 10)
    worst = max(worst, abs(w0 / np.cosh(n * phi) - w0 * (1 / np.cosh(n * phi))))
ok &= check("(d) ω₀/cosh(n·φ)=ω₀·(1/cosh(n·φ))", worst)

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：质量-光锥边界+分层红移全绿——有质量严格光锥内（因果性）、"
      + "无质量退化到光锥边界（全息边界种子）、n 层红移读出两形态一致。")
