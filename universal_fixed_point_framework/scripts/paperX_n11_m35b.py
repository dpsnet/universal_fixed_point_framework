# -*- coding: utf-8 -*-
"""M35b：56 起点随机删序（多路径全局性——不同起点/顺序可能到达不同极小）
- 3 轮：洗牌 56 → 逐因子试删（立即验证 0 冲突）→ 终局
- 若终局 <44 → 新下界；若 =44 → 44 跨起点稳健
"""
import os, json, pickle, sys, random, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len({sg(v) for v in vals}) > 1)


def group(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return pat


if __name__ == "__main__":
    factors = adj_partition_factors(11)
    NAMES = [factor_name(a, b) for a, b in factors]
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [NAMES.index(x) for x in basis50]
    m31 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m31_cross_seed.json"), encoding="utf-8"))
    idx56 = idx50 + [NAMES.index(x) for x in m31["added"]]
    print(f"起点：56 因子")

    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        d3 = pickle.load(f)
    with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
        d5 = pickle.load(f)
    all_samples = []
    for sd in ['77', '331', '777']:
        all_samples.extend(d3[sd])
    for sd in ['211', '555']:
        all_samples.extend(d5[sd])

    random.seed(20261006)
    N_ROUNDS = 3
    sizes = []
    best = (len(idx56), None)
    t0 = time.time()
    for r in range(N_ROUNDS):
        cur = list(idx56)
        random.shuffle(cur)
        while True:
            removed_any = False
            for i in list(cur):
                trial = [x for x in cur if x != i]
                if conflict_count(group(all_samples, trial)) == 0:
                    cur = trial
                    removed_any = True
            if not removed_any:
                break
        sizes.append(len(cur))
        if len(cur) < best[0]:
            best = (len(cur), list(cur))
        print(f"  轮 {r+1}: 终局 {len(cur)}（{time.time()-t0:.0f}s）")
    print(f"\n终局分布：{sizes}——最小 {best[0]}")

    out = {"rounds_sizes": sizes, "min_size": best[0],
           "min_names": sorted([NAMES[i] for i in best[1]]) if best[1] else None}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m35b_56path.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m35b_56path.json")
