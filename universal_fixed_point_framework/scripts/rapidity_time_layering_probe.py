# -*- coding: utf-8 -*-
"""§6 先证伪：rapidity 恒等式 + 谱流保迹（质量=谱流不动点的谱侧）。
按 Lean 目标翻译：
  1) cosh(φ1+φ2) = coshφ1·coshφ2 + sinhφ1·sinhφ2   （rapidity 可加）
  2) cosh²φ − sinh²φ = 1
  3) sec²θ = 1 + tan²θ（cosθ ≠ 0）
  4) trace(exp(−t·G)·A·exp(t·G)) = trace A          （谱流保迹）
随机样本残差 < 1e-8 全部通过。
"""
import numpy as np

rng = np.random.default_rng(20261024)
ok = True
for trial in range(8):
    phi1, phi2 = rng.normal(size=2)
    theta = rng.uniform(-1.2, 1.2)          # cosθ 非零区
    n = int(rng.integers(2, 5))
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    G = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    t = float(rng.uniform(0.3, 1.5))

    r1 = np.cosh(phi1 + phi2) - (np.cosh(phi1) * np.cosh(phi2) + np.sinh(phi1) * np.sinh(phi2))
    r2 = np.cosh(phi1) ** 2 - np.sinh(phi1) ** 2 - 1.0
    r3 = (1.0 / np.cos(theta)) ** 2 - (1.0 + (np.sin(theta) / np.cos(theta)) ** 2)
    Af = np.linalg.matrix_power(np.eye(n), 1)  # 占位
    expm = __import__("scipy.linalg", fromlist=["expm"]).expm
    A_flow = expm(-t * G) @ A @ expm(t * G)
    r4 = np.abs(np.trace(A_flow) - np.trace(A))
    print(f"trial {trial}: rapidity_add={r1:.3e}  cosh2_minus_sinh2={r2:.3e}  sec2_tan2={r3:.3e}  flow_trace={r4:.3e}")
    ok = ok and abs(r1) < 1e-8 and abs(r2) < 1e-8 and abs(r3) < 1e-8 and r4 < 1e-8

print("ALL PASS（命题为真，可投入证明）" if ok else "FAIL（命题为假，走勘误流程）")
