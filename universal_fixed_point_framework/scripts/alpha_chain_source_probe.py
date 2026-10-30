# -*- coding: utf-8 -*-
"""α⁻¹ 生成链溯源系统探索（#70，数值内生层命门）

目标：α⁻¹=137.035999084 能否由 Δφ=ln2 链/Cl(1,3) 结构常数组合内生。
结构常数库：2（每维 2 态）、4（时空维）、6（双向量=SO(1,3) 维数）、
8（2³）、15（16−1 非标量）、16（2⁴ 全态）、17（2⁴+1）、36（6²）、
128（2⁷）、136（2³(2⁴+1)=8×17）、137（136+1）、Δλ_min=(√3−1)/6、
ln2、ln15、ln(16/15)、d_H=16259/6000。

探索族：
  F1  2 的幂和差逼近 α⁻¹ 与余量
  F2  结构常数有理组合 k·(2^a±1)±j
  F3  余量 δ=α⁻¹−137 的 2 幂级数展开
  F4  Δλ_min/结构常数组合修正
  F5  ln 组合
"""
import numpy as np
from itertools import product

a_inv = 137.035999084
D = (np.sqrt(3) - 1) / 6
ln2 = np.log(2)
ln15 = np.log(15)
ln16 = np.log(16)
ln1615 = np.log(16/15)
dH = 16259/6000

print("=== 锚点 ===")
print(f"α⁻¹={a_inv:.9f}  137−α⁻¹={137-a_inv:.6f}  α⁻¹−136={a_inv-136:.6f}")
print(f"136=2^3(2^4+1)=8×17  137=128+8+1=2^7+2^3+2^0")
print(f"Δλ_min={D:.9f}  ln15={ln15:.9f}  ln(16/15)={ln1615:.9f}  d_H={dH:.9f}")
print()

print("=== F1：2 的幂和差逼近 α⁻¹（top 8，复杂度=项数） ===")
res = []
for a in range(0, 9):
    for b in range(0, 9):
        for c in range(0, 9):
            terms = [2**a, 2**b, 2**c]
            for s1 in (+1, -1):
                for s2 in (+1, -1):
                    v = 2**a + s1*2**b + s2*2**c
                    if v <= 0: continue
                    res.append((abs(v - a_inv), v, f"2^{a}{'+' if s1>0 else '-'}2^{b}{'+' if s2>0 else '-'}2^{c}"))
res.sort()
for d, v, s in res[:8]:
    print(f"  {s} = {v:.9f}  误差 {d:.6f}（{d/a_inv*100:.4f}%）")

print()
print("=== F2：结构常数组合 k·(2^a±1)±j 逼近 α⁻¹（top 8） ===")
res = []
for k in range(1, 20):
    for a in range(0, 9):
        base = k*(2**a + 1) if k*(2**a+1) > 0 else 0
        for j in range(0, 20):
            for s in (+1, -1):
                v = k*(2**a + 1) + s*j
                res.append((abs(v - a_inv), v, f"{k}·2^{a}+{k}{'+' if s>0 else '-'}{j}"))
            v = k*(2**a - 1) + j
            res.append((abs(v - a_inv), v, f"{k}·(2^{a}-1)+{j}"))
res.sort()
for d, v, s in res[:8]:
    print(f"  {s} = {v:.9f}  误差 {d:.6f}（{d/a_inv*100:.4f}%）")

print()
print("=== F3：余量 δ=α⁻¹−137=0.036 的 2 幂级数展开（top 6） ===")
delta = a_inv - 137
res = []
for n in range(1, 6):
    for combo in product(range(0, 12), repeat=n):
        v = sum(2**(-e) for e in combo) * (1 if all(x > 0 for x in combo) else 1)
        # 简化：只允许正的负幂和
        v = sum(2**(-e) for e in combo)
        res.append((abs(v - delta), v, "+".join(f"2^-{e}" for e in combo)))
res.sort()
for d, v, s in res[:6]:
    print(f"  {s} = {v:.9f}  误差 {d:.6e}（{d/delta*100:.4f}%）")

print()
print("=== F4：Δλ_min 组合修正（α⁻¹−136 的分解） ===")
gap_rem = a_inv - 136
print(f"α⁻¹−136 = {gap_rem:.9f}")
for p in range(1, 30):
    for q in range(1, 30):
        v = D * p / q
        rel = abs(v - gap_rem) / gap_rem
        if rel < 0.005:
            print(f"  Δλ_min·{p}/{q} = {v:.9f}  误差 {rel*100:.4f}%")
print(f"  136(1+Δλ_min/16) = {136*(1+D/16):.9f}  误差 {abs(136*(1+D/16)-a_inv)/a_inv*100:.4f}%")

print()
print("=== F5：ln 组合（top 6） ===")
res = []
for n in range(1, 40):
    for m in range(0, 40):
        for c in (+1, -1):
            v = n*ln15 + m*ln2 + c*ln1615
            res.append((abs(v - (a_inv - 128)), v, f"{n}·ln15{m:+.0f}·ln2{c:+.0f}·ln(16/15)+128"))
res.sort()
for d, v, s in res[:6]:
    print(f"  {s} = {v+128:.9f}  误差 {d:.6f}（{d/a_inv*100:.4f}%）")

print()
print("=== 结论 ===")
best = None
for a in range(0, 9):
    for b in range(0, 9):
        v = 2**a + 2**b + 1
        if best is None or abs(v - a_inv) < best[0]:
            best = (abs(v - a_inv), v, f"2^{a}+2^{b}+1")
print(f"最优 2 幂和候选：{best}")
print("注：F3 全枚举 6 项成本高，仅做 5 项内；137=2^7+2^3+2^0 为最简整数结构命中。")
