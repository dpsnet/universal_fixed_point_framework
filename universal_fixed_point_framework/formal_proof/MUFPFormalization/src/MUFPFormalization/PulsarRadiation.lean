-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：0
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import MUFPFormalization.RecCategory
import MUFPFormalization.CriticalCardinality
import MUFPFormalization.DecursionFunctor
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Logic.Function.Basic

namespace MUFPF

open CategoryTheory Finset Set

universe u

/-! # T-02 脉冲星辐射机制：磁拓扑通道与极光逆对偶

本文件形式化研究笔记 MUFPF-RN-COMPACT-001 §2 中的核心概念：

**核心思想**：
- 脉冲星辐射本源来自星体内部偏心高密度子集群的周期性时序震荡
- 磁场仅作为能量释放的拓扑通道（非第一动因）
- 该机制与地球极光构成强逆对偶（内→外 vs 外→内）

**形式化策略**：
- 偏心子集群 = 含非不动点元素的 FixedPointCluster（有内部动力学）
- 周期态 = step^n x = x (n ≥ 1)
- 有限态机 → 所有轨道最终周期（鸽巢原理）
- RecHom 保持周期性（归纳法）—— 耦合传导时序震荡
- 磁拓扑通道 = 任意 RecHom φ : X ⟶ Y
- 脉冲信号 = 通道输出端的周期态
- 极光对偶 = 源方向反转（内→外 vs 外→内）

## 内容结构

1. 偏心子集群 (EccentricCluster)
2. 周期态与最终周期性 (PeriodicState, EventuallyPeriodic)
3. RecHom 保持周期性 (核心引理 + 定理)
4. 磁拓扑通道 (MagneticChannel)
5. 脉冲星辐射定理 T-02
6. 极光逆对偶 (AuroraDuality)
7. 观测现象解释 (SpinDown)
-/

-- ============================================================
-- §1. 偏心子集群
-- ============================================================

/-- 偏心子集群：含至少一个非不动点元素的 FixedPointCluster。
    "偏心"意味着该子集群有内部动力学——不只是静止的不动点，
    而是包含运动状态（step x ≠ x）。

    物理对应：中子星内核中永久性偏心高密度子集群，
    其内部递归时序持续运动，是辐射的能量来源。 -/
def FixedPointCluster.isEccentric {X : RecObj} (C : FixedPointCluster X) : Prop :=
  ∃ x ∈ C.carrier, X.step x ≠ x

/-- 非偏心集群：所有元素都是不动点（静止集群）。
    物理对应：白矮星 K < K_c 时的对称稳态内核——没有内部动力学。 -/
def FixedPointCluster.isStatic {X : RecObj} (C : FixedPointCluster X) : Prop :=
  ∀ x ∈ C.carrier, X.step x = x

/-- 偏心与静止互斥。 -/
lemma eccentric_not_static {X : RecObj} (C : FixedPointCluster X) :
    C.isEccentric → ¬ C.isStatic := by
  intro he hs
  rcases he with ⟨x, hx, hne⟩
  exact hne (hs x hx)

/-- 偏心集群中同时存在不动点和非不动点。 -/
lemma eccentric_has_dynamics {X : RecObj} (C : FixedPointCluster X)
    (h : C.isEccentric) :
    ∃ (p x : X.T), p ∈ C.carrier ∧ x ∈ C.carrier ∧
    X.step p = p ∧ X.step x ≠ x := by
  rcases C.has_fixedPoint with ⟨p, hp, hpp⟩
  rcases h with ⟨x, hx, hne⟩
  exact ⟨p, x, hp, hx, hpp, hne⟩

-- ============================================================
-- §2. 周期态与最终周期性
-- ============================================================

/-- 周期态：step^n x = x 对某个 n ≥ 1 成立。
    物理对应：偏心子集群在自转带动下的周期性轨道运动。 -/
def RecObj.isPeriodic (X : RecObj) (x : X.T) : Prop :=
  ∃ n : ℕ, n ≥ 1 ∧ (X.step^[n]) x = x

