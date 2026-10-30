/-
ClosureFamily.lean — MUFPF 子集闭包家族结构定理（104az-194/195 形式化）

内容：
V1. Closed3/Constr 定义：无单位 3 元子集闭包 ⟺ 三约束（[2,16] 域内）
V2. 结构定理 A：closed3_iff_constr_range（全枚举 native_decide）
V3. 11 个无单位闭包清单 + 计数
V4. 结构定理 B：closed3_mem_list（闭包 ⟺ 清单成员）
V5. 结构定理 C（显式代数）：Closed4 1 a b c → Closed3 a b c（面闭包的子集蕴含，非黑箱）
V6. 4 元闭包完备性：Closed4 1 a b c ⟺ (a,b,c) ∈ closure3List
V7. 5 元封顶：无单调 5 元闭包（[1,16] 域）

注：FW/FWSum/closure3List 用 Finset 而非 List——Finset 的成员判定与
`Finset.decidableDforallFinset` 实例在 Mathlib 中稳定存在，native_decide
对 `∀ a ∈ Finset.Icc ...` 有界枚举可自动合成 Decidable。
-/
import Mathlib.Tactic
import Mathlib.Data.Finset.Interval

-- 4 元/5 元闭包的长合取（30+/60+ 项）在 native_decide 归约时超出默认递归深度
set_option maxRecDepth 50000

namespace MUFPFormalization.ClosureFamily

-- FW 表（49 个已登记框架量整数，104az-193 口径）
def FW : Finset ℕ :=
  ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 21, 28, 29, 30, 31,
   32, 35, 40, 42, 44, 45, 46, 48, 49, 56, 58, 60, 61, 63, 64, 65, 84, 98, 100,
   105, 125, 210, 253, 320, 675, 729, 1000} : Finset ℕ)

-- FW_SUM（和谱集合 = 值 ≤ 64 者 ∪ 大值，104az-193 口径）
def FWSum : Finset ℕ :=
  FW.filter (fun n => n ≤ 64) ∪ ({105, 125, 210, 253, 320, 675, 729} : Finset ℕ)

-- 无单位 3 元子集闭包：(a,b,c) 严格递增互异，全部 7 非空子集和 ∈ FWSum、积 ∈ FW
abbrev Closed3 (a b c : ℕ) : Prop :=
  a < b ∧ b < c ∧
  a ∈ FWSum ∧ b ∈ FWSum ∧ c ∈ FWSum ∧
  a + b ∈ FWSum ∧ a + c ∈ FWSum ∧ b + c ∈ FWSum ∧
  a + b + c ∈ FWSum ∧
  a ∈ FW ∧ b ∈ FW ∧ c ∈ FW ∧
  a * b ∈ FW ∧ a * c ∈ FW ∧ b * c ∈ FW ∧
  a * b * c ∈ FW

-- 三约束（[2,16] 域内严格递增互异；素基 ⊆ {2,3,5,7} ⟺ 排除 {11,13}）
abbrev Constr (a b c : ℕ) : Prop :=
  a < b ∧ b < c ∧
  2 ≤ a ∧ a ≤ 16 ∧ 2 ≤ b ∧ b ≤ 16 ∧ 2 ≤ c ∧ c ≤ 16 ∧
  a ≠ 11 ∧ a ≠ 13 ∧ b ≠ 11 ∧ b ≠ 13 ∧ c ≠ 11 ∧ c ≠ 13 ∧
  a + b + c ≤ 15 ∧
  a * b ∈ FW ∧ a * c ∈ FW ∧ b * c ∈ FW ∧
  a * b * c ∈ FW

-- V2. 结构定理 A：无单位 3 元闭包 ⟺ 三约束（[2,16] 全枚举）
theorem closed3_iff_constr_range :
    (∀ a ∈ Finset.Icc 2 16, ∀ b ∈ Finset.Icc 2 16, ∀ c ∈ Finset.Icc 2 16,
      Closed3 a b c ↔ Constr a b c) := by
  native_decide

-- 11 个无单位 3 元闭包清单（104az-194 全积谱 {30,40,42,56,60,64,84,105} 分解）
def closure3List : Finset (ℕ × ℕ × ℕ) :=
  ({(2, 3, 5), (2, 3, 7), (2, 3, 10), (2, 4, 5), (2, 4, 7), (2, 4, 8),
    (2, 5, 6), (2, 6, 7), (3, 4, 5), (3, 4, 7), (3, 5, 7)} : Finset (ℕ × ℕ × ℕ))

-- V3. 计数 = 11
theorem closure3List_count : closure3List.card = 11 := by
  native_decide

