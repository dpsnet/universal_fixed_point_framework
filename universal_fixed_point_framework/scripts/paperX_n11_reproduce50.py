# -*- coding: utf-8 -*-
"""复现 M15 判定 + 列出 50 基座 80000 级多值模式的 A 值对"""
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


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [NAMES.index(x) for x in basis50]

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    for sd, data in datas.items():
        pat_a = defaultdict(set)
        pat_samp = defaultdict(list)
        for full, a in data:
            pat = tuple(full[i] for i in idx50)
            pat_a[pat].add(a)
            pat_samp[pat].append(a)
        multi = {p: sorted(v) for p, v in pat_a.items() if len(v) > 1}
        print(f"seed {sd}: 多值模式 {len(multi)}")
        for p, v in list(multi.items())[:8]:
            # 该模式的样本数
            cnt = len(pat_samp[p])
            print(f"  A 值 {v}  样本数 {cnt}")
