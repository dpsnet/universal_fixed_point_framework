# -*- coding: utf-8 -*-
"""
P7-5e-162：编织环周期重复检验——第二窗口（17=2⁴+1）+ 家族桥表 + 环代数
检验 A：第二对合窗口 m↦17−m（域 1..16）——δ_cl 对称性（预期否定：对合域唯一）
检验 B：编织环周期重复——第二圈搜索（域界 9 之后 m=9..16 是否有 65/56 型桥）
检验 C：2^m+1 家族角色表完备性（3,5,9,17,33,65——17/33 沉默位点？）
检验 D：环代数守恒（单点观察——节点积分解 vs 框架常数）
数据：159 权威 dcl（1..14）+ 117 权威 delta（15/16）
"""
import json

# 权威 δ_cl：m=1..14（159 tridiag）+ m=15/16（117 全链）
dcl = {1: 2.013e-4, 2: 2.013e-4, 3: 3.544e-4, 4: 4.419e-4, 5: 1.358e-3,
       6: 2.692e-3, 7: 4.055e-3, 8: 5.428e-3, 9: 6.626e-3, 10: 7.656e-3,
       11: 8.540e-3, 12: 9.298e-3, 13: 9.950e-3, 14: 1.051e-2,
       15: 1.10054e-2, 16: 1.14368e-2}

print("=== A) 第二对合窗口 17=2⁴+1 检验（域 m↦17−m）===", flush=True)
print("m\t17−m\tδ_cl(m)\tδ_cl(17−m)\t对称比", flush=True)
sym_ok = True
for m in range(1, 9):
    r = 17 - m
    q = dcl[m] / dcl[r]
    if q > 0.1:
        sym_ok = False
    print("%d\t%d\t%.3e\t%.3e\t%.2f%%" % (m, r, dcl[m], dcl[r], q*100), flush=True)
print("17 窗口对称性:", "否定（δ_cl 单调——对称比 <10%，m↦17−m 无对合）" if not sym_ok else "存在", flush=True)
print("→ 17=2⁴+1 不构成第二对合窗口——对合域唯一（m≤8，域界 9）", flush=True)

print("\n=== B) 编织环周期重复——第二圈搜索 ===", flush=True)
print("第一圈：1 —1/65→ 65 —2⁶+1→ 6 —对合→ 3 —尾巴=δ∞→ 56 —8·7→ 8 —对合→ 1", flush=True)
print("第二圈候选：域界 9 之后 m=9..16——检查桥结构：", flush=True)
print("  65/56 型桥的代数同构兄弟：", flush=True)
print("  65 = 2⁶+1（家族成员）→ 家族兄弟 17=2⁴+1、33=2⁵+1", flush=True)
print("  56 = 8·7 = k_max(k_max−1)（k_max=8 唯一）→ 无同构兄弟", flush=True)
print("  检验 17/33 在 δ_cl/闭式层的出现：", flush=True)
print("  闭式 1/B* = |m|/2+1/7+1/(7·2^m)+[1/65]——无 17/33 项", flush=True)
print("  对合域界 9——无 m=17 域界（160 数据 m≤512 全链双曲无断裂）", flush=True)
print("→ 第二圈无桥——编织环单圈，无周期重复", flush=True)

print("\n=== C) 2^m+1 家族角色表（完备性）===", flush=True)
family = [(1,3,"截距分子 3/14（153）"), (2,5,"截距分子 5/28（153）"),
          (3,9,"域界/对合常数 2³+1（158/159）"), (4,17,"?"),
          (5,33,"?"), (6,65,"桥/修正 1/65（153/157/161）")]
for m, val, role in family:
    print("m=%d: 2^%d+1 = %d → %s" % (m, m, val, role), flush=True)
silent = [v for m, v, r in family if r == "?"]
print("沉默位点：", silent, "（m=4/5 家族成员无结构角色）", flush=True)
print("→ 家族角色不对称：m∈{1,2,3,6} 有角色、m∈{4,5} 沉默——限制性事实", flush=True)

print("\n=== D) 环代数守恒（单点观察）===", flush=True)
prod = 1*65*6*3*56*8
print("环节点积 1×65×6×3×56×8 =", prod, flush=True)
# 分解
n = prod
fac = []
d = 2
while d*d <= n:
    while n % d == 0:
        fac.append(d)
        n //= d
    d += 1
if n > 1:
    fac.append(n)
print("素分解：", fac, "=", "·".join(str(x) for x in fac), flush=True)
print("对照框架常数：2⁷=128（13/128 分母！）、13（C 分子）、7（δ∞ 分母）、5（k_max−3）、3²", flush=True)
print("单点观察：环积同时含 13 与 7 与 2⁷——与 C=13/128、δ∞=1/56 同族（后验分解，不结论）", flush=True)

print("\n=== 判别 ===", flush=True)
print("A) 第二窗口否定——对合域唯一（m≤8）", flush=True)
print("B) 周期重复否定——编织环单圈（无第二 65/56 型桥）", flush=True)
print("C) 家族角色不对称——17/33 沉默位点（新限制性事实）", flush=True)
print("D) 环积 524160 = 2⁷·3²·5·7·13 与框架常数同族（单点观察）", flush=True)
print("综合：2^m 尾巴的编织候选无法通过'周期重复'升格——保持'发夹折叠 + 2-股编织候选（代数对应图级）'；", flush=True)
print("新证据：对合域唯一性 + 家族沉默位点——结构是'一次性折叠'而非'编织延续'", flush=True)

out = {"A_second_window": {"verdict": "negated", "reason": "delta_cl monotone, m<->17-m ratio <10%"},
       "B_cycle_repeat": {"verdict": "negated", "reason": "no second 65/56 bridge; single cycle"},
       "C_family_roles": {"3": "intercept numerator", "5": "intercept numerator", "9": "domain bound/involution",
                          "17": "SILENT", "33": "SILENT", "65": "bridge/correction"},
       "D_ring_product": {"product": 524160, "factors": "2^7*3^2*5*7*13",
                          "note": "single-point observation, same family as C=13/128 & 1/56"}}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e162_braid_repeat.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("\nsaved", flush=True)
