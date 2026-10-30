# -*- coding: utf-8 -*-
"""判据域修正验证：非零样本真实性 + n=10 同口径复核
- A≠0 样本的真实值分布（确认非数值误差）
- n=10 的 59 基座排除 A=0 后非决定（cache_n10_3x80000.pkl）
"""
import os, pickle, json, sys
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


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    # 1) n=11 非零样本真实值分布
    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        datas = pickle.load(f)
    nz_vals = []
    for sd, data in datas.items():
        for full, a in data:
            if sign(a) != 0:
                nz_vals.append(a)
    nz_vals.sort()
    import statistics
    print(f"n=11 非零样本 {len(nz_vals)} 个")
    print(f"  值分布: min {nz_vals[0]:.6f} max {nz_vals[-1]:.6f} median {nz_vals[len(nz_vals)//2]:.6f}")
    print(f"  绝对值中位数: {statistics.median(abs(x) for x in nz_vals):.6f}")
    neg = sum(1 for x in nz_vals if x < 0)
    print(f"  符号: 负 {neg} / 正 {len(nz_vals)-neg}")

    # 2) n=10 判据域复核
    n = 10
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    j10 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n10_final_summary_59.json"), encoding="utf-8"))
    b59 = [NAMES.index(x) for x in j10["base"]]
    with open(os.path.join(SCRIPT_DIR, "cache_n10_3x80000.pkl"), "rb") as f:
        d10 = pickle.load(f)
    rep10 = {}
    for sd, data in d10.items():
        pat_all = defaultdict(set)
        pat_nz = defaultdict(set)
        n_zero = 0
        for full, a in data:
            pat = tuple(full[i] for i in b59)
            pat_all[pat].add(a)
            if sign(a) == 0:
                n_zero += 1
                continue
            pat_nz[pat].add(a)
        rep10[sd] = {"n_total": len(data), "n_A_zero": n_zero,
                     "nondet_59_all": sum(1 for v in pat_all.values() if len(v) > 1),
                     "nondet_59_excl_zero": sum(1 for v in pat_nz.values() if len(v) > 1)}
        print(f"n=10 seed {sd}: 含零 {rep10[sd]['nondet_59_all']} / 排除零 {rep10[sd]['nondet_59_excl_zero']}（A=0 {n_zero}）", flush=True)

    with open(os.path.join(SCRIPT_DIR, "paperX_n10_domain_audit.json"), "w", encoding="utf-8") as f:
        json.dump({"nz_vals_n11": {"count": len(nz_vals), "min": nz_vals[0], "max": nz_vals[-1],
                                     "median_abs": statistics.median(abs(x) for x in nz_vals),
                                     "neg": neg, "pos": len(nz_vals)-neg},
                   "n10": rep10}, f, ensure_ascii=False, indent=1)
    print("DONE -> paperX_n10_domain_audit.json")
