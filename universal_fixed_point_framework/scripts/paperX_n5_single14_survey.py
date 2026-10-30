# -*- coding: utf-8 -*-
"""③ 测绘：14 个单因子模式的投影序结构（h_extra 依赖关系）。

对 SINGLE_6（8 模式，列 6=E6）+ SINGLE_7（6 模式，列 7=E7）：
1. 模式内 h_extra = sg([λ₂₃,λ₄])（bk{1,2}{3}）与 A_BG 的相关性：
   - h_extra 是否模式内恒定（投影序等价类固定）？
   - A_BG 是否对 h_extra 不敏感（单因子判据成立的基础）？
2. h_extra 是否可从 8sg 推出（h_extra == s234 或 == -s234 或模式内两值都出现）？
3. 输出 14 模式的 28 情形表（因子值 → A_BG），供 Lean 化逐模式定理目标。
"""
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}
SINGLE_6 = {
    (1, 1, -1, -1, -1, -1, 1, -1), (-1, -1, 1, 1, 1, 1, -1, 1),
    (1, 1, -1, -1, 1, -1, 1, 1), (1, 1, -1, -1, 1, 1, 1, 1),
    (-1, -1, 1, 1, -1, -1, -1, -1), (1, 1, 1, 1, -1, -1, 1, -1),
    (-1, -1, -1, -1, 1, 1, -1, 1), (-1, -1, 1, 1, -1, 1, -1, -1),
}
SINGLE_7 = {
    (-1, 1, -1, -1, -1, -1, 1, -1), (1, -1, 1, 1, 1, 1, -1, 1),
    (1, -1, -1, -1, 1, 1, -1, 1), (1, 1, -1, -1, 1, 1, -1, 1),
    (-1, 1, 1, 1, -1, -1, 1, -1), (-1, -1, 1, 1, -1, -1, 1, -1),
}
TARGET = SINGLE_6 | SINGLE_7


def ext_sgs(omega, zbar):
    """列 6 = sg([λ12,λ123]) = sg_block((0,1),(0,1,2))；列 7 = sg([λ12,λ1234]) = sg_block((0,1),(0,1,2,3))"""
    return (sg_block(omega, zbar, (0, 1), (0, 1, 2)), sg_block(omega, zbar, (0, 1), (0, 1, 2, 3)))


def h_extra(omega, zbar):
    """sg([λ₂₃,λ₄]) = bk{1,2}{3}（0-based 粒子 2,3 vs 4）"""
    return sg_block(omega, zbar, (1, 2), (3,))


def main():
    rng = random.Random(20261002)
    per = defaultdict(lambda: {"e6": defaultdict(list), "e7": defaultdict(list),
                               "hx": defaultdict(set), "a": defaultdict(set),
                               "hx_by_a": defaultdict(set), "a_by_hx": defaultdict(set)})
    n = 300000
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in TARGET:
            continue
        a = A_BG(5, omega, zbar)
        e6, e7 = ext_sgs(omega, zbar)
        hx = h_extra(omega, zbar)
        rec = per[pat]
        rec["e6"][e6].append(a)
        rec["e7"][e7].append(a)
        rec["hx"][hx].add(a)
        rec["a"][a].add(hx)
        rec["hx_by_a"][a].add(hx)
        rec["a_by_hx"][hx].add(a)
    print(f"=== 14 个单因子模式投影序结构（{n} 样本采样） ===")
    print(f"{'模式':<38} {'列':<3} {'因子值→A_BG':<28} {'hx变化':<10} {'hx==s234?':<9} {'A对hx敏感?'}")
    summary = {}
    for pat in sorted(TARGET):
        rec = per[pat]
        col = 6 if pat in SINGLE_6 else 7
        vals = rec["e6"] if col == 6 else rec["e7"]
        # 因子值 → A_BG 唯一值
        rule = {}
        for v, lst in sorted(vals.items(), key=lambda kv: kv[0]):
            s = set(round(x, 6) for x in lst)
            rule[v] = sorted(s)
        # h_extra 分析
        hxs = rec["hx"].keys()
        hx_vary = len(hxs) > 1
        hx_is_s234 = None
        if not hx_vary:
            hx = list(hxs)[0]
            hx_is_s234 = (hx == pat[6])  # s234 是 tuple 第 7 位（索引 6）
        a_by_hx_sens = any(len(v) > 1 for v in rec["a_by_hx"].values())
        summary[str(pat)] = {"col": col, "rule": {str(k): v for k, v in rule.items()},
                             "hx": sorted(hxs), "hx_is_s234": hx_is_s234,
                             "A_depends_on_hx": a_by_hx_sens}
        print(f"{str(pat):<38} {col:<3} {str(rule):<28} {'变化' if hx_vary else '固定'!r:<10} "
              f"{str(hx_is_s234):<9} {'敏感' if a_by_hx_sens else '不敏感'}")
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_single14_survey_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print("DONE -> scripts/paperX_n5_single14_survey_results.json")


if __name__ == "__main__":
    main()
