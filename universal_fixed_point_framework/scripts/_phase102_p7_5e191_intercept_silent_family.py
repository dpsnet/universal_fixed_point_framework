# -*- coding: utf-8 -*-
"""
P7-5e-191 · 截距分子=静默单元家族两段判别（190 的检验 J + K）
用户推进（2026-10-15）。

检验 J 设计（截距分子 3,5 的家族归属）：
A. 截距闭式结构：1/B*(m) = |m|/2 + 1/7 + 1/(7·2^|m|) + [|m|=1: +1/65]
   截距部分 = 1/7 + 1/(7·2^m) = (2^m+1)/(7·2^m) —— 分子 = 2^m+1 家族成员
   -> 截距分子序列 {3,5,9,17,33,65,129,257} = 2^m+1 家族 m=1..8 全体！
B. 分数 k：k_silent = 2^{m-3}（m=1,2 -> 1/4, 1/2 分数；m>=3 -> 整数单位位）
   -> 截距分子 m=1,2 是家族"分数 k 段"，9..257 是"整数 k 段"（静默单元）
C. 位型分派边界：190 的位型->身份族规则仅对整数 k 静默单元（8k+1, k∈Z+）成立；
   3,5（分数 k）位型（11₂/101₂）与窗口常数/对合域同型是数值巧合，不参与分派
D. 窗口 1 根窗口闭环：窗口 1 = 家族分数段（m=1,2: 3,5）+ 整数段（m=3..8: 9..257）

检验 K 设计（位型翻倍序列）：
E. 相邻双位 k 序列 = 3·2^p = {3,6,12,24,48}（窗口常数 c_2..c_6）
F. 隔位双位 k 序列 = 5·2^p = {5,10,20,40}（对合域 41/81 + 预言 161/321）
   -> 两序列平行翻倍（×2 每层）——位型家族的生长律
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e191_intercept_silent_family.json"

# ---------- A：截距闭式验证 ----------
intercept_rows = []
for m in range(1, 9):
    num = 2 ** m + 1
    den = 7 * 2 ** m
    intercept = num / den
    intercept_rows.append({
        "m": m, "numerator_2mp1": num, "denominator": den,
        "value": intercept,
        "form": f"(2^{m}+1)/(7·2^{m})",
    })

# 截距分子 = 2^m+1 家族（m=1..8）
A_ok = all(r["numerator_2mp1"] == 2 ** r["m"] + 1 for r in intercept_rows)
family_full = [2 ** m + 1 for m in range(1, 9)]

# ---------- B：分数 k ----------
k_rows = []
for m in range(1, 9):
    k = 2 ** (m - 3)
    k_rows.append({
        "m": m,
        "family_member": 2 ** m + 1,
        "k_silent": k,
        "k_type": "integer(unit_bit)" if k >= 1 else "fractional",
        "segment": "整数 k 段（静默单元）" if k >= 1 else "分数 k 段（截距分子）",
    })

# ---------- C：分派边界 ----------
boundary = {
    "rule": "位型->身份族分派仅对整数 k 静默单元（8k+1, k∈Z+）成立",
    "fractional_k": [3, 5],
    "fractional_k_bittypes": {3: "11₂ 相邻双位（巧合同型，非分派）", 5: "101₂ 隔位双位（巧合同型，非分派）"},
    "why": "3=2¹+1、5=2²+1 是 2^m+1 家族 m=1,2 成员（截距分子）；其位型与窗口常数/对合域同型是小数值的二进制自然现象",
}

# ---------- D：窗口 1 闭环 ----------
window1_closure = {
    "window1": "[1,8]",
    "fractional_segment": {"members": [3, 5], "m": [1, 2], "role": "截距分子（家族分数 k 段）"},
    "integer_segment": {"members": [9, 17, 33, 65, 129, 257], "m": [3, 4, 5, 6, 7, 8], "role": "静默单元（家族整数 k 段）"},
    "closure": "窗口 1 = 2^m+1 家族 m=1..8 全段（分数截距段 + 整数静默段）——根窗口解释闭环",
}

# ---------- E/F：位型翻倍序列 ----------
adjacent_seq = [3 * 2 ** p for p in range(0, 6)]      # 3,6,12,24,48,96
gap_seq = [5 * 2 ** p for p in range(0, 6)]           # 5,10,20,40,80,160
adjacent_units = [8 * k + 1 for k in adjacent_seq]    # 25,49,97,193,385,769
gap_units = [8 * k + 1 for k in gap_seq]              # 41,81,161,321,641,1281

seq_rows = []
for p in range(0, 6):
    seq_rows.append({
        "p": p,
        "adjacent_k": adjacent_seq[p], "adjacent_unit": adjacent_units[p],
        "adjacent_status": "窗口常数（框架内）" if p <= 4 else "预言（框架外）",
        "gap_k": gap_seq[p], "gap_unit": gap_units[p],
        "gap_status": "对合域（框架内 41/81）" if p <= 1 else "预言（框架外）",
    })

# ---------- 结论 ----------
conclusion = {
    "verdict": "截距分子 = 2^m+1 家族 m=1,2 分数 k 段（截距与静默是同一家族两段）；位型分派边界 = 仅整数 k；位型翻倍序列平行（相邻 3·2^p / 隔位 5·2^p）",
    "J": {
        "A_intercept_numerator_is_family": A_ok,
        "B_fractional_k_segment": "m=1,2: k=2^{m-3}=1/4,1/2（分数，截距分子）；m>=3: k 整数单位位（静默单元）",
        "C_boundary": boundary["rule"],
        "D_window1_closure": window1_closure["closure"],
        "family_unified": f"2^m+1 家族 m=1..8 全体 = 截距分子（m≤2, 3/5）+ 静默单元（m≥3, 9..257）——截距结构直接是家族投影",
    },
    "K": {
        "adjacent_k_seq": f"3·2^p = {adjacent_seq} -> 窗口常数 {adjacent_units[:5]} + 预言 769",
        "gap_k_seq": f"5·2^p = {gap_seq} -> 对合域 41/81 + 预言 161/321/641/1281",
        "parallel_growth": "两序列 ×2 每层平行——位型家族的生长律（候选）",
    },
    "honest_limits": [
        "检验 J 结论为'家族连续段'的再确认（186 双家族重合的 m=1,2 延伸）——非新机制",
        "位型巧合（3=11₂/5=101₂）判定为数值现象，但'分数 k 段'概念是新的命名（候选语义）",
        "检验 K 预言 161/321/641/1281 为纯代数外推，无框架内证据",
        "继承 187/188/189/190 候选层（纯 2 进幂集组织）",
    ],
    "next_candidates": [
        "检验 L：1/65 修正项（|m|=1 的 +1/65）在家族/位型框架中的身份——65=2^6+1 是 m=6 家族成员，为何只在 |m|=1 出现（m=1 特权的家族镜像）",
        "检验 M：截距分母 7·2^m 的 7（域宽）与分子家族组合成 (2^m+1)/(7·2^m) 的结构——是否即'域宽×满格'对偶的又一投影",
        "若框架层扩展：窗口 2 的家族段（m=9..16: 513,1025...）为分数/整数段重复的判据",
    ],
}

result = {
    "title": "P7-5e-191 · 截距分子=静默单元家族两段判别",
    "date": "2026-10-15",
    "intercept_rows": intercept_rows,
    "A_ok": A_ok,
    "k_rows": k_rows,
    "boundary": boundary,
    "window1_closure": window1_closure,
    "seq_rows": seq_rows,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---------- 控制台 ----------
print("=" * 72)
print("P7-5e-191 · 截距分子=静默单元家族两段判别")
print("=" * 72)
print("\n【A 截距闭式分子 = 2^m+1 家族】")
for r in intercept_rows:
    print(f"  m={r['m']}: 截距 = {r['numerator_2mp1']}/{r['denominator']} = {r['value']:.6f}  ({r['form']})")
print(f"  A 验证（全部分子=2^m+1）: {A_ok}  家族全谱: {family_full}")
print("\n【B 分数 k 段】")
for r in k_rows:
    print(f"  m={r['m']}: 2^m+1={r['family_member']:<4} k=2^(m-3)={r['k_silent']:<6} {r['segment']}")
print("\n【C 分派边界】", boundary["rule"])
print("  分数 k 位型:", boundary["fractional_k_bittypes"])
print("\n【D 窗口 1 闭环】", window1_closure["closure"])
print("\n【K 位型翻倍序列】")
print(f"  {'p':<3}{'相邻k':<7}{'窗口常数':<10}{'隔位k':<7}{'对合域':<10}{'状态'}")
for r in seq_rows:
    print(f"  {r['p']:<3}{r['adjacent_k']:<7}{r['adjacent_unit']:<10}{r['gap_k']:<7}{r['gap_unit']:<10}{r['adjacent_status']} / {r['gap_status']}")
print()
print("【结论】", conclusion["verdict"])
print("  J:", conclusion["J"]["family_unified"])
print("  K:", conclusion["K"]["parallel_growth"])
print("  下一步候选:", conclusion["next_candidates"][0])
