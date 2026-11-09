import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.CategoryTheory.Iso
import MUFPFormalization.RAP5a_explicit_adjunction
import MUFPFormalization.DecursionFunctor
import MUFPFormalization.RecCategory
import MUFPFormalization.SpCategory

/-! # AdjunctionAnchor.lean — SpImD 唯一性边界 + 伴随锚点（登记层）

## 本文件定位

承接 RAP5a_explicit_adjunction.lean 的边界讨论（§6-§9），集中登记：

  1. Universe 诚实边界（RecObj universe-polymorphic vs SpObj fixed Type 0）
  2. 已机检 theorem 的列表引用
  3. SpImD 唯一性的对象层 + 态射层骨架（登记注释 + 开放组件标记）
  4. Phase 16B 升级路线图

本文件**不重新证明 theorem**——那些在 RAP5a 里都有。
本文件的价值是把分散在多个模块里的伴随边界相关结论集中到一个锚文件，
方便论文引用和 Phase 16B 路线图查阅。

## Universe 诚实边界（必须先声明）

| 类型 | Universe 绑定 | 来源 |
|---|---|---|
| RecObj | **universe-polymorphic** `universe u; structure RecObj where T : Type u ...` | RecCategory.lean L23-27 |
| SpObj | **固定 Type 0** `structure SpObj where n : ℕ; A : Matrix (Fin n) (Fin n) ℂ` | SpCategory.lean L31-33 |
| SpImD | **固定 Type 1**（`structure SpImD : Type 1`，字段绑定到 SpObj 与 RecObj 在 Type 0 的实例） | RAP5a.lean §3 |
| DFunctor_obj | **固定 Type 0 → Type 0**（`(X : RecObj) : SpObj`，X 自动推断 Type 0） | DecursionFunctor.lean L73 |

**关键**：RecObj 是 universe-polymorphic 但 SpObj 不是，导致
`∃ (X : RecObj.{u}), Nonempty (Iso (DFunctor_obj X) E)` 对 E : SpObj
是 **universe mismatch**——DFunctor_obj 的参数 RecObj 无法接受 .{u} 的提升。

这不是 Lean 代码错误，是**设计选择**：当前层所有对象固定在 Type 0，
所以 Lean 库侧的 theorem 都在 Type 0 工作。跨 universe 版本需要 SpObj 先升级。
广义 MUFPF（Paper I 设计）把 Rec 和 Sp 都做成同一 universe 的对象，
那边的伴随问题不需要 universe-polymorphic SpObj。 -/

namespace MUFPF.AdjunctionAnchor

-- ═══════════════════════════════════════════════════════════════════════════
-- Part 1: 已机检 theorem 列表（从 RAP5a 引用）
-- ═══════════════════════════════════════════════════════════════════════════

/-- **已机检的伴随边界 theorem 列表**（全部在 RAP5a_explicit_adjunction.lean 里）：

  ① `DFunctor_faithful` (RAP5a §4)
     DFunctor 全范畴 faithful——transferMatrix 单射
     universe: Type 0（自动推断）
     状态: ✅ theorem

  ② `DIm_full` (RAP5a §6)
     DIm 在 SpImD 上 full——DIm_map 是满射
     universe: Type 0（自动推断）
     状态: ✅ theorem（`intro φ; refine' ⟨φ.hom, rfl⟩` 闭合）

  ③ `DIm_faithful` (RAP5a §6)
     DIm 在 SpImD 上 faithful
     universe: Type 0（自动推断）
     状态: ✅ theorem

  ④ `D_not_full` (RAP5a §7)
     D 全范畴不 full——存在合法谱态射不在 D 的像里
     universe: Type 0
     状态: ✅ theorem

  ⑤ `no_global_right_adjoint` (RAP5a §9)
     不存在任何 R : SpObj ⥤ RecObj 使 DFunctor ⊣ R 在全范畴成立
     证明: adjunction hom-equivalence 强制 Hom_Sp(DX,DX) ≅ Hom_Rec(X,R(DX))
           对二态平凡系统 X，左=ℂ⁴(不可数)，右有限，矛盾
     universe: Type 0
     状态: ✅ theorem

  ⑥ `DImAdjRIm` (RAP5a §7)
     DIm ⊣ RIm 在 SpImD 上成立（受限伴随）
     universe: Type 0
     状态: ✅ theorem（三角恒等式已机检）

  所有 theorem 依赖仅 Mathlib + RecCategory/SpCategory/DFunctor/SpImD，
  不依赖任何项目 axiom（7 个候选级 axiom 分布在其他模块）。 -/

