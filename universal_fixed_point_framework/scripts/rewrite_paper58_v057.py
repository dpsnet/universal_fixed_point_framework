# -*- coding: utf-8 -*-
"""Paper 58 v0.57：稿态未决句更新（m-pattern 判别）+ 推论 5.9 补充"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("**版本**：v0.56（2026-10-06）", "**版本**：v0.57（2026-10-06）", 1)

old = "**当前未决**：解析完全闭合（终极路径——退化机制核心已确立：符号对相反（通式 (39) 乘积因子，A=0 99.86% 含）——判据完备性沿通式结构证明；324 例外与 generic 区非充分性为诚实边界）；跨 seed 合并口径补因子；n=12 测绘。"
new = "**当前未决**：解析完全闭合（终极路径——退化光谱已精细：m-pattern 判别（A=0 偏中段 m 组合/|m|峰值 4、A≠0 偏大端 m/空模式）——强判别非完备；判据完备性 = 光谱分类 + 边界枚举）；跨 seed 合并口径补因子；n=12 测绘。"
assert old in s
s = s.replace(old, new, 1)

# 推论 5.9 补充（符号对相反条目后）
anchor = "* 诚实标注："
add_cor = ("* **退化光谱（M23）**：m-pattern（符号对相反的 m 集合）判别——A=0 偏中段 m 组合"
           "（Top [4,6,8]，|m| 峰值 4 占 32.9%）、A≠0 偏大端 m/空（空模式 7.3% vs 0.14%——52 倍）——"
           "|m| 大小强判别非完备（153 重叠 + 324 空模式例外）——退化判据粗粒化解析特征。\n\n"
           )
assert anchor in s
s = s.replace(anchor, add_cor + anchor, 1)

old = "| v0.56 | 2026-10-06 | **符号对相反机制（Phase 77 M22）**"
add = ("| v0.57 | 2026-10-06 | **m-pattern 判别（Phase 77 M23）**：退化光谱结构——A=0 偏中段 m 组合、A≠0 偏大端/空"
       "（空模式 52 倍相对）——强判别非完备（153 重叠 + 324 例外）。 |\n| v0.56 | 2026-10-06 | **符号对相反机制（Phase 77 M22）**")
assert old in s
s = s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.57 written")
