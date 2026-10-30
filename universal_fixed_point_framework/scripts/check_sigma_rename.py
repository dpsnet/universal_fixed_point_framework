# -*- coding: utf-8 -*-
"""验证 transform 后框架常数 σ 保留（6σ³/σ³/σ⁻¹/σ=1/15/σ²等）"""
import sys, re
sys.path.insert(0, r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts')
from rename_sigma_score import transform

for path in [r'E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md',
             r'E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md']:
    with open(path, encoding='utf-8') as f:
        t = f.read()
    nt, nA, nB, nC = transform(t)
    print(f"=== {path.split(chr(92))[-1]} ===")
    # 框架常数保护检查
    checks = ['6σ³', 'σ³(1', 'σ³', 'σ⁻¹', 'σ = 1/15', 'σ²', 'σ⁵', 'σ⁷', '1+6σ³', '(1+6σ³)', 'σ 恒等', 'σ 锁定', 'σ 通道', 'σ 身份']
    for c in checks:
        # 检查替换后框架模式是否仍在（未被 σ_score 污染）
        polluted = ('σ_score' in nt) and (c in nt.replace('σ_score', 'σ'))
        print(f"  {c}: {'保留' if c in nt or c.replace('σ_score','σ') in nt else '缺失?'}")
    # 抽样判定替换正确性
    samples = ['0.034σ_score', '63 万σ_score', 'σ_score = 0.064', 'σ_score = 632055', 'σ_score 口径', 'σ_score 提示']
    for s in samples:
        print(f"  判定{s}: {'OK' if s in nt else '未出现'}")
