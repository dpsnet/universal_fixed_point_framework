# -*- coding: utf-8 -*-
"""n=11 判据口径澄清（解析完全闭合第三步）
- 排除 A=0 样本（临界，判据域外）后：46/50/4长块 符号模式 → A 符号单值性
- 177 个无长块翻转的 A 翻转对：翻转块归属分析
"""
import os, pickle, json, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

CACHE = os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl")


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


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    j46 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill45.json"), encoding="utf-8"))
    basis46 = list(j46["final_set"])
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    extra50 = list(j50.get("added", []))
    idx46 = [NAMES.index(x) for x in basis46]
    idx50 = [NAMES.index(x) for x in basis50]
    idx_extra = [NAMES.index(x) for x in extra50]

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    # 1) 排除 A=0 后的单值性
    stats = {"total_nz": 0, "extra4_multi": 0, "b46_multi": 0, "b50_multi": 0}
    pats = {"extra4": defaultdict(set), "b46": defaultdict(set), "b50": defaultdict(set)}
    # 2) 无长块翻转的 A 翻转对：翻转块统计
    flip_blocks_counter = defaultdict(int)
    no_extra_flip_total = 0

    for sd, data in datas.items():
        for full, a in data:
            sa = sign(a)
            if sa == 0:
                continue  # 判据域外
            stats["total_nz"] += 1
            se = tuple(sign(full[k]) for k in idx_extra)
            pats["extra4"][se].add(sa)
            s46 = tuple(sign(full[k]) for k in idx46)
            pats["b46"][s46].add(sa)
            s50 = tuple(sign(full[k]) for k in idx50)
            pats["b50"][s50].add(sa)
        for i in range(len(data) - 1):
            f0, a0 = data[i]
            f1, a1 = data[i + 1]
            if sign(a0) != sign(a1) and sign(a0) != 0 and sign(a1) != 0:
                any_extra_flip = any(sign(f0[k]) != sign(f1[k]) for k in idx_extra)
                if not any_extra_flip:
                    no_extra_flip_total += 1
                    for k in range(len(factors)):
                        if sign(f0[k]) != sign(f1[k]):
                            flip_blocks_counter[NAMES[k]] += 1
        print(f"seed {sd} done", flush=True)

    for key in ["extra4", "b46", "b50"]:
        multi = sum(1 for v in pats[key].values() if len(v) > 1)
        stats[key + "_multi"] = multi
        print(f"{key}: {len(pats[key])} 模式, 多符号 {multi} ({'FAIL' if multi else '单值 ✓'})")
    print(f"非零样本总数: {stats['total_nz']}")
    print(f"\n无长块翻转的 A 翻转对: {no_extra_flip_total}")
    top = sorted(flip_blocks_counter.items(), key=lambda x: -x[1])[:15]
    print("其翻转块 Top15:")
    for b, c in top:
        print(f"  {b}: {c}")

    with open(os.path.join(SCRIPT_DIR, "paperX_n11_criterion_domain.json"), "w", encoding="utf-8") as f:
        json.dump({"stats": stats, "no_extra_flip_total": no_extra_flip_total,
                   "flip_block_top": top}, f, ensure_ascii=False, indent=1)
    print("DONE -> paperX_n11_criterion_domain.json")
