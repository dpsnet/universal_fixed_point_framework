import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import MUFPFormalization.RecCategory
import MUFPFormalization.NoiseCategory
import MUFPFormalization.CoherenceToBranching
import MUFPFormalization.LorentzSignatureBridge
import MUFPFormalization.SignatureTimeBridge
import MUFPFormalization.RecActiveSignatureBridge

set_option maxHeartbeats 500000

namespace MUFPF.NoiseSignatureBridge

universe u

open MUFPF.CoherenceToBranching
open MUFPF.LorentzSignatureBridge
open MUFPF.RecActiveSignatureBridge

/-
## 噪声系统 ↔ Signature 桥接层

### 双层结构

**层 A（可机检，零新矩阵，引用已验证模块）**：
  Diss（§17.3）的 contraction 机制 ↔ silent_factor（§10b）

  核心洞察：
    Diss : Rec × NoiseData → Σ-Rec 仅在 contraction i < 1 时产生分量
    silent_factor_c1 d < 1, silent_factor_c2 d < 1, silent_factor_c3 d = 1
    → Diss 溶解的只是"已经静默"的 c₁, c₂
    → c₃（时间分支，权重 = 1）不在 Diss 图像里
    → Σ-Rec 噪声层只包含静默分支，不破坏 c₃ 的时间唯一性

**层 B（可机检，M₈ 字面量）**：
  Cl(3,1) 时间+空间 4 维 → M₈ 提升版本，验证 γ₀² = -I₈, γ₁-₃² = +I₈

### 诚实边界

本文件确认"兼容性"：Diss 噪声层与 c₃ 时间唯一性共存，
M₈ Clifford 代数继承原始 Cl(3,1)。不声称 contraction 数值 = silent_factor 物理值。
--/

/-
## 层 A：Diss ↔ SilentFactor 桥接

Diss : Rec × NoiseData → Σ-Rec 的 contraction 条件与 silent_factor 权重的天然对应：
  - contraction < 1 → Diss 产生分量（被噪声溶解）
  - silent_factor_c1 d < 1, silent_factor_c2 d < 1 → 这两个是静默分支
  - silent_factor_c3 d = 1 → 唯一不被溶解的时间分支
--/

/-- **Diss 静默噪声数据**：将 silent_factor 权重编码为 NoiseData.contractions。

    设计：
      i = 0 → contraction = silent_factor_c1 d（< 1，双重静默）
      i = 1 → contraction = silent_factor_c2 d（< 1，单重静默）
      i = 2 → contraction = 1（c₃ 权重 = 1 → Diss 不产生分量）
      i ≥ 3 → contraction = 0（空分量，不产生）
    
    物理诠释：
      Diss 对 c₁ 和 c₂ 的 contraction < 1 → 这两个是可被噪声溶解的静默分支
      Diss 对 c₃ 的 contraction = 1 → c₃ 不被溶解，保持唯一时间方向
--/
noncomputable def dissSilentNoiseData (d : ℝ) (_hd : 0 < d) : NoiseData where
  scales := fun _ => Real.exp d
  steps := fun _ R => R  -- 恒等局部变换（Diss 不检查 steps 的具体值）
  contractions := fun i =>
    match i with
    | 0 => silent_factor_c1 d     -- e⁻³·e⁻ᵈ < 1
    | 1 => silent_factor_c2 d     -- e⁻ᵈ < 1
    | 2 => 1                       -- c₃ = 1，Diss 不产生分量
    | _ => 0                       -- 其他分量空

/-
### 引理 1：SilentFactor 的基本性质（CoherenceToBranching 已机检）
--/

/-- silent_factor_c1 d < 1（双重静默）。 -/
lemma c1_lt_one (d : ℝ) (hd : 0 < d) : silent_factor_c1 d < 1 :=
  (c3_unique_silent_factor d hd).1

/-- silent_factor_c2 d < 1（单重静默）。 -/
lemma c2_lt_one (d : ℝ) (hd : 0 < d) : silent_factor_c2 d < 1 :=
  (c3_unique_silent_factor d hd).2.1

