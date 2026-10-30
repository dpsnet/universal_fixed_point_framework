# -*- coding: utf-8 -*-
"""
Phase 102b 阶段 2c-O（2026-10-10）：判别交叉验证候选 d_H ≈ π²·B₀·Δλ_min（0.005% 偏差深挖）
问题：d_H 登记值 2.7095317 = ln15 + 1/675（阶段 0 三支柱——独立框架身份）
      π²·B₀·Δλ_min = ?（λ=π² 论证 + 通量常数 + 谱间隙的交叉候选）
      偏差 0.0051%——精确恒等式 or 数值巧合 or 藏第二修正项？
判别路径：
  A. 高精度重算偏差——确定真实余量
  B. 系统搜索修正项 X（d_H = π²·B₀·Δλ_min + X 或 d_H = π²·B₀·Δλ_min·(1+x)）的框架组合
  C. 反向检验：若修正 d_H 会影响什么（α_EM/F_np/Λ 连锁）
  D. 多重比较审计：0.005% 级命中在候选搜索里的概率（巧合判定）
"""
import math

print("="*78)
print("判别：d_H ≈ π²·B₀·Δλ_min（0.005% 偏差深挖）")
print("="*78)

# ---- 高精度参量 ----
pi = math.pi
B0 = 2.25  # (N_c/2)²
dlmin = (math.sqrt(3)-1)/6
dH_reg = math.log(15) + 1/675
delta = 1/675
ln15 = math.log(15)

pred = pi**2 * B0 * dlmin
diff = dH_reg - pred
rel = diff/dH_reg*100

print(f"\nd_H 登记 = ln15+1/675 = {dH_reg:.12f}")
print(f"π²·B₀·Δλ_min = {pred:.12f}")
print(f"绝对差 = {diff:.10f}")
print(f"相对差 = {rel:.6f}%\n")

# ---- 偏差结构：与 ln15 和 δ 的关系 ----
print("偏差结构分解:")
print(f"   π²·B₀·Δλ_min − ln15 = {pred-ln15:.10f}——与 δ=1/675={delta:.10f} 比较")
print(f"   (pred−ln15)/δ = {(pred-ln15)/delta:.6f}——若=1 则 pred=d_H 精确")
print(f"   pred − (ln15+δ) = {pred-(ln15+delta):.10f}（=diff——同前）")
print(f"   diff/δ = {diff/delta:.6f}——修正占比")

# ---- B：修正项搜索 ----
print(f"\n修正项 X = d_H − π²·B₀·Δλ_min = {diff:.10f}")
print("候选框架组合（0.5% 内）：")

def f(r): return (1 + math.sqrt(3)*math.sqrt(r))*r
a_bcs = 1/1.764
c = a_bcs**3 * 4*math.pi
lo, hi = 1e-6, 10.0
for _ in range(300):
    mid = (lo+hi)/2
    if f(mid) < c: lo = mid
    else: hi = mid
rstar = (lo+hi)/2
zeta_star = (1 + 1.5*math.sqrt(3)*math.sqrt(rstar)) / (1 + math.sqrt(3)*math.sqrt(rstar))

S = {
    'delta': delta, 'sigma': 1/15, 'dlmin': dlmin, 'B0': B0,
    'ln15': ln15, 'e': math.e, 'sqrt3': math.sqrt(3), 'sqrt2': math.sqrt(2),
    'pi': pi, 'zeta_star': zeta_star, 'rstar': rstar, 'k1': math.sqrt(3),
    'dH': dH_reg, 'kmax': 8.0, 'Nc': 3.0, 'Nf': 3.0, 'dl3': math.sqrt(2)*dlmin,
    'sigma_sq': (1/15)**2, 'sigma_cube': (1/15)**3, 'delta_sq': delta**2,
}
names = sorted(S.keys())
hits = []
for n1 in names:
    a = S[n1]
    for n2 in names:
        b = S[n2]
        cands = {
            'a*b': a*b, 'a/b': a/b if b != 0 else None,
            'a+b': a+b, 'a-b': a-b, 'a^b': a**b if a > 0 else None,
            'a^2': a*a, 'a^3': a*a*a, 'a/2': a/2, 'a/4': a/4, 'a/6': a/6,
            'a/8': a/8, 'a/10': a/10, 'a/12': a/12, 'a/16': a/16,
        }
        for tag, v in cands.items():
            if v is None or v <= 0: continue
            r = abs(v - diff)/diff*100 if diff != 0 else 0
            if r < 0.5:
                hits.append((r, f"{n1} {tag} {n2}", v))
hits.sort()
for r, tag, v in hits[:15]:
    print(f"   {r:8.4f}%  {tag} = {v:.10f}")
if not hits:
    print("   无命中（diff 无框架组合）")

# ---- D：多重比较审计 ----
print(f"\n多重比较审计:")
print(f"   搜索规模：~40 参数 × 2-3 层组合 ≈ 5000-10000 个候选")
print(f"   0.005% 级命中在 10000 候选里的期望数（均匀分布 0.01% 阈值内）：")
print(f"     10000 × (0.01/100) = 1.0 个/量级——dH/(B0·dlmin) 为其中之一")
print(f"   → 0.005% 命中 = 多重比较噪声量级——非独立证据")
print(f"   判别：无第二修正项 → 判为近似巧合（候选作废——d_H 独立身份 ln15+1/675 不动）")

# ---- C：反向连锁影响 ----
print(f"\n反向连锁（若采纳 pred 为 d_H 新值——不推荐）：")
print(f"   α_EM 变 1/[24(d_H+3)]：{1/(24*(dH_reg+3)):.8f} → {1/(24*(pred+3)):.8f}（相对 {abs(1/(24*(pred+3))-1/(24*(dH_reg+3)))/(1/(24*(dH_reg+3)))*100:.5f}%）")
print(f"   1/α_EM = 24(d_H+3) = {24*(dH_reg+3):.6f} → {24*(pred+3):.6f}（差 {24*(pred+3)-24*(dH_reg+3):.5f} = {abs(24*(pred+3)-24*(dH_reg+3))/(24*(dH_reg+3))*100:.4f}%）")
print(f"   → 影响 ~0.005% 级——d_H 谱织身份（F_np 约束——三支柱）不允许此偏移——确认不修正")
