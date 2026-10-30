# -*- coding: utf-8 -*-
"""Paper 58 v0.56：稿态未决句更新（符号对相反机制）+ 推论 5.9 补充一条"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("**版本**：v0.55（2026-10-06）", "**版本**：v0.56（2026-10-06）", 1)

old = "**当前未决**：解析完全闭合（终极路径——块和层判别退化已被证伪（含零块/无零块区均不可分），转向判据完备性定理：符号判据映射与 A 真实符号一致——BG 递归符号代数 F 推导，小 n 起步）；跨 seed 合并口径补因子；n=12 测绘。"
new = "**当前未决**：解析完全闭合（终极路径——退化机制核心已确立：符号对相反（通式 (39) 乘积因子，A=0 99.86% 含）——判据完备性沿通式结构证明；324 例外与 generic 区非充分性为诚实边界）；跨 seed 合并口径补因子；n=12 测绘。"
assert old in s
s = s.replace(old, new, 1)

# 推论 5.9 补充一条（在"阶数规律反转"后、诚实标注前）
anchor = "* 诚实标注："
add_cor = ("* **退化机制解析根源（M22）**：通式 (39) 乘积结构 A|R1 = 2^{2-n}∏(sg_{m,m+1}+sg_{1,2..m})——"
           "A=0 ⟺ 符号对相反（∃m: sg_{m,m+1}=-sg_{1,2..m}≠0 或双零）——R1 区解析精确；generic 区外推 "
           "A=0 的 99.86% 含符号对相反——判据“粒子 1 前缀块”= 通式 (39) 因子——退化判据核心为符号对判定；"
           "A≠0 的 92.7% 亦含（generic 非乘积）+ 324 例外（0.14%）——诚实边界细化。\n\n"
           )
assert anchor in s
s = s.replace(anchor, add_cor + anchor, 1)

old = "| v0.55 | 2026-10-06 | **块和层不可判退化（Phase 77 M20/M21）**"
add = ("| v0.56 | 2026-10-06 | **符号对相反机制（Phase 77 M22）**：通式 (39) 乘积因子解析根源——A=0 99.86% 含符号对相反、"
       "324 例外、A≠0 92.7% 亦含（generic 非乘积）；M19 T1 修正为符号对判定。 |\n| v0.55 | 2026-10-06 | **块和层不可判退化（Phase 77 M20/M21）**")
assert old in s
s = s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.56 written")
