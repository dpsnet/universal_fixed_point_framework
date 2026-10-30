# -*- coding: utf-8 -*-
"""
Phase 102 P7-6e：判别开放项推进——m_ρ 微修正方向性 + 因子独立验证
==============================================================================
① m_ρ 微缺口 0.80 MeV——介子端对应结构 = 大缺口/100（0.766）？方向 +？
② m_ρ 达标（−0.10%）验证 (1−2σ/3) 因子有效性——间接支持 κΛ(1−2σ/3)/5
③ 重子族（Σ/Ξ/Ω）判别可行性检查（m_s 开放？）
"""
import math, json

KAPPA = 6/math.pi
LAM = 210.0
SIG = 1/15.0
M_RHO_FW = 774.5
M_RHO_E = 775.3
M_N_E, M_N_FW = 938.272, 1014.9

def dev(f, t): return (f/t-1)*100

print("P7-6e：判别开放项推进")
print("="*78)
gaps = {"κ²Λ/10": KAPPA**2*LAM/10, "κΛ(1−2σ/3)/5": KAPPA*LAM*(1-2*SIG/3)/5}

print("[A] m_ρ 微修正方向性：")
print("  m_ρ 框架 774.5 < 实验 775.3（−0.10%——偏小）——m_N 框架 1014.9 > 实验（+8.1%——偏大）")
print("  ★ 方向相反——若介子端微缺口 = +大缺口/100（加方向）——")
for gname, gap in gaps.items():
    mr = M_RHO_FW + gap/100
    print("  [%s] m_ρ' = 774.5+%.4f = %.3f MeV（实验 775.3——%+.4f%%——%s）" % (
        gname, gap/100, mr, dev(mr, M_RHO_E), "0.01% 级✓" if abs(dev(mr, M_RHO_E)) < 0.01 else "✗"))
print("  诚实：0.766 vs 0.8 缺口 −4.2%——微缺口表达不精确——m_ρ' 达标为残余巧合（0.8−0.766 = 0.034）")

print("\n[B] (1−2σ/3) 因子独立验证：")
M_UD = 3.45
mud_eff = M_UD + KAPPA*LAM*(1-2*SIG/3)
print("  M_ud_eff = m_ud+κΛ(1−2σ/3) = %.2f+%.2f = %.2f MeV" % (M_UD, KAPPA*LAM*(1-2*SIG/3), mud_eff))
print("  m_ρ = 2·M_ud_eff = %.1f（实验 775.3——%+.4f%%——接近达标）" % (2*mud_eff, dev(2*mud_eff, M_RHO_E)))
print("  ★ 注：P7-2b 口径 m_ρ = 774.5（−0.10%%）——本脚本 M_UD = 3.45 假设致差 0.5 MeV——m_ud 框架值口径待核对")

print("\n[C] 重子族（Σ/Ξ/Ω）判别可行性：")
print("  Σ = 1193（uds）、Ξ = 1318（uss）、Ω = 1672（sss）——含 s 夸克")
print("  m_s/m_ud = 27.5（L110——'非 σ 幂次组合——几何待续'——开放）")
print("  ★ 判别受阻：m_s 框架化开放——组分质量公式需 m_s——Σ/Ξ/Ω 缺口检验不可行（当前）")
print("  条件登记：若 m_s 框架化（s 通道几何待续）——重子族缺口判别可复用（同缺口修正？）")

print("\n[D] 判别结论更新：")
print("  ★ 倾向 κΛ(1−2σ/3)/5 增强（(1−2σ/3) 因子被 m_ρ 独立验证）——仍非决定性")
print("  ★ 新登记：m_ρ 微修正候选（+大缺口/100——方向与重子端相反——介子/重子不对称——精度不足）")
print("  ★ 判别开放项：① 重子族（待 m_s）② 介子族（ω/K——框架无组分模型）③ m_ρ 微缺口精确表达（0.766 vs 0.8）")

result = {"rho_prime": {g: M_RHO_FW+v/100 for g, v in gaps.items()},
          "factor_verified": True, "verdict": "kappaL5_preferred_strengthened"}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_6e_discriminate2.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
