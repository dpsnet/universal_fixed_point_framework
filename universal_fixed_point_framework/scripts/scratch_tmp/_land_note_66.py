# -*- coding: utf-8 -*-
"""补笔记 §六十六：恒等式 B（锚对分解）Lean 机器证明落盘"""
import io

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 六十六、恒等式 B（锚对分解）的 Lean 机器证明（2026-10-06，Phase 77 M44 补记）

**补记**：§五十八末尾承诺的"恒等式 B——s61 展开"落盘在此完成（此前漏记——现补齐）。

**恒等式 B（锚对分解）**：对任意锚 k、任意 p≠k：$P[k][p] = -\\sum_{j\\neq k,p} P[k][j]$——即**跨区间单对 = 其余锚对之和的负值**。

**模块**：`MUFPFormalization/SingleMinusAnchorPair.lean`——theorem `anchor_pair_decomp`——lake build 通过（3049 jobs，零 sorry）。

**技术要点**：
- import `MUFPFormalization.SingleMinusAnchorSum` 必须在文件顶部（前缀 `MUFPFormalization.`）
- 复用恒等式 A 的线性展开（anchorSum_lin lemma）——P[k][p] 从和式中分离
- Finset.mem_erase 的 univ 成员用 mem_univ p 处理
- 证法：由恒等式 A（Σ_{j≠k}P[k][j]=0）移项——P[k][p] = −Σ_{j≠k,p}P[k][j]——ring 闭合

**意义（M37 的 s61 机制内核机器化）**：
- n=6 A6 显式公式 32 项 20 因子——仅 s61（[λ_6,λ_1] 环向单对）不在 35 相邻区间
- 级联展开 s61 = −Σ_{j=2..5}s_{6j}（数值恒等 10000×6 全过）——**现由 Lean 零 sorry 机器证明**
- **动量双守恒括号恒等式三件套闭环**：全补块恒 0（M42/§五十七）+ 恒等式 A 锚和恒 0（M43/§五十八）+ 恒等式 B 锚对分解（本篇）——**守恒约束的代数化完整机器化**

**链条意义**：动量守恒（物理输入）→ 括号恒等式（代数）→ 判据完备（组合）——三件套 Lean 证明完成——**判据映射完备性的内生推导链的代数环节零 sorry 形式化**。
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)
print("笔记 §六十六 恒等式 B 落盘完成")
