/-
  CouplingDecompAudit.lean — R-l：耦合块的 4 个自由参数逐一对上框架内已有对象
  =====================================================================================

## 问题

§25 判定：分层载体的耦合块 `B`（`2×2` 实矩阵）有 4 个自由参数，且不由两侧数据约束
⟹ 桥变自由参数。§27 又只条件式钉住了 `B_计数`。于是剩下一个具体问题：

> `B` 的 4 个实参数，能不能**逐个**对上框架里已经存在的对象？
> 若 4 个都对上，则「自由参数」是误判；若只有一部分对上，缺口就在剩下的那几个上。

## 判据与答案

用库内已有的四个基元把任意 `2×2` 实矩阵分解：

```
  M = α·1 + β·F + γ·S + δ·A
```

| 参数 | 读出 | 基元 | 框架内已有对象 |
|---|---|---|---|
| `α` | `(M₀₀+M₁₁)/2` | `1`（单位） | 单位元 / 迹的一半 |
| `β` | `(M₀₀−M₁₁)/2` | `F = diag(1,−1)` | 分谱差（与 `Δλ_min` 同类型） |
| `γ` | `(M₀₁+M₁₀)/2` | `S = !![0,1;1,0]` | 对称非对角（层间对称混合） |
| `δ` | `(M₀₁−M₁₀)/2` | `A = !![0,1;−1,0]` | 反对称生成元（`rotGen`，`SO(2)`） |

**4 个参数确实逐个对上了已有基元**（判①）。但「对上基元」不等于「被框架钉住」：

- **判②**：框架自带的对称化 `groupAverage` 恰好把 `β·F + γ·S` 整块抹掉
  （对称无迹 2 维入核），4 参数降到 2。
- **判③**：剩下的两个性质**相反**——
  - `α` 是**相似不变量**（迹的一半），基无关的「数值型」参数，**大小自由、无判据**；
  - `δ` **逃出相似类**（同一相似类里 `δ` 可取不同值），基依赖的「结构型」参数，
    其**方向**被 `A`（`rotGen`）钉住，**大小仍自由**。

## 净结果

逐一对上的结论不是「耦合块被钉住」，而是 §24 的结论在耦合块内部**原样复现**：

> 4 个参数 → 2 个（平均）→ 方向有身份（`A`）+ 大小无判据（`δ`），另有一个基无关自由标量（`α`）。
> **耦合块能同时持有「数值型」与「结构型」两样东西，但两者的「大小」都没有判据。**

这与 §24.5 的「数值与结构从不同时被同一载体传递」不矛盾：§24 说的是**取自两侧数据**的
数值与结构；这里 `α`、`δ` 的数值都不取自两侧，而是耦合块自身的自由参数。
故本批把 §24 的判词精确化为：**传递失败的原因是「大小无判据」，不是「载体不能同时持有两类量」。**

## 诚实边界

1. 分解用库内基元 `1`、`F`（`Isotropy`）、`S`（`offDiag`）、`A`（`rotGen`）；
   完备性由重建恒等式给出（`decomp_reconstruct`），**未单独证明四基元线性独立**
   （那需要线性代数层，本模块不引入）。
2. `δ` 的非不变性只给**一个具体见证**（`S` 在 `T = !![1,1;0,1]` 下的共轭），
   不做「任意可逆 `T`」的全称刻画。
3. `β ↔ Δλ_min` 只是**类型相同**（都是分谱差），不声称 `β = Δλ_min`；
   `α ↔ 1/15` 之类更无据，明确不做。
4. 不新增常数、不新增公设。
-/

import MUFPFormalization.IntertwinerRepairAudit
import Mathlib.Tactic

namespace MUFPF.CouplingDecompAudit

open MUFPF.Isotropy (groupAverage F)
open MUFPF.IntertwinerRepairAudit (rotGen offDiag groupAverage_general_form
  trace_eq_of_invertible_intertwine_real)

/-! ## 判①：4 参数分解完备 —— 每个参数都对应库内一个已有基元 -/

/-- ★★ **判①**：任意 `2×2` 实矩阵分解为 `α·1 + β·F + γ·S + δ·A`，
    四个系数由四个读出公式给出（`α` 迹半、`β` 对角差半、`γ` 非对角和半、`δ` 非对角差半）。 -/
theorem decomp_reconstruct (M : Matrix (Fin 2) (Fin 2) ℝ) :
    M = ((M 0 0 + M 1 1) / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ)
      + ((M 0 0 - M 1 1) / 2) • F
      + ((M 0 1 + M 1 0) / 2) • offDiag
      + ((M 0 1 - M 1 0) / 2) • rotGen := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [F, offDiag, rotGen] <;> ring

/-! ## 判②：框架自带平均把对称无迹的 2 维整块抹掉 —— 4 参数降到 2 -/

