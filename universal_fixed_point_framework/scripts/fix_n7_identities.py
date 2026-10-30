# -*- coding: utf-8 -*-
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n7_identities.py"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

old = """IDENTITIES = [
    ("s1_2 = s2_34567", (0,), (1, 2, 3, 4, 5, 6), [(1,), (2, 3, 4, 5, 6)]),
    ("s1_23 = s23_4567", (0, 1, 2), (3, 4, 5, 6), [(1, 2), (3, 4, 5, 6)]),
    ("s1_234 = s234_567", (0, 1, 2, 3), (4, 5, 6), [(1, 2, 3), (4, 5, 6)]),
    ("s1_2345 = s2345_67", (0, 1, 2, 3, 4), (5, 6), [(1, 2, 3, 4), (5, 6)]),
    ("s1_23456 = s23456_7", (0, 1, 2, 3, 4, 5), (6,), [(1, 2, 3, 4, 5), (6,)]),
    ("s1_234567 = 0", (0, 1, 2, 3, 4, 5, 6), (), []),
]"""

new = """IDENTITIES = [
    # (名字, [λ1+λ_A], [λ_A], [λ_B])：恒等式 [λ1, λ_A] = [λ_A, λ_B]（λ1+λ_A+λ_B=0）
    ("s1_2 = s2_34567", (0,), (1,), (2, 3, 4, 5, 6)),
    ("s1_23 = s23_4567", (0,), (1, 2), (3, 4, 5, 6)),
    ("s1_234 = s234_567", (0,), (1, 2, 3), (4, 5, 6)),
    ("s1_2345 = s2345_67", (0,), (1, 2, 3, 4), (5, 6)),
    ("s1_23456 = s23456_7", (0,), (1, 2, 3, 4, 5), (6,)),
    ("s1_234567 = 0", (0,), (1, 2, 3, 4, 5, 6), ()),
]"""

assert old in s, "old not found"
s = s.replace(old, new)

# 修 run() 中的 lhs/rhs 计算逻辑
old_run = """        for name, A1, Bfull, AB in IDENTITIES:
            tot[name] += 1
            lhs = bracket(omega, zbar, A1, Bfull)  # [λ1+Σ_A, λ_B]
            if not AB:
                rhs = 0.0
            else:
                rhs = bracket(omega, zbar, AB[0], AB[1])
            if abs(lhs - rhs) > 1e-8:
                viol[name] += 1"""
new_run = """        for name, A1, AA, BB in IDENTITIES:
            tot[name] += 1
            lhs = bracket(omega, zbar, A1, AA)  # [λ1, λ_A]
            if not BB:
                rhs = 0.0
            else:
                rhs = bracket(omega, zbar, AA, BB)  # [λ_A, λ_B]
            if abs(lhs - rhs) > 1e-8:
                viol[name] += 1"""
assert old_run in s, "run block not found"
s = s.replace(old_run, new_run)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("fixed")
