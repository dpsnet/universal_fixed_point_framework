# -*- coding: utf-8 -*-
"""Phase 95 M95-1：Harper 模型有限尺寸标度扩展（N=8000/16000，λ=2.0）
复用 harper_enhanced_analysis 的 analyze_lambda
"""
import sys, json, io, os
import numpy as np
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\harper_analysis")
from harper_enhanced_analysis import analyze_lambda

alpha = (np.sqrt(5) - 1) / 2
print("=== M95-1 Harper λ=2.0 N=8000/16000 ===", flush=True)
res = []
for N in (8000, 16000):
    print("  N=%d ..." % N, end=" ", flush=True)
    try:
        r = analyze_lambda(2.0, N, alpha, 0.0)
        res.append(r)
        print("D0=%.3f D2=%.3f eta=%.3f IPR/N=%.1f (%.1fs)" % (
            r['D_q']['0'], r['D2'], r['eta_sc'], r['ipr_over_N'], r['elapsed_seconds']), flush=True)
    except MemoryError:
        print("MemoryError", flush=True)
        res.append({"N": N, "error": "MemoryError"})
with io.open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\numerics\paperX_harper_n8k16k.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("done")
