# paperX_n5_criterion.py
# Phase 72 阶段1：n=5 符号模式深化画像
# 1a: 复现 52 模式枚举（36 决定性 / 16 非决定性）
# 1b: 非决定性模式内部结构——A_BG 模式内取值集合 vs A5(31) 模式内取值集合
#     归因：A_BG 模式内决定性(单一值) 且 A5 非决定性 → (31) 公式结构缺陷
#           A_BG 模式内也非决定性 → 8 sg 符号结构不足（需扩展因子）
# 1c: 非决定性模式逐模式画像（取值分布/频次）
import sys
import json
import random
from collections import Counter, defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_pair, sg_block, A5
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5


def scan(n_samples=60000, seed=42):
    rng = random.Random(seed)
    pat_a_bg = defaultdict(set)     # 模式 -> A_BG 取值集合
    pat_a5 = defaultdict(set)       # 模式 -> A5(31) 取值集合
    pat_cnt = Counter()
    pat_agree = Counter()           # 模式内 (31) vs BG 一致样本数
    pat_disagree = Counter()
    examples = defaultdict(list)

    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        a_bg = A_BG(5, omega, zbar)
        a5 = A5(omega, zbar)
        pat_cnt[pat] += 1
        pat_a_bg[pat].add(round(a_bg, 6))
        pat_a5[pat].add(round(a5, 6))
        if abs(a_bg - a5) < 1e-9:
            pat_agree[pat] += 1
        else:
            pat_disagree[pat] += 1
            if len(examples[pat]) < 2:
                examples[pat].append({"a_bg": a_bg, "a5": a5, "omega": omega, "zbar": zbar})

    # 决定性判定
    det_bg = [p for p in pat_cnt if len(pat_a_bg[p]) == 1]
    nondet_bg = [p for p in pat_cnt if len(pat_a_bg[p]) > 1]
    det_a5 = [p for p in pat_cnt if len(pat_a5[p]) == 1]
    nondet_a5 = [p for p in pat_cnt if len(pat_a5[p]) > 1]

    # 归因分类（在 16 个 A_BG 非决定性模式中）：
    #  型1: A_BG 决定性 & A5 非决定性 -> (31) 公式结构缺陷（符号结构对 BG 已充分）
    #  型2: A_BG 非决定性 & A5 非决定性 -> 符号结构不足（需扩展因子）
    #  型3: A_BG 非决定性 & A5 决定性 -> (31) 模式内"压平"BG 依赖的额外信息（A5 决定性但可能错误）
    type1 = [p for p in nondet_a5 if len(pat_a_bg[p]) == 1]
    type2 = [p for p in nondet_a5 if len(pat_a_bg[p]) > 1]
    type3 = [p for p in nondet_bg if len(pat_a5[p]) == 1]

    print(f"样本: {n_samples}")
    print(f"模式总数: {len(pat_cnt)}")
    print(f"A_BG 决定性模式: {len(det_bg)} / 非决定性: {len(nondet_bg)}")
    print(f"A5(31) 决定性模式: {len(det_a5)} / 非决定性: {len(nondet_a5)}")
    print(f"归因: 型1[(31)公式缺陷]={len(type1)} 型2[符号结构不足]={len(type2)} 型3[(31)压平BG信息]={len(type3)}")

    # 型2 详情：A_BG 在模式内取几个值？
    type2_valcount = {}
    for p in type2:
        type2_valcount[p] = (len(pat_a_bg[p]), sorted(pat_a_bg[p]), len(pat_a5[p]), sorted(pat_a5[p]))

    # 16 个 A_BG 非决定性模式的画像（tuple 键转字符串供 JSON）
    def pstr(p):
        return ",".join(str(x) for x in p)

    portrait = {}
    for p in nondet_bg:
        portrait[pstr(p)] = {
            "count": pat_cnt[p],
            "A_BG_vals": sorted(pat_a_bg[p]),
            "A5_vals": sorted(pat_a5[p]),
            "agree": pat_agree[p],
            "disagree": pat_disagree[p],
            "examples": examples[p],
        }

    res = {
        "samples": n_samples,
        "total_patterns": len(pat_cnt),
        "det_BG": len(det_bg),
        "nondet_BG": len(nondet_bg),
        "det_A5": len(det_a5),
        "nondet_A5": len(nondet_a5),
        "attribution_type1_formula_defect": [pstr(p) for p in type1],
        "attribution_type2_symbol_insufficient": [pstr(p) for p in type2],
        "attribution_type3_formula_flattens_BG": [pstr(p) for p in type3],
        "type2_BG_valcount": {pstr(p): v for p, v in type2_valcount.items()},
        "nondeterministic_portrait": portrait,
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_criterion_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n5_criterion_results.json")


if __name__ == "__main__":
    scan()
