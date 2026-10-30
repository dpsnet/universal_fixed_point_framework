# -*- coding: utf-8 -*-
"""
paperX_n5_analytic_closure.py
单非零项解析闭合的最终数值确认：
对 8 个 BG 分割的每个 ratio_k，用解析符号表（单参数 s）+ 守恒恒等式预测符号，
与数值 ratio_sgn 比对（0 违反 = 解析证明与数值完全一致）。
每分割给出解析表达式（供论文引用）。
"""
import sys
import itertools
import random
import json
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_bg_recursion import bracket, compositions, split_into_blocks
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5
from paperX_single_minus_numerics import sg_pair, sg_block

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}

# 解析预测函数：输入 s（单参数符号表）与困难模式已知恒等式，返回每分割 ratio 符号元组
def analytic_ratios(s):
    """困难模式解析预测（全部经守恒+双线性+符号表闭合）：
    s = s12 = s23 = s51 = s1234 = s14 = s25 = s35
    −s = s34 = s45 = s123 = s234 = s13 = s15 = s24
    E6=E7=s（非零条件）
    活分割 [1]|[234]：ratio=(1,)（num=d 恒）
    [123]|[4]：ratio=(1,)（num=d 恒）
    [12]|[34]：ratio=(1,)
    [12]|[3]|[4]：ratio₀=s123/s234=(−s)/(−s)=1；ratio₁=s51/s45=s/(−s)=−1
    [1]|[23]|[4]：ratio₀=s12/s234=s/(−s)=−1；ratio₁=s51/E7=s/s=1
    [1]|[2]|[34]：ratio₀=s12/s23=1；ratio₁=s123/E6=(−s)/s=−1
    [1]|[2]|[3]|[4]：ratio₀=s12/s23=1；ratio₁=s123/s34=(−s)/(−s)=1；ratio₂=s51/s45=−1
    """
    return {
        "1234": (),
        "123|4": (1,),
        "12|34": (1,),
        "12|3|4": (1, -1),
        "1|234": (1,),
        "1|23|4": (-1, 1),
        "1|2|34": (1, -1),
        "1|2|3|4": (1, 1, -1),
    }


def numeric_ratios(blocks, omega, zbar):
    out = []
    A_ = len(blocks)
    for k in range(A_ - 1):
        d = bracket(blocks[k], blocks[k + 1], omega, zbar)
        K1 = tuple(itertools.chain.from_iterable(blocks[:k + 1]))
        K2 = tuple(itertools.chain.from_iterable(blocks[k + 1:]))
        num = bracket(K1, K2, omega, zbar)
        if d == 0:
            out.append(0)
            continue
        r = num / d
        out.append((r > 0) - (r < 0))
    return tuple(out)


def scan(n_samples=60000, seed=823):
    rng = random.Random(seed)
    elems = tuple(range(1, 5))
    splits = {}
    for cuts in compositions(4, min_parts=1):
        blocks = split_into_blocks(elems, cuts)
        splits["|".join("".join(str(x) for x in b) for b in blocks)] = blocks
    stat = {lbl: {"n": 0, "viol": 0, "numeric_patterns": {}} for lbl in splits}
    n_hard = 0
    n_nonzero = 0
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        n_hard += 1
        s = sg_pair(omega, zbar, 0, 1)
        e6 = sg_block(omega, zbar, (0, 1), (0, 1, 2))
        e7 = sg_block(omega, zbar, (0, 1), (0, 1, 2, 3))
        nonzero = (e6 == e7 and e6 != 0)
        if not nonzero:
            continue
        n_nonzero += 1
        pred = analytic_ratios(s)
        for lbl, blocks in splits.items():
            nr = numeric_ratios(blocks, omega, zbar)
            stat[lbl]["n"] += 1
            stat[lbl]["numeric_patterns"][str(nr)] = stat[lbl]["numeric_patterns"].get(str(nr), 0) + 1
            if tuple(nr) != pred[lbl]:
                stat[lbl]["viol"] += 1
    print(f"困难模式: {n_hard}，非零计入: {n_nonzero}")
    print(f"{'分割':<14}{'n':>6}{'解析预测':>14}{'违反':>6}  数值模式分布")
    all_ok = True
    for lbl in sorted(splits):
        st = stat[lbl]
        pred = analytic_ratios(s if True else 0)[lbl] if False else None
        # 用任一 s 的预测（两模式同构）
        pred = analytic_ratios(1)[lbl]
        ok = st["viol"] == 0 and set(st["numeric_patterns"].keys()) == {str(pred)}
        all_ok = all_ok and ok
        print(f"{lbl:<14}{st['n']:>6}{str(pred):>14}{st['viol']:>6}  {dict(sorted(st['numeric_patterns'].items(), key=lambda x: -x[1]))}")
    print(f"\n全部闭合（解析预测 = 数值 0 违反）: {all_ok}")
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_analytic_closure_results.json", "w", encoding="utf-8") as f:
        json.dump({"n_hard": n_hard, "n_nonzero": n_nonzero,
                   "stat": {k: {"n": v["n"], "viol": v["viol"], "patterns": v["numeric_patterns"]} for k, v in stat.items()},
                   "all_closed": all_ok}, f, ensure_ascii=False, indent=2)
    print("DONE")


if __name__ == "__main__":
    scan()