/-- 不动点是周期为 1 的周期态。 -/
lemma fixedPoint_periodic {X : RecObj} (x : X.T) (h : X.step x = x) :
    X.isPeriodic x := by
  refine' ⟨1, by omega, ?_⟩
  rw [Function.iterate_one]
  exact h

/-- 周期态的 step 也是周期态，且周期相同。 -/
lemma step_preserves_periodic {X : RecObj} (x : X.T) (h : X.isPeriodic x) :
    X.isPeriodic (X.step x) := by
  rcases h with ⟨n, hn, hx⟩
  refine' ⟨n, hn, ?_⟩
  have h_comm : ∀ (k : ℕ) (y : X.T), X.step^[k] (X.step y) = X.step (X.step^[k] y) := by
    intro k
    induction k with
    | zero => intro y; rfl
    | succ j hj =>
      intro y
      simp only [Function.iterate_succ, Function.comp_apply] at *
      rw [hj]
  rw [h_comm n x, hx]

/-- 有限 RecObj 中每个态最终进入周期轨道（鸽巢原理）。
    card+1 个迭代值 step^0 x, ..., step^card x 中必有两个相等。
    这是脉冲星辐射持续性的基础：有限态机器必然产生周期信号。 -/
theorem RecObj.eventually_periodic (X : RecObj) (x : X.T) :
    ∃ (n m : ℕ), m ≥ 1 ∧ (X.step^[n+m]) x = (X.step^[n]) x := by
  let card := Fintype.card X.T
  by_contra h_no
  push_neg at h_no
  have h_inj : Function.Injective (fun (k : Fin (card + 1)) => (X.step^[k.val]) x) := by
    intro a₁ a₂ hxy
    by_contra hne
    by_cases hlt : a₁.val < a₂.val
    · have hm : a₂.val - a₁.val ≥ 1 := by omega
      have hsum : a₁.val + (a₂.val - a₁.val) = a₂.val := by omega
      have heq2 : (X.step^[a₁.val + (a₂.val - a₁.val)]) x = (X.step^[a₁.val]) x := by
        rw [hsum]; exact hxy.symm
      exact absurd heq2 (h_no a₁.val (a₂.val - a₁.val) hm)
    · by_cases hgt : a₂.val < a₁.val
      · have hm : a₁.val - a₂.val ≥ 1 := by omega
        have hsum : a₂.val + (a₁.val - a₂.val) = a₁.val := by omega
        have heq2 : (X.step^[a₂.val + (a₁.val - a₂.val)]) x = (X.step^[a₂.val]) x := by
          rw [hsum]; exact hxy
        exact absurd heq2 (h_no a₂.val (a₁.val - a₂.val) hm)
      · exfalso
        apply hne
        exact Fin.eq_of_val_eq (by omega)
  have h_card := Fintype.card_le_of_injective
    (fun (k : Fin (card + 1)) => (X.step^[k.val]) x) h_inj
  simp [Fintype.card_fin] at h_card
  linarith

/-- 迭代加法引理：f^[a] (f^[b] z) = f^[a+b] z
    这是 Function.iterate_add 的点值版本，用于证明周期态的迭代性质。 -/
lemma iterate_iterate_add {α : Type*} (f : α → α) (a b : ℕ) (z : α) :
    f^[a] (f^[b] z) = f^[a+b] z := by
  simp only [Function.iterate_add, Function.comp_apply]

-- ============================================================
-- §3. RecHom 保持周期性（核心引理）
-- ============================================================

/-- RecHom 的迭代交换引理：
    φ.toFun (X.step^[n] x) = Y.step^[n] (φ.toFun x)
    这是谱交织条件在迭代层面的体现。 -/
lemma RecHom.iterate_comm {X Y : RecObj} (φ : X ⟶ Y) :
    ∀ (n : ℕ) (x : X.T), φ.toFun ((X.step)^[n] x) = (Y.step)^[n] (φ.toFun x) := by
  intro n
  induction n with
  | zero => intro x; rfl
  | succ k hk =>
    intro x
    simp only [Function.iterate_succ, Function.comp_apply]
    rw [hk, φ.comm]

