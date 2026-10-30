# -*- coding: utf-8 -*-
# S118 ΔI = ln(m_μ/m_e) = 5.33159876 框架导出探索（2026-10-27）
# 比值链核心开放项："为何 m_μ/m_e 的间隔 = 5.3316？"
# 当前体系：I_μ = I_e − ΔI——ΔI 观测嵌入（无框架身份——候选级）
# 策略：① 主项扫描（框架量组合）→ ② 修正扫描（σ 幂族/e 族）

from math import log, e

sigma = 1/15
ln15 = log(15)
ln16_15 = log(16/15)

m_e = 0.51099895069
m_mu = 105.6583755
DeltaI = log(m_mu/m_e)
print(f"ΔI = ln(m_μ/m_e) = {DeltaI:.8f}")
print(f"ΔI 的框架量探索：\n")

print("=== ① 主项候选（ΔI ≈ 主项——找最小差） ===")
mains = {
    "16/3（全态/静默³·16？）": 16/3,
    "5（静默）": 5,
    "5·16/15（静默×全态比）": 5*16/15,
    "3e/√(2/3)（N_gen×超越/√(2/3)）": 3*e/(2/3)**0.5,
    "e^2-2": e**2-2,
    "16/3·(1+σ/100)": 16/3*(1+sigma/100),
    "σ⁻¹/3（静默逆/生成）": (1/sigma)/3,
    "3e−σ³(1+α_v')−0.3": None,
    "16·ln16/15·2.5?": None,
}
alpha_v = 16/15 + (2/3)**0.5*(1+6*sigma**3)
I_e = 3*e - sigma**3*(1+alpha_v)
mains["I_e−2.8224?"] = I_e - 2.8223920247
mains["3e−2.8224?"] = 3*e - 2.8223920247
for name, v in mains.items():
    if v is None: continue
    d = abs(v-DeltaI)/DeltaI*100
    print(f"  {name} = {v:.8f}——差 {d:.3f}%")

print("\n=== ② ΔI 与 16/3 的差——修正项分解 ===")
x = 16/3 - DeltaI
print(f"16/3 − ΔI = {x:.8e}")
print(f"x/σ³ = {x/sigma**3:.4f}")
print(f"x/σ⁴ = {x/sigma**4:.4f}")
print(f"x/6σ³ = {x/(6*sigma**3):.4f}")
print(f"x/σ³(1+α_v) = {x/(sigma**3*(1+alpha_v)):.4f}")
print(f"x/e^{{-16}} = {x/e**(-16):.4f}")

print("\n=== ③ 修正候选扫描（x = 16/3 − ΔI = 1.734573e-3） ===")
cands = {
    "6σ³": 6*sigma**3,
    "6σ³(1−σ/2)": 6*sigma**3*(1-sigma/2),
    "6σ³(16/15)⁻¹": 6*sigma**3/(16/15),
    "2σ³(1+α_v)": 2*sigma**3*(1+alpha_v),
    "σ³(1+α_v)(1+σ/2)": sigma**3*(1+alpha_v)*(1+sigma/2),
    "σ³·6(1−σ/2)²": 6*sigma**3*(1-sigma/2)**2,
    "σ³·(16/3)⁻¹·29": 29*sigma**3/(16/3),
    "σ⁴·(2⁴+σ)": sigma**4*(16+sigma),
    "σ⁵·1317": sigma**5*1317,
    "ε_μ·0.107": None,
    "e^{−16}·15416": None,
}
results = []
for name, v in cands.items():
    if v is None: continue
    d = abs(v-x)/x*100
    results.append((d, name, v))
for d, name, v in sorted(results):
    print(f"  {name} = {v:.6e}——差 {d:.2f}%")

print("\n=== ④ 更广主项：ΔI 的连分数/代数身份 ===")
print(f"ΔI·15/16 = {DeltaI*15/16:.6f}（vs 5——差 {(DeltaI*15/16-5)/5*100:.3f}%）")
print(f"ΔI·3/16 = {DeltaI*3/16:.6f}（vs 1——差 {(DeltaI*3/16-1)*100:.3f}%）")
print(f"ΔI·15 = {DeltaI*15:.4f}（vs 80——差 {(DeltaI*15-80)/80*100:.3f}%）")
print(f"ΔI/e = {DeltaI/e:.5f}（≈1.9615?）")
print(f"ΔI·(15/16)⁻¹ = {DeltaI*16/15:.6f}")
print(f"ΔI/ln16 = {DeltaI/log(16):.5f}")
