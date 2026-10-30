# -*- coding: utf-8 -*-
"""M33：34 极小性验证 + 因子敏感性排序
- 34 因子逐因子试删（280000）→ 每因子删除后的冲突数（>0 = 必要）
- 全必要 → 34 为极小完备集（单因子不可再删）
- 敏感性排序：删除后冲突数越多 = 因子越重要（Φ 的结构权重）
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
    m32 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m32_minimal2.json"), encoding="utf-8"))
    idx34 = [NAMES.index(x) for x in m32["final_names"]]
    print(f"34 因子")

    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        d3 = pickle.load(f)
    with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
        d5 = pickle.load(f)
    all_samples = []
    for sd in ['77', '331', '777']:
        all_samples.extend(d3[sd])
    for sd in ['211', '555']:
        all_samples.extend(d5[sd])

    # 基线：34 冲突
    c0 = conflict_count(group(all_samples, idx34))
    print(f"34 基线冲突：{c0}")

    # 逐因子试删
    t0 = time.time()
    sens = []
    for i in idx34:
        trial = [x for x in idx34 if x != i]
        c = conflict_count(group(all_samples, trial))
        sens.append((c, NAMES[i]))
    sens.sort(reverse=True)
    print(f"敏感性排序（删因子后冲突数——{time.time()-t0:.0f}s）：")
    all_necessary = True
    for c, nm in sens:
        flag = "必要" if c > 0 else "冗余!"
        if c == 0:
            all_necessary = False
        print(f"  {nm}: {c} {flag}")
    print(f"\n全部必要（极小完备集）：{all_necessary}")

    out = {"baseline_conflict": c0, "all_necessary": all_necessary,
           "sensitivity": [(nm, c) for c, nm in sens]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m33_necessary.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m33_necessary.json")
