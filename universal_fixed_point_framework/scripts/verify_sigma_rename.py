# -*- coding: utf-8 -*-
import sys, io
sys.path.insert(0, r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts')
from rename_sigma_score import transform

for path in [r'E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md',
             r'E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md']:
    t = io.open(path, encoding='utf-8').read()
    nt, a, b, c = transform(t)
    print(f"=== {path.split(chr(92))[-1]} ===")
    print(f"  σ = 1/15 保留数: {nt.count('σ = 1/15')}（原 {t.count('σ = 1/15')}）")
    print(f"  σ_score = 替换数: {nt.count('σ_score = ')}")
    print(f"  A={a} B={b} C={c}")
    print(f"  抽样: {[m for m in ['σ_score = 0.064','σ_score = 632055','0.034σ_score','63 万σ_score','σ_score 口径','σ_score 提示'] if m in nt]}")
    print(f"  6σ³ 保留: {'6σ³' in nt}")
    print()
