# -*- coding: utf-8 -*-
"""M48：R1 通式 → 完备覆盖的生长律（Φ 解析形式入口）
- R1 通式 18 因子（阈值化口径）冲突
- 从 R1 18 出发贪心加因子（每步选冲突减少最多的）→ 0 冲突所需追加数
- 生长名单 vs 40/43 极小名单的交集
"""
import os, sys, json, pickle
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


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    with open(os.path.join(SCRIPT_DIR, "cache_n11_thr3x20000.pkl"), "rb") as f:
        d = pickle.load(f)
    all_samples = []
    for sd in ["77", "331", "777"]:
        all_samples.extend(d[sd])
    print(f"阈值化样本 {len(all_samples)}", flush=True)

    # R1 通式 18 因子：s2_3..s10_11（9 相邻）+ s1_2..s1_2345678910（9 前缀）
    r1 = []
    for m in range(2, 11):
        r1.append("s%s_%s" % (str(m), str(m + 1)))
    for m in range(1, 10):
        r1.append("s1_%s" % "".join(str(x) for x in range(2, m + 2)))
    # 上面生成验证：s2_3..s10_11 ✓；s1_2, s1_23, ..., s1_2345678910 ✓
    r1_idx = [NAMES.index(x) for x in r1 if x in NAMES]
    print(f"R1 通式 {len(r1_idx)} 因子：{r1}", flush=True)

    # R1 阈值化冲突
    c_r1 = conflict_count(group(all_samples, r1_idx))
    print(f"R1 18 因子阈值化冲突：{c_r1}", flush=True)

    # 贪心生长：每步加冲突减少最多的未用因子
    cur = list(r1_idx)
    used = set(cur)
    growth = []
    c = c_r1
    step = 0
    while c > 0 and step < 210:
        best = None
        best_c = c
        for i in range(len(factors)):
            if i in used:
                continue
            trial = cur + [i]
            ci = conflict_count(group(all_samples, trial))
            if ci < best_c:
                best_c = ci
                best = i
        if best is None:
            print(f"无法继续减少（卡在 {c}）", flush=True)
            break
        cur.append(best)
        used.add(best)
        growth.append((NAMES[best], best_c))
        c = best_c
        step += 1
        if step % 10 == 0:
            print(f"步 {step}：冲突 {c}（追加 {step} 因子）", flush=True)

    print(f"\nR1 生长：{step} 步到冲突 {c}（总 {len(cur)} 因子）", flush=True)
    if c == 0:
        print(f"追加名单：{growth}", flush=True)

    # 与 40/43 极小名单交集
    m40 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m40_thr_spectral.json"), encoding="utf-8"))
    m46 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m46_globalmin.json"), encoding="utf-8"))
    names43 = m40["final_names"]
    names40 = m46["min_names"]
    inter43 = [x for x in growth if x in names43]
    inter40 = [x for x in growth if x in names40]
    print(f"生长追加 ∩ 43 名单：{len(inter43)}/{len(growth)}")
    print(f"生长追加 ∩ 40 名单：{len(inter40)}/{len(growth)}")

    out = {"n": n, "r1_names": r1, "c_r1": c_r1, "growth": growth,
           "final_conflict": c, "final_size": len(cur),
           "inter43": inter43, "inter40": inter40}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m48_r1growth.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m48_r1growth.json", flush=True)
