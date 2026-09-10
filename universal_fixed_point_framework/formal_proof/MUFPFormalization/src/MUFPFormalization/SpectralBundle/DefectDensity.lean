-- ============================================================
-- MUFPF SpectralBundle sub-module
-- §26. 缺陷体密度桥：从缺陷计数到 Ω 分配
-- Phase 69.8（Ω 值第一性原理推导的离散桥接层）
-- ============================================================
--
-- 研究背景（Paper LII §10.3 开放问题 1）：
--   Ω_m / Ω_Λ 的数值当前在数值模拟中作为输入参数
--   （phase69_large_scale_structure.py 中 0.3/0.7）。
--   本文建立从缺陷计数统计到 Ω 分配的离散桥接定理：
--
--   区域划分（粗粒化）→ 区域缺陷计数 → 束缚/弥散分割 → Ω 分配比
--
--   桥接链四段（对应研究笔记 phase69_omega_first_principles.md）：
--   1. G_N 闭式定标缺陷单元质量（Paper XXXI，已闭环）
--   2. 缺陷计数区域分解（本文 sum_regionDefectCount_eq_total）
--   3. 束缚/弥散阈值分割（本文 bound_plus_diffuse_eq_total）
--   4. 临界密度定标得绝对 Ω 值（接口 criticalDensity，
--      需连续极限 Paper XXXIV + Hubble 参数，定量部分留待对接）
--
-- 数值验证：numerical/phase69b_omega_from_defects.py
--   FoF 聚类生成束缚比例 f_b = 0.313（σ8=1.2, b=0.10, q=0.20），
--   与观测 Ω_m/(Ω_m+Ω_Λ) = 0.315 一致（误差 < 1%）。

import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Disjoint
import Mathlib.Data.Real.Basic
import MUFPFormalization.SpectralBundle.Cosmology

namespace MUFPF

-- ============================================================
-- §26.1 区域划分与缺陷计数
-- ============================================================

/-! ### 区域划分

    对有限事件系统 T 的一个划分（partition）：
    - 覆盖性：每个事件属于某区域
    - 不相交性：不同区域不交

    物理含义：粗粒化的"分辨率"——
    区域 = 宏观尺度的一个"像素"（对应 CoarseGrainingRegion，LSS §23.1）。
    与 LSS 的区别：LSS 的划分建立在 CausalStructure 上，
    本文的建立在任意有限类型上，使缺陷计数（RecObj 概念）可直接桥接。 -/

structure RegionPartition (T : Type) [Fintype T] [DecidableEq T] where
  /-- 区域集合（每个区域是事件的有限子集） -/
  regions : Finset (Finset T)
  /-- 覆盖性：每个事件属于至少一个区域 -/
  covers : ∀ x : T, ∃ r ∈ regions, x ∈ r
  /-- 不相交性：不同区域不交 -/
  disjoint : ∀ r₁ ∈ regions, ∀ r₂ ∈ regions, r₁ ≠ r₂ → Disjoint r₁ r₂

/-- 区域缺陷计数：区域 R 中的缺陷事件数。
    物理含义：粗粒化像素的缺陷密度分子。
    缺陷集合 `defects` 对应 RecObj 中非不动点事件的集合
    （defectMeasure 的载体集合版本）。 -/
def regionDefectCount {T : Type} [Fintype T] [DecidableEq T]
    (defects r : Finset T) : ℕ :=
  (r ∩ defects).card

/-- **缺陷计数粗粒化守恒**（核心定理）。
    区域分解后的缺陷计数之和 = 总缺陷数。

    物理含义：粗粒化不创造或消灭缺陷——
    总缺陷量在区域分割下严格守恒。
    这是 `coarse_graining_preserves_total_events`（LSS §23.1）
    的缺陷计数版本，是离散 → 连续密度桥的第一块基石。

    证明策略：
    1. ⋃ (Rᵢ ∩ D) = D（由覆盖性）
    2. (Rᵢ ∩ D) 两两不交（由区域不相交性）
    3. Finset.card_biUnion 求和 -/
