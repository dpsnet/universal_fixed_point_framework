# -*- coding: utf-8 -*-
# Phase 104az-81b: σ 身份候选双表达 + 修正项完全框架化确认
import numpy as np

N_gen = 3.0; k_max = 8.0
sigma = 1.0/15.0

print("=== σ = 1/15 的身份候选 ===")
# 候选1: 1/[N_gen·(k_max−3)]
c1 = 1.0/(N_gen*(k_max-3))
# 候选2: 1/(2^(k_max/2)−1) Mersenne
c2 = 1.0/(2**(k_max/2.0)-1)
print(f"  σ 定义 = {sigma:.10f}")
print(f"  候选1 1/[N_gen(k_max−3)] = {c1:.10f}  差 {abs(c1-sigma)/sigma*100:.2e}%")
print(f"  候选2 1/(2^(k_max/2)−1) = {c2:.10f}  差 {abs(c2-sigma)/sigma*100:.2e}%")

print("\n=== Mersenne 连接 ===")
print(f"  15 = 2^4−1 = M_4 (k_max/2 = 4)")
print(f"  15 = 2^(k_max/2)−1: P7-5e-204/205 Mersenne/Fermat 对偶登记")
print(f"  Mersenne 序列: M_2=3(N_gen), M_4=15(σ 分母), M_6=63?")

print("\n=== 修正项完全框架化 (不含 σ 独立常数) ===")
# 用 σ = 1/[N_gen(k_max−3)]:
# 修正项 = σ²/N_gen² × (1 − 1/[(k_max−3)k_max²])
#        = 1/[N_gen⁴(k_max−3)²] × (k_max²(k_max−3)−1)/[k_max²(k_max−3)]
#        = [k_max²(k_max−3)−1]/[N_gen⁴·(k_max−3)³·k_max²]
num = int(k_max**2*(k_max-3) - 1)
den = int(N_gen**4*(k_max-3)**3*k_max**2)
print(f"  修正项 = {num}/{den} = {num/den:.12f}")
print(f"  319/648000 = {319/648000:.12f}")
print(f"  等价? {abs(num/den - 319/648000) < 1e-15}")

print("\n=== m_s/T_c 全框架闭式 (N_gen, k_max 两参数) ===")
# m_s/T_c = 5Δλ_min − [k_max²(k_max−3)−1]/[N_gen⁴(k_max−3)³k_max²]
# Δλ_min = (√3−1)/6 — 谱隙, 独立框架量
import numpy as np
dlmin = (np.sqrt(3)-1)/6
msTc = 5*dlmin - num/den
print(f"  m_s/T_c = 5(√3−1)/6 − 319/648000 = {msTc:.12f}")
print(f"  实际 4/(9a₀) = {4/(9*((62/3)/(12*np.pi*np.sqrt(2)))**(1/3)):.12f}")
print(f"  差 = {(msTc - 4/(9*((62/3)/(12*np.pi*np.sqrt(2)))**(1/3)))/msTc*100:.3e}%")

print("\n=== 家族分子 39/319 对照 ===")
print(f"  39 = k_max(k_max−3)−1 = 8·5−1 (P7-5e-244 静默单元家族)")
print(f"  319 = k_max²(k_max−3)−1 = 64·5−1 (本轮)")
print(f"  同族: k_max^j·(k_max−3)−1, j=1,2")
print(f"  家族语义: '静默单元 −1 侧' (k_max−3=5 静默单元) 的 k_max 幂推广")
