# -*- coding: utf-8 -*-
"""
P7-5e-194 · B*(1) 框架常数分解判别（193 的检验 P + Q）
用户推进（2026-10-15）。

检验 P 设计（B*(1)=455/332 的框架常数分解）：
P1. B*(1) = 455/332（闭式 129 精确值）
P2. 分子 455 = 7·65 = 7·5·13 = 域宽(7) × 修正锚点(65) = 域宽 × 隔位种子(5) × C分子(13)
P3. 65 = 5·13 = 隔位种子 × C分子（修正锚点的素数分解绑定两框架常数）
P4. 分母 332 = 4·83 = 4·(2·41+1) = 满格(4) × D分子线性(83=2·41+1)
P5. 1/B*(1) = 332/455 = [4·(2·41+1)]/[7·5·13] —— B*(1) 完全由框架常数表达
P6. m≥2 对照：B*(m) 分子 = 7·2^m（域宽×满格）；m=1 例外 = 7·5·13
    （修正把"域宽×满格"替换为"域宽×种子×C分子"）

检验 Q 设计（m=1 vs m=2 对称性，预期负）：
Q1. B*(1) = 455/332 ≈ 1.37048；B*(2) = 28/33 ≈ 0.84848
Q2. 比值 = 15015/9296 ≈ 21/13？→ 非精确（负）
Q3. 和/积无整洁（负）
"""
import json
from fractions import Fraction

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e194_bstar1_framework_decomposition.json"

# ---------- P1/P2 ----------
P1 = {
    "B1_inv": str(Fraction(332, 455)),
    "B1": str(Fraction(455, 332)),
    "B1_float": 455 / 332,
}
P2 = {
    "455_factorization": "455 = 7·65 = 7·5·13",
    "455_eq_7x65": 455 == 7 * 65,
    "455_eq_7x5x13": 455 == 7 * 5 * 13,
    "check": "分子 455 = 域宽(7) × 修正锚点(65) = 域宽 × 隔位种子(5) × C分子(13)",
}
P3 = {
    "65_eq_5x13": 65 == 5 * 13,
    "check": "65 = 5·13 = 隔位种子 × C分子（修正锚点素数分解绑定两框架常数）",
}
P4 = {
    "332_factorization": "332 = 4·83 = 4·(2·41+1)",
    "332_eq_4x83": 332 == 4 * 83,
    "83_eq_2x41_plus_1": 83 == 2 * 41 + 1,
    "check": "分母 332 = 满格(4) × D分子线性(83 = 2·41+1)",
}
P5 = {
    "B1_inv_decomposed": "1/B*(1) = [4·(2·41+1)] / [7·5·13]",
    "factors_all_framework": "7=域宽, 5=隔位种子(家族m2), 13=C分子(C=13/128), 41=D分子(D=41/2000), 4=2²",
}

# ---------- P6：m>=2 B* 分子对照 ----------
P6_rows = []
for m in range(1, 8):
    if m == 1:
        B_inv = Fraction(332, 455)
        B = Fraction(455, 332)
        num, den = B.numerator, B.denominator
    else:
        B_inv = Fraction(m, 2) + Fraction(1, 7) + Fraction(1, 7 * 2 ** m)
        B = 1 / B_inv
        num, den = B.numerator, B.denominator
    P6_rows.append({
        "m": m, "B_inv": str(B_inv), "B": str(B),
        "B_numerator": num, "B_denominator": den,
        "num_is_7x2m": num == 7 * 2 ** m,
        "num_factorization": f"7·2^{m}" if num == 7 * 2 ** m else f"{num}",
    })

# ---------- Q ----------
Q1 = {
    "B1": 455 / 332, "B2": 28 / 33,
}
Q2 = {
    "ratio": str((Fraction(455, 332)) / (Fraction(28, 33))),
    "ratio_str": str((Fraction(455, 332)) / (Fraction(28, 33))),  # 15015/9296
    "vs_21_13": str((Fraction(455, 332)) / (Fraction(28, 33)) - Fraction(21, 13)),
    "is_exact_21_13": (Fraction(455, 332)) / (Fraction(28, 33)) == Fraction(21, 13),
    "verdict": "比值 ≈ 21/13 仅近似非精确 → 无 Fibonacci 关系（负）",
}
Q3 = {
    "sum": str(Fraction(455, 332) + Fraction(28, 33)),
    "product": str(Fraction(455, 332) * Fraction(28, 33)),
    "verdict": "和/积无整洁框架形式（负）",
}