theorem sum_regionDefectCount_eq_total {T : Type} [Fintype T] [DecidableEq T]
    (p : RegionPartition T) (defects : Finset T) :
    Finset.sum p.regions (fun r => regionDefectCount defects r) = defects.card := by
  have h_union : Finset.biUnion p.regions (fun r => r ∩ defects) = defects := by
    ext x
    simp only [Finset.mem_biUnion, Finset.mem_inter]
    constructor
    · rintro ⟨r, _hr, _hxr, hxd⟩
      exact hxd
    · intro hxd
      obtain ⟨r, hr, hxr⟩ := p.covers x
      exact ⟨r, hr, hxr, hxd⟩
  -- (Rᵢ ∩ D) 两两不交：由区域不相交性（用 disjoint_left 逐元素验证）
  have h_disj : (p.regions : Set (Finset T)).PairwiseDisjoint (fun r => r ∩ defects) := by
    intro r₁ hr₁ r₂ hr₂ hne
    have hd := p.disjoint r₁ hr₁ r₂ hr₂ hne
    rw [Finset.disjoint_left] at hd
    -- onFun 形式先换型回 Disjoint，rw 才能匹配
    show Disjoint (r₁ ∩ defects) (r₂ ∩ defects)
    rw [Finset.disjoint_left]
    intro a ha hap
    exact hd (Finset.mem_inter.1 ha).1 (Finset.mem_inter.1 hap).1
  have h_card : (Finset.biUnion p.regions (fun r => r ∩ defects)).card =
      Finset.sum p.regions (fun r => (r ∩ defects).card) :=
    Finset.card_biUnion h_disj
  calc Finset.sum p.regions (fun r => regionDefectCount defects r)
      = (Finset.biUnion p.regions (fun r => r ∩ defects)).card := h_card.symm
    _ = defects.card := by rw [h_union]

/-- 区域缺陷密度：单位事件的缺陷率 ρ_d(R) = |R ∩ D| / |R| ∈ [0, 1]。
    物理含义：粗粒化像素的缺陷密度（离散版本）。
    连续极限下收敛到缺陷体密度场（Paper XXXIV 对接后严格化）。 -/
noncomputable def regionDefectDensity {T : Type} [Fintype T] [DecidableEq T]
    (defects r : Finset T) : ℝ :=
  ((r ∩ defects).card : ℝ) / (r.card : ℝ)

-- ============================================================
-- §26.2 束缚/弥散阈值分割
-- ============================================================

/-! ### 束缚/弥散分割

    核心思想：Ω 分配比由缺陷的聚类状态决定——
    - 束缚态缺陷（暗物质）：处于 K > K_c 引力束缚结构中的缺陷
      （数值实现：FoF 聚类成员，phase69b 脚本）
    - 弥散态缺陷（暗能量）：未束缚的均匀背景缺陷

    离散形式化：以阈值 a/b 判定区域是否为束缚区域
    （区域缺陷率 ≥ a/b ⟺ 束缚），所有判定在 ℕ 上可判定。 -/

/-- 束缚区域判定：区域缺陷率 ≥ a/b。
    即 |R ∩ D|·b ≥ |R|·a（避免实数除法，全程可判定）。 -/
def isBoundRegion {T : Type} [Fintype T] [DecidableEq T]
    (defects : Finset T) (a b : ℕ) (r : Finset T) : Prop :=
  (r ∩ defects).card * b ≥ r.card * a

/-- 束缚判定在 ℕ 上可判定（实例供 if-then-else 使用）。 -/
instance isBoundRegion.decidable {T : Type} [Fintype T] [DecidableEq T]
    (defects : Finset T) (a b : ℕ) (r : Finset T) :
    Decidable (isBoundRegion defects a b r) := by
  unfold isBoundRegion
  infer_instance

/-- 束缚态缺陷总量：所有束缚区域中的缺陷计数之和。 -/
def boundDefects {T : Type} [Fintype T] [DecidableEq T]
    (p : RegionPartition T) (defects : Finset T) (a b : ℕ) : ℕ :=
  Finset.sum p.regions
    (fun r => if isBoundRegion defects a b r then (r ∩ defects).card else 0)

