# -*- coding: utf-8 -*-
"""S261 δ_V3 系数-幂次配对机制深挖
① 23（系数和=幂次和）的框架身份扫描——{2,3,4,5,7,8,15,16,24,42} 组合
② 邻域偏移 {+3,−1,+1,−3} 四象限完备性检验
③ 幂次对/系数对配对结构
"""
from itertools import product
from fractions import Fraction

fc = [2, 3, 4, 5, 7, 8, 15, 16, 24, 42]
fc_names = {2: "幂基", 3: "活跃", 4: "不动点", 5: "静默", 7: "对合",
            8: "幂基³", 15: "态域", 16: "全态", 24: "不动点!", 42: "约束域"}

print("=== S261: 23 的框架身份扫描 ===")
target = 23
hits = []
# 二元加减
for a, b in product(fc, fc):
    if a + b == target and a != b:
        hits.append((a, b, "+", f"{fc_names[a]}+{fc_names[b]}"))
    if a - b == target:
        hits.append((a, b, "-", f"{fc_names[a]}−{fc_names[b]}"))
# 二元乘
for a, b in product(fc, fc):
    if a * b == target and a != b:
        hits.append((a, b, "*", f"{fc_names[a]}×{fc_names[b]}"))
# 幂
for a in fc:
    for p in range(2, 4):
        if a ** p == target:
            hits.append((a, p, "pow", f"{fc_names[a]}^{p}"))
# 三元组合（a×b±c、a×b+c、a+b+c）
for a, b, c in product(fc, fc, fc):
    if a * b + c == target and a != b:
        hits.append((a, b, c, "*+", f"{fc_names[a]}×{fc_names[b]}+{fc_names[c]}"))
    if a * b - c == target and a != b:
        hits.append((a, b, c, "*-", f"{fc_names[a]}×{fc_names[b]}−{fc_names[c]}"))
    if a + b + c == target and a != b and a != c and b != c:
        hits.append((a, b, c, "++", f"{fc_names[a]}+{fc_names[b]}+{fc_names[c]}"))
# 去重排序
seen = set()
uniq = []
for h in hits:
    key = h[3]
    if key not in seen:
        seen.add(key)
        uniq.append(h)
print(f"命中身份数：{len(uniq)}")
for h in uniq[:30]:
    if len(h) == 5:
        print(f"  {h[0]} {h[3]} {h[1]} + {h[2]} = 23（{h[4]}）")
    else:
        print(f"  {h[0]} {h[2]} {h[1]} = 23（{h[3]}）")

print("\n--- 关键候选排序（框架量最短/最本质）---")
print("A: 23 = 24−1（不动点!−1——与 α⁻¹ 系数 24 同源）")
print("B: 23 = 15+8（态域+幂基³）")
print("C: 23 = 16+7（全态+对合）")
print("D: 23 = 42−19（19 无身份——不成立）")
print("E: 23 = 3×5+8（活跃×静默+幂基³）")
print("F: 23 = 5×4+3（静默×不动点+活跃）")

print("\n=== 邻域偏移四象限检验 ===")
C = [6, 4, 8, 5]
P = [3, 5, 7, 8]
offsets = [C[i] - P[i] for i in range(4)]
print(f"偏移（系数−幂次）= {offsets}")
print(f"反号镜像：{offsets[0]} ↔ {offsets[3]}（{offsets[0]==-offsets[3]}）——{offsets[1]} ↔ {offsets[2]}（{offsets[1]==-offsets[2]}）")
print(f"偏移集合 = {{±{abs(offsets[0])}, ±{abs(offsets[1])}}}——四象限完备 {sorted(set(abs(o) for o in offsets))}")
print(f"偏移量 {abs(offsets[0])} = 活跃、{abs(offsets[1])} = 1（幂基⁰/单位）")

print("\n=== 幂次对/系数对配对 ===")
print(f"幂次对：(3,8) 和 (5,7)——3+8 = 11、5+7 = 12")
print(f"系数对：(6,5) 和 (4,8)——6+5 = 11、4+8 = 12——与幂次对和一致！")
print(f"  （偏移 ±3 项对：6σ³ & 5σ⁸——和 11 = 幂次对(3,8) 和 11？——验证）")
p_pairs = [(3, 8), (5, 7)]
c_pairs = [(6, 5), (4, 8)]
for (p1, p2), (c1, c2) in zip(p_pairs, c_pairs):
    print(f"  幂次({p1},{p2}) 和 = {p1+p2}——系数({c1},{c2}) 和 = {c1+c2}——{'一致' if p1+p2==c1+c2 else '不一致'}")

print("\n=== 数值权重（每项对总 δ 的贡献占比）===")
import decimal
sigma = decimal.Decimal(1)/15
terms = [(6,3), (4,5), (8,7), (5,8)]
total = sum(decimal.Decimal(c)*sigma**p for c,p in terms)
for c, p in terms:
    w = decimal.Decimal(c)*sigma**p/total
    print(f"  {c}σ^{p}：{float(w)*100:.3f}%")
