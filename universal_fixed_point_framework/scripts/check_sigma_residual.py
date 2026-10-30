# -*- coding: utf-8 -*-
"""检查替换后残留的判定语义 σ（简化正则）"""
import io, re

for path in [r'E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md',
             r'E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md']:
    t = io.open(path, encoding='utf-8').read()
    print(f"=== {path.split(chr(92))[-1]} ===")
    # 残留 σ = 数字（非 1/15）
    res = re.findall(r'σ = \d+\.?\d*[^/]', t)
    print(f"  残留 σ = 数字: {len(res)}")
    for r in res[:8]: print(f"    {r}")
    # 残留 数字σ + 空格判定词
    res2 = re.findall(r'\d+(?:\.\d+)?σ \w+', t)
    print(f"  残留 数字σ+词: {len(res2)}")
    for r in res2[:8]: print(f"    {r}")
    # 残留 σ + 判定词
    res3 = re.findall(r'σ (?:提示|达标|不达标|口径|方法论|判定|分级|矩阵|审计|重审计|体系化|统一后|不适用|锁定|恒等|身份)', t)
    print(f"  残留 σ+词: {len(res3)}")
    for r in res3[:8]: print(f"    {r}")
    # 残留 σ_score 后跟公式字符（检查替换是否把判定和公式混淆）
    bad = re.findall(r'σ_score(?=³|²|⁴|⁵|⁶|⁷|⁸|⁻|\^)', t)
    print(f"  σ_score+上标（错误）: {len(bad)}")
    print()
