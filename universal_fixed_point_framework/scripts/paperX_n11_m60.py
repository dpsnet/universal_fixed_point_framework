# -*- coding: utf-8 -*-
"""M60：锚 1 特权检验——各锚族覆盖力比较
- 假设：锚 1（唯一负 ω 粒子）的序关系是符号信息主载体——锚 1 族最经济
- 对 k=1..n：锚 k 族 = 相邻单对 + 锚 k 前缀（s_{k,k+1..m}）+ 锚 k 前缀块分裂（s_{k..j, j+1..}）
- R1 式生长（从锚 k 族出发贪心追加）——比较覆盖力
"""
import os, sys, json, pickle, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len(set(vals)) > 1)


def group(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return pat


def anchor_family(n, k):
    """锚 k 族：相邻单对 + 锚 k 前缀 + 锚 k 前缀块分裂（覆盖所有含 k 的区间块）"""
    fam = []
    # 相邻单对（全部——不是锚专属，作为公共基座）
    for m in range(2, n):
        fam.append("s%s_%s" % (str(m), str(m + 1)))
    # 锚 k 前缀：s_{k, k+1..m}
    for m in range(k, n):
        fam.append("s%s_%s" % (str(k), "".join(str(x) for x in range(k + 1, m + 1))))
    # 锚 k 前缀块分裂：s_{k..j, j+1..}
    for j in range(k, n - 1):
        fam.append("s%s_%s" % ("".join(str(x) for x in range(k, j + 1)),
                               "".join(str(x) for x in range(j + 1, n))))
    return fam


def grow(samples, names, NAMES, factors, max_steps=100):
    idx = [NAMES.index(x) for x in names if x in NAMES]
    used = set(idx)
    cur = list(idx)
    c = conflict_count(group(samples, cur))
    growth = []
    step = 0
    while c > 0 and step < max_steps:
        best = None
        best_c = c
        for i in range(len(factors)):
            if i in used:
                continue
            ci = conflict_count(group(samples, cur + [i]))
            if ci < best_c:
                best_c = ci
                best = i
        if best is None:
            break
        cur.append(best)
        used.add(best)
        growth.append((NAMES[best], best_c))
        c = best_c
        step += 1
    return cur, growth, c


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    with open(os.path.join(SCRIPT_DIR, "cache_n11_thr3x20000.pkl"), "rb") as f:
        d = pickle.load(f)
    all_samples = []
    for sd in ["77", "331", "777"]:
        all_samples.extend(d[sd])
    print(f"样本 {len(all_samples)}", flush=True)

    results = {}
    t0 = time.time()
    for k in range(1, n + 1):
        fam = anchor_family(n, k)
        # 去重 + 只留有效因子
        fam = sorted(set(fam), key=lambda x: NAMES.index(x) if x in NAMES else 999)
        fam = [x for x in fam if x in NAMES]
        idx = [NAMES.index(x) for x in fam]
        c0 = conflict_count(group(all_samples, idx))
        cur, growth, cf = grow(all_samples, fam, NAMES, factors)
        results[str(k)] = {"family_size": len(fam), "c0": c0,
                           "growth": len(growth), "final": len(cur), "cf": cf}
        print(f"锚 {k}：族 {len(fam)} 因子冲突 {c0}——生长 {len(growth)}——总 {len(cur)} 冲突 {cf}（{time.time()-t0:.0f}s）", flush=True)

    # 最小覆盖的锚
    best_anchor = min(results, key=lambda k: results[k]["final"])
    print(f"\n最经济锚：{best_anchor}（{results[best_anchor]['final']} 因子）", flush=True)

    out = {"n": n, "results": results, "best_anchor": best_anchor,
           "anchor1_final": results["1"]["final"]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m60_anchor.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m60_anchor.json", flush=True)
