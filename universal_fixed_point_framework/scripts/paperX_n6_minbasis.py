# -*- coding: utf-8 -*-
"""n=6 最小基座搜索 v2（缓存加速版）：
1. 一次采样缓存 (20 因子, A_BG)（40000 样本）
2. 子集充分性 = 缓存上模式键 → A_BG 全单值（无需重跑 BG）
3. 贪心删除 + 贪心添加交叉验证
"""
import json, os, random, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_pair, sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_fullbasis import sg_pattern6_full

NAMES = ["s1_23","s12_3","s123_4","s56","s23","s1_234","s12_34","s34",
         "s2_34","s23_4","s12","s345_6","s45_6","s45","s3_45","s34_5",
         "s234_5","s61","s2_345","s23_45"]

def cache_samples(n=40000, seed=31):
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        data.append((sg_pattern6_full(omega, zbar), round(A_BG(6, omega, zbar), 6)))
    return data

def sufficient_on(data, idx):
    pat_a = defaultdict(set)
    for full, a in data:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return all(len(v) == 1 for v in pat_a.values())

def nondet_count_on(data, idx, sample=None):
    """子集下非决定性模式数（可抽样加速）"""
    pat_a = defaultdict(set)
    src = data if sample is None else data[:sample]
    for full, a in src:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return sum(1 for v in pat_a.values() if len(v) > 1)

if __name__ == "__main__":
    print("缓存采样 40000 ...")
    data = cache_samples(40000)
    # 全集充分性确认
    full_idx = list(range(20))
    print(f"全集 20 因子充分: {sufficient_on(data, full_idx)}  非决定性: {nondet_count_on(data, full_idx)}")

    # 贪心删除
    cur = list(full_idx)
    changed = True
    while changed:
        changed = False
        for i in range(len(cur)):
            trial = cur[:i] + cur[i+1:]
            if sufficient_on(data, trial):
                cur = trial
                changed = True
                break
    print(f"贪心删除最小集 ({len(cur)}/20): {[NAMES[i] for i in cur]}")
    print(f"复核(独立 20000): {sufficient_on(cache_samples(20000, 77), cur)}")

    # 贪心添加（交叉验证）：每次加入使非决定性减少最多的因子
    add = []
    while len(add) < 20:
        best = None
        best_nd = None
        cur_nd = nondet_count_on(data, add, 20000) if add else float("inf")
        for j in range(20):
            if j in add:
                continue
            nd = nondet_count_on(data, add + [j], 20000)
            if best_nd is None or nd < best_nd:
                best_nd = nd
                best = j
        if best is None or best_nd == 0:
            break
        add.append(best)
        print(f"  +{NAMES[best]} -> 非决定性 {best_nd} (集大小 {len(add)})")
    print(f"贪心添加最小集 ({len(add)}/20): {[NAMES[i] for i in add]}")
    print(f"复核(独立 20000): {sufficient_on(cache_samples(20000, 77), add)}")

    res = {"remove_set": [NAMES[i] for i in cur], "remove_size": len(cur),
           "add_set": [NAMES[i] for i in add], "add_size": len(add)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_minbasis_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
