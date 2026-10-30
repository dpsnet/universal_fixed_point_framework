# -*- coding: utf-8 -*-
"""M41：n=10 全补污染检查（跨 n 评估）
- n=10 全补块（a∪b = 全 10）识别——165 全因子 + M36 极小名单（49）
- 缓存删除全补 → 冲突（污染判别）
"""
import os, sys, json, pickle
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
    n = 10
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    fullset = set(range(n))

    # 165 全因子中全补块
    all_fc = []
    for a, b in factors:
        if set(a) | set(b) == fullset:
            all_fc.append(factor_name(a, b))
    print(f"n=10 全因子 {len(factors)} 中全补块：{len(all_fc)} -> {all_fc}")

    # M36 极小名单（49）中全补
    m36 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n10_m36_spectral.json"), encoding="utf-8"))
    names49 = m36["final_names"]
    fc_in = [nm for nm in names49 if nm in all_fc]
    print(f"M36 极小名单 {len(names49)} 中全补块：{len(fc_in)} -> {fc_in}")

    # 缓存删除全补 → 冲突
    with open(os.path.join(SCRIPT_DIR, "cache_n10_3x80000.pkl"), "rb") as f:
        d = pickle.load(f)
    all_samples = []
    for sd in d:
        all_samples.extend(d[sd])
    idx49 = [NAMES.index(x) for x in names49]
    fc_idx = [NAMES.index(x) for x in fc_in]
    idx37 = [i for i in idx49 if i not in set(fc_idx)]

    # 全补清零 + 删除
    all_s2 = []
    for facs, a in all_samples:
        f2 = list(facs)
        for i in fc_idx:
            f2[i] = 0
        all_s2.append((tuple(f2), a))

    c49 = conflict_count(group(all_samples, idx49))
    c49_zerofc = conflict_count(group(all_s2, idx49))
    c37 = conflict_count(group(all_s2, idx37))
    print(f"49 因子冲突：{c49}")
    print(f"49 因子（全补清零）冲突：{c49_zerofc}")
    print(f"37 因子（删全补+清零）冲突：{c37}")

    out = {"n": n, "full_fc": len(all_fc), "in_49": fc_in,
           "c49": c49, "c49_zerofc": c49_zerofc, "c37": c37}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_m41_fullcomp.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n10_m41_fullcomp.json")
