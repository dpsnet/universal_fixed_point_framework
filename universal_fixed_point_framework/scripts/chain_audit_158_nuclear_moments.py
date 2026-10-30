# -*- coding: utf-8 -*-
"""chain_audit_158_nuclear_moments.py — 核磁子链家族扩展：μ_t（氚核）、μ_d（氘核）、g_p/g_n 比值"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

gp2 = 2.79284734462      # g_p/2（μ_p/μ_N）
gn2 = 1.91304273         # g_n/2（|μ_n|/μ_N）
mt  = 2.9789624656       # μ_t（氚核 ³H）μ_N
md  = 0.8574382308       # μ_d（氘核 ²H）μ_N
mhe = 2.127497723        # |μ_³He| μ_N
sig = 1/15

print("=== 1. 氚核 μ_t 检验 ===")
print(f"μ_t 观测 = {mt:.7f}")
c1 = gp2*(1+sig)  # g_p/2 × 16/15
print(f"g_p/2×(1+σ) = g_p/2×16/15 = {gp2:.7f}×{16/15:.7f} = {c1:.7f}")
print(f"  dev = {(mt-c1)/c1*100:+.5f}%")
c2 = gn2*(1+sig)*gp2/gn2
c3 = mt/3
print(f"  μ_t/3 = {c3:.7f}（对比 N_gen 基准）")
c4 = 3 - 1/47.5
print(f"  3−1/47.5 = {c4:.7f}（对照）")

print("\n=== 2. 氘核 μ_d 检验 ===")
print(f"μ_d 观测 = {md:.7f}")
c5 = 6/7  # (N_gen×幂基)/对合域
print(f"6/7 = (N_gen×幂基)/对合域 = {c5:.7f}；dev = {(md-c5)/c5*100:+.5f}%（观察级不达）")
c6 = md*7
print(f"  μ_d×对合域 = {c6:.5f}（对比 6）")
print(f"  μ_p+μ_n−μ_d = {gp2-gn2-md:.7f}（D 态混合修正 δ_d 观测参考 0.02237）")

print("\n=== 3. g_p/g_n 比值 = 73/50 交叉候选 ===")
r = gp2/gn2
c7 = 73/50  # 73 = k_max×N_gen²+1 = 8·9+1；50 = 静默²×幂基
print(f"g_p/2 : g_n/2 观测 = {r:.7f}")
print(f"73/50 = (k_max·N_gen²+1)/(静默²·幂基) = {c7:.7f}；dev = {(r-c7)/c7*100:+.5f}%")

print("\n=== 4. 框架值比自洽复核 ===")
fr = (40217/14400)/(44/23)
print(f"(40217/14400)/(44/23) = {fr:.7f} vs 观测 {r:.7f}；dev = {(r-fr)/fr*100:+.7f}%")

print("\n=== 5. 氦-3 |μ_³He| 检验 ===")
print(f"|μ_³He| 观测 = {mhe:.7f}")
print(f"  49/23 = {49/23:.7f}；dev = {(mhe-49/23)/(49/23)*100:+.4f}%（对照，不达）")
print(f"  2+1/7.84？1/(mhe-2) = {1/(mhe-2):.4f}")
print(f"  g_n/2+0.2144？{mhe-gn2:.6f}（对照）")

print("\n=== 6. 核磁子链家族全景 ===")
print(f"g_p/2 = {gp2:.7f} = 40217/14400（锁定 4.4e-8）")
print(f"g_n/2 = {gn2:.7f} = 44/23（强候选 3.9e-7）")
print(f"μ_t   = {mt:.7f} ≈ g_p/2×(1+σ)（候选 {abs(mt-c1)/c1*100:.4f}%）")
print(f"μ_d   = {md:.7f} ≈ 6/7（观察 +0.034%）")
print(f"μ_N/μ_B = m_e/m_p = 1/1836.1526734（371/2430 覆盖）")
