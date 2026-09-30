# -*- coding: utf-8 -*-
"""
诊断：(31) 在 generic z 下 2.4% 偏差的来源——s1234 首索引 vs 块和记号混淆？
==========================================================================
假设：不一致全部源于 (31) 项7/8 的 s1234 = sg([λ1, λ2+λ3+λ4])（首索引）
      vs 逗号块和 sg_{12,34} = sg([λ1+λ2, λ3+λ4])。
若不一致样本中两者不同且改块和后全一致 → 记号混淆源确认，解析判定可闭合。
"""
import random
import sys
from collections import Counter

sys.path.insert(0, "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts")
from paperX_single_minus_numerics import sg, sg_pair, sg_block, A5
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear

SEED = 20260930
random.seed(SEED)


def A5_alt_s1234(omega, zbar):
    """(31) 变体：s1234 改用逗号块和 sg_{12,34}，其余项不变"""
    w, z = omega, zbar
    s51 = sg_block(w, z, (4,), (0,))
    s12 = sg_pair(w, z, 0, 1)
    s23 = sg_pair(w, z, 1, 2)
    s34 = sg_pair(w, z, 2, 3)
    s45 = sg_pair(w, z, 3, 4)
    s234 = sg_block(w, z, (1,), (2, 3))
    s123 = sg_block(w, z, (0,), (1, 2))
    s1234 = sg_block(w, z, (0, 1), (2, 3))  # 块和版
    return 0.25 * (
        s51 * s34 * s234
        + s51 * s23 * s234
        - s51 * s234 * s234
        + s45 * s23 * s123
        + s45 * s12 * s123
        - s45 * s123 * s123
        + s51 * s45 * s1234
        + s12 * s34 * s1234
    )


def main():
    n_samples = 20000
    n_agree = 0
    disagree = 0
    disagree_s1234_same = 0
    disagree_s1234_diff = 0
    disagree_alt_agree = 0
    diff_pat = Counter()
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True)
        a_bg = A_BG(5, omega, zbar)
        a5 = A5(omega, zbar)
        if abs(a_bg - a5) < 1e-9:
            n_agree += 1
            continue
        disagree += 1
        s1234_head = sg_block(omega, zbar, (0,), (1, 2, 3))
        s1234_block = sg_block(omega, zbar, (0, 1), (2, 3))
        if s1234_head == s1234_block:
            disagree_s1234_same += 1
        else:
            disagree_s1234_diff += 1
        a5_alt = A5_alt_s1234(omega, zbar)
        if abs(a_bg - a5_alt) < 1e-9:
            disagree_alt_agree += 1
            diff_pat["alt_fixed"] += 1
        else:
            diff_pat["alt_not_fixed"] += 1
    print("=" * 72)
    print("诊断：(31) generic z 偏差来源——s1234 首索引 vs 块和")
    print("=" * 72)
    print(f"采样={n_samples}, 一致={n_agree}, 不一致={disagree} ({disagree/n_samples:.4f})")
    print(f"不一致中 s1234 首索引==块和: {disagree_s1234_same}")
    print(f"不一致中 s1234 首索引!=块和: {disagree_s1234_diff}")
    print(f"改块和后与 BG 一致: {disagree_alt_agree}")
    print(f"改块和后仍不一致: {diff_pat['alt_not_fixed']}")
    if disagree > 0:
        if disagree_s1234_diff == disagree and disagree_alt_agree == disagree:
            print("结论候选：记号混淆确认（100% 不一致由 s1234 记号引起）")
        else:
            print("结论候选：记号混淆不充分——存在其他结构差异")


if __name__ == "__main__":
    main()