/-- ★★ **判②**：`groupAverage (β·F + γ·S) = 0`。
    对称无迹 2 维（`F`、`S` 张成）被框架自己的对称化整块投影掉。 -/
theorem avg_kills_symmetric_traceless (β γ : ℝ) :
    groupAverage (β • F + γ • offDiag) = 0 := by
  rw [groupAverage_general_form]
  simp [F, offDiag]

/-- 判② 的镜像：平均后只剩 `α`（单位）与 `δ`（生成元）两个方向。 -/
theorem avg_keeps_alpha_delta (M : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage M = ((M 0 0 + M 1 1) / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ)
      + ((M 0 1 - M 1 0) / 2) • rotGen :=
  groupAverage_general_form M

/-! ## 判③：剩下的两个参数性质相反 —— 一个相似不变、一个逃出相似类 -/

/-- `trace M = M₀₀ + M₁₁`（`2×2` 口径）。 -/
theorem trace_fin_two_eq (M : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.trace M = M 0 0 + M 1 1 := by
  simp [Matrix.trace, Fin.sum_univ_two]

/-- ★★ **判③-a**：`α` **相似不变**——可逆交织下 `(M₀₀+M₁₁)/2` 不变。
    故 `α` 是基无关的「数值型」参数：在相似类上取常值，不可能携带基的信息。 -/
theorem alpha_survives_similarity {M M' T U : Matrix (Fin 2) (Fin 2) ℝ}
    (hTU : T * U = 1) (hUT : U * T = 1) (h : T * M' = M * T) :
    (M' 0 0 + M' 1 1) / 2 = (M 0 0 + M 1 1) / 2 := by
  have htr := trace_eq_of_invertible_intertwine_real (A := M) (B := M') hTU hUT h
  rw [trace_fin_two_eq M, trace_fin_two_eq M'] at htr
  linarith

/-- ★★ **判③-b**：`δ` **逃出相似类**——存在可逆交织对 `(M, M')` 使
    `(M₀₁−M₁₀)/2 ≠ (M'₀₁−M'₁₀)/2`。见证：`M' = S`、`M = !![1,0;1,−1]`、
    `T = !![1,1;0,1]`、`U = !![1,−1;0,1]`（`T·U = U·T = 1`，`T·S = M·T`），
    `δ(M′) = 0` 而 `δ(M) = −1/2`。

    ⇒ `δ` 是基依赖的「结构型」参数：方向由 `A`（`rotGen`）给出，大小由基的选择决定。 -/
theorem delta_escapes_similarity :
    ∃ (M M' T U : Matrix (Fin 2) (Fin 2) ℝ),
      T * U = 1 ∧ U * T = 1 ∧ T * M' = M * T ∧
        (M 0 1 - M 1 0) / 2 ≠ (M' 0 1 - M' 1 0) / 2 := by
  refine ⟨!![(1 : ℝ), 0; 1, -1], offDiag, !![(1 : ℝ), 1; 0, 1],
    !![(1 : ℝ), -1; 0, 1], ?_, ?_, ?_, ?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two]
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two]
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two, offDiag]
  · norm_num [offDiag]

/-! ## 判④：汇总 -/

/-- **R-l 判决汇总**：
    ① 4 参数分解完备（系数由读出公式给出）；
    ② 框架自带平均抹掉 `β·F + γ·S` ⟹ 4 → 2（只剩 `α`、`δ`）；
    ③ `α` 相似不变（数值型，大小无判据）；`δ` 逃出相似类（结构型，方向有身份、大小无判据）；
    ④ 故「逐一对上」的净结果 = §24 结论在耦合块内部复现：两样都持有，大小都没判据。 -/
theorem coupling_decomp_verdict :
    (∀ M : Matrix (Fin 2) (Fin 2) ℝ,
        M = ((M 0 0 + M 1 1) / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ)
          + ((M 0 0 - M 1 1) / 2) • F
          + ((M 0 1 + M 1 0) / 2) • offDiag
          + ((M 0 1 - M 1 0) / 2) • rotGen) ∧
      (∀ β γ : ℝ, groupAverage (β • F + γ • offDiag) = 0) ∧
      (∀ M : Matrix (Fin 2) (Fin 2) ℝ,
        groupAverage M = ((M 0 0 + M 1 1) / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ)
          + ((M 0 1 - M 1 0) / 2) • rotGen) ∧
      (∃ (M M' T U : Matrix (Fin 2) (Fin 2) ℝ),
        T * U = 1 ∧ U * T = 1 ∧ T * M' = M * T ∧
          (M 0 1 - M 1 0) / 2 ≠ (M' 0 1 - M' 1 0) / 2) :=
  ⟨decomp_reconstruct, avg_kills_symmetric_traceless, avg_keeps_alpha_delta,
    delta_escapes_similarity⟩

end MUFPF.CouplingDecompAudit
