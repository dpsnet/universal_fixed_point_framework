# -*- coding: utf-8 -*-
"""全量复查：σ_score 污染异常 + 残留判定 + 框架常数保护"""
import io, re

for path in [r'E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md',
             r'E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md']:
    t = io.open(path, encoding='utf-8').read()
    print(f"=== {path.split(chr(92))[-1]} ===")
    bad1 = re.findall(r'σ_score(?:σ|_score|³|²|⁴|⁵|⁶|⁷|⁸|⁻|\^)', t)
    print(f"  污染异常（σ_score+σ/上标）: {len(bad1)}  {bad1[:6]}")
    res = re.findall(r'σ = \d+\.?\d*[^/]', t)
    print(f"  残留 σ = 数字: {len(res)}  {res[:6]}")
    res2 = re.findall(r'\d+(?:\.\d+)?σ \w+', t)
    print(f"  残留 数字σ+词: {len(res2)}  {res2[:6]}")
    print(f"  σ = 1/15 保留: {t.count('σ = 1/15')}  6σ³ 保留: {'6σ³' in t}")
    print()
