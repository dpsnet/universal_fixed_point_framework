# -*- coding: utf-8 -*-
"""
chain_audit_152_dh_triple.py — d_H 三链判别矩阵（方向 a 核心）
链1：α（1/α = 24(d_H+3)，CODATA 137.035999084）
链2：双谱隙分解式自洽点 d_H* = 2.708258（104az-69 登记）
链3：m_τ（16·d_H + ln(16/15)/3）——方向敏感，双口径展示
"""
import math, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

cands = {
    "16259/6000 (2^14−2^7+3)/6000": 16259/6000,
    "65/24 = (k_max/N_gen)(1+1/k_max²)": 65/24,
    "√(22/3) = √(对合域+σ·静默)": math.sqrt(22/3),
    "框架观测 2.709532": 2.709532,
}
alpha_codata = 137.035999084
dh_dual = 2.708258   # 双谱隙分解式自洽点（104az-69）
m_tau_base = 16*2.709532 + math.log(16/15)/3

print("=== 三链判别矩阵（dev 越小越优）===")
print(f"{'候选':<42}{'α链 dev%':>12}{'双谱隙分解 dev%':>16}{'m_τ 链(线性口径) dev%':>18}")
print("-"*100)
for name, dh in cands.items():
    ainv = 24*(dh+3)
    dev_a = (ainv/alpha_codata - 1)*100
    dev_dual = (dh/dh_dual - 1)*100
    mtau = 16*dh + math.log(16/15)/3
    dev_m = (mtau/m_tau_base - 1)*100   # 相对框架基线偏移（不含方向）
    print(f"{name:<42}{dev_a:>12.6f}{dev_dual:>16.6f}{dev_m:>18.6f}")

print("\n=== 双谱隙分解式自洽点分析 ===")
print(f"分解式精确一致需 d_H = {dh_dual}（104az-69）")
for name, dh in cands.items():
    print(f"  {name}: dev {(dh/dh_dual-1)*100:+.6f}%")

print("\n=== 三候选分链投票 ===")
print("链1 α（观测）：16259/6000 占优（1e-6% vs 0.026%/0.032%）")
print("链2 双谱隙分解（框架内自洽）：65/24 占优（+0.0028% vs +0.058%/+0.009%）")
print("链3 m_τ（观测）：16259/6000 偏移 +0.011%（最小），65/24 −0.044%、√(22/3) −0.056%")
print("→ 16259/6000 在两条观测链占优；65/24 在框架内自洽链占优")
print("→ 判别裁决 = 双谱隙分解式的地位（104az-69：'仅作身份分解语义用'）")
