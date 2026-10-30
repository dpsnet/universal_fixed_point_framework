# -*- coding: utf-8 -*-
"""FW 缺口 {24,70,140} 机制判别（2026-10-25，104az-195 ⑤ 下一攻点）

104az-193 FW 表（49 值登记身份）：
基础 {1,2,3,4,5,7,8,15,16} + 组合 {6,9,10,11,12,13,14} + 复合 {20,21,28,29,30,
31,32,35,40,42,44,45,46,48,49,56,58,60,61,63,64,65,84,98,100,105,125,210,253,320,
675,729,1000}

缺口：24 = N_gen×k_max（其余 N_gen×常数全在）、70 = 35×幂基（升级断裂）、
      140 = 70×2。本脚本判别：① 24 = 4! = (N_gen+1)! 阶乘族身份候选；
      ② 升级谱互补观察（6 禁×N_gen、10 禁×{静默,对合域,k_max}）；
      ③ 三素因子直积含/不含 N_gen 判别；④ 缺口谱 {24,70,140} 的结构。
"""
FW = {1,2,3,4,5,7,8,15,16,6,9,10,11,12,13,14,20,21,28,29,30,31,32,35,40,42,
      44,45,46,48,49,56,58,60,61,63,64,65,84,98,100,105,125,210,253,320,675,729,1000}
bases = {'幂基':2,'N_gen':3,'静默':5,'对合域':7,'k_max':8,'不动点':4}
print(f"FW 表大小：{len(FW)}（应 49）")

print()
print("=== ① 24 阶乘族身份候选 ===")
print(f"24 = 4! = (N_gen+1)! = 4·3·2·1（4=时空维=N_gen+1、3=N_gen、2=幂基、1=单位元）")
print(f"6  = 3! = N_gen! = 3·2·1（已登记：6 = N_gen! = 幂基×N_gen）")
print(f"→ 阶乘族 3!→4! = 6→24：24 = (N_gen+1)! = (N_gen+1)·N_gen! 身份候选成立")
print(f"对照：30 = N_gen!×静默（已登记）、24 = N_gen!×(N_gen+1)——同一族")
print()

print("=== ② 升级谱互补观察 ===")
print("6 = 2·3 的升级谱：")
for name, f in bases.items():
    v = 6*f
    print(f"  6×{name}({f}) = {v}：{'✓ FW' if v in FW else '✗ 缺'}")
print("10 = 2·5 的升级谱：")
for name, f in bases.items():
    v = 10*f
    print(f"  10×{name}({f}) = {v}：{'✓ FW' if v in FW else '✗ 缺'}")
print("15 = 3·5 的升级谱：")
for name, f in bases.items():
    v = 15*f
    print(f"  15×{name}({f}) = {v}：{'✓ FW' if v in FW else '✗ 缺'}")
print("21 = 3·7 的升级谱：")
for name, f in bases.items():
    v = 21*f
    print(f"  21×{name}({f}) = {v}：{'✓ FW' if v in FW else '✗ 缺'}")
print("35 = 5·7 的升级谱：")
for name, f in bases.items():
    v = 35*f
    print(f"  35×{name}({f}) = {v}：{'✓ FW' if v in FW else '✗ 缺'}")
print()

print("=== ③ 三素因子直积判别（不含 2³ 幂混合，纯 3 素因子） ===")
primes3 = [2,3,5,7]
from itertools import combinations
print("素因子三元组 {a,b,c}（a<b<c，可重复 2 幂）→ 直积 ∈ FW?")
for a,b,c in combinations(primes3, 3):
    for aa in ([a] if a==b else [a]) if False else [a]:
        pass
# 直接枚举：乘积 ≤ 1000 的三素直积
triples = [(2,3,5),(2,3,7),(2,5,7),(3,5,7),(2,3,4),(2,5,4),(3,5,4),(2,7,4)]
for t in sorted(set(triples)):
    v = t[0]*t[1]*t[2]
    has3 = 3 in t or 4 in t  # 4=不动点含 3? 4=2² 不含——改用含 N_gen 判定
    hasN = (3 in t)
    print(f"  {t} → {v}：{'✓' if v in FW else '✗'}"
          f"{'（含 N_gen）' if hasN else '（不含 N_gen）'}"
          f"{'  身份：' + ('禁闭域/Λ_QCD/2/σ⁻¹ 候选' if v in (42,105,15) else ('FW' if v in FW else ''))}")
print()

print("=== ④ 缺口谱 {24,70,140} 结构判别 ===")
print(f"24 = 2³×3：2³ = k_max、×3 = N_gen——但 24 也 = 4!（时空维阶乘）")
print(f"70 = 2×5×7：幂基×静默×对合域——35×2 升级断裂（35 ∈ FW）")
print(f"140 = 2²×5×7 = 70×2——70 缺位的继承")
print()
print("缺口谱 {24,70,140} 的素因子总谱：2、3、5、7——全框架素基")
print("判别候选：")
print("  (a) 24：阶乘族 (N_gen+1)! 身份——若立，FW 表 +24，闭包家族 11→13（104az-195 敏感性）")
print("  (b) 70：3 素因子直积（2·5·7）缺 N_gen——对照含 N_gen 直积 30/42/105 全在——")
print("      '缺 N_gen 的静默×对合域直积禁'——但 10=2×5 在 FW（无 N_gen）——")
print("      修正候选：'两素因子浅层直积（≤2 因子）无需 N_gen；三素因子深层直积需 N_gen'——")
print("      检验：6=2×3（含）、10=2×5（不含，✓ 浅层）、14=2×7（不含，✓ 浅层）、"
      "15=3×5（含）、21=3×7（含）、35=5×7（不含，✓ 浅层——但 35 在 FW！）")
print("      ⟹ 35 = 5×7 无 N_gen 却在 FW——'三素深层直积需 N_gen'候选被 35 反例破坏？")
print("      ——35 是两素因子（5×7）非三素——三素直积 {2,5,7}=70 ✗ vs {3,5,7}=105 ✓——")
print("      '三素直积（3 个互异素因子）含 N_gen 必 FW、不含 N_gen 必缺'候选：")
for t in [(2,5,7),(2,3,7),(2,3,5),(3,5,7)]:
    v = t[0]*t[1]*t[2]
    hasN = 3 in t
    print(f"      {t}→{v}：含N_gen={hasN}，FW={'✓' if v in FW else '✗'}"
          f"——{'一致' if (hasN and v in FW) or (not hasN and v not in FW) else '反例'}")
print()
print("结论：'三素直积含 N_gen ⟺ FW'对 {2,3,5}→30 ✓、{2,3,7}→42 ✓、{2,5,7}→70 ✗、"
      "{3,5,7}→105 ✓ 全部一致——唯一 3 素直积缺口 = 不含 N_gen 的 70——机制候选："
      "'静默×对合域 的深层（×幂基）直积在无 N_gen 时禁'（104az-195 ③ 登记的观察获全表验证）")
