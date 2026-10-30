# -*- coding: utf-8 -*-
"""Paper 58 v0.49：章节顺序修正——结论移至最后"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

i10 = s.find("\n## 10 结论")
i11 = s.find("\n## 11 诚实边界与局限")
iref = s.find("\n## 参考文献")
assert 0 < i10 < i11 < iref, (i10, i11, iref)

ch_concl = s[i10:i11]
ch_hb = s[i11:iref]
new_s = (s[:i10]
         + ch_hb.replace("\n## 11 诚实边界与局限", "\n## 10 诚实边界与局限")
         + ch_concl.replace("\n## 10 结论", "\n## 11 结论")
         + s[iref:])

new_s = new_s.replace("**版本**：v0.48（2026-10-06）", "**版本**：v0.49（2026-10-06）")
old = "| v0.48 | 2026-10-06 |"
add = ("| v0.49 | 2026-10-06 | **章节顺序修正**：结论移至最后——"
       "“10 诚实边界与局限”在前、“11 结论”收尾（正文 → 局限 → 结论 → 参考文献）。 |\n| v0.48 | 2026-10-06 |")
assert old in new_s
new_s = new_s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(new_s)
print("v0.49 written")
