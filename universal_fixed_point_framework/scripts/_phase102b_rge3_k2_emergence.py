# -*- coding: utf-8 -*-
"""
Phase 102b 阶段 2c-P（2026-10-10）：攻 Paper 57 §8.7#5——k₂ 的独立谱流方程自洽涌现
问题：k₂ = r*/√3 目前是"单一 c 的反向重标度"（后验代数倍率）。
     §8.7#5 要求：k₂ 由 EM 尺度自身的独立谱流方程自洽涌现。
论证候选：
  ① k₂ := f_EM(u) = c 的唯一正根（em_residual_root_unique——Lean 已证——方程独立于 r*）
  ② c = a_BCS³·4π = (πe^{−γ_E})⁻³·4π = 4e^{3γ_E}/π²——内生谱来源（a_BCS 普适分解——BCSConstantOrigin
    universal_ratio_cancellation——π=费米谱权重、e^{γ_E}=谱 ζ 正则化常数——Paper 57 §8.6c）
  ③ √3 = 电磁中间级锚因子（Δλ_min^(EM) = Δλ_min/√3——flow_em_anchor_constant——普适锚点）
  结论候选：k₂ 由 (EM 谱流函数 × 内生闭合常数 × 普适锚因子) 唯一确定——不从 r* 反推
验证：
  A. 用精确 c = 4e^{3γ_E}/π² 独立解 f_EM(k₂)=c（不引用 r*）→ k₂_new
  B. 对照 k₂_old = f⁻¹(c)/√3（同 c 口径）——折叠一致性
  C. 口径审计：1.764 舍入 vs πe^{−γ_E} 精确——k₂ 摆动
  D. k₂_new 的框架身份搜索（0.01% 内——EM 尺度关联候选）
"""
import math

print("="*78)
print("k₂ 独立谱流方程自洽涌现——数值验证（§8.7#5 攻点）")
print("="*78)

gamma_E = 0.5772156649015329

def f(r): return (1 + math.sqrt(3)*math.sqrt(r))*r
def f_EM(u): return f(math.sqrt(3)*u)  # √3·u + 3√(√3)·u√u

def solve_root(g, lo, hi):
    """二分求 g(x)=c 唯一正根"""
    for _ in range(300):
        mid = (lo+hi)/2
        if g(mid) < 0: lo = mid
        else: hi = mid
    return (lo+hi)/2

# ---- c 口径 ----
a_bcs_round = 1/1.764          # Paper 57 表列舍入
a_bcs_precise = 1/(math.pi*math.exp(-gamma_E))  # πe^{−γ_E} 精确
c_round = a_bcs_round**3 * 4*math.pi
c_precise = 4*math.exp(3*gamma_E)/math.pi**2   # 内生谱来源形式
print(f"\n口径审计:")
print(f"   a_BCS 舍入 = 1/1.764 = {a_bcs_round:.9f}")
print(f"   a_BCS 精确 = 1/(πe^{{−γ_E}}) = {a_bcs_precise:.9f}")
print(f"   差 = {(a_bcs_precise/a_bcs_round-1)*100:.5f}%")
print(f"   c 舍入 = {c_round:.9f}")
print(f"   c 精确 = 4e^(3γ_E)/π² = {c_precise:.9f}")
print(f"   c 差 = {(c_precise/c_round-1)*100:.5f}%")

# ---- A：独立解 k₂（精确 c——不引用 r*）----
print(f"\nA. 独立谱流方程解 k₂（c 精确口径——不引用 r*）:")
# f_EM(u) - c = 0 在 (0, 10) 唯一正根
k2_new = solve_root(lambda u: f_EM(u) - c_precise, 1e-9, 10.0)
print(f"   f_EM(k₂) = c_precise ⟹ k₂_new = {k2_new:.10f}")
print(f"   ln k₂ = {math.log(k2_new):.10f}")
print(f"   验证 f_EM(k₂) = {f_EM(k2_new):.9f} vs c_precise = {c_precise:.9f}（残差 {abs(f_EM(k2_new)-c_precise):.2e}）")

# ---- B：折叠一致性（同口径 r*）----
print(f"\nB. 折叠一致性（k₂ = ρ(c)/√3 同一几何事实）:")
rstar_new = solve_root(lambda r: f(r) - c_precise, 1e-9, 10.0)
k2_old = rstar_new/math.sqrt(3)
print(f"   r* = f⁻¹(c_precise) = {rstar_new:.10f}")
print(f"   k₂_old = r*/√3 = {k2_old:.10f}")
print(f"   差 |k₂_new − k₂_old| = {abs(k2_new-k2_old):.2e}（0——同根折叠 ✓）")

