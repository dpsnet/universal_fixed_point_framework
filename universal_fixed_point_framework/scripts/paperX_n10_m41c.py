# -*- coding: utf-8 -*-
"""M41c：n=10 全空间 165 删全补完备性验证（缓存——快）
- 165 全因子删 9 全补 → 156 因子冲突（应为 0——与 n=6/n=11 一致）
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
    fc_idx = [i for i, (a, b) in enumerate(factors) if set(a) | set(b) == fullset]
    print(f"n=10 全补块 {len(fc_idx)} 个")

    with open(os.path.join(SCRIPT_DIR, "cache_n10_3x80000.pkl"), "rb") as f:
        d = pickle.load(f)
    all_samples = []
    for sd in d:
        all_samples.extend(d[sd])
    print(f"样本 {len(all_samples)}")

    full = list(range(len(factors)))
    c165 = conflict_count(group(all_samples, full))
    print(f"165 全因子冲突：{c165}")

    idx156 = [i for i in full if i not in set(fc_idx)]
    # 删全补：全补列不参与分组
    c156 = conflict_count(group(all_samples, idx156))
    print(f"156 因子（删 9 全补）冲突：{c156}")

    out = {"n": n, "full_fc": len(fc_idx), "c165": c165, "c156": c156}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_m41c_fullspace.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n10_m41c_fullspace.json")