/-- silent_factor_c3 d = 1（唯一不静默）。 -/
lemma c3_eq_one (d : ℝ) (_hd : 0 < d) : silent_factor_c3 d = 1 := rfl

/-
### 引理 2：Diss 产生 c₁, c₂ 分量（contraction < 1）
--/

/-- Diss 在索引 0 产生分量（contraction 0 < 1 → some ...）。 -/
theorem dissProducesC1 (R : RecObj) (d : ℝ) (hd : 0 < d) :
    (dissFunctor R (dissSilentNoiseData d hd)).components 0 ≠ none := by
  have hc : (dissSilentNoiseData d hd).contractions 0 < 1 := c1_lt_one d hd
  have hsome : (dissFunctor R (dissSilentNoiseData d hd)).components 0 = some
      { T := R.T, fin := R.fin, dec := R.dec, step := R.step } := by
    simp [dissFunctor, hc]
  rw [hsome]
  simp

/-- Diss 在索引 1 产生分量（contraction 1 < 1 → some ...）。 -/
theorem dissProducesC2 (R : RecObj) (d : ℝ) (hd : 0 < d) :
    (dissFunctor R (dissSilentNoiseData d hd)).components 1 ≠ none := by
  have hc : (dissSilentNoiseData d hd).contractions 1 < 1 := c2_lt_one d hd
  have hsome : (dissFunctor R (dissSilentNoiseData d hd)).components 1 = some
      { T := R.T, fin := R.fin, dec := R.dec, step := R.step } := by
    simp [dissFunctor, hc]
  rw [hsome]
  simp

/-- **Diss 不在索引 2 产生分量**（c₃ contraction = 1，Diss 条件是 < 1 → none）。
    这正是"时间分支不被 Diss 溶解"的 Lean 化。 -/
theorem dissDoesNotProduceC3 (R : RecObj) (d : ℝ) (hd : 0 < d) :
    (dissFunctor R (dissSilentNoiseData d hd)).components 2 = none := by
  have h1 : (dissSilentNoiseData d hd).contractions 2 = 1 := by
    rfl
  have hneg : ¬ (dissSilentNoiseData d hd).contractions 2 < 1 := by
    rw [h1]; norm_num
  -- dissFunctor.components 2 是 dependent if（dite），条件是 contractions 2 < 1
  -- dite_eq_right 将 ¬condition 转为 dite = else-branch (none)
  exact dite_eq_right hneg

/-
### 核心定理：Diss 只溶解静默分支，不破坏 c₃ 时间唯一性

Diss 噪声层 + c₃ 时间唯一性 + γ₀² = -I₄ 的三层联合兼容性。
--/

/-- **Diss-签名兼容性定理**（层 A 核心结论）。

    Diss 噪声层的三个性质联合：
    1. Diss 产生 c₁, c₂ 分量（静默分支被溶解）
    2. Diss 不产生 c₃ 分量（时间分支不被溶解）
    3. c₃ = 1 + γ₀² = -I₄（时间唯一性 + Cl(3,1) 签名）

    结论：Diss 噪声系统只影响已静默的分支，c₃ 保持唯一时间方向，
    Cl(3,1) Clifford 签名的物理诠释不受噪声破坏。 -/
theorem diss_produces_silent_only :
    ∀ (R : RecObj) (d : ℝ) (hd : 0 < d),
      (dissFunctor R (dissSilentNoiseData d hd)).components 0 ≠ none ∧
      (dissFunctor R (dissSilentNoiseData d hd)).components 1 ≠ none ∧
      (dissFunctor R (dissSilentNoiseData d hd)).components 2 = none := by
  intro R d hd
  exact ⟨dissProducesC1 R d hd, dissProducesC2 R d hd, dissDoesNotProduceC3 R d hd⟩

theorem diss_signature_compatible :
    ∀ (R : RecObj) (d : ℝ) (hd : 0 < d),
      ((dissFunctor R (dissSilentNoiseData d hd)).components 0 ≠ none) ∧
      ((dissFunctor R (dissSilentNoiseData d hd)).components 1 ≠ none) ∧
      ((dissFunctor R (dissSilentNoiseData d hd)).components 2 = none) ∧
      silent_factor_c3 d = 1 ∧
      (gamma0 * gamma0 = -1 • I4) := by
  intro R d hd
  have h := diss_produces_silent_only R d hd
  exact ⟨h.1, h.2.1, h.2.2, c3_silent_factor_exists d, gamma0_sq_neg_I4⟩