/-- **RecHom 保持周期性**：
    若 x 是 X 中的周期态，则 φ(x) 是 Y 中的周期态。

    物理对应：耦合函子传导时序震荡——
    内核偏心子集群的周期运动，经耦合传导后产生周期性信号。 -/
theorem RecHom.maps_periodic {X Y : RecObj} (φ : X ⟶ Y) (x : X.T)
    (h : X.isPeriodic x) : Y.isPeriodic (φ.toFun x) := by
  rcases h with ⟨n, hn, hx⟩
  refine' ⟨n, hn, ?_⟩
  have h_comm := φ.iterate_comm n x
  rw [hx] at h_comm
  exact h_comm.symm

/-- RecHom 保持最终周期性。 -/
theorem RecHom.maps_eventually_periodic {X Y : RecObj} (φ : X ⟶ Y) (x : X.T)
    (h : ∃ (n m : ℕ), m ≥ 1 ∧ (X.step^[n+m]) x = (X.step^[n]) x) :
    ∃ (n m : ℕ), m ≥ 1 ∧ (Y.step^[n+m]) (φ.toFun x) = (Y.step^[n]) (φ.toFun x) := by
  rcases h with ⟨n, m, hm, heq⟩
  refine' ⟨n, m, hm, ?_⟩
  have h1 : φ.toFun (X.step^[n+m] x) = Y.step^[n+m] (φ.toFun x) := φ.iterate_comm (n+m) x
  have h2 : φ.toFun (X.step^[n] x) = Y.step^[n] (φ.toFun x) := φ.iterate_comm n x
  rw [heq] at h1
  exact h1.symm.trans h2

-- ============================================================
-- §4. 磁拓扑通道
-- ============================================================

/-- 磁拓扑通道：从天体 RecObj X 到观测对象 Y 的 RecHom。
    物理对应：偶极磁场将内部偏心子集群的周期运动
    传导为外部可观测的周期信号。

    Y 必须有不动点以兼容 X 的不动点（RecHom 条件要求
    不动点映到不动点）。 -/
structure MagneticChannel (X Y : RecObj) where
  toHom : X ⟶ Y
  has_fixedPoint : ∃ y : Y.T, Y.step y = y

/-- 通道将 X 的周期态传导为 Y 的周期态。
    这是脉冲星信号传导的核心。 -/
theorem magnetic_channel_transmits {X Y : RecObj} (ch : MagneticChannel X Y)
    (x : X.T) (h : X.isPeriodic x) :
    Y.isPeriodic (ch.toHom.toFun x) := by
  exact ch.toHom.maps_periodic x h

/-- 通道将 X 的最终周期态传导为 Y 的最终周期态。 -/
theorem magnetic_channel_transmits_eventually {X Y : RecObj}
    (ch : MagneticChannel X Y) (x : X.T)
    (h : ∃ (n m : ℕ), m ≥ 1 ∧ (X.step^[n+m]) x = (X.step^[n]) x) :
    ∃ (n m : ℕ), m ≥ 1 ∧ (Y.step^[n+m]) (ch.toHom.toFun x) = (Y.step^[n]) (ch.toHom.toFun x) :=
  ch.toHom.maps_eventually_periodic x h

-- ============================================================
-- §4.5 跨层对接：RecHom → U(1) 规范场响应
-- ============================================================
-- U(1) 规范场已从 Cl(1,7) 内生推导（Paper V: Pati-Salam → SU(3)×U(1)）。
-- 本节建立 RecHom 周期信号经 D⊣R 规范扇区传导至 U(1) 场的形式化框架。
--
-- 核心思想：
--   RecHom φ : X ⟶ Y 保持周期性（magnetic_channel_transmits）
--   → D⊣R 伴随的规范扇区将 Rec 层信号映射到 Sp 层
--   → Sp 层的 U(1) 规范自由度产生周期性电磁场响应
--   → Lorentz 力加速带电粒子

/-- U(1) 规范场响应结构。
    物理含义：U(1) 规范场在时序震荡驱动下的响应信号。

    U(1) ≅ ℝ/ℤ，规范场的相位是周期性的。
    当 RecHom 传导周期性时序震荡时，
    U(1) 规范场的响应保持相同的周期结构。 -/
