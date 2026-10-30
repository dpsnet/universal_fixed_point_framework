# -*- coding: utf-8 -*-
"""n=10 独立复核冲突诊断：重采样 seed 77/211（各 15000），
对 49 因子基座找冲突模式（内部非决定 + 主表值冲突），并做补因子诊断（组内恒定且组间互异）。
输出 paperX_n10_final_base.json（最终基座）供 verify2 复用。
"""
import json, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def pattern_on(omega, zbar, factors, idx):
    return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)


if __name__ == "__main__":
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_nondet_diag.json"), encoding="utf-8") as f:
        diag = json.load(f)
    BASE = diag["base"] + diag["chosen_complements"]
    BASE = list(dict.fromkeys(BASE))

    with open(os.path.join(SCRIPT_DIR, "paperX_n10_base_table.json"), encoding="utf-8") as f:
        main_table = json.load(f)

    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    base_idx = [NAMES.index(x) for x in BASE]
    base_set = set(base_idx)
    rest_idx = [i for i in range(len(factors)) if i not in base_set]
    print(f"基座 {len(base_idx)} 因子  待诊因子 {len(rest_idx)}", flush=True)

    # 冲突样本收集：保留 (omega, zbar) 对象
    conflict_samples = defaultdict(list)  # pat -> [(omega,zbar), ...]
    conflict_vals = {}
    conflict_seeds = defaultdict(set)
    conflict_main = {}
    for seed in (77, 211):
        rng = random.Random(seed)
        t0 = time.time()
        samples = []
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
            samples.append((omega, zbar))
        pat_samples = defaultdict(list)
        for si, (omega, zbar) in enumerate(samples):
            pat = pattern_on(omega, zbar, factors, base_idx)
            pat_samples[pat].append((omega, zbar))
        print(f"seed {seed} 采样+投影 ({time.time()-t0:.0f}s): 模式 {len(pat_samples)}", flush=True)
        for pat, objs in pat_samples.items():
            vals = set()
            for omega, zbar in objs:
                vals.add(round(A_BG(10, omega, zbar), 6))
            key = ",".join(str(x) for x in pat)
            main_v = None
            if key in main_table:
                main_v = main_table[key]["bg"]
            conflict = len(vals) > 1 or (main_v is not None and not vals <= {round(main_v, 6)})
            if conflict:
                conflict_samples[pat].extend(objs)
                conflict_vals.setdefault(pat, set()).update(vals)
                conflict_seeds[pat].add(seed)
                conflict_main[pat] = main_v
    print(f"冲突模式数: {len(conflict_samples)}", flush=True)
    for pat, objs in conflict_samples.items():
        print(f"  pat 频次 {len(objs)} 取值 {sorted(conflict_vals[pat])} 主表值 {conflict_main[pat]} seeds {sorted(conflict_seeds[pat])}", flush=True)

    res = {"base": BASE, "base_size": len(base_idx),
           "conflict_patterns": [{"freq": len(objs), "vals": sorted(conflict_vals[pat]), "main": conflict_main[pat], "seeds": sorted(conflict_seeds[pat])} for pat, objs in conflict_samples.items()]}

    if not conflict_samples:
        print("无冲突——基座充分")
        with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_base.json"), "w", encoding="utf-8") as f:
            json.dump({"base": BASE, "size": len(BASE)}, f, ensure_ascii=False, indent=2)
        print("DONE（最终基座）")
        sys.exit(0)

    # 补因子诊断（组内恒定且组间互异）
    candidates = defaultdict(list)
    for pat, objs in conflict_samples.items():
        groups = defaultdict(list)
        for omega, zbar in objs:
            a = round(A_BG(10, omega, zbar), 6)
            groups[("zero" if abs(a) < 1e-9 else ("pos" if a > 0 else "neg"))].append((omega, zbar))
        for fi in rest_idx:
            fa, fb = factors[fi]
            gvals = defaultdict(set)
            for gname, olist in groups.items():
                for omega, zbar in olist:
                    gvals[gname].add(sg_block(omega, zbar, fa, fb))
            if len(groups) == len(gvals) and all(len(v) == 1 for v in gvals.values()) and \
               len(set(next(iter(v)) for v in gvals.values())) == len(groups):
                candidates[fi].append(pat)

    print("候选补因子（区分冲突模式数）:", flush=True)
    for fi, pl in sorted(candidates.items(), key=lambda kv: -len(kv[1])):
        print(f"  {NAMES[fi]}: {len(pl)} 模式", flush=True)

    remaining = dict(conflict_samples)
    chosen = []
    while remaining:
        best, best_cnt = None, 0
        for fi, pl in candidates.items():
            if fi in chosen:
                continue
            c = sum(1 for p in remaining if p in pl)
            if c > best_cnt:
                best, best_cnt = fi, c
        if best is None:
            print("贪心停滞：剩余", len(remaining))
            break
        chosen.append(best)
        for p in list(remaining):
            if p in candidates[best]:
                del remaining[p]
        print(f"  选 {NAMES[best]}（覆盖 {best_cnt}），剩余 {len(remaining)}", flush=True)

    final = base_set | set(chosen)
    final_names = [NAMES[i] for i in sorted(final)]
    print(f"补因子 {len(chosen)}: {[NAMES[i] for i in chosen]}", flush=True)
    print(f"最终基座 {len(final)}", flush=True)

    # 最终基座在冲突样本 + 2×15000 上验证
    new_idx = sorted(final)
    pat_a = defaultdict(set)
    t0 = time.time()
    for seed in (77, 211):
        rng = random.Random(seed)
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
            pat = pattern_on(omega, zbar, factors, new_idx)
            pat_a[pat].add(round(A_BG(10, omega, zbar), 6))
    nd = sum(1 for v in pat_a.values() if len(v) > 1)
    print(f"最终基座 2×15000 独立样本: 模式 {len(pat_a)} 非决定性 {nd} ({time.time()-t0:.0f}s)", flush=True)
    res["candidates"] = {NAMES[fi]: len(pl) for fi, pl in candidates.items()}
    res["chosen_complements"] = [NAMES[i] for i in chosen]
    res["final_size"] = len(final)
    res["final_indep_nondet"] = nd

    with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_base.json"), "w", encoding="utf-8") as f:
        json.dump({"base": final_names, "size": len(final)}, f, ensure_ascii=False, indent=2)
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_diag_violations.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n10_final_base.json")
