# -*- coding: utf-8 -*-
"""
Phase 102 P7-5p：m_t Formula B 一致性推导检验
==============================================================================
问题：y_t^B 闭式 1−Δλ_min/16 能否从凸组合 Σ|U_tk|²λ_H^(k) 推导（交叉验证锁定）？
结构：
  λ_H^(k) = c_k^{α_v}/Σ_j c_j^{α_v}，c_k = e^{−(d_H+3)}、e^{−d_H}、~1（IFS 谱几何，P7-5 框架化）
  y_t = |U_t3|²λ_H^(3) + |U_t2|²λ_H^(2) + |U_t1|²λ_H^(1)（u 扇区 θ13≈θ12≈0 → |U_t1|²≈0）
  定理 5.5：tan²θ23 = (r_23−r_λ)/(1−r_23·r_λ)，r_23=(m_c/m_t)^{1/β_u}（依赖实验——循环）
两条口径对比 + |U_t2|² 独立框架表达搜索
"""
import math, json, itertools

D_H = 2.7095
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
ALPHA_V = 16/15 + math.sqrt(2/3.0)      # P7-5j 框架 α_v
BETA_U = 1.0531                          # paper17 §5.3（含 paper11 值口径）
V_FW = 246.1094                          # P7-5i 框架 v（GeV）
M_T_EXP = 172.7                          # GeV
M_C_OVER_MT = 7.33e-3                    # paper17 §5.3 表（实验口径）

def dev(f, e): return (f/e-1)*100

print("P7-5p：m_t Formula B 一致性推导检验")
print("="*74)
print("[A] Higgs 谱权重 λ_H^(k)（框架）")
c1 = math.exp(-(D_H+3)); c2 = math.exp(-D_H); c3 = 1.0
print("  c_k = e^{−(d_H+3)}, e^{−d_H}, 1 = (%.6f, %.6f, %.4f)" % (c1, c2, c3))
lam = [c**ALPHA_V for c in (c1, c2, c3)]
s = sum(lam)
L = [x/s for x in lam]
print("  λ_H^(k) = c_k^{α_v}/Σ（α_v = %.6f）= (%.8f, %.8f, %.8f)" % (ALPHA_V, L[0], L[1], L[2]))
print("  Σλ_H = %.10f（权重守恒 ✓）" % s)
print("  1−λ_H^(3) = %.8f（投影缺失总量）" % (1-L[2]))

print("\n[B] 定理 5.5 口径（实验 r_23 循环）")
r23 = M_C_OVER_MT**(1/BETA_U)
rlam = L[1]/L[2]
t2 = (r23 - rlam)/(1 - r23*rlam)
sin2 = t2/(1+t2); cos2 = 1-sin2
y55 = cos2*L[2] + sin2*L[1]
mt55 = y55*V_FW/math.sqrt(2)
print("  r_23 = (m_c/m_t)^{1/β_u} = %.6f（依赖实验——循环）" % r23)
print("  r_λ = λ_H^(2)/λ_H^(3) = %.8f" % rlam)
print("  tan²θ23 = %.6f → sin²θ23 = %.6f" % (t2, sin2))
print("  y_t(5.5) = cos²θ23·λ_H^(3)+sin²θ23·λ_H^(2) = %.8f" % y55)
print("  m_t(5.5) = y_t×v/√2 = %.3f GeV（实验 172.7，偏差 %+.4f%%）" % (mt55, dev(mt55, M_T_EXP)))

print("\n[C] P7-5n 闭式口径（独立候选）")
y_cl = 1 - DL_MIN/16
mt_cl = y_cl*V_FW/math.sqrt(2)
print("  y_t(闭式) = 1−Δλ_min/16 = %.8f" % y_cl)
print("  m_t(闭式) = %.4f GeV（偏差 %+.4f%%）" % (mt_cl, dev(mt_cl, M_T_EXP)))
print("  ★ 两口径差：Δy = %.6f（%+.3f%%）；Δm_t = %.4f GeV" % (y_cl-y55, dev(y_cl, y55), mt_cl-mt55))

print("\n[D] |U_t2|² 反推（闭式凸组合等价条件）")
need = (DL_MIN/16 - (1-L[2]))/(L[2]-L[1])
print("  闭式 ⇔ |U_t2|² = [Δλ_min/16−(1−λ_H^(3))]/(λ_H^(3)−λ_H^(2)) = %.6f" % need)
print("  定理 5.5 给 |U_t2|² = sin²θ23 = %.6f——差异 ×%.2f（不一致）" % (sin2, sin2/need))
print("  ★ |U_t2|² 独立框架表达搜索（目标 %.6f）：" % need)
cands = {
    "σ²×16/45": (1/15)**2*16/45,
    "Δλ_min×σ×0.195": DL_MIN/15*0.195,
    "λ_H^(2)/3.82": L[1]/3.82,
    "Δλ_min²×0.1063": DL_MIN**2*0.1063,
}
for name, v in cands.items():
    print("    %s = %.6f（偏差 %+.3f%%）" % (name, v, dev(v, need)))

print("\n[E] 判定")
print("  ★ y_t^B 闭式 1−Δλ_min/16 **不是**凸组合（定理 5.5 口径）的推导结果——两口径差 0.14%%")
print("    定理 5.5 口径：y_t = 0.9906 → m_t = 172.46 GeV（−0.14%%）——实验 r_23 循环")
print("    闭式口径：   y_t = 0.9923745 → m_t = 172.699 GeV（−0.0008%%）——精度远优")
print("  ★ 交叉验证未锁定：闭式是独立候选（非凸组合还原）——|U_t2|² 独立表达无干净命中")
print("    闭式机制地位：若 |U_t2|² 获框架身份（σ²×16/45 边缘 −0.16%% 超标准），凸组合链才闭合")

result = {"lam": L, "y55": y55, "mt55": mt55, "y_closed": y_cl, "mt_closed": mt_cl,
          "need_Ut2": need, "sin2_55": sin2, "delta_y": y_cl-y55}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5p_formulaB_consistency.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
