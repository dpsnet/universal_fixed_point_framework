# -*- coding: utf-8 -*-
"""δ 精确来源溯源第二轮（开放项⑤：新候选族）

第一轮无清洁命中。第二轮新增候选族：
  G1  m_τ 反解差分：dH(m_τ 反解)−ln15
  G2  双谱隙自洽点差分：d_H*−ln15（104az-152 d_H*=2.708258）
  G3  Δλ_min³ 修正族（Δλ_min³·(1±1/N)、Δλ_min³±k·ln(16/15)/N）
  G4  δ 的 ln 差分：ln(16/15)−k·Δλ_min 型
  G5  组合：Δλ_min²·(3/5)^m、Δλ_min·(3/5)^m/ln2
目标精度：<0.01% 相对（δ=0.001783132）
"""
import numpy as np

delta = 16259/6000 - np.log(15)
D = (np.sqrt(3) - 1) / 6
ln1615 = np.log(16/15)
ln2 = np.log(2)
ln15 = np.log(15)
E_tau = 43.37394
dH_mtau = (E_tau - ln1615/3) / 16
d_star = 2.708258

print(f"δ = {delta:.9f}")
print(f"G1: dH(m_τ 反解) = {dH_mtau:.9f}，dH(m_τ)−ln15 = {dH_mtau - ln15:.9f}")
print(f"    相对差 δ：{abs((dH_mtau-ln15)-delta)/delta*100:.3f}%")
print(f"G2: d_H*−ln15 = {d_star - ln15:.9f}，相对差 δ：{abs((d_star-ln15)-delta)/delta*100:.3f}%")
print()

def report(name, v):
    rel = abs(v - delta)/delta*100
    flag = "★" if rel < 0.01 else ("✓" if rel < 0.1 else " ")
    print(f"  {flag} {name} = {v:.9f}  相对差 {rel:.4f}%")

print("=== G3：Δλ_min³ 修正族 ===")
D3 = D**3
report("Δλ_min³", D3)
for N in range(2, 200):
    v = D3*(1 - 1/N)
    rel = abs(v - delta)/delta
    if rel < 0.01:
        report(f"Δλ_min³·(1−1/{N})", v)
for k in range(1, 20):
    for N in range(2, 100):
        v = D3 - k*ln1615/N
        rel = abs(v - delta)/delta
        if rel < 0.01:
            report(f"Δλ_min³−{k}·ln(16/15)/{N}", v)

print()
print("=== G4：ln(16/15) 与 Δλ_min 的线性组合 ===")
for k in range(1, 30):
    for m in range(1, 30):
        v = ln1615*k - D*m
        if v > 0:
            rel = abs(v - delta)/delta
            if rel < 0.005:
                report(f"{k}·ln(16/15)−{m}·Δλ_min", v)
        v = D*m - ln1615*k
        if v > 0:
            rel = abs(v - delta)/delta
            if rel < 0.005:
                report(f"{m}·Δλ_min−{k}·ln(16/15)", v)

print()
print("=== G5：谱隙×勾股比组合 ===")
for m in range(1, 12):
    for N in range(1, 60):
        v = D*(3/5)**m/N
        rel = abs(v - delta)/delta
        if rel < 0.01:
            report(f"Δλ_min·(3/5)^{m}/{N}", v)
        v = D**2*(3/5)**m/N
        rel = abs(v - delta)/delta
        if rel < 0.01:
            report(f"Δλ_min²·(3/5)^{m}/{N}", v)
        v = D**3*(3/5)**m*N
        rel = abs(v - delta)/delta
        if rel < 0.01:
            report(f"Δλ_min³·(3/5)^{m}·{N}", v)

print()
print("=== G6：δ 与静默窗口 1/15 的关系 ===")
report("ln(15/14.9732)/N=ln(1.00179)≈δ 观察", np.log(16259*15/6000) - np.log(15) if False else delta)
print(f"  e^δ−1 = {np.exp(delta)-1:.9f}（δ 小量展开一阶）")
print(f"  δ/ln15 = {delta/ln15:.6f}（≈1/1519.3）")

print()
print("=== 结论 ===")
print("若 G1-G6 无 ★（<0.01%）命中 → δ 溯源第二轮无清洁命中，开放维持，")
print("后续只登记结构清洁的候选（系数有框架身份）而非任何数值巧合。")
