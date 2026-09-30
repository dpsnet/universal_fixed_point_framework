# -*- coding: utf-8 -*-
"""系统搜索 n=5 显式公式(31) 的 sg 记号解释组合"""
import sys, itertools
sys.path.insert(0, "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts")
from paperX_single_minus_numerics import (
    sg_pair, sg_block, A_R1, gen_R1_momentum, gen_generic_halfcollinear,
)

def A5_alt(omega, zbar, sg234_mode, sg123_mode, sg12_3_mode, sg12_34_mode):
    """(31) 用可配置的 sg 解释。mode: 0 = '前块|后块', 1 = '单元素第一块'"""
    w, z = omega, zbar
    def S234():
        return sg_block(w, z, (1,), (2, 3)) if sg234_mode == 1 else sg_block(w, z, (1, 2), (3,))
    def S123():
        return sg_block(w, z, (0,), (1, 2)) if sg123_mode == 1 else sg_block(w, z, (0, 1), (2,))
    def S12_3():
        return sg_block(w, z, (0,), (1, 2)) if sg12_3_mode == 1 else sg_block(w, z, (0, 1), (2,))
    def S12_34():
        return sg_block(w, z, (0,), (1, 2, 3)) if sg12_34_mode == 1 else sg_block(w, z, (0, 1), (2, 3))
    s234, s123, s12_3, s12_34 = S234(), S123(), S12_3(), S12_34()
    return 0.25 * (
        sg_block(w, z, (4,), (0,)) * sg_pair(w, z, 2, 3) * s234
        + sg_block(w, z, (4,), (0,)) * sg_pair(w, z, 1, 2) * s234
        - sg_block(w, z, (4,), (0,)) * s234 * s234
        + sg_pair(w, z, 3, 4) * s234 * s123
        + sg_pair(w, z, 3, 4) * sg_pair(w, z, 0, 1) * s12_3
        - sg_pair(w, z, 3, 4) * s123 * s123
        + sg_block(w, z, (4,), (0,)) * sg_pair(w, z, 3, 4) * s12_34
        + sg_pair(w, z, 0, 1) * sg_pair(w, z, 2, 3) * s12_34
    )

print("=== 16 种解释组合 vs 通式(39)，R1+动量守恒，3000 采样 ===")
labels = ["sg234", "sg123", "sg12,3", "sg12,34"]
for combo in itertools.product([0, 1], repeat=4):
    fail = 0
    for _ in range(3000):
        omega, zbar = gen_R1_momentum(5)
        a5 = A5_alt(omega, zbar, *combo)
        ar = A_R1(omega, zbar)
        if abs(a5 - ar) > 1e-12:
            fail += 1
    tag = ", ".join(f"{lbl}={m}" for lbl, m in zip(labels, combo))
    print(f"  [{tag}] fail={fail}/3000 {'<<< PASS' if fail == 0 else ''}")

print("\n=== 对 pass 的组合做一般半共线一致性检查（循环性/反射/U1/KK）===")
for combo in itertools.product([0, 1], repeat=4):
    fail_c = fail_r = fail_u = fail_k = 0
    for _ in range(3000):
        omega, zbar = gen_generic_halfcollinear(5)
        # 循环性 A_12345 = A_23451
        a1 = A5_alt(omega, zbar, *combo)
        om = [omega[i] for i in [1, 2, 3, 4, 0]]; zb = [zbar[i] for i in [1, 2, 3, 4, 0]]
        a2 = A5_alt(om, zb, *combo)
        if abs(a1 - a2) > 1e-12: fail_c += 1
        # 反射 A_12345 = -A_54321
        om = [omega[i] for i in [4, 3, 2, 1, 0]]; zb = [zbar[i] for i in [4, 3, 2, 1, 0]]
        if abs(a1 - (-1) ** 5 * A5_alt(om, zb, *combo)) > 1e-12: fail_r += 1
        # U1: A_12345+A_13452+A_14523+A_15234 = 0
        perms = [[0, 2, 3, 4, 1], [0, 3, 4, 1, 2], [0, 4, 1, 2, 3]]
        total = a1
        for p in perms:
            om = [omega[i] for i in p]; zb = [zbar[i] for i in p]
            total += A5_alt(om, zb, *combo)
        if abs(total) > 1e-12: fail_u += 1
        # KK: A_12345+A_12354+A_12435+A_14235 = 0
        perms = [[0, 1, 2, 4, 3], [0, 1, 3, 2, 4], [0, 3, 1, 2, 4]]
        total = a1
        for p in perms:
            om = [omega[i] for i in p]; zb = [zbar[i] for i in p]
            total += A5_alt(om, zb, *combo)
        if abs(total) > 1e-12: fail_k += 1
    tag = ", ".join(f"{lbl}={m}" for lbl, m in zip(labels, combo))
    print(f"  [{tag}] cyc={fail_c} ref={fail_r} u1={fail_u} kk={fail_k}")
