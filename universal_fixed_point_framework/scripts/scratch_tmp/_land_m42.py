# -*- coding: utf-8 -*-
"""落盘 M42：roadmap + 笔记 §57 + Paper 58 v0.73（Lean 全补恒 0 闭合）"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase77_n11_crossset_greedy.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 开放登记（更新）"
add = """## M42 ✅ 全补恒 0 定理 Lean 机器证明（2026-10-06，零 sorry）

- **新模块** `MUFPFormalization.SingleMinusFullCompZero`——`lake build` 通过（3048 jobs，零 sorry）
- **定理 fullcomp_zero**：A∪B = univ、A∩B = ∅、Σω = 0、Σωz = 0 ⇒ bracket [A,B] = Σ_{a∈A}Σ_{b∈B} ωa ωb (za−zb) = 0
- **证明结构**（纯代数）：双求和线性展开 [A,B] = (Σ_A ωz)(Σ_B ω) − (Σ_A ω)(Σ_B ωz) → 补集求和（Finset.sum_union + linarith）→ ring
- **先证伪再证明闭环**：M38 数值 102000 检验 + M39 阈值化 50000 检验 → Lean 形式证明——"全补块恒 0"从采样级定理升级为机器证明定理
- **对 Paper 58 的意义**：谱维数修正（44 含 7 全补伪影）获得严格数学内核——"守恒的零模式"不是浮点现象而是理论事实

## 开放登记（更新）
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 五十七、全补恒 0 定理的 Lean 机器证明（2026-10-06，Phase 77 M42）

**新模块**：`MUFPFormalization/SingleMinusFullCompZero.lean`——lake build 通过（3048 jobs，零 sorry）。

**定理**（fullcomp_zero）：
```
A∪B = univ ∧ A∩B = ∅ ∧ Σω = 0 ∧ Σωz = 0
  ⇒ bracket [A,B] = Σ_{a∈A} Σ_{b∈B} ω_a ω_b (z_a − z_b) = 0
```

**证明链**（纯代数，三步）：
1. **双求和线性展开**：bracket = (Σ_A ωz)(Σ_B ω) − (Σ_A ω)(Σ_B ωz)
   —— 逐项 ring 展开 (za−zb)、sum_sub_distrib 拆分、Finset.mul_sum/sum_mul 提出常数
2. **补集求和**：Σ_B ω = −Σ_A ω、Σ_B ωz = −Σ_A ωz
   —— Finset.sum_union（disjoint）+ hcover（A∪B = univ）+ hsum/hmom（Σuniv = 0）+ linarith
3. **代入闭合**：(Σ_A ωz)(−Σ_A ω) − (Σ_A ω)(−(Σ_A ωz)) = 0（ring）

**技术要点（环境）**：
- `∑ x ∈ s`（∈ 而非 in）是 Lean 4 Finset 求和语法；BigOperators scope 需 `open scoped BigOperators`
- 结合律坑：`ω a * ω b * z b` ≠ `ω a * (ω b * z b)`——rw [← Finset.mul_sum] 前需 funext+ring 重组
- Mathlib 部分构建（BigOperators.Finset olean 缺失）——用 Mathlib.Data.Real.Basic + Mathlib.Tactic 足够（Finset 求和是 core）

**意义**：
- "全补块恒 0"从采样级定理（M38/M39 数值）升级为**机器证明定理**——谱维数修正的数学内核
- 动量守恒在括号代数中的直接表现——"守恒的零模式"是理论事实而非浮点现象
- 为后续"双守恒括号恒等式（Σ_{j≠k}P[k][j]=0）"的形式化提供模板（同样代数结构）
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)

p3 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
s3 = io.open(p3, "r", encoding="utf-8").read()
s3 = s3.replace("**版本**：v0.72（2026-10-06）", "**版本**：v0.73（2026-10-06）", 1)
old = "| v0.72 | 2026-10-06 | **n=10 全空间完备性实测（Phase 77 M41c）**"
add3 = "| v0.73 | 2026-10-06 | **全补恒 0 定理 Lean 机器证明（Phase 77 M42）**：新模块 SingleMinusFullCompZero 零 sorry——全补块恒 0 = 机器证明定理（非浮点现象）。 |\n| v0.72 | 2026-10-06 | **n=10 全空间完备性实测（Phase 77 M41c）**"
assert old in s3
s3 = s3.replace(old, add3, 1)
io.open(p3, "w", encoding="utf-8").write(s3)
print("M42 落盘完成（roadmap + 笔记 §57 + Paper 58 v0.73）")
