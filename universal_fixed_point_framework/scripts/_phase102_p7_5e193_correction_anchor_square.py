# -*- coding: utf-8 -*-
"""
P7-5e-193 · 1/65 修正锚点平方结构判别（192 的检验 N + O）
用户推进（2026-10-15）。

检验 N 设计（7 分数互补，预期弱）：
N1. 65 ≡ 2 mod 7（65 = 7·9+2）
N2. 2/7 = 1 − 5/7（互补）
N3. 1/65 数值是否由 2/7 生成（预期无整洁代数 → 弱结论）

检验 O 设计（65 的窗口平方锚点，主发现）：
O1. 65 = b_1²+1 = 8²+1（根窗口终边界 b_1 = 8 的平方+1）
O2. 推广：b_j²+1 = 2^{2(j+2)}+1 = 家族 m=2j+4 成员 = a_{2j+3}（窗口 2j+3 起边界）
    j=1: 65 = a_5 ✓；j=2: 257 = a_7 ✓；j=3: 1025 = a_9（k_max=8 框架外）
O3. m=1 修正 = 1/(b_1²+1) —— 锚定根窗口自身的平方结构
O4. 候选解释：m=1 是根窗口（窗口 1）根通道，修正锚定根窗口终边界平方；
    65 的"窗口 5 起边界"身份 = 同一数的等价身份（b_1²+1 = a_5）
"""
import json
from fractions import Fraction

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e193_correction_anchor_square.json"

# ---------- N1/N2 ----------
N1 = {
    "65_mod_7": 65 % 7,
    "65_eq_7x9_plus_2": 65 == 7 * 9 + 2,
    "check": "65 ≡ 2 (mod 7) ✓",
}
N2 = {
    "5over7_plus_2over7": str(Fraction(5, 7) + Fraction(2, 7)),
    "is_1": Fraction(5, 7) + Fraction(2, 7) == 1,
    "check": "2/7 = 1 − 5/7（互补）✓",
}

# ---------- N3：1/65 与 2/7 数值关系 ----------
N3 = {
    "1over65": 1 / 65,
    "2over7": 2 / 7,
    "ratio_2o7_over_1o65": (2 / 7) / (1 / 65),   # 130/7 = 18.5714...
    "ratio_not_clean": True,  # 130/7 非整洁代数
    "candidate": "65 ≡ 2 mod 7 是模算术事实；1/65 数值由 B*(1) 精确值决定（数值第一性），非由 2/7 生成 → 互补候选弱",
}

# ---------- O1 ----------
O1 = {
    "b1": 8,
    "b1_sq_plus_1": 8 ** 2 + 1,
    "is_65": 8 ** 2 + 1 == 65,
    "check": "65 = b_1²+1 = 8²+1（根窗口终边界 b_1=8 的平方+1）✓",
}

# ---------- O2：推广 b_j²+1 ----------
O2_rows = []
for j in range(1, 4):
    bj = 2 ** (j + 2)
    bj_sq_p1 = bj ** 2 + 1
    family_m = 2 * j + 4
    window_k = 2 * j + 3
    O2_rows.append({
        "j": j, "b_j": bj, "b_j^2+1": bj_sq_p1,
        "as_2p_family": 2 ** family_m + 1,
        "family_m": family_m,
        "window_a_index": window_k,
        "as_a_window_start": 2 ** (window_k + 1) + 1,
        "in_window": window_k <= 6,
        "identity_ok": bj_sq_p1 == 2 ** family_m + 1 == 2 ** (window_k + 1) + 1,
    })

# ---------- O3 ----------
O3 = {
    "m1_correction": "1/65 = 1/(b_1²+1)，b_1 = 8 = 2^{j+2}（j=1 根窗口）",
    "anchor": "m=1 修正锚定根窗口自身的平方结构（终边界平方+1）",
    "a5_equivalence": "65 的'窗口 5 起边界'身份 = b_1²+1 的等价身份（同一数）",
}