/-
## 层 A 总结

层 A 完成了 Diss 噪声系统 + Signature 时间分支 + Cl(3,1) 代数签名的
**三层联合兼容性确认**。所有 theorem 引用已验证模块，无 sorry，无新矩阵。
--/

/-
## 层 B：M₈ 版本的 γ₀-₃ 提升

将 Cl(3,1) 的 4×4 矩阵提升到 8×8。验证 γ₀² = -I₈, γ₁-₃² = +I₈。
策略：与 LorentzSignatureBridge M₄ 完全相同——字面量 + funext + fin_cases + simp。
--/

/-- 8×8 单位矩阵。 -/
def I8 : Matrix (Fin 8) (Fin 8) ℂ := (1 : Matrix (Fin 8) (Fin 8) ℂ)

/-- γ₀ 的 M₈ 提升（左上角 + 右下角两个 γ₀ 块）。 -/
noncomputable def gamma0_8 : Matrix (Fin 8) (Fin 8) ℂ :=
  !![0, 0, 1, 0, 0, 0, 0, 0;
     0, 0, 0, 1, 0, 0, 0, 0;
     -1, 0, 0, 0, 0, 0, 0, 0;
     0, -1, 0, 0, 0, 0, 0, 0;
     0, 0, 0, 0, 0, 0, 1, 0;
     0, 0, 0, 0, 0, 0, 0, 1;
     0, 0, 0, 0, -1, 0, 0, 0;
     0, 0, 0, 0, 0, -1, 0, 0]

/-- γ₁ 的 M₈ 提升（左上角 + 右下角两个 γ₁ 块）。 -/
noncomputable def gamma1_8 : Matrix (Fin 8) (Fin 8) ℂ :=
  !![0, 1, 0, 0, 0, 0, 0, 0;
     1, 0, 0, 0, 0, 0, 0, 0;
     0, 0, 0, -1, 0, 0, 0, 0;
     0, 0, -1, 0, 0, 0, 0, 0;
     0, 0, 0, 0, 0, 1, 0, 0;
     0, 0, 0, 0, 1, 0, 0, 0;
     0, 0, 0, 0, 0, 0, 0, -1;
     0, 0, 0, 0, 0, 0, -1, 0]

/-- γ₂ 的 M₈ 提升（左上角 + 右下角两个 γ₂ 块，含 i）。 -/
noncomputable def gamma2_8 : Matrix (Fin 8) (Fin 8) ℂ :=
  !![0, -Complex.I, 0, 0, 0, 0, 0, 0;
     Complex.I, 0, 0, 0, 0, 0, 0, 0;
     0, 0, 0, Complex.I, 0, 0, 0, 0;
     0, 0, -Complex.I, 0, 0, 0, 0, 0;
     0, 0, 0, 0, 0, -Complex.I, 0, 0;
     0, 0, 0, 0, Complex.I, 0, 0, 0;
     0, 0, 0, 0, 0, 0, 0, Complex.I;
     0, 0, 0, 0, 0, 0, -Complex.I, 0]

/-- γ₃ 的 M₈ 提升（左上角 + 右下角两个 γ₃ 块）。 -/
noncomputable def gamma3_8 : Matrix (Fin 8) (Fin 8) ℂ :=
  !![1, 0, 0, 0, 0, 0, 0, 0;
     0, -1, 0, 0, 0, 0, 0, 0;
     0, 0, -1, 0, 0, 0, 0, 0;
     0, 0, 0, 1, 0, 0, 0, 0;
     0, 0, 0, 0, 1, 0, 0, 0;
     0, 0, 0, 0, 0, -1, 0, 0;
     0, 0, 0, 0, 0, 0, -1, 0;
     0, 0, 0, 0, 0, 0, 0, 1]

