# -*- coding: utf-8 -*-
"""n=11 M3：补因子计算 + 跨集复验
1. 采样 20000（seed 131）：基座非决定模式 → (full, bg) 记录
2. 每模式 min_sets：全集因子中模式内决定性最小集（贪心加因子）
3. 补因子 = union(min_sets) - 基座
4. 跨集审计（基座 + 补因子）：主 20000 + 5 seed × 5000 → 0 冲突 PASS
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
    """records: [(full_vec, bg)]；cols: 因子索引子集；模式内决定性？"""
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
    mb = json.load(open(SCRIPT_DIR + "/paperX_n11_minbasis_results.json", encoding="utf-8"))
    base_names = mb["remove_set"]
    base_idx = [NAMES.index(x) for x in base_names]
    base_set = set(base_idx)

    # 1. 主表采样
    rng = random.Random(131)
    rec = defaultdict(list)
    t0 = time.time()
    for _ in range(20000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        pat = tuple(full[i] for i in base_idx)
        bg = round(A_BG(n, omega, zbar), 6)
        if len(rec[pat]) < 6:
            rec[pat].append((full, bg))
    print(f"主表 20000 ({time.time()-t0:.0f}s)", flush=True)

    base_nondet = [p for p, rs in rec.items() if len(set(r[1] for r in rs)) > 1]
    print(f"基座非决定模式: {len(base_nondet)}", flush=True)

    # 2. 每模式 min_sets（全集贪心加因子）
    min_sets = {}
    used = set()
    for p in base_nondet:
        rs = rec[p]
        chosen = []
        while not sufficient(rs, chosen):
            best = None
            best_score = -1
            for i in range(len(factors)):
                if i in chosen:
                    continue
                trial = chosen + [i]
                # 分数 = 模式内区分出的 bg 对数增量（贪心启发）
                seen = {}
                score = 0
                for full, bg in rs:
                    key = tuple(full[j] for j in trial)
                    if key in seen:
                        if abs(seen[key] - bg) > 1e-6:
                            score += 1000
                    else:
                        seen[key] = bg
                if score > best_score:
                    best_score = score
                    best = i
            chosen.append(best)
        min_sets[tuple(p)] = chosen
        used.update(chosen)
        print(f"  模式非决定补充因子 {len(chosen)} 个", flush=True)

    extra = [i for i in sorted(used - base_set)]
    print(f"补因子（超出基座 {len(extra)} 个）: {[NAMES[i] for i in extra]}", flush=True)
    full_base = base_idx + extra

    # 3. 跨集审计（基座 + 补因子）
    def audit(seed, ns):
        rng = random.Random(seed)
        pat2 = defaultdict(set)
        for _ in range(ns):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
            pat = tuple(full[i] for i in full_base)
            pat2[pat].add(round(A_BG(n, omega, zbar), 6))
        return sum(1 for v in pat2.values() if len(v) > 1)

    bad = audit(131, 20000)
    print(f"主样本 20000 冲突: {bad}", flush=True)
    total = bad
    for sd in (77, 211, 331, 777, 555):
        b = audit(sd, 5000)
        total += b
        print(f"seed {sd}: 冲突 {b} ({time.time()-t_start:.0f}s)", flush=True)
    print(f"总计冲突 {total} -> {'PASS' if total == 0 else 'FAIL'}", flush=True)

    res = {"n": n, "base_size": len(base_idx), "base_set": base_names,
           "extra_size": len(extra), "extra_set": [NAMES[i] for i in extra],
           "closed_size": len(full_base),
           "nondet_pats": len(base_nondet),
           "min_sets_sizes": {str(p): len(c) for p, c in min_sets.items()},
           "total_violations": total, "pass": total == 0,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_closed.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_closed.json")
