# -*- coding: utf-8 -*-
"""n=11 M3 v2：补因子计算（冲突对区分迭代）+ 跨集复验
每非决定模式：
  1. 取记录对（bg 不同）→ 区分因子集 D = {i: |f_a[i]-f_b[i]|>1e-6}
  2. 检查 D 是否模式内充分（sufficient 所有记录）——不足则取未区分对补 D
  3. 补因子 = union(D) - 基座
然后：跨集审计（基座 + 补因子）0 冲突 PASS
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
    mb = json.load(open(SCRIPT_DIR + "/paperX_n11_minbasis_results.json", encoding="utf-8"))
    base_names = mb["remove_set"]
    base_idx = [NAMES.index(x) for x in base_names]
    base_set = set(base_idx)

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
    print(f"主表 20000 ({time.time()-t0:.0f}s)", flush=True)

    base_nondet = [p for p, rs in rec.items() if len(set(r[1] for r in rs)) > 1]
    print(f"基座非决定模式: {len(base_nondet)}", flush=True)

    extra = set()
    details = {}
    for p in base_nondet:
        rs = rec[p]
        D = set()
        # 迭代：取未区分对补区分因子
        while not sufficient(rs, sorted(D)):
            # 找 D 投影下键相同但 bg 不同的记录对
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
                break  # 所有 bg 不同对已被 D 区分（sufficient 判定应已 True）
            fa, fb = pair
            add = [i for i in range(len(factors)) if abs(fa[i] - fb[i]) > 1e-6]
            D.update(add)
        extra.update(D - base_set)
        details[tuple(p)] = sorted(D)
        print(f"  模式补因子 {len(D)} 个（额外 {len(D - base_set)}）", flush=True)

    extra_list = sorted(extra)
    print(f"补因子（超出基座 {len(extra_list)} 个）: {[NAMES[i] for i in extra_list]}", flush=True)
    full_base = base_idx + extra_list

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
           "extra_size": len(extra_list), "extra_set": [NAMES[i] for i in extra_list],
           "closed_size": len(full_base), "nondet_pats": len(base_nondet),
           "per_pat_extra": {str(p): [NAMES[i] for i in sorted(d) - base_set] for p, d in details.items()},
           "total_violations": total, "pass": total == 0,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_closed.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_closed.json")