/-
### 8×8 Lorentz 度量

原始 η₄ = diag(-1, +1, +1, +1)。这里扩展到 diag(-1,+1,+1,+1,-1,-1,-1,-1)（假设内部 4 维是时间型）。
内部签名的最终选择需要 γ₄-₇ 验证——当前选择作为保守方案。
--/

noncomputable def etaExt : Matrix (Fin 8) (Fin 8) ℝ :=
  !![-1, 0, 0, 0, 0, 0, 0, 0;
     0, 1, 0, 0, 0, 0, 0, 0;
     0, 0, 1, 0, 0, 0, 0, 0;
     0, 0, 0, 1, 0, 0, 0, 0;
     0, 0, 0, 0, -1, 0, 0, 0;
     0, 0, 0, 0, 0, -1, 0, 0;
     0, 0, 0, 0, 0, 0, -1, 0;
     0, 0, 0, 0, 0, 0, 0, -1]

/-
### 平方值验证

策略与 LorentzSignatureBridge M₄ 完全相同：
  unfold + funext + fin_cases 8 + fin_cases 8 + simp
  64 个 entry，simp 自动闭合。
--/

theorem gamma0_8_sq_neg_I8 : gamma0_8 * gamma0_8 = -1 • I8 := by
  unfold gamma0_8 I8
  funext i j
  fin_cases i <;> fin_cases j <;> simp

theorem gamma1_8_sq_pos_I8 : gamma1_8 * gamma1_8 = 1 • I8 := by
  unfold gamma1_8 I8
  funext i j
  fin_cases i <;> fin_cases j <;> simp

theorem gamma2_8_sq_pos_I8 : gamma2_8 * gamma2_8 = 1 • I8 := by
  unfold gamma2_8 I8
  funext i j
  fin_cases i <;> fin_cases j <;> simp

theorem gamma3_8_sq_pos_I8 : gamma3_8 * gamma3_8 = 1 • I8 := by
  unfold gamma3_8 I8
  funext i j
  fin_cases i <;> fin_cases j <;> simp

/-
### M₈ γ₄-₆：内部静默空间（2×2 Pauli 四重复制尺度，Cl(3,0) 子代数）

三个全正定生成元 γ₄²=γ₅²=γ₆²=+I₈，两两反对易。

构造策略：γ₄-₆ 都是 2×2 Pauli 形式的四重复制——diag(σᵢ, σᵢ, σᵢ, σᵢ) 的 8×8 版本。
这种"内部空间正定复制"与 γ₀-₃ 的 Cl(3,1) 手征结构（γ₀ off-diagonal）形成对照。

结构性事实：2×2 矩阵空间只张成 3 个两两反对易方向（σ₁,σ₂,σ₃），
不存在与三者同时反对易的非零 8×8 块矩阵——故该尺度最多 3 个生成元，
第 4 个生成元（γ₇）只能落在 4×4 Dirac 两重复制尺度（见下文 γ₇ = γ⁵）。
--/

noncomputable def gamma4_8 : Matrix (Fin 8) (Fin 8) ℂ :=
  !![0, 1, 0, 0, 0, 0, 0, 0;
     1, 0, 0, 0, 0, 0, 0, 0;
     0, 0, 0, 1, 0, 0, 0, 0;
     0, 0, 1, 0, 0, 0, 0, 0;
     0, 0, 0, 0, 0, 1, 0, 0;
     0, 0, 0, 0, 1, 0, 0, 0;
     0, 0, 0, 0, 0, 0, 0, 1;
     0, 0, 0, 0, 0, 0, 1, 0]

noncomputable def gamma5_8 : Matrix (Fin 8) (Fin 8) ℂ :=
  !![0, -Complex.I, 0, 0, 0, 0, 0, 0;
     Complex.I, 0, 0, 0, 0, 0, 0, 0;
     0, 0, 0, -Complex.I, 0, 0, 0, 0;
     0, 0, Complex.I, 0, 0, 0, 0, 0;
     0, 0, 0, 0, 0, -Complex.I, 0, 0;
     0, 0, 0, 0, Complex.I, 0, 0, 0;
     0, 0, 0, 0, 0, 0, 0, -Complex.I;
     0, 0, 0, 0, 0, 0, Complex.I, 0]