-- V4. 结构定理 B：闭包 ⟺ 清单成员（全枚举）
theorem closed3_mem_list :
    (∀ a ∈ Finset.Icc 2 16, ∀ b ∈ Finset.Icc 2 16, ∀ c ∈ Finset.Icc 2 16,
      Closed3 a b c ↔ (a, b, c) ∈ closure3List) := by
  native_decide

-- 含单位元 1 的 4 元子集闭包（1 < a < b < c 严格递增互异，全部 15 非空子集和 ∈ FWSum、积 ∈ FW）
abbrev Closed4 (one a b c : ℕ) : Prop :=
  one < a ∧ a < b ∧ b < c ∧
  one ∈ FWSum ∧ a ∈ FWSum ∧ b ∈ FWSum ∧ c ∈ FWSum ∧
  one + a ∈ FWSum ∧ one + b ∈ FWSum ∧ one + c ∈ FWSum ∧
  a + b ∈ FWSum ∧ a + c ∈ FWSum ∧ b + c ∈ FWSum ∧
  one + a + b ∈ FWSum ∧ one + a + c ∈ FWSum ∧ one + b + c ∈ FWSum ∧
  a + b + c ∈ FWSum ∧
  one + a + b + c ∈ FWSum ∧
  one ∈ FW ∧ a ∈ FW ∧ b ∈ FW ∧ c ∈ FW ∧
  one * a ∈ FW ∧ one * b ∈ FW ∧ one * c ∈ FW ∧
  a * b ∈ FW ∧ a * c ∈ FW ∧ b * c ∈ FW ∧
  one * a * b ∈ FW ∧ one * a * c ∈ FW ∧ one * b * c ∈ FW ∧
  a * b * c ∈ FW ∧
  one * a * b * c ∈ FW

-- 长合取（30+ 项）在 native_decide 全称枚举时 typeclass 合成预算不足，
-- 显式缓存 Decidable 实例（展开一次后复用）
instance (one a b c : ℕ) : Decidable (Closed4 one a b c) := by
  unfold Closed4
  infer_instance

-- V5. 结构定理 C（显式代数证明，非黑箱）：4 元闭包 (1,a,b,c) ⟹ 无单位 3 元闭包 (a,b,c)
-- 依据：Closed3 的 14 项条件全部是 Closed4 相应子集条件（面闭包的子集蕴含），
-- 递增约束 a<b ∧ b<c 由 Closed4 的 one<a ∧ a<b ∧ b<c 直接继承
theorem closed4_l1_implies_closed3 (a b c : ℕ) :
    Closed4 1 a b c → Closed3 a b c := by
  intro h
  rcases h with ⟨h_1lt, h_ab, h_bc,
                h_one_s, h_a_s, h_b_s, h_c_s,
                h_1a_s, h_1b_s, h_1c_s, h_ab_s, h_ac_s, h_bc_s,
                h_1ab_s, h_1ac_s, h_1bc_s, h_abc_s, h_1abc_s,
                h_one_p, h_a_p, h_b_p, h_c_p,
                h_1a_p, h_1b_p, h_1c_p, h_ab_p, h_ac_p, h_bc_p,
                h_1ab_p, h_1ac_p, h_1bc_p, h_abc_p, h_1abc_p⟩
  exact ⟨h_ab, h_bc,
         h_a_s, h_b_s, h_c_s, h_ab_s, h_ac_s, h_bc_s, h_abc_s,
         h_a_p, h_b_p, h_c_p, h_ab_p, h_ac_p, h_bc_p, h_abc_p⟩

-- V6. 4 元闭包完备性：含 1 的 4 元闭包 ⟺ 非 1 部分 ∈ closure3List（全枚举）
theorem closed4_l1_mem_list :
    (∀ a ∈ Finset.Icc 2 16, ∀ b ∈ Finset.Icc 2 16, ∀ c ∈ Finset.Icc 2 16,
      Closed4 1 a b c ↔ (a, b, c) ∈ closure3List) := by
  native_decide

-- V7. 5 元封顶：不存在单调 5 元子集闭包（[1,16] 域；5 元闭包 ⟹ 4 元面闭包，枚举无解）
-- 5 元子集闭包 = 和条件（31 项）+ 积条件（30 项），拆两个子谓词避免合成超预算
abbrev Sums5 (a b c d e : ℕ) : Prop :=
  a ∈ FWSum ∧ b ∈ FWSum ∧ c ∈ FWSum ∧ d ∈ FWSum ∧ e ∈ FWSum ∧
  a + b ∈ FWSum ∧ a + c ∈ FWSum ∧ a + d ∈ FWSum ∧ a + e ∈ FWSum ∧
  b + c ∈ FWSum ∧ b + d ∈ FWSum ∧ b + e ∈ FWSum ∧
  c + d ∈ FWSum ∧ c + e ∈ FWSum ∧ d + e ∈ FWSum ∧
  a + b + c ∈ FWSum ∧ a + b + d ∈ FWSum ∧ a + b + e ∈ FWSum ∧
  a + c + d ∈ FWSum ∧ a + c + e ∈ FWSum ∧ a + d + e ∈ FWSum ∧
  b + c + d ∈ FWSum ∧ b + c + e ∈ FWSum ∧ b + d + e ∈ FWSum ∧
  c + d + e ∈ FWSum ∧
  a + b + c + d ∈ FWSum ∧ a + b + c + e ∈ FWSum ∧
  a + b + d + e ∈ FWSum ∧ a + c + d + e ∈ FWSum ∧ b + c + d + e ∈ FWSum ∧
  a + b + c + d + e ∈ FWSum

