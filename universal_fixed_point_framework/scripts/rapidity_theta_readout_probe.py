# -*- coding: utf-8 -*-
"""开放口推进先证伪：φ↔θ 桥 + §8 读出红移公式。
按 Lean 目标翻译：
  1) sinθ = tanhφ ⟹ coshφ²·cosθ² = 1      （rapidity_theta_identity，平方层桥）
  2) sinθ = tanhφ ∧ cosθ>0 ⟹ coshφ·cosθ = 1 （gamma_cosh_sec，coshφ=secθ）
  3) ω₀/coshφ = ω₀·(1/coshφ)               （readout_frequency_redshift，trivial 恒等）
  4) coshφ·cosθ=1 ⟹ ω₀/coshφ = ω₀·cosθ     （readout_sec_form，读出红移偏转角形式）
随机样本残差 < 1e-8 全部通过。
"""
import numpy as np

rng = np.random.default_rng(20261024)
ok = True
for trial in range(10):
    phi = float(rng.uniform(-2.0, 2.0))
    v = np.tanh(phi)
    theta = float(np.arcsin(np.clip(v, -0.99, 0.99)))   # sinθ = tanhφ
    w0 = float(rng.uniform(0.5, 3.0))

    r1 = np.cosh(phi) ** 2 * np.cos(theta) ** 2 - 1.0
    r2 = np.cosh(phi) * np.cos(theta) - 1.0
    r3 = w0 / np.cosh(phi) - w0 * (1.0 / np.cosh(phi))
    r4 = w0 / np.cosh(phi) - w0 * np.cos(theta)
    print(f"trial {trial}: theta_id={r1:.3e}  cosh_sec={r2:.3e}  freq_def={r3:.3e}  sec_form={r4:.3e}")
    ok = ok and abs(r1) < 1e-8 and abs(r2) < 1e-8 and abs(r3) < 1e-8 and abs(r4) < 1e-8

print("ALL PASS（命题为真，可投入证明）" if ok else "FAIL（命题为假，走勘误流程）")
