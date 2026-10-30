# -*- coding: utf-8 -*-
"""Phase 74：跨集一致性回溯审计（n=6..9，与 n=10 同标准）
- 基座：各阶最小充分基座（summary json）
- 主样本 40000（seed 131）+ 5 独立 seed × 15000（77/211/331/777/555）
- 输出：paperX_crossset_audit_n{n}.json（跨集冲突数 + 冲突模式）
用法：python paperX_crossset_audit.py 9 [8 7 6]
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


def get_basis(n):
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    if n == 9:
        d = json.load(open(base + "paperX_n9_final_summary.json", encoding="utf-8"))
        return list(d["base"])
    if n == 8:
        d = json.load(open(base + "paperX_n8_final_summary.json", encoding="utf-8"))
        return list(d["basis"])
    if n == 7:
        d = json.load(open(base + "paperX_n7_final_summary.json", encoding="utf-8"))
        return list(d["basis"])
    if n == 6:
        d = json.load(open(base + "paperX_n6_minbasis_results.json", encoding="utf-8"))
        return list(d["remove_set"])
    raise ValueError(n)


def audit(n, seeds=(77, 211, 331, 777, 555)):
    basis = get_basis(n)
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = []
    unknown = []
    for x in basis:
        if x in NAMES:
            idx.append(NAMES.index(x))
        else:
            unknown.append(x)
    if unknown:
        print(f"n={n} 因子名不在全集: {unknown}", flush=True)
    print(f"n={n}: 基座 {len(idx)} 因子", flush=True)

    def pattern_on(omega, zbar):
        return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)

    # 主样本
    rng = random.Random(131)
    pat_a = defaultdict(set)
    pat_cnt = defaultdict(int)
    t0 = time.time()
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar)
        pat_cnt[pat] += 1
        pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
    main_nondet = [p for p in pat_a if len(pat_a[p]) > 1]
    print(f" 主样本 40000 ({time.time()-t0:.0f}s): 模式 {len(pat_a)} 非决定 {len(main_nondet)}", flush=True)

    # 独立复核
    total = 0
    per_seed = []
    for sd in seeds:
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
        per_seed.append({"seed": sd, "patterns": len(pat2), "bad": bad, "secs": round(time.time() - t0)})
        print(f" seed {sd}: 模式 {len(pat2)} 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    print(f"n={n} 总计冲突 {total} -> {'PASS' if total == 0 else 'FAIL'}", flush=True)

    res = {"n": n, "basis": basis, "basis_size": len(idx), "main_samples": 40000,
           "main_nondet": len(main_nondet), "seeds": seeds, "per_seed": per_seed,
           "total_violations": total, "pass": total == 0}
    with open(os.path.join(SCRIPT_DIR, f"paperX_crossset_audit_n{n}.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    return res


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or [9]
    for n in ns:
        audit(n)
    print("DONE")
