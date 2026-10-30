# -*- coding: utf-8 -*-
"""δ 精确来源溯源探针（开放项⑤：δ=d_H−ln15=0.001783132，精度需求 ~1e−4 相对 0.01%）

框架常数库：2,3,4,5,6,7,8,15,16,17,35,36,42,60,128,136,137,675,
Δλ_min=(√3−1)/6, ln2, ln(16/15), ln15, 1/e≈0.367879

候选族：
  F1  ln(16/15)/N（N 大范围）
  F2  1/N
  F3  Δλ_min^p · k/m 组合
  F4  ln(16/15)·p/q
  F5  Δλ_min·ln(16/15)·k 组合
精度目标：<0.01% 相对（m_τ 链 0.1% 标准需 δ 到 ~1e−4 → 相对 0.56% 即可勉强，
但目标收紧到 0.01% 找精确候选）。
"""
import numpy as np
from itertools import product

delta = 16259/6000 - np.log(15)
D = (np.sqrt(3) - 1) / 6
ln1615 = np.log(16/15)
ln2 = np.log(2)
ln15 = np.log(15)
inv_e = 1/np.e

print(f"δ = {delta:.9f}（目标精度：相对 0.01% → ±{delta*1e-4:.3e}）")
print()

def report(name, v):
    rel = abs(v - delta)/delta*100
    flag = "★" if rel < 0.01 else ("✓" if rel < 0.1 else " ")
    print(f"  {flag} {name} = {v:.9f}  相对差 {rel:.4f}%")

print("=== F1：ln(16/15)/N（N=1..5000） ===")
best = None
for N in range(1, 5001):
    v = ln1615/N
    rel = abs(v - delta)/delta
    if best is None or rel < best[0]:
        best = (rel, N, v)
report(f"ln(16/15)/{best[1]}", best[2])
print(f"    最优 N={best[1]}（相对 {best[0]*100:.4f}%）")

print()
print("=== F2：1/N ===")
best = None
for N in range(1, 20000):
    v = 1/N
    rel = abs(v - delta)/delta
    if best is None or rel < best[0]:
        best = (rel, N, v)
report(f"1/{best[1]}", best[2])
print(f"    最优 N={best[1]}（相对 {best[0]*100:.4f}%）")

print()
print("=== F3：Δλ_min^p·k/m ===")
best = []
for p in (1, 2, 3):
    base = D**p
    for k in range(1, 100):
        for m in range(1, 100):
            v = base*k/m
            rel = abs(v - delta)/delta
            if rel < 0.005:
                best.append((rel, f"Δλ_min^{p}·{k}/{m}", v))
best.sort()
for rel, s, v in best[:5]:
    report(s, v)

print()
print("=== F4：ln(16/15)·p/q（p,q 小） ===")
best = []
for p in range(1, 100):
    for q in range(1, 100):
        v = ln1615*p/q
        rel = abs(v - delta)/delta
        if rel < 0.002:
            best.append((rel, f"ln(16/15)·{p}/{q}", v))
best.sort()
for rel, s, v in best[:5]:
    report(s, v)

print()
print("=== F5：Δλ_min·ln(16/15)·k ===")
best = []
for k in range(1, 50):
    for m in range(1, 20):
        v = D*ln1615*k/m
        rel = abs(v - delta)/delta
        if rel < 0.01:
            best.append((rel, f"Δλ_min·ln(16/15)·{k}/{m}", v))
best.sort()
for rel, s, v in best[:5]:
    report(s, v)

print()
print("=== F6：Δλ_min²/N、Δλ_min³/N、Δλ_min²·ln(16/15)/N ===")
best = []
for combo in product(range(1, 200), repeat=1):
    N = combo[0]
    for c, nm in [(D**2, "Δλ_min²"), (D**3, "Δλ_min³"), (D**2*ln1615, "Δλ_min²·ln(16/15)"), (D*ln1615**2, "Δλ_min·ln(16/15)²")]:
        v = c/N
        rel = abs(v - delta)/delta
        if rel < 0.003:
            best.append((rel, f"{nm}/{N}", v))
best.sort()
for rel, s, v in best[:6]:
    report(s, v)

print()
print("=== F7：ln15 基组合（ln15·k/m ± 修正） ===")
best = []
for k in range(1, 100):
    for m in range(2, 100):
        for j in range(1, 20):
            for sj in (+1, -1):
                v = ln15*k/m + sj*j*ln1615/100
                rel = abs(v - delta)/delta
                if rel < 0.002:
                    best.append((rel, f"ln15·{k}/{m}{'+' if sj>0 else '-'}{j}·ln(16/15)/100", v))
best.sort()
for rel, s, v in best[:4]:
    report(s, v)

print()
print("=== 结论 ===")
print("若 F1-F6 均无 <0.01% 命中 → δ 无简洁框架组合（0.01% 级），保持开放；")
print("若存在 ★ 命中 → 登记候选待判别（结构清洁性再评估）。")
