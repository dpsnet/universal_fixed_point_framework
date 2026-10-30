# -*- coding: utf-8 -*-
"""n=6 条件判据搜索：固定某因子值后，剩余 11 因子是否有 2 因子非零判据。
若存在 → 判据 = "条件因子条件 ∧ 剩余 2 因子规则"（分块判定结构）。
"""
import json, os, random, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_fullbasis import sg_pattern6_full
from paperX_n6_base12 import BASE12

NAMES = ["s1_23","s12_3","s123_4","s56","s23","s1_234","s34","s12",
         "s345_6","s45_6","s45","s61"]

def cache(n=80000, seed=71):
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        full = sg_pattern6_full(omega, zbar)
        base = tuple(full[i] for i in BASE12)
        data.append((base, round(A_BG(6, omega, zbar), 6)))
    return data

if __name__ == "__main__":
    data = cache(80000)
    pat_a = {}
    for b, a in data:
        pat_a[b] = a
    nz = {b: a for b, a in pat_a.items() if abs(a) > 1e-9}
    print(f"模式: {len(pat_a)}  非零: {len(nz)}")

    # 对每个条件因子 c 和值 v：子集中找 2 因子判据
    results = {}
    for c in range(12):
        for v in (-1, 1):
            sub = {b: a for b, a in pat_a.items() if b[c] == v}
            if not sub:
                continue
            found = []
            for i in range(12):
                if i == c:
                    continue
                for j in range(i+1, 12):
                    if j == c:
                        continue
                    groups = defaultdict(set)
                    for b, a in sub.items():
                        groups[(b[i], b[j])].add(1 if abs(a) > 1e-9 else 0)
                    if all(len(g) == 1 for g in groups.values()):
                        found.append((i, j))
            if found:
                results[f"{NAMES[c]}={v}"] = [[NAMES[i], NAMES[j]] for i, j in found]
                print(f"条件 {NAMES[c]}={v} (模式 {len(sub)}): {len(found)} 个 2 因子判据, 例: {[NAMES[i] for i in found[0]]}")

    print(f"\n条件判据族数: {len(results)}")

    # 若无条件判据：报告最接近的（混合组数）分布
    if not results:
        best = []
        for c in range(12):
            for v in (-1, 1):
                sub = {b: a for b, a in pat_a.items() if b[c] == v}
                if not sub:
                    continue
                min_mixed = None
                for i in range(12):
                    if i == c: continue
                    for j in range(i+1, 12):
                        if j == c: continue
                        groups = defaultdict(set)
                        for b, a in sub.items():
                            groups[(b[i], b[j])].add(1 if abs(a) > 1e-9 else 0)
                        m = sum(1 for g in groups.values() if len(g) > 1)
                        if min_mixed is None or m < min_mixed:
                            min_mixed = m
                best.append((min_mixed, f"{NAMES[c]}={v}", len(sub)))
        best.sort()
        print("最接近条件判据:")
        for m, name, n in best[:10]:
            print(f"  {name} (模式 {n}): 最小混合组 {m}")

    res = {
        "patterns": len(pat_a),
        "nonzero": len(nz),
        "conditional_families": {k: v for k, v in results.items()},
    }
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_cond_criterion_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
