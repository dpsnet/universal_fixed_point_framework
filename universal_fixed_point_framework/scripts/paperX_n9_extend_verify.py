# -*- coding: utf-8 -*-
"""n=9 补因子跨集验证（通用）：27 基座 + extra 因子 → 40000 主 + 5×15000 独立
用法：python paperX_n9_extend_verify.py s12_3456 s1234_56789 s123456_789 s12345678_9
"""
import json, os, random, sys, time
from collections import defaultdict

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


if __name__ == "__main__":
    n = 9
    extra = list(dict.fromkeys(sys.argv[1:]))
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    d = json.load(open(base + "paperX_n9_final_summary.json", encoding="utf-8"))
    basis = list(dict.fromkeys(list(d["base"]) + extra))
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in basis]
    print(f"n=9 基座 {len(idx)}/120 (+{len(extra)})", flush=True)

    def pattern_on(omega, zbar):
        return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)

    rng = random.Random(131)
    pat_a = defaultdict(set)
    t0 = time.time()
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar)
        pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
    main_nondet = [p for p in pat_a if len(pat_a[p]) > 1]
    print(f"主样本 40000 ({time.time()-t0:.0f}s): 模式 {len(pat_a)} 非决定 {len(main_nondet)}", flush=True)

    total = 0
    for sd in (77, 211, 331, 777, 555):
        rng = random.Random(sd)
        pat2 = defaultdict(set)
        bad = 0
        t0 = time.time()
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            pat = pattern_on(omega, zbar)
            pat2[pat].add(round(A_BG(n, omega, zbar), 6))
        for p, vals in pat2.items():
            if len(vals) > 1:
                bad += 1
            if p in pat_a and not vals <= pat_a[p]:
                bad += 1
        total += bad
        print(f"seed {sd}: 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    print(f"总计冲突 {total} -> {'PASS' if total == 0 else 'FAIL'} 基座 {len(idx)}", flush=True)

    res = {"n": n, "basis": basis, "basis_size": len(idx), "extra": extra,
           "total_violations": total, "pass": total == 0}
    with open(os.path.join(SCRIPT_DIR, "paperX_n9_extend_summary.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
