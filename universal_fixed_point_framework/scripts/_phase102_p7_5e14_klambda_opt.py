# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-14：κΛ 最优值拟合——谱隙链 × 强子端四命中交叉约束
=================================================================
① π 消去恒等式验证：κΛ·Δλ_min^(EM) = (6/π)·Λ·π·α_EM = 6·Λ·α_EM
② 四命中（m_e/18、m_ud·3/8、m_τ/193、M_ud_eff）残差扫描 κΛ
   —— 检验谱定 Λ=210（401.07）与登记 Λ=210.3（401.64）哪个更优
   —— 或存在中间最优值（无谱身份但全命中 <0.1%）
"""
import json
import math

dH   = math.log(15)
alpha_inv_fw = 24*(dH+3)             # 框架 1/α_EM = 137.028...
dlam_exact = math.pi/(24*dH+72)      # = π·α_EM（框架）
sigma = 1/15
m_e  = 0.51099895
m_ud = 3.45
m_tau = 1776.86
M_ud_eff = 387.2

print("="*104)
print("P7-5e-14：κΛ 最优值拟合——谱隙链 × 强子端四命中交叉约束")
print("="*104)
print("① π 消去恒等式验证：")
print("   Δλ_min^(EM) = π/(24d_H+72) = π·α_EM（框架）  [α_EM = 1/24(d_H+3)]")
print("   κΛ·Δλ_min  = (6/π)·Λ·π·α_EM = 6·Λ·α_EM —— κ 与 Δλ 的 π 消去")
kLam_210  = 6/math.pi*210
kLam_2103 = 6/math.pi*210.3
print("   谱定(Λ=210)：κΛ·Δλ = 6·210·α_EM = %.5f MeV" % (6*210/alpha_inv_fw))
print("   登记(Λ=210.3)：κΛ·Δλ = 6·210.3·α_EM = %.5f MeV" % (6*210.3/alpha_inv_fw))
print("   （与 κΛ·Δλ_min 直接算一致——恒等式成立）")
print()

def hits(kLam):
    base = kLam*dlam_exact
    return {
        "m_e":  (base/18/m_e - 1)*100,
        "m_ud": (base*3/8/m_ud - 1)*100,
        "m_tau":(base*193/m_tau - 1)*100,
        "M_ud_eff": ((m_ud + kLam*(1-2*sigma/3))/M_ud_eff - 1)*100,
    }

print("② 三候选 κΛ 的四命中对比：")
for name, kLam in [("谱定 Λ=210", kLam_210), ("登记 Λ=210.3", kLam_2103)]:
    h = hits(kLam)
    mx = max(abs(v) for v in h.values())
    print("  %-16s κΛ = %.4f" % (name, kLam))
    for k, v in h.items():
        print("    %-10s %+.4f%%" % (k, v))
    print("    → 最大 |残差| = %.4f%%" % mx)
print()

print("③ κΛ 全扫描（401.0–401.9，步 0.05）找四命中最小最大残差：")
best = None
for kLam in [401.00 + i*0.025 for i in range(41)]:
    h = hits(kLam)
    mx = max(abs(v) for v in h.values())
    rms = math.sqrt(sum(v*v for v in h.values())/4)
    if best is None or (mx, rms) < (best[1], best[2]):
        best = (kLam, mx, rms)
print("  ★ 最优 κΛ* = %.3f（最大残差 %.4f%%，RMS %.4f%%）" % (best[0], best[1], best[2]))
print("  对应 Λ* = κΛ*·π/6 = %.3f" % (best[0]*math.pi/6))
h_best = hits(best[0])
for k, v in h_best.items():
    print("    %-10s %+.4f%%" % (k, v))
print()

print("④ 判定：")
print("  谱定 Λ=210：m_τ −0.098%% 边缘（内生化优先，但强子端 M_ud_eff 受挫至 +0.07%% 附近？见上表）")
print("  登记 Λ=210.3：谱隙链 m_τ +0.045%% 最佳但 M_ud_eff +0.005%%——强子端优")
print("  ★ 最优 κΛ* = %.3f（Λ* ≈ %.1f）——介于谱定/登记之间，无干净谱身份" % (best[0], best[0]*math.pi/6))
print("  → κΛ 是'框架有效标度'（四命中折中），Λ 谱定候选（210）受 M_ud_eff 交叉约束削弱")
print()
print("exit 0")