/-- 弥散态缺陷总量：所有非束缚区域中的缺陷计数之和。 -/
def diffuseDefects {T : Type} [Fintype T] [DecidableEq T]
    (p : RegionPartition T) (defects : Finset T) (a b : ℕ) : ℕ :=
  Finset.sum p.regions
    (fun r => if ¬isBoundRegion defects a b r then (r ∩ defects).card else 0)

/-- 束缚缺陷不超过总缺陷（分割的单调性）。 -/
theorem boundDefects_le_total {T : Type} [Fintype T] [DecidableEq T]
    (p : RegionPartition T) (defects : Finset T) (a b : ℕ) :
    boundDefects p defects a b ≤ defects.card := by
  rw [← sum_regionDefectCount_eq_total p defects]
  apply Finset.sum_le_sum
  intro r _hr
  -- 逐项：束缚贡献 ≤ 区域缺陷计数（if-分支取走或取 0）
  unfold regionDefectCount
  split_ifs <;> simp

/-- **分割守恒律**（核心定理）：束缚 + 弥散 = 总缺陷数。
    物理含义：Ω_m + Ω_Λ = Ω_defect（Paper LII 定理 2.3）
    在区域分割层的实现——无论阈值 (a, b) 如何选取，
    两相分配之和恒等于总缺陷量。

    这是 Paper LII `darkMatter_plus_darkEnergy_eq_total` 的
    微观统计基础：CosmicDefectDistribution 的 bound/diffuse
    计数正是本定理左右两端在宇宙学尺度的读数。 -/
theorem bound_plus_diffuse_eq_total {T : Type} [Fintype T] [DecidableEq T]
    (p : RegionPartition T) (defects : Finset T) (a b : ℕ) :
    boundDefects p defects a b + diffuseDefects p defects a b = defects.card := by
  rw [← sum_regionDefectCount_eq_total p defects]
  -- 先展开为 Finset.sum 的语法形式，rw ← sum_add_distrib 才能匹配
  unfold boundDefects diffuseDefects
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro r _hr
  unfold regionDefectCount
  split_ifs <;> omega

-- ============================================================
-- §26.3 Ω 分配比
-- ============================================================

/-! ### Ω 分配比

    归一化分配比（不依赖临界密度定标）：
    - Ω_m 份额 = 束缚缺陷 / 总缺陷
    - Ω_Λ 份额 = 弥散缺陷 / 总缺陷

    数值验证（phase69b_omega_from_defects.py）：
    σ8 = 1.2, b = 0.10, q = 0.20 时 f_b = 0.313，
    与观测 Ω_m/(Ω_m+Ω_Λ) = 0.315 一致（误差 < 1%）。
    分配比是聚类动力学的输出，而非输入参数。 -/

/-- Ω_m 份额：束缚缺陷占缺陷总量的比例。 -/
noncomputable def OmegaMatterShare {T : Type} [Fintype T] [DecidableEq T]
    (p : RegionPartition T) (defects : Finset T) (a b : ℕ) : ℝ :=
  (boundDefects p defects a b : ℝ) / (defects.card : ℝ)

/-- Ω_Λ 份额：弥散缺陷占缺陷总量的比例。 -/
noncomputable def OmegaLambdaShare {T : Type} [Fintype T] [DecidableEq T]
    (p : RegionPartition T) (defects : Finset T) (a b : ℕ) : ℝ :=
  (diffuseDefects p defects a b : ℝ) / (defects.card : ℝ)

/-- **分配比归一化**：Ω_m 份额 + Ω_Λ 份额 = 1（总缺陷 > 0）。
    物理含义：Ω_m + Ω_Λ = Ω_defect = 1（归一化框架内）。
    这是宇宙学巧合问题（Why now?）分析的起点：
    份额比 Ω_m/Ω_Λ 由聚类阈值与结构形成史决定。 -/
