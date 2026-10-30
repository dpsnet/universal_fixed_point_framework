# -*- coding: utf-8 -*-
"""M58：因子独立性分析——括号值层线性秩 vs 谱维数 26
- 假设 H1：谱维数 = 括号值层独立因子数（线性依赖秩）
- 对样本计算 220 因子括号值的数值矩阵 rank（zbar 线性形式）
- 检验 rank vs 26（预期 rank ≤ n-2 —— 动量约束后 zbar 自由度）
"""
import os, sys, json, pickle, random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors
from paperX_degenerate_family_scan import gen_partial_collinear


def matrix_rank(rows, tol=1e-8):
    """纯 Python 高斯消元求秩"""
    m = [list(r) for r in rows]
    nrows = len(m)
    ncols = len(m[0]) if nrows else 0
    rank = 0
    for col in range(ncols):
        # 找主元
        pivot = None
        for r in range(rank, nrows):
            if abs(m[r][col]) > tol:
                pivot = r
                break
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        pv = m[rank][col]
        for c in range(col, ncols):
            m[rank][c] /= pv
        for r in range(nrows):
            if r != rank and abs(m[r][col]) > tol:
                f = m[r][col]
                for c in range(col, ncols):
                    m[r][c] -= f * m[rank][c]
        rank += 1
        if rank >= nrows:
            break
    return rank


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)

    ranks = []
    n_samples = 200
    rng = random.Random(20261008)
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        M = []
        for a, b in factors:
            SA = sum(omega[x] for x in a)
            SB = sum(omega[y] for y in b)
            row = []
            for i in range(n):
                c = 0.0
                if i in a:
                    c += SB
                if i in b:
                    c -= SA
                row.append(omega[i] * c)
            M.append(row)
        ranks.append(matrix_rank(M, tol=1e-8))

    import collections
    dist = collections.Counter(ranks)
    print(f"括号值层秩（{n_samples} 样本）：min={min(ranks)} max={max(ranks)} dist={dict(dist)}", flush=True)
    print(f"n={n}（动量约束后 zbar 自由度 ≤ {n-2}）——谱维数 26 远超线性秩——H1 检验：", flush=True)
    h1 = all(r < 26 for r in ranks)
    print(f"H1（谱维数 = 线性秩）{'证伪' if h1 else '部分成立'}", flush=True)

    out = {"n": n, "n_samples": n_samples, "ranks_dist": dict(dist),
           "min_rank": min(ranks), "max_rank": max(ranks),
           "spectral_dim": 26, "h1_rejected": h1}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m58_rank.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("DONE -> paperX_n11_m58_rank.json", flush=True)
