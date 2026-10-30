# -*- coding: utf-8 -*-
"""
Phase 104az-96b: 公理化收官验证补充
1. δ = σ²/N_gen 恒等（CF/4 = 1/N_gen 当 N_c=N_gen=3）
2. β₀ = N_gen² = k_max+1 双身份交汇
3. F_np β 函数完全形式数值
4. 织³ vs 织a 0.0186% 判别（代数 β 读法 vs 几何 D9 等距）
5. a₀ = (β₀/(β₀+1))³ × 修正? 检查 0.0186% 差的候选分解
6. 21/5 家族：F_np ≈ N_gen·M_3/静默单元 × (1+σ²)
"""
from decimal import Decimal, getcontext
from mpmath import mp, mpf, power
getcontext().prec = 50
mp.dps = 40

Nc = Nf = Ngen = 3
kmax = 8
sigma = Decimal(1)/Decimal(15)
CF = Decimal(Nc**2-1)/(2*Nc)

print("=" * 70)
print("[1] δ = σ²/N_gen 恒等（新简化）")
delta1 = sigma**2 * CF / 4
delta2 = sigma**2 / Decimal(Ngen)
print(f"  δ = σ²·CF/4 = {delta1}")
print(f"  δ = σ²/N_gen = {delta2}")
print(f"  恒等? {delta1 == delta2}")
print(f"  机制: CF/4 = (N_c²−1)/(8N_c) = 1/N_gen ⟺ (N_c²−1) = 8N_c/N_gen = 8（N_c=N_gen=3: 9−1=8 ✓）")
print(f"  → δ = σ²/N_gen = 1/(N_gen·静默单元)²/N_gen = 静默修正 = 静默²/生成³")
print(f"  新表述: 1−δ = 1 − 1/[N_gen³·(k_max−3)²] = 1 − 1/675（分母 = N_gen³·静默² ✓ 104az-94）")

print("\n[2] β₀ 双身份交汇")
b0 = Decimal(11*Nc - 2*Nf)/3
print(f"  β₀ = (11N_c−2N_f)/3 = {b0} = N_gen² = {Decimal(Ngen)**2}? {b0 == Decimal(Ngen)**2}")
print(f"  β₀ = k_max+1 = {kmax+1}? {b0 == Decimal(kmax+1)}")
print(f"  交汇: β₀ = N_gen² = k_max+1 = 9（物理公式 vs 框架量的双身份）")
print(f"  → 织³ = (β₀/(β₀+1))³ = ((k_max+1)/(k_max+2))³ = 729/1000")

print("\n[3] F_np β 函数完全形式")
dlmin = (Decimal(3).sqrt() - 1)/6
dl3 = Decimal(2).sqrt() * dlmin
corr = 1 - sigma**2/Decimal(Ngen)
inv = 1/dl3
F = (Decimal(9)/10)**3 * corr * inv
print(f"  F_np = (9/10)³·(1−σ²/N_gen)·1/(√2·Δλ_min) = {F}")
print(f"  展开: = (9/10)³·(674/675)·{inv:.12f}")

print("\n[4] 织³ vs 织a 判别")
w3 = (Decimal(9)/10)**3
d_eff = mpf(62)/3
a0 = power(d_eff/(4*mp.pi*Nc)*mpf(1)/mp.sqrt(2), mpf(1)/3)
print(f"  代数侧: (β₀/(β₀+1))³ = {w3}（β 函数第一性——渐近自由临界指数式）")
print(f"  几何侧: a₀ = (d_eff/4πN_c·Δλ_min/Δλ₃)^(1/3) = {a0}（D9 等距条件）")
dev = (mpf(w3)/a0 - 1)*100
print(f"  差 = {dev:+.6f}% —— 双登记维持")
print(f"  判别: 代数侧获 β 函数新身份（物理结构非数值巧合）；几何侧 D9 等距仍第一性")
print(f"  → 织³ 名称语义更新: 织³ = 渐近自由临界指数³（β₀/(β₀+1) 的立方）")

print("\n[5] 21/5 整数有理候选（'为何 4.2' 候选）")
cand = Decimal(21)/5 * (1 + sigma**2)
print(f"  F_np = {F}")
print(f"  N_gen·M₃/静默单元 × (1+σ²) = (3×7/5)·(226/225) = {cand}")
dev2 = (cand/F - 1)*100
print(f"  dev = {dev2:+.9f}% —— 非恒等（F_np 含 √6+√2），近命中登记")
print(f"  '为何 4.2': 4.2 = N_gen·(k_max−1)/(k_max−3) = 生成×缺失对偶/静默单元（主结构）")
print(f"  F_np = 4.2 × (1+σ²) × (1 + {((F/cand)-1):.3e}) 尾修正")

print("\n[6] 一循环语义总结")
print(f"  修正族（全部 σ² 级, σ²=1/225）:")
print(f"    (1−σ²/N_gen) = 674/675 —— F_np 分子（静默修正, 104az-94 家族）")
print(f"    (1−N_gen·σ/k_max²) = 319/320 —— m_s/T_c 修正（320=静默·k_max²）")
print(f"    (1+σ²) = 226/225 —— 21/5 近命中修正")
print(f"  语义: QFT 一循环 1+g²C 结构类比——静默耦合² 级单圈修正族")

print("\n[7] Δλ_min 的 N_gen 读法")
print(f"  Δλ_min = (√3−1)/6 = (√N_gen−1)/(2N_gen)（N_active=N_gen=3）")
print(f"  Δλ₃ = √2·Δλ_min = √(k_max/4)·Δλ_min（双谱隙桥 × 基谱隙）")
print(f"  隙倒数 = 1/Δλ₃ = 2N_gen/√(k_max/4)·1/(√N_gen−1)")
print(f"  → F_np 全 N_gen/k_max 闭式（σ 由 N_gen·(k_max−3) 派生——104az-81 零独立常数确认）")
