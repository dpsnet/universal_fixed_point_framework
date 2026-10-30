# -*- coding: utf-8 -*-
"""
Phase 104az-99: 织³ vs 织a 判别材料系统化
1. 机制身份可追溯性: 织³(β函数公式) vs 织a(D9等距条件)
2. 纯框架性: 织³ 纯有理 + F_np 织³口径纯代数闭式 vs 织a 含 π
3. π 框架身份候选检查（λ=π² 生成元谱身份之外有无直接身份）
4. 观测判别力: Λ 层 0.0186% vs 观测误差 ~0.1%
5. 织a/织³ 修正的身份检查
"""
from decimal import Decimal, getcontext
from mpmath import mp, mpf, power, pi as mppi
getcontext().prec = 50
mp.dps = 50

Ngen = 3
kmax = 8

print("=" * 70)
print("[1] 机制身份可追溯性")
print(f"  织³ = (β₀/(β₀+1))³ = (9/10)³——β 函数公式直接给出（β₀=(11N_c−2N_f)/3=9 可追溯）")
print(f"  织a = a₀ = (d_eff/4πN_c·Δλ_min/Δλ₃)^(1/3)——D9 等距'条件'的解（等距本身未推导）")
print(f"  判别: 公式身份（可追溯）vs 条件身份（假设）→ 织³ 机制身份更强")

print("\n[2] 纯框架性")
w3 = Decimal(729)/Decimal(1000)
print(f"  织³ = {w3}（纯有理——零超越数）")
w3sq = w3**2
print(f"  织³² = {w3sq} = 3^12/10^6 = N_gen^12/(k_max+2)^6（指数 12=4·N_gen=k_max+4——纯幂身份）")
print(f"  织³³ = {w3**3} = 3^18/10^9")
print(f"  织a 含 π（超越数）——需 π 框架身份方可框架化")

print("\n[3] π 框架身份候选检查（≥0.1% 差则无身份）")
cands = [
    ('π/3', mppi/3, 3),
    ('π/(√3)', mppi/mp.sqrt(3), 3),
    ('π/σ⁻¹', mppi/15, 15),
    ('π²/10', mppi**2/10, 10),
    ('π·Δλ_min', mppi*(mp.sqrt(3)-1)/6, 3),
    ('π/(k_max−5)', mppi/3, 3),
    ('2π/3', 2*mppi/3, 3),
    ('4π−k_max', 4*mppi-8, 8),
    ('π·σ', mppi/15, 15),
]
for name, val, ref in cands:
    dev = (val/mpf(ref) - 1)*100
    flag = '✓' if abs(dev) < 0.1 else '✗'
    print(f"  {name} = {mp.nstr(val, 10)} vs {ref} → dev {dev:+.4f}% {flag}")
print(f"  π² = {mp.nstr(mppi**2, 12)} vs k_max+2 = 10 → dev {(mppi**2/10-1)*100:+.4f}%（λ=π² 生成元谱身份 104az-2c-N 已登记——π² 有身份，π 本身无）")

print("\n[4] F_np 两口径的代数性质")
# 织³ 口径: 27297·(√6+√2)/25000 —— 代数数
sqrt6 = Decimal(6).sqrt()
sqrt2 = Decimal(2).sqrt()
F3 = Decimal(27297)/Decimal(25000)*(sqrt6+sqrt2)
print(f"  织³ 口径 F_np = 27297·(√6+√2)/25000 = {F3}（代数数——√6,√2 的代数组合）")
# 织a 口径: a₀³ = 31/(18π√2) → F_np = a₀³·(1−δ)·1/Δλ₃ 含 π^(1/3)? 不对——F_np 里是 a₀³（织因子立方）
# 织a 作为织因子立方 = a₀³ = 31/(18π√2)——含 π 分母
print(f"  织a³ = 31/(18π√2)（含 π 分母——F_np 织a 口径含 π 超越因子）")
print(f"  判别: 织³ 口径 = 代数数（√6+√2 代数组合）vs 织a 口径含 π（超越数）")

print("\n[5] Λ 观测判别力")
Fa = mpf('4.21948317')  # 织a 口径（KEY_FACTS 登记值）
dev_ratio = (Fa/mpf(F3) - 1)*100
print(f"  F_np 织³ = 4.2187003648340, 织a = 4.21948317")
print(f"  口径比 = {mp.nstr(Fa/mpf(F3), 12)} → Λ 预言差 = {dev_ratio:+.6f}%")
print(f"  Λ 观测精度（210.0 vs 210.3 双口径）= 0.14% >> 0.0186%")
print(f"  → Λ 层无判别力（0.0186% < 0.1% 观测误差）——判别保持开放")

print("\n[6] 织a/织³ 修正身份检查")
ratio = mpf('0.7291352691136843395383762143130225946542')/mpf('0.729')
print(f"  织a/织³ = {mp.nstr(ratio, 15)} → 修正 = {mp.nstr(ratio-1, 10)}")
cands2 = [
    ('σ⁴', mpf(1)/50625),
    ('σ³', mpf(1)/3375),
    ('δ', mpf(1)/675),
    ('σ²/N_gen²', mpf(1)/2025),
    ('1/5400', mpf(1)/5400),
    ('Δλ_min²', ((mp.sqrt(3)-1)/6)**2),
]
for name, val in cands2:
    print(f"  {name} = {mp.nstr(val, 10)} vs 修正 {mp.nstr(ratio-1, 10)} → dev {(val/(ratio-1)-1)*100:+.2f}%")
print(f"  → 无干净框架修正——两口径是独立候选而非同一量的两个精度")

print("\n[7] 判别结论")
print(f"  三方向一致倾向织³：① 机制身份可追溯（β 函数公式 vs D9 等距假设）")
print(f"  ② 纯框架性（纯有理 + 代数闭式 vs 含未身份化 π）")
print(f"  ③ 更近观测 4.2（0.0187 vs 0.0195）")
print(f"  判别保持开放原因明确: Λ 层判别力不足（0.0186% < 0.1%）")
print(f"  → 织³ 升格'主导候选'，织a 保留几何侧登记；决定性判别待独立可测预言")
