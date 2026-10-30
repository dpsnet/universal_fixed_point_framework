# -*- coding: utf-8 -*-
"""
Phase 104az-96: 织³ 的 β 函数第一性 —— "为何 10" 公理化闭合候选
核心问题：F_np = (b0/10)^3 * (1-delta)/dl3 的机制动机（104az-83 ④ 公理化路径第 1 环）
新候选：织³ = (b0/(b0+1))^3 —— Wilson-Fisher 型临界指数结构
  - b0 = (11Nc-2Nf)/3 = 9 = Ngen^2（渐近自由 β 函数一阶系数，Nc=Nf=3）
  - 10 = b0+1（β 函数 Wilson-Fisher 分母）—— 回答"为何 10"
  - 框架读法：(k_max+1)/(k_max+2) = 9/10（k_max=8）—— 双身份交汇判别
另检：F_np = 21/5 * (1+sigma^2) 整数有理近命中（21 = Ngen*M_3, 5 = 静默单元）
"""
import math
from decimal import Decimal, getcontext
getcontext().prec = 50

# --- 框架常数 ---
Nc = Nf = Ngen = 3
kmax = 8
sigma = Decimal(1)/Decimal(15)
CF = Decimal(Nc**2 - 1)/(2*Nc)
delta = sigma**2 * CF / 4          # 1/675
dlmin = (Decimal(3).sqrt() - 1) / 6
dl3 = Decimal(2).sqrt() * dlmin
b0 = (11*Nc - 2*Nf) / 3            # 9

# --- 1. 织³ = (b0/(b0+1))^3 恒等 ---
w = (Decimal(b0)/Decimal(b0+1))**3
print("=" * 70)
print("[1] 织³ β 函数第一性")
print(f"  b0 = {b0} = (11Nc-2Nf)/3 = Ngen^2（渐近自由 β 函数一阶系数）")
print(f"  b0+1 = {b0+1} = 10（Wilson-Fisher 分母）—— 回答'为何 10'")
print(f"  (b0/(b0+1))^3 = (9/10)^3 = {w} = 729/1000")
print(f"  == (Ngen^2/10)^3? {w == (Decimal(Ngen**2)/10)**3}")

# 框架读法：k_max+1 / k_max+2
print(f"  框架读法: (k_max+1)/(k_max+2) = {kmax+1}/{kmax+2} = 9/10 —— 与 β 函数双身份交汇")
print(f"  交汇: β0 = 9 = k_max+1, β0+1 = 10 = k_max+2（数值恒等，双身份判别）")

# --- 2. F_np 全框架闭式（β 函数形式） ---
corr = 1 - delta
inv_dl3 = 1/dl3
F_np = w * corr * inv_dl3
print(f"\n[2] F_np = (b0/(b0+1))^3 * (1-delta) / dl3 = {F_np}")
print(f"  组件: 织³={w:.12f}  修={corr:.12f}  隙倒数={inv_dl3:.12f}")
print(f"  组件分解: 织³=(Ngen^2/(Ngen+kmax-1))^3  修=(1-sigma^2/Nc)  隙=1/(sqrt2*dlmin)")
print(f"  语义: 临界穿越强度 = β 临界指数³ × 静默修正 × 穿越前谱间隙倒数")

# --- 3. 21/5 × (1+σ²) 整数有理近命中 ---
cand = (Decimal(21)/5) * (1 + sigma**2)
print(f"\n[3] 21/5 × (1+σ²) 候选（21=Ngen*M_3=3×7, 5=静默单元）")
print(f"  21/5 * (1+1/225) = {cand}")
print(f"  = 4746/1125 = {Decimal(4746)/1125}")
print(f"  F_np = {F_np}")
dev = (cand/F_np - 1)
print(f"  dev = {dev*100:+.9f}%")
print(f"  判别: 有理数 vs F_np 无理数（含 √6+√2）→ 非恒等；近命中登记")

# F_np 精确代数：27297*(√6+√2)/25000?
# (729/1000)(674/675)/(√2·Δλ_min), Δλ_min=(√3-1)/6
# = 729·674·6/(1000·675·√2·(√3-1)) = 729·674·6/(675000) · (√3+1)/(√2·2)
# 729*674*6 = 2948076; 675000*... 化简:
num = 729*674*6
den = 1000*675
g = math.gcd(num, den)
n1, d1 = num//g, den//g
# 1/[√2(√3-1)] = (√3+1)/(2√2) = (√6+√2)/4
# F = (n1/d1) * (√6+√2)/4 = n1(√6+√2)/(4 d1)
print(f"\n[4] F_np 精确代数形态")
print(f"  F_np = ({n1}/{d1})·(√6+√2)/4 = {n1}·(√6+√2)/{4*d1}")
r1 = Decimal(n1)*((Decimal(6).sqrt()+Decimal(2).sqrt()))/Decimal(4*d1)
print(f"  数值复核 = {r1}  vs  {F_np}  一致? {abs(r1-F_np) < Decimal('1e-40')}")

# --- 5. β0/(β0+1) 与 a0（D9 等距）的 0.0186% 关系判别 ---
d_eff = Decimal(62)/3
a0 = (d_eff/(Decimal(36)*Decimal(3).sqrt()*Decimal(2).sqrt()*1))**(Decimal(1)/3)  # (62/3/(4πNc·?))... 用 π 需精度
# a0 = (d_eff/(4πNc)·(Δλ_min/Δλ₃))^(1/3)，用 mpmath 式高精度更稳
from mpmath import mp, mpf, power
mp.dps = 40
d_eff_m = mpf(62)/3
a0_m = power(d_eff_m/(4*mp.pi*Nc) * (mpf(1)/mp.sqrt(2)), mpf(1)/3)
# Δλ_min/Δλ₃ = 1/√2
b_b1 = mpf(9)/10
print(f"\n[5] β0/(β0+1)=0.9 vs a0(D9 等距) = {a0_m}")
print(f"  dev = {(b_b1/a0_m-1)*100:+.6f}%")
print(f"  a0^3 = {a0_m**3}")
print(f"  判别: 0.0186% 双口径（代数 0.729000 vs 几何 0.729135）继续并存；")
print(f"        β 函数读法给代数侧新身份（β0/(β0+1)），几何侧仍 D9 等距")

# --- 6. 一循环语义检查: 修正族全部 σ² 级 ---
print(f"\n[6] 修正族一循环语义（全部 σ² 级）")
print(f"  σ² = {sigma**2} = 1/{(Decimal(1)/sigma**2)}")
print(f"  1/320 = Ngen·σ/kmax² = {Decimal(Ngen)*sigma/Decimal(kmax**2)} (≈σ²·0.703)")
print(f"  1/675 = δ = σ²·CF/4 = {delta}")
print(f"  修正比 320/675 = {Decimal(320)/675}")
print(f"  语义候选: 两修正均为'静默单元参与'的 σ² 级单圈修正（QFT 一循环 1+g²C 结构类比）")
