import MUFPFormalization.BerryChern

namespace MUFPF

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [FiniteDimensional ℂ E]

/-- 引理 A：同维有限维子空间间存在等距等价。 -/
theorem exists_isometry_of_eq_finrank (V W : Submodule ℂ E)
    (h : Module.finrank ℂ V = Module.finrank ℂ W) : Nonempty (V ≃ₗᵢ[ℂ] W) := by
  let bV : OrthonormalBasis (Fin (Module.finrank ℂ V)) ℂ V := stdOrthonormalBasis ℂ V
  let bW : OrthonormalBasis (Fin (Module.finrank ℂ W)) ℂ W := stdOrthonormalBasis ℂ W
  let f : Fin (Module.finrank ℂ V) ≃ Fin (Module.finrank ℂ W) := Equiv.cast (congrArg Fin h)
  exact ⟨bV.equiv bW f⟩

/-- 引理 B：把子空间等距等价延伸到全空间等距等价
    （通过 `LinearIsometry.extend`：在子空间为 e，在正交补上为其像的正交补）。 -/
noncomputable def linearIsometryEquiv_of_submodule (S T : Submodule ℂ E)
    (e : S ≃ₗᵢ[ℂ] T) : E ≃ₗᵢ[ℂ] E := by
  let L : S →ₗᵢ[ℂ] E := T.subtypeₗᵢ.comp e.toLinearIsometry
  have hfin : Module.finrank ℂ E = Module.finrank ℂ E := rfl
  exact (LinearIsometry.extend L).toLinearIsometryEquiv hfin

/-- 引理 B 作用：U 在子空间 S 上等于 e（U∘ι_S = ι_T∘e）。 -/
theorem linearIsometryEquiv_of_submodule_apply (S T : Submodule ℂ E)
    (e : S ≃ₗᵢ[ℂ] T) (s : S) :
    (linearIsometryEquiv_of_submodule S T e : E → E) (s : E) = (e s : E) := by
  unfold linearIsometryEquiv_of_submodule
  simp [LinearIsometry.extend_apply]

/-- 引理 C：U 把正交补 Sᗮ 映到 Tᗮ（等距保持内积 + e 满射覆盖 T）。 -/
theorem linearIsometryEquiv_of_submodule_mem_orthogonal (S T : Submodule ℂ E)
    (e : S ≃ₗᵢ[ℂ] T) {b : E} (hb : b ∈ Sᗮ) :
    linearIsometryEquiv_of_submodule S T e b ∈ Tᗮ := by
  rw [Submodule.mem_orthogonal']
  intro t ht
  rcases e.surjective ⟨t, ht⟩ with ⟨s, hst⟩
  calc
    ⟪linearIsometryEquiv_of_submodule S T e b, t⟫
        = ⟪linearIsometryEquiv_of_submodule S T e b, (e s : E)⟫ := by rw [hst]
    _ = ⟪linearIsometryEquiv_of_submodule S T e b,
          (linearIsometryEquiv_of_submodule S T e (s : E))⟫ := by
            rw [linearIsometryEquiv_of_submodule_apply S T e s]
    _ = ⟪b, (s : E)⟫ := by
            rw [LinearIsometryEquiv.inner_map_map (linearIsometryEquiv_of_submodule S T e) b (s : E)]
    _ = 0 := (Submodule.mem_orthogonal' (b : E)).mp hb (s : E) s.property

/-- 主定理：同秩自伴幂等投影酉等价（Q = U∘P∘U⁻¹，U†=U⁻¹）。 -/
theorem same_rank_selfAdjoint_idempotent_unitary_conj (P Q : E →ₗ[ℂ] E)
    (hPid : IsIdempotentElem P) (hPsa : LinearMap.IsSelfAdjoint P)
    (hQid : IsIdempotentElem Q) (hQsa : LinearMap.IsSelfAdjoint Q)
    (hr : Module.finrank ℂ (LinearMap.range P) = Module.finrank ℂ (LinearMap.range Q)) :
    ∃ U : E ≃ₗᵢ[ℂ] E, Q ∘ₗ U.toLinearMap = U.toLinearMap ∘ₗ P := by
  classical
  have hkerP : (LinearMap.range P)ᗮ = LinearMap.ker P :=
    (selfAdjoint_idempotent_ker_eq_orthogonal P hPsa).symm
  have hkerQ : (LinearMap.range Q)ᗮ = LinearMap.ker Q :=
    (selfAdjoint_idempotent_ker_eq_orthogonal Q hQsa).symm
  rcases exists_isometry_of_eq_finrank (LinearMap.range P) (LinearMap.range Q) hr with ⟨e, _⟩
  let U : E ≃ₗᵢ[ℂ] E := linearIsometryEquiv_of_submodule (LinearMap.range P) (LinearMap.range Q) e
  refine ⟨U, ?_⟩
  ext x
  have hPc : IsCompl (LinearMap.range P) (LinearMap.ker P) :=
    IsIdempotentElem.isCompl (f := P) hPid
  let eP : (LinearMap.range P × LinearMap.ker P) ≃ₗ[ℂ] E := Submodule.prodEquivOfIsCompl hPc
  rcases eP.surjective x with ⟨pr, hpr⟩
  rw [← hpr]
  rcases pr with ⟨a, b⟩
  have hUa : U (a : E) = (e a : E) := by
    simpa using (linearIsometryEquiv_of_submodule_apply (LinearMap.range P) (LinearMap.range Q) e a)
  have hUa_mem : U (a : E) ∈ LinearMap.range Q := by
    rw [hUa]; exact (e a).property
  have hQidrange : Q (U (a : E)) = U (a : E) := by
    exact idempotent_apply_of_mem_range Q hQid ⟨U (a : E), hUa_mem⟩
  have hUb_mem_ker : U (b : E) ∈ LinearMap.ker Q := by
    have hbb : (b : E) ∈ (LinearMap.range P)ᗮ := by simpa [hkerP] using b.property
    have hUp := linearIsometryEquiv_of_submodule_mem_orthogonal
      (LinearMap.range P) (LinearMap.range Q) e hbb
    simpa [hkerQ] using hUp
  have hQzero : Q (U (b : E)) = 0 := by
    exact idempotent_apply_mem_ker Q ⟨U (b : E), hUb_mem_ker⟩
  have hLP : P (eP (a, b)) = (a : E) := by
    calc
      P (eP (a, b)) = P ((a : E) + (b : E)) := by rw [Submodule.coe_prodEquivOfIsCompl']
      _ = P (a : E) + P (b : E) := by simp
      _ = (a : E) := by
        rw [idempotent_apply_of_mem_range P hPid a, idempotent_apply_mem_ker P b]
        simp
  have hU_lin : U (eP (a, b)) = U (a : E) + U (b : E) := by
    calc
      U (eP (a, b)) = U ((a : E) + (b : E)) := by rw [Submodule.coe_prodEquivOfIsCompl']
      _ = U (a : E) + U (b : E) := by simp
  calc
    Q (U (eP (a, b))) = Q (U (a : E) + U (b : E)) := by rw [hU_lin]
    _ = Q (U (a : E)) + Q (U (b : E)) := by simp
    _ = U (a : E) + 0 := by rw [hQidrange, hQzero]
    _ = U (a : E) := by simp
    _ = U (P (eP (a, b))) := by rw [← hLP]

end MUFPF