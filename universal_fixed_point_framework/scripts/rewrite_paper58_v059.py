# -*- coding: utf-8 -*-
"""Paper 58 v0.59：稿态未决句更新（M25a 环向因子）+ 推论 5.9 补充"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("**版本**：v0.58（2026-10-06）", "**版本**：v0.59（2026-10-06）", 1)

old = "**当前未决**：解析完全闭合（终极路径——定位钉死：退化判别在块和层不可行（重叠区 152/153 不可判），目标 = 判据映射完备性定理（50 基座映射与 A 符号一致，A=0 默认 0）——小 n 符号公式 F 推导为下一锚点）；跨 seed 合并口径补因子；n=12 测绘。"
new = "**当前未决**：解析完全闭合（终极路径——F 已探：动量守恒恒等式 sg_41=sg_12-sg_23+sg_34（括号值精确）但符号超块和层——8 冲突理论来源 = 环向因子 s_{n,1} 独立翻转（M26 验证中）；判据映射完备性 = F 的相邻块投影 + 环向边界）；跨 seed 合并口径补因子；n=12 测绘。"
assert old in s
s = s.replace(old, new, 1)

# 推论 5.9 补充（块和层极限条目后）
anchor = "* 诚实标注："
add_cor = ("* **环向因子与 F（M25a）**：动量守恒下 sg_{n,1} = 相邻块线性组合（括号值精确恒等）但符号超块和符号层"
           "——n=4 的 23.95% 样本判据符号非决定（同 (sg_12,sg_23,sg_34) 不同 A4）——判据基座（无环向因子）"
           "的 8 冲突理论来源 = 环向因子符号独立翻转（假说登记 M26 验证）。\n\n"
           )
assert anchor in s
s = s.replace(anchor, add_cor + anchor, 1)

old = "| v0.58 | 2026-10-06 | **重叠区不可判（Phase 77 M24）**"
add = ("| v0.59 | 2026-10-06 | **n=4 符号公式 F（Phase 77 M25a）**：动量守恒恒等式括号值精确、符号超块和层；"
       "A4 23.95% 判据符号非决定——8 冲突理论来源 = 环向因子（假说登记 M26）。 |\n| v0.58 | 2026-10-06 | **重叠区不可判（Phase 77 M24）**")
assert old in s
s = s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.59 written")
