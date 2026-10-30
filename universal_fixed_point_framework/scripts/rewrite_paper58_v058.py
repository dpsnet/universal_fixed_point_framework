# -*- coding: utf-8 -*-
"""Paper 58 v0.58：稿态未决句更新（M24 定位钉死）+ 推论 5.9 补充"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("**版本**：v0.57（2026-10-06）", "**版本**：v0.58（2026-10-06）", 1)

old = "**当前未决**：解析完全闭合（终极路径——退化光谱已精细：m-pattern 判别（A=0 偏中段 m 组合/|m|峰值 4、A≠0 偏大端 m/空模式）——强判别非完备；判据完备性 = 光谱分类 + 边界枚举）；跨 seed 合并口径补因子；n=12 测绘。"
new = "**当前未决**：解析完全闭合（终极路径——定位钉死：退化判别在块和层不可行（重叠区 152/153 不可判），目标 = 判据映射完备性定理（50 基座映射与 A 符号一致，A=0 默认 0）——小 n 符号公式 F 推导为下一锚点）；跨 seed 合并口径补因子；n=12 测绘。"
assert old in s
s = s.replace(old, new, 1)

# 推论 5.9 补充（退化光谱条目后）
anchor = "* 诚实标注："
add_cor = ("* **块和层极限（M24）**：重叠 m-pattern 区 152/153 判别基座 = 0（202 附加因子不可补）、空模式区不可判"
           "——退化（A=0）依赖超出块和符号的信息——**完备判据不存在于块和层**——判据完备性定位为"
           "基座映射与 A 符号一致（非退化判别）。\n\n"
           )
assert anchor in s
s = s.replace(anchor, add_cor + anchor, 1)

old = "| v0.57 | 2026-10-06 | **m-pattern 判别（Phase 77 M23）**"
add = ("| v0.58 | 2026-10-06 | **重叠区不可判（Phase 77 M24）**：152/153 判别基座 0、空模式区 0——"
       "块和层极限钉死——解析完全闭合定位 = 判据映射完备性（非退化判别）。 |\n| v0.57 | 2026-10-06 | **m-pattern 判别（Phase 77 M23）**")
assert old in s
s = s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.58 written")
