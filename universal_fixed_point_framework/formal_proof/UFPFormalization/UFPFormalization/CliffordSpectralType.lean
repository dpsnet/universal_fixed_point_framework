import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic

namespace UFPFormalization

/-!
## Cl(1,7) 生成元谱类型（B1 推进：Γ 谱 ↔ 可证编码层的代数骨架）

代数事实（约定内确定，机器可证；数值复核 scripts/paperX_cl17_gamma_spectrum.py 11/11）：

  α) A² = +I ⟹ 特征值 ∈ {±1}（实谱）
  β) A² = −I ⟹ 特征值 ∈ {±i}（纯虚谱）
  γ) 同类双线性对 (AB)² = −I（反对易 + 同类平方 ε²=1，**约定无关**）⟹ 纯虚谱
     —— 静默子代数 Cl(0,4) 的 SO(4) 旋转生成元（同类对）纯虚谱 ±i/2

约定登记（ζ，笔记 §4.7 S2，2026-08-16 修正）：**统一约定 = 数学标准 Cl(1,7)**（1 正号时间²=+1 + 7 负号空间²=−1），
与主导脚本一致（`paperX_cl17_first_principle.py` / `gammas_fixed.py`，Dirac 度规）。
历史探针 `paperX_delta_spatial_probe.py` 用时间²=−1（= 主导约定表示整体乘 i，酉等价，
探针判定不变）。`Clifford.lean` 的 e_01/e_10 命名颠倒已于 2026-08-16 修正为数学标准。
**单生成元谱类型标签随约定翻转**；双线性对谱类型约定无关。
-/

/-- 矩阵特征值（本项目层面定义）：∃ 非零向量 v，A v = mu v -/
def HasEig {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) (mu : ℂ) : Prop :=
  ∃ v : Fin n → ℂ, v ≠ 0 ∧ A.mulVec v = mu • v

/-- α) A² = I ⟹ 特征值 ∈ {±1}（实谱）。约定无关：与时间² 符号无关。 -/
theorem eig_sq_eq_one {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) (hA : A * A = 1)
    {mu : ℂ} (hmu : HasEig A mu) : mu = 1 ∨ mu = -1 := by
  rcases hmu with ⟨v, hv0, hv⟩
  have h1 : A.mulVec (A.mulVec v) = v := by
    calc
      A.mulVec (A.mulVec v) = (A * A).mulVec v := by rw [Matrix.mulVec_mulVec]
      _ = v := by rw [hA]; simp
  have h2 : A.mulVec (A.mulVec v) = mu ^ 2 • v := by
    rw [hv, Matrix.mulVec_smul, hv]
    simp [pow_two, smul_smul]
  have h3 : (mu ^ 2 - 1) • v = 0 := by
    rw [sub_smul, sub_eq_zero]
    simpa using h2.symm.trans h1
  have hmu2 : mu ^ 2 = 1 := by
    exact eq_of_sub_eq_zero ((smul_eq_zero.mp h3).resolve_right hv0)
  have hfac : (mu - 1) * (mu + 1) = 0 := by
    calc
      (mu - 1) * (mu + 1) = mu ^ 2 - 1 := by ring
      _ = 0 := by rw [hmu2]; ring
  exact (mul_eq_zero.mp hfac).imp sub_eq_zero.mp add_eq_zero_iff_eq_neg.mp

/-- β) A² = −I ⟹ 特征值 ∈ {±i}（纯虚谱） -/
theorem eig_sq_eq_neg_one {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) (hA : A * A = -1)
    {mu : ℂ} (hmu : HasEig A mu) : mu = Complex.I ∨ mu = -Complex.I := by
  rcases hmu with ⟨v, hv0, hv⟩
  have h1 : A.mulVec (A.mulVec v) = -v := by
    calc
      A.mulVec (A.mulVec v) = (A * A).mulVec v := by rw [Matrix.mulVec_mulVec]
      _ = (-1 : Matrix (Fin n) (Fin n) ℂ).mulVec v := by rw [hA]
      _ = -v := by rw [Matrix.neg_mulVec]; simp
  have h2 : A.mulVec (A.mulVec v) = mu ^ 2 • v := by
    rw [hv, Matrix.mulVec_smul, hv]
    simp [pow_two, smul_smul]
  have h3 : (mu ^ 2 + 1) • v = 0 := by
    rw [add_smul, add_eq_zero_iff_eq_neg]
    simpa using h2.symm.trans h1
  have hmu2 : mu ^ 2 = -1 := by
    exact add_eq_zero_iff_eq_neg.mp ((smul_eq_zero.mp h3).resolve_right hv0)
  have hfac : (mu - Complex.I) * (mu + Complex.I) = 0 := by
    calc
      (mu - Complex.I) * (mu + Complex.I) = mu ^ 2 - Complex.I ^ 2 := by ring
      _ = mu ^ 2 + 1 := by rw [Complex.I_sq]; ring
      _ = 0 := by rw [hmu2]; ring
  exact (mul_eq_zero.mp hfac).imp sub_eq_zero.mp add_eq_zero_iff_eq_neg.mp