# ---- C：舍入口径对 k₂ 的摆动 ----
rstar_round = solve_root(lambda r: f(r) - c_round, 1e-9, 10.0)
k2_round = rstar_round/math.sqrt(3)
print(f"\nC. 舍入口径摆动:")
print(f"   k₂(1.764 口径) = {k2_round:.10f}")
print(f"   k₂(πe^{{−γ_E}} 精确) = {k2_new:.10f}")
print(f"   摆动 = {(k2_new/k2_round-1)*100:.5f}%")

# ---- D：k₂_new 框架身份搜索（0.01% 内）----
print(f"\nD. k₂_new = {k2_new:.10f} 的框架身份搜索（0.01% 内）:")
S = {
    'delta': 1/675, 'sigma': 1/15, 'dlmin': (math.sqrt(3)-1)/6,
    'dlmin_EM': (math.sqrt(3)-1)/6/math.sqrt(3),
    'dl3': math.sqrt(2)*(math.sqrt(3)-1)/6,
    'B0': 2.25, 'dH': math.log(15)+1/675, 'ln15': math.log(15),
    'e': math.e, 'pi': math.pi, 'sqrt2': math.sqrt(2), 'sqrt3': math.sqrt(3),
    'Nc': 3.0, 'kmax': 8.0, 'CF': 4/3, 'kappa': 6/math.pi,
    'alpha_EM': 1/(24*(math.log(15)+1/675+3)),
    'inv_alpha_EM': 24*(math.log(15)+1/675+3),
    'gamma_E': gamma_E, 'e_gamma': math.exp(gamma_E),
    'c_precise': c_precise, 'rstar': rstar_new, 'zeta_star': None,
    'sigma_sq': (1/15)**2, 'sigma_cube': (1/15)**3, 'delta_sq': (1/675)**2,
}
S['zeta_star'] = (1 + 1.5*math.sqrt(3)*math.sqrt(rstar_new)) / (1 + math.sqrt(3)*math.sqrt(rstar_new))
names = sorted(S.keys())
hits = []
for n1 in names:
    a = S[n1]
    for n2 in names:
        b = S[n2]
        cands = {
            'a*b': a*b, 'a/b': a/b if b != 0 else None, 'a+b': a+b, 'a-b': a-b,
            'a^b': a**b if a > 0 else None, 'a/2': a/2, 'a/4': a/4, 'a/8': a/8,
            'a/16': a/16, 'a^2': a*a, 'a^3': a*a*a, 'sqrt(a)': math.sqrt(a) if a > 0 else None,
        }
        for tag, v in cands.items():
            if v is None or v <= 0: continue
            r = abs(v - k2_new)/k2_new*100
            if r < 0.01:
                hits.append((r, f"{n1} {tag} {n2}", v))
hits.sort()
if hits:
    for r, tag, v in hits[:10]:
        print(f"   {r:8.5f}%  {tag} = {v:.10f}")
else:
    print("   0.01% 内无命中")
    # 放宽容差看最近
    near = []
    for n1 in names:
        a = S[n1]
        for n2 in names:
            b = S[n2]
            cands = {
                'a*b': a*b, 'a/b': a/b if b != 0 else None, 'a+b': a+b, 'a-b': a-b,
                'a^b': a**b if a > 0 else None, 'a/2': a/2, 'a/4': a/4, 'a/8': a/8,
            }
            for tag, v in cands.items():
                if v is None or v <= 0: continue
                r = abs(v - k2_new)/k2_new*100
                if r < 0.5:
                    near.append((r, f"{n1} {tag} {n2}", v))
    near.sort()
    print("   0.5% 内最近 5 组:")
    for r, tag, v in near[:5]:
        print(f"   {r:8.4f}%  {tag} = {v:.10f}")

# ---- 关键候选：k₂ vs 1/2 与 Δλ_min^(EM) ----
print(f"\n关键候选检查:")
print(f"   k₂/0.5 = {k2_new/0.5:.8f}（1/2 差 {(k2_new/0.5-1)*100:.5f}%）")
print(f"   k₂·2 = {k2_new*2:.10f}")
print(f"   k₂ + 1/2 = {k2_new+0.5:.10f}")
print(f"   1/k₂ = {1/k2_new:.10f}——≈ ?（1.9815 ≈ α_v+1/10=1.9832 差 {(1/k2_new-1.983163)/1.983163*100:.5f}%）")
alpha_v = 1 + 1/15 + math.sqrt(2/3)
print(f"   α_v = 1+σ+√(2/3) = {alpha_v:.8f}——1/k₂ vs α_v 差 {(1/k2_new-alpha_v)/alpha_v*100:.4f}%")
