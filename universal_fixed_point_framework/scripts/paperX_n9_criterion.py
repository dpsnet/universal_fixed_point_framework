# -*- coding: utf-8 -*-
"""n=9 判据外推画像：相邻区间二元分割全集（120 因子）→ 是否决定 A_BG。
目的：验证"判据阶数随 n 增长"（+4/级）在 n=9 是否持续：n=6 12、n=7 16、n=8 20+3、n=9 ?
- 全集决定性 0 非决定 → 逗号块和记号在 n=9 仍完备 → 检验最小充分基座规模
- 若 >0 → 记号不完备（罕见退化区分缺失）
"""
import json, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear


def adj_partition_factors(n):
    """逗号块和记号的相邻区间二元分割全集（0-based）。"""
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                names.append((a, b))
    return names


def sg_pattern9(omega, zbar, factors):
    return tuple(sg_block(omega, zbar, a, b) for a, b in factors)


def scan(n_samples=15000, seed=23, n=9):
    factors = adj_partition_factors(n)
    print(f"n={n} 相邻区间二元分割因子数: {len(factors)}", flush=True)
    rng = random.Random(seed)
    pat_a_bg = defaultdict(set)
    pat_cnt = Counter()
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern9(omega, zbar, factors)
        pat_cnt[pat] += 1
        pat_a_bg[pat].add(round(A_BG(n, omega, zbar), 6))
    dt = time.time() - t0
    nondet = [p for p in pat_cnt if len(pat_a_bg[p]) > 1]
    det = [p for p in pat_cnt if len(pat_a_bg[p]) == 1]
    print(f"样本 {n_samples} ({dt:.0f}s): 模式 {len(pat_cnt)}  决定性 {len(det)} / 非决定性 {len(nondet)}", flush=True)
    nz = Counter()
    for p in nondet:
        nz[tuple(sorted(v for v in pat_a_bg[p] if abs(v) > 1e-9))] += 1
    print(f"非零取值形态: {dict(nz)}")
    if nondet:
        for p in list(nondet)[:3]:
            print(f"  示例非决定模式取值 {sorted(pat_a_bg[p])}: 频次 {pat_cnt[p]}")
    res = {"n": n, "factors": len(factors), "samples": n_samples,
           "total": len(pat_cnt), "det": len(det), "nondet": len(nondet),
           "valcount_dist": dict(Counter(len(pat_a_bg[p]) for p in nondet)),
           "nonzero_sets": {str(k): v for k, v in nz.items()}}
    with open(os.path.join(SCRIPT_DIR, "paperX_n9_criterion_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n9_criterion_results.json")
    return factors, pat_cnt, pat_a_bg, res


if __name__ == "__main__":
    scan()