noncomputable def gamma6_8 : Matrix (Fin 8) (Fin 8) ℂ :=
  !![1, 0, 0, 0, 0, 0, 0, 0;
     0, -1, 0, 0, 0, 0, 0, 0;
     0, 0, 1, 0, 0, 0, 0, 0;
     0, 0, 0, -1, 0, 0, 0, 0;
     0, 0, 0, 0, 1, 0, 0, 0;
     0, 0, 0, 0, 0, -1, 0, 0;
     0, 0, 0, 0, 0, 0, 1, 0;
     0, 0, 0, 0, 0, 0, 0, -1]

/-- gamma7_8：手征算符 γ⁵ 的 4×4 两重复制。

    gamma7_8 = diag(γ⁵, γ⁵)（γ⁵ = iγ⁰γ¹γ²γ³ = [[0,I],[I,0]]），
    与 gamma0-3 同尺度。{γ⁰..γ³, γ⁷=γ⁵} 构成 Cl(4,1) 手征扩张。
    与 gamma4-6（Pauli 四重复制尺度）跨尺度不反对易（B1）。 -/
noncomputable def gamma7_8 : Matrix (Fin 8) (Fin 8) ℂ :=
  !![0, 0, 1, 0, 0, 0, 0, 0;
     0, 0, 0, 1, 0, 0, 0, 0;
     1, 0, 0, 0, 0, 0, 0, 0;
     0, 1, 0, 0, 0, 0, 0, 0;
     0, 0, 0, 0, 0, 0, 1, 0;
     0, 0, 0, 0, 0, 0, 0, 1;
     0, 0, 0, 0, 1, 0, 0, 0;
     0, 0, 0, 0, 0, 1, 0, 0]

/-
### M₈ γ₄-₇ 平方值验证

γ₄-₆（Pauli 尺度）全正定 +I₈；γ₇ = γ⁵（Dirac 尺度手征算符）亦正定 +I₈。
tactic 模式：与 γ₀-₃ 完全相同。
--/

theorem gamma4_8_sq_pos_I8 : gamma4_8 * gamma4_8 = 1 • I8 := by
  unfold gamma4_8 I8
  funext i j
  fin_cases i <;> fin_cases j <;> simp

theorem gamma5_8_sq_pos_I8 : gamma5_8 * gamma5_8 = 1 • I8 := by
  unfold gamma5_8 I8
  funext i j
  fin_cases i <;> fin_cases j <;> simp

theorem gamma6_8_sq_pos_I8 : gamma6_8 * gamma6_8 = 1 • I8 := by
  unfold gamma6_8 I8
  funext i j
  fin_cases i <;> fin_cases j <;> simp

theorem gamma7_8_sq_pos_I8 : gamma7_8 * gamma7_8 = 1 • I8 := by
  unfold gamma7_8 I8
  funext i j
  fin_cases i <;> fin_cases j <;> simp

/-
### M₈ γ₁ 与 γ₄ 的 block 级对照

γ₁（Cl(3,1) 子代数，Dirac 两重复制尺度）= diag(σₓ, -σₓ)
γ₄（Cl(3,0) 子代数，Pauli 四重复制尺度）= diag(σₓ, σₓ, σₓ, σₓ)

关键区别：γ₁ 是手征（bot block 有 - 号，sign flip 是 Cl(3,1) signature 的根源），
γ₄ 是纯正定复制（无 - 号）。这正是 Cl(3,1)（Lorentz 时空）vs Cl(3,0)（静默维度）
两种尺度的 block 级结构标志——也是跨尺度反对易结构性失败的 block 来源（B1）。
--/

theorem m8_gamma1_vs_gamma4_block_signature :
    (gamma1_8 0 0 = 0) ∧ (gamma1_8 0 1 = 1) ∧  -- top block σₓ
    (gamma1_8 2 2 = 0) ∧ (gamma1_8 2 3 = -1) ∧ -- bot block -σₓ
    (gamma4_8 0 0 = 0) ∧ (gamma4_8 0 1 = 1) ∧  -- 第一块 σₓ
    (gamma4_8 6 6 = 0) ∧ (gamma4_8 6 7 = 1) := by -- 第四块 σₓ（无 - 号！）
  simp [gamma1_8, gamma4_8]

