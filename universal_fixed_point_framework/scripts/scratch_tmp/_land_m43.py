# -*- coding: utf-8 -*-
"""落盘 M43：roadmap + 笔记 §58 + Paper 58 v0.74（锚恒等式 Lean 闭合）"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase77_n11_crossset_greedy.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 开放登记（更新）"
add = """## M43 ✅ 动量双守恒恒等式 A（锚 k）Lean 机器证明（2026-10-06，零 sorry）

- **新模块** `MUFPFormalization.SingleMinusAnchorSum`——`lake build` 通过（3048 jobs，零 sorry）
- **定理 anchor_sum_zero**：Σω = 0、Σωz = 0 ⇒ Σ_{j≠k} P[k][j] = Σ_{j∈univ.erase k} ω_k ω_j (z_k−z_j) = 0（任何锚 k）
- **证明结构**（纯代数）：线性展开 → Finset.sum_erase_add（Σ_erase ω = −ω_k、Σ_erase ωz = −ω_k·z_k）→ ring
- **先证伪再证明闭环**：M38 跨 n 102000 检验 → Lean 形式证明——"动量双守恒"从采样级定理升级为机器证明定理
- **与 M42 的关系**：全补恒 0 定理的锚级（单对）推广——同一守恒律的两个代数表现

## 开放登记（更新）
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 五十八、动量双守恒恒等式 A 的 Lean 机器证明（2026-10-06，Phase 77 M43）

**新模块**：`MUFPFormalization/SingleMinusAnchorSum.lean`——lake build 通过（3048 jobs，零 sorry）。

**定理**（anchor_sum_zero）：
```
Σω = 0 ∧ Σωz = 0 ⇒ Σ_{j∈univ.erase k} ω_k ω_j (z_k − z_j) = 0（任何锚 k）
```

**证明链**（纯代数，三步）：
1. **线性展开**：Σ_{j≠k} ω_k ω_j (z_k−z_j) = ω_k [z_k Σ_{j≠k} ω_j − Σ_{j≠k} ω_j z_j]
   —— sum_congr + ring 逐项（ω_k ω_j (z_k−z_j) = ω_k(z_k ω_j − ω_j z_j)）、← Finset.mul_sum 提出 ω_k、sum_sub_distrib + ← mul_sum 提出 z_k
2. **erase 求和**：Σ_{j≠k} ω_j = −ω_k、Σ_{j≠k} ω_j z_j = −ω_k z_k
   —— Finset.sum_erase_add（mem_univ）+ hsum/hmom + linarith
3. **代入闭合**：ω_k [z_k(−ω_k) − (−ω_k z_k)] = 0（ring）

**技术要点**：`Finset.sum_erase_add`（s.erase a 求和 + f a = 全集求和）；congr 1 对 (A−B)=(C−D) 只生成 1 个子目标（余项 rfl 自动）——删除多余 rfl。

**意义**：
- "任何粒子锚定单对括号和恒 0"——动量守恒的**逐粒子**代数表现——机器证明定理
- 与 M42 全补恒 0 定理构成守恒律的两个表现（锚级单对 vs 块级全补）——后续"跨区间单对 = 相邻单对线性组合"（恒等式 B——s61 展开）可在同一结构上形式化
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)

p3 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
s3 = io.open(p3, "r", encoding="utf-8").read()
s3 = s3.replace("**版本**：v0.73（2026-10-06）", "**版本**：v0.74（2026-10-06）", 1)
old = "| v0.73 | 2026-10-06 | **全补恒 0 定理 Lean 机器证明（Phase 77 M42）**"
add3 = "| v0.74 | 2026-10-06 | **动量双守恒恒等式 A Lean 机器证明（Phase 77 M43）**：锚 k 单对括号和恒 0——守恒律的逐粒子代数表现。 |\n| v0.73 | 2026-10-06 | **全补恒 0 定理 Lean 机器证明（Phase 77 M42）**"
assert old in s3
s3 = s3.replace(old, add3, 1)
io.open(p3, "w", encoding="utf-8").write(s3)
print("M43 落盘完成（roadmap + 笔记 §58 + Paper 58 v0.74）")