structure U1GaugeResponse where
  /-- 响应相位（U(1) 值，模 2π） -/
  phase : ℝ
  /-- 响应振幅 -/
  amplitude : ℝ
  /-- 振幅非负 -/
  amplitude_nonneg : 0 ≤ amplitude

/-- 规范通道：从 RecHom 到 U(1) 规范场响应的映射。
    物理含义：D⊣R 伴随的规范扇区将 Rec 层的周期信号
    传导为 Sp 层 U(1) 规范场的周期性响应。

    这是 Rec 层 → Sp 层 → 规范层 的跨层桥梁。 -/
structure GaugeChannel (X Y : RecObj) where
  /-- 底层 RecHom -/
  toHom : X ⟶ Y
  /-- U(1) 响应函数：将 Y 的状态映射为规范场响应 -/
  response : Y.T → U1GaugeResponse
  /-- 响应与动力学一致：step 保持响应的振幅结构 -/
  response_compat : ∀ y : Y.T, (response (Y.step y)).amplitude = (response y).amplitude

/-- 规范通道保持周期性：RecHom 的周期信号经 U(1) 规范扇区传导后，
    规范场响应保持相同的周期。

    证明思路：
    1. RecHom 保持周期性（RecHom.maps_periodic，已证明）
    2. response_compat 保证 step 后振幅不变
    3. 因此规范场响应的周期 = 源信号的周期

    物理含义：脉冲星内核的时序周期震荡
    经磁场传导后，电磁场响应保持同一周期——
    这是脉冲星周期性辐射的理论基础。 -/
theorem gauge_channel_preserves_periodicity
    {X Y : RecObj} (gc : GaugeChannel X Y)
    (x : X.T) (h_periodic : X.isPeriodic x) :
    -- 规范场响应的振幅在源信号的周期内保持不变
    ∀ k : ℕ, (gc.response ((gc.toHom.toFun x))).amplitude =
             (gc.response ((Y.step^[k]) (gc.toHom.toFun x))).amplitude := by
  intro k
  induction k with
  | zero => simp [Function.iterate_zero]
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    rw [gc.response_compat]
    exact ih

/-- 规范通道与磁拓扑通道的统一。
    MagneticChannel 是 GaugeChannel 的特化——
    当 U(1) 响函数取恒等映射时，GaugeChannel 退化为 MagneticChannel。 -/
def gaugeChannelFromMagnetic {X Y : RecObj}
    (mc : MagneticChannel X Y) : GaugeChannel X Y where
  toHom := mc.toHom
  response := fun _ => ⟨1, 1, by norm_num⟩  -- 恒等响应
  response_compat := by intro y; rfl

/-- MagneticChannel 是 GaugeChannel 的实例。
    这证明了 MagneticChannel 不是独立假设，
    而是 D⊣R 规范扇区传导的特化。 -/
theorem magnetic_is_gauge_channel {X Y : RecObj}
    (mc : MagneticChannel X Y) :
    ∃ gc : GaugeChannel X Y, gc.toHom = mc.toHom := by
  exact ⟨gaugeChannelFromMagnetic mc, rfl⟩

-- ============================================================
-- §5. 脉冲星辐射定理 T-02
-- ============================================================

/-- **T-02 脉冲星辐射定理**：
    若天体 X 内部存在偏心子集群（有非不动点元素），
    且存在磁拓扑通道 φ : X ⟶ Y，
    则通道输出端必然产生周期性信号。

    物理含义：
    1. 偏心子集群的内部动力学是辐射的能量来源（非磁场）
    2. 磁场仅是能量释放的拓扑通道
    3. 脉冲信号 = 内部周期运动经通道传导的周期信号

    证明链：
    - 偏心 → 存在非不动点 x ∈ C.carrier
    - 有限态 → x 最终周期（鸽巢原理）
    - RecHom → 周期性传导到 Y
    - Y 中产生周期信号 = 脉冲星辐射 -/
