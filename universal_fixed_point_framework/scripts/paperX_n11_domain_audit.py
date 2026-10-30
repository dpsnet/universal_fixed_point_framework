# -*- coding: utf-8 -*-
"""n=11 判据域修正复核（关键验证）
- float 模式（块和原值）+ 排除 A=0 样本：46/50 基座非决定判定（与 M14 同口径但过滤临界）
- 含 A=0 对照（复现 M14 的 6/7/5）与排除后对比
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
    idx46 = [NAMES.index(x) for x in basis46]
    idx50 = [NAMES.index(x) for x in basis50]

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    rep = {}
    for sd, data in datas.items():
        pat_all = defaultdict(set)    # 含 A=0（复现 M14）
        pat_nz = defaultdict(set)     # 排除 A=0
        n_zero = 0
        for full, a in data:
            pat = tuple(full[i] for i in idx46)
            pat_all[pat].add(a)
            if sign(a) == 0:
                n_zero += 1
                continue
            pat_nz[pat].add(a)
        nd_all = sum(1 for v in pat_all.values() if len(v) > 1)
        nd_nz = sum(1 for v in pat_nz.values() if len(v) > 1)
        rep[sd] = {"n_total": len(data), "n_A_zero": n_zero,
                   "nondet_46_all_M14口径": nd_all,
                   "nondet_46_excl_zero": nd_nz}
        print(f"seed {sd}: 含零 {nd_all} / 排除零 {nd_nz}（A=0 样本 {n_zero}）", flush=True)

    with open(os.path.join(SCRIPT_DIR, "paperX_n11_domain_audit.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    print("DONE -> paperX_n11_domain_audit.json")