abbrev Prods5 (a b c d e : ℕ) : Prop :=
  a ∈ FW ∧ b ∈ FW ∧ c ∈ FW ∧ d ∈ FW ∧ e ∈ FW ∧
  a * b ∈ FW ∧ a * c ∈ FW ∧ a * d ∈ FW ∧ a * e ∈ FW ∧
  b * c ∈ FW ∧ b * d ∈ FW ∧ b * e ∈ FW ∧
  c * d ∈ FW ∧ c * e ∈ FW ∧ d * e ∈ FW ∧
  a * b * c ∈ FW ∧ a * b * d ∈ FW ∧ a * b * e ∈ FW ∧
  a * c * d ∈ FW ∧ a * c * e ∈ FW ∧ a * d * e ∈ FW ∧
  b * c * d ∈ FW ∧ b * c * e ∈ FW ∧ b * d * e ∈ FW ∧
  c * d * e ∈ FW ∧
  a * b * c * d ∈ FW ∧ a * b * c * e ∈ FW ∧
  a * b * d * e ∈ FW ∧ a * c * d * e ∈ FW ∧ b * c * d * e ∈ FW ∧
  a * b * c * d * e ∈ FW

abbrev Closed5 (a b c d e : ℕ) : Prop := Sums5 a b c d e ∧ Prods5 a b c d e

-- 显式缓存 Decidable 实例（拆分子谓词后各自可合成）
instance (a b c d e : ℕ) : Decidable (Sums5 a b c d e) := by
  unfold Sums5
  infer_instance
instance (a b c d e : ℕ) : Decidable (Prods5 a b c d e) := by
  unfold Prods5
  infer_instance
instance (a b c d e : ℕ) : Decidable (Closed5 a b c d e) := by
  unfold Closed5
  infer_instance

theorem no_closed5_range :
    (∀ a ∈ Finset.Icc 1 16, ∀ b ∈ Finset.Icc 1 16, ∀ c ∈ Finset.Icc 1 16,
      ∀ d ∈ Finset.Icc 1 16, ∀ e ∈ Finset.Icc 1 16,
        a < b → b < c → c < d → d < e → ¬ Closed5 a b c d e) := by
  native_decide

/-! ## 敏感性条件判别：FW ∪ {24} 口径（2026-10-25，fw_gap_discern + closure_family_sensitivity_24）

若 24 = 4! = (N_gen+1)! 阶乘族身份候选立档（与 6 = N_gen! 同族），FW 表 49→50。
闭包家族重算（closure_family_sensitivity_24.py，2026-10-25）：
  无单位 3 元闭包 11→14、4 元闭包 11→14——新增 3 个，**修正 104az-195 敏感性
  预期（+2 → 13）：(2,3,4)→24 被漏算**（24 ∈ FW 后 (2,3,4) 三积 24 过约束）。
  新闭包：(2,3,4)、(2,3,8)、(2,4,6)；新 4 元闭包含 (1,2,3,4) = 阶乘塔底
  （全积 24 = 4!）——24 身份与闭包家族自洽。
本块为条件定理（FW+24 口径），不改动 49 值口径的 V1~V7。 -/

-- FW∪{24}（50 值；24 = 4! = (N_gen+1)! 阶乘族身份候选）
def FW24 : Finset ℕ := FW ∪ ({24} : Finset ℕ)

def FWSum24 : Finset ℕ :=
  FW24.filter (fun n => n ≤ 64) ∪ ({105, 125, 210, 253, 320, 675, 729} : Finset ℕ)

-- 无单位 3 元子集闭包（FW24 口径）
abbrev Closed3_24 (a b c : ℕ) : Prop :=
  a < b ∧ b < c ∧
  a ∈ FWSum24 ∧ b ∈ FWSum24 ∧ c ∈ FWSum24 ∧
  a + b ∈ FWSum24 ∧ a + c ∈ FWSum24 ∧ b + c ∈ FWSum24 ∧
  a + b + c ∈ FWSum24 ∧
  a ∈ FW24 ∧ b ∈ FW24 ∧ c ∈ FW24 ∧
  a * b ∈ FW24 ∧ a * c ∈ FW24 ∧ b * c ∈ FW24 ∧
  a * b * c ∈ FW24

