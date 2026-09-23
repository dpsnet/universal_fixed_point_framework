import MUFPFormalization.BerryChern

namespace MUFPF

open Matrix Complex

section PureAlgebra

variable {E F : Type*} [AddCommGroup E] [AddCommGroup F] [Module ℂ E] [Module ℂ F]

/-- **子空间乘积 → 类型级乘积的线性等价（`finrank(S.prod T)=finrank S + finrank T` 的桥）**：
    `Submodule.prod S T` 是 $E\times F$ 的子空间，作为类型其载体为满足
    `x.1 ∈ S ∧ x.2 ∈ T` 的二元组；把它线性地重排为类型级乘积 `S × T`。
    这是 §2.15 秩映射直和加性的构造核：收紧子空间乘积的 finrank 为**分量之和**。 -/
def prodSubmoduleLinearEquiv (S : Submodule ℂ E) (T : Submodule ℂ F) :
    Submodule.prod S T ≃ₗ[ℂ] S × T where
  toFun x := ⟨⟨(x : E × F).1, (Submodule.mem_prod).mp x.property |>.1⟩,
             ⟨(x : E × F).2, (Submodule.mem_prod).mp x.property |>.2⟩⟩
  invFun y := ⟨((y.1 : E), (y.2 : F)), (Submodule.mem_prod).mpr ⟨y.1.property, y.2.property⟩⟩
  map_add' := by intro x y; ext <;> rfl
  map_smul' := by intro a x; ext <;> rfl
  left_inv := by intro x; ext <;> rfl
  right_inv := by intro y; ext <;> rfl

/-- **直和的幂等性（块对角投影仍是投影）**：幂等 $P,Q$ 的直和（块对角）算子
    `P ⊕ Q := P.prodMap Q` 仍幂等——谱投影直和保持投影性质，这是 K₀ 加法幺半
    结构的代数基础。证明经 `LinearMap.prodMap_mul`（直和乘法=分量乘法）。 -/
theorem directSum_idempotent (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F)
    (hP : IsIdempotentElem P) (hQ : IsIdempotentElem Q) :
    IsIdempotentElem (P.prodMap Q) := by
  calc
    (P.prodMap Q) * (P.prodMap Q) = (P * P).prodMap (Q * Q) :=
      (LinearMap.prodMap_mul P P Q Q).symm
    _ = P.prodMap Q := by rw [hP, hQ]

variable [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]

/-- **秩映射的直和加性（rank(P ⊕ Q) = rank P + rank Q）**：同秩（同维像）幂等投影
    P、Q 的直和 `P.prodMap Q : E × F →ₗ E × F` 的秩等于分量秩之和。这是把 §2.14
    「秩唯一决定酉等价类」（完全不变量）升级为 **K₀(ℂ) ≅ ℤ 群同态**的关键加性
    性质：`rank` 沿直和相加。证明：`range (P.prodMap Q) = range P .prod range Q`
    （`LinearMap.range_prodMap`）+ 子空间乘积线性等价（`prodSubmoduleLinearEquiv`）
    + `Module.finrank_prod`（类型级乘积加性）。 -/
theorem directSum_rank_add (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F) :
    Module.finrank ℂ (LinearMap.range (P.prodMap Q)) =
      Module.finrank ℂ (LinearMap.range P) + Module.finrank ℂ (LinearMap.range Q) := by
  calc
    Module.finrank ℂ (LinearMap.range (P.prodMap Q))
        = Module.finrank ℂ (Submodule.prod (LinearMap.range P) (LinearMap.range Q)) := by
          rw [LinearMap.range_prodMap]
    _ = Module.finrank ℂ (LinearMap.range P × LinearMap.range Q) :=
          (prodSubmoduleLinearEquiv (LinearMap.range P) (LinearMap.range Q)).finrank_eq
    _ = Module.finrank ℂ (LinearMap.range P) + Module.finrank ℂ (LinearMap.range Q) :=
          Module.finrank_prod

end PureAlgebra

end MUFPF