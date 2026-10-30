# -*- coding: utf-8 -*-
"""M3 快速诊断：57 维主表中 seed 77 冲突模式的 count + 主样本几何
- 重跑 seed 77 独立复核（57 维）捕获冲突模式投影
- 查 base57 主表该模式 count；若 count>1 直接对比主/独立分支的前缀括号
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG, bracket
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_base.json"), encoding="utf-8") as f:
        fb = json.load(f)
    base_names = list(dict.fromkeys(fb["base"] + ["s23_45678910", "s234_5678910", "s2345_678910",
                                                  "s23456_78910", "s234567_8910", "s2345678_910",
                                                  "s23456789_10"]))
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in base_names]

    def pattern_on(omega, zbar):
        return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)

    # 主表 57 维（含 count 与主样本几何）
    rng = random.Random(131)
    pat_main = defaultdict(list)
    for k in range(40000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar)
        pat_main[pat].append((round(A_BG(10, omega, zbar), 6), omega, zbar))
    print(f"主表 {len(pat_main)} 模式", flush=True)

    # seed 77 冲突
    rng = random.Random(77)
    conflicts = []
    for k in range(15000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar)
        v = round(A_BG(10, omega, zbar), 6)
        main_entries = pat_main.get(pat)
        if main_entries and not any(abs(e[0] - v) < 1e-9 for e in main_entries):
            conflicts.append({"sample": k, "main": main_entries[0][0], "indep": v,
                              "omega": omega, "zbar": zbar, "pat": pat, "main_count": len(main_entries)})
    print(f"seed 77 冲突 {len(conflicts)}", flush=True)

    # 前缀括号候选（8 个，0-based：粒子 2=索引1 … 粒子10=索引9）
    pref = [((1,), (2, 3, 4, 5, 6, 7, 8, 9)), ((1, 2), (3, 4, 5, 6, 7, 8, 9)),
            ((1, 2, 3), (4, 5, 6, 7, 8, 9)), ((1, 2, 3, 4), (5, 6, 7, 8, 9)),
            ((1, 2, 3, 4, 5), (6, 7, 8, 9)), ((1, 2, 3, 4, 5, 6), (7, 8, 9)),
            ((1, 2, 3, 4, 5, 6, 7), (8, 9)), ((1, 2, 3, 4, 5, 6, 7, 8), (9,))]
    pnames = ["s" + "".join(str(x + 1) for x in a) + "_" + "".join(str(x + 1) for x in b) for a, b in pref]

    out = []
    for ci, c in enumerate(conflicts):
        entry = {"sample": c["sample"], "main": c["main"], "indep": c["indep"],
                 "main_count": c["main_count"]}
        # 独立样本的 8 前缀括号符号
        ind_sig = tuple(1 if bracket(a, b, c["omega"], c["zbar"]) > 1e-9 else (-1 if bracket(a, b, c["omega"], c["zbar"]) < -1e-9 else 0) for a, b in pref)
        entry["indep_prefix"] = dict(zip(pnames, ind_sig))
        # 主样本同模式分支样本（若有）
        mains = pat_main[c["pat"]]
        entry["main_variants"] = []
        for mv, wo, zo in mains[:5]:
            msig = tuple(1 if bracket(a, b, wo, zo) > 1e-9 else (-1 if bracket(a, b, wo, zo) < -1e-9 else 0) for a, b in pref)
            entry["main_variants"].append({"bg": mv, "prefix": dict(zip(pnames, msig))})
        out.append(entry)
        print(f"冲突 {ci}: main={c['main']} indep={c['indep']} main_count={c['main_count']}", flush=True)
        print(f"  indep_prefix: {dict(zip(pnames, ind_sig))}", flush=True)
        for m in entry["main_variants"]:
            print(f"  main bg={m['bg']} prefix={m['prefix']}", flush=True)
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_recursive_diag2.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("DONE")