/-
### M₈ 四种签名的精确归属

  gamma0-3 → Cl(3,1)（4D Lorentz 时空，signature (−,+,+,+)）
  gamma0-3 + gamma7 → Cl(4,1)（手征扩张，signature (−,+,+,+,+)，物理诠释：手征对称性）
  gamma4-6 → Cl(3,0)（静默维度，signature (+,+,+)）
  gamma4-7 全正定联合（theorem `m8_gamma4to7_all_positive_sq`）→ 跨两个尺度的正定平方确认（非单一 Clifford 代数）
--/

theorem m8_cl31_signature_verified :
    (gamma0_8 * gamma0_8 = -1 • I8) ∧
    (gamma1_8 * gamma1_8 = 1 • I8) ∧
    (gamma2_8 * gamma2_8 = 1 • I8) ∧
    (gamma3_8 * gamma3_8 = 1 • I8) := by
  exact ⟨gamma0_8_sq_neg_I8, gamma1_8_sq_pos_I8,
          gamma2_8_sq_pos_I8, gamma3_8_sq_pos_I8⟩

/-- m8_gamma4to7_all_positive_sq：gamma4-7 四个平方值全正定。

    跨两个尺度：gamma4-6 是 Pauli 四重复制尺度（Cl(3,0) 子代数），
    gamma7 是 Dirac 两重复制尺度（Cl(4,1) 手征扩张子代数），
    非单一 Clifford 代数。 -/
theorem m8_gamma4to7_all_positive_sq :
    (gamma4_8 * gamma4_8 = 1 • I8) ∧
    (gamma5_8 * gamma5_8 = 1 • I8) ∧
    (gamma6_8 * gamma6_8 = 1 • I8) ∧
    (gamma7_8 * gamma7_8 = 1 • I8) := by
  exact ⟨gamma4_8_sq_pos_I8, gamma5_8_sq_pos_I8,
          gamma6_8_sq_pos_I8, gamma7_8_sq_pos_I8⟩

/-
### M₈ 反对易表（已验证部分）

M₈ 的 gamma 有两种 block 尺度：
  gamma0-3_8 = diag(gamma_i4, gamma_i4)  —— 4×4 Dirac 的两重复制（Cl(3,1)）
  gamma7_8   = diag(γ⁵, γ⁵)               —— 4×4 手征算符的两重复制（同 Dirac 尺度）
  gamma4-6_8 = diag(σ, σ, σ, σ)          —— 2×2 Pauli 的四重复制（Cl(3,0)）

**同一尺度内部反对易已机检**：
  - gamma0-3_8 之间（C(4,2)=6 对）全部反对易
  - gamma7_8 = γ⁵ 与 gamma0-3_8（4 对）全部反对易
    → {γ⁰,γ¹,γ²,γ³,γ⁷=γ⁵} = 5 个两两反对易生成元，签名 (−,+,+,+,+)
    → Cl(3,1) 的手征扩张 Cl(4,1) 复实现（8×8）
  - gamma4-6_8 之间（C(3,2)=3 对）全部反对易

**跨尺度（Dirac 尺度 {0-3,7} × Pauli 尺度 {4-6}）不自动反对易**——
两种 block 结构不同，乘法后 block 位置混合，反对易结构性失败。诚实边界 B1 保留。
--/

