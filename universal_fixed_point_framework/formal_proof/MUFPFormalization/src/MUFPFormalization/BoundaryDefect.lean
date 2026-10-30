import Mathlib.Tactic
import MUFPFormalization.SilenceModel

/-! ## 边界缺陷度：Rec → Sp 的映射定律（2026-10-24 语义切割勘误）

   语义切割：`defectMeasure`（SpectralBundle/Core，RecObj → ℕ，偏心元素/非不动点计数）
   是**内部离散量**；§5 映射口径 C 终点的"缺陷度 d = 4·ln g"是**边界连续量**。
   两者由**对数映射定律**连接（Rec → Sp），不是同一符号的相等：
   离散侧 g : ℕ（锁定窗口/周期轨道计数）⟶ 连续侧 boundaryDefect g = 4·ln g : ℝ。
   这正对应框架主张"纯内生离散生成链 → 连续物理量"，且消解 ℕ/ℝ 类型张力
   （内部缺陷度归零 = 配置干净；边界缺陷度随锁定窗口规模增长，引力存在）。 -/

namespace MUFPF

/-- 边界缺陷度：由离散计数 g（锁定窗口/周期轨道数）经对数映射得到的连续边界量。
    d = 4·ln g —— §5 映射口径 C 终点的离散→连续形式（M_Pl=1、codim=2 系数 4）。 -/
noncomputable def boundaryDefect (g : ℕ) : ℝ := 4 * Real.log (g : ℝ)

/-- boundaryDefect 15 = 4·ln 15：g=15 实现（离散侧）在连续侧的取值。 -/
theorem boundaryDefect_15 : boundaryDefect 15 = 4 * Real.log (15 : ℝ) := by
  rfl

open MUFPF.PeriodicOrbitCount

/-- 组装：离散侧 g=15 实现（orbitCount = 15，反向翻译主定理已绿）
    ⟹ 连续侧边界缺陷度 = 4·ln 15。
    引理链：orbitCount_eq_15_iff（SilenceModel，已绿）→ boundaryDefect 定义展开。 -/
theorem silence_chain_boundary_defect (S : Finset (Fin 15))
    (h : S = Finset.univ ∨ S = Finset.univ.erase 14) :
    boundaryDefect (orbitCount (silenceRec15_layered S)) = 4 * Real.log (15 : ℝ) := by
  have ho : orbitCount (silenceRec15_layered S) = 15 :=
    (MUFPF.PeriodicOrbitCount.orbitCount_eq_15_iff S).mpr h
  rw [ho]
  rfl

end MUFPF
