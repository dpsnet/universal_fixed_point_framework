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
-- 本文件中 UFPF 相关引用数量：16
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

/-
最小可构建原型：验证 Lean 4 工具链与 Lake 构建系统可用。

∞-Category 模块编译入口：此处 import 触发所有 ∞-范畴模块的编译。

更名计划通知（2026-08-24）：
框架名称将从 UFPF (Universal Fixed Point Framework) 更名为
MUFPF (Meta-Universal Fixed-Point Functorial Framework)，
以解决与 IEEE 生物图像识别框架的命名冲突。
当前代码中的 UFPF 引用将在更名计划确认后统一修改。
详见 roadmap/mu_renaming_plan.md
-/

import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.AInfinityAlgebra
import UFPFormalization.DecursionFunctor
import UFPFormalization.HigherSpCategory
import UFPFormalization.RecInfinity
import UFPFormalization.SpecInfinity
import UFPFormalization.InfinityCategory
import UFPFormalization.SpectralFlowHomotopy
import UFPFormalization.DInfinityFunctor

namespace UFPFormalization.Basic

def hello : String := "UFPFormalization ready"

#eval hello

end UFPFormalization.Basic
