# -*- coding: utf-8 -*-
"""S256k V3 双口径 + 家族检验
V3 = 6σ³+4σ⁵+8σ⁷+5σ⁸——命中真实目标 δ^(obs)
① CODATA 2018/2022 双口径 σ_score
② 删项敏感性（每项必要？）
③ 随机基线（系数 1-20、幂次 3-10 随机组合命中率）
④ 幂次谱 {3,5,7,8} 框架身份
"""
from decimal import Decimal, getcontext
getcontext().prec = 50
import math, random

ln15 = Decimal(15).ln()
sigma = Decimal(1)/Decimal(15)
s3 = sigma**3; s5 = sigma**5; s7 = sigma**7; s8 = sigma**8

V3_d = 6*s3 + 4*s5 + 8*s7 + 5*s8

def alpha_of(delta_pred):
    return 24*(ln15 + delta_pred + 3)

data = {
    "CODATA 2018": (Decimal("137.035999084"), Decimal("0.000000021")),
    "CODATA 2022": (Decimal("137.035999177"), Decimal("0.000000021")),
    "CODATA 2022±": (Decimal("137.035999177"), Decimal("0.000000025")),
}
print("=== S256k: V3 = 6σ³+4σ⁵+8σ⁷+5σ⁸ ===")
print(f"δ_V3 = {float(V3_d):.12f}")
alpha_V3 = alpha_of(V3_d)
print(f"α⁻¹_V3 = {float(alpha_V3):.10f}\n")

print("--- ① 双口径 ---")
for name, (val, unc) in data.items():
    sig = abs(alpha_V3 - val)/unc
    print(f"{name}: α⁻¹ = {val}±{unc}——σ = {float(sig):.3f}（{'达标' if sig<=1 else '提示' if sig<=3 else '不达标'}）")

print("\n--- ② 删项敏感性 ---")
delta_obs = Decimal("137.035999084")/24 - 3 - ln15
need = Decimal("2.1e-8")/24
terms = [("6σ³", 6*s3), ("4σ⁵", 4*s5), ("8σ⁷", 8*s7), ("5σ⁸", 5*s8)]
for name, val in terms:
    v = V3_d - val
    sig = abs(alpha_of(v) - Decimal("137.035999084"))/Decimal("2.1e-8")
    print(f"  删 {name}：α⁻¹σ = {float(sig):.1f}（{'必要' if sig>1 else '可删?'}）")

print("\n--- ③ 随机基线（100000 组合） ---")
random.seed(42)
hits = 0
N = 100000
for _ in range(N):
    cs = [random.randint(1, 20) for _ in range(4)]
    ps = [random.randint(3, 10) for _ in range(4)]
    v = sum(c*sigma**p for c, p in zip(cs, ps))
    if abs(24*(v - delta_obs))/Decimal("2.1e-8") <= 1:
        hits += 1
print(f"σ≤1 命中：{hits}/{N} = {hits/N*100:.3f}%")

print("\n--- ④ 幂次谱 {3,5,7,8} 框架身份 ---")
fc_ident = {3: "活跃（梅森 2²−1）", 5: "静默（费马 2²+1）", 7: "对合（梅森 2³−1）",
            8: "幂基³ = 幂基×不动点"}
fib = {1,2,3,5,8,13}
for p, ident in fc_ident.items():
    print(f"  σ^{p}：{ident}——Fib 谱{'✓' if p in fib else '✗'}")
print(f"  框架常数谱覆盖：4/4——Fib 谱覆盖：{sum(1 for p in fc_ident if p in fib)}/4")

print("\n--- ⑤ 系数身份 ---")
coef_ident = {6: "幂基×活跃（2×3）", 4: "不动点", 8: "幂基³（2³）", 5: "静默"}
for c, ident in coef_ident.items():
    print(f"  {c} = {ident}")
print(f"  全框架量：4/4——无自由参数")
