# -*- coding: utf-8 -*-
"""
Phase 104az-97: 修的一循环语义闭环候选
环 2 核心：为何 F_np 用 (1-delta)=674/675 而非其他修正?
1. ★★ delta 单位分解双身份: delta = sigma^2/N_gen = sigma^3*静默单元 = 1/675
   (104az-81 单位分解 1 = N_gen*sigma*静默单元 的直接推论)
2. ★★ 织-修连接: beta0*delta = N_gen*sigma^2 = 1/75
3. ★ 修正分母家族层级匹配规则: 强度量(生成主导)->生成^3*静默^2(675);
   质量比量(静默主导)->静默*Bott^2(320)
4. ★ m_s/T_c 修正 319/648000 的生成^4 层分解
5. ★ 一循环完备性: F_np 三组件全为单圈量
"""
from decimal import Decimal, getcontext
getcontext().prec = 50

Nc = Nf = Ngen = 3
kmax = 8
sigma = Decimal(1)/Decimal(15)
silent = Decimal(kmax - 3)          # 5
CF = Decimal(Nc**2-1)/(2*Nc)

print("=" * 70)
print("[1] delta 单位分解双身份")
d1 = sigma**2 / Decimal(Ngen)                 # 1/675
d2 = sigma**3 * silent                        # 1/3375 * 5 = 1/675
print(f"  delta = sigma^2/N_gen = {d1}")
print(f"  delta = sigma^3*静默单元 = {d2}")
print(f"  恒等? {d1 == d2}")
print(f"  机制: sigma^2/N_gen = sigma^3*静默  ⟺  N_gen*sigma*静默 = 1（单位分解 104az-81 直接推论）")
print(f"  → 静默修正 = 静默耦合²/生成 = 静默耦合³×静默单元（双读法）")

print("\n[2] 织-修连接: beta0*delta")
b0 = Decimal(11*Nc - 2*Nf)/3                  # 9
print(f"  beta0*delta = {b0}*{d1} = {b0*d1}")
print(f"  N_gen*sigma^2 = {Decimal(Ngen)*sigma**2}")
print(f"  恒等? {b0*d1 == Decimal(Ngen)*sigma**2}  = 1/75 = 1/(N_gen*静默^2)? {b0*d1 == Decimal(1)/(Decimal(Ngen)*silent**2)}")
print(f"  → 织(beta0) 与 修(delta) 通过 sigma² 连接：beta0*delta = N_gen*sigma²")

print("\n[3] 修正分母家族层级匹配规则")
print(f"  F_np 主结构 21/5 = N_gen*M3/静默（生成×Mersenne/静默——生成主导）")
print(f"    修正分母 675 = N_gen^3*静默^2（生成³×静默²——生成立方）")
print(f"  m_s/T_c 主结构 5Δλ_min = 静默×基谱隙（静默主导）")
print(f"    修正分母 320 = 静默*k_max^2（静默×Bott²——静默×平方）")
print(f"  规则: 修正分母 = 主量主导框架量^(层级)  ×  次级框架量")
print(f"  强度量(生成³) 用 675；质量比量(静默·Bott²) 用 320")
print(f"  验证实例: F_np(675) + m_s/T_c(320) 两实例一致")

print("\n[4] m_s/T_c 修正 319/648000 的生成^4 层分解")
r = Decimal(319)/Decimal(648000)
c1 = sigma**2 / Decimal(Ngen)**2 * (1 - Decimal(1)/Decimal(320))
print(f"  319/648000 = {r}")
print(f"  sigma^2/N_gen^2 × (1−1/320) = {c1}")
print(f"  恒等? {r == c1}")
print(f"  分解: sigma²/N_gen² = 1/2025 = 1/(N_gen·σ⁻¹)² = 1/45²（生成⁴层——质量比量更深一层）")
print(f"  × (1−1/320)（静默·Bott 修正 320 家族）")
print(f"  648000 = 320×2025 = (静默·k_max²)×(N_gen·σ⁻¹)² = 5×64×45²")

print("\n[5] 一循环完备性")
print(f"  F_np 三组件:")
print(f"    织³ = (beta0/(beta0+1))^3 —— beta0 一阶（渐近自由 β 函数单圈系数）")
print(f"    修  = 1−delta = 1−sigma²/N_gen —— sigma² 一阶（静默耦合²单圈修正）")
print(f"    隙  = 1/delta_lambda3 —— 谱隙一阶（端点倒数）")
print(f"  全部为单圈量，无高阶项 —— '临界穿越强度在单圈级精确'假设")
print(f"  织³展开高阶项 (1+1/9)^{-3} = 1−1/3+2/27−10/729+... 被吸收/不出现 → 单圈完备")

print("\n[6] m_tau 锚定交叉核对（P7-5t: delta = sigma^3*5）")
print(f"  sigma^3*5 = {sigma**3*Decimal(5)} = 1/675 ✓ 与 delta = sigma^2/N_gen 一致（同一对象双读法）")

print("\n[7] 诚实边界")
print(f"  层级匹配规则为两实例归纳（F_np/m_s/T_c）——需第三实例检验（E_b/v/m_tau）")
print(f"  beta0*delta = N_gen*sigma^2 是新恒等（由定义直接推出，非独立）——登记为连接而非发现")
