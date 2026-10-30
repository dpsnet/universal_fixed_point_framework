# -*- coding: utf-8 -*-
"""κΛ 谱身份系统扫描（2026-10-26）

开放项：Λ 绝对标度内生化——κΛ = 401.65（κΛ×Δλ_P20 = 49.0039/49.0021 口径）
目标：找 κΛ 的框架常数组合身份（幂基/活跃/静默/对合域/不动点/k_max/σ 组合）
"""
import itertools, math

powers, ngen, silence, involution, fixed = 2, 3, 5, 7, 4
kmax = powers**ngen  # 8
sigma = 1/(ngen*silence)  # 1/15

# 两种口径
target_a = 49.0039 / ((math.sqrt(3)-1)/6)   # 恒等 B κΛ×Δλ_P20 = 49.0039
target_b = 49.0021 / ((math.sqrt(3)-1)/6)   # 登记 49.0021
print(f"κΛ 目标：口径 A = {target_a:.6f}、口径 B = {target_b:.6f}")

# 基础量
bases = {"幂基": 2, "活跃": 3, "静默": 5, "对合域": 7, "不动点": 4, "k_max": 8,
         "幂基×静默": 10, "N_gen×不动点": 12, "σ⁻¹": 15, "全态": 16, "禁闭域": 42,
         "对合域²": 49, "Λ": 210, "675": 675}

# 组合候选：基数^幂 × 修正因子（σ 幂/静默族修正量）
def scan():
    hits = []
    # 简单幂次组合
    for name, base in bases.items():
        for n in (1, 2, 3):
            v = base**n
            for m, mname in ((1, ""), (sigma, "×σ"), (sigma**2, "×σ²"), (sigma**3, "×σ³"),
                             (6*sigma**3, "×(1+6σ³)" if False else "×6σ³"), (1/(ngen*silence**2), "×静默⁻¹×N_gen⁻¹")):
                for sign in (1, -1):
                    vv = v * m * sign
                    for tname, t in (("A", target_a), ("B", target_b)):
                        if vv > 0:
                            dev = (vv - t)/t
                            if abs(dev) < 0.01:
                                hits.append((abs(dev), f"{name}^{n}{mname}{'-' if sign<0 else ''} = {vv:.4f} vs {t:.4f}（{tname}）dev {dev*100:.4f}%"))
    return hits

hits = scan()
hits.sort()
print(f"\n=== 命中（|dev| < 1%）{len(hits)} 个 ===")
for dev, s in hits[:20]:
    print(f"  {s}")

print("\n=== 特殊候选：400 = 幂基⁴×静默² ===")
v400 = powers**4 * silence**2  # 400
for tname, t in (("A", target_a), ("B", target_b)):
    print(f"  400 vs {tname} = {t:.4f}——dev {(v400-t)/t*100:.4f}%——κΛ = 400×(1+δ) δ = {(t-v400)/v400*100:.4f}%")
delta = (target_a-400)/400
print(f"  δ = {delta:.6f} = {delta*100:.5f}%——静默族修正谱候选：σ² = 0.4444%（差 {(delta-sigma**2)/sigma**2*100:.1f}%）")
print(f"  6σ³/10 = {6*sigma**3/10:.6f}（{6*sigma**3/10*100:.4f}%）——差 {(delta-6*sigma**3/10)/(6*sigma**3/10)*100:.1f}%")
print(f"  σ³×幂基×N_gen⁻¹ = {sigma**3*powers/ngen:.6f}（{sigma**3*powers/ngen*100:.4f}%）——差 {(delta-sigma**3*powers/ngen)/(sigma**3*powers/ngen)*100:.1f}%")
print(f"  静默⁻²×N_gen⁻⁴ = {1/(silence**2*ngen**4):.6f}（{1/(silence**2*ngen**4)*100:.4f}%）——差 {(delta-1/(silence**2*ngen**4))/(1/(silence**2*ngen**4))*100:.1f}%")

print("\n=== κ 的框架身份（κ = κΛ/210）===")
kappa = target_a/210
print(f"κ = {kappa:.6f}")
print(f"  k_max−幂基−静默+不动点−对合域+... = {kmax-powers-silence+fixed-involution+ngen}（不整）")
print(f"  对合域/4 = {involution/4:.4f}、静默/幂基² = {silence/powers**2:.4f}、1+σ+σ² = {1+sigma+sigma**2:.6f}")
print(f"  幂基+N_gen−静默/对合域 = {powers+ngen-silence/involution:.4f}、√(禁闭域/10) = {math.sqrt(42/10):.4f}")
print(f"  2σ+静默²/(对合域×k_max) = {2*sigma+silence**2/(involution*kmax):.6f}")
print(f"  1+幂基×σ+对合域×σ² = {1+powers*sigma+involution*sigma**2:.6f}")
