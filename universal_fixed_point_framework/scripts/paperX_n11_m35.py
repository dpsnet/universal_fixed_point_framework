# -*- coding: utf-8 -*-
"""M35：44 全局最小性——多轮随机删序贪心
- M34c 是固定顺序扫描删（贪心局部极小）——换删序可能更小
- 10 轮：每轮随机洗牌因子顺序 → 逐因子试删（立即验证 0 冲突）→ 终局大小
- 若全停 44 → 强极小；若某轮 <44 → 新下界
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
    m34c = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m34c_minimal.json"), encoding="utf-8"))
    idx44 = [NAMES.index(x) for x in m34c["final_names"]]
    print(f"起点：44 因子")

    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        d3 = pickle.load(f)
    with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
        d5 = pickle.load(f)
    all_samples = []
    for sd in ['77', '331', '777']:
        all_samples.extend(d3[sd])
    for sd in ['211', '555']:
        all_samples.extend(d5[sd])
    print(f"样本 {len(all_samples)}")

    random.seed(20261006)
    N_ROUNDS = 10
    sizes = []
    best = (len(idx44), None)
    t0 = time.time()
    for r in range(N_ROUNDS):
        cur = list(idx44)
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
    print(f"\n分布：{sorted(set(sizes))} 出现次数 {[sizes.count(k) for k in sorted(set(sizes))]}")
    print(f"最小：{best[0]}")

    out = {"rounds_sizes": sizes, "min_size": best[0],
           "min_names": sorted([NAMES[i] for i in best[1]]) if best[1] else None}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m35_global_min.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m35_global_min.json")
