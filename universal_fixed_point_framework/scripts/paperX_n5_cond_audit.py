# -*- coding: utf-8 -*-
"""n=5 模式条件判据跨集审计（统一标准：40000 主 + 5 seed × 15000）
判据：sg_pattern5 8 因子基模式 + 16 非决定模式各配 min_sets 扩展因子（重叠块对 sg_block）
检验：同 (pat, min_sets 向量) → A_BG 单值（主表 + 跨集）
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

if __name__ == "__main__":
    n = 5
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    m = json.load(open(base + "paperX_n5_minimal_results.json", encoding="utf-8"))
    min_sets = {eval(k): v for k, v in m["min_sets"].items()}
    ext_labels = m["ext_labels"]
    nondet = set(min_sets.keys())
    print(f"n=5 模式条件判据: 非决定模式 {len(nondet)}，扩展因子 {len(ext_labels)}", flush=True)

    def ext_vec(omega, zbar):
        n = len(omega)
        labels = []
        for i in range(n):
            for j in range(i + 1, n + 1):
                labels.append((i + 1, j))
        out = []
        for a in labels:
            for b in labels:
                ia, ja = a
                ib, jb = b
                if ja <= ib or jb <= ia:
                    continue
                out.append(sg_block(omega, zbar, tuple(range(ia - 1, ja - 1)), tuple(range(ib - 1, jb - 1))))
        return out

    # 映射 ext_labels → 列索引（label 顺序与 all_ext_sgs 一致）
    labels = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            labels.append((i + 1, j))
    lab2idx = {lab: k for k, lab in enumerate(labels)}
    ext_pairs = []
    for a in labels:
        for b in labels:
            ia, ja = a
            ib, jb = b
            if ja <= ib or jb <= ia:
                continue
            ext_pairs.append((a, b))

    def criterion(omega, zbar, ext):
        pat = tuple(sg_pattern5(omega, zbar))
        if pat not in nondet:
            return (pat,), None
        cols = min_sets[pat]
        vec = tuple(ext[c] for c in cols)
        return (pat,), vec

    rng = random.Random(131)
    pat_a = defaultdict(set)
    t0 = time.time()
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        key, vec = criterion(omega, zbar, ext_vec(omega, zbar))
        pat = (key[0], vec) if vec is not None else (key[0], None)
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
            key, vec = criterion(omega, zbar, ext_vec(omega, zbar))
            pat = (key[0], vec) if vec is not None else (key[0], None)
            pat2[pat].add(round(A_BG(n, omega, zbar), 6))
        for p, vals in pat2.items():
            if len(vals) > 1:
                bad += 1
            if p in pat_a and not vals <= pat_a[p]:
                bad += 1
        total += bad
        print(f"seed {sd}: 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    print(f"n=5 模式条件判据总计冲突 {total} -> {'PASS' if total == 0 else 'FAIL'}", flush=True)

    res = {"n": 5, "type": "pattern_conditional", "nondet": len(nondet),
           "main_samples": 40000, "main_nondet": len(main_nondet),
           "total_violations": total, "pass": total == 0}
    with open(os.path.join(SCRIPT_DIR, "paperX_n5_crossset_audit.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
