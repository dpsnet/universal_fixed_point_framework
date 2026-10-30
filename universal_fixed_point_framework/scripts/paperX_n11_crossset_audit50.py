# -*- coding: utf-8 -*-
"""M16 部分：50 基座交叉验证——211/555 @20000（复用 cache_n11_5seed.pkl）"""
import json, os, pickle, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

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

def nondet_count(patterns, idx):
    pat_a = defaultdict(set)
    for full, a in patterns:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return sum(1 for v in pat_a.values() if len(v) > 1)

n = 11
factors = adj_partition_factors(n)
NAMES = [factor_name(a, b) for a, b in factors]
fj = json.load(open(SCRIPT_DIR + "/paperX_n11_fill46_80000.json", encoding="utf-8"))
b50 = [NAMES.index(x) for x in fj["final_set"]]
with open(SCRIPT_DIR + "/cache_n11_5seed.pkl", "rb") as f:
    datas = pickle.load(f)

res = {}
for sd in ["77", "211", "331", "777", "555"]:
    data = datas[sd]
    nd = nondet_count(data, b50)
    uniq = len(set(tuple(d[i] for i in b50) for d, _ in data))
    res[sd] = {"nondet_20000": nd, "unique_rate": round(uniq / 20000, 4)}
    print(f"seed {sd} @20000: 非决定 {nd} 唯一率 {uniq/20000:.3f}", flush=True)

out = {"basis_size": len(b50), "per_seed": res,
       "all_zero_20000": all(v["nondet_20000"] == 0 for v in res.values())}
with open(SCRIPT_DIR + "/paperX_n11_crossset_audit50.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("DONE -> paperX_n11_crossset_audit50.json")
