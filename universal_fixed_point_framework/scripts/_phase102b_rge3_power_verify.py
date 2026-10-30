# -*- coding: utf-8 -*-
"""
Phase 102b 2c-M (a')：rge3 幂恒等式 Lean 形式化的数值真值检验（2026-10-10）
按 mufpf-formalization-env 先证伪再证明：逐字翻译 Lean 命题 → 计算残差（容差 1e-8）
定理候选（Rge3SpectralIdentity.lean）：
  rge3_power_identity : 2 ^ (c_qcd) = (dl3 / dlmin) ^ (Nc ^ 2 / 2)
    ——c_qcd = (Nc/2)² = 9/4、dl3/dlmin = √2、Nc = 3
    ——即 2^{9/4} = (√2)^{9/2}——B₀=C_QCD 通量常数的幂恒等式
  rge3_flux_identity : π²·2^{c_qcd} = π²·(dl3/dlmin)^{Nc²/2}（组合）
"""
import math

print("="*78)
print("rge3 幂恒等式数值真值检验（先证伪再证明）")
print("="*78)

# ---- Lean 定义逐字翻译（MassChainConstants.lean）----
Nc = 3.0
Nf = 3.0
c_qcd = (Nc / 2) ** 2      # = 9/4
dlmin = (math.sqrt(3) - 1) / 6
dl3 = math.sqrt(2) * dlmin
Nc_sq_over_2 = Nc ** 2 / 2  # = 9/2

# ---- 定理 1：rge3_power_identity ----
lhs1 = 2 ** c_qcd
rhs1 = (dl3 / dlmin) ** Nc_sq_over_2
print(f"\n定理 1: 2^c_qcd = (dl3/dlmin)^(Nc²/2)")
print(f"   c_qcd = (Nc/2)² = {c_qcd:.10f}（9/4）")
print(f"   dl3/dlmin = √2 = {dl3/dlmin:.10f}")
print(f"   Nc²/2 = {Nc_sq_over_2:.10f}（9/2）")
print(f"   LHS = 2^{c_qcd:.4f} = {lhs1:.12f}")
print(f"   RHS = (√2)^{Nc_sq_over_2:.4f} = {rhs1:.12f}")
res1 = abs(lhs1 - rhs1)
print(f"   残差 = {res1:.2e}——容差 1e-8: {'✓ 通过' if res1 < 1e-8 else '✗ 失败'}")
print(f"   参考: 2^(9/4) = {2**2.25:.12f}——(√2)^(9/2) = {math.sqrt(2)**4.5:.12f}")

# ---- 定理 2：rge3_flux_identity（组合——乘 π²）----
pi2 = math.pi ** 2
lhs2 = pi2 * 2 ** c_qcd
rhs2 = pi2 * (dl3 / dlmin) ** Nc_sq_over_2
print(f"\n定理 2: π²·2^c_qcd = π²·(dl3/dlmin)^(Nc²/2)")
print(f"   LHS = {lhs2:.12f}")
print(f"   RHS = {rhs2:.12f}")
res2 = abs(lhs2 - rhs2)
print(f"   残差 = {res2:.2e}——容差 1e-8: {'✓ 通过' if res2 < 1e-8 else '✗ 失败'}")
print(f"   与 π²·2^B₀ 目标一致: {lhs2:.8f}（2c-K 发现）")

# ---- 定理 3（辅助）：c_qcd = 9/4、Nc²/2 = 9/2、dl3/dlmin = √2 ----
print(f"\n定理 3（辅助恒等式）:")
print(f"   c_qcd = (Nc/2)²: {c_qcd:.10f}——9/4 = {9/4:.10f}——残差 {abs(c_qcd-9/4):.2e}")
print(f"   Nc²/2: {Nc_sq_over_2:.10f}——9/2 = {9/2:.10f}——残差 {abs(Nc_sq_over_2-9/2):.2e}")
print(f"   (dl3/dlmin)² = 2: {(dl3/dlmin)**2:.10f}——残差 {abs((dl3/dlmin)**2-2):.2e}")

# ---- 随机样本稳健性（全称命题对应）----
print(f"\n随机样本稳健性（6 组——幂恒等式结构）:")
ok = True
for i in range(6):
    # 变体：2^(a·9/4) = (√2)^(a·9/2) 对任意 a∈{0.5..3}
    a = 0.5 + i * 0.5
    L = 2 ** (a * c_qcd)
    R = (dl3 / dlmin) ** (a * Nc_sq_over_2)
    r = abs(L - R)
    flag = "✓" if r < 1e-8 else "✗"
    if r >= 1e-8: ok = False
    print(f"   a={a:.1f}: 2^(a·{c_qcd:.2f})={L:.10e} vs (√2)^(a·{Nc_sq_over_2:.2f})={R:.10e}——残差 {r:.2e} {flag}")
print(f"   全 6 组通过: {ok}")
