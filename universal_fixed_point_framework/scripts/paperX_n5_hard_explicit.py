# paperX_n5_hard_explicit.py
# Phase 72 阶段4：困难模式 (E6,E7) 显式判定表 + 零态机制分析
# 目标：2 个困难模式的 (sg(E6), sg(E7)) 9 组合 -> A_BG 的显式映射；分析 A_BG=0 的零态结构
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}


def all_ext_sgs(omega, zbar):
    n = len(omega)
    labels = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            labels.append((i + 1, j))
    out = []
    for a in labels:
        for b in labels:
            ia, ja = a
            ib, jb = b
            if ja <= ib or jb <= ia:
                continue
            va = sg_block(omega, zbar, tuple(range(ia - 1, ja - 1)), tuple(range(ib - 1, jb - 1)))
            out.append(((a, b), va))
    return out


def hard_table(n_target=1500, seed=251):
    """困难模式 (E6,E7) 显式判定表 + 零态结构"""
    rng = random.Random(seed)
    counts = defaultdict(int)
    combo = defaultdict(lambda: defaultdict(set))  # 模式 -> (e6,e7) -> A_BG 值集
    zero_struct = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # 模式 -> (e6,e7) -> [A=0, A!=0]
    for _ in range(400000):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        if counts[pat] >= n_target:
            continue
        counts[pat] += 1
        exts = all_ext_sgs(omega, zbar)
        e6, e7 = exts[6][1], exts[7][1]
        a = A_BG(5, omega, zbar)
        combo[pat][(e6, e7)].add(round(a, 6))
        zero_struct[pat][(e6, e7)][0 if a == 0.0 else 1] += 1
    print("困难模式 (E6,E7) 显式判定表（9 组合 -> A_BG）：")
    for pat in sorted(HARD, key=str):
        print(f"  pat={pat}")
        for e6 in (-1, 0, 1):
            row = []
            for e7 in (-1, 0, 1):
                vals = combo[pat].get((e6, e7))
                if vals is None:
                    row.append("  --  ")
                else:
                    row.append("   " + str(sorted(vals)[0]))
            print(f"    E6={e6}: {row}")
        # 零态结构
        print(f"    零态结构 (E6,E7) -> [A=0, A!=0]:")
        for k, v in sorted(zero_struct[pat].items()):
            print(f"      {k} -> zero={v[0]}, nz={v[1]}")
    # 汇总：A_BG=0 的 (E6,E7) 组合是否唯一模式
    res = {"table": {str(p): {str(k): sorted(v) for k, v in combo[p].items()} for p in HARD}}
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_hard_explicit_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n5_hard_explicit_results.json")


if __name__ == "__main__":
    hard_table()
