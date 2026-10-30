# paperX_n6_criterion.py
# Phase 72 延伸：n=6 符号判据推进——第一步：模式枚举与决定性/非决定性画像
# 基座因子集（n=5 的 8sg 循环推广，12 个）：
#   单对：s12,s23,s34,s45,s56,s61（0-based: (0,1),(1,2),(2,3),(3,4),(4,5),(5,0)）
#   首索引块：s123,s234,s345,s1234,s2345,s12345
# 目标：A_BG(6) 模式内取值集合 → 决定性/非决定性；归因（型1/2/3 vs A6(32)）
import sys
import json
import random
from collections import Counter, defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_pair, sg_block, A6
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear


def sg_pattern6(omega, zbar):
    """n=6 的 12 个基座 sg 因子（8sg 的循环推广）"""
    w, z = omega, zbar
    return (
        sg_pair(w, z, 0, 1), sg_pair(w, z, 1, 2), sg_pair(w, z, 2, 3),
        sg_pair(w, z, 3, 4), sg_pair(w, z, 4, 5), sg_block(w, z, (5,), (0,)),
        sg_block(w, z, (0,), (1, 2)), sg_block(w, z, (1,), (2, 3)),
        sg_block(w, z, (2,), (3, 4)),
        sg_block(w, z, (0,), (1, 2, 3)), sg_block(w, z, (1,), (2, 3, 4)),
        sg_block(w, z, (0,), (1, 2, 3, 4)),
    )


def scan(n_samples=10000, seed=42):
    rng = random.Random(seed)
    pat_a_bg = defaultdict(set)
    pat_a6 = defaultdict(set)
    pat_cnt = Counter()
    pat_agree = Counter()
    pat_disagree = Counter()
    examples = defaultdict(list)

    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern6(omega, zbar)
        a_bg = A_BG(6, omega, zbar)
        a6 = A6(omega, zbar)
        pat_cnt[pat] += 1
        pat_a_bg[pat].add(round(a_bg, 6))
        pat_a6[pat].add(round(a6, 6))
        if abs(a_bg - a6) < 1e-9:
            pat_agree[pat] += 1
        else:
            pat_disagree[pat] += 1
            if len(examples[pat]) < 2:
                examples[pat].append({"a_bg": a_bg, "a6": a6, "omega": omega, "zbar": zbar})

    det_bg = [p for p in pat_cnt if len(pat_a_bg[p]) == 1]
    nondet_bg = [p for p in pat_cnt if len(pat_a_bg[p]) > 1]
    det_a6 = [p for p in pat_cnt if len(pat_a6[p]) == 1]
    nondet_a6 = [p for p in pat_cnt if len(pat_a6[p]) > 1]

    type1 = [p for p in nondet_a6 if len(pat_a_bg[p]) == 1]
    type2 = [p for p in nondet_a6 if len(pat_a_bg[p]) > 1]
    type3 = [p for p in nondet_bg if len(pat_a6[p]) == 1]

    print(f"样本: {n_samples}")
    print(f"模式总数: {len(pat_cnt)}")
    print(f"A_BG 决定性模式: {len(det_bg)} / 非决定性: {len(nondet_bg)}")
    print(f"A6(32) 决定性模式: {len(det_a6)} / 非决定性: {len(nondet_a6)}")
    print(f"归因: 型1[(32)公式缺陷]={len(type1)} 型2[符号结构不足]={len(type2)} 型3[(32)压平BG信息]={len(type3)}")

    # 多值性结构：非决定性模式内 A_BG 取值集合
    nondet_valcount = {}
    for p in nondet_bg:
        nondet_valcount[p] = (len(pat_a_bg[p]), sorted(pat_a_bg[p]))

    def pstr(p):
        return ",".join(str(x) for x in p)

    res = {
        "samples": n_samples,
        "total_patterns": len(pat_cnt),
        "det_BG": len(det_bg),
        "nondet_BG": len(nondet_bg),
        "det_A6": len(det_a6),
        "nondet_A6": len(nondet_a6),
        "attribution_type1_formula_defect": [pstr(p) for p in type1],
        "attribution_type2_symbol_insufficient": [pstr(p) for p in type2],
        "attribution_type3_formula_flattens_BG": [pstr(p) for p in type3],
        "nondet_BG_valcount": {pstr(p): v for p, v in nondet_valcount.items()},
    }
    # 非决定性模式画像（含 A6 值、违反样本）
    portrait = {}
    for p in nondet_bg:
        portrait[pstr(p)] = {
            "count": pat_cnt[p],
            "A_BG_vals": sorted(pat_a_bg[p]),
            "A6_vals": sorted(pat_a6[p]),
            "agree": pat_agree[p],
            "disagree": pat_disagree[p],
            "examples": examples[p],
        }
    res["nondeterministic_portrait"] = portrait

    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n6_criterion_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n6_criterion_results.json")


if __name__ == "__main__":
    scan()
