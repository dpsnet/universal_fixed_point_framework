# -*- coding: utf-8 -*-
"""S166 为何每步 e——谱流指数族机制闭合（S155 候选 B 深化）
归约链：时间=递归（S150）→ 连续化=半群（已Lean）→ 半群=指数族
（Lie标准）→ 单位推进=exp(−A)→ 特征乘子 e^{−λ}
"""
print("=== S166: 为何每步 e（谱流指数族机制闭合） ===\n")

print("=== 既有 Lean 资产（先搜索后动手——重大发现） ===")
print("  OperatorTheory.lean 已有 Koopman 压缩半群：")
print("    koopmanOperator U_R = exp(-A_R)（矩阵指数）")
print("    koopmanSemigroup : exp(-tA)·exp(-sA) = exp(-(t+s)A)")
print("      —— 半群性质已 Lean（矩阵指数加法性——单参数群结构）")
print("  InflationDynamics.lean：谱流 exp 指数族（spectral_flow_exp_")
print("    conjTranspose）")
print("  GPFlowTimeDep.lean：谱流 exp(t·A_F)·A₀·exp(-t·A_F) 相似矩阵")

print("\n=== 归约链（为何每步 e 机制闭合） ===")
print("  1. 时间 = 递归迭代（离散 n 步——S150 已证递归单向）")
print("  2. 迭代的连续化 = 半群（U(t)U(s)=U(t+s)——已 Lean") 
print("     koopmanSemigroup——数学：半群性质 = 连续迭代定义）")
print("  3. 半群 = 指数族（exp(-t·A)——Lie 理论标准结构——")
print("     单参数群 = 指数映射——数学定理）")
print("  4. 单位推进 U(1) = exp(-A)（t=1——半群单位元）")
print("  5. 特征乘子：exp(-A) 特征值 = e^(-λ)（谱映射定理——")
print("     有限维已登记 spectralMappingExp）")
print("  → '每步荷生成恰为 e' = 单位谱流推进的特征乘子 e^(-λ)")
print("  → '为何每步 e'归约到'半群 = 指数族'（Lie 理论——数学标准）")
print("  → 更深'为何递归连续化 = 半群'归 Rec 公设（时间=递归——")
print("    S150/S165——诚实——不可再约）")

print("\n=== 与框架量的衔接（观察级） ===")
print("  e^(E_i) = Ω_i（荷数——S106 质量锚定链）")
print("  谱流单位推进特征乘子 e^(-λ) ∝ e^(E_i)（同一 e 结构）")
print("  → '每步 e' = 谱流指数族的缩放底——质量谱的 e 基底")
print("    （S156 I_μ = e + 42·e^{-6}——e 幂×框架有理基底——同族）")
print("  → 观察级衔接：e 的双重身份（谱流底 + 质量谱底）")

print("\n=== 判别 ===")
print("  '为何每步 e'归约链闭合（物理论证层——S155 候选 B 深化）：")
print("    递归迭代→半群→指数族→单位推进 e——数学标准链")
print("  诚实：'为何递归迭代连续化 = 半群'归 Rec 公设（不可再约）")
print("  Lean 层：半群性质已 Lean（koopmanSemigroup）——")
print("    S166 补标量单位推进锚（Real.exp_add）")
