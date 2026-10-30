# -*- coding: utf-8 -*-
"""M32：56 全局最小性下探（对 56 整体贪心删减——含 50 基座内因子）
- 56 = basis50 + M31 added——280000 上 0 冲突
- 逐因子试删（280000 上仍 0 冲突则删）——多轮——直到稳定
- 预期：左端冗余因子（s1_* 等）被删——更小完备集
"""
import os, json, pickle, sys, time
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
    print(f"56 基座 {len(idx56)} 因子")

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

    cur = list(idx56)
    t0 = time.time()
    n_round = 0
    while True:
        n_round += 1
        removed = []
        for i in cur:
            trial = [x for x in cur if x != i]
            if conflict_count(group(all_samples, trial)) == 0:
                removed.append(i)
        for i in removed:
            cur.remove(i)
        print(f"  轮 {n_round}: 删除 {len(removed)}（{','.join(NAMES[i] for i in removed)[:60]}...）——当前 {len(cur)}（{time.time()-t0:.0f}s）")
        if not removed:
            break
    print(f"\n最终：{len(cur)} 因子（280000 上 0 冲突）")
    names = [NAMES[i] for i in sorted(cur)]
    print("  名单:", names)

    # 对照：删掉的（56 - 最终）
    removed_names = [NAMES[i] for i in set(idx56) - set(cur)]
    print(f"删掉 {len(removed_names)} 个：", removed_names)

    out = {"final_size": len(cur), "final_names": names,
           "removed_from_56": removed_names}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m32_minimal2.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m32_minimal2.json")
