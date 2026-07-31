module Everything where

-- UFPF Agda 重形式化：全部模块导入
-- B1 ✅  Sp 4-范畴定义
-- B2 ✅  高阶态射（2-态射、3-态射）
-- B3 ✅  D 函子 + 右伴随 R + 伴随对 D ⊣ R
-- B4 ✅  d_H 结构分析与不等式链
-- B5 ✅  统一 3 定理（Unified3Theorem）
-- B6 ✅  Bott 塔（BottTower）
-- B7 ✅  静默定理组（CoherenceToBranching）
-- B8 ✅  IFS 排序定理（IFSFractal）
-- NatArith ✅  ℕ 算术引理库（闭合基础）

open import Sp.SpCategory
open import Sp.HigherSpCategory
open import Rec.RecCategory
open import NatArith.NatArith
open import DecursionFunctor.DecursionFunctor
open import DHStructural.DHStructuralAnalysis
open import Unified3.Unified3Theorem
open import BottTower.BottTower
open import CoherenceToBranching.CoherenceToBranching
open import IFSFractal.IFSFractal