# ---------- 结论 ----------
conclusion = {
    "verdict": "B*(1) 完全由框架常数表达：1/B*(1) = [4·(2·41+1)]/[7·5·13]（分母 7·65 = 域宽×修正锚点，65=5·13=隔位种子×C分子；分子 332=4·83=满格×D分子线性）——候选结构；m≥2 的 B* 分子 = 7·2^m（域宽×满格），m=1 例外把'域宽×满格'替换为'域宽×种子×C分子'；Q 负（无 m=1/m=2 对称性）",
    "P": {
        "P1": str(Fraction(455, 332)),
        "P2": P2["check"],
        "P3": P3["check"],
        "P4": P4["check"],
        "P5": "1/B*(1) = [4·(2·41+1)] / [7·5·13]——B*(1) 完全由框架常数（域宽7、隔位种子5、C分子13、D分子41、满格4）表达",
        "P6": "m≥2 B* 分子 = 7·2^m（域宽×满格）；m=1 例外 = 455 = 7·5·13——修正把'域宽×满格'替换为'域宽×种子×C分子'",
    },
    "Q": {
        "Q2": Q2["verdict"],
        "Q3": Q3["verdict"],
        "verdict": "负（无 m=1/m=2 对称性）",
    },
    "honest_limits": [
        "素数分解可巧合；判别靠'因子均为已锁定框架常数'+'m=1 唯一性'的语境强度——登记为候选结构非定案",
        "65=5·13 的'隔位种子×C分子'绑定是新身份重合（65 已有四重身份，现第五重）",
        "m≥2 分子 7·2^m 是直接代数（B*(m)=1/(m/2+截距)），非新发现",
        "继承 187-193 候选层",
    ],
    "next_candidates": [
        "检验 R：C 分子 13 与 D 分子 41 的线性关系族（83=2·41+1；是否还有 13 的线性出现在其他锁定量的分母/分子）",
        "检验 S：B*(m) 分母序列 {332,33,93,241,593,1409,...} 的 2 进/家族结构",
        "窗口 2 家族段判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-194 · B*(1) 框架常数分解判别",
    "date": "2026-10-15",
    "P1": P1, "P2": P2, "P3": P3, "P4": P4, "P5": P5,
    "P6_rows": P6_rows,
    "Q1": Q1, "Q2": Q2, "Q3": Q3,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---------- 控制台 ----------
print("=" * 72)
print("P7-5e-194 · B*(1) 框架常数分解判别")
print("=" * 72)
print("\n【P1 精确值】")
print(f"  1/B*(1) = {P1['B1_inv']}；B*(1) = {P1['B1']} = {P1['B1_float']:.8f}")
print("\n【P2 分子 455】")
print(f"  455 = 7·65？ {P2['455_eq_7x65']}；455 = 7·5·13？ {P2['455_eq_7x5x13']}")
print(f"  {P2['check']}")
print("\n【P3 65 = 5·13】")
print(f"  65 = 5·13？ {P3['65_eq_5x13']}；{P3['check']}")
print("\n【P4 分母 332】")
print(f"  332 = 4·83？ {P4['332_eq_4x83']}；83 = 2·41+1？ {P4['83_eq_2x41_plus_1']}")
print(f"  {P4['check']}")
print("\n【P5 完整分解】")
print(f"  1/B*(1) = {P5['B1_inv_decomposed']}")
print(f"  因子：{P5['factors_all_framework']}")
print("\n【P6 m>=2 分子对照】")
for r in P6_rows:
    print(f"  m={r['m']}: B*(m) = {r['B']:<12} 分子 = {r['B_numerator']:<5} 7·2^{r['m']}？ {r['num_is_7x2m']}")
print("\n【Q m=1 vs m=2】")
print(f"  B*(1) = {Q1['B1']:.8f}，B*(2) = {Q1['B2']:.8f}")
print(f"  比值 = {Q2['ratio_str']} vs 21/13：差 = {Q2['vs_21_13']}（精确？ {Q2['is_exact_21_13']}）→ {Q2['verdict']}")
print(f"  和 = {Q3['sum']}，积 = {Q3['product']} → {Q3['verdict']}")
print("\n【结论】", conclusion["verdict"])
print("  下一步候选:", conclusion["next_candidates"][0])
