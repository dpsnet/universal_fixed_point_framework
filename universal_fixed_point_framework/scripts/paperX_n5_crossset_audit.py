# -*- coding: utf-8 -*-
"""n=5 跨集一致性统一审计（启发⑥落地：方法统一）
- 基座：sg_pattern5 8 因子（4 单粒子对 + 环对 s5_1 + 3 前缀块）
- 40000 主（seed 131）+ 5 seed × 15000（同 n=6..10 标准）
- 若 FAIL → 补扩展因子（8+2）重验
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5


def audit(use_ext=False):
    n = 5
    # n=5 判据：8 sg 或 +2 扩展
    if use_ext:
        # 扩展因子（s12_34, s1_234 补?）：minimal_results ext_labels 为块对 label——
        # 采用等价扩展：sg_block((0,1),(2,3)) s12_34 + sg_block((0,),(2,3,4)) s1_345
        from paperX_single_minus_numerics import sg_block
        def pat_fn(omega, zbar):
            p = list(sg_pattern5(omega, zbar))
            p.append(sg_block(omega, zbar, (0, 1), (2, 3)))
            p.append(sg_block(omega, zbar, (0,), (2, 3, 4)))
            return tuple(p)
    else:
        def pat_fn(omega, zbar):
            return tuple(sg_pattern5(omega, zbar))

    rng = random.Random(131)
    pat_a = defaultdict(set)
    t0 = time.time()
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = pat_fn(omega, zbar)
        pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
    main_nondet = [p for p in pat_a if len(pat_a[p]) > 1]
    print(f"n=5 {'10 因子' if use_ext else '8 因子'} 主样本 40000 ({time.time()-t0:.0f}s): "
          f"模式 {len(pat_a)} 非决定 {len(main_nondet)}", flush=True)

    total = 0
    for sd in (77, 211, 331, 777, 555):
        rng = random.Random(sd)
        pat2 = defaultdict(set)
        bad = 0
        t0 = time.time()
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            pat = pat_fn(omega, zbar)
            pat2[pat].add(round(A_BG(n, omega, zbar), 6))
        for p, vals in pat2.items():
            if len(vals) > 1:
                bad += 1
            if p in pat_a and not vals <= pat_a[p]:
                bad += 1
        total += bad
        print(f"seed {sd}: 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    print(f"n=5 {'10' if use_ext else '8'} 因子总计冲突 {total} -> {'PASS' if total == 0 else 'FAIL'}", flush=True)
    return {"n": 5, "use_ext": use_ext, "n_factors": 10 if use_ext else 8,
            "main_samples": 40000, "main_nondet": len(main_nondet),
            "total_violations": total, "pass": total == 0}


if __name__ == "__main__":
    res = audit(False)
    if not res["pass"]:
        print("8 因子 FAIL → 补扩展 10 因子重验", flush=True)
        res2 = audit(True)
        res["ext_result"] = res2
    with open(os.path.join(SCRIPT_DIR, "paperX_n5_crossset_audit.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
