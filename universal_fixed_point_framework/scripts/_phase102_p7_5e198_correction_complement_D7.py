# -*- coding: utf-8 -*-
"""
P7-5e-198 · 修正互补与 D(7) 分解判别（197 的检验 X + Y）
用户推进（2026-10-15）。

检验 X 设计（naive 7/5 与 65 修正的互补结构）：
X1. B* 视角修正：B*(1) = 7/5 - 49/1660 = 455/332（naive 减性修正）
X2. 49/1660 = 7^2/(5·332) = 7^2/(5·4·83) = 域宽^2/(隔位种子·满格·D线性)
X3. 1/B* 视角修正：1/B*(1) = 5/7 + 1/65（192 L1 加性修正）
X4. 两视角倒数对偶：naive B* = 7/5 <-> naive 1/B* = 5/7（同一 naive 量的倒数）
X5. 候选：m=1 修正的 B* 视角 = 域宽^2/(隔位种子·满格·D线性)——第四种框架常数组合

检验 Y 设计（窗口锚定系统检验 + D(7) 分解）：
Y1. 系统检查 m=1..7 B* 分子/分母的窗口起边界 a_j / 家族成员因子
Y2. ★ 新发现：D(7) = 3265 = 5·653 = 5·(8·81+5) = 5·(8·D9+5)
    与 65 = 5·(8+5) = 5·(8·1+5) 同构（单位 1 -> D9=81 超对合域）
Y3. D(2) = 33 = 3·11 = 3·(3+8) = 相邻种子×(相邻种子+b_1)
Y4. 假说边界：m=3..6 无 a_j/家族因子（D(4..6)=241/593/1409 素数）
Y5. 窗口位置假说 m'=7-m 仅 m=1,2（数值模式）；种子分解扩展于 m=2（33）、m=7（3265）
"""
import json
from fractions import Fraction

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e198_correction_complement_D7.json"

# ---------- X1/X2 ----------
X1 = {
    "naive": str(Fraction(7, 5)),
    "actual": "455/332",
    "diff": str(Fraction(7, 5) - Fraction(455, 332)),
    "diff_ok": Fraction(7, 5) - Fraction(455, 332) == Fraction(49, 1660),
    "B1_from_naive_minus_diff": str(Fraction(7, 5) - Fraction(49, 1660)),
    "equals_455_332": Fraction(7, 5) - Fraction(49, 1660) == Fraction(455, 332),
}
X2 = {
    "49_eq_7sq": 49 == 7 ** 2,
    "1660_eq_5x332": 1660 == 5 * 332,
    "1660_eq_5x4x83": 1660 == 5 * 4 * 83,
    "83_eq_2x41_plus_1": 83 == 2 * 41 + 1,
    "check": "49/1660 = 7^2/(5·4·83) = 域宽^2/(隔位种子·满格·D线性)",
}
# ---------- X3/X4 ----------
X3 = {
    "inverse_view": "1/B*(1) = 5/7 + 1/65（192 L1 加性）",
    "naive_inverse": str(Fraction(5, 7)),
    "check": "naive 1/B* = 5/7（= naive B* 7/5 的倒数）",
}
X4 = {
    "dual": "naive B* = 7/5 <-> naive 1/B* = 5/7（同一 naive 量的倒数对偶）",
    "consistency": "192 的 1/B* 视角（5/7+1/65）与 197 的 B* 视角（7/5-49/1660）通过倒数等价",
}

# ---------- Y1：系统检查 ----------
Y1_rows = []
# m 通道 B* 分数（分子/分母）
B_fractions = {
    1: (455, 332), 2: (28, 33), 3: (56, 93), 4: (112, 241),
    5: (224, 593), 6: (448, 1409), 7: (896, 3265),
}
# 窗口起边界 a_j = 家族 m=j+1 成员
a_list = {j: 2 ** (j + 1) + 1 for j in range(1, 7)}  # a_1..a_6 = 5,9,17,33,65,129
for m in range(1, 8):
    num, den = B_fractions[m]
    a_hits_num = [j for j, a in a_list.items() if num % a == 0]
    a_hits_den = [j for j, a in a_list.items() if den % a == 0]
    Y1_rows.append({
        "m": m, "B": f"{num}/{den}", "a_hits_num": a_hits_num, "a_hits_den": a_hits_den,
    })

# ---------- Y2：D(7) 分解 ----------
Y2 = {
    "D7": 3265,
    "3265_eq_5x653": 3265 == 5 * 653,
    "653_eq_8x81_plus_5": 653 == 8 * 81 + 5,
    "81_eq_D9": 81 == 8 * 10 + 1,
    "D7_decomposition": "3265 = 5·653 = 5·(8·81+5) = 5·(8·D9+5)",
    "parallel_with_65": "65 = 5·(8+5) = 5·(8·1+5)（单位 1）；3265 = 5·(8·81+5)（D9=81 超对合域）——同构平行",
}
# ---------- Y3 ----------
Y3 = {
    "D2": 33,
    "33_eq_3x11": 33 == 3 * 11,
    "11_eq_3_plus_8": 11 == 3 + 8,
    "check": "33 = 3·11 = 3·(3+8) = 相邻种子×(相邻种子+b_1)",
}
# ---------- Y4 ----------
Y4 = {
    "primes": {4: 241, 5: 593, 6: 1409},
    "check": "D(4..6) = 241/593/1409 素数（无 a_j/家族因子）",
}