/-- 一般化：A² = c·I ⟹ 特征值 λ² = c（谱值嵌入构造 A_R = γI + S 的代数骨架） -/
theorem eig_sq_eq_scalar {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) {c : ℂ} (hA : A * A = c • 1)
    {mu : ℂ} (hmu : HasEig A mu) : mu ^ 2 = c := by
  rcases hmu with ⟨v, hv0, hv⟩
  have h1 : A.mulVec (A.mulVec v) = c • v := by
    calc
      A.mulVec (A.mulVec v) = (A * A).mulVec v := by rw [Matrix.mulVec_mulVec]
      _ = (c • (1 : Matrix (Fin n) (Fin n) ℂ)).mulVec v := by rw [hA]
      _ = c • v := by rw [Matrix.smul_mulVec]; simp
  have h2 : A.mulVec (A.mulVec v) = mu ^ 2 • v := by
    rw [hv, Matrix.mulVec_smul, hv]
    simp [pow_two, smul_smul]
  have h3 : (mu ^ 2 - c) • v = 0 := by
    rw [sub_smul, sub_eq_zero]
    simpa using h2.symm.trans h1
  exact eq_of_sub_eq_zero ((smul_eq_zero.mp h3).resolve_right hv0)

/-- 推论：静默 SO(4) 旋转生成元 S² = −(1/4)·I ⟹ 特征值 ∈ {±i/2}（纯虚谱，约定无关） -/
theorem sq_neg_quarter_eig {n : ℕ} (S : Matrix (Fin n) (Fin n) ℂ)
    (hS : S * S = -(1 / 4 : ℂ) • 1) {mu : ℂ} (hmu : HasEig S mu) :
    mu = Complex.I / 2 ∨ mu = -(Complex.I / 2) := by
  have hmu2 : mu ^ 2 = -(1 / 4 : ℂ) := eig_sq_eq_scalar S hS hmu
  have hfac : (mu - Complex.I / 2) * (mu + Complex.I / 2) = 0 := by
    calc
      (mu - Complex.I / 2) * (mu + Complex.I / 2) = mu ^ 2 - (Complex.I / 2) ^ 2 := by ring
      _ = mu ^ 2 + 1 / 4 := by
        have hIsq2 : (Complex.I / 2 : ℂ) ^ 2 = -1 / 4 := by
          rw [show (Complex.I / 2 : ℂ) ^ 2 = Complex.I ^ 2 / 2 ^ 2 by ring]
          rw [Complex.I_sq]
          norm_num
        rw [hIsq2]
        ring
      _ = 0 := by rw [hmu2]; ring
  exact (mul_eq_zero.mp hfac).imp sub_eq_zero.mp add_eq_zero_iff_eq_neg.mp

/-- γ) 同类双线性对 (AB)² = −I（反对易 + 同类平方 ε²=1，约定无关） -/
theorem bivec_sq_eq_neg_one {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℂ) {ε : ℂ} (hε : ε * ε = 1)
    (hA : A * A = ε • 1) (hB : B * B = ε • 1) (hAB : A * B = -(B * A)) :
    (A * B) * (A * B) = -1 := by
  have hBA : B * A = -(A * B) := by rw [hAB]; simp
  calc
    (A * B) * (A * B) = (A * (B * A)) * B := by
      conv_lhs =>
        rw [← Matrix.mul_assoc]
        pattern (A * B) * A
        rw [Matrix.mul_assoc]
    _ = (A * (-(A * B))) * B := by rw [hBA]
    _ = -((A * A) * (B * B)) := by
      rw [Matrix.mul_neg]
      rw [Matrix.neg_mul]
      congr 1
      rw [Matrix.mul_assoc, Matrix.mul_assoc, ← Matrix.mul_assoc]
    _ = -1 := by
      rw [hA, hB]
      have hsmul : (ε • (1 : Matrix (Fin n) (Fin n) ℂ)) * (ε • (1 : Matrix (Fin n) (Fin n) ℂ)) = 1 := by
        rw [Matrix.smul_mul, Matrix.mul_smul]
        rw [Matrix.one_mul]
        rw [smul_smul]
        rw [hε]
        simp
      rw [hsmul]

end UFPFormalization
