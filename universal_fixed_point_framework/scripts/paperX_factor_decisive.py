# -*- coding: utf-8 -*-
"""Phase 75 M1/M2：补因子决定性验证（n=8/9）
对冲突 pat（原基座版）：收集该 pat 内全部样本 (bg, 补因子投影)
- 决定性：同 (pat, 补因子投影) → bg 单值
- 必需性：删单个补因子后是否仍决定性（冗余检测）
用法：python paperX_factor_decisive.py 8
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors

EXTRA = {
    8: ["s1_23456", "s1_2345678", "s12_345678", "s123_45678", "s12345_678",
        "s1234567_8", "s23456_78", "s1234_56"],
    9: ["s12_3456", "s1234_56789", "s123456_789", "s12345678_9",
        "s1_23456", "s123_456", "s1234567_89", "s23_45", "s2_345678",
        "s23456_789", "s456_789"],
}


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def get_base(n):
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    if n == 8:
        return list(json.load(open(base + "paperX_n8_final_summary.json", encoding="utf-8"))["basis"])
    if n == 9:
        return list(json.load(open(base + "paperX_n9_final_summary.json", encoding="utf-8"))["base"])


if __name__ == "__main__":
    n = int(sys.argv[1])
    extra = EXTRA[n]
    basis0 = get_base(n)
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx0 = [NAMES.index(x) for x in basis0]
    ex_idx = [NAMES.index(x) for x in extra]
    print(f"n={n}: 原基座 {len(idx0)} + 补因子 {len(ex_idx)}", flush=True)

    # 收集：冲突 pat（原基座下）内全部样本的 (bg, 补因子投影)
    conf_samples = defaultdict(list)  # pat -> [(bg, tuple(补因子投影))]
    seeds = (77, 211, 331, 777, 555)
    for sd in [131] + list(seeds):
        rng = random.Random(sd)
        nn = 40000 if sd == 131 else 15000
        t0 = time.time()
        for _ in range(nn):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx0)
            bg = round(A_BG(n, omega, zbar), 6)
            conf_samples[pat].append((bg, tuple(sg_block(omega, zbar, factors[k][0], factors[k][1]) for k in ex_idx)))
        print(f"seed {sd} 采集 ({time.time()-t0:.0f}s)", flush=True)

    # 冲突 pat = 组内 bg 多值
    conf = {p: recs for p, recs in conf_samples.items() if len(set(x[0] for x in recs)) > 1}
    print(f"冲突 pat 数: {len(conf)}", flush=True)

    out = []
    for p, recs in conf.items():
        bgs = sorted(set(x[0] for x in recs))
        # 决定性检查：同 (pat, 补因子投影) → bg 单值？
        byproj = defaultdict(set)
        for bg, proj in recs:
            byproj[proj].add(bg)
        nondet = {proj: sorted(v) for proj, v in byproj.items() if len(v) > 1}
        # 必需性：删单个补因子
        necessity = []
        for k in range(len(ex_idx)):
            byproj_k = defaultdict(set)
            for bg, proj in recs:
                pp = proj[:k] + proj[k + 1:]
                byproj_k[pp].add(bg)
            nd = sum(1 for v in byproj_k.values() if len(v) > 1)
            necessity.append({"factor": extra[k], "nondet_without": nd})
        dec = {"pat": "".join(str(x) for x in p), "main_bg": None, "seeds_bg": bgs,
               "n_records": len(recs), "n_projs": len(byproj),
               "nondet_with_full_extra": len(nondet),
               "necessity": necessity,
               "determining_subset": [x["factor"] for x in necessity if x["nondet_without"] > 0]}
        out.append(dec)
        print(f"pat {''.join(str(x) for x in p)}: bg={bgs} 记录 {len(recs)} 投影 {len(byproj)} "
              f"补全决定性 {len(nondet)==0}; 必需因子 {len(dec['determining_subset'])}: {dec['determining_subset']}", flush=True)

    with open(os.path.join(SCRIPT_DIR, f"paperX_n{n}_factor_decisive.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("DONE")
