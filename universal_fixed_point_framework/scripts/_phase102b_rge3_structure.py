# -*- coding: utf-8 -*-
"""
Phase 102b 阶段 2c-K：rge3 数值结构攻点（2026-10-10）
目标：ln(rge3) = −46.947974 的框架身份（达标线 0.01%）
候选方向：谱流↔RGE（Paper 11 A6/Paper 57）——'运行因子'的几何结构
"""
import math

print("="*78)
print("rge3 数值结构攻点：ln(rge3) 的框架分解")
print("="*78)

# ---- 精确基准 ----
rge3 = 4.0811e-21
ln_rge3 = math.log(rge3)
print(f"\n精确基准: ln(rge3) = ln(4.0811e−21) = {ln_rge3:.10f}")

# ---- 候选 1：4π²·2^{1/4}（新候选——手工侦察发现）----
c1 = 4*math.pi**2 * 2**0.25
print(f"\n候选 1: 4π²·∜2 = {c1:.10f}")
dev1 = abs(c1 - (-ln_rge3))/abs(ln_rge3)*100
print(f"    vs −ln(rge3) = {-ln_rge3:.10f}——偏差 {dev1:.6f}%")

# ---- 候选 2：系统搜索（框架常数代数组合）----
print(f"\n系统搜索：框架常数组合逼近 −ln(rge3) = {-ln_rge3:.10f}")
dlmin = (math.sqrt(3)-1)/6
dH = math.log(15) + 1/675
sigma = 1/15
kappa = 6/math.pi
alphaEM_inv = 24*(dH+3)
target = -ln_rge3  # 46.947974

# 基本常数库
base = {
    "π": math.pi, "2π": 2*math.pi, "π²": math.pi**2, "4π²": 4*math.pi**2,
    "e": math.e, "e²": math.e**2, "√2": math.sqrt(2), "∜2": 2**0.25, "√3": math.sqrt(3),
    "Δλ_min": dlmin, "Δλ₃": math.sqrt(2)*dlmin, "d_H": dH, "σ": sigma, "κ": kappa,
    "1/α_EM": alphaEM_inv, "N_c": 3.0, "C_F": 4/3, "b₀": 9.0, "B₀": 9/4,
    "16": 16.0, "24": 24.0, "15": 15.0, "137": 137.0, "ln15": math.log(15),
}
# 生成候选：c·(a±b) 型 + a·b 型
results = []
keys = list(base.keys())
for i in range(len(keys)):
    for j in range(i, len(keys)):
        a, b = base[keys[i]], base[keys[j]]
        for expr, val in [
            (f"{keys[i]}·{keys[j]}", a*b),
            (f"{keys[i]}/{keys[j]}", a/b),
            (f"{keys[i]}+{keys[j]}", a+b),
            (f"{keys[i]}−{keys[j]}", a-b),
        ]:
            if val <= 0: continue
            dev = abs(val-target)/target*100
            if dev < 0.05:
                results.append((dev, expr, val))
results.sort()
print(f"   （0.05% 内命中 {len(results)} 个——Top 15:）")
for dev, expr, val in results[:15]:
    print(f"   {dev:8.5f}%  {expr} = {val:.8f}")

# ---- 候选 3：16·x 型（x = 3−σ−ε）----
print(f"\n候选 3: 16·x 型（x = 2.934245）")
x = target/16
print(f"   x = {x:.8f}——3−σ = {3-sigma:.8f}——差 ε = {x-(3-sigma):.8f}")
print(f"   ε = {x-3+sigma:.8f}——ε/δ = {(x-3+sigma)/(1/675):.4f}（δ=1/675）")

# ---- 候选 4：2π²·x 型（x = 2.378441）----
print(f"\n候选 4: 2π²·x 型（x = 2.378441）")
x4 = target/(2*math.pi**2)
print(f"   x = {x4:.8f}——d_H−1/3 = {dH-1/3:.8f}——差 {x4-(dH-1/3):.6f}")
print(f"   2^¼·2 = {2**0.25*2:.8f}——∜2·2 = 2^{{1.25}} = {2**1.25:.8f}")
print(f"   x/∜2 = {x4/2**0.25:.8f}")

print(f"\n候选 5: 4π²·x 型（x = 1.189215）——x 是否 = ∜2？")
x5 = target/(4*math.pi**2)
print(f"   x = {x5:.10f}——∜2 = {2**0.25:.10f}——差 {x5-2**0.25:.2e}——相对 {abs(x5-2**0.25)/2**0.25*100:.6f}%")
