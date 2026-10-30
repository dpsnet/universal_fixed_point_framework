# -*- coding: utf-8 -*-
"""M34c：56 正确极小化（修正 M32 bug——逐因子立即删 + 每步验证 0 冲突）
- M32 bug：每轮收集多因子统一删——同时删破坏完备性
- 正确：逐因子试删——删除后立即验证 0 冲突——0 则永久删——多轮直到稳定
- 输出：真正保持完备性的极小集（0 冲突实测）
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

    # 基线验证 56
    c0 = conflict_count(group(all_samples, idx56))
    print(f"56 基线冲突：{c0}")
    assert c0 == 0

    # 正确极小化：逐因子立即删
    cur = list(idx56)
    t0 = time.time()
    n_round = 0
    while True:
        n_round += 1
        removed_any = False
        for i in list(cur):
            trial = [x for x in cur if x != i]
            if conflict_count(group(all_samples, trial)) == 0:
                cur = trial
                removed_any = True
        print(f"  轮 {n_round}: 当前 {len(cur)}（{time.time()-t0:.0f}s）")
        if not removed_any:
            break
    # 最终验证
    c_f = conflict_count(group(all_samples, cur))
    print(f"\n最终：{len(cur)} 因子——冲突 {c_f}（280000 实测）")
    names = [NAMES[i] for i in sorted(cur)]
    print("  名单:", names)
    removed_names = [NAMES[i] for i in sorted(set(idx56) - set(cur))]
    print(f"从 56 删除 {len(removed_names)} 个：", removed_names)

    out = {"final_size": len(cur), "final_names": names,
           "removed_from_56": removed_names, "final_conflict": c_f}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m34c_minimal.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m34c_minimal.json")
