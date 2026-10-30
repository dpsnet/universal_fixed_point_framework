# -*- coding: utf-8 -*-
"""闭包家族敏感性重算（2026-10-25）：FW 表 +24（4! 阶乘族身份）后 11→13？

104az-194/195：FW 49 值口径下无单位 3 元闭包 = 11、4 元闭包 = 11（{1}∪无单位3元）
104az-195 敏感性：若 24 获身份 → (2,3,8)/(2,4,6) 过约束 → 无单位闭包 +2 → 4 元闭包 13
本脚本：FW∪{24}（50 值）口径精确重算闭包家族。
"""
from itertools import combinations

FW = {1,2,3,4,5,7,8,15,16,6,9,10,11,12,13,14,20,21,28,29,30,31,32,35,40,42,
      44,45,46,48,49,56,58,60,61,63,64,65,84,98,100,105,125,210,253,320,675,729,1000}
FW24 = FW | {24}

def closed3(F, a, b, c):
    """无单位 3 元闭包三约束（104az-194 结构定理 A）"""
    if not (2 <= a < b < c <= 16):
        return False
    # ① 素因子 ⊆ {2,3,5,7}
    for x in (a, b, c):
        v = x
        for p in (2,3,5,7):
            while v % p == 0:
                v //= p
        if v != 1:
            return False
    # ② 全和 ≤ 15
    if a+b+c > 15:
        return False
    # ③ 两两积/三积 ∈ FW
    return (a*b in F) and (a*c in F) and (b*c in F) and (a*b*c in F)

def closed4(F, a, b, c, d):
    """4 元闭包：所有非空子集和 ∈ FW_SUM ∧ 积 ∈ FW（104az-193）"""
    elems = [a,b,c,d]
    if not (1 <= a < b < c < d <= 16):
        return False
    # 积 ∈ FW（包含子集积）
    for r in range(1, 5):
        for sub in combinations(elems, r):
            prod = 1
            for x in sub:
                prod *= x
            if prod not in F:
                return False
    # 和 ∈ FW_SUM（FW ∪ 组合恒等 6..14）
    FW_SUM = F | {6,9,10,11,12,13,14} | set(range(1,17))
    for r in range(1, 5):
        for sub in combinations(elems, r):
            if sum(sub) not in FW_SUM:
                return False
    return True

def count(F, label):
    c3 = [(a,b,c) for a,b,c in combinations(range(2,17), 3) if closed3(F, a, b, c)]
    c4 = [(a,b,c,d) for a,b,c,d in combinations(range(1,17), 4) if closed4(F, a, b, c, d)]
    print(f"=== {label}（FW 表 {len(F)} 值） ===")
    print(f"无单位 3 元闭包：{len(c3)} 个")
    for t in c3:
        print(f"  {t}（积 {t[0]*t[1]*t[2]}）")
    print(f"4 元闭包：{len(c4)} 个")
    for t in c4:
        print(f"  {t}（全积 {t[0]*t[1]*t[2]*t[3]}）")
    print()
    return c3, c4

c3_49, c4_49 = count(FW, "原口径 FW-49")
c3_50, c4_50 = count(FW24, "新口径 FW-50（+24）")

print("=== 敏感性对比 ===")
new3 = set(c3_50) - set(c3_49)
print(f"新增无单位 3 元闭包：{len(new3)} 个 {new3}")
new4 = set(c4_50) - set(c4_49)
print(f"新增 4 元闭包：{len(new4)} 个 {new4}")
print(f"预期（104az-195）：无单位 +2、4 元 +2 → 11→13 / 11→13")
print(f"实测：{len(c3_49)}→{len(c3_50)}（+{len(c3_50)-len(c3_49)}）、"
      f"{len(c4_49)}→{len(c4_50)}（+{len(c4_50)-len(c4_49)}）")

print()
print("=== 补充：24 自身的 3 元闭包地位 ===")
print(f"(2,3,4)→24：closed3 = {closed3(FW24, 2, 3, 4)}（24 作为三积，两两积 6/8/12 全在）")
print(f"——24 是闭包积而非闭包成员（4 元闭包 (1,2,3,4) 的全积 24 需要 24 ∈ FW）")
print(f"4 元闭包含 24 全积者：{[t for t in c4_50 if t[0]*t[1]*t[2]*t[3]==24]}")
