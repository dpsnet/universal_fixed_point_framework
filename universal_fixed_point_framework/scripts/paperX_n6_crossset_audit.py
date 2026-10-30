# -*- coding: utf-8 -*-
"""n=6 跨集一致性审计（环状 20 因子空间）：
基座 12（minbasis remove_set）→ 40000 主（seed 31，与原 minbasis 同）+ 5×15000 独立
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_fullbasis import sg_pattern6_full

NAMES6 = ["s1_23", "s12_3", "s123_4", "s56", "s23", "s1_234", "s12_34", "s34",
          "s2_34", "s23_4", "s12", "s345_6", "s45_6", "s45", "s3_45", "s34_5",
          "s234_5", "s61", "s2_345", "s23_45"]

if __name__ == "__main__":
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    d = json.load(open(base + "paperX_n6_minbasis_results.json", encoding="utf-8"))
    basis = list(d["remove_set"])
    idx = [NAMES6.index(x) for x in basis]
    print(f"n=6 基座 {len(idx)}/20", flush=True)

    def pattern_on(omega, zbar):
        full = sg_pattern6_full(omega, zbar)
        return tuple(full[i] for i in idx)

    rng = random.Random(31)
    pat_a = defaultdict(set)
    t0 = time.time()
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar)
        pat_a[pat].add(round(A_BG(6, omega, zbar), 6))
    main_nondet = [p for p in pat_a if len(pat_a[p]) > 1]
    print(f"主样本 40000 ({time.time()-t0:.0f}s): 模式 {len(pat_a)} 非决定 {len(main_nondet)}", flush=True)

    total = 0
    for sd in (77, 211, 331, 777, 555):
        rng = random.Random(sd)
        pat2 = defaultdict(set)
        bad = 0
        t0 = time.time()
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
            pat = pattern_on(omega, zbar)
            pat2[pat].add(round(A_BG(6, omega, zbar), 6))
        for p, vals in pat2.items():
            if len(vals) > 1:
                bad += 1
            if p in pat_a and not vals <= pat_a[p]:
                bad += 1
        total += bad
        print(f"seed {sd}: 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    print(f"n=6 总计冲突 {total} -> {'PASS' if total == 0 else 'FAIL'} 基座 {len(idx)}", flush=True)

    res = {"n": 6, "basis": basis, "basis_size": len(idx), "main_samples": 40000,
           "main_nondet": len(main_nondet), "total_violations": total, "pass": total == 0}
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_crossset_audit.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
