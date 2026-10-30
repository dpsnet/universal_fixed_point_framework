# -*- coding: utf-8 -*-
"""M28：跨 seed 合并口径补跨区间因子——8 冲突归零检验
- 采样 3 seed × 80000（与 M18 一致：77/331/777）
- 每样本：50 基座 + 9 跨区间对（s_{k,1}, k=2..10）+ A_BG
- 合并口径冲突：50 基座 vs 50+9 基座——若 50+9 归零 → 判据完备性定理跨区间补全
"""
import os, json, sys, random, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_single_minus_bg_recursion import A_BG
from paperX_single_minus_numerics import sg_block


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def fast_basis_and_cross(omega, zbar, basis50):
    n = len(omega)
    P = [[0.0] * n for _ in range(n)]
    for i in range(n):
        wi = omega[i]
        zi = zbar[i]
        for j in range(i + 1, n):
            v = wi * omega[j] * (zi - zbar[j])
            P[i][j] = v
            P[j][i] = -v
    vals = []
    for b in basis50:
        a_part, bb_part = b.split("_")
        A = tuple(int(c) - 1 for c in a_part[1:])
        B = tuple(int(c) - 1 for c in bb_part)
        v = 0.0
        for i in A:
            row = P[i]
            for j in B:
                v += row[j]
        vals.append(sg(v))
    cross = tuple(sg(P[k - 1][0]) for k in range(2, n))
    return tuple(vals), cross


if __name__ == "__main__":
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])

    N_PER = 80000
    seeds = [77, 331, 777]
    pat50_a = defaultdict(list)   # 50 基座模式 -> A 值
    pat59_a = defaultdict(list)   # 50+9 跨区间 -> A 值
    t0 = time.time()
    for sd in seeds:
        rng = random.Random(sd)
        cnt = 0
        while cnt < N_PER:
            omega, zbar, _ = gen_partial_collinear(11, 0, rng=rng, r1=True, momentum=True)
            k50, cross = fast_basis_and_cross(omega, zbar, basis50)
            a = A_BG(11, omega, zbar)
            pat50_a[k50].append(a)
            pat59_a[k50 + cross].append(a)
            cnt += 1
        print(f"seed {sd} done（{time.time()-t0:.0f}s）")

    def conflict(pats):
        tot = 0
        c = 0
        for p, vals in pats.items():
            syms = {sg(v) for v in vals}
            tot += len(vals)
            if len(syms) > 1:
                c += 1
        return c, tot

    c50, t50 = conflict(pat50_a)
    c59, t59 = conflict(pat59_a)
    print(f"\n50 基座：冲突模式 {c50} / 样本 {t50}（率 {c50/t50:.3e}）")
    print(f"50+9 跨区间：冲突模式 {c59} / 样本 {t59}（率 {c59/t59:.3e}）")

    # 冲突样本明细（59 因子下若仍有冲突——列出跨区间分裂情况）
    if c59 > 0:
        print("\n59 因子冲突模式（前 5 个）:")
        shown = 0
        for p, vals in pat59_a.items():
            syms = {sg(v) for v in vals}
            if len(syms) > 1:
                print(" ", p, sorted(syms))
                shown += 1
                if shown >= 5:
                    break

    out = {"c50": c50, "t50": t50, "c59": c59, "t59": t59,
           "n_patterns_50": len(pat50_a), "n_patterns_59": len(pat59_a)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m28_crossset.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m28_crossset.json")
