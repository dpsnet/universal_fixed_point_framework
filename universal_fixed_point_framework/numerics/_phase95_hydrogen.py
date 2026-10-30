# -*- coding: utf-8 -*-
"""Phase 95 M95-2：2D 氢大网格收敛复核 (6000, 120, 16) vs 基准 (1500, 60, 8)
B=0.2 a.u.（η_sc 峰值），k_per_m=150 控算力
"""
import sys, json, io, importlib.util
import numpy as np
# 环境缺 PIL——绕过模块顶部 matplotlib import，源码级加载所需函数
_spec = importlib.util.spec_from_file_location(
    "p48conv", r"E:\workspace\hyper-resolution\universal_fixed_point_framework\numerics\paper48_convergence.py")
_mod = importlib.util.module_from_spec(_spec)
_src = open(_spec.origin, encoding="utf-8").read()
# 剥离 matplotlib import 后 exec
_lines = [l for l in _src.splitlines(True)
          if not l.lstrip().startswith("import matplotlib")
          and "matplotlib.use" not in l
          and "matplotlib.pyplot" not in l
          and "plt.rcParams" not in l
          and "import matplotlib" not in l]
exec("".join(_lines), _mod.__dict__)
compute_spectrum = _mod.compute_spectrum
compute_d2 = _mod.compute_d2
compute_eta_sc = _mod.compute_eta_sc

B = 0.2
print("=== M95-2 2D 氢大网格 ===", flush=True)
res = {}
for cfg in [(1500, 60, 8), (6000, 120, 16)]:
    N_r, r_max, m_max = cfg
    print("  cfg N_r=%d r_max=%d m_max=%d ..." % cfg, flush=True)
    lambdas = compute_spectrum(N_r, r_max, m_max, B, k_per_m=150)
    n = len(lambdas)
    D2, rsq = compute_d2(lambdas)
    eta = compute_eta_sc(D2)
    res["%s" % (cfg,)] = {"n": n, "D2": D2, "rsq": rsq, "eta_sc": eta}
    print("    n=%d D2=%.4f (R2=%.3f) eta=%.4f" % (n, D2, rsq, eta), flush=True)
with io.open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\numerics\paperX_hydrogen_largegrid.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("done")
