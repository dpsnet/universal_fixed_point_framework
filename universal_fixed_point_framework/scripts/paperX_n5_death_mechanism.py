# -*- coding: utf-8 -*-
"""
paperX_n5_death_mechanism.py
死亡机制的解析结构验证：
1. PT̂=0 型分割：PT̂ = ∏sg(d)·(∏theta − ∏theta')，PT̂=0 ⟺ 非全 ratio 同号。
   验证每分割在困难模式内的 ratio 符号模式（是否固定/异号位置固定）
2. [123]|[4] 的 Ā_{123}=0：3 元素预振幅 = −V₃ 单块，V 的哪个 theta 恒死？
3. 输出每分割 ratio 符号模式 → 解析论证素材
"""
import sys
import itertools
import random
import json
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_bg_recursion import bracket, compositions, split_into_blocks
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5
from paperX_single_minus_numerics import sg_block

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}


def bs(A, B, omega, zbar):
    A = tuple(a - 1 for a in A); B = tuple(b - 1 for b in B)
    return sg_block(omega, zbar, A, B)


def ratios_of(blocks, omega, zbar):
    """每相邻对 k 的 (num_k, d_k, ratio 符号, num符号, d符号)"""
    out = []
    A_ = len(blocks)
    for k in range(A_ - 1):
        Sk = blocks[k]; Sk1 = blocks[k + 1]
        d = bracket(Sk, Sk1, omega, zbar)
        K1 = tuple(itertools.chain.from_iterable(blocks[:k + 1]))
        K2 = tuple(itertools.chain.from_iterable(blocks[k + 1:]))
        num = bracket(K1, K2, omega, zbar)
        rsgn = (num > 0) - (num < 0) if num != 0 else 0
        dsgn = (d > 0) - (d < 0) if d != 0 else 0
        ratio_sgn = rsgn * dsgn if dsgn != 0 else 0  # sgn(num/d) = sgn(num)·sgn(d)
        out.append({"num": round(num, 6), "d": round(d, 6),
                    "num_sgn": rsgn, "d_sgn": dsgn, "ratio_sgn": ratio_sgn})
    return out


def death_mechanism(n_samples=60000, seed=523):
    rng = random.Random(seed)
    # 分割集合（n=5, elems=(1,2,3,4)）
    elems = tuple(range(1, 5))
    splits = {}
    for cuts in compositions(4, min_parts=1):
        blocks = split_into_blocks(elems, cuts)
        splits["|".join("".join(str(x) for x in b) for b in blocks)] = blocks
    stat = {lbl: {"count": 0, "ratio_patterns": {}} for lbl in splits}
    n_nonzero = 0
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        e6 = bs((1, 2), (1, 2, 3), omega, zbar)
        e7 = bs((1, 2), (1, 2, 3, 4), omega, zbar)
        if not (e6 == e7 and e6 != 0):
            continue
        n_nonzero += 1
        for lbl, blocks in splits.items():
            if len(blocks) == 1:
                continue  # 1 块 PT̂=0 平凡
            r = ratios_of(blocks, omega, zbar)
            key = tuple(x["ratio_sgn"] for x in r)
            stat[lbl]["count"] += 1
            stat[lbl]["ratio_patterns"][str(key)] = stat[lbl]["ratio_patterns"].get(str(key), 0) + 1
    print(f"非零样本: {n_nonzero}")
    for lbl in sorted(splits):
        if len(splits[lbl]) == 1:
            print(f"{lbl:<22}（1块，PT̂=0 平凡）")
            continue
        s = stat[lbl]
        print(f"{lbl:<22} n={s['count']}   ratio符号模式: {dict(sorted(s['ratio_patterns'].items(), key=lambda x: -x[1]))}")
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_death_mechanism_results.json", "w", encoding="utf-8") as f:
        json.dump({lbl: {"count": stat[lbl]["count"], "patterns": stat[lbl]["ratio_patterns"]}
                   for lbl in splits if len(splits[lbl]) > 1}, f, ensure_ascii=False, indent=2)
    print("DONE")


if __name__ == "__main__":
    death_mechanism()
