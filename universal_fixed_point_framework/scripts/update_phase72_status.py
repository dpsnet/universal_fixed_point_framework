# -*- coding: utf-8 -*-
import io
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase72_n5_symbol_criterion.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()
old = '阶数规律修正"20 尾部 + 退化补"**'
new = '阶数规律修正"20 尾部 + 退化补"；n=8 级联机制数值+Lean 闭合（M13/M14，2026-10-01）——13 条恒等式 0 违反 + N8Criterion 零 sorry（双元素块块积模式）；n=9 判据数值闭合（M15/M16，2026-10-01）——27 因子基座（25 尾部 + 2 补因子 s1_2345/s123_456789），15212 模式全决定性，2×15000 独立复核 0 冲突，非零率 5.6%**'
assert old in s, "anchor not found"
s = s.replace(old, new, 1)
with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("status line updated")
