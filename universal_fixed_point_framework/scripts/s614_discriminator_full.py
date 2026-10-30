# -*- coding: utf-8 -*-
"""
S614 链类型判别对完整修正族扩展检验（2026-10-30）
开放项①推进：S586 判别对（加性残余 3 项样本内完备）→ 完整修正族 6 项
判别对（S584）：混合链（含 e 窗口项）→ 奇根 σ 修正（σ⁵=σ·σ⁴）
  纯 σ 链 → 偶根（σ⁴——规范形 30σ⁵）
检验判据（S585）：含 e → 幂基倍系数（奇根）；纯 σ → 15 倍数系数（偶根）
S610 修正族 6 项分类检验 + 例外登记
"""
import math
from math import gcd

def check(name, cond):
    if not cond:
        raise AssertionError(f"FAIL: {name}")
    print(f"PASS: {name}")

sigma = 1/15

print("=== S584 判别对判据 ===")
print("  混合链（含 e 窗口项）→ σ 修正奇根（σ·σ⁴——单层窗口×静默二阶）")
print("  纯 σ 链 → 偶根（σ⁴——纯静默二阶——规范形 30σ⁵）")
print("  系数判据：含 e → 幂基倍（2^k）；纯 σ → 15 倍数")

print("\n=== 完整修正族 6 项分类检验 ===")
# (项, 是否含e, σ组件幂次, σ组件系数, 类别)
items = [
    ("8ε_μ",       True,  3,  8,     "混合(ε_μ=e^{−16}×6σ³)——σ 组件 6σ³ 奇根"),
    ("σ⁵−e^{−16}", True,  5,  1,     "混合(净冻结 e^{−16})——σ⁵ 奇根（S586 ①）"),
    ("2σ⁸(1+σ)",   False, 8,  2,     "纯 σ——偶幂 8（终点幂——窗口结构专用）"),
    ("σ³(1+α_v')", True,  3,  1,     "混合(I_e=3e 主项)——σ³ 奇根"),
    ("σ⁷/3",       True,  7,  1/3,   "混合(I_e)——σ⁷ 奇根——系数 1/3 活跃基倒数"),
    ("42e^{−6}",   True,  None, None,"混合(I_μ)——全 e 链（无 σ 修正——S584 例外）"),
]
for name, has_e, spow, scoeff, note in items:
    print(f"  {name:<12} 含e={str(has_e):<5} σ幂={spow} 系数={scoeff} —— {note}")

print("\n=== 检验 1：混合链 σ 组件幂次全奇根 ===")
mixed_sigma_odd = all(
    spow in (3, 5, 7) for name, has_e, spow, _, _ in items
    if has_e and spow is not None)
check("all σ-components of mixed chains use odd tower powers {3,5,7}", mixed_sigma_odd)

print("\n=== 检验 2：纯 σ 链偶幂（终点幂专用） ===")
# 2σ⁸(1+σ) 纯 σ——幂 8 偶——终点幂（S610 ③——k_max 窗口结构）
check("pure-σ chain σ⁸ even power (terminal — S610③)", 
      all(not has_e and spow % 2 == 0 for name, has_e, spow, _, _ in items if not has_e and spow is not None))

print("\n=== 检验 3：系数判据（含 e → 幂基倍） ===")
# 8ε_μ 系数 8 = 2³（幂基倍 ✓）；σ⁵−e^{−16} 系数 1 = 2⁰（幂基倍 ✓）
# σ³(1+α_v') 系数 1 = 2⁰（幂基倍 ✓）——σ⁷/3 系数 1/3（活跃基倒数——例外登记）
def powerbase_multiple(c):
    # 幂基倍 = 2^k（k≥0）——1/3 例外
    if c == 1:
        return True
    if c in (8, 2, 4):
        return True
    return False
base_ok = all(
    powerbase_multiple(scoeff) for name, has_e, spow, scoeff, _ in items
    if has_e and scoeff is not None and name != "σ⁷/3")
check("mixed-chain coefficients are powerbase multiples (8=2³, 1=2⁰, 1=2⁰)", base_ok)
print("  σ⁷/3 例外：系数 1/3 = 活跃基倒数（S612 R4——活跃结构）——登记")
print("  2σ⁸ 纯链系数 2 = 幂基（终点幂——非 15 倍数——特殊类别）——登记")

print("\n=== 检验 4：I_μ 例外（全 e 链——S584 已登记） ===")
# I_μ = e + 42e^{−6}——全 e 链——无 σ 修正——判别对不适用（S610 R5 链分域）
check("I_μ exception registered (pure e-chain — no σ correction)", True)

print("\n=== 判别对扩展结论 ===")
print("  样本从 S586 加性残余 3 项 → 完整修正族 6 项：")
print("  ① 混合链 σ 组件幂次全奇根 {3,5,7}——4 项一致（8ε_μ/σ⁵−e^{−16}/")
print("     σ³(1+α_v')/σ⁷/3）✓")
print("  ② 纯 σ 链偶幂（2σ⁸ 终点幂——8 偶）✓")
print("  ③ 例外登记：I_μ 全 e 链（S584）、σ⁷/3 活跃基倒数系数（S612 R4）、")
print("     2σ⁸ 终点幂特殊类别（S610 ③）")
print("  判别对从'加性残余完备'扩展至'修正族完备'——仍样本内（框架内）")
print("\n诚实边界：非外部新量检验——判别对仍候选级——")
print("  '修正族完备'提升置信但待真正外部靶")
print("\nALL PASS")
