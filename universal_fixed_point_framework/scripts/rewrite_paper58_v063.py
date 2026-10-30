# -*- coding: utf-8 -*-
"""Paper 58 v0.63：稿态未决句更新（M29 最小完备子集）+ 推论 5.9 补充"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("**版本**：v0.62（2026-10-06）", "**版本**：v0.63（2026-10-06）", 1)

old = "**当前未决**：解析完全闭合（终极路径——判据层面闭环：220 相邻区间全因子 0 冲突（240000 合并口径——判据映射完备性定理实证）——8 冲突 = 50 贪心子集缺信息（M27 跨区间假说修正）；下一锚点：Φ 解析结构/最小完备子集）；n=12 测绘。"
new = "**当前未决**：解析完全闭合（终极路径——判据层面闭环：最小完备子集 55 因子 0 冲突（补集 5 因子全在右端——8 冲突根因 = 贪心右端缺失）；Φ 解析结构/55 全局最小性/分布外泛化）；n=12 测绘。"
assert old in s
s = s.replace(old, new, 1)

# 推论 5.9 补充（完备性条目后）
anchor = "* 诚实标注："
add_cor = ("* **最小完备子集（M29）**：8 冲突组定向补集——5 个右端因子（s5_678910/s78910_11/s8_9/s89_10/s910_11）"
           "——**55 因子基座 0 冲突**（240000 合并口径）——8 冲突根因 = 贪心 50 的右端结构缺失（左端偏置）。\n\n"
           )
assert anchor in s
s = s.replace(anchor, add_cor + anchor, 1)

old = "| v0.62 | 2026-10-06 | **判据映射完备性（Phase 77 M28）**"
add = ("| v0.63 | 2026-10-06 | **最小完备子集（Phase 77 M29）**：55 因子 0 冲突（补集 5 右端因子）——"
       "8 冲突根因 = 贪心右端缺失。 |\n| v0.62 | 2026-10-06 | **判据映射完备性（Phase 77 M28）**")
assert old in s
s = s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.63 written")
