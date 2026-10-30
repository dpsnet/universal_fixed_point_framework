# -*- coding: utf-8 -*-
"""落盘 M44/M45：roadmap + 笔记 §60 + Paper 58 v0.76"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase77_n11_crossset_greedy.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 开放登记（更新）"
add = """## M44 ✅ 极小基座非唯一（2026-10-06，谱维数概念修正）

- **5 轮随机序极小化终局 [45,43,44,45,47]**——43 非唯一极小
- **5 轮公共因子 = 0**——不同极小集零交集——**判据映射的完备覆盖高度非唯一**（220 因子中每因子可被其他组合替代——无核心因子集）

## M45 ✅ 必要性 + 分布深化（2026-10-06，谱维数 ∈ [41,47]）

- **M40 的 43 名单全必要**（43/43——删任一 → 冲突 1-18——"名单内每因子必要"确认）
- **10 轮终局 [45,43,44,45,47,43,41,46,42,43]**——**轮7 找到 41**——43 非最小
- **谱维数观测区间 [41,47]**（均值 43.9）——真实谱维数 ≤ 41（待 M46 30 轮下探）
- 证据：`paperX_n11_m44_strongmin.json` + `paperX_n11_m45_strongmin2.json`
- **M46 已启动**：30 轮全局搜索（保存名单 + 公共因子 + 最小名单必要性）——后台 ~48 分钟

## 开放登记（更新）
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 六十、谱维数的非唯一性：极小基座区间（2026-10-06，Phase 77 M44/M45）

**M44**：5 轮随机序阈值化极小化终局 [45,43,44,45,47]——**非唯一极小**——**5 轮公共因子 0**（不同极小集零交集）。

**M45**：
- **M40 的 43 名单全必要**（43/43——删任一 → 冲突 1-18）——"在名单内每因子必要"
- 10 轮最小 **41**（轮7）——**43 非最小**
- **谱维数观测区间 [41,47]**（均值 43.9）

**理论重构（重要）**：
1. **"谱维数"不是唯一数**——而是**完备覆盖的多样性**：存在多个（可能很多个）不相交的极小基座（41-47 因子），都能 0 冲突完备编码剥离振幅符号
2. **公共因子 0 的意义**：判据映射的因子冗余极高——每个因子可被其他因子组合"替代"（符号信息多重编码）——**没有单个因子是任何完备覆盖所必需**
3. **"谱维数"作为概念应改为"极小覆盖区间 [min, max]"**——min = 最小完备覆盖大小（信息论意义）、max = 最大必要覆盖
4. **与 M34d "1-锚定链状覆盖"的关系**：那是**单名单内必要性**（删任一破坏完备）——**跨名单无公共因子**——即"名单内必要但非全局必要"——覆盖的强非唯一性

**待 M46**：30 轮下探（能否 < 41？）+ 30 轮公共因子（是否仍 0？）+ 最小名单必要性
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)

p3 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
s3 = io.open(p3, "r", encoding="utf-8").read()
s3 = s3.replace("**版本**：v0.75（2026-10-06）", "**版本**：v0.76（2026-10-06）", 1)
old = "| v0.75 | 2026-10-06 | **阈值化真实谱维数 43（Phase 77 M40）**"
add3 = "| v0.76 | 2026-10-06 | **谱维数非唯一性（Phase 77 M44/M45）**：极小基座区间 [41,47]（10 轮）——43 内全必要但非最小——公共因子 0（覆盖强非唯一）——全局极小待 M46。 |\n| v0.75 | 2026-10-06 | **阈值化真实谱维数 43（Phase 77 M40）**"
assert old in s3
s3 = s3.replace(old, add3, 1)
io.open(p3, "w", encoding="utf-8").write(s3)
print("M44/M45 落盘完成（roadmap + 笔记 §60 + Paper 58 v0.76）")
