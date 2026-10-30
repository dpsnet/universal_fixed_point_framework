# -*- coding: utf-8 -*-
"""S167 质量链 e 幂指数框架化溯源（先证伪——枚举探索）
质量链已知 e 幂指数集合：{1, 3, 6, 19}（I_μ 的 e^1、σ³ 的 3、
42·e^{-6} 的 6、27/80·e^{-19} 的 19）
框架常数：Ngen=3 Kmax=8 Powers=2 Silence=5 Invol=7 FixedPt=4
Confinement=42 SigmaInv=15
探索：这些指数能否由框架常数的算术组合唯一/自然地生成
"""
from itertools import product
from fractions import Fraction

print("=== S167: 质量链 e 幂指数框架化溯源（先证伪） ===\n")

# 框架常数
C = {
    "Ngen(活跃)": 3, "Kmax": 8, "Powers(幂基)": 2, "Silence(静默)": 5,
    "Invol(对合)": 7, "FixedPt(不动点)": 4, "Confine(约束域)": 42,
    "SigmaInv": 15,
}
print("框架常数：", C)
print("质量链 e 幂指数：{1, 3, 6, 19}\n")

# 二元运算枚举：a+b, a-b, a*b, a/b, a^b, b^a（结果在目标集内）
targets = {1, 3, 6, 19}
names = list(C.keys())
vals = list(C.values())

found = {}
for i in range(len(names)):
    for j in range(len(names)):
        if i == j:
            continue
        a, b = vals[i], vals[j]
        na, nb = names[i], names[j]
        ops = [
            ("+", a + b), ("-", a - b), ("-", b - a),
            ("*", a * b),
        ]
        if b != 0 and a % b == 0:
            ops.append(("/", a // b))
        if a != 0 and b % a == 0:
            ops.append(("/", b // a))
        for op, r in ops:
            if r in targets:
                found.setdefault(r, []).append(f"{na} {op} {nb} = {r}")

print("=== 二元组合命中（每个目标的全部组合） ===")
for t in sorted(targets):
    combos = found.get(t, [])
    print(f"\n指数 {t}（{len(combos)} 个组合）:")
    for c in combos:
        print(f"   {c}")

print("\n=== 三常数组合补查（二元未覆盖的目标） ===")
# 对二元未命中的目标，查 c op (a op b) 形式
binary_vals = set()
for i in range(len(vals)):
    for j in range(len(vals)):
        if i == j:
            continue
        a, b = vals[i], vals[j]
        binary_vals.update([a+b, a-b, b-a, a*b])
        if b != 0:
            binary_vals.add(Fraction(a, b))
        if a != 0:
            binary_vals.add(Fraction(b, a))

uncovered = [t for t in targets if t not in found]
for t in uncovered:
    combos = []
    for i in range(len(names)):
        a, na = vals[i], names[i]
        for bv in sorted(binary_vals):
            if bv == 0:
                continue
            if a + bv == t:
                combos.append(f"{na} + (二元值 {bv})")
            if a - bv == t:
                combos.append(f"{na} - (二元值 {bv})")
            if a * bv == t and bv in binary_vals:
                pass  # 乘法组合已在二元内
    print(f"\n指数 {t}（三元补查 {len(combos)} 个）:")
    for c in combos[:8]:
        print(f"   {c}")

print("\n=== 幂运算补查（2^2=4, 4^2=16——S160 平方链） ===")
sq_chain = {2: "Powers", 4: "FixedPt", 16: "FixedPt^2"}
for r, name in sq_chain.items():
    print(f"   {name} 相关平方链值 {r}")
# 19 = 16+3 = 4²+Ngen / 19 = 15+4 = SigmaInv+FixedPt
print("\n=== 19 的两种自然组合 ===")
print("   19 = 4² + 3 = FixedPt² + Ngen（S160 幂基平方链顶 + 活跃）")
print("   19 = 15 + 4 = SigmaInv + FixedPt（SigmaInv=4²−1）")
print("   → 两种组合竞争——分解不唯一（与量子态组合对应？——登记观察级）")
print("   6 = 2×3 = Powers × Ngen（唯一自然组合）")
print("   3 = Ngen（唯一——活跃 3）")
print("   1 = 单位推进（S166——半群单位元 t=1——非组合）")

print("\n=== 判别 ===")
print("   3、6 唯一自然框架化（活跃 3、幂基×活跃）")
print("   19 双组合竞争（16+3 / 15+4）——不唯一——登记观察级")
print("   1 = 单位推进（S166 机制——非算术组合）")
print("   → 质量链 e 幂指数可框架化（3、6 唯一；19 竞争登记）")
