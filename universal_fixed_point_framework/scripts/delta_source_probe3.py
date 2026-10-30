# -*- coding: utf-8 -*-
"""δ 溯源第三轮：轻子链新锚（开放项⑤）

新候选族：轻子代间隔锚（e、3e、e^{−3}、ln16+e^{−3}）、E_τ 分解、
双谱隙锚、0.036（α 小数）、7/10 修正（7=k_max−1、10=N_gen+k_max−1）
"""
import numpy as np

delta = 16259/6000 - np.log(15)
ln15 = np.log(15)
ln1615 = np.log(16/15)
ln16 = np.log(16)
e = np.e
E_tau = 43.37394  # ln(M_Pl/m_τ)，M_Pl=1.221e22（框架谱定）
M_Pl = 1.221e22
m_tau = 1776.86
E_tau_fw = np.log(M_Pl/m_tau)
M_Pl_pdg = 1.2209e22
E_tau_pdg = np.log(M_Pl_pdg/m_tau)
D = (np.sqrt(3)-1)/6

print(f"δ = {delta:.9f}")
print(f"E_τ(框架 M_Pl) = {E_tau_fw:.9f}   E_τ(PDG M_Pl) = {E_tau_pdg:.9f}   笔记口径 43.37394")
print()

def report(name, v, target=E_tau_fw):
    rel = abs(v - target)/abs(target)*100
    flag = "★" if rel < 0.002 else ("✓" if rel < 0.02 else " ")
    print(f"  {flag} {name} = {v:.9f}  相对差 {rel:.5f}%")

print("=== 主候选：E_τ = 16·ln15 + (7/10)·ln(16/15) ===")
v1 = 16*ln15 + (7/10)*ln1615
report("16·ln15+(7/10)·ln(16/15)", v1)
print(f"  vs E_τ(PDG) = {E_tau_pdg:.9f}：差 {v1-E_tau_pdg:+.7f}（{(v1-E_tau_pdg)/E_tau_pdg*1e6:+.1f} ppm）")
print(f"  组件身份：16=2⁴（全态）、ln15=Moran 主项 d_H、7/10=(k_max−1)/(N_gen+k_max−1)=7/10")
print()

print("=== 对照：P7-5c E_τ = 16·dH + ln(16/15)/3（dH 反解 2.7094998） ===")
dH_p7 = (E_tau_fw - ln1615/3)/16
print(f"  P7-5c 反解 dH = {dH_p7:.9f}（vs 16259/6000={16259/6000:.9f}：差 {abs(dH_p7-16259/6000)/16259*6000*100:.4f}%；vs ln15：差 {abs(dH_p7-ln15)/ln15*100:.4f}%）")
v2 = 16*dH_p7 + ln1615/3
report("16·dH+ln(16/15)/3（P7-5c）", v2)
print(f"  隐含 δ_P7 = (ln15+δ 口径) = {dH_p7-ln15:.9f}（vs 实际 δ={delta:.9f}：差 {abs(dH_p7-ln15-delta)/delta*100:.1f}%）")
print()

print("=== 新公式与 P7-5c 的 δ 一致性检验 ===")
d_from_new = (11/30)*ln1615/16  # (7/10−1/3)·ln1615/16
print(f"  若两式相等 ⟹ δ = (11/30)·ln(16/15)/16 = {d_from_new:.9f}")
print(f"  vs 实际 δ = {delta:.9f}：差 {abs(d_from_new-delta)/delta*100:.1f}%——不一致（两式不同构）")
print()

print("=== 轻子间隔锚族 ===")
for k in range(1, 40):
    for m in range(1, 60):
        v = e**(-k)/m
        rel = abs(v - delta)/delta
        if rel < 0.01:
            print(f"  ★ e^{{-{k}}}/{m} = {v:.9f}  相对差 {rel*100:.4f}%")
print()

print("=== E_τ 分解族（7/10、2/3、11/30 等修正） ===")
for c in [7/10, 2/3, 11/30, 1/3, 3/10, 9/10, 7/3, 11/10]:
    v = 16*ln15 + c*ln1615
    rel = abs(v - E_tau_fw)/E_tau_fw
    print(f"  16·ln15+{c}·ln(16/15) = {v:.9f}  相对差 {rel*100:.5f}%")
print()

print("=== δ 与 e^{−3}（静默三次，m_μ/m_τ 锚） ===")
for m in range(1, 80):
    v = np.exp(-3)/m
    rel = abs(v - delta)/delta
    if rel < 0.005:
        print(f"  e^{{-3}}/{m} = {v:.9f}  相对差 {rel*100:.4f}%")
print()

print("=== 双谱隙差（Δλ_min 与 231/5800=Δλ₁₆） ===")
dl16 = 231/5800
print(f"  Δλ₁₆ = {dl16:.9f}；Δλ_min = {D:.9f}")
print(f"  Δλ_min−Δλ₁₆ = {D-dl16:.9f}   vs δ：差 {abs(D-dl16-delta)/delta*100:.1f}%")
print(f"  Δλ₁₆/Δλ_min = {dl16/D:.6f}；Δλ₁₆−Δλ_min/3 = {dl16-D/3:.9f} vs δ：差 {abs(dl16-D/3-delta)/delta*100:.1f}%")
print()

print("=== 结论 ===")
print("★ E_τ=16·ln15+(7/10)·ln(16/15)（组件全框架量：16 全态、ln15 Moran 主项、")
print("  7/10=(k_max−1)/(N_gen+k_max−1)）命中 E_τ（1e-6 级）——强候选，")
print("  与 P7-5c（16dH+ln1615/3）同量级且纯内生（无判别 dH）；")
print("  但两式不等价（隐含 δ 差 17%）→ 两公式为独立命中，需判别。")