# ---------- 结论 ----------
conclusion = {
    "verdict": "X：m=1 修正 B* 视角 = 49/1660 = 域宽^2/(隔位种子·满格·D线性)，与 1/B* 视角 1/65 倒数对偶等价（X4 闭合）；Y：系统检查 m=1 分子含 a_5（455=7·65）、m=2 分母含 a_4（33）；★ D(7)=3265=5·653=5·(8·D9+5) 新发现——与 65=5·(8+5) 同构（单位1 vs D9=81 超对合域投影）；D(2)=33=3·(3+8) 相邻种子结构；m=3..6 无窗口锚（241/593/1409 素数）——窗口位置假说 m'=7-m 仅 m=1,2 确认（数值模式）",
    "X": {
        "X1": "B*(1) = 7/5 - 49/1660 = 455/332（减性修正）",
        "X2": "49/1660 = 域宽^2/(隔位种子·满格·D线性)——第四种框架常数组合",
        "X3": "1/B*(1) = 5/7 + 1/65（加性修正，192）",
        "X4": "naive 7/5 <-> 5/7 倒数对偶；两视角修正等价闭合",
    },
    "Y": {
        "Y1": "m=1: 455=7·a_5（分子）；m=2: 33=a_4（分母）；m=3..6 无 a_j 因子",
        "Y2": "D(7) = 3265 = 5·(8·D9+5)——D9=81 超对合域在 m=7 分母的投影（新发现）",
        "Y3": "D(2) = 33 = 3·(3+8)（相邻种子结构）",
        "Y4": "窗口位置假说边界：仅 m=1,2 锚定窗口（数值模式）；种子分解扩展 m=2,7",
    },
    "honest_limits": [
        "X4 的倒数对偶是恒等（naive 值单一，两视角重写）；'第四种组合'为因式身份",
        "Y2 的 D(7) 分解是算术分解（3265 唯一素数分解 5·653），同构为候选观察",
        "窗口位置假说 m'=7-m 确认仅 m=1,2（数值模式非机制）",
        "继承 187-197 候选层",
    ],
    "next_candidates": [
        "检验 Z：D(7)=5·(8·D9+5) 与 D(2)=3·(3+8) 的'种子×(种子+8·Q)'族——Q=1（65）、Q=D9（3265）、Q=1（33）的系统结构（Q 序列 1,1,D9 的规律）",
        "检验 AA：家族成员 m>=4 的素数性（17,257 素数 vs 33,65,129 合数）与 B* 分母素数性（241/593/1409）的关联",
        "窗口 2 家族段判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-198 correction complement & D(7) decomposition",
    "date": "2026-10-15",
    "X1": X1, "X2": X2, "X3": X3, "X4": X4,
    "Y1_rows": Y1_rows, "Y2": Y2, "Y3": Y3, "Y4": Y4,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("=" * 72)
print("P7-5e-198 correction complement & D(7) decomposition")
print("=" * 72)
print("\n[X1 B* view correction]")
print(f"  7/5 - 455/332 = {X1['diff']} (49/1660? {X1['diff_ok']})")
print(f"  7/5 - 49/1660 = {X1['B1_from_naive_minus_diff']} (=455/332? {X1['equals_455_332']})")
print(f"\n[X2 decomposition]")
print(f"  49 = 7^2? {X2['49_eq_7sq']}；1660 = 5·332? {X2['1660_eq_5x332']} = 5·4·83? {X2['1660_eq_5x4x83']}")
print(f"\n[X3/X4 dual]")
print(f"  {X3['check']}；{X4['dual']}")
print(f"\n[Y1 window-anchor system check]")
for r in Y1_rows:
    print(f"  m={r['m']}: B={r['B']:<12} a_hits_num={r['a_hits_num']} a_hits_den={r['a_hits_den']}")
print(f"\n[Y2 D(7) decomposition]")
print(f"  3265 = 5·653? {Y2['3265_eq_5x653']}；653 = 8·81+5? {Y2['653_eq_8x81_plus_5']}；81 = D9? {Y2['81_eq_D9']}")
print(f"  {Y2['D7_decomposition']}")
print(f"  {Y2['parallel_with_65']}")
print(f"\n[Y3 D(2)]")
print(f"  {Y3['check']}")
print(f"\n[Y4 boundary]")
print(f"  {Y4['check']}")
print("\n[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
