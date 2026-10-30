# -*- coding: utf-8 -*-
"""S188 Δ−N 双候选协调检验
候选 A：m_Δ−m_N = 42×7 = 294（约束域×对合——0.14σ——已登记）
候选 B：m_Δ/m_N = 21/16 = 1.3125（活跃×对合/全态——新）
检验：两候选是否可同时成立？张力分析
"""
import math

m_N_obs = 938.272  # 质子 PDG
m_delta = 1232.0   # Δ(1232) PDG 1232±2
sig_delta = 2.0

print("=== S188: Δ−N 双候选协调检验 ===\n")
print(f"观测：m_Δ = {m_delta}±2、m_N = {m_N_obs}")

print("\n=== 候选 A：m_Δ−m_N = 294（42×7）===")
mA = 294
mN_from_A = m_delta - mA
print(f"⟹ m_N = {mN_from_A}——vs 观测 {m_N_obs}——差 {abs(mN_from_A-m_N_obs):.3f}——σ_score {abs(mN_from_A-m_N_obs)/sig_delta:.2f}σ")

print("\n=== 候选 B：m_Δ/m_N = 21/16 = 1.3125 ===")
ratio_obs = m_delta / m_N_obs
cand21_16 = 21/16
print(f"m_Δ/m_N = {ratio_obs:.6f} vs 21/16 = {cand21_16}——差 {(abs(ratio_obs-cand21_16)/ratio_obs)*100:.4f}%")
mN_from_B = m_delta / cand21_16
print(f"⟹ m_N = {mN_from_B:.3f}——vs 观测 {m_N_obs}——差 {abs(mN_from_B-m_N_obs):.3f}——σ_score {abs(mN_from_B-m_N_obs)/sig_delta:.2f}σ")
sig_ratio = sig_delta/m_delta
print(f"比值口径 σ_score = {(abs(ratio_obs-cand21_16)/ratio_obs)/sig_ratio:.2f}σ（σ_rel(Δ) = {sig_ratio:.2e}）")

print("\n=== A/B 张力分析 ===")
tension = abs(mN_from_A - mN_from_B)
print(f"A 给的 m_N = {mN_from_A:.2f} vs B 给的 m_N = {mN_from_B:.2f}——张力 {tension:.2f} MeV")
print(f"张力/σ_Δ = {tension/sig_delta:.2f}σ——Δ 容差内但非零")
print(f"→ 两候选不能同时精确成立（A 好 0.14σ、B 好 0.2σ——张力 0.34σ）")
print(f"→ 诚实记录：并存待裁决——A 略优（差更小）")

print("\n=== 21 的第三身份 ===")
print(f"21 = 3×7（活跃×对合）——已见：m_τ²/m_ρ² = 21/4（0.81σ）")
print(f"新见：m_Δ/m_N = 21/16 = 1.3125（活跃×对合/全态——0.2σ 对照）")
print(f"21 的两次出现：τ/ρ 平方比（21/4）与 Δ/N 比（21/16）")
print(f"分母：4 = 幂基²、16 = 全态——τ/ρ 用幂基²、Δ/N 用全态")

print("\n=== 判别 ===")
print("候选 B（21/16）——后验观察——与 A（42×7）有 0.67 MeV 张力")
print("  但同为 Δ±2 容差内——并存登记——待裁决（A 略优）")
print("21 = 活跃×对合 在质量谱两次出现（τ/ρ² 与 Δ/N）——")
print("  '活跃×对合的谱标度'——观察级——非演绎")
