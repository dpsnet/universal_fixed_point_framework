# -*- coding: utf-8 -*-
"""n=10 选项 A：15000 独立样本复核 46 因子基座（seed 331，避开缓存 41/97/53、主 131、独立 77/211）。
输出：非决定模式数/频次/取值 + 补因子候选诊断（组内恒定且组间互异）+ 贪心最小补集 + 补后非决定数。
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
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_minbasis_results.json"), encoding="utf-8") as f:
        mb = json.load(f)
    BASE = mb["remove_set"]
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    base_idx = [NAMES.index(x) for x in BASE]
    base_set = set(base_idx)
    rest_idx = [i for i in range(len(factors)) if i not in base_set]
    print(f"基座 {len(base_idx)} 因子  待诊因子 {len(rest_idx)}", flush=True)

    # 15000 独立样本
    rng = random.Random(331)
    samples = []
    t0 = time.time()
    for _ in range(15000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        samples.append((omega, zbar))
    print(f"采样 15000 ({time.time()-t0:.0f}s)", flush=True)

    # 模式投影 + 非决定
    pat_samples = defaultdict(list)
    t0 = time.time()
    for si, (omega, zbar) in enumerate(samples):
        pat = pattern_on(omega, zbar, factors, base_idx)
        pat_samples[pat].append(si)
    print(f"模式投影 ({time.time()-t0:.0f}s): 模式 {len(pat_samples)}", flush=True)

    nondet_pats = {}
    for pat, sis in pat_samples.items():
        vals = set()
        for si in sis:
            omega, zbar = samples[si]
            vals.add(round(A_BG(10, omega, zbar), 6))
        if len(vals) > 1:
            nondet_pats[pat] = (sis, vals)
    print(f"非决定性模式数: {len(nondet_pats)}", flush=True)
    for pat, (sis, vals) in nondet_pats.items():
        print(f"  pat 频次 {len(sis)} 取值 {sorted(vals)}", flush=True)

    res = {"base": BASE, "base_size": len(base_idx), "indep_samples": 15000,
           "total_patterns": len(pat_samples), "nondet": len(nondet_pats),
           "nondet_details": [{"freq": len(sis), "vals": sorted(vals)} for pat, (sis, vals) in nondet_pats.items()]}

    if nondet_pats:
        # 补因子候选诊断（组内恒定且组间互异）
        candidates = defaultdict(list)
        for pat, (sis, vals) in nondet_pats.items():
            groups = defaultdict(list)
            for si in sis:
                omega, zbar = samples[si]
                a = round(A_BG(10, omega, zbar), 6)
                groups[("zero" if abs(a) < 1e-9 else ("pos" if a > 0 else "neg"))].append(si)
            for fi in rest_idx:
                fa, fb = factors[fi]
                gvals = defaultdict(set)
                for gname, sil in groups.items():
                    for si in sil:
                        omega, zbar = samples[si]
                        gvals[gname].add(sg_block(omega, zbar, fa, fb))
                if len(groups) == len(gvals) and all(len(v) == 1 for v in gvals.values()) and \
                   len(set(next(iter(v)) for v in gvals.values())) == len(groups):
                    candidates[fi].append(pat)
        print("候选补因子（区分非决定模式数）:", flush=True)
        for fi, pl in sorted(candidates.items(), key=lambda kv: -len(kv[1])):
            print(f"  {NAMES[fi]}: {len(pl)} 模式", flush=True)

        # 贪心最小补集
        remaining = dict(nondet_pats)
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
                print("贪心停滞：剩余未覆盖", len(remaining))
                break
            chosen.append(best)
            for p in list(remaining):
                if p in candidates[best]:
                    del remaining[p]
            print(f"  选 {NAMES[best]}（覆盖 {best_cnt}），剩余 {len(remaining)}", flush=True)
        final = base_set | set(chosen)
        res["candidates"] = {NAMES[fi]: len(pl) for fi, pl in candidates.items()}
        res["chosen_complements"] = [NAMES[i] for i in chosen]
        res["final_size"] = len(final)

        # 补后验证（15000 样本上）
        new_idx = sorted(final)
        pat_a = defaultdict(set)
        t0 = time.time()
        for omega, zbar in samples:
            pat = pattern_on(omega, zbar, factors, new_idx)
            pat_a[pat].add(round(A_BG(10, omega, zbar), 6))
        nd = sum(1 for v in pat_a.values() if len(v) > 1)
        print(f"补后基座 {len(final)} 15000 样本: 模式 {len(pat_a)} 非决定性 {nd} ({time.time()-t0:.0f}s)", flush=True)
        res["final_nondet_on_indep"] = nd

    with open(os.path.join(SCRIPT_DIR, "paperX_n10_indep_check_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n10_indep_check_results.json")
