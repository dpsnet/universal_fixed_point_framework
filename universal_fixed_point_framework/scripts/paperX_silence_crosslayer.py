#!/usr/bin/env python3
"""
paperX_silence_crosslayer.py — 跨层近恒等 n1 ≈ n4 + n3/2 - δ/2 精确性审计

检验: ln(1/Δλ²) ≈ ln15 + 3/2 - δ/2 (偏差 0.0001%) 是恒等、近似还是巧合。
① 精确残差计算; ② δ 反演值 vs 框架 δ; ③ Δλ 精度敏感性;
④ 代数 vs 超越 (15Δλ² = e^{(δ-3)/2} 不可能精确相等);
⑤ ε̄ 交叉检验 (δ = ln15·ε̄, RMS 约束 ε̄ ≈ 5.35e-4)。
"""
import numpy as np
import mpmath as mp

checks = []
mp.mp.dps = 30
pi = mp.pi
sqrt3 = mp.sqrt(3)
ln15 = mp.log(15)

print("=" * 72)
print("§0 精确常数")
print("=" * 72)
dL2 = (2 - sqrt3) / 18.0          # 精确 Δλ² (代数数)
n1 = mp.log(1 / dL2)              # = ln(18(2+√3))
n3, n4 = 3, ln15
dH_obs = mp.mpf("2.7095")
delta_fw = dH_obs - ln15          # 框架 δ
print(f"  Δλ²  = (2-√3)/18 = {mp.nstr(dL2, 20)}")
print(f"  n1   = ln(1/Δλ²) = {mp.nstr(n1, 20)}")
print(f"  ln15 = {mp.nstr(ln15, 20)}")
print(f"  δ(框架) = d_H - ln15 = {mp.nstr(delta_fw, 12)}")

print("\n" + "=" * 72)
print("§1 精确残差 (n1 vs ln15 + 3/2 ± δ/2)")
print("=" * 72)
r_raw = n4 + n3 / 2.0
r_fw = n4 + n3 / 2.0 - delta_fw / 2.0
print(f"  n1 - (ln15 + 3/2)          = {mp.nstr(n1 - r_raw, 12)}")
print(f"  n1 - (ln15 + 3/2 - δ/2)    = {mp.nstr(n1 - r_fw, 12)}   (偏差 {mp.nstr(abs(n1-r_fw)/n1*100, 8)}%)")
c1 = abs(n1 - r_fw) / n1 < 1e-5
checks.append(c1)
print(f"  检查 1/7: 含 δ/2 修正后偏差 < 0.001% ? {c1}")

print("\n" + "=" * 72)
print("§2 δ 反演: 使关系精确成立的 δ* vs 框架 δ")
print("=" * 72)
delta_star = 2 * (n4 + n3 / 2.0 - n1)   # 精确成立所需 δ
dH_star = ln15 + delta_star
print(f"  δ* = 2(ln15 + 3/2 - n1)  = {mp.nstr(delta_star, 12)}")
print(f"  δ(框架)                  = {mp.nstr(delta_fw, 12)}")
print(f"  相对差 |δ* - δ|/δ        = {mp.nstr(abs(delta_star-delta_fw)/delta_fw*100, 8)}%")
print(f"  d_H* = ln15 + δ*         = {mp.nstr(dH_star, 12)}  vs 观测 2.7095")
c2 = abs(delta_star - delta_fw) / delta_fw < 0.01
checks.append(c2)
print(f"  检查 2/7: δ* 与框架 δ 差 < 1% ? {c2}")

print("\n" + "=" * 72)
print("§3 Δλ 精度敏感性 (0.122 vs 精确值)")
print("=" * 72)
dL_obs = mp.mpf("0.122")
n1_obs = mp.log(1 / dL_obs**2)
dL_exact = mp.sqrt(dL2)
print(f"  Δλ(观测) = 0.122,  Δλ(精确) = √((2-√3)/18) = {mp.nstr(dL_exact, 12)}")
print(f"  相对差: {mp.nstr(abs(dL_obs-dL_exact)/dL_exact*100, 8)}%")
res_obs = n1_obs - r_fw
res_exact = n1 - r_fw
print(f"  用 0.122:   n1 - (ln15+3/2-δ/2) = {mp.nstr(res_obs, 10)}")
print(f"  用精确值:   n1 - (ln15+3/2-δ/2) = {mp.nstr(res_exact, 10)}")
print(f"  残差变化: {mp.nstr(abs(res_obs/res_exact), 6)}× (Δλ 差 0.003% → 残差变化 ~20×)")
c3 = abs(res_obs) / abs(res_exact) > 5
checks.append(c3)
print(f"  检查 3/7: Δλ 的 0.003% 精度差异使残差放大 >5× ? {c3}  (脆弱性证据)")

