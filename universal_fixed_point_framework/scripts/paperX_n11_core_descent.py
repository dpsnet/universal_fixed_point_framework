# -*- coding: utf-8 -*-
"""n=11 M11：90 核心下探（双 80000 缓存逐因子必要性 + 组合删除）
- 采样 80000（seed 131/555）
- 90 中每因子删除 → 两缓存非决定（都 0 才可删）
- 可删集贪心组合删除 → 最小强闭合基座
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
    bw = json.load(open(SCRIPT_DIR + "/paperX_n11_basis_weights.json", encoding="utf-8"))
    b90 = [NAMES.index(x) for x in bw["b90"]]
    print(f"起点：90 核心完备基座", flush=True)

    # 双 80000 缓存（seed 131/555）
    d131 = sample(n, factors, 131, 80000)
    print(f"seed 131: 80000 采样 ({time.time()-t_start:.0f}s)", flush=True)
    d555 = sample(n, factors, 555, 80000)
    print(f"seed 555: 80000 采样 ({time.time()-t_start:.0f}s)", flush=True)

    # 逐一删除验证
    removable = []
    necessary = []
    for i, fi in enumerate(b90):
        trial = [x for x in b90 if x != fi]
        nd1 = nondet_count(d131, trial)
        nd5 = nondet_count(d555, trial)
        if nd1 == 0 and nd5 == 0:
            removable.append(fi)
        else:
            necessary.append(fi)
        if (i + 1) % 15 == 0:
            print(f"  逐因子 {i+1}/90: 可删 {len(removable)} 必要 {len(necessary)} ({time.time()-t_start:.0f}s)", flush=True)
    print(f"单因子测试：可删 {len(removable)} / 必要 {len(necessary)}", flush=True)

    # 可删集贪心组合删除（迭代：删除后重新验证）
    cur = list(b90)
    removed_comb = []
    changed = True
    while changed:
        changed = False
        # 遍历当前基座中每个因子尝试删
        for i in range(len(cur)):
            trial = cur[:i] + cur[i + 1:]
            if nondet_count(d131, trial) == 0 and nondet_count(d555, trial) == 0:
                cur = trial
                removed_comb.append(i)
                changed = True
                break
        if changed:
            print(f"  组合删除 {len(b90)-len(cur)} 个 → 当前 {len(cur)} 因子", flush=True)
    print(f"组合删除后最小强闭合基座：{len(cur)} 因子", flush=True)

    res = {"n": n, "b90_size": len(b90), "seeds": [131, 555], "samples": 80000,
           "single_removable": [NAMES[i] for i in removable],
           "single_necessary": [NAMES[i] for i in necessary],
           "single_removable_count": len(removable),
           "single_necessary_count": len(necessary),
           "combo_min_size": len(cur),
           "combo_min_set": [NAMES[i] for i in cur],
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_core_descent.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_core_descent.json")
