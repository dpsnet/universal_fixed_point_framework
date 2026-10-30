# -*- coding: utf-8 -*-
# S103 G2 桥闭合候选先证伪（2026-10-27）
# 候选：K_max=8 层递归后谱流 rapidity = 8·ln2 = ln(2^8) = ln 256
#   256 三重身份：2^8（幂基翻倍）、16^2（16 态窗口平方）、Σ_{k<=8}choose(8,k)（组合计数）
# 连接 S101：Σchoose(8,k)=256 是卷积系数恒等锚的结构来源
# 连接翻倍说：Δφ=ln2 已锚定（用户确认——勾股族 3-4-5/8-15-17/...）

import math
from math import comb

print("=== 1. 8·ln2 = ln(2^8) = ln 256（对数值） ===")
v1 = 8 * math.log(2)
v2 = math.log(256)
print(f"8·ln2 = {v1:.12f}   ln256 = {v2:.12f}   diff = {abs(v1 - v2):.3e}")

print("\n=== 2. 256 三重身份 ===")
print(f"2^8 = {2**8}")
print(f"16^2 = {16**2}")
s = sum(comb(8, k) for k in range(9))
print(f"Σ_{{k<=8}} choose(8,k) = {s}")
print(f"三重一致: {2**8 == 16**2 == s == 256}")

print("\n=== 3. 与 S101 锚的连接（conv_coeff_anchor_8 的分母） ===")
print(f"1/8! = {1/math.factorial(8):.10f}  256·(0.5^8)/8! = {256 * 0.5**8 / math.factorial(8):.10f}")
print(f"验证: 0.5^8·256/8! = 1/8!?  {256 * 0.5**8 == 1}")

print("\n=== 4. 分层 rapidity 勾股族（翻倍说——已锚定） ===")
for n in range(1, 5):
    v = math.tanh(n * math.log(2))
    # 有理勾股 (g^2-1)/(g^2+1), g = 2^n
    g = 2**n
    rat = (g*g - 1) / (g*g + 1)
    print(f"n={n}: tanh({n}·ln2) = {v:.10f}  (2^{2*n}-1)/(2^{2*n}+1) = {rat:.10f}  diff={abs(v-rat):.2e}")

print("\n=== 5. G2 桥闭合表述 ===")
print(f"8 层递归（K_max=8）后 rapidity = 8·ln2 = ln256")
print(f"ln256 = ln(2^8) = ln(16^2) = ln(Σ_{{k<=8}}choose(8,k))——谱流位置的对数 = 框架计数")
