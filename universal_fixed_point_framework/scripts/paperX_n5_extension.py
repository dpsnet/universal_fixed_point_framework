# paperX_n5_extension.py
# Phase 72 阶段2：扩展因子检验——16 个非决定性模式内，能否用"累积块和序 sg"区分 A_BG=0 vs A_BG=±1
# 候选扩展因子（n=5 累积块对，递归树 Θ 因子的符号投影）：
#   C1 = sg([λ1, λ2+λ3+λ4+λ5])       (1|2345)
#   C2 = sg([λ1+λ2, λ3+λ4+λ5])       (12|345)
#   C3 = sg([λ1+λ2+λ3, λ4+λ5])       (123|45)
#   C4 = sg([λ1+λ2+λ3+λ4, λ5])       (1234|5)
# 检验：16 模式内 A_BG=0 与 A_BG!=0 是否被 (C1..C4) 完全区分（模式细分成决定性）
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_pair, sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

NONDET = [
    (-1, 1, -1, -1, -1, -1, 1, -1), (1, -1, 1, 1, 1, 1, -1, 1),
    (1, 1, -1, -1, -1, -1, 1, -1), (-1, -1, 1, 1, 1, 1, -1, 1),
    (-1, -1, 1, 1, -1, -1, -1, -1), (1, 1, -1, -1, 1, 1, 1, 1),
    (-1, -1, 1, 1, -1, 1, -1, -1), (1, 1, -1, -1, 1, -1, 1, 1),
    (1, 1, 1, 1, -1, -1, 1, -1), (-1, -1, -1, -1, 1, 1, -1, 1),
    (1, -1, -1, -1, 1, 1, -1, 1), (-1, -1, 1, 1, -1, -1, 1, -1),
    (-1, 1, 1, 1, -1, -1, 1, -1), (1, 1, -1, -1, 1, 1, -1, 1),
    (1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1),
]
NONDET_SET = set(NONDET)


def cum_blocks(omega, zbar):
    """累积块对 sg：C1..C4"""
    n = len(omega)
    out = []
    for m in range(1, n):  # m = 1..n-1  (1-based)
        A = tuple(range(m))          # 1..m
        B = tuple(range(m, n))       # m+1..n
        out.append(sg_block(omega, zbar, A, B))
    return tuple(out)


def ext_blocks(omega, zbar):
    """扩展：全部连续块 vs 连续块（非累积型补充）：如 [23] vs [45] 等内层块"""
    n = len(omega)
    blocks = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            blocks.append((i, j))  # 连续块 [i..j) 1-based: i+1..j
    out = []
    for ia, ja in blocks:
        for ib, jb in blocks:
            if ja <= ib or jb <= ia:  # 不交
                continue
            out.append(sg_block(omega, zbar, tuple(range(ia, ja)), tuple(range(ib, jb))))
    return tuple(out)


def scan(n_samples=200000, seed=7):
    rng = random.Random(seed)
    # 16 模式内：A_BG=0 vs !=0 的 (C1..C4, ext) 取值
    pat_zero = defaultdict(set)      # 模式 -> (cum, ext) 集合，A_BG==0
    pat_nz = defaultdict(set)        # 模式 -> (cum, ext) 集合，A_BG!=0
    pat_cum_zero = defaultdict(set)
    pat_cum_nz = defaultdict(set)
    hit = 0
    total = 0
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in NONDET_SET:
            continue
        total += 1
        a = A_BG(5, omega, zbar)
        cum = cum_blocks(omega, zbar)
        ext = ext_blocks(omega, zbar)
        if a == 0.0:
            pat_zero[pat].add((cum, ext))
            pat_cum_zero[pat].add(cum)
        else:
            pat_nz[pat].add((cum, ext))
            pat_cum_nz[pat].add(cum)
    # 判定：扩展因子能否完全区分（零集合与非零集合不交）
    sep_cum = 0
    sep_full = 0
    not_sep = []
    for p in NONDET:
        zc = pat_cum_zero.get(p, set())
        nc = pat_cum_nz.get(p, set())
        sep_cum += 1 if zc.isdisjoint(nc) else 0
        zf = pat_zero.get(p, set())
        nf = pat_nz.get(p, set())
        ok_full = zf.isdisjoint(nf)
        sep_full += 1 if ok_full else 0
        if not ok_full:
            not_sep.append((p, len(zf), len(nf)))
    print(f"非决定性模式样本: {total}")
    print(f"累积块对(C1..C4)区分: {sep_cum}/16")
    print(f"全扩展因子区分: {sep_full}/16")
    print(f"未区分模式(扩展因子集): {len(not_sep)}")
    for p, z, nz in not_sep[:10]:
        print(f"  pat={p} zero_sigs={z} nonzero_sigs={nz}")
    res = {
        "samples_total": total,
        "sep_cum": sep_cum,
        "sep_full": sep_full,
        "not_separated": [(list(p), z, nz) for p, z, nz in not_sep],
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_extension_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n5_extension_results.json")


if __name__ == "__main__":
    scan()
