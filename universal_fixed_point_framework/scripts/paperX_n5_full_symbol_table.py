# -*- coding: utf-8 -*-
"""
paperX_n5_full_symbol_table.py
困难模式下全部单对括号符号是否 100% 固定？
若成立：困难模式 = R₁ 区投影序的等价类，全符号表确定 → ratio 符号恒定性
可从符号表直接推出（"单非零项"解析证明的数学基础）。
统计：15 个单对 sg(i,j)（0-based，含 s24/s25/s35/s13/s14/s15 等非 8sg 成员）
      + 8sg + E6/E7 在困难模式样本上的取值分布。
"""
import sys
import random
from collections import Counter
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_pair, sg_block
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}


def full_table(omega, zbar):
    """全部单对 sg + 8sg + E6/E7"""
    out = {}
    for i in range(5):
        for j in range(i + 1, 5):
            out[f"s{i+1}{j+1}"] = sg_pair(omega, zbar, i, j)
    p = sg_pattern5(omega, zbar)
    for name, v in zip(["s12", "s23", "s34", "s45", "s51", "s123", "s234", "s1234"], p):
        out[name] = v
    out["E6"] = sg_block(omega, zbar, (0, 1), (0, 1, 2))
    out["E7"] = sg_block(omega, zbar, (0, 1), (0, 1, 2, 3))
    return out


def scan(n_samples=60000, seed=631):
    rng = random.Random(seed)
    counts = {}   # 名称 -> {值: 计数}
    n_hard = 0
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        n_hard += 1
        t = full_table(omega, zbar)
        for k, v in t.items():
            counts.setdefault(k, Counter())[v] += 1
    print(f"困难模式样本: {n_hard}")
    fixed, unfixed = [], []
    for k in sorted(counts):
        c = counts[k]
        if len(c) == 1:
            fixed.append((k, list(c.keys())[0]))
        else:
            unfixed.append((k, dict(c)))
    print(f"固定符号 ({len(fixed)}/{len(counts)}):")
    print("  " + ", ".join(f"{k}={v}" for k, v in sorted(fixed, key=lambda x: x[0])))
    if unfixed:
        print(f"不固定 ({len(unfixed)}):")
        for k, c in unfixed:
            print(f"  {k}: {c}")
    # 困难模式特征验证
    s_map = {k: v for k, v in fixed}
    if unfixed:
        print("\n注意：存在不固定符号，需逐项分析")
    import json
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_full_symbol_table_results.json", "w", encoding="utf-8") as f:
        json.dump({"n_hard": n_hard, "fixed": dict(fixed), "unfixed": unfixed}, f, ensure_ascii=False, indent=2)
    print("DONE")


if __name__ == "__main__":
    scan()
