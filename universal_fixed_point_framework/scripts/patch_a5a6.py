# -*- coding: utf-8 -*-
"""一次性 patch：修正 scripts/paperX_single_minus_numerics.py 的 A5/A6"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_single_minus_numerics.py"
with io.open(p, "r", encoding="utf-8") as f:
    src = f.read()

old5 = '''def A5(omega, zbar):
    """(31) A_12345，8 项"""
    w, z = omega, zbar
    return 0.25 * (
        sg_block(w, z, (4,), (0,)) * sg_pair(w, z, 2, 3) * sg_block(w, z, (1,), (2, 3))
        + sg_block(w, z, (4,), (0,)) * sg_pair(w, z, 1, 2) * sg_block(w, z, (1,), (2, 3))
        - sg_block(w, z, (4,), (0,)) * sg_block(w, z, (1,), (2, 3)) * sg_block(w, z, (1,), (2, 3))
        + sg_pair(w, z, 3, 4) * sg_block(w, z, (1,), (2, 3)) * sg_block(w, z, (0,), (1, 2))
        + sg_pair(w, z, 3, 4) * sg_pair(w, z, 0, 1) * sg_block(w, z, (0, 1), (2,))
        - sg_pair(w, z, 3, 4) * sg_block(w, z, (0,), (1, 2)) * sg_block(w, z, (0,), (1, 2))
        + sg_block(w, z, (4,), (0,)) * sg_pair(w, z, 3, 4) * sg_block(w, z, (0, 1), (2, 3))
        + sg_pair(w, z, 0, 1) * sg_pair(w, z, 2, 3) * sg_block(w, z, (0, 1), (2, 3))
    )'''

new5 = '''def A5(omega, zbar):
    """(31) A_12345，8 项（2026-09-30 修正：项1= sg_51【第1版OCR】，首索引规则
    sg_{abc...} = sg([λ_a, λ_b+λ_c+...])；项4/5/7/8 原实现用错 sg 级联记号，已修正）
    注：generic 配置下与 (21)/(39) 完全一致；剥离振幅=0 的退化配置（预振幅 Θ 消失）
    下存在残余不一致（≈0.6%），疑似论文印刷级问题，待 paperX 验证小结记录。
    """
    w, z = omega, zbar
    s51 = sg_block(w, z, (4,), (0,))
    s12 = sg_pair(w, z, 0, 1)
    s23 = sg_pair(w, z, 1, 2)
    s34 = sg_pair(w, z, 2, 3)
    s45 = sg_pair(w, z, 3, 4)
    s234 = sg_block(w, z, (1,), (2, 3))
    s123 = sg_block(w, z, (0,), (1, 2))
    s1234 = sg_block(w, z, (0,), (1, 2, 3))
    return 0.25 * (
        s51 * s34 * s234
        + s51 * s23 * s234
        - s51 * s234 * s234
        + s45 * s23 * s123
        + s45 * s12 * s123
        - s45 * s123 * s123
        + s51 * s45 * s1234
        + s12 * s34 * s1234
    )'''

assert old5 in src, "old5 not found"
src = src.replace(old5, new5)

old6_start = src.index("def A6(omega, zbar):")
old6_end = src.index("EXPLICIT = {3: A3, 4: A4, 5: A5, 6: A6}")
new6 = '''def A6(omega, zbar):
    """(32) A_123456，32 项（2026-09-30 依据第2版OCR实现；首索引规则 sg_{abc...}=sg([λ_a,Σ其余λ])）
    注：与 A5 同理，generic 配置下应与 (21)/(39) 一致；退化配置下可能残余不一致。
    """
    w, z = omega, zbar
    s12   = sg_pair(w, z, 0, 1)
    s23   = sg_pair(w, z, 1, 2)
    s34   = sg_pair(w, z, 2, 3)
    s45   = sg_pair(w, z, 3, 4)
    s56   = sg_pair(w, z, 4, 5)
    s61   = sg_block(w, z, (5,), (0,))
    s123  = sg_block(w, z, (0,), (1, 2))
    s1234 = sg_block(w, z, (0,), (1, 2, 3))
    s234  = sg_block(w, z, (1,), (2, 3))
    s456  = sg_block(w, z, (3,), (4, 5))
    s345  = sg_block(w, z, (2,), (3, 4))
    s3456 = sg_block(w, z, (2,), (3, 4, 5))
    s2345 = sg_block(w, z, (1,), (2, 3, 4))
    return 1.0 / 8.0 * (
        -s123 * s123 * s1234 * s56
        + s123 * s1234 * s23 * s56
        + s1234 * s1234 * s1234 * s56
        - s1234 * s1234 * s34 * s56
        - s1234 * s1234 * s45 * s56
        - s1234 * s23 * s234 * s56
        + s1234 * s23 * s34 * s56
        + s1234 * s234 * s234 * s56
        + s12 * s123 * s1234 * s456
        - s12 * s1234 * s1234 * s456
        + s12 * s1234 * s34 * s456
        + s12 * s345 * s456 * s456
        - s123 * s123 * s345 * s456
        + s123 * s23 * s345 * s456
        + s12 * s123 * s345 * s456
        - s12 * s345 * s345 * s3456
        + s12 * s345 * s345 * s456
        + s12 * s2345 * s345 * s456
        - s2345 * s2345 * s345 * s456
        + s234 * s2345 * s345 * s456
        + s2345 * s2345 * s2345 * s61
        - s2345 * s2345 * s45 * s61
        - s2345 * s2345 * s34 * s61
        - s2345 * s345 * s345 * s61
        + s2345 * s345 * s45 * s61
        + s2345 * s34 * s345 * s61
        + s234 * s234 * s2345 * s61
        - s234 * s2345 * s2345 * s61
        + s23 * s234 * s2345 * s61
        + s3456 * s45 * s456 * s61
        + s23 * s456 * s56 * s61
        + s34 * s3456 * s61
    )


'''
src = src[:old6_start] + new6 + src[old6_end:]

with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(src)
print("A5/A6 已更新")
