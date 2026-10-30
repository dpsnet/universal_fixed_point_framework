# -*- coding: utf-8 -*-
"""
Phase 102 P7-5k：★ v 双路径等价性检验（用户质询驱动）
==============================================================================
路径1（P7-5i）：v = m_τ × 3⁴·∛5（+0.044%）
路径2（P7-5j）：v = m_t × c₁^{α_v−α_t}，α_v = 16/15+√(2/N_c)、α_t = ln7
联立 → m_t/m_τ 框架预言 = 3⁴∛5 / c₁^{α_v−α_t}（若两条路径等价，此式应命中实验 97.19）
检验：等价性 + 缺口诊断（Δα 差被 c₁ 指数放大？）
"""
import math, json

M_T = 172.7          # GeV 实验（PDG pole mass ≈ 172.69）
M_TAU = 1776.86      # MeV 实验
D_H = 2.7095
N_GEN = 3.0
K_MAX = 8.0
SIGMA = 1/15.0
C1 = math.exp(-(D_H+3))        # 框架 c₁ = e^{−(d_H+3)}
ALPHA_T_FW = math.log(7)       # P7-4 框架 α_t = ln7
ALPHA_V_FW = 16/15 + math.sqrt(2/N_GEN)   # P7-5j 框架 α_v = 16/15+√(2/3)
V3_4 = (K_MAX/2)/N_GEN  # 不用
V_OVER_TAU = N_GEN**(K_MAX/2) * (K_MAX-N_GEN)**(1/N_GEN)   # 3⁴·∛5

def dev(f, e): return (f/e-1)*100

print("P7-5k：★ v 双路径等价性检验")
print("="*74)
print("  路径1：v = m_τ × 3⁴∛5（P7-5i，v/m_τ = %.6f）" % V_OVER_TAU)
print("  路径2：v = m_t × c₁^{α_v−α_t}，α_v = %.6f、α_t = %.6f" % (ALPHA_V_FW, ALPHA_T_FW))

print("\n[A] 联立 → m_t/m_τ 框架预言：")
d_alpha = ALPHA_V_FW - ALPHA_T_FW
c1_pow = C1**d_alpha
m_t_over_tau_fw = V_OVER_TAU / c1_pow
m_t_over_tau_exp = M_T*1000/M_TAU
print("  Δα_vt = α_v−α_t = %.6f" % d_alpha)
print("  c₁^{Δα} = e^{−%.6f×%.6f} = %.6f" % (D_H+3, -d_alpha, c1_pow))
print("  m_t/m_τ(框架) = 3⁴∛5 / c₁^{Δα} = %.6f/%.6f = %.4f" % (V_OVER_TAU, c1_pow, m_t_over_tau_fw))
print("  m_t/m_τ(实验) = %.4f（172.7 GeV / 1776.86 MeV）" % m_t_over_tau_exp)
print("  偏差 = %+.4f%%" % dev(m_t_over_tau_fw, m_t_over_tau_exp))

print("\n[B] 路径1 隐含 Δα*（联立反推）：")
d_alpha_star = math.log(V_OVER_TAU*M_TAU/(M_T*1000))/math.log(C1)
print("  Δα* = ln(3⁴∛5·m_τ/m_t)/ln(c₁) = ln(%.6f)/ln(%.6f) = %.6f" % (V_OVER_TAU*M_TAU/(M_T*1000), C1, d_alpha_star))
print("  框架 Δα_vt = %.6f——差 = %.6f（%+.2f%%）" % (d_alpha, d_alpha-d_alpha_star, dev(d_alpha, d_alpha_star)))
print("  指数放大：e^{−ln(c₁)×|ΔΔα|} = e^{%.4f×%.6f} = %.4f（→ m_t/m_τ 偏差 %+.3f%%）" % (D_H+3, abs(d_alpha-d_alpha_star), math.exp((D_H+3)*abs(d_alpha-d_alpha_star)), dev(m_t_over_tau_fw, m_t_over_tau_exp)))

print("\n[C] 缺口诊断（哪个候选精度不足）：")
alpha_v_star = ALPHA_T_FW + d_alpha_star
alpha_t_star = ALPHA_V_FW - d_alpha_star
print("  若 α_t 保持 ln7：α_v* = %.6f（vs 框架 %.6f，差 %+.6f = %+.4f%%）" % (alpha_v_star, ALPHA_V_FW, alpha_v_star-ALPHA_V_FW, dev(alpha_v_star, ALPHA_V_FW)))
print("  若 α_v 保持 16/15+√(2/3)：α_t* = %.6f（vs ln7 = %.6f，差 %+.6f = %+.4f%%）" % (alpha_t_star, ALPHA_T_FW, alpha_t_star-ALPHA_T_FW, dev(alpha_t_star, ALPHA_T_FW)))
print("  两候选各 0.01%/0.05% 精度，但 Δα 差 0.00071 被 c₁ 指数（5.7095）放大 → 0.4%")

print("\n[D] 判定：")
print("  ★ v 双路径等价性：✗ 不成立（0.4% 失调）——m_t/m_τ 框架预言 −0.40% 超 0.1% 标准")
print("  ★ 先证伪成果：α_v(fw) 与 α_t(fw) 不能互相背书——v 的框架身份仅路径1（3⁴∛5）独立可靠")
print("  ★ 诊断：Δα 差 0.00071（α_v 或 α_t 候选精度不足）→ 指数放大成 0.4%")
print("  诚实登记：m_t/m_τ 无独立框架命中（96.80 候选 −0.40% 不达标）")

result = {"m_t_over_tau_fw": m_t_over_tau_fw, "m_t_over_tau_exp": m_t_over_tau_exp, "dev": dev(m_t_over_tau_fw, m_t_over_tau_exp),
          "d_alpha_fw": d_alpha, "d_alpha_star": d_alpha_star, "d_alpha_gap": d_alpha-d_alpha_star,
          "alpha_v_star": alpha_v_star, "alpha_t_star": alpha_t_star,
          "equivalence": "✗ 0.4% 失调——m_t/m_τ 框架预言不达标"}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5k_dual_path.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
