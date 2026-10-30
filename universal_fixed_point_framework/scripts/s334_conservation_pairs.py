# -*- coding: utf-8 -*-
"""S334 δ* 唯一守恒配对检验
δ* = 6σ³+4σ⁵+8σ⁷+5σ⁸——4 项两两配对共 3 种——检验'幂和=系数和'唯一性
守恒值：11（显态数 16-5）与 12（24/2=4!/2）
"""
import itertools

print("=== S334 δ* 唯一守恒配对 ===\n")

SIGMA = 1/15
terms = [(6,3),(4,5),(8,7),(5,8)]  # (系数, 幂次)
print(f"[1] 全部 3 种配对方式（4 项两两分组）")
seen = set()
for pair1 in itertools.combinations(terms, 2):
    rest = [t for t in terms if t not in pair1]
    pair2 = tuple(rest)
    key = frozenset([frozenset(pair1), frozenset(pair2)])
    if key in seen:
        continue
    seen.add(key)
    pairs = [pair1, pair2]
    sums = [(a[1]+b[1], a[0]+b[0]) for a,b in pairs]  # (幂和, 系数和)
    conserve = all(pw==cf for pw,cf in sums)
    mark = "★ 守恒！" if conserve else ""
    print(f"    ({pair1[0][0]}σ^{pair1[0][1]} {pair1[1][0]}σ^{pair1[1][1]}) | "
          f"({pair2[0][0]}σ^{pair2[0][1]} {pair2[1][0]}σ^{pair2[1][1]})——"
          f"幂和/系数和 {sums[0][0]}/{sums[0][1]} {sums[1][0]}/{sums[1][1]} {mark}")

print(f"\n[2] 唯一守恒配对确认")
print(f"    (6σ³, 5σ⁸) 与 (4σ⁵, 8σ⁷)：")
print(f"      对1：幂和 3+8=11——系数和 6+5=11——守恒 11")
print(f"      对2：幂和 5+7=12——系数和 4+8=12——守恒 12")
print(f"    3 种配对中唯一守恒——非偶然（其他配对全不守恒）")

print(f"\n[3] 守恒值身份")
print(f"    11 = 显态数 = 全态 16 − 静默 5（S 系列——显态/全态结构）")
print(f"    12 = 24/2 = 4!/2（半阶乘——幂基阶乘的一半）")
print(f"    11 与 12 均为框架量（显态数、半阶乘）——非任意数")

print(f"\n[4] 结构解读")
print(f"    对1：活跃(3)→2·活跃(6) 与 k_max(8)→静默(5)——显态守恒 11")
print(f"       ——'活跃的翻倍'配'k_max→静默'——和=显态数")
print(f"    对2：静默(5)→不动点(4) 与 对合(7)→k_max(8)——半阶乘守恒 12")
print(f"       ——'静默→不动点'(−1) 与 '对合→k_max'(+1)——±1 镜像对（S321）")
print(f"    ——配对结构：一个'翻倍对' + 一个'镜像对'——")
print(f"      翻倍对守恒 11、镜像对守恒 12")

print(f"\n[5] 先验化评估")
print(f"    ★ 唯一守恒配对是强筛选：4 项两两配对的 3 种方式中唯一满足")
print(f"      '幂和=系数和'——若'守恒律'有机制基础（显态守恒/半阶乘守恒）——")
print(f"      系数配对从'任意框架常数'降为'守恒唯一解'——先验性提升")
print(f"    诚实边界：")
print(f"      ① 仍为观察级结构——守恒律来源未解释（为何守恒于 11 和 12？）——")
print(f"        升格需机制论证（显态数/半阶乘为何是守恒值）")
print(f"      ② 配对操作不统一（翻倍 vs ±1 镜像）——需统一机制")
print(f"      ③ S321 已登记 ±1 镜像对（5→4、7→8）——本发现为其上叠加")
print(f"        '唯一守恒配对'整体结构——增量：配对唯一性 + 守恒值身份")

print(f"\n[6] 结论")
print(f"    ✓ δ* 唯一守恒配对成立：(6σ³,5σ⁸)守恒 11=显态数、(4σ⁵,8σ⁷)守恒 12=24/2")
print(f"    ✓ 3 种配对唯一守恒——非偶然")
print(f"    △ 观察级结构——登记为'守恒配对'候选机制——待机制论证")
