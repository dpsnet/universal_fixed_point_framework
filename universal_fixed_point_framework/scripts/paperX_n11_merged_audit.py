# -*- coding: utf-8 -*-
"""跨 seed 合并判定（跨集一致性的严格口径）
- 3 seed 合并 240000 样本：46/50/4长块 基座模式 → A 符号冲突
- 冲突模式细节（哪些 seed 提供哪个值）
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

    for name, idx in [("46", idx46), ("50", idx50), ("4长块", idx_extra)]:
        pat_val = defaultdict(set)    # 模式 → A 符号集合
        pat_seed = defaultdict(set)   # 模式 → seed 集合
        pat_a = defaultdict(set)      # 模式 → A 值集合
        for sd, data in datas.items():
            for full, a in data:
                pat = tuple(full[i] for i in idx)
                pat_val[pat].add(sign(a))
                pat_seed[pat].add(sd)
                pat_a[pat].add(a)
        # 符号冲突（>1 符号）或 值冲突（>1 A 值）
        sym_conf = {p: sorted(v) for p, v in pat_val.items() if len(v) > 1}
        val_conf = {p: sorted(v) for p, v in pat_a.items() if len(v) > 1}
        print(f"\n{name} 基座（3 seed 合并 240000）:")
        print(f"  符号冲突模式: {len(sym_conf)} / 值冲突模式: {len(val_conf)}")
        for p, v in list(sym_conf.items())[:5]:
            print(f"    符号 {v}  seed {sorted(pat_seed[p])}")
        for p, v in list(val_conf.items())[:5]:
            print(f"    值 {v}  seed {sorted(pat_seed[p])}")
