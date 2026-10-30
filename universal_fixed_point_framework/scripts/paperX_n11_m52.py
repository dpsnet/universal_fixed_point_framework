# -*- coding: utf-8 -*-
"""M52：保存真实 26 名单（28 起点随机删序）+ 必要性 + n=10 26 验证
- M50 的 26 名单未保存——重跑 10 轮保存
- 26 名单 0 冲突 + 必要性
- n=10 R1 16+10=26 名单：0 冲突 + 必要性
"""
import os, sys, json, pickle, random, time
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


def minimize(samples, start_idx, seed):
    random.seed(seed)
    cur = list(start_idx)
    random.shuffle(cur)
    while True:
        removed_any = False
        for i in list(cur):
            trial = [x for x in cur if x != i]
            if conflict_count(group(samples, trial)) == 0:
                cur = trial
                removed_any = True
        if not removed_any:
            break
    return cur


def necessity(samples, idx, NAMES):
    sens = {}
    n_nec = 0
    for i in idx:
        trial = [x for x in idx if x != i]
        c = conflict_count(group(samples, trial))
        sens[NAMES[i]] = c
        if c > 0:
            n_nec += 1
    red = [nm for nm, c in sens.items() if c == 0]
    return sens, n_nec, red


if __name__ == "__main__":
    # ===== n=11：28 起点 10 轮保存名单 =====
    n11 = 11
    f11 = adj_partition_factors(n11)
    N11 = [factor_name(a, b) for a, b in f11]
    with open(os.path.join(SCRIPT_DIR, "cache_n11_thr3x20000.pkl"), "rb") as f:
        d11 = pickle.load(f)
    s11 = []
    for sd in ["77", "331", "777"]:
        s11.extend(d11[sd])
    m50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m50_r1min.json"), encoding="utf-8"))
    names28 = m50["names28"]
    idx28 = [N11.index(x) for x in names28]

    finals = []
    t0 = time.time()
    for r in range(10):
        cur = minimize(s11, idx28, 20261006 + r)
        finals.append([N11[i] for i in sorted(cur)])
        print(f"轮{r+1}：{len(cur)} 因子（{time.time()-t0:.0f}s）", flush=True)
    sizes = [len(x) for x in finals]
    print(f"10 轮：{sizes}——最小 {min(sizes)}", flush=True)

    # 找完备 26 名单（冲突 0 的第一个）
    best26 = None
    for f in finals:
        idx = [N11.index(x) for x in f]
        c = conflict_count(group(s11, idx))
        if c == 0:
            best26 = f
            break
    print(f"完备 26 名单：{best26}", flush=True)
    if best26:
        idx26 = [N11.index(x) for x in best26]
        c26 = conflict_count(group(s11, idx26))
        sens26, n26, red26 = necessity(s11, idx26, N11)
        print(f"26 冲突 {c26}、必要 {n26}/26、冗余 {red26}", flush=True)
    else:
        c26, sens26, n26, red26 = None, {}, 0, []

    # ===== n=10：R1 26 名单验证 =====
    n10 = 10
    f10 = adj_partition_factors(n10)
    N10 = [factor_name(a, b) for a, b in f10]
    with open(os.path.join(SCRIPT_DIR, "cache_n10_thr3x20000.pkl"), "rb") as f:
        d10 = pickle.load(f)
    s10 = []
    for sd in ["77", "331", "777"]:
        s10.extend(d10[sd])
    m51 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m51_r1scale.json"), encoding="utf-8"))
    names10 = m51["n10"]["final_names"]
    idx10 = [N10.index(x) for x in names10]
    c10 = conflict_count(group(s10, idx10))
    sens10, n10n, red10 = necessity(s10, idx10, N10)
    print(f"\nn=10 R1 26 名单：冲突 {c10}、必要 {n10n}/26、冗余 {red10}", flush=True)

    out = {"n11": {"sizes": sizes, "best26": best26, "c26": c26,
                   "sens26": sens26, "n26_necessary": n26, "redundant26": red26},
           "n10": {"names26": names10, "c26": c10, "sens26": sens10,
                   "n26_necessary": n10n, "redundant26": red10}}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m52_scale26.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m52_scale26.json", flush=True)
