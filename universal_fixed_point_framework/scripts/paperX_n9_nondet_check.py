# -*- coding: utf-8 -*-
"""n=9 非决定性复核：诊断 8 个非决定模式的真实结构。
疑问：诊断脚本判 s1_2 区分 8 模式，但 26 因子重算仍 8 非决定、模式数不变。
假设：s1_2 在非决定模式的样本上取值被 25 维模式决定（未分裂）。
逐一打印非决定模式的样本 A_BG 与 s1_2/s12_3 取值，验证真相。
"""
import json, os, random, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n9_criterion import adj_partition_factors

BASE = ['s2_3', 's2_3456789', 's23_456789', 's234_56789', 's2345678_9',
        's3_4', 's3_456789', 's34_56789', 's345_6789',
        's4_5', 's4_56789', 's45678_9',
        's5_6', 's5_678', 's56_78', 's5_6789', 's5678_9',
        's6_7', 's67_8', 's6_789', 's678_9',
        's7_8', 's7_89', 's78_9', 's8_9']


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    factors = adj_partition_factors(9)
    NAMES = [factor_name(a, b) for a, b in factors]
    base_idx = [NAMES.index(x) for x in BASE]

    rng = random.Random(131)
    pat_sis = defaultdict(list)
    t0 = 0
    for si in range(40000):
        omega, zbar, _ = gen_partial_collinear(9, 0, r1=True, momentum=True, rng=rng)
        pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in base_idx)
        pat_sis[pat].append((omega, zbar))
    print(f"采样投影完成", flush=True)

    # 非决定模式
    nondet = []
    for pat, lst in pat_sis.items():
        vals = set(round(A_BG(9, o, z), 6) for o, z in lst)
        if len(vals) > 1:
            nondet.append((pat, lst, vals))
    print(f"非决定模式数: {len(nondet)}", flush=True)

    # 对每个非决定模式打印 s1_2 / s12_3 取值
    for idx, (pat, lst, vals) in enumerate(nondet):
        print(f"--- 非决定模式 {idx}: 样本 {len(lst)} 取值 {sorted(vals)}", flush=True)
        s12_vals = defaultdict(set)
        for o, z in lst:
            a = round(A_BG(9, o, z), 6)
            g = "zero" if abs(a) < 1e-9 else ("pos" if a > 0 else "neg")
            s12_vals[g].add(sg_block(o, z, (0,), (1,)))
            s12_vals[g].add(("s12_3", sg_block(o, z, (0, 1), (2,))))
        for g, v in s12_vals.items():
            print(f"   组 {g}: s1_2 取值 {[x for x in v if not isinstance(x, tuple)]}  s12_3 取值 {[x for x in v if isinstance(x, tuple)]}", flush=True)
