# -*- coding: utf-8 -*-
"""n=11 M15：46 的 80000 级补因子链
- 复用 cache_n11_5seed.pkl 前 20000 → 77/331/777 续采 60000（累积 80000，保存 cache_n11_3x80000.pkl）
- 46 基座 80000 级非决定冲突对 → 区分因子候选 → 贪心补入 → 3 seed 全 0
- 输出：强闭合级最小基座（46–90 间）
"""
import json, os, pickle, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear

CACHE5 = os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl")
CACHE3 = os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl")


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
    fj = json.load(open(SCRIPT_DIR + "/paperX_n11_fill45.json", encoding="utf-8"))
    b46 = [NAMES.index(x) for x in fj["final_set"]]
    print(f"起点基座：46 因子", flush=True)

    # 采样：复用 5 seed 前 20000 + 续采 60000（保存缓存）
    if os.path.exists(CACHE3):
        with open(CACHE3, "rb") as f:
            datas = pickle.load(f)
        print("80000 缓存命中", flush=True)
    else:
        with open(CACHE5, "rb") as f:
            data5 = pickle.load(f)
        datas = {}
        for sd in ["77", "331", "777"]:
            rng = random.Random(int(sd))
            for _ in range(20000):
                gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            data = []
            for _ in range(60000):
                omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
                full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
                data.append((full, round(A_BG(n, omega, zbar), 6)))
            datas[sd] = data5[sd] + data
            print(f"seed {sd} 80000 完成 ({time.time()-t_start:.0f}s)", flush=True)
        with open(CACHE3, "wb") as f:
            pickle.dump(datas, f)
        print("80000 缓存已保存", flush=True)

    base_nd = {sd: nondet_count(datas[sd], b46) for sd in ["77", "331", "777"]}
    print(f"46 基线（80000 级）：{base_nd}", flush=True)

    # 冲突对 → 区分因子候选 → 贪心补入（3 seed 全 0 判定）
    cur = list(b46)
    while True:
        candidates = set()
        for sd in ["77", "331", "777"]:
            for (f1, a1), (f2, a2) in nondet_pairs(datas[sd], cur):
                for j in range(len(factors)):
                    if j in cur:
                        continue
                    if f1[j] != f2[j]:
                        candidates.add(j)
        if not candidates:
            print("无可补候选——停止", flush=True)
            break
        best_j, best_sum, best_nd = None, None, None
        for j in sorted(candidates - set(cur)):
            trial = cur + [j]
            nds = {sd: nondet_count(datas[sd], trial) for sd in ["77", "331", "777"]}
            s = sum(nds.values())
            if best_sum is None or s < best_sum:
                best_sum, best_j, best_nd = s, j, nds
        if best_sum == 0:
            cur = cur + [best_j]
            print(f"补入 {NAMES[best_j]} → 3 seed 全 0（规模 {len(cur)}）", flush=True)
            break
        cur = cur + [best_j]
        print(f"补入 {NAMES[best_j]} → 非决定和 {best_sum} {best_nd}（规模 {len(cur)}）", flush=True)
        if len(cur) >= 140:
            break

    final_nd = {sd: nondet_count(datas[sd], cur) for sd in ["77", "331", "777"]}
    stable = all(v == 0 for v in final_nd.values())
    print(f"最终基座 {len(cur)} 因子：非决定 {final_nd}，强闭合 = {stable}", flush=True)

    res = {"n": n, "start_size": len(b46), "final_size": len(cur),
           "added": [NAMES[i] for i in cur if i not in b46],
           "final_set": [NAMES[i] for i in cur],
           "final_nondet": {sd: int(v) for sd, v in final_nd.items()},
           "strong_closed_80000": stable,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_fill46_80000.json")
