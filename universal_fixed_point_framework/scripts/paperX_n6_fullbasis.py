# -*- coding: utf-8 -*-
"""n=6 基座对比：12 因子推广基座 vs (32) 公式全集 20 因子基座。
若 (32) 全集基座下非决定性模式显著减少 → 正确基座应含 (32) 全部因子，
判据最小化问题重构（类似 n=5：8sg = (31) 因子全集恰好最小）。
"""
import json, os, random, sys
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_pair, sg_block, A6
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear


def sg_pattern6_full(omega, zbar):
    """(32) 公式全集 20 因子（0-based；变量名=1-based 块名）"""
    w, z = omega, zbar
    return (
        sg_block(w, z, (0,), (1, 2)),        # s1_23
        sg_block(w, z, (0, 1), (2,)),        # s12_3
        sg_block(w, z, (0, 1, 2), (3,)),     # s123_4
        sg_pair(w, z, 4, 5),                 # s56
        sg_pair(w, z, 1, 2),                 # s23
        sg_block(w, z, (0,), (1, 2, 3)),     # s1_234
        sg_block(w, z, (0, 1), (2, 3)),      # s12_34
        sg_pair(w, z, 2, 3),                 # s34
        sg_block(w, z, (1,), (2, 3)),        # s2_34
        sg_block(w, z, (1, 2), (3,)),        # s23_4
        sg_pair(w, z, 0, 1),                 # s12
        sg_block(w, z, (2, 3, 4), (5,)),     # s345_6
        sg_block(w, z, (3, 4), (5,)),        # s45_6
        sg_pair(w, z, 3, 4),                 # s45
        sg_block(w, z, (2,), (3, 4)),        # s3_45
        sg_block(w, z, (2, 3), (4,)),        # s34_5
        sg_block(w, z, (1, 2, 3), (4,)),     # s234_5
        sg_block(w, z, (5,), (0,)),          # s61
        sg_block(w, z, (1,), (2, 3, 4)),     # s2_345
        sg_block(w, z, (1, 2), (3, 4)),      # s23_45
    )


def scan(n_samples=40000, seed=23):
    rng = random.Random(seed)
    pat_a_bg = defaultdict(set)
    pat_cnt = Counter()
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern6_full(omega, zbar)
        pat_cnt[pat] += 1
        pat_a_bg[pat].add(round(A_BG(6, omega, zbar), 6))
    nondet = [p for p in pat_cnt if len(pat_a_bg[p]) > 1]
    det = [p for p in pat_cnt if len(pat_a_bg[p]) == 1]
    print(f"样本 {n_samples}: 模式 {len(pat_cnt)}  决定性 {len(det)} / 非决定性 {len(nondet)}")
    vc = Counter(len(pat_a_bg[p]) for p in nondet)
    print(f"非决定性按取值数: {dict(vc)}")
    # 无法用 0/±1 二分？检查非零值集合
    nz = Counter()
    for p in nondet:
        nz[tuple(sorted(v for v in pat_a_bg[p] if abs(v) > 1e-9))] += 1
    print(f"非零取值形态: {dict(nz)}")
    # 关键：12 基座非决定性 vs 20 基座非决定性的交集结构——记录两种模式键
    res = {"samples": n_samples, "total": len(pat_cnt), "det": len(det), "nondet": len(nondet),
           "valcount_dist": dict(vc), "nonzero_sets": {str(k): v for k, v in nz.items()}}
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_fullbasis_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")


if __name__ == "__main__":
    scan()
