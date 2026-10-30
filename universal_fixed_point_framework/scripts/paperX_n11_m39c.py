# -*- coding: utf-8 -*-
"""M39c：缓存全补清零 → 37 因子冲突判别
- 全补块符号强制 0（数学恒 0 修正）→ 37 因子分组
- 0 → 缓存口径 37 完备（577 纯浮点伪影确认）
- >0 → 其他因子也有近零噪声——需全面阈值化重采样
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


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    m34c = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m34c_minimal.json"), encoding="utf-8"))
    names44 = m34c["final_names"]
    fullset = set(range(n))
    fullcomp = [nm for nm in names44 if set(factors[NAMES.index(nm)][0]) | set(factors[NAMES.index(nm)][1]) == fullset]
    idx37 = [NAMES.index(x) for x in names44 if x not in fullcomp]
    fc_idx = [NAMES.index(x) for x in fullcomp]

    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        d3 = pickle.load(f)
    with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
        d5 = pickle.load(f)
    all_samples = []
    for sd in ['77', '331', '777']:
        for facs, a in d3[sd]:
            f2 = list(facs)
            for i in fc_idx:
                f2[i] = 0
            all_samples.append((tuple(f2), a))
    for sd in ['211', '555']:
        for facs, a in d5[sd]:
            f2 = list(facs)
            for i in fc_idx:
                f2[i] = 0
            all_samples.append((tuple(f2), a))

    # 37 因子（全补清零）冲突
    pat = defaultdict(list)
    for facs, a in all_samples:
        pat[tuple(facs[i] for i in idx37)].append(a)
    c = conflict_count(pat)
    print(f"37 因子（全补清零）冲突：{c}/{len(all_samples)}")

    # 对照：全 220（全补清零）冲突
    idx220 = list(range(len(factors)))
    pat2 = defaultdict(list)
    for facs, a in all_samples:
        pat2[tuple(facs[i] for i in idx220)].append(a)
    c2 = conflict_count(pat2)
    print(f"220 全因子（全补清零）冲突：{c2}")

    out = {"c37_zerofc": c, "c220_zerofc": c2}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m39c_zerofc.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m39c_zerofc.json")