# ---------- 结论 ----------
conclusion = {
    "verdict": "检验 N 弱（7 分数互补是模算术事实，非 1/65 来源）；检验 O 主发现：65 = b_1²+1（根窗口终边界平方+1）= a_5（窗口 5 起边界），推广 b_j²+1 = 家族 m=2j+4 = a_{2j+3}——m=1 修正锚定根窗口平方结构",
    "N": {
        "N1": N1["check"], "N2": N2["check"], "N3": N3["candidate"],
        "verdict": "弱——降级登记（数值第一性：65 由 B*(1) 精确值决定）",
    },
    "O": {
        "O1": O1["check"],
        "O2_generalization": "b_j²+1 = 2^{2(j+2)}+1 = 家族 m=2j+4 成员 = 窗口 2j+3 起边界（j=1: 65=a_5 ✓, j=2: 257=a_7 ✓, j=3: 1025=a_9 框架外）",
        "O3_anchor": "m=1 修正 = 1/(b_1²+1)——根窗口平方结构锚定（候选机制）",
    },
    "honest_limits": [
        "检验 N 弱结论登记（无代数来源，数值第一性）",
        "检验 O 的'为什么是平方结构'未解释（65 的选择仍由 B*(1) 决定；b_1²+1 是身份解释非机制）",
        "b_j²+1 推广 j=3 超出 k_max=8 窗口（1025=a_9 框架外）",
        "继承 187-192 候选层",
    ],
    "next_candidates": [
        "检验 P：B*(1) = 455/332 的分数结构（455=5·7·13, 332=4·83；455−332=123=3·41 D 分子）",
        "检验 Q：m=1 修正是否唯一（m 通道 1 特权的其他表现：|m|/2 项 1/2 = 0.5 的 B* 值 ~1.37 与 m=2 的 ~0.85 对称性）",
        "窗口 2 家族段（m=9..16）为分数/整数段重复判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-193 · 1/65 修正锚点平方结构判别",
    "date": "2026-10-15",
    "N1": N1, "N2": N2, "N3": N3,
    "O1": O1, "O2_rows": O2_rows, "O3": O3,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---------- 控制台 ----------
print("=" * 72)
print("P7-5e-193 · 1/65 修正锚点平方结构判别")
print("=" * 72)
print("\n【N 7 分数互补（预期弱）】")
print(f"  N1: 65 mod 7 = {N1['65_mod_7']}（65 = 7·9+2: {N1['65_eq_7x9_plus_2']}）")
print(f"  N2: 5/7 + 2/7 = {N2['5over7_plus_2over7']} = 1？ {N2['is_1']}")
print(f"  N3: 1/65={N3['1over65']:.8f} vs 2/7={N3['2over7']:.8f}，比值={N3['ratio_2o7_over_1o65']:.4f}=130/7 非整洁")
print(f"  N 结论: {N3['candidate']}")
print("\n【O 65 平方锚点（主发现）】")
print(f"  O1: b_1=8，b_1²+1 = {O1['b1_sq_plus_1']} = 65？ {O1['is_65']}")
print(f"  {'j':<3}{'b_j':<6}{'b_j²+1':<10}{'家族m':<8}{'a下标':<8}{'a值':<10}{'框架内'}")
for r in O2_rows:
    print(f"  {r['j']:<3}{r['b_j']:<6}{r['b_j^2+1']:<10}{r['family_m']:<8}{r['window_a_index']:<8}{r['as_a_window_start']:<10}{r['in_window']}")
print(f"  身份恒等（b_j²+1=2^(2j+4)+1=a_{'{2j+3}'}）: 全 True = {all(r['identity_ok'] for r in O2_rows)}")
print(f"  O3: {O3['m1_correction']}")
print(f"  O3: {O3['anchor']}")
print("\n【结论】", conclusion["verdict"])
print("  下一步候选:", conclusion["next_candidates"][0])
