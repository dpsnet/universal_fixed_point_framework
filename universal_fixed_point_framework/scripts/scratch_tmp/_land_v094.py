# -*- coding: utf-8 -*-
"""Paper 58 v0.93 -> v0.94：变更记录追加"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper58_channel_separation_single_minus.md'
s = io.open(p, encoding='utf-8').read()

old = "| v0.93 | 2026-10-07 | **M81c 第 10 章边界更新（P81 终稿化）**"
new = "| v0.94 | 2026-10-07 | **M81d 附录证据索引补全（P81 终稿化）+ Phase 78 支线收官**：附录 A 追加谱维数链（Phase 77/79）＋P80/P82/P83＋Phase 78（P1\u2013P4）证据索引；Phase 78 收官（P3 层单值性 0 奇异点、P4 孔洞指数增长 2^(-1.05n)\u2014\u2014符号场 = 多孔胞腔流形良定义层）。 |\n| v0.93 | 2026-10-07 | **M81c 第 10 章边界更新（P81 终稿化）**"
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('v0.94 写入完成')
