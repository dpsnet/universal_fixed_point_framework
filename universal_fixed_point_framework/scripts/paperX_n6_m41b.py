# -*- coding: utf-8 -*-
"""M41b：n=6 35 因子全补污染检查（M37 结论稳健性）
- 35 相邻区间中全补块（a∪b = 全 6）——动量恒等 0
- 删除全补 → 冲突（浮点 vs 阈值化）
"""
import os, sys, random, json
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_single_minus_numerics import sg, sg_block, A6


def adj_factors_names(n):
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                A = "".join(str(x + 1) for x in range(i, k + 1))
                B = "".join(str(x + 1) for x in range(k + 1, j + 1))
                names.append(("s%s_%s" % (A, B), (tuple(range(i, k + 1)), tuple(range(k + 1, j + 1)))))
    return names


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len({sg(v) for v in vals}) > 1)


if __name__ == "__main__":
    n = 6
    names35 = adj_factors_names(n)
    fullset = set(range(n))
    fc = [(nm, ab) for nm, ab in names35 if set(ab[0]) | set(ab[1]) == fullset]
    print(f"n=6 35 因子中全补块：{len(fc)} -> {[nm for nm, _ in fc]}")

    N = 100000
    rng = random.Random(20261006)
    samples = []
    for _ in range(N):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        vals = [sg_block(omega, zbar, a, b) for a, b in [ab for _, ab in names35]]
        samples.append((tuple(vals), A6(omega, zbar)))
    print(f"采样 {N}")

    # 35 全因子冲突
    pat = defaultdict(list)
    for facs, a in samples:
        pat[facs].append(a)
    c35 = conflict_count(pat)
    print(f"35 因子冲突：{c35}")

    # 删全补（30 真实）
    fc_idx = {names35.index((nm, ab)) for nm, ab in fc}
    idx30 = [i for i in range(35) if i not in fc_idx]
    pat30 = defaultdict(list)
    for facs, a in samples:
        pat30[tuple(facs[i] for i in idx30)].append(a)
    c30 = conflict_count(pat30)
    print(f"30 因子（删 5 全补）冲突：{c30}")

    # 全补清零 + 删（等价——删了就不在分组里——30 因子冲突就是答案）
    out = {"n": n, "fullcomp": [nm for nm, _ in fc], "c35": c35, "c30": c30}
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_m41b_fullcomp.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n6_m41b_fullcomp.json")
