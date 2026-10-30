# -*- coding: utf-8 -*-
"""π 连分数后续部分商框架量扫描（2026-10-26 用户推进 ①）

292 之后的部分商框架身份识别——高精度连分数展开。
"""
try:
    import mpmath as mp
    mp.mp.dps = 120
    pi = mp.pi
    print("mpmath 高精度 π 可用")
except Exception as e:
    print("mpmath 不可用，用 Decimal")
    from decimal import Decimal, getcontext
    getcontext().prec = 120
    pi = Decimal(3).atan().scaleb(2)  # 4*atan(1) 太复杂——用常数
    pi = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196")

# 连分数展开
parts = []
x = pi
for _ in range(60):
    a = int(x)
    parts.append(a)
    x = 1 / (x - a)

print(f"π 连分数前 {len(parts)} 项：")
print(parts)

# 框架量识别
fw = {
    3: "活跃", 7: "对合域", 15: "σ⁻¹", 5: "静默", 2: "幂基",
    8: "k_max", 4: "不动点", 1: "单位", 11: "显态=对合域+不动点",
    16: "全态", 42: "覆盖域",
}
fw_combos = {
    6: "双向量数/活跃×幂基", 9: "活跃²", 12: "N_gen×不动点",
    14: "幂基×对合域", 13: "全态−活跃", 21: "N_gen×对合域",
    25: "静默²", 28: "不动点×对合域", 35: "静默×对合域",
    64: "k_max²", 84: "幂基×覆盖域", 99: "活跃²×显态",
    24: "静默×幂基×.../3!", 10: "静默×幂基", 20: "静默×不动点",
    30: "N_gen×幂基×静默", 40: "k_max×静默", 48: "全态×活跃",
    45: "静默×活跃²", 56: "对合域×k_max", 63: "对合域×9",
    72: "k_max×活跃²", 73: "k_max²+活跃²", 5*7*3: "静默×对合域×活跃",
}

print("\n=== 框架量识别 ===")
hits = []
for i, p in enumerate(parts):
    if p in fw:
        hits.append((i, p, fw[p]))
    elif p in fw_combos:
        hits.append((i, p, fw_combos[p]))
for i, p, label in hits:
    print(f"位置 {i:2d}: {p:3d} = {label}")

print(f"\n=== 统计 ===")
print(f"总项数: {len(parts)}")
print(f"框架量命中: {len(hits)} 项")
# 排除太普遍的 1 和 2
special = [(i,p,l) for i,p,l in hits if p not in (1,2)]
print(f"排除 1/2 后命中: {len(special)} 项")
for i, p, label in special:
    print(f"  位置 {i:2d}: {p:3d} = {label}")
