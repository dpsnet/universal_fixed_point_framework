# -*- coding: utf-8 -*-
"""M34d：44 敏感性重算（修正 M33——基线 0 的正确必要判定）
- 44 基线 0 冲突（M34c 实测）——删任一因子 → 冲突数（>0 = 必要）
- 正确敏感性排序（M33 在错误 34 上做的作废）
"""
import os, json, pickle, sys, time
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
    factors = adj_partition_factors(11)
    NAMES = [factor_name(a, b) for a, b in factors]
    m34c = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m34c_minimal.json"), encoding="utf-8"))
    idx44 = [NAMES.index(x) for x in m34c["final_names"]]
    print(f"44 因子")

    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        d3 = pickle.load(f)
    with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
        d5 = pickle.load(f)
    all_samples = []
    for sd in ['77', '331', '777']:
        all_samples.extend(d3[sd])
    for sd in ['211', '555']:
        all_samples.extend(d5[sd])

    c0 = conflict_count(group(all_samples, idx44))
    print(f"44 基线冲突：{c0}")

    t0 = time.time()
    sens = []
    for i in idx44:
        trial = [x for x in idx44 if x != i]
        c = conflict_count(group(all_samples, trial))
        sens.append((c, NAMES[i]))
    sens.sort(reverse=True)
    print(f"敏感性排序（{time.time()-t0:.0f}s）：")
    all_necessary = True
    for c, nm in sens:
        flag = "必要" if c > 0 else "冗余!"
        if c == 0:
            all_necessary = False
        print(f"  {nm}: {c} {flag}")
    print(f"\n全部必要（极小完备集）：{all_necessary}")

    out = {"baseline_conflict": c0, "all_necessary": all_necessary,
           "sensitivity": [(nm, c) for c, nm in sens]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m34d_sens.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m34d_sens.json")
