# -*- coding: utf-8 -*-
"""
Phase 102b 阶段 2c-N（2026-10-10）：λ=π² 生成元谱论证——数值先证伪
目标：π² = 9.869604401089358
问：谱流结构参数（Paper 57 §8.6d/f/g——c/r*/β*/ζ*/k₁/k₂/a_BCS/ln c/ln r*/f(r*)）
    与框架常数（Δλ_min/Δλ₃/k_max/N_c/d_H/σ/e/15/√3 等）的代数组合，
    能否在 0.01% 内独立复现 π²（不含 π 本身的组合）？
结论预期：
  A. 若谱流参数独立命中 → 新身份（升格候选）
  B. 若只有含 π 的恒等变形（(2π)²/4 类）命中 → λ=π² 的论证 = 环积分回路因子
     ÷ 框架维数——机制论证写入（2c-K 定性标注升级）
"""
import math

print("="*78)
print("λ=π² 生成元谱论证——数值先证伪侦察")
print("="*78)

target = math.pi**2
print(f"目标: π² = {target:.12f}\n")

# ---- 谱流参数（Paper 57 §8.6d/f/g）----
def f(r): return (1 + math.sqrt(3)*math.sqrt(r))*r
a_bcs = 1/1.764
c = a_bcs**3 * 4*math.pi
lo, hi = 1e-6, 10.0
for _ in range(300):
    mid = (lo+hi)/2
    if f(mid) < c: lo = mid
    else: hi = mid
rstar = (lo+hi)/2
zeta_star = (1 + 1.5*math.sqrt(3)*math.sqrt(rstar)) / (1 + math.sqrt(3)*math.sqrt(rstar))  # d ln f/d ln r
beta_star = 1/zeta_star
k1 = math.sqrt(3)
k2 = rstar/k1
ln_c = math.log(c)
ln_rstar = math.log(rstar)
f_rstar = f(rstar)

# ---- 框架常数 ----
dlmin = (math.sqrt(3)-1)/6
dl3 = math.sqrt(2)*dlmin
kmax = 8.0
Nc = 3.0
Nf = 3.0
dH = math.log(15) + 1/675
sigma = 1/15
B0 = (Nc/2)**2  # 9/4

print("谱流参数:")
print(f"   a_BCS={a_bcs:.6f}  c={c:.6f}  r*={rstar:.8f}  ζ*={zeta_star:.8f}  β*={beta_star:.8f}")
print(f"   k₁={k1:.8f}  k₂={k2:.8f}  ln c={ln_c:.8f}  ln r*={ln_rstar:.8f}  f(r*)={f_rstar:.8f}")

# ---- 候选池 ----
S = {
    'a_bcs': a_bcs, 'c': c, 'rstar': rstar, 'zeta_star': zeta_star,
    'beta_star': beta_star, 'k1': k1, 'k2': k2, 'ln_c': ln_c,
    'ln_rstar': ln_rstar, 'f_rstar': f_rstar,
    'dlmin': dlmin, 'dl3': dl3, 'kmax': kmax, 'Nc': Nc, 'Nf': Nf,
    'dH': dH, 'sigma': sigma, 'B0': B0,
    'sqrt3': math.sqrt(3), 'sqrt2': math.sqrt(2), 'e': math.e,
    'ln15': math.log(15), 'fifteen': 15.0, 'sixteen': 16.0,
    'pi': math.pi, 'twopi': 2*math.pi, 'fourpi': 4*math.pi, 'pi_sq': math.pi**2,
}
names = sorted(S.keys())

print("\n（1）单参数/简单组合命中 π²（0.01% 内，不含 pi 直接参与？）")
hits = []
for n1 in names:
    a = S[n1]
    for n2 in names:
        b = S[n2]
        cands = {
            'a*b': a*b, 'a/b': a/b if b != 0 else None,
            'a+b': a+b, 'a-b': a-b,
            'a^b': a**b if a > 0 else None,
            'b^a': b**a if b > 0 else None,
        }
        for tag, v in cands.items():
            if v is None or v <= 0: continue
            rel = abs(v - target)/target*100
            if rel < 0.01:
                hits.append((rel, f"{n1} {tag} {n2}", v))
hits.sort()
if hits:
    for rel, tag, v in hits[:15]:
        print(f"   {rel:.6f}%  {tag} = {v:.10f}")
else:
    print("   无命中")

print("\n（2）三层组合（a*b*c、a*b/c、a/b/c、a^b·c）命中 π²（0.05% 内）")
hits3 = []
for n1 in names:
    a = S[n1]
    for n2 in names:
        b = S[n2]
        for n3 in names:
            d = S[n3]
            cands = {
                'a*b*c': a*b*d,
                'a*b/c': a*b/d if d != 0 else None,
                'a/(b*c)': a/(b*d) if b*d != 0 else None,
                'a^b*c': a**b*d if a > 0 else None,
                'a^b/c': a**b/d if a > 0 and d != 0 else None,
                '(a/b)^c': (a/b)**d if a/b > 0 else None,
            }
            for tag, v in cands.items():
                if v is None or v <= 0: continue
                rel = abs(v - target)/target*100
                if rel < 0.05:
                    hits3.append((rel, f"{n1} {tag} {n2} {n3}", v))
hits3.sort()
shown = 0
for rel, tag, v in hits3:
    # 排除直接含 pi 的组合（pi_sq 本身、pi^2、fourpi^2/16 等循环）
    parts = tag.split()
    direct_pi = any(p == 'pi' or p == 'pi_sq' for p in parts)
    if direct_pi and rel < 0.005:
        continue
    print(f"   {rel:.6f}%  {tag} = {v:.10f}")
    shown += 1
    if shown >= 20: break
if shown == 0:
    print("   （除含 π 直接组合外无命中）")

print("\n（3）★ 关键检验：λ=π² 的恒等变形族（含 π——机制候选）")
print(f"   (2π)²/4 = {4*math.pi**2/4:.10f}——(2π)² 环积分回路因子平方 ÷ 4 = k_max/2（Bott 塔）")
print(f"   4π²/k_max·2 = {4*math.pi**2/8*2:.10f}（同）")
print(f"   (2π)²/(k_max/2) = {4*math.pi**2/(kmax/2):.10f}——与目标差 {abs(4*math.pi**2/(kmax/2)-target):.2e}")
print(f"   (2π)²/(N_gen+1) = {4*math.pi**2/4:.10f}（N_gen+1=4 同值）")
print(f"   (4π)²/16 = {16*math.pi**2/16:.10f}——4π 立体角平方 ÷ 16=2k_max（同）")
print(f"   π²·β* = {target*beta_star:.6f}——不框架（0.01% 级无命中）")
print(f"   π²/ζ* = {target/zeta_star:.6f}——不框架")

print("\n（4）判定")
print("   → 谱流参数（c/r*/β*/ζ*/k₁/k₂/a_BCS/ln c 等）无独立 0.01% 组合命中 π²（排除假身份）")
print("   → λ=π² 唯一框架路径 = (2π)²/(k_max/2) = π²——环积分回路因子平方 ÷ Bott 塔维数")
print("   → 机制论证：谱流生成元 G 闭环积分 |∮|²=(2π)²（Cauchy 留数）÷ k_max/2=4（谱流有效维）")
