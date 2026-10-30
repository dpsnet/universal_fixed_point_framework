# -*- coding: utf-8 -*-
"""M39b：删除 7 全补块 → 冲突判别（谱维数 37 vs 浮点伪影）
- 缓存（浮点符号）删除 7 全补 → 冲突数
- 0 → 谱维数 ≤ 37（真实）；>0 → 全补删除合并浮点子组 → 伪冲突（噪声相关）
- 对照：M34d 单删 s1_234567891011 = 22 冲突（噪声伪影级）
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


def group(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return pat


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    m34c = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m34c_minimal.json"), encoding="utf-8"))
    names44 = m34c["final_names"]
    fullset = set(range(n))
    fullcomp = [nm for nm in names44 if set(factors[NAMES.index(nm)][0]) | set(factors[NAMES.index(nm)][1]) == fullset]
    print(f"44 名单全补块 {len(fullcomp)}：{fullcomp}")
    idx44 = [NAMES.index(x) for x in names44]
    idx37 = [i for i in idx44 if i not in set(NAMES.index(x) for x in fullcomp)]
    print(f"37 因子 = 44 - 7 全补")

    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        d3 = pickle.load(f)
    with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
        d5 = pickle.load(f)
    all_samples = []
    for sd in ['77', '331', '777']:
        all_samples.extend(d3[sd])
    for sd in ['211', '555']:
        all_samples.extend(d5[sd])

    c44 = conflict_count(group(all_samples, idx44))
    c37 = conflict_count(group(all_samples, idx37))
    print(f"44 因子冲突：{c44}")
    print(f"37 因子（删 7 全补）冲突：{c37}")

    # 全补因子在缓存中的"非零率"（伪符号率）
    nz = 0
    tot = 0
    for sd in ['77', '331', '777']:
        for facs, a in d3[sd]:
            for nm in fullcomp:
                i = NAMES.index(nm)
                if facs[i] != 0:
                    nz += 1
                tot += 1
    print(f"全补块浮点伪符号率：{nz}/{tot}（{nz/tot:.3f}）")

    out = {"n": n, "fullcomp": fullcomp, "c44": c44, "c37": c37,
           "fullcomp_noise_rate": round(nz / tot, 4)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m39b_fullcomp.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m39b_fullcomp.json")
