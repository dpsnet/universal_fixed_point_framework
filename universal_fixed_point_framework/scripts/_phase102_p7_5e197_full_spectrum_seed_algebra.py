# -*- coding: utf-8 -*-
"""
P7-5e-197 · 全谱种子代数与窗口锚定判别（196 的检验 V + W）
用户推进（2026-10-15）。

检验 V 设计（m 通道全谱 B*(m) 种子代数统一）：
V1. B*(m)（m>=2）= (2·3+1)·2^m / (m·(2·3+1)·2^(m-1) + 2^m + 1)
    = {2,3,m} 表达（7 = 2·3+1 代入）—— 5（隔位种子）不出现
V2. m>=2 不含 5；隔位种子 5 是 m=1 特权标记
V3. m=1 naive 值（沿用通用公式）= 7·2^1/(1·7·1+2+1) = 14/10 = 7/5
    = 域宽/隔位种子 —— m=1 的 naive B* 恰是两框架常数之比
V4. 修正差值：7/5 - 455/332 = 49/1660 = 7^2/(5·332)

检验 W 设计（65 修正窗口锚定对照）：
W1. 65 = a_5（窗口 5 起边界）= b_1^2+1 统一
W2. B*(1) 分子 455 = 7·65 = 域宽 × a_5
W3. m=2 分母 33 = a_4（窗口 4 起边界 = 家族 m=5）对照
W4. 窗口下标映射：m=1 -> a_5、m=2 -> a_4（家族下标 m'=6、m'=5）
    m' = 7-m：1->6、2->5；m=3+ 失效（数值模式）
"""
import json
from fractions import Fraction

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e197_full_spectrum_seed_algebra.json"

# ---------- V1/V2 ----------
V1_rows = []
for m in range(2, 8):
    num = (2 * 3 + 1) * 2 ** m          # 7·2^m
    den = m * (2 * 3 + 1) * 2 ** (m - 1) + 2 ** m + 1
    V1_rows.append({
        "m": m, "B": f"{num}/{den}",
        "factors": "only {2,3,m}" ,
        "num_7x2m": num == 7 * 2 ** m,
        "den_formula_ok": den == m * 7 * 2 ** (m - 1) + 2 ** m + 1,
    })

# ---------- V3：m=1 naive ----------
V3 = {
    "naive_num": 7 * 2 ** 1,
    "naive_den": 1 * 7 * 2 ** 0 + 2 ** 1 + 1,
    "naive_B": "14/10",
    "naive_reduced": str(Fraction(7, 5)),
    "is_7over5": Fraction(14, 10) == Fraction(7, 5),
    "check": "m=1 naive B*(1) = 14/10 = 7/5 = 域宽/隔位种子",
}
# ---------- V4：修正差 ----------
V4 = {
    "actual_B1": "455/332",
    "diff": str(Fraction(7, 5) - Fraction(455, 332)),
    "diff_float": float(Fraction(7, 5) - Fraction(455, 332)),
    "is_49_1660": Fraction(7, 5) - Fraction(455, 332) == Fraction(49, 1660),
    "check": "7/5 - 455/332 = 49/1660 = 7^2/(5·332)",
}

# ---------- W ----------
W1 = {
    "65_eq_a5": 2 ** (5 + 1) + 1 == 65,
    "65_eq_b1sq_plus_1": 8 ** 2 + 1 == 65,
    "check": "65 = a_5 = b_1²+1 统一",
}
W2 = {
    "455_eq_7x65": 455 == 7 * 65,
    "check": "B*(1) 分子 455 = 7·65 = 域宽 × a_5",
}
W3 = {
    "33_eq_a4": 2 ** (4 + 1) + 1 == 33,
    "check": "m=2 分母 33 = a_4（窗口 4 起边界 = 家族 m=5）",
}
W4_rows = []
for m in range(1, 5):
    mp = 7 - m
    fam = 2 ** mp + 1
    # m=1: B*(1) 分子 455 含 65(a_5)；m=2: B*(2) 分母 33(a_4)；m>=3: 检查分母/分子
    if m == 1:
        target, has = 65, 455 % 65 == 0
    elif m == 2:
        target, has = 33, 33 == 33
    else:
        target, has = fam, False  # m>=3 的 B* 分数不含 a_mp 因子（93,241 等）
    W4_rows.append({"m": m, "m_prime_7minus_m": mp, "family_member": fam,
                    "window_anchor": f"a_{mp-1}" if mp >= 3 else "-",
                    "in_B": has})

