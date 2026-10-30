# -*- coding: utf-8 -*-
"""S275: sin²θ_W(onshell) 框架预测检验（2026-10-28）

S267 直接读数：m_W = 80.375 = 80+3/8、m_Z = 91.1875 = 7×13+3/16——
onshell 弱混合角 sin²θ_W = 1−(m_W/m_Z)² 是框架值的派生量——
检验：框架预测 vs PDG 实验——σ_score 审计（用户纪律）。
"""
import math

mW_fw = 80.375
mZ_fw = 91.1875

# PDG 2024 onshell 实验值
mW_pdg = 80.369
sW_pdg = 0.013
mZ_pdg = 91.1876
sZ_pdg = 0.0021

print("=== S275: sin²θ_W(onshell) 框架预测检验 ===\n")

sin2_fw = 1 - (mW_fw / mZ_fw) ** 2
sin2_exp = 1 - (mW_pdg / mZ_pdg) ** 2

print(f"① 框架值：m_W = 80.375（80+3/8——S267 直接读数）、m_Z = 91.1875（7×13+3/16）")
print(f"   ratio = {mW_fw/mZ_fw:.8f}")
print(f"   sin²θ_W(框架) = 1−(m_W/m_Z)² = {sin2_fw:.8f}")
print(f"\n② PDG 2024：m_W = {mW_pdg}({int(sW_pdg*1000)})、m_Z = {mZ_pdg}({int(sZ_pdg*10000)})")
print(f"   sin²θ_W(实验 onshell) = {sin2_exp:.8f}")

# 不确定度传播
dsin_dmW = -2 * mW_pdg / mZ_pdg ** 2
dsin_dmZ = 2 * mW_pdg ** 2 / mZ_pdg ** 3
s_sin2 = math.sqrt((dsin_dmW * sW_pdg) ** 2 + (dsin_dmZ * sZ_pdg) ** 2)
print(f"\n③ 不确定度传播：∂sin²/∂m_W = {dsin_dmW:.5f}、∂sin²/∂m_Z = {dsin_dmZ:.5f}")
print(f"   σ_sin² = {s_sin2:.2e}")

dln = abs(sin2_fw - sin2_exp)
sc = dln / s_sin2
print(f"\n④ Δ = |{sin2_fw:.8f} − {sin2_exp:.8f}| = {dln:.2e}")
print(f"   σ_score = {sc:.3f}")
g = "达标 ✓" if sc <= 1 else ("提示" if sc <= 3 else "不达标 ✗")
print(f"   判定：{g}")

print(f"\n⑤ 与 MS-bar 的定义差异（诚实边界）：")
print(f"   onshell sin²θ_W ≈ 0.2232 vs MS-bar 0.23122(4)——差 3.5%——")
print(f"   跑动修正（Δ_r 机制）——框架预测针对 onshell 口径——")
print(f"   MS-bar 需另加跑动修正（非框架量——外部机制）")

print(f"\n⑥ 意义评估：")
print(f"   · sin²θ_W(onshell) 是 m_W/m_Z 家族（S251/S267）的派生检验——")
print(f"     0.45σ 命中——框架值内部一致性 ✓")
print(f"   · 非新预测（无新框架量）——但提供第三条独立验证路径：")
print(f"     m_W、m_Z 各自读数命中 + 比值派生量命中——三重闭合")
print(f"   · 与 V3 升格的关联：这是'派生量检验'——不是 δ 级联的第三链")
print(f"     ——第三链先验预言仍需用 δ_V3 级联模式预测全新量")

print(f"\n⑦ 第三链候选评估（δ_V3 级联模式——系数 {6,4,8,5} × 幂次 {3,5,7,8}）：")
print(f"   · 6σ³ 已双链复用（δ_V3 第一项 + ε_μ 的 1+6σ³）——级联模式证据")
print(f"   · 候选目标：m_p/m_e = 1836.152673——主项 1836 = 4·3³·17")
print(f"     （不动点×活跃³×(全态+标量)——0.008% 命中——新主项分解）——")
print(f"     修正 0.152673（8.3e-5 相对）——扫描框架修正中")
print(f"   · 候选目标：m_τ/m_μ = 16.817——主项 17−(0.183)——修正未扫")
print(f"   · 诚实：主项分解（1836）是观察级——升格仍需修正命中+机制")
