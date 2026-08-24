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
-- 本文件中 UFPF 相关引用数量：3
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import Lake
open Lake DSL

package «UFPFormalization» where
  -- add package configuration options here

require mathlib from ".lake/packages/mathlib"

lean_lib «UFPFormalization» where
  -- add library configuration options here

@[default_target]
lean_exe «ufpformalization» where
  root := `Main
