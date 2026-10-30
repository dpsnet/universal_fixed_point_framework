# -*- coding: utf-8 -*-
"""m_s/T_c 静默族分解验证 + 静默⁻² 双链（2026-10-26）

旧身份：m_s/T_c = 320/648000（320 = 静默×k_max²——本批 S16）
新候选：648000 = 静默³×k_max²×N_gen⁴ → m_s/T_c = 1/(静默²×N_gen⁴)
静默⁻² 双链：Δλ_4 = 静默⁻²×(231/232)、m_s/T_c = 静默⁻²×N_gen⁻⁴
"""
import math

powers, ngen, silence = 2, 3, 5
kmax = powers**ngen
sigma = 1/15

print("=== 648000 静默族分解 ===")
print(f"静默³×k_max²×N_gen⁴ = {silence**3}×{kmax**2}×{ngen**4} = {silence**3*kmax**2*ngen**4}——648000: {silence**3*kmax**2*ngen**4 == 648000}")
print()

print("=== m_s/T_c 新身份 ===")
mstc = 320/648000
cand = 1/(silence**2 * ngen**4)
print(f"m_s/T_c = 320/648000 = {mstc:.10f}")
print(f"1/(静默²×N_gen⁴) = 1/({silence**2}×{ngen**4}) = {cand:.10f}——恒等: {mstc == cand}")
print()

print("=== 静默⁻² 双链 ===")
print("Δλ_4 = 静默⁻²×(231/232) = (1/25)×(231/232) = 0.0398276（S13 已机检）")
print(f"m_s/T_c = 静默⁻²×N_gen⁻⁴ = (1/25)×(1/81) = {cand:.10f}")
print("——静默⁻² 两处独立出现（谱参数宿主 + m_s/T_c）——静默族公共结构第二例")
print()

print("=== 静默族公共结构谱（更新）===")
print("6σ³ = N_gen!·σ³（轻子排列——双链：α_v^l、ε_μ）")
print("静默⁻² = 1/25（双链：Δλ_4、m_s/T_c）")
print("k_max 投影：ε_μ 系数 {1, 2/75, 8}、320 = 静默×k_max²")
print("σ³×静默 = 1/675（675 家族）")
print()

print("=== 判别 ===")
print("静默族公共结构：排列（6σ³）、静默⁻²（双链）、k_max-投影——")
print("均为'冻结窗口幂次组合'——机制候选统一（仍观察级）")
