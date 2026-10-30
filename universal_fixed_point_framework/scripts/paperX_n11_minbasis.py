# -*- coding: utf-8 -*-
"""n=11 外推探索（阶段 1：全集决定性 + 贪心基座 + 独立复核）：
- 验证盲区尺度递减律延续：n=8 大块前缀 → n=9 中段合并 → n=10 单粒子对（s2_3/s3_4）→ n=11 ?
- 全集 220 因子（n=10 165 → +55）
- 采样缓存 15000 + 抽查 5000（双检查贪心删除）+ 独立复核 8000
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear


def adj_partition_factors(n):
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                names.append((a, b))
    return names


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def sg_pattern(omega, zbar, factors):
    return tuple(sg_block(omega, zbar, a, b) for a, b in factors)


def cache_samples(n_samples, seed, n_particles=11):
    rng = random.Random(seed)
    factors = adj_partition_factors(n_particles)
    data = []
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n_particles, 0, r1=True, momentum=True, rng=rng)
        data.append((sg_pattern(omega, zbar, factors), round(A_BG(n_particles, omega, zbar), 6)))
    print(f"  采样 {n_samples} ({time.time()-t0:.0f}s)", flush=True)
    return data


def sufficient_on(data, idx):
    pat_a = defaultdict(set)
    for full, a in data:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return all(len(v) == 1 for v in pat_a.values())


def nondet_count_on(data, idx):
    pat_a = defaultdict(set)
    for full, a in data:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return sum(1 for v in pat_a.values() if len(v) > 1)


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    print(f"n={n} 全集因子数: {len(factors)}", flush=True)

    data = cache_samples(15000, 41)
    data_i = cache_samples(5000, 97)
    data_v = cache_samples(8000, 53)

    full_idx = list(range(len(factors)))
    print(f"全集充分: {sufficient_on(data, full_idx)}  非决定性: {nondet_count_on(data, full_idx)}", flush=True)

    # 贪心删除（双检查）
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
                print(f"  删除 {len(full_idx)-len(cur)} 个 (pass {passes}, {time.time()-t_start:.0f}s)", flush=True)
                break
    print(f"贪心删除最小集 ({len(cur)}/{len(full_idx)}): {[NAMES[i] for i in cur]}", flush=True)

    ok2 = sufficient_on(data_v, cur)
    print(f"独立 8000 复核: {ok2}  非决定性: {nondet_count_on(data_v, cur)}", flush=True)

    head = [NAMES[i] for i in cur if "s1_" in NAMES[i]]
    tail = [NAMES[i] for i in cur if "s1_" not in NAMES[i]]
    print(f"头部因子(含粒子1) {len(head)}: {head}", flush=True)
    print(f"尾部因子(无粒子1) {len(tail)}: {tail}", flush=True)

    # 递减律对照：n=11 是否出现单粒子对（s2_3/s3_4 类推 = 中间相邻单粒子对）
    single_pairs = [x for x in [NAMES[i] for i in cur] if len(x) == 5 and x[0] == 's' and x[1].isdigit() and x[3] == '_' and x[2].isdigit() and x[4].isdigit()]
    print(f"单粒子对因子: {single_pairs}", flush=True)

    res = {"n": n, "factors_total": len(full_idx), "remove_set": [NAMES[i] for i in cur],
           "remove_size": len(cur), "verify_independent": ok2,
           "head_count": len(head), "tail_count": len(tail),
           "head_set": head, "tail_set": tail, "single_pairs": single_pairs,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_minbasis_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n11_minbasis_results.json")
