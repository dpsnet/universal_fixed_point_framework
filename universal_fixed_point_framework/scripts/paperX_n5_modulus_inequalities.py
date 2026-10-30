# -*- coding: utf-8 -*-
"""
paperX_n5_modulus_inequalities.py
待闭合引理 L1/L2 验证：
  L1：|[λ₂,λ₃]| > |[λ₁,λ₃]|（模式 s=+1）⟺ sg([λ₃,λ₄₅]) = s
  L2：|[λ₂,λ₄]| > |[λ₂,λ₃]|（模式 s=+1）⟺ sg([λ₂,λ₃₄]) = −s
验证两不等式在困难模式样本内是否 100% 成立（大样本）。
输出：违反样本计数 + 模长比分布（是否远离边界）。
"""
import sys
import random
import json
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_pair
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}


def bracket(i, j, omega, zbar):
    """[λ̃_i, λ̃_j] = ωᵢωⱼ(z̄ᵢ−z̄ⱼ)（R₁ 半共线，0-based）"""
    return omega[i] * omega[j] * (zbar[i] - zbar[j])


def scan(n_samples=200000, seed=719):
    rng = random.Random(seed)
    n_hard = 0
    viol_l1 = 0
    viol_l2 = 0
    min_ratio_l1 = 1e9
    min_ratio_l2 = 1e9
    examples = []
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        n_hard += 1
        s = sg_pair(omega, zbar, 0, 1)  # s12 = s
        from paperX_single_minus_numerics import sg_block
        e6 = sg_block(omega, zbar, (0, 1), (0, 1, 2))
        e7 = sg_block(omega, zbar, (0, 1), (0, 1, 2, 3))
        nonzero = (e6 == e7 and e6 != 0)
        # L1（非零条件口径）：[λ₃,λ₄₅] 恒 = s₁₂₃ = −s？（[1]|[2]|[34] ratio₁ 分母）
        b23 = bracket(1, 2, omega, zbar)   # [λ₂,λ₃]
        b13 = bracket(0, 2, omega, zbar)   # [λ₁,λ₃]
        b34_5 = bracket(2, 3, omega, zbar) + bracket(2, 4, omega, zbar)  # [λ₃,λ₄₅]
        if abs(b34_5 - (b13 + b23)) > 1e-9:
            examples.append(("ident_fail", b34_5, b13 + b23))
            continue
        sg_b345 = (b34_5 > 0) - (b34_5 < 0)
        if nonzero and sg_b345 != s:
            viol_l1 += 1
            if len(examples) < 5:
                examples.append(("L1", s, sg_b345, e6, e7, b13, b23, b34_5))
        r1 = abs(b23) / max(abs(b13), 1e-12)
        min_ratio_l1 = min(min_ratio_l1, r1)
        # L2（非零条件口径）：[λ₂,λ₃₄] 恒 = −s？（[1]|[23]|[4] ratio₀ 分母）
        b24 = bracket(1, 3, omega, zbar)   # [λ₂,λ₄]
        b2_34 = bracket(1, 2, omega, zbar) + bracket(1, 3, omega, zbar)  # [λ₂,λ₃₄]
        if abs(b2_34 - (b23 + b24)) > 1e-9:
            examples.append(("ident_fail2", b2_34, b23 + b24))
            continue
        sg_b234 = (b2_34 > 0) - (b2_34 < 0)
        if nonzero and sg_b234 != -s:
            viol_l2 += 1
            if len(examples) < 5:
                examples.append(("L2", s, sg_b234, e6, e7, b23, b24, b2_34))
        r2 = abs(b24) / max(abs(b23), 1e-12)
        min_ratio_l2 = min(min_ratio_l2, r2)
    print(f"困难模式样本: {n_hard}")
    print(f"L1 违反（非零条件, sg=[λ₃,λ₄₅]≠s）: {viol_l1}；|λ₂λ₃|/|λ₁λ₃| 最小比: {min_ratio_l1:.4f}")
    print(f"L2 违反（非零条件, sg=[λ₂,λ₃₄]≠−s）: {viol_l2}；|λ₂λ₄|/|λ₂λ₃| 最小比: {min_ratio_l2:.4f}")
    if examples:
        print("示例:", examples[:3])
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_modulus_inequalities_results.json", "w", encoding="utf-8") as f:
        json.dump({"n_hard": n_hard, "viol_l1": viol_l1, "viol_l2": viol_l2,
                   "min_ratio_l1": min_ratio_l1, "min_ratio_l2": min_ratio_l2,
                   "examples": examples[:3]}, f, ensure_ascii=False, indent=2)
    print("DONE")


if __name__ == "__main__":
    scan()
