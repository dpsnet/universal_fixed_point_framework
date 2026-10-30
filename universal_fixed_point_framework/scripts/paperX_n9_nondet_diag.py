# -*- coding: utf-8 -*-
"""n=9 25 因子尾部基座非决定性诊断（参照 n=8 paperX_n8_nondet_diag.py）：
40000 样本收集 8 个稀有非决定性模式（0 vs ±1），
扫描 120 因子全集中未入基座的 95 因子，贪心找最小补因子集。
"""
import json, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n9_criterion import adj_partition_factors, sg_pattern9

BASE = ['s2_3', 's2_3456789', 's23_456789', 's234_56789', 's2345678_9',
        's3_4', 's3_456789', 's34_56789', 's345_6789',
        's4_5', 's4_56789', 's45678_9',
        's5_6', 's5_678', 's56_78', 's5_6789', 's5678_9',
        's6_7', 's67_8', 's6_789', 's678_9',
        's7_8', 's7_89', 's78_9', 's8_9']


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def pattern_on(omega, zbar, factors, idx):
    return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)


def sample_with_full(n_samples, seed, n=9):
    rng = random.Random(seed)
    out = []
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        out.append((omega, zbar))
    print(f"采样 {n_samples} ({time.time()-t0:.0f}s)", flush=True)
    return out


if __name__ == "__main__":
    factors = adj_partition_factors(9)
    NAMES = [factor_name(a, b) for a, b in factors]
    base_idx = [NAMES.index(x) for x in BASE]
    base_set = set(base_idx)
    rest_idx = [i for i in range(len(factors)) if i not in base_set]
    print(f"基座 {len(base_idx)}  待诊因子 {len(rest_idx)}", flush=True)

    samples = sample_with_full(40000, 131)

    # 收集非决定性模式及样本索引
    pat_samples = defaultdict(list)
    t0 = time.time()
    for si, (omega, zbar) in enumerate(samples):
        pat = pattern_on(omega, zbar, factors, base_idx)
        pat_samples[pat].append(si)
    print(f"模式投影 ({time.time()-t0:.0f}s)", flush=True)

    nondet_pats = {}
    for pat, sis in pat_samples.items():
        vals = set()
        for si in sis:
            omega, zbar = samples[si]
            vals.add(round(A_BG(9, omega, zbar), 6))
        if len(vals) > 1:
            nondet_pats[pat] = (sis, vals)
    print(f"非决定性模式数: {len(nondet_pats)}", flush=True)
    for pat, (sis, vals) in nondet_pats.items():
        print(f"  pat 频次 {len(sis)} 取值 {sorted(vals)}", flush=True)

    if not nondet_pats:
        print("无非决定性——无需补因子")
        sys.exit(0)

    # 对每个非决定性模式找能区分的候选因子（补集内）
    candidates = defaultdict(list)  # factor -> 区分模式数
    for pat, (sis, vals) in nondet_pats.items():
        # 样本按 A_BG 符号分组（0 vs ±1）
        groups = defaultdict(list)
        for si in sis:
            omega, zbar = samples[si]
            a = round(A_BG(9, omega, zbar), 6)
            groups[("zero" if abs(a) < 1e-9 else ("pos" if a > 0 else "neg"))].append(si)
        for fi in rest_idx:
            fa, fb = factors[fi]
            gvals = defaultdict(set)
            for gname, sil in groups.items():
                for si in sil:
                    omega, zbar = samples[si]
                    gvals[gname].add(sg_block(omega, zbar, fa, fb))
            # 修正判定：组内恒定 且 组间取值互不相同（同一非决定模式内真正分裂）
            if len(groups) == len(gvals) and all(len(v) == 1 for v in gvals.values()) and \
               len(set(next(iter(v)) for v in gvals.values())) == len(groups):
                candidates[fi].append(pat)

    print("候选补因子（区分非决定模式数）:", flush=True)
    for fi, pl in sorted(candidates.items(), key=lambda kv: -len(kv[1])):
        print(f"  {NAMES[fi]}: {len(pl)} 模式", flush=True)

    # 贪心最小补因子集
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
            print("贪心停滞：剩余未覆盖模式数", len(remaining))
            break
        chosen.append(best)
        for p in list(remaining):
            if p in candidates[best]:
                del remaining[p]
        print(f"  选 {NAMES[best]}（覆盖 {best_cnt} 模式），剩余 {len(remaining)}", flush=True)

    final = base_set | set(chosen)
    print(f"补因子 {len(chosen)}: {[NAMES[i] for i in chosen]}", flush=True)
    print(f"最终基座 {len(final)}: {sorted(NAMES[i] for i in final)}", flush=True)

    # 新基座在 40000 主样本上验证
    new_idx = sorted(final)
    pat_a = defaultdict(set)
    t0 = time.time()
    for omega, zbar in samples:
        pat = pattern_on(omega, zbar, factors, new_idx)
        pat_a[pat].add(round(A_BG(9, omega, zbar), 6))
    nondet = sum(1 for v in pat_a.values() if len(v) > 1)
    print(f"新基座 40000 主样本: 模式 {len(pat_a)} 非决定性 {nondet} ({time.time()-t0:.0f}s)", flush=True)

    res = {"base": BASE, "base_size": 25, "nondet_count": len(nondet_pats),
           "candidates": {NAMES[fi]: len(pl) for fi, pl in candidates.items()},
           "chosen_complements": [NAMES[i] for i in chosen],
           "final_size": len(final), "main_nondet": nondet}
    with open(os.path.join(SCRIPT_DIR, "paperX_n9_nondet_diag.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