-- Cl(3,1) 子代数内部（gamma0-3，6 对）
theorem anticomm_gamma08_gamma18 : gamma0_8 * gamma1_8 + gamma1_8 * gamma0_8 = 0 := by
  unfold gamma0_8 gamma1_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma08_gamma28 : gamma0_8 * gamma2_8 + gamma2_8 * gamma0_8 = 0 := by
  unfold gamma0_8 gamma2_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma08_gamma38 : gamma0_8 * gamma3_8 + gamma3_8 * gamma0_8 = 0 := by
  unfold gamma0_8 gamma3_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma18_gamma28 : gamma1_8 * gamma2_8 + gamma2_8 * gamma1_8 = 0 := by
  unfold gamma1_8 gamma2_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma18_gamma38 : gamma1_8 * gamma3_8 + gamma3_8 * gamma1_8 = 0 := by
  unfold gamma1_8 gamma3_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma28_gamma38 : gamma2_8 * gamma3_8 + gamma3_8 * gamma2_8 = 0 := by
  unfold gamma2_8 gamma3_8; funext i j; fin_cases i <;> fin_cases j <;> simp

-- Cl(3,0) 子代数内部（gamma4-6，3 对）
theorem anticomm_gamma48_gamma58 : gamma4_8 * gamma5_8 + gamma5_8 * gamma4_8 = 0 := by
  unfold gamma4_8 gamma5_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma48_gamma68 : gamma4_8 * gamma6_8 + gamma6_8 * gamma4_8 = 0 := by
  unfold gamma4_8 gamma6_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma58_gamma68 : gamma5_8 * gamma6_8 + gamma6_8 * gamma5_8 = 0 := by
  unfold gamma5_8 gamma6_8; funext i j; fin_cases i <;> fin_cases j <;> simp

-- 手征扩张（gamma7 = γ⁵ × gamma0-3，4 对）—— B2 消除：gamma7 已是纯 Clifford 生成元
theorem anticomm_gamma08_gamma78 : gamma0_8 * gamma7_8 + gamma7_8 * gamma0_8 = 0 := by
  unfold gamma0_8 gamma7_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma18_gamma78 : gamma1_8 * gamma7_8 + gamma7_8 * gamma1_8 = 0 := by
  unfold gamma1_8 gamma7_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma28_gamma78 : gamma2_8 * gamma7_8 + gamma7_8 * gamma2_8 = 0 := by
  unfold gamma2_8 gamma7_8; funext i j; fin_cases i <;> fin_cases j <;> simp
theorem anticomm_gamma38_gamma78 : gamma3_8 * gamma7_8 + gamma7_8 * gamma3_8 = 0 := by
  unfold gamma3_8 gamma7_8; funext i j; fin_cases i <;> fin_cases j <;> simp

/-
### M₈ Clifford 代数联合图景（平方 + 同尺度反对易）

γ₀-₇ 8 个生成元的平方值签名：
  γ₀² = -I₈（时间型）
  γ₁-₇² = +I₈（7 个正定）

同尺度反对易（已机检 13 对）：
  Dirac 尺度 {γ⁰,γ¹,γ²,γ³,γ⁷=γ⁵}：C(5,2)=10 对全部反对易
    → Cl(3,1) 手征扩张 Cl(4,1) 复实现（签名 (−,+,+,+,+)）
  Pauli 尺度 {γ⁴,γ⁵P,γ⁶}（gamma4-6_8）：3 对全部反对易
    → Cl(3,0) 子代数

诚实边界：跨尺度反对易结构性失败（B1 保留）；
  γ₁-₇ 的 block 复制布局是否对应某种物理分裂结构——物理诠释跳跃，不做数学声明。
--/

/-
### M₈ Clifford 代数总结（已验证）

- 13 对 gamma 同尺度两两反对易（全部已机检）：
  Dirac 尺度 10 对（gamma0-3 间 6 对 + gamma7=γ⁵ × gamma0-3 4 对）
  Pauli 尺度 3 对（gamma4-6 间）
- 8 个平方值（1 负定 γ₀ + 7 正定 γ₁-₇）
- Cl(3,1) 签名：gamma0_8²=-I₈, gamma1-3_8²=+I₈
- 手征扩张：gamma7_8 = γ⁵ 两重复制，与 gamma0-3 全反对易（Cl(4,1) 复实现）

诚实边界：超大型 And 链（>4 项）触发 universe 泄漏——
采用"单独 theorem + 少量小分组"的工程策略。
数学内容完整，只是不做超大型合取组装。
--/

end MUFPF.NoiseSignatureBridge
