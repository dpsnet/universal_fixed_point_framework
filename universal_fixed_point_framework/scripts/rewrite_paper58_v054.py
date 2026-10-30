# -*- coding: utf-8 -*-
"""Paper 58 v0.54：稿态两句话更新（M19 机制强化）+ 变更记录"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("**版本**：v0.53（2026-10-06）", "**版本**：v0.54（2026-10-06）", 1)

# 稿态未决句更新（就地改写，不追加）
old = "**当前未决**：解析完全闭合（终极路径——退化 ⟺ 长块过零/翻转机制待解析化）；跨 seed 合并口径补因子；n=12 测绘。"
new = "**当前未决**：解析完全闭合（终极路径——退化机制已实证：含零块 A=0 样本 100% 伴粒子 1 长块过零，定理候选 T1 待解析证明；无零块 26.5% 为分子相消第二机制待解析化）；跨 seed 合并口径补因子；n=12 测绘。"
assert old in s
s = s.replace(old, new, 1)

old = "| v0.53 | 2026-10-06 | **摘要压缩与更新**"
add = ("| v0.54 | 2026-10-06 | **退化机制图谱（Phase 77 M19）**：含零块 A=0 样本 100% 含粒子 1 长零块"
       "（退化 ⟺ 粒子 1 长块过零，240000 样本严格验证——定理候选 T1）；无零块 26.5% 分子相消第二机制；"
       "50 基座退化判据失败率 3.4e-5。 |\n| v0.53 | 2026-10-06 | **摘要压缩与更新**")
assert old in s
s = s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.54 written")
