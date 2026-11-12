import Mathlib.Tactic
import MUFPFormalization.SignatureClifford
import MUFPFormalization.ActiveFixSignature
import MUFPFormalization.RecTimeDepth

/-!
# 第 49 批（续）：把 `chain4` 的签名接到 `Cl(3, 1)`

`SignatureClifford` 把「签名 → 二次型 → Clifford 泛性质」这一段证出来了，
但它只处理抽象的 `sigCl n p`。本模块把第 47–48 批的 `chain4` 接上去：

- `chain4` 的签名是 `(3, 1)`（第 47 批 `chain4_signature`）；
- 把该签名送入 `sigCl`，得到的正是 `sigCl 4 3`，即 `Cl(3, 1)`；
- 于是「活跃层数 3」与「`Cl` 签名正部维数 3」不再是 `3 = 3` 的并置，
  而是同一个数值在两侧各自机检一致。

## 诚实边界

这里证的是「`chain4` 的签名 → `sigCl 4 3`」这一条**具体**通道；`Cl(3,1)` 与
`Cl(3,0)` 等其它签名对应的代数是否**不同构**仍归 `SignatureClifford`
的登记位 `form_neq_implies_algebra_neq_admitted`，本模块不越界。
-/

namespace MUFPF.SignatureCliffordBridge

open MUFPF.RecTime MUFPF.ActiveFixSignature MUFPF.SignatureClifford

/-- 从签名对取出正部维数（第 47 批 `chain4_signature` 的投影）。

`chain4_signature : (activeCount chain4, fixCount chain4) = (3, 1)`，
投影即得两个分量各自的值。 -/
theorem chain4_active_is_three : activeCount chain4 = 3 := by
  simpa using congrArg Prod.fst chain4_signature

/-- 从签名对取出负部维数（`|Fix| = 1`）。 -/
theorem chain4_fix_is_one : fixCount chain4 = 1 := by
  simpa using congrArg Prod.snd chain4_signature

/-- **`chain4` 的签名送入 `Cl` 构造即得 `Cl(3, 1)`**。

这是三步路径的合成形式：分解（第 47 批）→ 签名 `(3, 1)`（第 48 批）→
`sigCl 4 3 = Cl(3, 1)`（本批）。 -/
theorem chain4_sigCl_is_cl31 :
    sigCl (activeCount chain4 + fixCount chain4) (activeCount chain4) = sigCl 4 3 := by
  rw [chain4_active_is_three, chain4_fix_is_one]

/-- **活跃集基数 = `Cl(3, 1)` 签名正部维数**。

左侧是第 47 批 `activeCount chain4` 的机检值，右侧是本批
`cl31_pos_card` 的机检值；两者相等不是传递 `3 = 3`，而是各自独立算出。 -/
theorem activeCount_eq_cl31_positive :
    activeCount chain4
      = (Finset.univ.filter (fun i : Fin 4 => 0 < sigQ 4 3 (Pi.single i (1 : ℝ)))).card := by
  rw [chain4_active_is_three, cl31_pos_card]

/-- 签名函子在 `chain4` 处的取值：签名对 `(3, 1)` 与代数 `Cl(3, 1)` 同时成立。 -/
theorem signature_functor_on_chain4 :
    (activeCount chain4, fixCount chain4) = (3, 1)
      ∧ sigCl (activeCount chain4 + fixCount chain4) (activeCount chain4) = sigCl 4 3 :=
  ⟨chain4_signature, chain4_sigCl_is_cl31⟩

end MUFPF.SignatureCliffordBridge