-- 三约束（FW24 口径；素基 ⊆ {2,3,5,7} ⟺ 排除 {11,13}）
abbrev Constr24 (a b c : ℕ) : Prop :=
  a < b ∧ b < c ∧
  2 ≤ a ∧ a ≤ 16 ∧ 2 ≤ b ∧ b ≤ 16 ∧ 2 ≤ c ∧ c ≤ 16 ∧
  a ≠ 11 ∧ a ≠ 13 ∧ b ≠ 11 ∧ b ≠ 13 ∧ c ≠ 11 ∧ c ≠ 13 ∧
  a + b + c ≤ 15 ∧
  a * b ∈ FW24 ∧ a * c ∈ FW24 ∧ b * c ∈ FW24 ∧
  a * b * c ∈ FW24

-- 结构定理 A'（FW24 口径全枚举）
theorem closed3_24_iff_constr24_range :
    (∀ a ∈ Finset.Icc 2 16, ∀ b ∈ Finset.Icc 2 16, ∀ c ∈ Finset.Icc 2 16,
      Closed3_24 a b c ↔ Constr24 a b c) := by
  native_decide

-- 14 个无单位 3 元闭包清单（FW24 口径）
def closure3List24 : Finset (ℕ × ℕ × ℕ) :=
  ({(2, 3, 4), (2, 3, 5), (2, 3, 7), (2, 3, 8), (2, 3, 10), (2, 4, 5), (2, 4, 6),
    (2, 4, 7), (2, 4, 8), (2, 5, 6), (2, 6, 7), (3, 4, 5), (3, 4, 7),
    (3, 5, 7)} : Finset (ℕ × ℕ × ℕ))

-- 计数 = 14（修正 104az-195 敏感性预期 13）
theorem closure3List24_count : closure3List24.card = 14 := by
  native_decide

-- 结构定理 B'（FW24 口径闭包 ⟺ 清单成员）
theorem closed3_24_mem_list :
    (∀ a ∈ Finset.Icc 2 16, ∀ b ∈ Finset.Icc 2 16, ∀ c ∈ Finset.Icc 2 16,
      Closed3_24 a b c ↔ (a, b, c) ∈ closure3List24) := by
  native_decide

-- 4 元闭包（FW24 口径）
abbrev Closed4_24 (one a b c : ℕ) : Prop :=
  one < a ∧ a < b ∧ b < c ∧
  one ∈ FWSum24 ∧ a ∈ FWSum24 ∧ b ∈ FWSum24 ∧ c ∈ FWSum24 ∧
  one + a ∈ FWSum24 ∧ one + b ∈ FWSum24 ∧ one + c ∈ FWSum24 ∧
  a + b ∈ FWSum24 ∧ a + c ∈ FWSum24 ∧ b + c ∈ FWSum24 ∧
  one + a + b ∈ FWSum24 ∧ one + a + c ∈ FWSum24 ∧ one + b + c ∈ FWSum24 ∧
  a + b + c ∈ FWSum24 ∧
  one + a + b + c ∈ FWSum24 ∧
  one ∈ FW24 ∧ a ∈ FW24 ∧ b ∈ FW24 ∧ c ∈ FW24 ∧
  one * a ∈ FW24 ∧ one * b ∈ FW24 ∧ one * c ∈ FW24 ∧
  a * b ∈ FW24 ∧ a * c ∈ FW24 ∧ b * c ∈ FW24 ∧
  one * a * b ∈ FW24 ∧ one * a * c ∈ FW24 ∧ one * b * c ∈ FW24 ∧
  a * b * c ∈ FW24 ∧
  one * a * b * c ∈ FW24

instance (one a b c : ℕ) : Decidable (Closed4_24 one a b c) := by
  unfold Closed4_24
  infer_instance

-- 新增 4 元闭包（FW24 口径）：(1,2,3,4) 阶乘塔底（全积 24=4!）、(1,2,3,8)、(1,2,4,6)
theorem new_closed4_24 :
    Closed4_24 1 2 3 4 ∧ Closed4_24 1 2 3 8 ∧ Closed4_24 1 2 4 6 := by
  native_decide

-- 4 元闭包完备性（FW24 口径）：含 1 的 4 元闭包 ⟺ 非 1 部分 ∈ closure3List24
theorem closed4_24_l1_mem_list :
    (∀ a ∈ Finset.Icc 2 16, ∀ b ∈ Finset.Icc 2 16, ∀ c ∈ Finset.Icc 2 16,
      Closed4_24 1 a b c ↔ (a, b, c) ∈ closure3List24) := by
  native_decide

end MUFPFormalization.ClosureFamily
