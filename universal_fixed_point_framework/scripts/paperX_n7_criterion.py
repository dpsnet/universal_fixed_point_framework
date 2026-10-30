# -*- coding: utf-8 -*-
"""n=7 判据外推画像：逗号块和记号的相邻区间二元分割全集 → 是否决定 A_BG。
目的：验证"判据阶数随 n 增长"是否持续。
- n=5：(31) 首索引 8 因子 → 16/52 非决定性 → 需 2 扩展（块-块序缺失）
- n=6：(32) 逗号块和 20 因子 → 0 非决定性（天然完备，12 因子最小充分）
- n=7：无显式公式 (33)，外推相邻区间二元分割全集（57 因子）→ 非决定性？
  若 0 → 逗号块和记号在 n=7 仍完备 → 检验最小充分基座规模（阶数增长量化）
  若 >0 → 记号不完备 → 需更高阶因子（阶数增长的直接证据）
"""
import json, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_pair, sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear


def adj_partition_factors(n):
    """逗号块和记号的相邻区间二元分割全集（0-based）。
    对每个长度 >=2 的相邻区间 [i..j]，全部二元分割 [i..k]|[k+1..j]。
    返回因子名列表（含单对：区间长 2 只有一个分割）。
    """
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                names.append((a, b))
    return names


def sg_pattern7(omega, zbar, factors):
    w, z = omega, zbar
    return tuple(sg_block(w, z, a, b) for a, b in factors)


def scan(n_samples=30000, seed=23, n=7):
    factors = adj_partition_factors(n)
    print(f"n={n} 相邻区间二元分割因子数: {len(factors)}")
    rng = random.Random(seed)
    pat_a_bg = defaultdict(set)
    pat_cnt = Counter()
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern7(omega, zbar, factors)
        pat_cnt[pat] += 1
        pat_a_bg[pat].add(round(A_BG(n, omega, zbar), 6))
    dt = time.time() - t0
    nondet = [p for p in pat_cnt if len(pat_a_bg[p]) > 1]
    det = [p for p in pat_cnt if len(pat_a_bg[p]) == 1]
    print(f"样本 {n_samples} ({dt:.0f}s): 模式 {len(pat_cnt)}  决定性 {len(det)} / 非决定性 {len(nondet)}")
    nz = Counter()
    for p in nondet:
        nz[tuple(sorted(v for v in pat_a_bg[p] if abs(v) > 1e-9))] += 1
    print(f"非零取值形态: {dict(nz)}")
    if nondet:
        # 非决定性模式示例
        for p in nondet[:3]:
            print(f"  示例非决定模式取值 {sorted(pat_a_bg[p])}: 频次 {pat_cnt[p]}")
    res = {"n": n, "factors": len(factors), "samples": n_samples,
           "total": len(pat_cnt), "det": len(det), "nondet": len(nondet),
           "valcount_dist": dict(Counter(len(pat_a_bg[p]) for p in nondet)),
           "nonzero_sets": {str(k): v for k, v in nz.items()}}
    with open(os.path.join(SCRIPT_DIR, f"paperX_n7_criterion_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n7_criterion_results.json")
    return factors, pat_cnt, pat_a_bg, res


if __name__ == "__main__":
    scan()
