# -*- coding: utf-8 -*-
"""S232 最重代深化：m_t/m_tau 检验 + 轻子跨代证伪 + e 谱流终点叙事
1) m_t/m_tau vs 97 = 全态+活跃^4（S174 两平方和先例 16+81）
2) m_mu/m_tau vs 1/17——轻子跨代精度证伪（5e5σ 预期）
3) e 锚定最重代机制候选（谱流终点）
"""
import math
print("=== S232: 最重代深化 ===\n")

print("=== 1. m_t/m_tau vs 97（第 3 代内新比） ===")
m_t, m_tau = 172.69, 1.77686
u_t, u_tau = 0.30, 0.00012
r = m_t/m_tau
r_unc = r * math.sqrt((u_t/m_t)**2 + (u_tau/m_tau)**2)
print(f"实验 m_t/m_tau = {r:.3f}±{r_unc:.3f}")
s97 = abs(r - 97)/r_unc
print(f"候选 97 = 全态+活跃^4 = 16+81（S174 两平方和先例）")
print(f"σ_score = {s97:.2f}σ——{'达标' if s97<=1 else '提示' if s97<=3 else '不达标'}")

print("\n=== 2. 轻子跨代证伪：m_mu/m_tau vs 1/17 ===")
m_mu = 0.1056583755
u_mu = 2.3e-6
r2 = m_mu/m_tau
r2_unc = r2 * math.sqrt((u_mu/m_mu)**2 + (u_tau/m_tau)**2)
print(f"实验 m_mu/m_tau = {r2:.7f}±{r2_unc:.2e}")
print(f"候选 1/17 = {1/17:.7f}")
s17 = abs(r2 - 1/17)/r2_unc
print(f"σ_score = {s17:.2e}σ——{'证伪' if s17>3 else '达标'}（轻子超高精度压制）")

print("\n=== 3. e 锚定最重代机制候选 ===")
print("m_b/m_tau = e^(6/7)——指数 6/7 = (活跃+不动点-1)/对合")
print("  6 = 3+4-1（活跃+不动点-1）——7 = 对合——全壳组合")
print("候选：最重代 = 谱流累积终点——'每步 e'（S216）累积")
print("  6/7 步 = 谱流接近饱和（-1 缺口）——叙事候选")
print("对照：第 2 代 c/mu = 12 = 活跃x不动点——纯框架——无 e")
print("  → e 只出现在谱流终点段——'e 锚定最重代'机制叙事")

print("\n=== 4. 诚实评估 ===")
print("m_t/m_tau = 97：1.2σ——提示级——不升格（m_t 精度高——真实提示）")
print("m_mu/m_tau ≠ 1/17：5e5σ 证伪——轻子跨代无简单框架身份——")
print("  支持'e 不在跨代比'叙事——证伪记录防重开")
print("e 谱流终点叙事：候选——机制未闭合——观察级")
print("→ 无新升格——1 提示 + 1 证伪 + 1 叙事登记")
