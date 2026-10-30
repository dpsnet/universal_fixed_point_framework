# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-43：第一/二代谱隙修正成员依赖候选（δ_ud = Δλ_EM/16×(k_max−1)/(k_max+1)）
================================================================
P7-5e-37 遗留：δ_e = 0.0013419、δ_ud = 0.001115、δ_s = 0.001553 vs Δλ_EM/16 = 0.0014333
新候选：δ_ud = Δλ_EM/16×7/9——7/9 = (k_max−1)/(k_max+1)——静默单元对偶比值
"""
import math, json

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
dlam_P20 = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
C  = 2*math.sqrt(math.log(10))
C2 = C*C
kappa = 6/math.pi
Lam  = 16*math.log(10)*(dH+3)
kL   = kappa*Lam
sigma = 1/15
kmax, Ngen = 8, 3
alpha0 = 1/2
alpha0_3 = alpha0**3
N_total = kmax - Ngen

delta0 = dlam_EM/16
delta_e_req, delta_ud_req, delta_s_req = 0.0013419, 0.001115, 0.001553

print("="*104)
print("P7-5e-43：谱隙修正成员依赖候选（静默单元对偶比值）")
print("="*104)

print()
print("【δ 成员依赖回顾（P7-5e-37）】")
print("-"*104)
print("δ_e  = %.7f（轻子第一代）——m_e 精确 PDG——δ 精确" % delta_e_req)
print("δ_ud = %.7f（夸克第一代）——m_ud = 3.45 中心值（±8.6%%）——δ 有不确定度" % delta_ud_req)
print("δ_s  = %.7f（夸克第二代）——m_s = 93.4（±30%%）——δ 有不确定度" % delta_s_req)
print("Δλ_EM/16 = %.7f（谱隙基准）" % delta0)
print()
print("【候选结构】")
print("-"*104)
cand = {
 "δ_ud = Δλ_EM/16×(k_max−1)/(k_max+1) = 7/9": delta0*(kmax-1)/(kmax+1),
 "δ_s  = Δλ_EM/16×13/12": delta0*13/12,
 "δ_e  = Δλ_EM/16×15/16": delta0*15/16,
}
for name, v in cand.items():
    print("%s = %.7f" % (name, v))
print()
print("【精确度评估】")
print("-"*104)
for name, v in cand.items():
    target = delta_e_req if "δ_e" in name else (delta_ud_req if "δ_ud" in name else delta_s_req)
    dev = (v/target-1)*100
    print("%-56s vs 目标 %.7f——差 %+6.3f%%" % (name, target, dev))
print()
print("【7/9 的框架身份】")
print("-"*104)
print("7/9 = (k_max−1)/(k_max+1) = %d/%d——k_max±1 比值" % (kmax-1, kmax+1))
print("→ 静默单元对偶比值：k_max−1 = 7（乘法静默）除以 k_max+1 = 9")
print("→ δ_ud 修正 = 谱隙基准 × 静默单元对偶比值——第一代夸克的谱隙修正含静默结构！")
print()
print("【15/16 与 13/12 的框架身份检查】")
print("-"*104)
print("15/16：15 = N_gen×(k_max−N_gen) = 3×5 ✓——16 = ？——Λ 的 16 因子（16·ln10·(d_H+3)）——但 16 本身身份开放")
print("13/12：13 = k_max+N_gen+2？——2 无身份——13/12 不干净")
print("→ 15/16 部分结构（15 = 3×5）但 16 开放；13/12 不干净——均弱于 7/9")
print()
print("【结论】")
print("-"*104)
print("1. ★★ δ_ud = Δλ_EM/16×(k_max−1)/(k_max+1) = 7/9——唯一干净框架候选（静默单元对偶比值）")
print("   ——第一/二代谱隙修正成员依赖的第一个机制候选（ud 用 7/9）")
print("2. δ_e 的 15/16（差 0.13%——m_e 精确故偏差真实）不命中；δ_s 的 13/12（目标不确定）不干净")
print("3. ★ 谱隙修正成员依赖方向：δ = Δλ_EM/16×f(成员)——f 含静默单元对偶结构（ud 的 7/9）")
print("4. 诚实边界：δ_ud 目标来自 m_ud 中心值（±8.6% 不确定度）——0.02% 命中在不确定度内——方向性候选")
print("   δ_e/δ_s 无干净候选保持开放；为何 ud 用 7/9（成员选择机制）开放")
print()
json.dump({"delta0": delta0, "deltas": {"e": delta_e_req, "ud": delta_ud_req, "s": delta_s_req},
           "cand_ud": {"form": "dlam_EM/16*(kmax-1)/(kmax+1)", "value": cand["δ_ud = Δλ_EM/16×(k_max−1)/(k_max+1) = 7/9"], "dev_pct": (cand["δ_ud = Δλ_EM/16×(k_max−1)/(k_max+1) = 7/9"]/delta_ud_req-1)*100},
           "cand_s": cand["δ_s  = Δλ_EM/16×13/12"], "cand_e": cand["δ_e  = Δλ_EM/16×15/16"]},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e43_delta_member.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
