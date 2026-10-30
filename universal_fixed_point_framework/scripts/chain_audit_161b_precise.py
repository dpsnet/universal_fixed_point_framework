# -*- coding: utf-8 -*-
"""chain_audit_161b_precise.py — μ_³H/μ_³He 残差精确判别（7/5×(1+1/80²) 候选）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

mh3 = 2.9789624656       # ³H CODATA 9 位
mhe3 = 2.127497723       # ³He CODATA 9 位
r = mh3/mhe3
print(f"μ_³H/|μ_³He|（9 位精确）= {r:.10f}")
print(f"7/5 = {7/5:.10f}：dev {(r-7/5)/(7/5)*100:+.6f}%")

resid = (r - 7/5)/(7/5)
print(f"\n残差 ε = {resid:.10f} = {resid*100:.6f}%")
print(f"ε vs 1/6400 = {1/6400:.10f}：dev {(resid-1/6400)/(1/6400)*100:+.5f}%")

cand = 7/5*(1+1/6400)
print(f"\n候选 (7/5)×(1+1/6400) = {cand:.10f}")
print(f"vs 观测比 {r:.10f}：dev {(r-cand)/cand*100:+.7f}%")

print("\n=== 1/6400 的框架身份 ===")
print(f"80² = {80**2}；80 = 静默×k_max×幂基 = 5·8·2 = {5*8*2}")
print(f"64×100 = 8²×(5×2)² = k_max²×静默²×幂基²？{64*100}")
print(f"2⁶·5²·？= 6400？{2**6*5**2}")
print(f"（静默×k_max）²×不动点 = 40²×4 = {40**2*4}？= 6400 ✓")
print(f"40 = 静默×k_max = 5·8 ✓；6400 = 不动点×40² = 4×1600")

print("\n=== 交叉核对：用候选反推 μ_³He ===")
cand_mhe3 = mh3/(7/5*(1+1/6400))
print(f"μ_³H / [(7/5)(1+1/6400)] = {cand_mhe3:.9f}")
print(f"vs PDG |μ_³He| = {mhe3:.9f}：dev {(cand_mhe3-mhe3)/mhe3*100:+.7f}%")

print("\n=== 无身份替代对照（防止网格效应）===")
for n in [6300, 6350, 6400, 6450, 6500]:
    c = 7/5*(1+1/n)
    print(f"  (7/5)(1+1/{n}) dev {(r-c)/c*100:+.5f}%")

print("\n=== 判别 ===")
print("μ_³H/|μ_³He| ≈ (7/5)×(1+1/80²)，80 = 幂基·静默·k_max")
print("→ 组合候选：对合域/静默 主比 + 1/80² 修正——核磁子链 ³H~³He 系结构")
