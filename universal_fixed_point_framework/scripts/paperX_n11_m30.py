# -*- coding: utf-8 -*-
"""M30：55 泛化验证 + 反向贪心全局最小下探
- M30a：55 因子在 5seed（211/555 新 seed——分布外）0 冲突验证
- M30b：反向贪心（220 → 删冗余——5seed 100000 样本合并口径）——全局更小完备集
"""
import os, json, pickle, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name

CACHE = os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl")


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def conflict_count(pats):
    c = 0
    for p, vals in pats.items():
        if len({sg(v) for v in vals}) > 1:
            c += 1
    return c


def group_conflict(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return conflict_count(pat)


if __name__ == "__main__":
    factors = adj_partition_factors(11)
    NAMES = [factor_name(a, b) for a, b in factors]
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [NAMES.index(x) for x in basis50]
    m29 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m29_minimal.json"), encoding="utf-8"))
    idx55 = idx50 + [NAMES.index(x) for x in m29["added"]]
    print(f"55 基座 {len(idx55)} 因子")

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)
    samples = [(facs, a) for sd, data in datas.items() for facs, a in data]
    print(f"5seed 总样本 {len(samples)}（seed: {list(datas.keys())}）")

    # M30a：55 在 5seed 泛化
    c55 = group_conflict(samples, idx55)
    print(f"[M30a] 55 因子 5seed（100000 样本）冲突：{c55}")

    # M30b：反向贪心（从 220 精简）
    cur = list(range(220))
    t0 = time.time()
    n_round = 0
    while True:
        n_round += 1
        removed = 0
        for i in list(cur):
            trial = [x for x in cur if x != i]
            if group_conflict(samples, trial) == 0:
                cur = trial
                removed += 1
        print(f"  轮 {n_round}: 删除 {removed}——当前 {len(cur)} 因子（累计 {time.time()-t0:.0f}s）")
        if removed == 0:
            break
        if len(cur) < 40:
            break
    print(f"[M30b] 反向贪心最终：{len(cur)} 因子（0 冲突）")
    final_names = [NAMES[i] for i in sorted(cur)]
    print("  名字:", final_names)

    # 与 55 比较
    s55 = set(idx55)
    snew = set(cur)
    print(f"55 缺失（反向集有 55 无）：{len(snew - s55)} 个 -> {[NAMES[i] for i in sorted(snew - s55)][:20]}")
    print(f"反向集缺失（55 有反向无）：{len(s55 - snew)} 个 -> {[NAMES[i] for i in sorted(s55 - snew)][:20]}")

    out = {"c55_5seed": c55, "reverse_size": len(cur), "reverse_names": final_names,
           "diff_rev_minus_55": [NAMES[i] for i in sorted(snew - s55)],
           "diff_55_minus_rev": [NAMES[i] for i in sorted(s55 - snew)]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m30_reverse.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m30_reverse.json")
