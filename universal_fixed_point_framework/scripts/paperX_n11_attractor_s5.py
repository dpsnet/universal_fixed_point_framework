# -*- coding: utf-8 -*-
"""n=11 M10：吸引子收敛性验证 + S5 必要性
- seed 555：采样 80000（前 20000 构建 140 内部删除链；全 80000 测 90(131)/95 非决定）
- seed 777/999：各采样 20000 → 构建链 + 自身缓存测 90(131)/95
- 收敛性：新链 0 非决定最小规模构成 vs 90/95
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


def nondet_count(patterns, idx):
    pat_a = defaultdict(set)
    for full, a in patterns:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return sum(1 for v in pat_a.values() if len(v) > 1)


def build_chain_from_data(data, start_idx):
    chain = [list(start_idx)]
    cur = list(start_idx)
    while True:
        changed = False
        for i in range(len(cur)):
            trial = cur[:i] + cur[i + 1:]
            if nondet_count(data, trial) == 0:
                cur = trial
                chain.append(list(cur))
                changed = True
                break
        if not changed:
            break
    return chain


def sample(n, factors, seed, cap):
    rng = random.Random(seed)
    data = []
    for _ in range(cap):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        data.append((full, round(A_BG(n, omega, zbar), 6)))
    return data


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    ac = json.load(open(SCRIPT_DIR + "/paperX_n11_approx_closed.json", encoding="utf-8"))
    cg = json.load(open(SCRIPT_DIR + "/paperX_n11_crossset_greedy.json", encoding="utf-8"))
    start_names = cg["remove_set"] + ac["extra_set"]
    start_idx = [NAMES.index(x) for x in start_names]

    bw = json.load(open(SCRIPT_DIR + "/paperX_n11_basis_weights.json", encoding="utf-8"))
    b90 = [NAMES.index(x) for x in bw["b90"]]
    b95 = [NAMES.index(x) for x in bw["b95"]["77"]]  # 3 链相同构成

    # seed 555：80000 采样（前 20000 构建链；全量测 90/95）
    data555 = sample(n, factors, 555, 80000)
    print(f"seed 555: 80000 采样 ({time.time()-t_start:.0f}s)", flush=True)
    ch555 = build_chain_from_data(data555[:20000], start_idx)
    # 新链 0 非决定最小规模（自身 20000 缓存级）
    min_sz = len(ch555[-1])
    print(f"seed 555 链: 缓存级最小 {min_sz}", flush=True)
    # 90/95 在 555 全 80000 缓存
    nd90_555 = nondet_count(data555, b90)
    nd95_555 = nondet_count(data555, b95)
    print(f"seed 555 @80000: 90 非决定 {nd90_555} | 95 非决定 {nd95_555}", flush=True)

    # seed 777/999：各 20000
    res_new = {"555": {"cache_min": min_sz, "nd90_80000": nd90_555, "nd95_80000": nd95_555}}
    for sd in [777, 999]:
        data = sample(n, factors, sd, 20000)
        ch = build_chain_from_data(data, start_idx)
        min_sz = len(ch[-1])
        nd90 = nondet_count(data, b90)
        nd95 = nondet_count(data, b95)
        res_new[str(sd)] = {"cache_min": min_sz, "nd90_20000": nd90, "nd95_20000": nd95}
        print(f"seed {sd}: 缓存级最小 {min_sz} | 90 非决定 {nd90} | 95 非决定 {nd95} ({time.time()-t_start:.0f}s)", flush=True)

    res = {"n": n, "start_size": len(start_idx),
           "b90_size": len(b90), "b95_size": len(b95),
           "chains": res_new,
           "converged_95": all(res_new[s]["cache_min"] >= len(b95) for s in res_new),
           "s5_needed_80000": nd90_555 > 0,
           "s5_needed_20000_any": any(res_new[str(s)]["nd90_20000"] > 0 for s in [777, 999]),
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_attractor_s5.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_attractor_s5.json")
