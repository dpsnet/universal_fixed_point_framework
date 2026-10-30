# -*- coding: utf-8 -*-
"""11 四重框架身份 + 静默域对称分裂判别（2026-10-26）

用户三式：11 = 2³+3 = 5×3−4 = 3²+2（k_max+活跃 / σ⁻¹−不动点 / 活跃²+幂基）
已知：11 = 对合域+不动点（7+4）
结合 29 = 静默²+不动点——对称分裂候选：
  11 = σ⁻¹−不动点、29 = 静默²+不动点——围绕不动点 4 的对称对
"""
import math

n_gen, silence, powers, involution, fixed = 3, 5, 2, 7, 4
kmax = powers**n_gen
active = n_gen
sigma_inv = active*silence

print("=== 用户三式验证 ===")
print(f"① 11 = 2³+3 = k_max+活跃 = {kmax}+{active} = {kmax+active} ✓")
print(f"② 11 = 5×3−4 = 静默×活跃−不动点 = {silence}×{active}−{fixed} = {silence*active-fixed} ✓")
print(f"③ 11 = 3²+2 = 活跃²+幂基 = {active}²+{powers} = {active**2+powers} ✓")
print(f"④ 11 = 对合域+不动点 = {involution}+{fixed} = {involution+fixed} ✓（已知）")

print("\n=== 四重身份的等价谱 ===")
print(f"11 = 2×活跃+静默（展开①：k_max = 活跃+静默）")
print(f"11 = 活跃×静默−不动点（②——σ⁻¹−不动点）")
print(f"11 = 活跃²+幂基（③）")
print(f"11 = 活跃+2×不动点（展开④：对合域 = 活跃+不动点）")
print(f"→ 11 的框架分解多重冗余（四重身份）——代数出现密度高")

print("\n=== ★★ 静默域围绕不动点的对称分裂 ===")
eleven = sigma_inv - fixed
twenty9 = silence**2 + fixed
print(f"11 = σ⁻¹−不动点 = {sigma_inv}−{fixed} = {eleven} ✓（用户式②）")
print(f"29 = 静默²+不动点 = {silence}²+{fixed} = {twenty9} ✓（已知）")
print(f"——11 与 29 = 静默域（σ⁻¹、静默²）围绕不动点 4 的对称分裂")
print(f"和：11+29 = σ⁻¹+静默² = {eleven+twenty9} = 静默×k_max = {silence*kmax} ✓")
print(f"差：29−11 = 静默²−σ⁻¹+2×不动点 = {twenty9-eleven} = 幂基×活跃² = {powers*active**2} ✓")

print("\n=== 对称分裂的框架结构 ===")
print(f"σ⁻¹ = 活跃×静默（韦达积）——静默² = 纯静默平方——两者 = 静默域的两种形态")
print(f"分裂点 = 不动点 4——σ⁻¹ 减、静默² 加——围绕不动点的对称偏移")
print(f"和守恒 = 静默×k_max（40）——差 = 幂基×活跃²（18）——皆框架量")
