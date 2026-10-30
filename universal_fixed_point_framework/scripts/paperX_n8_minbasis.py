# -*- coding: utf-8 -*-
"""n=8 最小充分基座搜索（缓存加速版，参照 paperX_n7_minbasis.py）：
1. 一次采样缓存 (84 相邻分割因子, A_BG)（20000 样本）
2. 子集充分性 = 缓存上模式键 → A_BG 全单值
3. 贪心删除 + 独立样本复核
目的：量化"判据阶数随 n 增长"——n=5 需 8+2、n=6 需 12、n=7 需 16、n=8 需 ?
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_pair, sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n8_criterion import adj_partition_factors, sg_pattern8


def factor_name(a, b):
    """0-based 块对 → 1-based 名称，如 (0,) vs (1,2) → s1_23"""
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def cache_samples(n=20000, seed=41, n_particles=8):
    rng = random.Random(seed)
    factors = adj_partition_factors(n_particles)
    data = []
    t0 = time.time()
    for _ in range(n):
        omega, zbar, _ = gen_partial_collinear(n_particles, 0, r1=True, momentum=True, rng=rng)
        data.append((sg_pattern8(omega, zbar, factors), round(A_BG(n_particles, omega, zbar), 6)))
    print(f"缓存 {n} 样本 ({time.time()-t0:.0f}s)")
    return factors, data


def sufficient_on(data, idx):
    pat_a = defaultdict(set)
    for full, a in data:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return all(len(v) == 1 for v in pat_a.values())


def nondet_count_on(data, idx, sample=None):
    pat_a = defaultdict(set)
    src = data if sample is None else data[:sample]
    for full, a in src:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return sum(1 for v in pat_a.values() if len(v) > 1)


if __name__ == "__main__":
    factors, data = cache_samples(30000, 41)
    _, data_i = cache_samples(8000, 97)  # 实时独立抽查集
    _, data_v = cache_samples(10000, 53)  # 最终独立复核
    NAMES = [factor_name(a, b) for a, b in factors]
    full_idx = list(range(len(factors)))
    print(f"因子数 {len(full_idx)}  全集充分: {sufficient_on(data, full_idx)}  非决定性: {nondet_count_on(data, full_idx)}")

    # 贪心删除（每步双检查：缓存 + 独立抽查）
    cur = list(full_idx)
    changed = True
    passes = 0
    while changed:
        changed = False
        passes += 1
        for i in range(len(cur)):
            trial = cur[:i] + cur[i + 1:]
            if sufficient_on(data, trial) and sufficient_on(data_i, trial):
                cur = trial
                changed = True
                print(f"  删除 {len(full_idx)-len(cur)} 个 (pass {passes})")
                break
    print(f"贪心删除最小集 ({len(cur)}/{len(full_idx)}): {[NAMES[i] for i in cur]}")

    # 独立样本复核
    ok2 = sufficient_on(data_v, cur)
    print(f"独立 10000 复核: {ok2}  非决定性: {nondet_count_on(data_v, cur)}")

    res = {"remove_set": [NAMES[i] for i in cur], "remove_size": len(cur),
           "verify_independent": ok2, "factors_total": len(full_idx)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n8_minbasis_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
