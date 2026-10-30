# -*- coding: utf-8 -*-
"""
P7-5e-192 · 1/65 修正项家族镜像判别（191 的检验 L + M）
用户推进（2026-10-15）。

检验 L 设计（1/65 修正项身份）：
闭式 129：1/B*(m) = |m|/2 + 1/7 + 1/(7·2^|m|) + [|m|=1: +1/65]
L1. 高精度验证：1/B*(1) - 1/65 = 5/7 精确分解
L2. 65 的三重身份：65 = 2^6+1（家族 m=6 成员）；65 = a_5（窗口 5 起边界 2^{5+1}+1）；
    65 = 8·8+1（静默单元 k=8 单位位）
L3. 5/7 的身份：5 = 2^2+1（家族 m=2 成员）= 隔位种子；7 = 域宽
L4. m=2 对照：1/B*(2) = 1 + 5/28 = 33/28 —— 33 = 2^5+1（家族 m=5 成员）
L5. 候选解释登记（不锁定）：
    - 1/B*(1) = 5/7 + 1/65：主值（无修正）为纯 7 分数 5/7，修正 1/65 补足
    - m=1 特权 = 唯一使主值为纯 7 分数的通道（m>=2 主值含 2^m 分母）
    - 65 的窗口边界身份（a_5）与 m=1 的根窗口异类（a_1=1）的关联候选
    - m=1,2 主值分子 = 家族 m'=m^2+1 成员（1->5=m2, 2->33=m5）；m=3 失效（93!=1025）→ 数值模式非机制

检验 M 设计（截距分母对偶）：
M1. 截距分母分解：7·2^m = 7（域宽）× 2^m（满格）
M2. 截距 = (2^m+1)/(7·2^m) = 家族分子 / (域宽·满格)
M3. 1/7 + 1/(7·2^m) = (2^m+1)/(7·2^m) 恒等验证
M4. 结论：截距 = 家族分子 × (域宽·满格)^{-1} —— "域宽×满格"对偶的又一投影
"""
import json
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 50

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e192_correction_family_mirror.json"

# ---------- L1：精确分解 1/B*(1) - 1/65 = 5/7 ----------
# 闭式 129 m=1：1/2 + 1/7 + 1/14 + 1/65
B1_inv = Fraction(1, 2) + Fraction(1, 7) + Fraction(1, 14) + Fraction(1, 65)
main_part = Fraction(1, 2) + Fraction(1, 7) + Fraction(1, 14)  # 无修正
L1 = {
    "B1_inv": str(B1_inv),
    "B1_inv_float": float(B1_inv),
    "main_part": str(main_part),
    "main_part_float": float(main_part),
    "main_part_value": str(Fraction(5, 7)),
    "B1_inv_minus_1over65": str(B1_inv - Fraction(1, 65)),
    "is_exact_5over7": (B1_inv - Fraction(1, 65)) == Fraction(5, 7),
    "check": "1/B*(1) = 5/7 + 1/65（精确）",
}

# ---------- L2：65 三重身份 ----------
L2 = {
    "65_as_2p6_plus_1": 2 ** 6 + 1 == 65,
    "65_as_window5_start": 2 ** (5 + 1) + 1 == 65,
    "65_as_silent_k8": 8 * 8 + 1 == 65,
    "identity_notes": {
        "family_member_m6": "65 = 2^6+1 = 2^m+1 家族 m=6 成员",
        "window5_start": "65 = a_5 = 2^{5+1}+1（窗口 5 起边界 [65,128]）",
        "silent_unit_k8": "65 = 8·8+1（静默单元 k=8 单位位）",
    },
}

# ---------- L3：5/7 身份 ----------
L3 = {
    "5_as_family_m2": 2 ** 2 + 1 == 5,
    "5_as_gap_seed": "5 = 2^2+1 = 隔位种子（191 种子观察）",
    "7_as_domain_width": "7 = 域宽（闭式 129 主截距 1/7）",
    "5over7_as_4x_intercept_m2": str(Fraction(5, 7)) + " = 4·(5/28) = 4×截距(m=2)",
}

# ---------- L4：m=2 主值分子 ----------
L4 = {
    "B2_inv": str(Fraction(1, 1) + Fraction(5, 28)),  # 1 + 5/28 = 33/28
    "numerator_33": 33,
    "33_as_family_m5": 2 ** 5 + 1 == 33,
    "check": "m=2 主值 1/B*(2) = 33/28，分子 33 = 2^5+1（家族 m=5 成员）",
}

# ---------- L5：m'=m^2+1 模式检验 ----------
L5_rows = []
for m in range(1, 6):
    mp = m ** 2 + 1
    family_member = 2 ** mp + 1
    # 主值分子（1/B* 的精确分数分子）
    if m == 1:
        num = Fraction(1, 2) + Fraction(1, 7) + Fraction(1, 14)  # 5/7
    elif m == 2:
        num = Fraction(1, 1) + Fraction(1, 7) + Fraction(1, 28)  # 33/28
    else:
        num = Fraction(m, 2) + Fraction(1, 7) + Fraction(1, 7 * 2 ** m)
    L5_rows.append({
        "m": m, "m_prime": mp, "family_member": family_member,
        "main_value": str(num), "num_numerator": num.numerator,
        "matches": num.numerator == family_member,
    })