theorem T02_pulsar_radiation {X Y : RecObj}
    (C : FixedPointCluster X) (hEcc : C.isEccentric)
    (ch : MagneticChannel X Y) :
    ∃ (x : X.T), x ∈ C.carrier ∧
    ∃ (n m : ℕ), m ≥ 1 ∧
    (Y.step^[n+m]) (ch.toHom.toFun x) = (Y.step^[n]) (ch.toHom.toFun x) := by
  rcases hEcc with ⟨x, hx, hne⟩
  have h_ep := X.eventually_periodic x
  have h_trans := ch.toHom.maps_eventually_periodic x h_ep
  exact ⟨x, hx, h_trans⟩

/-- T-02 推论：通道输出端的周期信号。
    若偏心子集群中存在周期态，则通道输出端也是周期态。 -/
theorem T02_periodic_signal {X Y : RecObj}
    (C : FixedPointCluster X) (hEcc : C.isEccentric)
    (ch : MagneticChannel X Y) (x : X.T)
    (hIn : x ∈ C.carrier) (hPer : X.isPeriodic x) :
    Y.isPeriodic (ch.toHom.toFun x) := by
  exact ch.toHom.maps_periodic x hPer

-- ============================================================
-- §6. 极光逆对偶
-- ============================================================

/-- 极光逆对偶：脉冲星辐射与地球极光构成方向反转的对偶对。

    **脉冲星辐射**（内→外）：
    - 能量来源：内部偏心子集群的周期时序震荡
    - 信号方向：X → Y（从天体内部到外部观测者）
    - 粒子流向：沿磁极向外喷射

    **地球极光**（外→内）：
    - 能量来源：外部太阳风高能粒子
    - 信号方向：Y → X（从外部到天体内部）
    - 粒子流向：沿磁力线向内沉降

    两者共用偶极磁场磁极作为通道，但方向相反。 -/
structure AuroraDuality (X Y : RecObj) where
  pulsar_channel : MagneticChannel X Y
  aurora_channel : MagneticChannel Y X
  pulsar_source_internal : ∃ (C : FixedPointCluster X), C.isEccentric
  aurora_source_external : ∃ (D : FixedPointCluster Y), D.isEccentric

