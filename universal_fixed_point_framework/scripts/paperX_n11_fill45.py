# -*- coding: utf-8 -*-
"""n=11 M13：45+ 补因子探索（跨集稳定最小）
- 5 seed × 20000 采样（保存 pickle 缓存 cache_n11_5seed.pkl 供复用）
- seed 331 的冲突对 → 区分因子候选 → 贪心补入（5 seed 审计 0 非决定判定）
- 输出跨集稳定最小基座 + 补入因子
"""
import json, os, pickle, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear

CACHE = os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl")


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


def nondet_pairs(patterns, idx):
    """返回非决定模式内的冲突对 (full1, full2, a1, a2)"""
    pat_a = defaultdict(list)
    for full, a in patterns:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].append((full, a))
    out = []
    for v in pat_a.values():
        if len(v) > 1:
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    if v[i][1] != v[j][1]:
                        out.append((v[i], v[j]))
    return out


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    cd = json.load(open(SCRIPT_DIR + "/paperX_n11_core_descent.json", encoding="utf-8"))
    b45 = [NAMES.index(x) for x in cd["combo_min_set"]]
    seeds = [77, 211, 331, 777, 555]

    # 采样（保存缓存）
    if os.path.exists(CACHE):
        with open(CACHE, "rb") as f:
            datas = pickle.load(f)
        print("缓存命中", flush=True)
    else:
        datas = {}
        for sd in seeds:
            rng = random.Random(sd)
            data = []
            for _ in range(20000):
                omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
                full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
                data.append((full, round(A_BG(n, omega, zbar), 6)))
            datas[str(sd)] = data
            print(f"seed {sd} 采样完成 ({time.time()-t_start:.0f}s)", flush=True)
        with open(CACHE, "wb") as f:
            pickle.dump(datas, f)
        print("缓存已保存", flush=True)

    # 基线：45 在 5 seed 的非决定
    base_nd = {sd: nondet_count(datas[str(sd)], b45) for sd in seeds}
    print(f"45 基线非决定：{base_nd}", flush=True)
    fail_seed = [sd for sd, v in base_nd.items() if v > 0]
    print(f"FAIL seed：{fail_seed}", flush=True)

    # 冲突对 → 区分因子（候选）
    cur = list(b45)
    candidates = set()
    for sd in fail_seed:
        pairs = nondet_pairs(datas[str(sd)], cur)
        for (f1, a1), (f2, a2) in pairs:
            # 找区分 f1/f2 的因子（在全集投影下值不同）
            for j in range(len(factors)):
                if j in cur:
                    continue
                if f1[j] != f2[j]:
                    candidates.add(j)
    print(f"冲突对区分候选因子：{len(candidates)}", flush=True)

    # 贪心补入：每步补入后 5 seed 非决定和最小
    while True:
        best_j, best_sum, best_nd = None, None, None
        for j in sorted(candidates - set(cur)):
            trial = cur + [j]
            nds = {sd: nondet_count(datas[str(sd)], trial) for sd in seeds}
            s = sum(nds.values())
            if best_sum is None or s < best_sum:
                best_sum, best_j, best_nd = s, j, nds
        if best_j is None or best_sum == 0:
            if best_j is None:
                print("无可补候选——停止", flush=True)
            else:
                cur = cur + [best_j]
                print(f"补入 {NAMES[best_j]} → 5 seed 全 0（规模 {len(cur)}）", flush=True)
            break
        cur = cur + [best_j]
        print(f"补入 {NAMES[best_j]} → 非决定和 {best_sum} {best_nd}（规模 {len(cur)}）", flush=True)
        if len(cur) >= 140:
            break

    final_nd = {sd: nondet_count(datas[str(sd)], cur) for sd in seeds}
    print(f"最终基座 {len(cur)} 因子：非决定 {final_nd}，跨集稳定 = {all(v == 0 for v in final_nd.values())}", flush=True)

    res = {"n": n, "start_size": len(b45), "final_size": len(cur),
           "added": [NAMES[i] for i in cur if i not in b45],
           "final_set": [NAMES[i] for i in cur],
           "final_nondet": {sd: int(v) for sd, v in final_nd.items()},
           "crossset_stable": all(v == 0 for v in final_nd.values()),
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_fill45.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_fill45.json")
