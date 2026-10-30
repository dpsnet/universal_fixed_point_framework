# -*- coding: utf-8 -*-
"""n=11 M4：48 基座 + 补因子近似闭合（Phase 77 登记项）
- 采样 seed 131 × 20000（48 基座投影）→ 非决定模式（预期 4）
- 冲突对区分迭代补因子（close2 方法）
- 验证：131 同缓存 0 非决定 + 5 seed × 5000 跨集复核
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear


def adj_partition_factors(n):
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                names.append((a, b))
    return names


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def sufficient(records, cols):
    seen = {}
    for full, bg in records:
        key = tuple(full[i] for i in cols)
        if key in seen and abs(seen[key] - bg) > 1e-6:
            return False
        seen[key] = bg
    return True


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    cg = json.load(open(SCRIPT_DIR + "/paperX_n11_crossset_greedy.json", encoding="utf-8"))
    base_names = cg["remove_set"]
    base_idx = [NAMES.index(x) for x in base_names]
    base_set = set(base_idx)
    print(f"n=11 跨集贪心基座 {len(base_idx)} 因子", flush=True)

    # 采样 131 × 20000（累积记录）
    rng = random.Random(131)
    rec = defaultdict(list)
    t0 = time.time()
    for _ in range(20000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        pat = tuple(full[i] for i in base_idx)
        bg = round(A_BG(n, omega, zbar), 6)
        if len(rec[pat]) < 10:
            rec[pat].append((full, bg))
    print(f"采样 20000 ({time.time()-t0:.0f}s)", flush=True)

    nondet = [p for p, rs in rec.items() if len(set(r[1] for r in rs)) > 1]
    print(f"基座非决定模式: {len(nondet)}", flush=True)

    # 补因子（冲突对区分迭代）
    extra = set()
    details = {}
    for p in nondet:
        rs = rec[p]
        D = set()
        while not sufficient(rs, sorted(D)):
            pair = None
            for a in range(len(rs)):
                for b in range(a + 1, len(rs)):
                    fa, ba = rs[a]
                    fb, bb = rs[b]
                    if abs(ba - bb) > 1e-6:
                        key_a = tuple(fa[i] for i in sorted(D))
                        key_b = tuple(fb[i] for i in sorted(D))
                        if key_a == key_b:
                            pair = (fa, fb)
                            break
                if pair:
                    break
            if pair is None:
                break
            fa, fb = pair
            add = [i for i in range(len(factors)) if abs(fa[i] - fb[i]) > 1e-6]
            D.update(add)
        extra.update(D - base_set)
        details[tuple(p)] = sorted(D - base_set)
        print(f"  模式补因子 {len(D)} 个（额外 {len(D - base_set)}）", flush=True)

    extra_list = sorted(extra)
    print(f"补因子（超出跨集贪心基座 {len(extra_list)} 个）: {[NAMES[i] for i in extra_list]}", flush=True)
    closed = base_idx + extra_list
    print(f"近似闭合基座规模: {len(closed)}", flush=True)

    # 验证 1：131 同缓存
    def nondet_on(data_samples, idx):
        pat_a = defaultdict(set)
        for full, a in data_samples:
            pat = tuple(full[i] for i in idx)
            pat_a[pat].add(a)
        return sum(1 for v in pat_a.values() if len(v) > 1)

    data_131 = []
    rng = random.Random(131)
    for _ in range(20000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        data_131.append((full, round(A_BG(n, omega, zbar), 6)))
    nd = nondet_on(data_131, closed)
    print(f"131 同缓存 20000 复核: 非决定 {nd} -> {'PASS' if nd == 0 else 'FAIL'}", flush=True)

    # 验证 2：5 seed × 5000 跨集
    total = 0
    for sd in (77, 211, 331, 777, 555):
        rng = random.Random(sd)
        pat2 = defaultdict(set)
        t0 = time.time()
        for _ in range(5000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
            pat = tuple(full[i] for i in closed)
            pat2[pat].add(round(A_BG(n, omega, zbar), 6))
        bad = sum(1 for v in pat2.values() if len(v) > 1)
        total += bad
        print(f"seed {sd} × 5000: 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    print(f"5 seed × 5000 总计冲突 {total} -> {'PASS' if total == 0 else 'FAIL'}", flush=True)

    res = {"n": n, "base_type": "crossset_greedy_48", "base_size": len(base_idx),
           "extra_size": len(extra_list), "extra_set": [NAMES[i] for i in extra_list],
           "closed_size": len(closed),
           "per_pat_extra": {str(p): [NAMES[i] for i in c] for p, c in details.items()},
           "verify_131_nondet": nd, "verify_crossset_total": total,
           "approx_pass": nd == 0 and total == 0,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_approx_closed.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_approx_closed.json")
