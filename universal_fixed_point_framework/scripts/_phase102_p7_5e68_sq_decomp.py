# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-68：束缚态数平方和分解——"2²+k² 主族"检验
================================================================
用户洞察：13 = 2²+3²、8 = 2²+2²、5 = 2²+1²——第一项固定 2²！
扩展：20 = 2²+4²（0.04 au 已有）——k = 4, 3, 2, 1 连续递减
检验：全部 17 点是否有短平方和分解（2-4 项、底数 ∈ 框架量集合）
主族候选：n = 2² + k²（k = 6?, 4, 3, 2, 1）
框架量集合：{1, 2, 3, 4, 5, 7, 8, 12, 13, 15, 16, ...}（k_max=8, N_gen=3, N_Weyl=4, 静默单元族）
"""
import json, os, itertools, math, io

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
d = json.load(io.open(os.path.join(BASE, "_gaia_abs", "paperX_eta_sc_B_bound.json"), encoding="utf-8"))
new = json.load(io.open(os.path.join(BASE, "_phase102_p7_5e66_bound_predict.json"), encoding="utf-8"))

pts = [(r["B_au"]*2350, r["n_bound"]) for r in d] + [(r["B_MG"], r["n_bound"]) for r in new]
pts.sort()

# 框架量集合（底数候选）：主框架量 + 静默单元 + 小整数组合
FRAME_BASES = [1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 15]

def sq_decomp(n, max_terms=4, bases=None):
    """寻找底数∈bases 的平方和分解，优先短分解"""
    if bases is None:
        bases = FRAME_BASES
    sqs = [(b, b*b) for b in bases if b*b <= n]
    best = None
    def rec(rem, terms, start):
        nonlocal best
        if best is not None and len(terms) >= len(best):
            return
        if rem == 0:
            best = list(terms)
            return
        if len(terms) >= max_terms:
            return
        for i in range(start, len(sqs)):
            b, s = sqs[i]
            if s <= rem:
                terms.append(b)
                rec(rem - s, terms, i)  # 允许重复底数
                terms.pop()
                if best is not None:
                    return
    rec(n, [], 0)
    return best

print("="*104)
print("P7-5e-68：束缚态数平方和分解——2²+k² 主族检验")
print("="*104)

print()
print("【主族检验：n = 2² + k²（k = 6, 4, 3, 2, 1 候选）】")
print("-"*104)
main_family = {}
for b, n in pts:
    k2 = n - 4
    if k2 >= 0 and int(math.sqrt(k2))**2 == k2:
        k = int(math.sqrt(k2))
        main_family[b] = (n, k)
        print("  B=%6.1f MG → n=%d = 2² + %d²（k=%d）★" % (b, n, k, k))
    else:
        print("  B=%6.1f MG → n=%d — 非 2²+k² 形式" % (b, n))

print()
print("【全部 17 点平方和分解（底数 ∈ 框架量集合，≤4 项）】")
print("-"*104)
for b, n in pts:
    dec = sq_decomp(n)
    if dec:
        s = " + ".join("%d²" % x for x in dec)
        print("  B=%6.1f MG → n=%d = %s  (%d 项)" % (b, n, s, len(dec)))
    else:
        print("  B=%6.1f MG → n=%d — 无框架底数平方和分解" % (b, n))

json.dump({"main_family_2sq": {str(b): [n, k] for b, n, k in
           [(b, n, k) for b, (n, k) in main_family.items()]},
           "all_pts": [[b, n, sq_decomp(n)] for b, n in pts]},
          open(os.path.join(BASE, "_phase102_p7_5e68_sq_decomp.json"), "w", encoding="utf-8"), indent=1)
print()
print("JSON 落盘 ✓  exit 0")
