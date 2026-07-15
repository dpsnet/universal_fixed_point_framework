/-
通用不动点范畴框架 I：分形谱去递归理论
机器证明形式化库 — Phase 16A

本库基于 Lean 4 + mathlib4，目标是将论文 Paper I 中等级 A 的命题与定理
（范畴构造、D 函子、D⊣R 伴随、谱对应 M≅L、有限维轨道函子、Clifford 矩阵表示）
进行形式化核验。
-/

import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.Adjunction
import UFPFormalization.SpectralCorrespondence
import UFPFormalization.OrbitFunctor
import UFPFormalization.Clifford