# ---------- M：截距分母对偶 ----------
M_rows = []
for m in range(1, 9):
    M_rows.append({
        "m": m,
        "den": 7 * 2 ** m,
        "domain_width": 7,
        "full_lattice": 2 ** m,
        "numerator_family": 2 ** m + 1,
        "intercept": str(Fraction(2 ** m + 1, 7 * 2 ** m)),
        "identity_check": Fraction(1, 7) + Fraction(1, 7 * 2 ** m) == Fraction(2 ** m + 1, 7 * 2 ** m),
    })

M_ok = all(r["identity_check"] for r in M_rows)

# ---------- 结论 ----------
conclusion = {
    "verdict": "1/65 修正 = 家族 m=6 成员（65=2^6+1）的精确补足项：1/B*(1)=5/7+1/65 精确分解；m=1 特权 = 唯一纯 7 分数主值通道（候选解释）；截距分母 7·2^m = 域宽×满格对偶投影（M 验证通过）",
    "L": {
        "exact_decomposition": "1/B*(1) = 5/7 + 1/65（精确，非近似）",
        "65_triple_identity": "家族 m=6 成员 / 窗口 5 起边界 a_5 / 静默 k=8 单位位",
        "m1_privilege_candidate": "m=1 是唯一使主值（无修正）为纯 7 分数 5/7 的通道；m>=2 主值含 2^m 分母 → 1/65 补足仅 m=1 需要",
        "m2_contrast": "m=2 主值 33/28 分子 33=家族 m=5 —— m=1,2 主值分子均为家族成员（m'=m^2+1: 1->2, 2->5 成立；m=3 失效 93!=1025 → 数值模式非机制）",
    },
    "M": {
        "intercept_dual": "截距 = (2^m+1)/(7·2^m) = 家族分子/(域宽·满格)",
        "verified": M_ok,
    },
    "honest_limits": [
        "m=1 特权解释为候选（纯 7 分数主值 + 窗口 1 根窗口异类同源候选），未定案",
        "65 的三重身份（家族/窗口边界/静默）是身份重合而非因果机制",
        "m'=m^2+1 分子模式仅 m=1,2 成立，判定为数值模式",
        "继承 187-191 候选层",
    ],
    "next_candidates": [
        "检验 N：m=1 的 5/7 主值与 1/65 修正的'7 分数互补'（5/7+2/7=1；65≡2 mod 7）",
        "检验 O：窗口 5 起边界 a_5=65 在闭式中的角色——是否 m=1 修正锚定窗口 5（对称窗口？）",
        "窗口 2 家族段（m=9..16）为分数/整数段重复判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-192 · 1/65 修正项家族镜像判别",
    "date": "2026-10-15",
    "L1": L1,
    "L2": L2,
    "L3": L3,
    "L4": L4,
    "L5_rows": L5_rows,
    "M_rows": M_rows,
    "M_ok": M_ok,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---------- 控制台 ----------
print("=" * 72)
print("P7-5e-192 · 1/65 修正项家族镜像判别")
print("=" * 72)
print("\n【L1 精确分解】")
print(f"  1/B*(1) = {B1_inv} = {float(B1_inv):.10f}")
print(f"  主值（无修正）= {main_part} = 5/7？ {main_part == Fraction(5,7)}")
print(f"  1/B*(1) - 1/65 = {B1_inv - Fraction(1,65)} = 5/7？ {L1['is_exact_5over7']}")
print("\n【L2 65 三重身份】")
for k, v in L2["identity_notes"].items():
    print(f"  {v}")
print("\n【L3 5/7 身份】")
print(f"  5 = 2^2+1（家族 m=2）？ {L3['5_as_family_m2']}；5 = 隔位种子；7 = 域宽")
print(f"  5/7 = 4×截距(m=2)（4·5/28）")
print("\n【L4 m=2 对照】")
print(f"  1/B*(2) = {L4['B2_inv']}；33 = 2^5+1？ {L4['33_as_family_m5']}")
print("\n【L5 m'=m^2+1 模式】")
for r in L5_rows:
    print(f"  m={r['m']}: 主值={r['main_value']}（分子 {r['num_numerator']}）vs 家族 m'={r['m_prime']} = {r['family_member']} → {'匹配' if r['matches'] else '不匹配'}")
print("\n【M 截距分母对偶】")
for r in M_rows:
    print(f"  m={r['m']}: {r['numerator_family']}/({r['domain_width']}·2^{r['m']}) = {r['intercept']}  恒等(1/7+1/(7·2^m)): {r['identity_check']}")
print(f"  M 全部恒等: {M_ok}")
print("\n【结论】", conclusion["verdict"])
print("  下一步候选:", conclusion["next_candidates"][0])
