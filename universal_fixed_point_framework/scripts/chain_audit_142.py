# -*- coding: utf-8 -*-
# chain_audit_142.py — 104az-142b/143 搜索脚本：
# A) 21cm 超精细框架表达（任务 1）
# B) 空白项补链：√3（Δλ_min 来源）、d_H（α 与 m_τ 共用）、e（指数链）——任务 2
# 数值环境：pyenv 3.11.8（标准库足够）
import math
from itertools import product

print("="*70)
print("A. 21cm 超精细结构框架表达")
print("="*70)

# 观测锚
f_hfs = 1420.405751768e6          # Hz, CODATA 21cm 线
Rc = 3.2898419602508e15           # c·R∞ Hz
ratio_obs = f_hfs / Rc
print(f"f_hfs/(c·R∞) 观测 = {ratio_obs:.6e}")

# 标准结构：f_hfs/(c·R∞) = (16/3)·α²·(m_e/m_p)·(g_p/2)·(1+δ)
alpha_codata = 1/137.035999084
me_mp = 1/1836.15267343
gp2 = 2.79284734463
K = 16/3
pred0 = K * alpha_codata**2 * me_mp * gp2
print(f"一阶 (16/3)α²(m_e/m_p)(g_p/2) = {pred0:.6e}  dev {100*(pred0/ratio_obs-1):+.4f}%")
print(f"→ (1+δ) 实际 = {ratio_obs/pred0:.8f}，δ = {ratio_obs/pred0-1:+.8f}")

# MUFPF 框架值重算
alpha_fw = 1/137.028            # 框架 α（d_H 级）
mp_fw = 938.251                 # 框架 m_N'
me_fw = 0.51099895
me_mp_fw = me_fw/mp_fw
pred_fw = K * alpha_fw**2 * me_mp_fw * gp2
print(f"框架值 (16/3)α²(m_e/m_p)(g_p/2) = {pred_fw:.6e}  dev {100*(pred_fw/ratio_obs-1):+.4f}%")

# g_p/2 框架候选搜索：2.792847
print("\n--- g_p/2 = 2.792847 框架候选 ---")
F = {2,3,4,5,7}
cands = []
for a,b in product(F, repeat=2):
    for sgn in (1,-1):
        v = a/b + sgn*1  # a/b±1 无意义跳过
# 简单有理候选 a/b、a+b/c、a(1±1/b) 等
for a in F:
    for b in F:
        if a*10/b == 0: continue
        v = a/b
        if abs(v-2.792847)/2.792847 < 0.05:
            cands.append((f"{a}/{b}", v, 100*(v/2.792847-1)))
        v = a*(1-1/b)
        if abs(v-2.792847)/2.792847 < 0.05:
            cands.append((f"{a}(1−1/{b})", v, 100*(v/2.792847-1)))
        v = a*(1+1/b)
        if abs(v-2.792847)/2.792847 < 0.05:
            cands.append((f"{a}(1+1/{b})", v, 100*(v/2.792847-1)))
for c in sorted(cands, key=lambda x: abs(x[2]))[:6]:
    print(f"  {c[0]} = {c[1]:.6f}  dev {c[2]:+.3f}%")

# 14/5 显式
v = 14/5
print(f"  14/5 = 2.8  dev {100*(v/2.792847-1):+.3f}%（=幂基×对合域/静默 = N_gen(1−σ)）")
v = 3*(1-1/15)
print(f"  3(1−σ) = {v:.6f}  dev {100*(v/2.792847-1):+.3f}%")

print("\n--- 框架值下的残差 δ 身份搜索 ---")
delta_fw = ratio_obs/pred_fw - 1
print(f"δ_fw = {delta_fw:+.6f}")
for cand, name in [(1/2381,"1/2381"), (1/2400,"1/2400"), (-1/15**2,"−σ²"), (-1/675,"−1/675"),
                   (-0.00116,"−α/π·1/2"), (-0.00232,"−α/π")]:
    print(f"  {name} = {cand:+.6f}  相对 δ_fw 比值 {cand/delta_fw:.3f}")

print()
print("="*70)
print("B. 空白项补链：√3 / d_H / e")
print("="*70)

print("\n--- B1. Δλ_min 的 √3 来源 ---")
s3 = math.sqrt(3)
print(f"√3 = {s3:.10f}")
print(f"√(k_max−静默) = √(8−5) = √3 = √N_gen ✓  → Δλ_min = (√N_gen−1)/(2·N_gen) 全框架化")

print("\n--- B2. d_H（1/α_EM=24(d_H+3) → d_H = α_EM⁻¹/24−3）---")
dH = 137.028/24 - 3
print(f"d_H = 137.028/24−3 = {dH:.6f}")
c1 = math.sqrt(7 + 1/3)
print(f"候选 √(对合域+σ·静默) = √(7+1/3) = {c1:.6f}  dev {100*(c1/dH-1):+.4f}%")
c2 = (8/3)*(1+1/60)
print(f"候选 (k_max+1)/N_gen·(1+σ/4) = 8/3·(1+1/60) = {c2:.6f}  dev {100*(c2/dH-1):+.4f}%")
c3 = 2 + 1/15*10 + 1/15**2*16
print(f"候选 2+10σ+16σ² = {c3:.6f}  dev {100*(c3/dH-1):+.4f}%")

print("\n--- B3. 欧拉数 e（指数链张力点）---")
e = math.e
print(f"e = {e:.10f}")
c = 27/10
print(f"候选 N_gen³/(幂基×静默) = 27/10 = {c:.6f}  dev {100*(c/e-1):+.3f}%")
print(f"结构性判断：e 为超越数，框架量为代数数——任意代数近似偏差无法为 0。")
print(f"  → 指数链引入 e 与『代数纯内生』结构性冲突：要么 e 升格为根集公设（破纯内生），")
print(f"  要么指数链机制需重述（如指数衰减形式改由其他链实现）——登记为深层开放项。")

print("\n--- B4. m_p/m_e = 1836.1527 框架候选（21cm 因子之一）---")
r = 1836.15267343
for a,b in product(F, repeat=2):
    for c in F:
        for sgn in (1,-1):
            v = a*b*c + sgn
            if abs(v-r)/r < 0.01:
                print(f"  {a}×{b}×{c}{'+' if sgn==1 else '−'}1 = {v}  dev {100*(v/r-1):+.3f}%")
v = 3*7*8*11 - 12
print(f"  3×7×8×11−12 = {v} dev {100*(v/r-1):+.3f}%（非框架 11 组合，仅参考）")