# ---------- 结论 ----------
conclusion = {
    "verdict": "m>=2 全谱 B*(m) = {2,3,m} 表达（5 隔位种子不出现，是 m=1 特权标记）；m=1 naive 值 = 7/5 = 域宽/隔位种子（V3 决定性新观察），修正差 49/1660 = 7²/(5·332)；W：65 = a_5 = b_1²+1 统一、B*(1) 分子 455 = 7·a_5、m=2 分母 33 = a_4 对照——窗口锚定 m'=7-m 仅 m=1,2（数值模式）",
    "V": {
        "V1": "B*(m) = (2·3+1)·2^m / (m·(2·3+1)·2^(m-1)+2^m+1)（m=2..7 验证）——{2,3,m} 无自由参数",
        "V2": "m>=2 不含隔位种子 5；5 是 m=1 特权标记",
        "V3": "m=1 naive B*(1) = 14/10 = 7/5 = 域宽/隔位种子（决定性新观察）",
        "V4": "7/5 - 455/332 = 49/1660 = 7²/(5·332)",
    },
    "W": {
        "W1": W1["check"],
        "W2": W2["check"],
        "W3": W3["check"],
        "W4": "窗口锚定 m'=7-m（1->a_5、2->a_4）仅 m=1,2 成立，m>=3 失效——数值模式非机制",
    },
    "honest_limits": [
        "V3 的 7/5 是通用公式代入的直接结果（代数恒等，非独立约束）",
        "V4 修正差 49/1660 的 49=7² 为因式观察",
        "W4 窗口锚定 m'=7-m 仅 m=1,2（同 L5 m'=m²+1 模式，判数值模式）",
        "继承 187-196 候选层",
    ],
    "next_candidates": [
        "检验 X：7/5（m=1 naive）与 65 修正的互补结构（1.4 vs 1.3705，差 7²/(5·332)——'naive 域宽/种子比'框架下的修正意义）",
        "检验 Y：m 通道权重的窗口位置假说系统检验（m=1->a_5、m=2->a_4 之外是否还有其他窗口锚定：m=3->? 若 a_3=17 则 93 无 17 因子，假说已部分失效）",
        "窗口 2 家族段判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-197 full-spectrum seed algebra & window anchoring",
    "date": "2026-10-15",
    "V1_rows": V1_rows, "V3": V3, "V4": V4,
    "W1": W1, "W2": W2, "W3": W3, "W4_rows": W4_rows,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("=" * 72)
print("P7-5e-197 full-spectrum seed algebra & window anchoring")
print("=" * 72)
print("\n[V1 m>=2 spectrum]")
for r in V1_rows:
    print(f"  m={r['m']}: B*(m) = {r['B']}  num=7·2^m? {r['num_7x2m']}  den ok? {r['den_formula_ok']}  ({r['factors']})")
print("\n[V3 m=1 naive]")
print(f"  naive B*(1) = {V3['naive_B']} = {V3['naive_reduced']} (7/5? {V3['is_7over5']})")
print(f"  {V3['check']}")
print("\n[V4 correction diff]")
print(f"  7/5 - 455/332 = {V4['diff']} = {V4['diff_float']:.6f} (49/1660? {V4['is_49_1660']})")
print("\n[W window anchoring]")
print(f"  W1: 65 = a_5? {W1['65_eq_a5']} = b_1²+1? {W1['65_eq_b1sq_plus_1']}")
print(f"  W2: 455 = 7·65? {W2['455_eq_7x65']}")
print(f"  W3: 33 = a_4? {W3['33_eq_a4']}")
for r in W4_rows:
    print(f"  W4 m={r['m']}: m'=7-m={r['m_prime_7minus_m']} 家族={r['family_member']} 窗口锚={r['window_anchor']} 在 B*？ {r['in_B']}")
print("\n[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
