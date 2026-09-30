# -*- coding: utf-8 -*-
"""一次性 patch：用放大OCR逗号版(32)替换 numerics.py 的 A6（3000/3000 与 BG 递归一致）"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_single_minus_numerics.py"
with io.open(p, "r", encoding="utf-8") as f:
    src = f.read()

old6_start = src.index("def A6(omega, zbar):")
old6_end = src.index("EXPLICIT = {3: A3, 4: A4, 5: A5, 6: A6}")
new6 = '''def A6(omega, zbar):
    """(32) A_123456，32 项（2026-09-30 依据放大OCR：显式逗号，块和|块和规则
    sg_{A,B} = sg([Σλ_A, Σλ_B])；与 BG 递归(21) 3000/3000 一致）
    """
    w, z = omega, zbar
    s1_23  = sg_block(w, z, (0,), (1, 2))
    s12_3  = sg_block(w, z, (0, 1), (2,))
    s123_4 = sg_block(w, z, (0, 1, 2), (3,))
    s56    = sg_pair(w, z, 4, 5)
    s23    = sg_pair(w, z, 1, 2)
    s1_234 = sg_block(w, z, (0,), (1, 2, 3))
    s12_34 = sg_block(w, z, (0, 1), (2, 3))
    s34    = sg_pair(w, z, 2, 3)
    s2_34  = sg_block(w, z, (1,), (2, 3))
    s23_4  = sg_block(w, z, (1, 2), (3,))
    s12    = sg_pair(w, z, 0, 1)
    s345_6 = sg_block(w, z, (2, 3, 4), (5,))
    s45_6  = sg_block(w, z, (3, 4), (5,))
    s45    = sg_pair(w, z, 3, 4)
    s3_45  = sg_block(w, z, (2,), (3, 4))
    s34_5  = sg_block(w, z, (2, 3), (4,))
    s234_5 = sg_block(w, z, (1, 2, 3), (4,))
    s61    = sg_block(w, z, (5,), (0,))
    s2_345 = sg_block(w, z, (1,), (2, 3, 4))
    s23_45 = sg_block(w, z, (1, 2), (3, 4))
    return 1.0 / 8.0 * (
        -s1_23 * s12_3 * s123_4 * s56
        + s1_23 * s123_4 * s23 * s56
        + s1_234 * s12_34 * s123_4 * s56
        - s1_234 * s12_34 * s34 * s56
        - s1_234 * s123_4 * s23 * s56
        - s1_234 * s2_34 * s23_4 * s56
        + s1_234 * s2_34 * s34 * s56
        + s1_234 * s23 * s23_4 * s56
        + s12 * s12_3 * s123_4 * s56
        - s12 * s12_34 * s123_4 * s56
        + s12 * s12_34 * s34 * s56
        + s12 * s345_6 * s45_6 * s56
        - s1_23 * s12_3 * s45 * s45_6
        + s1_23 * s23 * s45 * s45_6
        + s12 * s12_3 * s45 * s45_6
        - s12 * s3_45 * s34_5 * s345_6
        + s12 * s3_45 * s345_6 * s45
        + s12 * s34 * s34_5 * s345_6
        - s2_34 * s23_4 * s234_5 * s61
        + s2_34 * s234_5 * s34 * s61
        + s2_345 * s23_45 * s234_5 * s61
        - s2_345 * s23_45 * s45 * s61
        - s2_345 * s234_5 * s34 * s61
        - s2_345 * s3_45 * s34_5 * s61
        + s2_345 * s3_45 * s45 * s61
        + s2_345 * s34 * s34_5 * s61
        + s23 * s23_4 * s234_5 * s61
        - s23 * s23_45 * s234_5 * s61
        + s23 * s23_45 * s45 * s61
        + s345_6 * s45 * s45_6 * s61
        + s23 * s45_6 * s56 * s61
        + s34 * s345_6 * s56 * s61
    )


'''
src = src[:old6_start] + new6 + src[old6_end:]

with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(src)
print("A6 已更新为逗号版（块和|块和规则）")
