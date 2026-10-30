# -*- coding: utf-8 -*-
"""Phase 103e: 转化映射定量化（观测连续谱增强 vs 三机制预测对比）
1) 读三机制分解 json，提取 eta_comp/eta_line 随 B
2) 与观测 blue_calres 分档增强对比
3) 检验 '转移 ∝ 横向压缩(eta_comp)' 假说 + 外推 B_crit
"""
import json, math

BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'
with open(BASE + r'\_phase100_p3_mechanism_decomposition.json', encoding='utf-8') as f:
    dec = json.load(f)
print('=== mechanism_decomposition 结构 ===')
print('keys:', list(dec.keys()) if isinstance(dec, dict) else type(dec).__name__)
s = json.dumps(dec, ensure_ascii=False)
print('chars:', len(s))
print(s[:2500])
