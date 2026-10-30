# -*- coding: utf-8 -*-
"""M28 旁路：n=6 判据 vs 判据+跨区间（A6 显式公式快速验证）
- 35 相邻区间因子（n=6 全判据空间）vs +9 跨区间单对（s_{k,1} k=2..5, s42/s52/s53/s62...）
- A6 显式公式（无 BG 递归——快）
- 检验：判据补跨区间后冲突是否归零（小 n 机制确认）
"""
import os, json, sys, random, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import gen_R1_momentum, EXPLICIT


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def adj_factors(omega, zbar):
    """35 相邻区间因子（n=6）：[i..k]|[k+1..j], i<j, k∈[i,j)"""
    n = len(omega)
    w = len(omega)
    P = [[0.0] * w for _ in range(w)]
    for i in range(w):
        wi = omega[i]
        zi = zbar[i]
        for j in range(i + 1, w):
            v = wi * omega[j] * (zi - zbar[j])
            P[i][j] = v
            P[j][i] = -v
    vals = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                A = tuple(range(i, k + 1))
                B = tuple(range(k + 1, j + 1))
                v = 0.0
                for x in A:
                    row = P[x]
                    for y in B:
                        v += row[y]
                vals.append(sg(v))
    # 跨区间单对（间隔 >1）：(k,1) k=2..5 + (4,2),(5,2),(5,3)
    cross = tuple(sg(P[k - 1][0]) for k in range(2, n)) + (sg(P[3][1]), sg(P[4][1]), sg(P[4][2]))
    return tuple(vals), cross


if __name__ == "__main__":
    N = 240000
    rng = random.Random(20261006)
    pat35 = defaultdict(list)
    pat44 = defaultdict(list)
    t0 = time.time()
    cnt = 0
    while cnt < N:
        omega, zbar = gen_R1_momentum(6, rng=rng)
        f35, cross = adj_factors(omega, zbar)
        a6 = EXPLICIT[6](omega, zbar)
        pat35[f35].append(a6)
        pat44[f35 + cross].append(a6)
        cnt += 1
    print(f"采样完成 {time.time()-t0:.0f}s")

    def conflict(pats):
        tot = 0
        c = 0
        for p, vals in pats.items():
            syms = {sg(v) for v in vals}
            tot += len(vals)
            if len(syms) > 1:
                c += 1
        return c, tot

    c35, t35 = conflict(pat35)
    c44, t44 = conflict(pat44)
    print(f"35 相邻区间：冲突模式 {c35} / 样本 {t35}（率 {c35/t35:.3e}）")
    print(f"35+9 跨区间：冲突模式 {c44} / 样本 {t44}（率 {c44/t44:.3e}）")

    # 若 35 有冲突——看跨区间在冲突样本中的分裂
    if c35 > 0:
        shown = 0
        for p, vals in pat35.items():
            if len({sg(v) for v in vals}) > 1:
                print("  35 冲突模式示例:", p, sorted({sg(v) for v in vals}))
                shown += 1
                if shown >= 3:
                    break

    out = {"c35": c35, "t35": t35, "c44": c44, "t44": t44,
           "n_patterns_35": len(pat35), "n_patterns_44": len(pat44)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_m28_crossset.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n6_m28_crossset.json")
