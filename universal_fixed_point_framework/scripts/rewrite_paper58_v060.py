# -*- coding: utf-8 -*-
"""Paper 58 v0.60：稿态未决句更新（M26 环向检验）+ 推论 5.9 补充"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("**版本**：v0.59（2026-10-06）", "**版本**：v0.60（2026-10-06）", 1)

old = "**当前未决**：解析完全闭合（终极路径——F 已探：动量守恒恒等式 sg_41=sg_12-sg_23+sg_34（括号值精确）但符号超块和层——8 冲突理论来源 = 环向因子 s_{n,1} 独立翻转（M26 验证中）；判据映射完备性 = F 的相邻块投影 + 环向边界）；跨 seed 合并口径补因子；n=12 测绘。"
new = "**当前未决**：解析完全闭合（终极路径——环向检验收敛：单对环向 s_{n,1} 被 50 基座隐含决定（稀有例外 3.3e-5 级 = 8 冲突候选，M27 百万级验证登记）、多粒子环向独立但影响待查——判据映射完备性 = 相邻块投影 + 环向边界）；跨 seed 合并口径补因子；n=12 测绘。"
assert old in s
s = s.replace(old, new, 1)

# 推论 5.9 补充（环向因子条目后）
anchor = "* 诚实标注："
add_cor = ("* **环向独立性（M26）**：n=11 采样 40000——s11_1 单对环向 50 基座组内 0 分裂（隐含决定，稀有例外 3.3e-5 级"
           "与 8 冲突量级自洽——M27 百万级登记）；s11_12/s11_123 多粒子环向 3.8%/5.8% 分裂（独立但可能不影响 A——"
           "A 公式含单对环向）。\n\n"
           )
assert anchor in s
s = s.replace(anchor, add_cor + anchor, 1)

old = "| v0.59 | 2026-10-06 | **n=4 符号公式 F（Phase 77 M25a）**"
add = ("| v0.60 | 2026-10-06 | **n=11 环向检验（Phase 77 M26）**：s11_1 组内 0 分裂（隐含决定 + 稀有例外量级自洽）、"
       "s11_12/s11_123 独立（影响待查）——环向假说部分支持。 |\n| v0.59 | 2026-10-06 | **n=4 符号公式 F（Phase 77 M25a）**")
assert old in s
s = s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.60 written")
