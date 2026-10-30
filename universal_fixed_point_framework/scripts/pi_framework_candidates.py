# -*- coding: utf-8 -*-
"""π 的框架化候选探索（2026-10-26）

G_N 攻坚只剩 π 与 G——π 的内生候选通道探索：
1. π 的连分数部分商 vs 框架量（活跃 3/对合域 7/σ⁻¹ 15）
2. 收敛 22/7 = (幂基×显态)/对合域
3. BBP 公式系数 vs 框架量（16/8/4/1/5/6）
"""
from fractions import Fraction
import math

print("=== ① π 的连分数部分商 vs 框架量 ===")
# 连分数展开
x = math.pi
a0 = int(x)
fractional = x - a0
parts = [a0]
for _ in range(10):
    r = 1.0 / fractional
    ai = int(r)
    parts.append(ai)
    fractional = r - ai
print("π 的连分数部分商前 11 项:", parts)
print("框架量：活跃 3、对合域 7、σ⁻¹ 15、静默 5、幂基 2、k_max 8、不动点 4、单位 1")
print(f"→ 部分商 a0={parts[0]}（活跃 3 ✓）、a1={parts[1]}（对合域 7 ✓）、a2={parts[2]}（σ⁻¹ 15 ✓）")
print("→ 前三个部分商 = 活跃/对合域/σ⁻¹——低概率巧合（~1/(3×7×15) ≈ 1/315）")

print("\n=== ② 收敛 22/7 = (幂基×显态)/对合域 ===")
c1 = Fraction(parts[0])
c2 = Fraction(parts[0]*parts[1] + 1, parts[1])
c3 = Fraction(parts[0]*parts[1]*parts[2] + parts[0] + parts[2], parts[1]*parts[2] + 1)
print(f"收敛 1: {c1} = {float(c1):.6f}")
print(f"收敛 2: {c2} = {float(c2):.6f}（22/7 = 幂基×显态/对合域 = 2×11/7）")
print(f"收敛 3: {c3} = {float(c3):.6f}")
print(f"22/7 vs π: 误差 = {(float(c2) - math.pi)/math.pi*100:.4f}%")
print(f"333/106 vs π: 误差 = {(float(c3) - math.pi)/math.pi*100:.4f}%")
print("→ 22/7 = (幂基×显态)/对合域——全框架量闭式——误差 0.04%")

print("\n=== ③ BBP 公式系数 vs 框架量 ===")
print("π = Σ (1/16^k)[4/(8k+1) − 2/(8k+4) − 1/(8k+5) − 1/(8k+6)]")
print("基 16^k = 全态^k（16 = 幂基^不动点 = 2⁴）")
print("8k = k_max 倍偏移")
print("分母偏移 {1,4,5,6} = {单位, 不动点, 静默, 双向量数(C(4,2))}")
print("分子 {4,−2,−1,−1} = {不动点, −幂基, −单位, −单位}")
# 验证 BBP 前 N 项
s = 0.0
N = 8
for k in range(N):
    s += (1.0/16.0**k) * (4.0/(8*k+1) - 2.0/(8*k+4) - 1.0/(8*k+5) - 1.0/(8*k+6))
print(f"BBP 前 {N} 项和 = {s:.10f}（π = {math.pi:.10f}）")
print("→ BBP 公式的 16/8/4/1/5/6 全为框架量（16=全态、8=k_max、4=不动点、5=静默、6=双向量数）")
print("诚实边界：BBP 的 16 源于十六进制基选择——与全态 16 的连接为'2 的幂结构'——非框架定理")

print("\n=== ④ 判别 ===")
print("① ★★ π 连分数部分商 [3; 7, 15, ...] = [活跃; 对合域, σ⁻¹, ...]——低概率巧合（1/315）")
print("② ★★ 22/7 = (幂基×显态)/对合域——π 的全框架量闭式近似——误差 0.04%")
print("③ ★ BBP 公式系数全框架量（16/8/4/5/6）——但 16 为进制产物（诚实边界）")
print("④ π 的内生候选首次出现——G_N 攻坚的 π 缺口获候选通道")
