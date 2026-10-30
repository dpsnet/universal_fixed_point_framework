# -*- coding: utf-8 -*-
"""n=9 独立复核违反诊断：seed 77 的 15000 样本中，
违反样本的 pat 是否在主样本表中？值是否匹配？模式特征？
"""
import json, os, random, sys
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n9_criterion import adj_partition_factors

BASE27 = ['s2_3', 's2_3456789', 's23_456789', 's234_56789', 's2345678_9',
          's3_4', 's3_456789', 's34_56789', 's345_6789',
          's4_5', 's4_56789', 's45678_9',
          's5_6', 's5_678', 's56_78', 's5_6789', 's5678_9',
          's6_7', 's67_8', 's6_789', 's678_9',
          's7_8', 's7_89', 's78_9', 's8_9',
          's1_2345', 's123_456789']


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    factors = adj_partition_factors(9)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in BASE27]

    # 主样本表（seed 131, 40000）
    rng = random.Random(131)
    pat_a = defaultdict(set)
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(9, 0, r1=True, momentum=True, rng=rng)
        pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)
        pat_a[pat].add(round(A_BG(9, omega, zbar), 6))
    print(f"主样本表 {len(pat_a)} 模式", flush=True)

    # seed 77 独立 15000
    rng = random.Random(77)
    missing = 0        # pat 不在表中
    mismatched = 0     # pat 在表中但值不同
    viol_pat_feat = Counter()
    viol_samples = []
    for _ in range(15000):
        omega, zbar, _ = gen_partial_collinear(9, 0, r1=True, momentum=True, rng=rng)
        pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)
        a = round(A_BG(9, omega, zbar), 6)
        vals = pat_a.get(pat)
        if vals is None:
            missing += 1
        elif a not in vals:
            mismatched += 1
            viol_pat_feat[tuple(sorted(vals))] += 1
            if len(viol_samples) < 8:
                viol_samples.append((pat, a, vals))
    print(f"独立样本 15000: 模式缺失 {missing}  值不匹配 {mismatched}", flush=True)
    print(f"值不匹配的表中值形态: {dict(viol_pat_feat)}", flush=True)
    for pat, a, vals in viol_samples:
        print(f"  viol: A_BG={a} 表中={sorted(vals)} 非零因子 {sum(1 for x in pat if x != 0)}/{len(pat)}", flush=True)
