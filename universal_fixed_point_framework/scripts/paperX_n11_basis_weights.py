# -*- coding: utf-8 -*-
"""n=11 M9：构成差异拆解（90 幸运 vs 95 稳健）
- seed 131 链取 90 规模点构成（M7 幸运）
- seed 77/211/331 链取各 95 规模点构成（M8 稳健）
- 集合运算：核心（90 ∩ 3×95）/ 鲁棒冗余（95 独有）/ 脆弱（90 独有）
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


def build_chain_140(n, factors, start_idx, seed, cap, target_size=None):
    """构建删除链；返回链（列表）与缓存数据"""
    rng = random.Random(seed)
    data = []
    for _ in range(cap):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        data.append((full, round(A_BG(n, omega, zbar), 6)))
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
    return data, chain


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    ac = json.load(open(SCRIPT_DIR + "/paperX_n11_approx_closed.json", encoding="utf-8"))
    cg = json.load(open(SCRIPT_DIR + "/paperX_n11_crossset_greedy.json", encoding="utf-8"))
    start_names = cg["remove_set"] + ac["extra_set"]
    start_idx = [NAMES.index(x) for x in start_names]

    # seed 131 → 90 构成（M7 幸运）
    _, ch131 = build_chain_140(n, factors, start_idx, 131, 20000)
    b90 = None
    for c in ch131:
        if len(c) == 90:
            b90 = c
            break
    assert b90 is not None, "seed131 链无 90 规模点"
    print(f"seed 131: 90 构成获取（{time.time()-t_start:.0f}s）", flush=True)

    # seed 77/211/331 → 各 95 构成（M8 稳健）
    b95s = {}
    for sd in [77, 211, 331]:
        _, ch = build_chain_140(n, factors, start_idx, sd, 20000)
        b95 = None
        for c in ch:
            if len(c) == 95:
                b95 = c
                break
        assert b95 is not None, f"seed {sd} 链无 95 规模点"
        b95s[sd] = b95
        print(f"seed {sd}: 95 构成获取（{time.time()-t_start:.0f}s）", flush=True)

    s90 = set(b90)
    s95_0, s95_1, s95_2 = (set(v) for v in b95s.values())
    core = s90 & s95_0 & s95_1 & s95_2            # 4 基座共有
    core_3 = (s95_0 & s95_1 & s95_2) - core        # 3 个 95 共有但 90 无
    robust_only = (s95_0 | s95_1 | s95_2) - s90   # 95 独有（任一）
    fragile_only = s90 - (s95_0 | s95_1 | s95_2)  # 90 独有
    print(f"核心（90∩3×95）: {len(core)}", flush=True)
    print(f"95 共有非核心: {len(core_3)}", flush=True)
    print(f"95 独有: {len(robust_only)}", flush=True)
    print(f"90 独有（脆弱）: {len(fragile_only)}", flush=True)

    res = {"n": n, "start_size": len(start_idx),
           "b90": [NAMES[i] for i in b90],
           "b95": {str(sd): [NAMES[i] for i in v] for sd, v in b95s.items()},
           "core": [NAMES[i] for i in sorted(core)],
           "core_3_95": [NAMES[i] for i in sorted(core_3)],
           "robust_only_95": [NAMES[i] for i in sorted(robust_only)],
           "fragile_only_90": [NAMES[i] for i in sorted(fragile_only)],
           "counts": {"core": len(core), "core_3_95": len(core_3),
                      "robust_only_95": len(robust_only), "fragile_only_90": len(fragile_only)},
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_basis_weights.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_basis_weights.json")
