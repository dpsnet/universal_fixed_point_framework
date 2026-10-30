# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-13：κΛ 反推拟合——谱隙链族三路径交叉定位
===========================================================
谱隙链族 {m_e/18, m_ud·(3/8)⁻¹, m_τ/193} 各自反推 κΛ*：
  若三路径收敛到同一 κΛ* < 登记值 401.64 → 登记值系统性偏高（瓶颈定位）
  并扫描 κΛ* 的谱身份。
"""
import json
import math

dH   = math.log(15)
dlam_exact = math.pi/(24*dH+72)
dlam_reg   = 0.0229
m_e  = 0.51099895
m_ud = 3.45
m_tau = 1776.86
kLam_reg = 6/math.pi*210.3

print("="*104)
print("P7-5e-13：κΛ 反推拟合——谱隙链族三路径交叉定位")
print("="*104)
print("  登记 κΛ = %.4f MeV（Λ = 210.3, κ = 6/π）" % kLam_reg)
print("  Δλ_min^(EM) 框架精确 = %.7f / 登记 %.4f" % (dlam_exact, dlam_reg))
print()

for dname, dlam in [("登记值口径", dlam_reg), ("框架精确值口径", dlam_exact)]:
    print("── %s ──" % dname)
    kA = 18*m_e/dlam          # 从 m_e
    kB = m_ud/(dlam*3/8)      # 从 m_ud
    kC = m_tau/(dlam*193)     # 从 m_τ
    print("  κΛ*(m_e)  = 18·m_e/Δλ     = %.4f（vs 登记 %+.4f%%）" % (kA, (kA/kLam_reg-1)*100))
    print("  κΛ*(m_ud) = m_ud/(Δλ·3/8) = %.4f（vs 登记 %+.4f%%）" % (kB, (kB/kLam_reg-1)*100))
    print("  κΛ*(m_τ)  = m_τ/(Δλ·193)  = %.4f（vs 登记 %+.4f%%）" % (kC, (kC/kLam_reg-1)*100))
    spread = max(kA, kB, kC) - min(kA, kB, kC)
    print("  三路径分散 = %.4f MeV（%.3f%%）" % (spread, spread/kLam_reg*100))
    kstar = (kA + kB + kC)/3
    print("  ★ 平均 κΛ* = %.4f（vs 登记 %+.4f%%）" % (kstar, (kstar/kLam_reg-1)*100))
    print()

# 框架精确值口径下最优 κΛ*
kA = 18*m_e/dlam_exact
kB = m_ud/(dlam_exact*3/8)
kC = m_tau/(dlam_exact*193)
kstar = (kA + kB + kC)/3
Lam_star = kstar*math.pi/6
print("κΛ* 的谱身份扫描（框架精确值口径，κΛ* = %.4f）：" % kstar)
print("  Λ* = κΛ*·π/6 = %.4f MeV" % Lam_star)
cands = {
    "210 = (k_max+2·N_gen)/σ": 14/ (1/15),
    "π·67 = π·(k_max²+N_gen)": math.pi*67,
    "210.3（登记）": 210.3,
    "14·15": 210.0,
}
for name, val in cands.items():
    dev = abs(Lam_star - val)/Lam_star*100
    print("  %-28s %10.4f  %s %5.2f%%" % (name, val, "≈" if dev < 0.3 else " ", dev))

cands_k = {
    "402 = 2·N_gen·(k_max²+N_gen)": 2*3*67,
    "401.64（登记）": kLam_reg,
    "401.3（反推均值）": kstar,
    "16·dH·κ·2.315": None,
}
print()
print("判定：")
print("  三路径反推 κΛ* = %.4f（%+.3f%% vs 登记）——均低于登记值" % (kstar, (kstar/kLam_reg-1)*100))
print("  → κΛ 登记值（Λ = 210.3）存在 ~0.1%% 系统性偏高候选（若 Δλ_min 框架值正确）")
print("  → 谱隙链族三命中共享同一绝对标度偏移——非独立缺陷，是 κΛ 精度瓶颈")
print("  Λ* = %.2f 谱身份：210 = (k_max+2·N_gen)/σ 最近（%.3f%%）——候选" % (Lam_star, abs(Lam_star-210)/Lam_star*100))
# 谱定 κΛ 候选检验：Λ = (k_max+2·N_gen)/σ = 210 → κΛ = (6/π)·210
Lam_sp = (8 + 2*3)/(1/15)          # 210
kLam_sp = 6/math.pi*Lam_sp         # 401.07
print()
print("★ 谱定候选检验：Λ = (k_max+2·N_gen)/σ = %d → κΛ = (6/π)·%d = %.4f" % (Lam_sp, Lam_sp, kLam_sp))
for dname, dlam in [("登记值口径", dlam_reg), ("框架精确值口径", dlam_exact)]:
    base = kLam_sp*dlam
    print("  %s：" % dname)
    print("    m_e  = base/18   = %.6f vs 实验 %.6f（%+.4f%%）" % (base/18, m_e, (base/18/m_e-1)*100))
    print("    m_ud = base·3/8  = %.6f vs PDG  %.6f（%+.4f%%）" % (base*3/8, m_ud, (base*3/8/m_ud-1)*100))
    print("    m_τ  = base·193  = %.4f vs 实验 %.4f（%+.4f%%）" % (base*193, m_tau, (base*193/m_tau-1)*100))
print()
print("  谱定 κΛ（401.07）vs 反推 κΛ*（401.24）——0.04%% 内一致")
print("  → Λ 谱定候选（210 = (k_max+2·N_gen)/σ）使三命中全部 <0.1%%（m_e 逼近 0.001%%）")
print()
print("exit 0")
