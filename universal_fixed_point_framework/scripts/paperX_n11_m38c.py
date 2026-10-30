# -*- coding: utf-8 -*-
"""M38c：s1_234567891011 重采样分布判别（恒等式 A vs 缓存一致性）
- 重采样 10000（seed 77）→ sg_block((0,),(1..10)) 分布
- 全 0 → 缓存生成 bug（旧数据）
- 非全 0 → 恒等式推导有误（需重新审视）
"""
import os, sys, random
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_single_minus_numerics import sg_block

cnt = Counter()
rng = random.Random(77)
for i in range(10000):
    omega, zbar, _ = gen_partial_collinear(11, 0, r1=True, momentum=True, rng=rng)
    v = sg_block(omega, zbar, (0,), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    cnt[v] += 1
print("重采样 s1_234567891011 分布:", dict(cnt))

# 同时实测恒等式 A：Σ_{j≠0} ω0 ωj (z0 - zj)
bad = 0
rng2 = random.Random(77)
for i in range(1000):
    omega, zbar, _ = gen_partial_collinear(11, 0, r1=True, momentum=True, rng=rng2)
    s = sum(omega[0] * omega[j] * (zbar[0] - zbar[j]) for j in range(1, 11))
    if abs(s) > 1e-9:
        bad += 1
print(f"恒等式 A 直接实测（Σ_{{j≠0}} P[0][j] = 0）：{bad}/1000 偏差")
