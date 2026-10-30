# -*- coding: utf-8 -*-
"""Paper 58 v0.52：稿态压缩（就地改写为简洁当前状态声明，不再追加细节）"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

# 1) 版本
s = s.replace("**版本**：v0.51（2026-10-06）", "**版本**：v0.52（2026-10-06）", 1)

# 2) 稿态整行替换（短锚点：以 "**稿态**：" 开头、到 "**前置依赖**：" 之前）
i0 = s.find("**稿态**：")
i1 = s.find("**前置依赖**：")
assert 0 < i0 < i1, (i0, i1)
old_para = s[i0:i1]
new_para = (
    "**稿态**：初稿（数值 + 解析 + Lean 混合完成度）。主线完成：BG 递归数值验证基座"
    "（通式 n=3–10、五项一致性、软定理全 pass）；符号判据闭合链 n=5→n=11 全阶完成"
    "（推论 5.2–5.9，各阶最小基座 12/16/31/38/59/50，n=11 判据域分层：符号域 46 基座闭合、"
    "退化域长块主导）；级联机制与判定表 Lean 化零 sorry；形变循环翻译与内生挂靠完成"
    "（定理 7.1 解析、静默分层 S3/S4、编码声明 B1'）。**当前未决**：解析完全闭合"
    "（终极路径——退化 ⟺ 长块过零/翻转机制待解析化）；跨 seed 合并口径补因子；n=12 测绘。\n\n"
)
new_s = s[:i0] + new_para + s[i1:]
print(f"稿态压缩: {len(old_para)} 字符 → {len(new_para)} 字符")

# 3) 变更记录
old = "| v0.51 | 2026-10-06 |"
add = ("| v0.52 | 2026-10-06 | **稿态压缩**：~1100 字符 → ~450 字符——各阶判据细节归推论条目，"
       "未决清单精简为 3 项（解析完全闭合/跨 seed 口径补因子/n=12 测绘）。 |\n| v0.51 | 2026-10-06 |")
assert old in new_s
new_s = new_s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(new_s)
print("Paper 58 v0.52 written")