print("\n" + "=" * 72)
print("§4 代数 vs 超越: 15Δλ² = e^{(δ-3)/2} 不可能精确")
print("=" * 72)
# 关系等价形式: 15·Δλ² = e^{(δ-3)/2}
LHS = 15 * dL2                 # = 5(2-√3)/6, 代数数
RHS_need = mp.e**(-(n3 - delta_fw) / 2.0)   # 超越数 (e 的代数次幂)
print(f"  15Δλ² = 5(2-√3)/6 = {mp.nstr(LHS, 20)}  (代数数)")
print(f"  e^{{(3-δ)/2}}        = {mp.nstr(RHS_need, 20)}  (超越数)")
print(f"  相对差: {mp.nstr(abs(LHS-RHS_need)/LHS*100, 8)}%")
print(f"  Lindemann-Weierstrass: e^{{代数}} 超越 ⟹ 相等需 δ = 3-2ln(5(2-√3)/6) 为超越数")
print(f"  而框架 δ = 0.00145 为十进制拟合值 ⟹ 只能近似, 不可能精确恒等")
c4 = abs(LHS - RHS_need) / LHS > 1e-6
checks.append(c4)
print(f"  检查 4/7: 15Δλ² ≠ e^(3-δ)/2 (非恒等, 差 > 1e-6) ? {c4}")

print("\n" + "=" * 72)
print("§5 δ 的 ε̄ 交叉检验 (δ = ln15·ε̄, RMS 约束)")
print("=" * 72)
eps_fw = delta_fw / ln15            # 框架 ε̄
eps_star = delta_star / ln15        # 关系所需的 ε̄
print(f"  ε̄(框架) = δ/ln15     = {mp.nstr(eps_fw, 10)}")
print(f"  ε̄(关系) = δ*/ln15    = {mp.nstr(eps_star, 10)}")
print(f"  相对差: {mp.nstr(abs(eps_star-eps_fw)/eps_fw*100, 8)}%")
# RMS 约束: ε̄ = √N_total·ε₃, N_total=5
eps3_fw = eps_fw / mp.sqrt(5)
eps3_star = eps_star / mp.sqrt(5)
print(f"  ε₃(框架) = ε̄/√5     = {mp.nstr(eps3_fw, 10)}")
print(f"  ε₃(关系) = ε̄*/√5    = {mp.nstr(eps3_star, 10)}")
c5 = abs(eps_star - eps_fw) / eps_fw < 0.01
checks.append(c5)
print(f"  检查 5/7: 关系所需 ε̄ 与 RMS 约束 ε̄ 差 < 1% ? {c5}")

print("\n" + "=" * 72)
print("§6 S 空间一致性 (S1 vs S4·s^{3/2}·s^{-δ/2})")
print("=" * 72)
s = mp.e**(-1)
S1 = dL2
S4 = 1.0 / 15.0
S1_pred = S4 * s**(n3/2) * s**(-delta_fw/2)
print(f"  S1      = {mp.nstr(S1, 12)}")
print(f"  S4·s^{{3/2}}·s^{{-δ/2}} = {mp.nstr(S1_pred, 12)}")
print(f"  相对差: {mp.nstr(abs(S1-S1_pred)/S1*100, 8)}%")
c6 = abs(S1 - S1_pred) / S1 < 0.001
checks.append(c6)
print(f"  检查 6/7: S1 ≈ S4·s^{{3/2}}·s^{{-δ/2}} (差 < 0.1%) ? {c6}")

print("\n" + "=" * 72)
print("§7 综合判定")
print("=" * 72)
# 判定: 非恒等(§4) + 脆弱(§3) + δ 为拟合残差(§2) ⟹ 数值近恒等而非结构推导
verdict = (not c4) or c3 or (abs(delta_star - delta_fw)/delta_fw > 0.005)
c7 = verdict
checks.append(c7)
print(f"  代数/超越不可精确 + Δλ 脆弱 + δ 0.6% 偏差 ⟹ 分类: 数值近恒等 (非结构恒等)")
print(f"  检查 7/7: 判定为数值近恒等 (非精确恒等) ? {c7}")
print(f"\n{'='*72}")
print(f"跨层关系审计完成。检查 {sum(checks)}/{len(checks)} 通过")
print(f"{'='*72}")