theorem verified_adjunction_anchor_list : True := trivial

-- ═══════════════════════════════════════════════════════════════════════════
-- Part 2: SpImD 唯一性骨架（登记注释 + 开放组件标记）
-- ═══════════════════════════════════════════════════════════════════════════

/-! **SpImD 唯一性论证的数学骨架（已登记注释，未机检完整等价）**

    SpImD 的唯一性来自它**恰好携带了**使 D full 所需的全部身份信息：

      对象层：(src, tgt, conn) = IsImageOfD 的完整显式见证
      态射层：SpImDMor.hom = RecHom（不携带 D 不支持的信息）

    唯一性论证分两步：

    Step A: 对象层互逆映射（已在本文件下方登记，universe 诚实边界需显式 Type 0）

      正向：F : SpImD → {E : SpObj // IsImageOfD E}
        F E = ⟨E.tgt, ⟨E.src, ⟨E.conn⟩⟩⟩
      逆向：G : {E : SpObj // IsImageOfD E} → SpImD
        G p = Classical.choose (p.property 的 ∃ 见证)
      G ∘ F ≡ id（tgt 字段恒等，src/conn 字段 Classical.choose 可能选不同值但同构）

      ⚠ 开放组件：对象层完整同构（src/conn 字段）——
        需要 Classical.choose 唯一性 lemma（给定 E，IsImageOfD 的见证 ∃ (X, conn)
        在同构意义下唯一，但 Classical.choose 抽出来的 X' 和 conn' 可能和
        原来的不同，只是 Iso-equivalent）。

    Step B: 态射层等价（开放组件，需要在 IsImageOfD_obj 上定义 Hom 集）

      SpImDMor.hom = RecHom 已机检（SpImDMor 的定义直接携带 RecHom）。
      IsImageOfD_obj 上的态射结构需要另行定义 Hom = RecHom——
      这是"为什么 SpImD 是使 D full 的唯一子范畴"的态射层论据。

    结论登记：

      SpImD_obj ≌ IsImageOfD_obj（对象层等价，Step A + Step B 完成后升级为范畴等价）
      SpImD ≌ Im(D)（完整范畴等价，需要 DImAdjRIm + 对象层 + 态射层全部完成）

    Phase 16B 路线图（见本文件 Part 3）：
      SpObj 升级 universe-polymorphic → IsImageOfD.{u} 可定义
      DFunctor_obj 升级 universe-polymorphic → D.{u} : RecObj.{u} ⥤ SpObj.{u}
      SpImD 升级 universe-polymorphic → SpImD.{u}
      完整范畴等价 F.{u} : SpImD.{u} ≌ Im(D.{u}) 机检 -/

theorem SpImD_uniqueness_skeleton : True := trivial

-- ═══════════════════════════════════════════════════════════════════════════
-- Part 3: Universe Type-0 受限版 IsImageOfD（登记 + 诚实边界）
-- ═══════════════════════════════════════════════════════════════════════════

/-! **Type-0 受限 IsImageOfD**

    Universe 诚实边界：RecObj 在 Type 0 实例下工作（DFunctor_obj 参数自动推断），
    所以 IsImageOfD 定义为：

      IsImageOfD (E : SpObj) : Prop :=
        ∃ (X : RecObj), Nonempty (Iso (DFunctor_obj X) E)

    Universe-polymorphic 版本（接受 RecObj.{u}）需要 SpObj 升级 universe-polymorphic——
    让 SpObj.obj.{u} 接受 universe 参数；当前 SpObj 固定 Type 0。
    这个升级在 Phase 16B 路线图里登记为"并行路线"。

    下面的 def 尝试提供 Type-0 受限版本；
    但 Lean 推断 X 的 universe 仍有问题——见文件顶部 Universe 诚实边界。 -/

-- ⚠ 以下 def 因 Lean universe 推断问题无法通过构建，登记为开放组件
--   具体修复需要 SpObj 升级 universe-polymorphic（Phase 16B）
-- def IsImageOfD_Type0 (E : SpObj) : Prop :=
--   ∃ (X : RecObj), Nonempty (Iso (DFunctor_obj X) E)

theorem Universe_boundary_open_for_Phase16B : True := trivial

-- ═══════════════════════════════════════════════════════════════════════════
-- Part 4: Phase 16B 路线图登记（Polish 路线 + 粗粒化路线并行）
-- ═══════════════════════════════════════════════════════════════════════════

/-! **Phase 16B 两条并行路线：让伴随在广义 MUFPF 层存在**

    当前 Lean 原型（集合语义 Fintype 层）：
      D : RecObj (Type 0) → SpObj (Type 0)
      Hom_Rec 有限 / Hom_Sp 不可数 → no_global_right_adjoint ✅
      SpImD 层（身份标记后）：DIm ⊣ RIm ✅ 已机检

    广义 MUFPF 设计（Paper I 路线）：
      D_gen : Polish 空间 + 线性谱匹配态射 → Hilbert 算子
      Hom_Rec 无限 / Hom_Sp 无限 → 伴随可能存在（Paper I 设计）
      Lean 侧：需要 Agda 的 11 postulate 降 theorem + Mathlib 升级

    **路线 P（Polish 路线，Paper I 设计直接实现）**：
      - Rec 侧：把 RecObj 从 Fintype 升级到 Polish 空间 + 线性谱匹配态射
      - Sp 侧：把 SpObj 从有限矩阵升级到 Hilbert 算子
      - 两边 Hom 集都变成无限 → 基数矛盾消失 → 伴随可构造
      - 工作量：极大（需要 Hilbert 算子的稠密定义域、半群、Hille-Yosida 等 Mathlib 组件）
      - 依赖：Agda 侧 11 postulate（Fuglede、Hille-Yosida 等）先降 theorem

    **路线 B（粗粒化路线，用户截断-精度对偶 M1 实现）**：
      - Sp 侧：在 SpObj 上引入粗粒化等价关系 ~
      - SpCrudeObj = SpObj / ~（按实验精度截断到有限个可分辨类）
      - Hom_SpCrude 对象 = Finite → 两边都有限 → 基数矛盾消失 → 伴随可构造
      - 工作量：中等（定义粗粒化等价 + 商范畴 + 在商上构造伴随）
      - 物理对应：粗粒化尺度 ~ 实验精度 = 截断尺度（M1 截断-精度对偶）

    两条路线的数学等价性（登记探索点）：
      Polish 路线在某种紧化/截断下的有限部分 ≌ 粗粒化路线的有限商范畴
      如果这个等价性成立，那么广义 MUFPF 其实有两条通向伴随存在的路线，
      而这两条路线在物理上对应同一个核心思想——截断、精度、有限维近似。

    Universe-polymorphic SpObj 升级（两条路线都需要）：
      SpObj 当前固定 Type 0（n : ℕ, A : Matrix (Fin n) (Fin n) ℂ）
      升级后：universe u; structure SpObj where n : ℕ; V : Type u [Fintype V]; A : Matrix V V ℂ
      这样 SpObj.{u} 和 RecObj.{u} 共享同一 universe，IsImageOfD.{u} 可定义。

    本文件 Part 1-4 构成 Phase 16B 规划文档的数学锚。 -/

theorem Phase16B_two_routes_registered : True := trivial

end MUFPF.AdjunctionAnchor
