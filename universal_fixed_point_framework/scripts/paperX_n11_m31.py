# -*- coding: utf-8 -*-
"""M31：跨 8 seed 完备集（280000 样本合并口径）
- 合并：3x80000（77/331/777 × 80000）+ 5seed（211/555 × 20000）= 280000
- 定向补集（50 冲突组区分因子）+ 贪心删 → 跨 seed 完备集
- 交叉验证：3seed 子集 / 5seed 子集 / 全 280000 均 0 冲突
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


def conflict_count(pats, key=None):
    if key is None:
        key = lambda v: v
    return sum(1 for vals in pats.values() if len({sg(key(v)) for v in vals}) > 1)


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

    c1 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        d3 = pickle.load(f)
    with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
        d5 = pickle.load(f)

    # 合并：3x80000 的 77/331/777 + 5seed 的 211/555（新 seed）
    all_samples = []
    for sd in ['77', '331', '777']:
        all_samples.extend(d3[sd])
    for sd in ['211', '555']:
        all_samples.extend(d5[sd])
    print(f"合并样本：{len(all_samples)}（3seed 240000 + 211/555 40000）")

    # 50 基座冲突（280000）——保留样本（facs, a）
    pat50_raw = defaultdict(list)
    for facs, a in all_samples:
        pat50_raw[tuple(facs[i] for i in idx50)].append((facs, a))
    c50 = conflict_count(pat50_raw, key=lambda v: v[1])
    print(f"50 基座冲突（280000）：{c50}")

    conf_groups = [(p, vals) for p, vals in pat50_raw.items() if len({sg(v) for _, v in vals}) > 1]

    # 定向补集
    cand = set()
    for gi, (p, vals) in enumerate(conf_groups):
        pos = [f for f, a in vals if sg(a) != 0]
        zero = [f for f, a in vals if sg(a) == 0]
        if not pos or not zero:
            continue
        for f1 in pos:
            for f2 in zero:
                for i in range(220):
                    if f1[i] != f2[i]:
                        cand.add(i)
    cand_list = sorted(cand - set(idx50))
    print(f"候选补集：{len(cand_list)} 个")

    # 贪心删减（280000 上）
    cur = set(cand_list)
    t0 = time.time()
    for f in list(cur):
        trial = idx50 + sorted(cur - {f})
        if conflict_count(group(all_samples, trial)) == 0:
            cur.remove(f)
    print(f"贪心删减后补集：{len(cur)}（用时 {time.time()-t0:.0f}s）")
    final_idx = idx50 + sorted(cur)
    print(f"最终基座：{len(final_idx)} 因子")

    # 交叉验证
    d3_all = [x for sd in ['77', '331', '777'] for x in d3[sd]]
    d5_new = [x for sd in ['211', '555'] for x in d5[sd]]
    for name, samp in [("3seed(240000)", d3_all), ("5seed新(40000)", d5_new),
                       ("全(280000)", all_samples)]:
        cf = conflict_count(group(samp, final_idx))
        print(f"  {name}: 冲突 {cf}")

    out = {"basis50": basis50, "cand": len(cand_list), "final_size": len(final_idx),
           "added": [NAMES[i] for i in sorted(cur)],
           "c50_280k": c50, "n_conf_groups": len(conf_groups)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m31_cross_seed.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m31_cross_seed.json")