theorem omega_shares_add_to_one {T : Type} [Fintype T] [DecidableEq T]
    (p : RegionPartition T) (defects : Finset T) (a b : ℕ)
    (h : defects.Nonempty) :
    OmegaMatterShare p defects a b + OmegaLambdaShare p defects a b = 1 := by
  have hcard : (0 : ℝ) < (defects.card : ℝ) := by
    exact_mod_cast Finset.card_pos.mpr h
  have hsum : (boundDefects p defects a b : ℝ) + (diffuseDefects p defects a b : ℝ)
      = (defects.card : ℝ) := by
    exact_mod_cast bound_plus_diffuse_eq_total p defects a b
  calc OmegaMatterShare p defects a b + OmegaLambdaShare p defects a b
      = ((boundDefects p defects a b : ℝ) + (diffuseDefects p defects a b : ℝ))
        / (defects.card : ℝ) := by
        unfold OmegaMatterShare OmegaLambdaShare
        rw [add_div]
    _ = (defects.card : ℝ) / (defects.card : ℝ) := by rw [hsum]
    _ = 1 := div_self (ne_of_gt hcard)

/-- 分配比对定标常数的不变性：
    物理定标（单个缺陷质量 m、体积单元 v）以公共因子 c 缩放
    分子分母时，份额比不变。
    物理含义：Ω_m/Ω_Λ 是计数比，与绝对单位选择无关——
    这正是"分配比可先验计算、绝对 Ω 后验定标"的数学表达。 -/
theorem omega_share_calibration_independent (c : ℝ) (hc : c ≠ 0)
    (B D : ℕ) (hBD : (B : ℝ) + D ≠ 0) :
    (c * (B : ℝ)) / (c * ((B : ℝ) + D)) = (B : ℝ) / ((B : ℝ) + D) := by
  field_simp [hc, hBD]

-- ============================================================
-- §26.4 与 CosmicDefectDistribution 对接 + 临界密度接口
-- ============================================================

/-- 区域分割统计 → CosmicDefectDistribution 的桥接构造。
    物理含义：Paper LII 的宇宙学缺陷分布结构
    可由区域分割的束缚/弥散计数直接填充。 -/
def toCosmicDefectDistribution (bound diffuse : ℕ) : CosmicDefectDistribution where
  bound_defect := bound
  diffuse_defect := diffuse
  bound_nonneg := Nat.zero_le bound
  diffuse_nonneg := Nat.zero_le diffuse
  total_defect_eq := trivial

/-- 桥接一致性：分割统计填入 CosmicDefectDistribution 后，
    暗物质量 = 束缚缺陷计数（定义即得）。 -/
theorem toCosmic_darkMatter_eq_bound (bound diffuse : ℕ) :
    (toCosmicDefectDistribution bound diffuse).darkMatter = bound := rfl

/-- 桥接一致性：分割统计填入 CosmicDefectDistribution 后，
    暗能量量 = 弥散缺陷计数（定义即得）。 -/
theorem toCosmic_darkEnergy_eq_diffuse (bound diffuse : ℕ) :
    (toCosmicDefectDistribution bound diffuse).darkEnergy = diffuse := rfl

/-- 桥接守恒：分割统计满足 Paper LII 的统一恒等式
    Ω_m + Ω_Λ = Ω_defect（由 Cosmology.lean §20 的定理保证）。 -/
theorem toCosmic_partition_conserves (bound diffuse : ℕ) :
    (toCosmicDefectDistribution bound diffuse).darkMatter
      + (toCosmicDefectDistribution bound diffuse).darkEnergy
      = (toCosmicDefectDistribution bound diffuse).total :=
  darkMatter_plus_darkEnergy_eq_total _

/-- 临界密度（连续极限定标接口）：ρ_crit = 3H²/(8πG_N)。
    物理含义：
    - G_N 由闭式 G_N = 18(2+√3)·Δλ_min² 给出（Paper XXXI，已闭环）
    - H 由谱流 → FLRW 尺度因子给出（推导阶段 11，Paper LI）
    - 绝对 Ω 值 = 物理缺陷密度 / ρ_crit
    定量对接依赖连续极限（Paper XXXIV），此处仅定义接口。
    分配比（Ω_m/Ω_Λ）不依赖本定标（见 omega_share_calibration_independent）。 -/
noncomputable def criticalDensity (H G : ℝ) : ℝ :=
  3 * H ^ 2 / (8 * Real.pi * G)

end MUFPF
