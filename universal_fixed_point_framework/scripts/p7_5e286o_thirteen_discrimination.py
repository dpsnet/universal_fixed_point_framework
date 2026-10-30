# -*- coding: utf-8 -*-
"""判别④ 13 生成链表达判别（2k_max-3 vs k_max+5）：
通式恒等 2k_max-3 = k_max+(k_max-3)；k_max=8 时 = k_max+5（E2 值集末项视角）。
闭式组装语言一致性：{k_max, k_max-3, 积±1, 2 幂, 16(k_max-3)^3}。
"""
from fractions import Fraction

print("== 13 通式恒等 ==")
for K in [8, 9, 7, 6, 12]:
    a = 2 * K - 3
    b = K + (K - 3)
    c = K + 5 if K == 8 else None
    line = f"k_max={K}: 2k_max-3={a}  k_max+(k_max-3)={b}  equal={a == b}"
    if c is not None:
        line += f"  k_max+5={c}  (k_max=8 特例) equal={a == c}"
    print(line)

print("\n== 闭式组装语言一致性（k_max=8） ==")
# 系数 -> 组装语言成员
items = [
    ("m/2      ", "k_max·m/16", "k_max"),
    ("1/8      ", "1/k_max", "k_max"),
    ("13/128   ", "(2k_max-3)/2^(k_max-1)", "k_max+(k_max-3) 与 2 幂"),
    ("41/2000  ", "(k_max(k_max-3)+1)/(16(k_max-3)^3)", "k_max·(k_max-3)+1"),
    ("39/2000  ", "(k_max(k_max-3)-1)/(16(k_max-3)^3)", "k_max·(k_max-3)-1"),
]
for name, expr, lang in items:
    print(f"{name} {expr}   组装语言: {lang}")

print("\n== 判别结论 ==")
print("2k_max-3 = k_max+(k_max-3) 通式恒等（任意 k_max）；k_max=8 时 = k_max+5（E2 值集末项，Demirror §11 邻域 {3,5,7,13}）。")
print("闭式/Lean（k8_C）规范化表达 = 2k_max-3 = k_max+(k_max-3)（框架成员和，与 39/41/2000 组装语言同构）；")
print("k_max+5 为 BowlChain i(2) 候选/E2 值集视角的等价写法（同值 13）。非真并列，判别闭环。")
