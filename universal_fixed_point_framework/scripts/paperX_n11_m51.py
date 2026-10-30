# -*- coding: utf-8 -*-
"""M51：n=10 R1 生长对照（跨 n 标度）+ 26 名单结构
- n=10 R1 通式 → 贪心追加 → 完备大小（对照 n=11 的 26）
- n=11 26 名单必要性 + 结构
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


def r1_formula(n):
    r1 = []
    for m in range(2, n):
        r1.append("s%s_%s" % (str(m), str(m + 1)))
    for m in range(1, n - 1):
        r1.append("s1_%s" % "".join(str(x) for x in range(2, m + 2)))
    return r1


def grow(samples, names, NAMES, factors):
    """从给定名单贪心追加到 0 冲突"""
    idx = [NAMES.index(x) for x in names if x in NAMES]
    used = set(idx)
    cur = list(idx)
    c = conflict_count(group(samples, cur))
    growth = []
    step = 0
    while c > 0 and step < 300:
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
    # ===== n=10 R1 生长 =====
    n10 = 10
    f10 = adj_partition_factors(n10)
    N10 = [factor_name(a, b) for a, b in f10]
    with open(os.path.join(SCRIPT_DIR, "cache_n10_thr3x20000.pkl"), "rb") as f:
        d10 = pickle.load(f)
    s10 = []
    for sd in ["77", "331", "777"]:
        s10.extend(d10[sd])
    print(f"n=10 样本 {len(s10)}", flush=True)
    r1_10 = r1_formula(n10)
    print(f"n=10 R1 通式 {len(r1_10)} 因子", flush=True)
    cur10, g10, c10 = grow(s10, r1_10, N10, f10)
    print(f"n=10 R1 生长：追加 {len(g10)} 到冲突 {c10}（总 {len(cur10)}）", flush=True)
    print(f"追加：{g10}", flush=True)

    # ===== n=11 26 名单 =====
    n11 = 11
    f11 = adj_partition_factors(n11)
    N11 = [factor_name(a, b) for a, b in f11]
    with open(os.path.join(SCRIPT_DIR, "cache_n11_thr3x20000.pkl"), "rb") as f:
        d11 = pickle.load(f)
    s11 = []
    for sd in ["77", "331", "777"]:
        s11.extend(d11[sd])
    m50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m50_r1min.json"), encoding="utf-8"))
    r1_11 = m50["r1"]
    g11 = m50["growth"]
    names28 = r1_11 + g11
    red3 = ["s1_23456", "s1_2345678", "s1_23456789"]
    names26 = [x for x in names28 if x not in red3]
    idx26 = [N11.index(x) for x in names26]
    c26 = conflict_count(group(s11, idx26))
    print(f"\nn=11 26 名单（28 删 3 冗余）冲突：{c26}", flush=True)
    sens = {}
    n_nec = 0
    for i in idx26:
        trial = [x for x in idx26 if x != i]
        c = conflict_count(group(s11, trial))
        sens[N11[i]] = c
        if c > 0:
            n_nec += 1
    print(f"26 必要 {n_nec}/26", flush=True)
    print(f"26 冗余：{[nm for nm, c in sens.items() if c == 0]}", flush=True)

    out = {"n10": {"r1_size": len(r1_10), "growth": g10, "final_conflict": c10,
                   "final_size": len(cur10), "final_names": [N10[i] for i in sorted(cur10)]},
           "n11": {"r1_size": len(r1_11), "growth": g11, "names26": names26,
                   "c26": c26, "sens26": sens, "n26_necessary": n_nec}}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m51_r1scale.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m51_r1scale.json", flush=True)
