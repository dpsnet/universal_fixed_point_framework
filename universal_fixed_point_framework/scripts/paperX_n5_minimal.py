# paperX_n5_minimal.py
# Phase 72 阶段2 深化：
# 1. 最小决定性扩展因子集（贪心：逐模式找最少扩展因子区分 0/±1；全局找覆盖集）
# 2. 大样本验证：8 个 (31) sg + 最小扩展集合并后，52 模式全决定性，0 违反
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_block
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


def all_ext_sgs(omega, zbar):
    """全部连续块 vs 连续块（不交）块和序 sg，带标签"""
    n = len(omega)
    # 连续块 [i..j) 1-based 标签
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
            va = sg_block(omega, zbar, tuple(range(ia - 1, ja - 1)), tuple(range(ib - 1, jb - 1)))
            out.append(((a, b), va))
    return out


def collect(seed=11, n_samples=300000):
    """在 16 模式内收集：每个模式内 (扩展因子向量) -> A_BG 是否零"""
    rng = random.Random(seed)
    per_pat = defaultdict(list)   # 模式 -> [(extvec, is_zero)]
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in NONDET_SET:
            continue
        ext = tuple(v for _, v in all_ext_sgs(omega, zbar))
        a = A_BG(5, omega, zbar)
        per_pat[pat].append((ext, a == 0.0))
    return per_pat


def min_per_pat(per_pat):
    """逐模式最小区分：找最少扩展因子（列索引）使 0/非零 完全分离"""
    # 先算每模式的扩展因子全列表（顺序固定）
    # 用全样本推断：对每个因子列，检查是否单独区分；否则贪心加列
    result = {}
    for pat, rows in per_pat.items():
        n_cols = len(rows[0][0])
        zero_mask = [r[1] for r in rows]
        # 贪心：逐步加入区分能力最强的列
        chosen = []
        remaining = set(range(n_cols))
        # 判定函数：当前列集下 0/非零样本的向量是否不交
        def separates(cols):
            zvec = set()
            nvec = set()
            for ext, isz in rows:
                v = tuple(ext[c] for c in cols)
                if isz:
                    zvec.add(v)
                else:
                    nvec.add(v)
            return zvec.isdisjoint(nvec)
        if separates([]):
            result[pat] = []
            continue
        # 贪心添加
        while remaining and not separates(chosen):
            best = None
            for c in sorted(remaining):
                if separates(chosen + [c]):
                    best = c
                    break
            if best is None:
                # 无单列能立即闭合，选信息增益最大的列
                best = max(remaining, key=lambda c: _gain(rows, chosen + [c]))
            chosen.append(best)
            remaining.discard(best)
            if len(chosen) >= len(rows[0][0]):
                break
        result[pat] = chosen
    return result


def _gain(rows, cols):
    """信息增益近似：按当前列集分桶后，桶内 0/非零 熵"""
    from math import log2
    buckets = defaultdict(lambda: [0, 0])
    for ext, isz in rows:
        v = tuple(ext[c] for c in cols)
        buckets[v][0 if isz else 1] += 1
    H = 0.0
    for z, nz in buckets.values():
        t = z + nz
        if z and nz:
            p = z / t
            H += t * (p * log2(p) + (1 - p) * log2(1 - p))
    return -H


def verify(min_sets, n_samples=40000, seed=13):
    """大样本验证：8 个 (31) sg + 最小扩展集 -> 所有模式（52）内 A_BG 决定性，0 违反"""
    rng = random.Random(seed)
    ext_labels = None
    total = 0
    per_pat_vals = defaultdict(set)
    # 困难模式零值分析：扩展因子含 0（块和为零）的占比
    zero_sig_stats = defaultdict(lambda: [0, 0])  # 模式 -> [含0样本, 总样本]
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        exts = all_ext_sgs(omega, zbar)
        if ext_labels is None:
            ext_labels = [lab for lab, _ in exts]
        cols = min_sets.get(pat, [])
        key = pat + tuple(exts[c][1] for c in cols)
        a = A_BG(5, omega, zbar)
        per_pat_vals[key].add(round(a, 6))
        if pat in NONDET_SET:
            zero_sig_stats[pat][1] += 1
            if any(v == 0 for _, v in exts):
                zero_sig_stats[pat][0] += 1
        total += 1
    nondet = {k: v for k, v in per_pat_vals.items() if len(v) > 1}
    return len(nondet), total, nondet, ext_labels, zero_sig_stats


def main():
    print("收集样本...", flush=True)
    per_pat = collect()
    print(f"模式样本覆盖: {len(per_pat)}/16")
    print("逐模式最小区分因子集...", flush=True)
    min_sets = min_per_pat(per_pat)
    n_used = {}
    for pat, cols in min_sets.items():
        print(f"  pat={pat}: 需 {len(cols)} 个扩展因子 (列索引 {cols})")
        n_used[len(cols)] = n_used.get(len(cols), 0) + 1
    print(f"扩展因子数量分布: {dict(sorted(n_used.items()))}")
    # 全局最小覆盖：不同模式是否需要不同列？找全局使用列集合
    all_cols = set()
    for cols in min_sets.values():
        all_cols |= set(cols)
    print(f"全局使用的扩展因子列总数: {len(all_cols)}")
    print("大样本验证...", flush=True)
    nondet_count, total, nondet, ext_labels, zstats = verify(min_sets)
    print(f"验证: {total} 样本, 扩展后非决定性模式 {nondet_count} 个 (应为 0)")
    if nondet_count:
        for k, v in list(nondet.items())[:5]:
            print(f"  反例: 模式 {k[:8]} 扩展列值 {k[8:]} -> A_BG 取值 {v}")
    print("困难模式零值占比（扩展因子含 0 的样本比例）:")
    for pat, (z, t) in sorted(zstats.items()):
        flag = " [困难]" if pat in ((1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)) else ""
        print(f"  pat={pat}: 含零 {z}/{t} = {z/t:.3f}{flag}")
    res = {
        "min_sets": {str(pat): cols for pat, cols in min_sets.items()},
        "used_columns_total": len(set(c for cols in min_sets.values() for c in cols)),
        "ext_labels": ext_labels,
        "verify_samples": total,
        "nondet_after_extension": nondet_count,
        "violations": {str(k): sorted(v) for k, v in list(nondet.items())[:5]},
        "zero_sig_stats": {str(pat): [z, t] for pat, (z, t) in zstats.items()},
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_minimal_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n5_minimal_results.json")


if __name__ == "__main__":
    main()
