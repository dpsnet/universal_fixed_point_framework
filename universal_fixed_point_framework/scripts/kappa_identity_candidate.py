# -*- coding: utf-8 -*-
"""κ 框架身份候选验证（2026-10-26）

候选：κ = 对合域×(√3+1)/(幂基×静默) = 7(√3+1)/10
（√3 来自 Δλ_P20 = (√3−1)/N_gen! 框架基谱隙家族——κΛ×Δλ_P20 = 对合域²）
"""
import math

powers, ngen, silence, involution, fixed = 2, 3, 5, 7, 4
kmax = powers**ngen

# 口径
dlam_p20 = (math.sqrt(3)-1)/6   # (√3−1)/N_gen!
kl_49a = 49.0039                # 恒等 B（104az-69）
kl_49b = 49.0021                # 登记
kl_a = kl_49a / dlam_p20
kl_b = kl_49b / dlam_p20
print(f"Δλ_P20 = {dlam_p20:.10f}")
print(f"κΛ 口径 A = {kl_a:.6f}、口径 B = {kl_b:.6f}")

# 候选 κ
kappa_cand = involution*(math.sqrt(3)+1)/(powers*silence)
print(f"\n=== κ 候选：对合域×(√3+1)/(幂基×静默) ===")
print(f"κ_cand = 7×(√3+1)/10 = {kappa_cand:.10f}")
for name, kl in (("A", kl_a), ("B", kl_b)):
    kappa = kl/210
    dev = (kappa_cand - kappa)/kappa
    print(f"  口径 {name}：κ = {kappa:.6f}——κ_cand 差 {dev*100:.5f}%")
print(f"  κΛ_cand = 7(√3+1)×210/10 = 147(√3+1) = {147*(math.sqrt(3)+1):.6f}")
for name, kl in (("A", kl_a), ("B", kl_b)):
    print(f"  vs 口径 {name} κΛ = {kl:.4f}——差 {(147*(math.sqrt(3)+1)-kl)/kl*100:.5f}%")

print("\n=== 代数结构 ===")
print("κΛ_cand = 147(√3+1) = 3×49(√3+1) = N_gen×对合域²×(√3+1)")
print("κΛ_cand×Δλ_P20 = 147(√3+1)×(√3−1)/6 = 147×2/6 = 49 = 对合域² ✓")
print("——κ 候选满足 κΛ×Δλ_P20 = 对合域² 恒等（代数闭环）")

print("\n=== 判别 ===")
print(f"κ_cand 差 0.005~0.008%（口径 B/A）——判据 0.001% 级未达——登记为候选身份")
print("（代数优雅：对合域×(√3+1)/(幂基×静默)——√3 谱隙家族延伸——非精确锁定）")
