# -*- coding: utf-8 -*-
"""Paper 58 就地补 P83 交叉引用声明（服务 Paper 48 完善）。"""
import io

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(P, "r", encoding="utf-8") as f:
    t = f.read()

old = "- **白矮星 EW 独立预言（P83 推进）**：M83a 方法框架完成"
new = "- **白矮星 EW 独立预言（P83 推进——服务 Paper 48 拓扑禁戒观测验证的专业模型大气复核，Paper 48 已同步 v0.5 并新增 §4.4）**：M83a 方法框架完成"
assert t.count(old) == 1, "anchor fail"
t = t.replace(old, new)

with io.open(P, "w", encoding="utf-8") as f:
    f.write(t)
print("OK paper58 cross-ref, len=%d" % len(t))
