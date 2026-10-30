# -*- coding: utf-8 -*-
"""Paper 58 v0.61：稿态未决句更新（M27 机制闭环）+ 推论 5.9 补充"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("**版本**：v0.60（2026-10-06）", "**版本**：v0.61（2026-10-06）", 1)

old = "**当前未决**：解析完全闭合（终极路径——环向检验收敛：单对环向 s_{n,1} 被 50 基座隐含决定（稀有例外 3.3e-5 级 = 8 冲突候选，M27 百万级验证登记）、多粒子环向独立但影响待查——判据映射完备性 = 相邻块投影 + 环向边界）；跨 seed 合并口径补因子；n=12 测绘。"
new = "**当前未决**：解析完全闭合（终极路径——机制闭环：判据空间（220 相邻区间）缺跨区间家族 {s_{k,1}}——中间对 6-30% 独立、末端对隐含决定——A 公式含中间对（s51 实证）——判据映射完备性 = 相邻块投影 + 跨区间自由度边界；解析完全闭合定理的边界条件已显式化）；跨 seed 合并口径补因子；n=12 测绘。"
assert old in s
s = s.replace(old, new, 1)

# 推论 5.9 补充（环向独立性条目后）
anchor = "* 诚实标注："
add_cor = ("* **跨区间家族与机制闭环（M27）**：100 万样本——末端跨区间对 s10_1/s11_1 组内 0 分裂（Poisson 上界 2.7e-5 < 8 冲突率）"
           "——**中间跨区间对 s_{k,1}（k=2..9）6%-30% 分裂——判据空间缺整个跨区间家族**——A6 含 s51（中间）实证——"
           "8 冲突 = 跨区间翻转 + A 判定的双重稀有边界事件。\n\n"
           )
assert anchor in s
s = s.replace(anchor, add_cor + anchor, 1)

old = "| v0.60 | 2026-10-06 | **n=11 环向检验（Phase 77 M26）**"
add = ("| v0.61 | 2026-10-06 | **跨区间家族（Phase 77 M27）**：100 万样本——末端对 0 分裂排除、中间对 6-30% 分裂——"
       "判据空间缺跨区间家族——8 冲突机制闭环。 |\n| v0.60 | 2026-10-06 | **n=11 环向检验（Phase 77 M26）**")
assert old in s
s = s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.61 written")
