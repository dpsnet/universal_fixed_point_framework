# -*- coding: utf-8 -*-
"""调试：定位 (31) n=5 显式公式与通式(39) 的不一致来源"""
import sys
sys.path.insert(0, "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts")
from paperX_single_minus_numerics import (
    sg_pair, sg_block, A5, A_R1, gen_R1_momentum, gen_generic_halfcollinear, sg,
)

# 找 n=5 失败样例
for trial in range(20000):
    omega, zbar = gen_R1_momentum(5)
    a5 = A5(omega, zbar)
    ar = A_R1(omega, zbar)
    if abs(a5 - ar) > 1e-12:
        print("=== n=5 失败样例 (R1+动量守恒) ===")
        print("omega =", [round(x, 4) for x in omega])
        print("zbar  =", [round(x, 4) for x in zbar])
        print("A5(31) =", a5, " A_R1(39) =", ar)
        # 打印所有相关 sg（用我的解释）
        w, z = omega, zbar
        sg_map = {
            "sg12": sg_pair(w, z, 0, 1), "sg23": sg_pair(w, z, 1, 2),
            "sg34": sg_pair(w, z, 2, 3), "sg45": sg_pair(w, z, 3, 4),
            "sg51": sg_block(w, z, (4,), (0,)),
            "sg234(2|34)": sg_block(w, z, (1,), (2, 3)),
            "sg234(23|4)": sg_block(w, z, (1, 2), (3,)),
            "sg123(1|23)": sg_block(w, z, (0,), (1, 2)),
            "sg123(12|3)": sg_block(w, z, (0, 1), (2,)),
            "sg12,3": sg_block(w, z, (0, 1), (2,)),
            "sg12,34": sg_block(w, z, (0, 1), (2, 3)),
        }
        for k, v in sg_map.items():
            print(f"  {k} = {v}")
        break
else:
    print("20000 次采样未找到 n=5 失败样例？")

# 无动量守恒的一般半共线下 A5 与 A_R1 的差异（R1 条件放宽）
print("\n=== 无动量守恒：A5(31) 是否等于 A_R1(39)？ ===")
fail_nc = 0
for _ in range(5000):
    omega, zbar = gen_generic_halfcollinear(5)
    # 加 R1 约束（无动量守恒）
    if omega[0] > 0:
        omega = [-x for x in omega]
    if any(x <= 0 for x in omega[1:]):
        continue
    if abs(A5(omega, zbar) - A_R1(omega, zbar)) > 1e-12:
        fail_nc += 1
print(f"无动量守恒+R1: fail = {fail_nc}/5000")
