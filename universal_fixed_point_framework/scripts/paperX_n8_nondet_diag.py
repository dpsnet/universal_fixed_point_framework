# -*- coding: utf-8 -*-
"""n=8 非决定性模式诊断：20 因子基座在 40000 主样本上的 6 个非决定性模式，
找全集 84 因子中能区分 A_BG 的最小补因子集（用于扩基座）。
"""
import json, os, random, sys
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n8_criterion import adj_partition_factors, sg_pattern8
from paperX_n8_minbasis import factor_name

N8 = 8


def load_basis():
    with open(os.path.join(SCRIPT_DIR, "paperX_n8_minbasis_results.json"), encoding="utf-8") as f:
        res = json.load(f)
    factors = adj_partition_factors(N8)
    names = [factor_name(a, b) for a, b in factors]
    basis_names = res["remove_set"]
    idx = [names.index(x) for x in basis_names]
    return factors, idx, names, basis_names


def main():
    factors, idx, names, basis_names = load_basis()
    rng = random.Random(101)
    pat_a = defaultdict(set)
    pat_full = defaultdict(set)  # 模式键 -> 全部 84 因子值集合
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(N8, 0, r1=True, momentum=True, rng=rng)
        full = sg_pattern8(omega, zbar, factors)
        key = tuple(full[i] for i in idx)
        pat_a[key].add(round(A_BG(N8, omega, zbar), 6))
        pat_full[key].add(full)
    nondet = [p for p in pat_a if len(pat_a[p]) > 1]
    print(f"非决定性模式数: {len(nondet)}")
    for p in nondet:
        vals = sorted(pat_a[p])
        print(f"\n模式键: {[names[i] + '=' + str(v) for i, v in zip(idx, p)]}")
        print(f"  A_BG 取值: {vals}")
        # 对每个样本的 full 因子，找区分因子
        fulls = list(pat_full[p])
        # 区分因子：在所有 fulls 中与 A_BG 值共变（每个因子值确定 A_BG）
        cand = []
        for fi, fname in enumerate(names):
            if fi in idx:
                continue
            fv_a = defaultdict(set)
            for full in fulls:
                # full 对应一个 A_BG（pat_a[p] 集合：可能多个值）
                pass
        # 更直接：重新采样这些模式，记录每个补因子值与 A_BG
        rng2 = random.Random(101)
        collected = []
        for _ in range(40000):
            omega, zbar, _ = gen_partial_collinear(N8, 0, r1=True, momentum=True, rng=rng2)
            full = sg_pattern8(omega, zbar, factors)
            key = tuple(full[i] for i in idx)
            if key == p:
                collected.append((full, round(A_BG(N8, omega, zbar), 6)))
        print(f"  该模式出现 {len(collected)} 次")
        # 补因子区分能力
        res_d = []
        for fi, fname in enumerate(names):
            if fi in idx:
                continue
            fv_a = defaultdict(set)
            for full, a in collected:
                fv_a[full[fi]].add(a)
            if all(len(v) == 1 for v in fv_a.values()) and len(fv_a) > 1:
                res_d.append(fname)
        print(f"  可区分补因子: {res_d}")
        # 最小补集（贪心）：逐个加，直到决定性
        chosen = []
        remaining = res_d[:]
        while remaining and len({tuple(full[names.index(c)] for c in chosen) for full, a in collected} | set()) >= 0:
            # 检查当前 chosen 是否决定性
            ca = defaultdict(set)
            for full, a in collected:
                ca[tuple(full[names.index(c)] for c in chosen)].add(a)
            if all(len(v) == 1 for v in ca.values()):
                break
            # 选减少非决定最多的
            best = None
            best_n = -1
            for c in remaining:
                ca2 = defaultdict(set)
                for full, a in collected:
                    ca2[tuple(full[names.index(c2)] for c2 in chosen + [c])].add(a)
                n_nondet = sum(1 for v in ca2.values() if len(v) > 1)
                if best is None or n_nondet < best_n:
                    best_n = n_nondet
                    best = c
            chosen.append(best)
            remaining.remove(best)
        print(f"  最小补因子（贪心）: {chosen}")


if __name__ == "__main__":
    main()
