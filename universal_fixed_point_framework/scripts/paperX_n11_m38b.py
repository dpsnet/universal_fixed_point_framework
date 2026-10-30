# -*- coding: utf-8 -*-
"""M38b：s1_234567891011 缓存分布检查（恒等式 A 矛盾排查）"""
import os, sys, pickle, json
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name

factors = adj_partition_factors(11)
NAMES = [factor_name(a, b) for a, b in factors]
print("220 因子总数:", len(factors))
idx = NAMES.index("s1_234567891011")
print("s1_234567891011 索引:", idx, "——因子定义:", factors[idx])

with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
    d3 = pickle.load(f)
with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
    d5 = pickle.load(f)

cnt = Counter()
n_samples = 0
for sd in ['77', '331', '777']:
    for facs, a in d3[sd]:
        cnt[facs[idx]] += 1
        n_samples += 1
for sd in ['211', '555']:
    for facs, a in d5[sd]:
        cnt[facs[idx]] += 1
        n_samples += 1
print(f"样本 {n_samples}——s1_234567891011 符号分布: {dict(cnt)}")

# 对比：44 名单里其他"大块"因子的分布（s1234567_8910 等）
for nm in ["s1234567_8910", "s123_4567891011", "s1_2345", "s2_34567891011"]:
    i2 = NAMES.index(nm)
    c2 = Counter()
    for sd in ['77', '331', '777']:
        for facs, a in d3[sd]:
            c2[facs[i2]] += 1
    print(f"{nm}: {dict(c2)}（3seed 240000）")
