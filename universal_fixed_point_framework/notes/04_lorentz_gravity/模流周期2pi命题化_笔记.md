# 模流周期 2π 命题化 —— 笔记（P1-B）

> 状态：**完成（2026-10-23）**｜Lean 内核：`TwoPiPeriodicity.lean` 全绿（`lake env lean` exit 0、`lake build MUFPFormalization.TwoPiPeriodicity` 2006/2006 jobs、零 sorry）
> 上游：推进建议 §3.1 风险记账 1（"2π 可能是单位约定而非同伦不变量"）；路线图 §1.2（"Clifford ⇒ 4π ⇒ 2π" 候选链）
> 下游：P2-B（de Sitter 符号论证）与 BW 对接命题

---

## 1. 本页裁决的问题

风险记账 1 问：**2π 是单位约定，还是由理论结构决定的量？**
推进建议 P1-B 的验收项是：把"周期闭合 ⇒ T = 2π"变成可证命题，不允许"2π 是定义"的循环。

**裁决结论（解析层）**：2π 在此不是单位约定——它是**复指数沿虚轴的最小正周期**，
该事实在 mathlib 中是**定理**（exp 由级数定义，其周期性、π 的取值均非公设），
因此"周期闭合 ⇒ 周期族 = 2πℤ"是一条可机检的解析事实，不是循环论证。

**裁决边界**：本裁决只覆盖"exp 层的 2π"。路线图 §1.2 把 2π 进一步绑定到
Bott/Clifford 周期（"Clifford ⇒ 4π ⇒ 2π"）——**该环节不被定理 1/2 支撑**（见 §4）。

---

## 2. Lean 内核：定理陈述（`TwoPiPeriodicity.lean`）

### 定理 1（周期族闭式）`exp_period_closed_form`

```
{T : ℝ} → 0 < T →
  ((∀ z : ℂ, exp (z + T·i) = exp z) ↔ ∃ n : ℕ, 1 ≤ n ∧ T = 2π·n)
```

即：**正周期全部形如 2π·n（n ≥ 1）**。周期闭合 ⇒ T ∈ 2πℤ⁺，无例外。

证明骨架（ℤ 系数 → ℕ 提升）：
1. `hperiod 0` ⇒ `exp(T·i) = 1`（周期点在 0 处的取值）；
2. `Complex.exp_eq_one_iff` ⇒ `T·i = n·(2π·i)`（n : ℤ）；
3. 取虚部（`congrArg Complex.im` + `Complex.mul_im`）⇒ `T = n·2π`（ℝ 层）；
4. `T > 0` + `2π > 0` ⇒ `n > 0`（`field_simp` + `div_pos`）；
5. `n.toNat` + `Int.toNat_of_nonneg` ⇒ 提升为 `∃ m ≥ 1, T = 2π·m`。

### 定理 2（最小正周期）`exp_minimal_period_two_pi`

```
Function.Periodic exp (2π·i) ∧
  (∀ {T}, 0 < T → (∀ z, exp (z + T·i) = exp z) → 2π ≤ T)
```

即：**2π·i 是 exp 的周期，且任何正周期 ≥ 2π**——2π 确为最小正周期。
由定理 1 直接给出（周期族 2π·n 的最小成员 = n=1 ⇒ 2π）。

### 引理（辅助）

- `exp_two_pi_eq_one`：`exp(2π·i) = 1`（`Complex.exp_periodic` 在 0 处取值，simp 直接闭合——证明 exp 周期性的是 mathlib 的级数展开，非本文件假设）；
- `of_exp_eq_one_coeff`：`T·i = n·(2π·i)` ⇒ `T = n·2π`（虚部提取，`Complex.mul_im` 等规则）。

### 验证记录

| 检查项 | 结果 |
| --- | --- |
| `lake env lean src\MUFPFormalization\TwoPiPeriodicity.lean` | exit 0，零 error 零 warning |
| `lake build MUFPFormalization.TwoPiPeriodicity` | 2006/2006 jobs 成功 |
| grep `sorry\|axiom\|admit` | 仅注释命中（"本文件不含 sorry"），**零 sorry** |

---

## 3. 物理对接命题（BW 定理 → 模流闭合）

**命题（本页登记，尚未 Lean 化）**：
> BW 定理给出模算子形如 Δ = e^{−2πM}（2310.12185 式 34：K_Ω = −2π M_0j 的谱表述）。
> 则模流 t ↦ Δ^{it} 的**闭合周期** T 满足
> Δ^{i(t+T)} = Δ^{it} ⇔ e^{−2πi M T} = 1 ⇔ **M·T ∈ ℤ**（M 的谱以整数为单位）。
> 结合定理 1（解析层 T ∈ 2πℤ⁺）：模流最小闭合周期 = 2π，且与 M 谱整数化条件
> **T = 2π/n（n ∈ ℤ⁺ 为使 n·M 为整数的谱整数化因子）** 一致——即
> **"模流闭合周期 = 2π"与"模 Hamilton 量 M 谱整数化"是同一事实的两面**。

这正是链条上"2π 单位"问题的物理面答案：2π 作为模流周期不是外加约定，
而是模算子谱结构（Δ = e^{−2πM} 中 2π 来自模 Hamilton 量的归一化约定 + exp 周期唯一性）的推论。

---

## 4. 诚实边界（必须随文引用）

1. **Bott/Clifford 周期 8 与 2π 无数值关联**。8 = 实 Clifford 代数周期（C𝓁(3,0) 相关），
   2π = 复指数最小正周期；两者在定理 1/2 中不产生任何数值联系。
   路线图 §1.2 的 "Clifford ⇒ 4π ⇒ 2π" 环节**不被本定理支撑**，维持"候选"地位。
2. **本内核只形式化 exp 层**。模流 Δ^{it} 的 T 唯一性依赖 BW 定理（Δ = e^{−2πM}）的
   谱表述——BW 定理本身是外部输入（2310 式 34），不在本文件证明范围内。
3. **2π 的来源分层**：exp 层唯一性（本文件，机检）+ 模流层对接（§3，登记级）+
   Bott 层绑定（路线图，候选级）。后两层的证明状态不得与本文件混为一谈。
4. 定理 1 的 (→) 方向用到 `Complex.exp_eq_one_iff`（全周期版，在
   `Mathlib.Analysis.SpecialFunctions.Complex.Log`）；该引理本身是 mathlib 已证明定理。

---

## 5. 登记与后续

- 推进建议文档：P1-B 行 → 已完成（本笔记路径）。
- generative_chain_map changelog：本条（2π 命题化，Template 资产：周期闭合 ⇒ 2π 的
  机器可检内核，可用作 B 系模板"荷生成/周期闭合"的 Lean 骨架）。
- RESEARCH_STATE 头部：本条。
- 后续候选（未开工）：
  - **P2-B**（de Sitter 符号论证，按"逐一推进"顺序下一项）；
  - Lean 追加候选：Rindler 线性权重 c=0（与 KappaAudit 同模板，登记于
    Rindler区_kappa重算.md §6.4）；
  - §3 对接命题的 Lean 化（需先固化为纯 ℝ/ℂ 陈述，依赖 BW 谱表述的外部输入层）。
