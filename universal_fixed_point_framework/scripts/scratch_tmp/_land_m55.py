# -*- coding: utf-8 -*-
"""落盘 M55：roadmap + 笔记 §67 + Paper 58 v0.84"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase77_n11_crossset_greedy.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 开放登记（更新）"
add = """## M55 ✅ n=12 粗测（2026-10-06，样本量依赖性问题——方法学警示）

- **n=12 R1 通式 20 因子冲突 16（6000 样本）——追加 3 → 23 因子 0 冲突——最小化后 17**（6000 样本）
- **⚠ 17 不可直接比**：6000 vs 60000 样本——**谱维数是采样规模相关的观测**——小样本过拟合（冲突没被采样到）给出过小覆盖
- **方法学结论**：谱维数（最小完备覆盖）必须同采样规模比较——n=8-11（30000-60000）→ 20-26——n=12 需 ≥30000 才可比（A_BG n=12 ~250ms/样本——60000 需 ~4h——登记后续）
- 证据：`paperX_n12_m55_scale.json` + `cache_n12_thr3x2000.pkl`

## 开放登记（更新）
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 六十七、n=12 粗测与样本量依赖性问题（2026-10-06，Phase 77 M55）

**n=12 粗测（3×2000=6000 阈值化）**：R1 通式 20 因子冲突 16——追加 3（s1234_5、s12345_67、s123456789_10）→ 23 因子 0 冲突——最小化后 **17 因子 0 冲突**。

**⚠ 方法学警示（重要）**：
1. **17 不可直接比**——6000 vs 60000 样本——**谱维数是采样规模相关的观测**
2. **小样本过拟合**：冲突模式没被采样到 → 因子覆盖需求虚低 → 谱维数下界偏差
3. **正确口径**：谱维数必须同采样规模比较——n=8-11（30000-60000）→ 20-26——n=12 需 ≥30000（A_BG n=12 ~250ms/样本——60000 需 ~4h——登记后续大样本任务）
4. **对 MUFPF 的意义**："谱维数"的观测值内含采样规模维度——完备覆盖的"收敛"需要样本量→∞的极限——这是**采样代表性理论**（Phase 76）在谱维数上的延续——**任何谱维数陈述必须附样本量**（同 EW 测量附信噪比）

**登记**：n=12 大样本（≥30000）谱维数——后台长任务。
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)

p3 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
s3 = io.open(p3, "r", encoding="utf-8").read()
s3 = s3.replace("**版本**：v0.83（2026-10-06）", "**版本**：v0.84（2026-10-06）", 1)
old = "| v0.83 | 2026-10-06 | **摘要与推论 5.9 同步（Phase 77 链）**"
add3 = "| v0.84 | 2026-10-06 | **n=12 粗测 + 样本量依赖性（Phase 77 M55）**：6000 样本下 17 因子（过拟合下界）——谱维数必须同采样规模比较——n=12 大样本登记后续。 |\n| v0.83 | 2026-10-06 | **摘要与推论 5.9 同步（Phase 77 链）**"
assert old in s3
s3 = s3.replace(old, add3, 1)
io.open(p3, "w", encoding="utf-8").write(s3)
print("M55 落盘完成（roadmap + 笔记 §67 + Paper 58 v0.84）")
