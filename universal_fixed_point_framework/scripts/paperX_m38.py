# -*- coding: utf-8 -*-
"""M38：跨 n 动量双守恒括号恒等式普适性验证（n=6..11）
- 恒等式 A：Σ_{j≠k} P[k][j] = 0（任何粒子 k 作锚）——Σω=0 + Σωz=0 导出
- 恒等式 B：跨区间单对展开 s_{k,1} = -Σ_{j≠k,1} s_{kj}（锚粒子 1）
- 与 A_BG 无关——只需 P 矩阵——2000 样本/n——快
"""
import os, sys, random, time, json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_degenerate_family_scan import gen_partial_collinear


def P_matrix(omega, zbar):
    n = len(omega)
    P = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            v = omega[i] * omega[j] * (zbar[i] - zbar[j])
            P[i][j] = v
            P[j][i] = -v
    return P


if __name__ == "__main__":
    N_PER_N = 2000
    rng = random.Random(20261006)
    results = {}
    for n in [6, 7, 8, 9, 10, 11]:
        badA = 0
        badB = 0
        totalA = 0
        for _ in range(N_PER_N):
            omega, zbar, pairs = gen_partial_collinear(n, 0, rng=rng, r1=True, momentum=True)
            P = P_matrix(omega, zbar)
            # A：任何 k 作锚全和 = 0
            for k in range(n):
                s = sum(P[k][j] for j in range(n) if j != k)
                if abs(s) > 1e-9:
                    badA += 1
                totalA += 1
            # B：跨区间单对 s_{k,1}（0-based k=1..n-2——1-based 2..n-1）= -Σ_{j≠k,1} s_{kj}
            for k in range(1, n - 1):
                lhs = P[k][0]
                rhs = sum(P[k][j] for j in range(1, n) if j != k)
                if abs(lhs + rhs) > 1e-9:
                    badB += 1
        results[n] = {"badA": badA, "totalA": totalA, "badB": badB}
        print(f"n={n}: 恒等式A（全锚和=0）偏差 {badA}/{totalA}；恒等式B（跨区间展开）偏差 {badB}/{N_PER_N*(n-2)}")
    with open(os.path.join(SCRIPT_DIR, "paperX_m38_crossn_identity.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_m38_crossn_identity.json")
