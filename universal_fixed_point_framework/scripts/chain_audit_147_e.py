# -*- coding: utf-8 -*-
"""
chain_audit_147_e.py — e 机制重述数值佐证
1. e 用法二分法：e^{-ln x} = 1/x 代数可吸收 vs e^{-3e} 真超越
2. e 代数近似精度极限 vs 轻子链精度需求（P7-5v m_e -0.0081% 达标）
3. e^{-0.1539} 附近代数候选检查（e^{-3e} 分解 = e^{-8}·e^{-0.1539}？）
"""
import math, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 1. 二分法验证
print("=== e 用法二分法 ===")
print(f"e^(-ln16) = {math.exp(-math.log(16)):.10f}  vs  1/16 = {1/16:.10f}  （精确代数等价）")
print(f"e^(-3)    = {math.exp(-3):.10f}  vs 代数候选 1/20 = {1/20:.10f} dev {(1/20/math.exp(-3)-1)*100:+.3f}%")
print(f"e^(-3e)   = {math.exp(-3*math.e):.10f}  vs (e^(-3))^e = {math.exp(-3)**math.e:.10f} （超越，不可代数化）")

# 2. 精度需求 vs 代数近似能力
print("\n=== 精度需求 vs 代数近似能力 ===")
print(f"轻子链达标精度（P7-5v m_e -0.0081%）：需要 e 相关因子精度 ~0.01%")
print(f"e 的最佳简单代数近似 27/10 = 2.7（dev {(2.7/math.e-1)*100:+.3f}%）；19/7 = 2.7143（dev {(19/7/math.e-1)*100:+.3f}%）；193/71（dev {(193/71/math.e-1)*100:+.5f}%）")
print(f"→ 代数近似无法达 0.01% 级（连分数收敛须用 ~71 分母才达 0.02%），且 e 无有限代数表达 → 真超越类不可去")

# 3. e^{-3e} 分解候选
print("\n=== e^{-3e} 分解探索（指数 = 3e - σ³(1+α_v) ≈ 8.1539）===")
alpha_v = 1 + 1/15 + math.sqrt(4/3/2)   # P7-5w：1+σ+√(C_F/2)
exp_val = 3*math.e - (1/15)**3 * (1 + alpha_v)
print(f"3e - σ³(1+α_v) = {exp_val:.9f}；e^{-exp_val} = {math.exp(-exp_val):.12f}")
m_tau = 1776.86
m_e_obs = 0.51099895000
print(f"m_e/m_τ = {m_e_obs/m_tau:.12f} vs e^{-exp_val} = {math.exp(-exp_val):.12f}  dev {(math.exp(-exp_val)/(m_e_obs/m_tau)-1)*100:+.5f}%")
# 分解：e^{-8}·e^{-0.1539}
frac = exp_val - 8
print(f"分解 exp = 8 + {frac:.9f}（8 = k_max）；e^-8 = {math.exp(-8):.10f}，e^-{frac:.4f} = {math.exp(-frac):.10f}")
# 分数部代数候选
for c, name in [(6/7, "6/7=N_gen·幂基/对合域"), (13/15, "13/15"), (7/8, "对合域/k_max"), (5/6, "静默/(静默+1)")]:
    print(f"  e^-{frac:.4f} vs {name} = {c:.10f}  dev {(c/math.exp(-frac)-1)*100:+.4f}%")