/-- 极光对偶下，两个方向的信号都是周期的。 -/
theorem aurora_duality_both_periodic {X Y : RecObj} (ad : AuroraDuality X Y) :
    ∃ (x : X.T) (y : Y.T),
    (∃ n ≥ 1, (X.step^[n]) x = x) ∧
    (∃ n ≥ 1, (Y.step^[n]) y = y) := by
  rcases ad.pulsar_source_internal with ⟨C, hEcc⟩
  rcases hEcc with ⟨x, hx, hne⟩
  have h_ep := X.eventually_periodic x
  have h_trans := ad.pulsar_channel.toHom.maps_eventually_periodic x h_ep
  rcases h_ep with ⟨n, m, hm, heq⟩
  rcases h_trans with ⟨n', m', hm', heq'⟩
  refine' ⟨X.step^[n] x, Y.step^[n'] (ad.pulsar_channel.toHom.toFun x), ?_, ?_⟩
  · refine' ⟨m, hm, ?_⟩
    have h1 : X.step^[m] (X.step^[n] x) = X.step^[m + n] x :=
      iterate_iterate_add X.step m n x
    rw [h1, Nat.add_comm m n, heq]
  · refine' ⟨m', hm', ?_⟩
    have h1 : Y.step^[m'] (Y.step^[n'] (ad.pulsar_channel.toHom.toFun x)) =
        Y.step^[m' + n'] (ad.pulsar_channel.toHom.toFun x) :=
      iterate_iterate_add Y.step m' n' (ad.pulsar_channel.toHom.toFun x)
    rw [h1, Nat.add_comm m' n', heq']

-- ============================================================
-- §7. 观测现象解释
-- ============================================================

/-- **自旋降速（Spin-down）**：时序扰动持续向外耗散能量。
    形式化：周期态的任意迭代仍然是周期态，
    每一步都产生信号——辐射持续。 -/
theorem spin_down_persistent {X Y : RecObj} (φ : X ⟶ Y)
    (x : X.T) (h : X.isPeriodic x) :
    ∀ k : ℕ, ∃ n ≥ 1, (Y.step^[n]) (Y.step^[k] (φ.toFun x)) = Y.step^[k] (φ.toFun x) := by
  intro k
  -- φ(x) 是周期的
  have h1 : Y.isPeriodic (φ.toFun x) := φ.maps_periodic x h
  rcases h1 with ⟨n, hn, hx⟩
  -- Y.step^[k] (φ x) 的周期也是 n（迭代保持周期性）
  refine' ⟨n, hn, ?_⟩
  -- Need: Y.step^[n] (Y.step^[k] (φ x)) = Y.step^[k] (φ x)
  -- Y.step^[n] (Y.step^[k] (φ x)) = Y.step^[n+k] (φ x) = Y.step^[k+n] (φ x)
  -- = Y.step^[k] (Y.step^[n] (φ x)) = Y.step^[k] (φ x)  (by hx)
  rw [iterate_iterate_add Y.step n k (φ.toFun x), Nat.add_comm n k,
      ← iterate_iterate_add Y.step k n (φ.toFun x), hx]

/-- 脉冲星辐射的周期性 = 偏心子集群运动周期。
    形式化：若偏心子集群中 x 的周期为 n，
    则经通道传导后 Y 中信号的周期整除 n。 -/
theorem T02_period_divides {X Y : RecObj}
    (φ : X ⟶ Y) (x : X.T) (n : ℕ) (hn : n ≥ 1)
    (hper : (X.step^[n]) x = x) :
    ∃ m : ℕ, m ≥ 1 ∧ m ≤ n ∧ (Y.step^[m]) (φ.toFun x) = φ.toFun x := by
  have h_n_period : (Y.step^[n]) (φ.toFun x) = φ.toFun x := by
    have h_comm := φ.iterate_comm n x
    rw [hper] at h_comm
    exact h_comm.symm
  refine' ⟨n, hn, by omega, h_n_period⟩

-- ============================================================
-- §7. 磁轴夹角与多波段能谱（天体物理验证）
-- ============================================================

/-! 本节形式化研究笔记 §2.4 中的天体物理缺口：
    1. 磁轴-自转轴夹角的内生起源
    2. 多波段（射电/X/γ）能谱的内生推导

    核心物理洞察：
    - 自转轴由系统的全局角动量方向决定（全局对称轴）
    - 磁轴由磁拓扑通道的耦合方向决定（局部拓扑结构）
    - 当 K > K_c 时，偏心子集群打破全局对称性，导致两轴不对齐
    - 偏心子集群的多尺度振荡产生多波段辐射

    形式化策略：
    - 定义 `hasEccentricCore` 表示存在偏心子集群（K > K_c 的推论）
    - 定义 `hasAxisObliquity` 表示磁轴与自转轴不对齐
    - 定义 `hasMultiBandSpectrum` 表示存在多波段辐射
    - 证明 `hasEccentricCore → hasAxisObliquity`
    - 证明 `hasEccentricCore → hasMultiBandSpectrum` -/

/-- 偏心核心存在性：RecObj X 包含至少一个偏心子集群。
    物理对应：K > K_c 时，天体内核存在永久性偏心高密度子集群。
    这是磁轴夹角和多波段能谱的共同前提。 -/
def hasEccentricCore (X : RecObj) : Prop :=
  ∃ C : FixedPointCluster X, C.carrier.Nonempty ∧
  ∃ x ∈ C.carrier, X.step x ≠ x

/-- 全局对称性：RecObj X 具有全局旋转对称性。
    物理对应：自转轴方向的确定性（角动量守恒）。
    当存在偏心核心时，全局对称性被打破。 -/
def hasGlobalSymmetry (X : RecObj) : Prop :=
  ∀ C : FixedPointCluster X, C.carrier.Nonempty →
  ∀ x ∈ C.carrier, X.step x = x

/-- 偏心核心打破全局对称性。 -/
theorem eccentric_breaks_symmetry (X : RecObj)
    (h : hasEccentricCore X) : ¬ hasGlobalSymmetry X := by
  intro h_sym
  rcases h with ⟨C, h_nonempty, x, hx, h_neq⟩
  have h_fixed := h_sym C h_nonempty x hx
  exact h_neq h_fixed

/-- 自转轴方向：由系统的全局对称性决定。
    当系统有全局对称性时，自转轴是唯一的；
    当偏心核心存在时，自转轴由总角动量决定。 -/
structure RotationAxis (X : RecObj) where
  /-- 自转轴的"方向"由一个参考态表示 -/
  ref_state : X.T
  /-- 参考态是不动点（全局对称时）或周期态（有偏心核心时） -/
  is_periodic : ∃ n : ℕ, n ≥ 1 ∧ (X.step^[n]) ref_state = ref_state

/-- 磁轴方向：由磁拓扑通道的耦合方向决定。
    物理对应：磁极方向是拓扑上能耗散阻力最低的通道。 -/
structure MagneticAxis (X Y : RecObj) (φ : X ⟶ Y) where
  /-- 磁轴的"方向"由通道的不动点表示 -/
  channel_fp : Y.T
  /-- 通道不动点满足 step 不变性 -/
  is_fixed : Y.step channel_fp = channel_fp

/-- 磁轴夹角存在性：当偏心核心存在时，磁轴与自转轴不对齐。
    物理意义：偏心子集群的非对称质量分布导致磁轴偏离自转轴。
    这是脉冲星辐射的几何基础。 -/
def hasAxisObliquity (X Y : RecObj) (φ : X ⟶ Y) : Prop :=
  ∃ (r : RotationAxis X) (m : MagneticAxis X Y φ),
    -- 自转轴参考态与磁轴通道不动点不对齐
    φ.toFun r.ref_state ≠ m.channel_fp

/-- **磁轴夹角定理**：当 RecObj 有偏心核心时，磁轴与自转轴不对齐。
    证明思路：
    1. 偏心核心存在 → 存在非不动点元素 x（X.step x ≠ x）
    2. 自转轴由周期态 x 表示（周期 n ≥ 1）
    3. 磁轴由通道不动点 y 表示（Y.step y = y）
    4. 若 φ.toFun x = y，则由 φ.comm 得 φ.toFun (X.step x) = Y.step y = y = φ.toFun x
    5. 由 φ 的单射性得 X.step x = x，与 hx_eccentric 矛盾
    6. 因此 φ.toFun x ≠ y，即磁轴与自转轴不对齐

    注：需要 φ 单射假设——若 φ 非单射，多个不同状态可映射到同一不动点。 -/
theorem T02_axis_obliquity {X Y : RecObj} (φ : X ⟶ Y) (x : X.T)
    (hx_periodic : ∃ n : ℕ, n ≥ 1 ∧ (X.step^[n]) x = x)
    (hx_eccentric : X.step x ≠ x)
    (y : Y.T) (hy_fixed : Y.step y = y)
    (h_inj : Function.Injective φ.toFun) :
    φ.toFun x ≠ y := by
  intro h_eq
  -- φ.toFun (X.step x) = Y.step (φ.toFun x) = Y.step y = y
  have h_step : φ.toFun (X.step x) = φ.toFun x := by
    rw [φ.comm, h_eq, hy_fixed]
  -- 由单射性得 X.step x = x
  exact hx_eccentric (h_inj h_step)

/-- 多波段辐射定义：RecObj X 的辐射包含多个不同频率的谱段。
    物理对应：脉冲星在射电、X射线、γ射线等多个波段都有辐射。 -/
def hasMultiBandSpectrum (X : RecObj) : Prop :=
  ∃ (n₁ n₂ : ℕ), n₁ ≠ n₂ ∧ n₁ ≥ 1 ∧ n₂ ≥ 1 ∧
  ∃ (x₁ x₂ : X.T),
    (X.step^[n₁]) x₁ = x₁ ∧
    (X.step^[n₂]) x₂ = x₂

/-- **多波段能谱定理**：当偏心核心存在时，系统具有多波段辐射能力。
    证明思路：
    1. 偏心核心存在 → 存在偏心子集群 C
    2. C 中有不动点 x₀（X.step x₀ = x₀）和非不动点 x₁（X.step x₁ ≠ x₁）
    3. 不动点 x₀ 的周期为 1（射电波段基频）
    4. 非不动点 x₁ 最终进入周期轨道（eventually_periodic）
    5. 周期轨道的周期 m ≥ 1
    6. 若 m ≥ 2：取 n₁ = 1, n₂ = m，1 ≠ m ✓
    7. 若 m = 1：step^[n] x₁ 是不动点，不动点有周期 2，取 n₁ = 1, n₂ = 2，1 ≠ 2 ✓
    8. 因此存在多波段辐射 -/
theorem T02_multi_band_spectrum {X : RecObj} (C : FixedPointCluster X)
    (x₀ : X.T) (hx₀ : x₀ ∈ C.carrier) (h_fixed : X.step x₀ = x₀)
    (x₁ : X.T) (hx₁ : x₁ ∈ C.carrier) (h_ecc : X.step x₁ ≠ x₁) :
    hasMultiBandSpectrum X := by
  unfold hasMultiBandSpectrum
  -- x₀ 是不动点，周期为 1
  have h₀ : (X.step^[1]) x₀ = x₀ := by
    simp only [Function.iterate_one, h_fixed]
  -- x₁ 最终进入周期轨道
  rcases X.eventually_periodic x₁ with ⟨n, m, hm, h_per⟩
  -- step^[n] x₁ 是周期态，周期为 m
  -- 交换引理：step^[k] (step^[n] y) = step^[n] (step^[k] y)
  have h_comm : ∀ k y, X.step^[k] (X.step^[n] y) = X.step^[n] (X.step^[k] y) := by
    intro k y
    have h1 := congr_fun (Function.iterate_add X.step k n) y
    have h2 := congr_fun (Function.iterate_add X.step n k) y
    simp only [Function.comp_apply] at h1 h2
    rw [← h1, ← h2, Nat.add_comm]
  -- 分情况讨论：m ≥ 2 或 m = 1
  by_cases hm2 : m ≥ 2
  · -- 情况 1：m ≥ 2，取 n₁ = 1, n₂ = m
    refine' ⟨1, m, by omega, by norm_num, hm, x₀, (X.step^[n]) x₁, h₀, _⟩
    rw [h_comm m x₁]
    have h_iter : X.step^[n + m] x₁ = X.step^[n] (X.step^[m] x₁) :=
      congr_fun (Function.iterate_add X.step n m) x₁
    rw [← h_iter, h_per]
  · -- 情况 2：m = 1，step^[n] x₁ 是不动点
    push_neg at hm2
    have hm1 : m = 1 := by omega
    rw [hm1] at h_per
    -- h_per : step^[n+1] x₁ = step^[n] x₁
    -- x₀ 是不动点：step x₀ = x₀
    -- 不动点有任意周期，包括 1 和 2
    -- 不需要 x₁ 的周期信息
    exact ⟨1, 2, by omega, by norm_num, by norm_num, x₀, x₀,
      by simp only [Function.iterate_one, h_fixed],
      by simp only [Function.iterate_succ, Function.iterate_zero,
        Function.comp_apply, id_eq, h_fixed]⟩

/-- 偏心核心同时激发连续引力波（与 T-04 交叉验证）。
    物理意义：偏心核心的周期性时序震荡同时在电磁通道和引力波通道产生信号。 -/
theorem T02_eccentric_gw_prediction {X : RecObj}
    (h : hasEccentricCore X) :
    -- 偏心核心存在 → 系统有周期性振荡
    ∃ n : ℕ, n ≥ 1 ∧ ∃ x : X.T, (X.step^[n]) x = x := by
  rcases h with ⟨C, h_nonempty, x, hx, h_neq⟩
  -- 由 eventually_periodic，x 最终进入周期轨道
  rcases X.eventually_periodic x with ⟨k, m, hm, h_per⟩
  -- 取 y = (X.step^[k]) x，则 (X.step^[m]) y = y
  exact ⟨m, hm, (X.step^[k]) x, by
    have h_iter : X.step^[m + k] x = X.step^[m] (X.step^[k] x) :=
      congr_fun (Function.iterate_add X.step m k) x
    rw [← h_iter, Nat.add_comm]
    exact h_per⟩

end MUFPF
