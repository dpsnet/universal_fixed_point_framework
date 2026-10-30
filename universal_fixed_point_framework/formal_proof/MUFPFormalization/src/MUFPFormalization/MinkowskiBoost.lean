import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import MUFPFormalization.Clifford

/-! # 1+1 闵氏 boost 层（时间偏转的谱流实现）

用户口述："时间在 MUFPF 中是分层的；'在时间中移动' = 沿 rapidity（谱流内禀时间）方向演化；
物理层'改变时间轴'（θ）⟷ 谱层'沿 rapidity 谱流移动'（φ）——同一谱流的两种表述；coshφ=secθ=γ。"
本节给出该口述的矩阵实现：boost = SO(1,1) 双曲旋转（1+1 闵氏时间偏转），
rapidity 可加（boost_add）→"在时间中移动"的代数核心；双曲指数 exp(φJ')（boostExp）与
欧氏 exp(θJ)（rotExp，见 ForceAverageIsotropy）互补——J'=e_10 平方 +1（类空-类空
双向量），J=e_01 平方 −1（欧氏双向量）：**两正交投影的生成元互补对**（Cl(1,1)⊕Cl(2,0)）。
-/

namespace MUFPF.MinkowskiBoost

/-- 1+1 boost（双曲旋转）：rapidity 谱流参数 φ 的矩阵实现。 -/
noncomputable def boost (φ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cosh φ, Real.sinh φ; Real.sinh φ, Real.cosh φ]

/-- 双曲生成元（Cl(1,1) 时空双向量，平方 = +1；与欧氏 J=e_01 平方 −1 互补）。 -/
def Jprime : Matrix (Fin 2) (Fin 2) ℝ :=
  !![0, 1; 1, 0]

/-- 1+1 闵氏度规 η = diag(1,−1)。 -/
def MinkowskiEta : Matrix (Fin 2) (Fin 2) ℝ :=
  !![1, 0; 0, -1]

/-- ★★ rapidity 可加性（矩阵实现）：boost(φ₁+φ₂)=boost(φ₁)·boost(φ₂)
    ——"在时间中移动 = 沿 rapidity 谱流演化"，每次递归步进 Δφ 线性累积。 -/
theorem boost_add (φ₁ φ₂ : ℝ) : boost (φ₁ + φ₂) = boost φ₁ * boost φ₂ := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [boost, Matrix.mul_apply, Real.cosh_add, Real.sinh_add] <;> ring_nf

/-- ★★ boost 保持闵氏度量（保光锥 = SO(1,1) 定义）：(boost φ)ᵀ·η·(boost φ) = η
    ——时间偏转谱流不改变时空间隔（cosh²−sinh²=1 的度量形态，"偏转时间轴"
    是双曲旋转而非剪切）。 -/
theorem boost_preserves_minkowski_metric (φ : ℝ) :
    Matrix.transpose (boost φ) * MinkowskiEta * boost φ = MinkowskiEta := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [boost, MinkowskiEta, Matrix.mul_apply]
  · nlinarith [Real.cosh_sq_sub_sinh_sq φ]
  · ring
  · ring
  · nlinarith [Real.cosh_sq_sub_sinh_sq φ]

/-- ★★ 双曲生成元平方 = +1：J'² = 1（Cl(1,1) 时空双向量；
    与欧氏 e_01 平方 = −1 互补——两正交投影的生成元互补对）。 -/
theorem Jprime_sq : Jprime * Jprime = (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Jprime, Matrix.mul_apply]

/-- 双曲指数：boostExp(φ)=coshφ·1+sinhφ·J'（exp(φJ')，因 J'²=1）。 -/
noncomputable def boostExp (φ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  Real.cosh φ • (1 : Matrix (Fin 2) (Fin 2) ℝ) + Real.sinh φ • Jprime

/-- ★★ 双曲指数 = boost：boostExp φ = boost φ（与欧氏 rotExp θ=rot θ 对称：
    紧群 exp(θJ)=旋转、非紧 exp(φJ')=boost——Rec/Sp 对偶的两侧实现）。 -/
theorem boostExp_eq_boost (φ : ℝ) : boostExp φ = boost φ := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [boostExp, boost, Jprime]

/-- ★★ Clifford 桥：Jprime = e_01 · e_10——Cl(1,1) 时空双向量
    = 空间生成元 × 时间生成元（平方 +1）；与 e_01 = J（欧氏，平方 −1）互补，
    构成"两正交投影"的生成元互补对。 -/
theorem Jprime_eq_e01_mul_e10 :
    Jprime = e_01 (rfl : 2 = 2) * e_10 (rfl : 2 = 2) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    (rw [show e_01 (rfl : 2 = 2) = (!![0, -1; 1, 0] : Matrix (Fin 2) (Fin 2) ℝ) from rfl,
        show e_10 (rfl : 2 = 2) = (!![1, 0; 0, -1] : Matrix (Fin 2) (Fin 2) ℝ) from rfl];
     simp [Jprime, Matrix.mul_apply])

/-- ★★ 双曲指数加性（谱流可加性的连续侧）：boostExp(φ₁+φ₂)=boostExp φ₁ · boostExp φ₂。 -/
theorem boostExp_add (φ₁ φ₂ : ℝ) : boostExp (φ₁ + φ₂) = boostExp φ₁ * boostExp φ₂ := by
  rw [boostExp_eq_boost, boostExp_eq_boost, boostExp_eq_boost]
  exact boost_add φ₁ φ₂

/-- ★★ 1+1 离散⟹连续桥（指数形态）：boostExp(n·φ) = (boostExp φ)^n
    ——递归层时钟 n 步 = 谱参数 n·φ 一步到位："每次递归=时间递进一层"在
    1+1 时间偏转层的代数实现（与 ForceAverageIsotropy.rotExp_nat_mul 构成
    紧/非紧双镜像：欧氏旋转侧与双曲 boost 侧同为整数幂指数律）。 -/
theorem boostExp_nat_mul (n : ℕ) (φ : ℝ) : boostExp (n • φ) = (boostExp φ) ^ n := by
  induction n with
  | zero =>
      ext i j
      fin_cases i <;> fin_cases j <;> simp [boostExp, Real.cosh_zero, Real.sinh_zero]
  | succ n ih =>
      calc
        boostExp ((n + 1) • φ) = boostExp (n • φ + φ) := by
            rw [succ_nsmul]
        _ = boostExp (n • φ) * boostExp φ := by
            rw [boostExp_add]
        _ = (boostExp φ) ^ n * boostExp φ := by
            rw [ih]
        _ = (boostExp φ) ^ (n + 1) := by
            rw [← pow_succ]

/-- ★★ 1+1 离散⟹连续桥（旋转形态）：boost(n·φ) = (boost φ)^n
    ——boost 形态时钟步进 ⟷ 谱参数线性累积（与 boostExp 版一致，
    经 boostExp_eq_boost 互译）。 -/
theorem boost_nat_mul (n : ℕ) (φ : ℝ) : boost (n • φ) = (boost φ) ^ n := by
  induction n with
  | zero =>
      ext i j
      fin_cases i <;> fin_cases j <;> simp [boost, Real.cosh_zero, Real.sinh_zero]
  | succ n ih =>
      calc
        boost ((n + 1) • φ) = boost (n • φ + φ) := by
            rw [succ_nsmul]
        _ = boost (n • φ) * boost φ := by
            rw [boost_add]
        _ = (boost φ) ^ n * boost φ := by
            rw [ih]
        _ = (boost φ) ^ (n + 1) := by
            rw [← pow_succ]

/-! ## Cl(1,1) 生成元代数 + Dirac 平方（#49）

时空 Clifford 层的代数关系：空间生成元 e_01（平方−1）与时间生成元 e_10（平方+1）
的乘积反对易（Cl(1,1) 非交换），交换子 [e_01,e_10]=2·J' 恰生成双曲生成元——
与 #24 "Δ 携带群作用（换位子结构内禀）"同构的时空层实现；
Dirac 平方 (E·e_10 − p·e_01)² = (E²−p²)·1：质量壳是 Dirac 算符平方的本征值。 -/

/-- ★★ Cl(1,1) 时空双向量反对易：e_01·e_10 = −(e_10·e_01)
    ——空间生成元 × 时间生成元非交换（时空代数的非交换性；
    与欧氏 e_01²=−1 互补：Cl(1,1) 的生成元乘积为双曲生成元且反对易）。 -/
theorem e01_mul_e10_anticomm :
    e_01 (rfl : 2 = 2) * e_10 (rfl : 2 = 2)
      = -(e_10 (rfl : 2 = 2) * e_01 (rfl : 2 = 2)) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [e_01, e_10, Matrix.mul_fin_two, Matrix.neg_apply]

/-- ★★ Cl(1,1) 交换子生成双曲生成元：[e_01,e_10] = e_01·e_10 − e_10·e_01 = 2·J'
    ——时空生成元交换子恰为 boost 生成元（Δ⟹群作用在时空层的实现：
    非交换性 ⟹ 双曲层生成元，与 commutator_twice_of_anticomm 同构）。 -/
theorem cl11_commutator_generates_boost :
    e_01 (rfl : 2 = 2) * e_10 (rfl : 2 = 2) - e_10 (rfl : 2 = 2) * e_01 (rfl : 2 = 2)
      = 2 • Jprime := by
  have hjo : e_10 (rfl : 2 = 2) * e_01 (rfl : 2 = 2) = -Jprime := by
    calc
      e_10 (rfl : 2 = 2) * e_01 (rfl : 2 = 2) = -(-(e_10 (rfl : 2 = 2) * e_01 (rfl : 2 = 2))) := by simp
      _ = -(e_01 (rfl : 2 = 2) * e_10 (rfl : 2 = 2)) := by rw [e01_mul_e10_anticomm]
      _ = -Jprime := by rw [Jprime_eq_e01_mul_e10]
  rw [e01_mul_e10_anticomm]
  simp [hjo]
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [Jprime, Matrix.mul_apply, Pi.add_apply, Pi.smul_apply, Fin.sum_univ_two]
  all_goals
    try norm_num
  all_goals
    try rfl
  all_goals
    try native_decide

/-- ★★ Dirac 平方（1+1）：(E·e_10 − p·e_01)² = (E²−p²)·1
    ——Clifford 代数表述：E²−p² 是 Dirac 算符平方的标量系数（e_10²=+1、e_01²=−1、
    反对易项 −Ep(e_10·e_01+e_01·e_10)=0）。质量壳 = Dirac 算符平方的本征值条件。 -/
theorem clifford_dirac_square (E p : ℝ) :
    (E • e_10 (rfl : 2 = 2) - p • e_01 (rfl : 2 = 2)) ^ 2
      = (E ^ 2 - p ^ 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  rw [pow_two]
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [e_01, e_10, Matrix.mul_fin_two, smul_eq_mul]
    ring

/-! ## Dirac 质量谱分解（#50）

Dirac 算符 D = E·e_10 − p·e_01 的质量层结构：D 无迹（谱对称 ±λ，tr(D)=0——
本征值以 0 为对称中心），壳上 E²−p²=m² ⟹ (D−m·1)(D+m·1)=0（零因子分解：
Dirac 算符在壳上分解为 ±m 两个核，质量 = Dirac 核，两互补投影 Π± 的前身——
"态射/右伴随两正交投影"直觉在质量层的投影对落地，与 #40 群平均投影对同构）。 -/

/-- ★★ Dirac 算符无迹：tr(E·e_10 − p·e_01) = 0
    ——谱以 0 对称（±λ 本征值对；质量壳上 λ²=m² ⟹ 谱恰为 ±m）。 -/
theorem clifford_dirac_trace_zero (E p : ℝ) :
    Matrix.trace (E • e_10 (rfl : 2 = 2) - p • e_01 (rfl : 2 = 2)) = 0 := by
  simp [Matrix.trace, Matrix.diag, sum_fin_two, e_01, e_10, smul_eq_mul]

/-- ★★ 壳上零因子分解：E²−p²=m² ⟹ (D−m·1)(D+m·1)=0
    ——Dirac 算符在质量壳上分解为 ±m 两个核（零因子对；质量=Dirac 核 ±m，
    两互补投影 Π± 的直接前身）。 -/
theorem clifford_dirac_factorization (E p m : ℝ) (hsq : E ^ 2 - p ^ 2 = m ^ 2) :
    (E • e_10 (rfl : 2 = 2) - p • e_01 (rfl : 2 = 2) - m • (1 : Matrix (Fin 2) (Fin 2) ℝ))
      * (E • e_10 (rfl : 2 = 2) - p • e_01 (rfl : 2 = 2) + m • (1 : Matrix (Fin 2) (Fin 2) ℝ))
      = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [e_01, e_10, Matrix.mul_fin_two, smul_eq_mul, Matrix.mul_apply, Fin.sum_univ_two]
    nlinarith [hsq]

/-! ## 1+3 洛伦兹 boost 层（#52，SO(1,3) 显式化第一步）

完整洛伦兹群的对等描述：4×4 沿 x 轴 boost Λ_x(φ)（块结构 = 2×2 boost ⊕ 空间单位），
保闵氏度规 η₄=diag(1,−1,−1,−1)（(Λφ)ᵀ·η₄·Λφ=η₄ —— SO(1,3) 定义），
rapidity 可加（SO(1,3) 内非紧子群），Nat 幂离散⟹连续桥（时间分层在 1+3 的延续）。
与 2×2 boost 层（#41/#44）构成维度升级：空间维加入但时间-空间块保持 SO(1,1) 结构。 -/

/-- 4×4 沿 x 轴洛伦兹 boost（SO(1,3) 非紧子群）：Λ_x(φ)=块对角(boost₂,1₂)。 -/
noncomputable def boost4_x (φ : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![Real.cosh φ, Real.sinh φ, 0, 0;
     Real.sinh φ, Real.cosh φ, 0, 0;
     0, 0, 1, 0;
     0, 0, 0, 1]

/-- 4×4 闵氏度规 η₄ = diag(1,−1,−1,−1)（Cl(1,3) 签名 (+−−−) 的矩阵实现）。 -/
def MinkowskiEta4 : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1, 0, 0, 0;
     0, -1, 0, 0;
     0, 0, -1, 0;
     0, 0, 0, -1]

/-- ★★ 4×4 boost 保闵氏度规：(Λ_x φ)ᵀ·η₄·(Λ_x φ) = η₄
    ——**SO(1,3) 洛伦兹变换的定义**（1+3 时间偏转谱流不改变时空间隔；
    Λ_x 由 2×2 boost 块 ⊕ 空间恒等块组成，cosh²−sinh²=1 的度量形态）。 -/
theorem boost4_x_preserves_minkowski4 (φ : ℝ) :
    Matrix.transpose (boost4_x φ) * MinkowskiEta4 * boost4_x φ = MinkowskiEta4 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [boost4_x, MinkowskiEta4, Matrix.mul_apply, Fin.sum_univ_succ]
    try nlinarith [Real.cosh_sq_sub_sinh_sq φ]

/-- ★★ 4×4 rapidity 可加性：Λ_x(φ₁+φ₂)=Λ_x φ₁·Λ_x φ₂
    ——SO(1,3) 内非紧子群的谱流参数线性累积（与 2×2 boost_add 同构，
    空间块恒等不破坏可加性）。 -/
theorem boost4_x_add (φ₁ φ₂ : ℝ) :
    boost4_x (φ₁ + φ₂) = boost4_x φ₁ * boost4_x φ₂ := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [boost4_x, Matrix.mul_apply, Real.cosh_add, Real.sinh_add, Fin.sum_univ_succ]
    try ring_nf

/-- ★★ 1+3 离散⟹连续桥：Λ_x(n·φ) = (Λ_x φ)^n
    ——递归层时钟 n 步 = 谱参数 n·φ 一步到位（时间分层在完整洛伦兹层的延续，
    与 #44 boost_nat_mul 的 4×4 版本）。 -/
theorem boost4_x_nat_mul (n : ℕ) (φ : ℝ) : boost4_x (n • φ) = (boost4_x φ) ^ n := by
  induction n with
  | zero =>
      ext i j
      fin_cases i <;> fin_cases j <;> simp [boost4_x, Real.cosh_zero, Real.sinh_zero]
  | succ n ih =>
      calc
        boost4_x ((n + 1) • φ) = boost4_x (n • φ + φ) := by
            rw [succ_nsmul]
        _ = boost4_x (n • φ) * boost4_x φ := by
            rw [boost4_x_add]
        _ = (boost4_x φ) ^ n * boost4_x φ := by
            rw [ih]
        _ = (boost4_x φ) ^ (n + 1) := by
            rw [← pow_succ]

/-! ## SO(1,3) 空间旋转层 + 洛伦兹生成元交换子（#53）

SO(1,3) 的紧子群：4×4 绕 z 空间旋转 R_z(θ)（SO(3) 子群），保闵氏度规 η₄、
角度可加、Nat 幂离散⟹连续桥（时间分层在空间侧延续）。
Cl(1,3) 六生成元的第一对混合关系：x-boost 生成元 K_x 与 z-旋转生成元 J_z
的交换子 = −y-boost 生成元 K_y（[K_x,J_z]=−K_y——**洛伦兹代数混合第一环**：
boost×旋转 = 另一 boost，Δ⟹群作用在完整洛伦兹代数的实现）。 -/

/-- 4×4 绕 z 空间旋转（SO(1,3) 紧子群）：R_z(θ)=块(1₁,rot(θ),1₁)。 -/
noncomputable def rot4_z (θ : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1, 0, 0, 0;
     0, Real.cos θ, -Real.sin θ, 0;
     0, Real.sin θ, Real.cos θ, 0;
     0, 0, 0, 1]

/-- x-boost 生成元（4×4）：K_x = Λ_x'(0)（2×2 块内为 J'，空间块为零）。 -/
def K_x : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0, 1, 0, 0;
     1, 0, 0, 0;
     0, 0, 0, 0;
     0, 0, 0, 0]

/-- z-旋转生成元（4×4）：J_z = R_z'(0)（(y,z) 块内为欧氏旋转生成元）。 -/
def J_z : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0, 0, 0, 0;
     0, 0, -1, 0;
     0, 1, 0, 0;
     0, 0, 0, 0]

/-- y-boost 生成元（4×4）：K_y（(x,z) 块内为 J'）。 -/
def K_y : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0, 0, 1, 0;
     0, 0, 0, 0;
     1, 0, 0, 0;
     0, 0, 0, 0]

/-- ★★ 4×4 空间旋转保闵氏度规：R_z θ · η₄ · (R_z θ)ᵀ = η₄
    ——SO(3) 子群正交保度规（紧侧对等描述：旋转不改时空间隔）。 -/
theorem rot4_z_preserves_minkowski4 (θ : ℝ) :
    rot4_z θ * MinkowskiEta4 * Matrix.transpose (rot4_z θ) = MinkowskiEta4 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [rot4_z, MinkowskiEta4, Matrix.mul_apply, Fin.sum_univ_succ]
    try nlinarith [Real.cos_sq_add_sin_sq θ]

/-- ★★ 4×4 空间旋转可加性：R_z(θ₁+θ₂)=R_z θ₁·R_z θ₂
    ——SO(3) 子群角度谱流线性累积（与 boost4_x_add 并列：紧/非紧双可加）。 -/
theorem rot4_z_add (θ₁ θ₂ : ℝ) :
    rot4_z (θ₁ + θ₂) = rot4_z θ₁ * rot4_z θ₂ := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [rot4_z, Matrix.mul_apply, Real.cos_add, Real.sin_add, Fin.sum_univ_succ]
    try ring_nf

/-- ★★ 1+3 空间侧离散⟹连续桥：R_z(n·θ) = (R_z θ)^n
    ——递归层时钟 n 步 = 空间谱参数 n·θ 一步到位（时间分层在空间旋转的延续，
    与 boost4_x_nat_mul 构成 SO(1,3) 紧/非紧双镜像）。 -/
theorem rot4_z_nat_mul (n : ℕ) (θ : ℝ) : rot4_z (n • θ) = (rot4_z θ) ^ n := by
  induction n with
  | zero =>
      ext i j
      fin_cases i <;> fin_cases j <;> simp [rot4_z, Real.cos_zero, Real.sin_zero]
  | succ n ih =>
      calc
        rot4_z ((n + 1) • θ) = rot4_z (n • θ + θ) := by
            rw [succ_nsmul]
        _ = rot4_z (n • θ) * rot4_z θ := by
            rw [rot4_z_add]
        _ = (rot4_z θ) ^ n * rot4_z θ := by
            rw [ih]
        _ = (rot4_z θ) ^ (n + 1) := by
            rw [← pow_succ]

/-- ★★ Cl(1,3) 李代数混合第一环：[K_x,J_z] = −K_y
    ——boost 生成元×旋转生成元的交换子 = 另一 boost 生成元（洛伦兹代数混合结构；
    Δ⟹群作用在完整洛伦兹代数的实现，与 #24 换位子代数同构）。 -/
theorem lorentz_commutator_Kx_Jz : K_x * J_z - J_z * K_x = -K_y := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [K_x, J_z, K_y, Matrix.mul_apply]

/-- ★★ 洛伦兹代数非交换：[K_x,J_z] ≠ 0
    ——洛伦兹生成元非交换（与 commutator_ne_zero_iff_ne_mul 同构：
    洛伦兹群作用由 Δ 换位子结构内禀驱动）。 -/
theorem lorentz_generators_nontrivial : K_x * J_z - J_z * K_x ≠ 0 := by
  intro h
  have h1 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 2) h
  simp [K_x, J_z, K_y] at h1

/-! ## Cl(1,3) 六生成元完整李代数（#54）

完整洛伦兹代数（索引 0=t,1=x,2=y,3=z）：旋转生成元 J_x（y-z 块）、J_y（x-z 块）、
J_z（x-y 块）与 boost 生成元 K_x/K_y/K_z（t-x / t-y / t-z）。
标准交换子表：so(3) 封闭 [J_i,J_j]=ε_ijk·J_k；混合 [J_i,K_j]=ε_ijk·K_k；
**boost 交换 [K_i,K_j]=−ε_ijk·J_k**（两 boost 复合=旋转——Wigner 转动/Thomas 进化的
代数根）；同轴交换 [J_x,K_x]=0。Δ⟹群作用在完整洛伦兹代数的实现闭合。 -/

/-- 绕 x 旋转生成元（4×4，y-z 块内欧氏旋转生成元）。 -/
def J_x : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0, 0, 0, 0;
     0, 0, 0, 0;
     0, 0, 0, -1;
     0, 0, 1, 0]

/-- 绕 y 旋转生成元（4×4，x-z 块内欧氏旋转生成元）。 -/
def J_y : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0, 0, 0, 0;
     0, 0, 0, 1;
     0, 0, 0, 0;
     0, -1, 0, 0]

/-- z-boost 生成元（4×4，t-z 块内为 J'）。 -/
def K_z : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0, 0, 0, 1;
     0, 0, 0, 0;
     0, 0, 0, 0;
     1, 0, 0, 0]

/-- ★★ so(3) 旋转子代数封闭：[J_x,J_y]=J_z
    ——空间旋转生成元闭合（旋转群的三维李代数，紧侧完整）。 -/
theorem so3_commutator_Jx_Jy : J_x * J_y - J_y * J_x = J_z := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [J_x, J_y, J_z, Matrix.mul_apply]

/-- ★★ 混合交换子：[J_x,K_y]=K_z（旋转×boost = boost）
    ——洛伦兹混合代数的正环（与 #53 [K_x,J_z]=−K_y 同为 ε_ijk·K_k 形态）。 -/
theorem lorentz_commutator_Jx_Ky : J_x * K_y - K_y * J_x = K_z := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [J_x, K_y, K_z, Matrix.mul_apply]

/-- ★★ boost 交换子：[K_x,K_y]=−J_z（**boost×boost = 旋转**）
    ——两 boost 复合产生旋转：Wigner 转动/Thomas 进化的代数根；
    "时间偏转的组合产生空间结构（旋转）"，Δ⟹群作用的完整洛伦兹实现。 -/
theorem lorentz_commutator_Kx_Ky : K_x * K_y - K_y * K_x = -J_z := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [K_x, K_y, J_z, Matrix.mul_apply]

/-- ★★ 同轴交换：[J_x,K_x]=0
    ——同一轴上的旋转与 boost 生成元交换（不相交块：J_x 作用 y-z、K_x 作用 t-x）。 -/
theorem lorentz_commutator_Jx_Kx : J_x * K_x - K_x * J_x = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [J_x, K_x, Matrix.mul_apply]

/-! ## boost 共轭层（#55，缺口②第一环）

旋转侧有 groupAverage（C₄ 等变平均⟹各向同性 λI，#23/#40）；boost 侧的对等
（等变）描述第一步：**boost 共轭** T ↦ B(φ)·T·B(φ)ᵀ 的结构性质——
对称保持（闭包基础）、迹按 boost(2φ) 谱流演化（质量读数在非紧侧的变换律）、
无迹对称张量的 boost 轨道显式参数化（各向异性 b 与对角混合，**非紧侧无有限
平均不动点 ⟹ 窗口正则化必要性的代数证据**；与静默窗口机制同构）。 -/

/-- ★★ boost 共轭保持对称：T 对称 ⟹ B(φ)·T·B(φ)ᵀ 对称
    ——等变平均闭包的单步基础（与 groupAverage_preserves_symmetric 镜像：
    旋转侧与 boost 侧共轭作用都保持对称闭包）。 -/
theorem boost_adjoint_symmetric (T : Matrix (Fin 2) (Fin 2) ℝ)
    (h : Matrix.transpose T = T) (φ : ℝ) :
    Matrix.transpose (boost φ * T * Matrix.transpose (boost φ))
      = boost φ * T * Matrix.transpose (boost φ) := by
  simp [Matrix.transpose_mul, Matrix.transpose_transpose, h]
  rw [← Matrix.mul_assoc]

/-- ★★ boost 共轭的迹演化：tr(B·T·Bᵀ) = tr(boost(2φ)·T)
    ——迹（质量读数 λ=trace/2）在 boost 下按 rapidity 加倍谱流演化
    （循环迹 + boost 平方：BᵀB=boost(2φ)；非紧侧迹不保持，读数是变换量）。 -/
theorem boost_adjoint_trace_eq (T : Matrix (Fin 2) (Fin 2) ℝ) (φ : ℝ) :
    Matrix.trace (boost φ * T * Matrix.transpose (boost φ)) = Matrix.trace (boost (2 * φ) * T) := by
  have hsym : Matrix.transpose (boost φ) = boost φ := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [boost]
  have hbb : Matrix.transpose (boost φ) * boost φ = boost (2 * φ) := by
    rw [hsym]
    rw [show 2 * φ = φ + φ by ring]
    rw [boost_add]
  calc
    Matrix.trace (boost φ * T * Matrix.transpose (boost φ))
        = Matrix.trace (Matrix.transpose (boost φ) * (boost φ * T)) := by
            rw [Matrix.trace_mul_comm]
        _ = Matrix.trace (Matrix.transpose (boost φ) * boost φ * T) := by
            rw [Matrix.mul_assoc]
        _ = Matrix.trace (boost (2 * φ) * T) := by
            rw [hbb]

/-- ★★ 无迹对称张量的 boost 轨道显式形态：T=[[a,b],[b,−a]] 时
    B·T·Bᵀ = [[a+2b·sinhφ·coshφ, b(coshφ²+sinhφ²)],[b(coshφ²+sinhφ²), −a+2b·sinhφ·coshφ]]
    ——各向异性分量 b 与对角混合（b 贡献入对角、无迹偏置不闭合）；
    非紧群轨道无有限不动点 ⟹ 等变平均需窗口正则化（静默窗口机制）。 -/
theorem boost_adjoint_traceless_explicit (a b φ : ℝ) :
    boost φ * !![a, b; b, -a] * Matrix.transpose (boost φ)
      = !![a + 2 * b * Real.sinh φ * Real.cosh φ, b * (Real.cosh φ ^ 2 + Real.sinh φ ^ 2);
          b * (Real.cosh φ ^ 2 + Real.sinh φ ^ 2), -a + 2 * b * Real.sinh φ * Real.cosh φ] := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [boost, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf
    try rw [show Real.cosh φ ^ 2 = 1 + Real.sinh φ ^ 2 by
        nlinarith [Real.cosh_sq_sub_sinh_sq φ]]
    try ring_nf

/-! ## 窗口 boost 平均（#56，缺口②收口）

非紧群平均无有限 Haar 测度（#55 轨道形态显示无迹偏置不闭合），
等变平均只能在**有限窗口**发生：3 点对称窗口
Avg_φ(T)=(1/3)[B(−φ)·T·B(−φ)ᵀ + T + B(φ)·T·B(φ)ᵀ]。
窗口=静默层（有限采样窗口，与静默 k_max 机制同构）：
sinh 奇函数在对称窗口内精确消零（对角不动），cosh 正函数保号（非对角同号缩放、
缩放因子 ≥1 不消灭各向异性）——**与旋转平均（消灭各向异性⟹λI）互补**：
boost 侧平均保持结构形态而不消灭空间各向异性（空间各向同性由旋转层负责）。 -/

/-- 3 点对称窗口 boost 平均：Avg_φ(T)=(1/3)[B(−φ)·T·B(−φ)ᵀ + T + B(φ)·T·B(φ)ᵀ]。 -/
noncomputable def boostWindowAvg3 (φ : ℝ) (T : Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  (1 / 3 : ℝ) • (boost (-φ) * T * Matrix.transpose (boost (-φ))
    + T + boost φ * T * Matrix.transpose (boost φ))

/-- ★★ 窗口平均保持无迹对称形态：无迹对称 T=[[a,b],[b,−a]] ⟹
    Avg_φ(T)=[[a, b(1+2(coshφ²+sinhφ²))/3],[b(1+2(coshφ²+sinhφ²))/3, −a]]
    ——对角分量精确不动（sinh 奇函数消零）、非对角同号缩放（cosh 正性），
    无迹对称闭包在窗口平均下闭合。 -/
theorem boost_window3_avg_traceless_form (a b φ : ℝ) :
    boostWindowAvg3 φ !![a, b; b, -a]
      = !![a, b * (1 + 2 * (Real.cosh φ ^ 2 + Real.sinh φ ^ 2)) / 3;
          b * (1 + 2 * (Real.cosh φ ^ 2 + Real.sinh φ ^ 2)) / 3, -a] := by
  unfold boostWindowAvg3
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [boost, Matrix.mul_apply, Real.cosh_neg, Real.sinh_neg, Fin.sum_univ_succ,
          Matrix.vecMul, Matrix.vecHead, Matrix.vecTail]
    try ring_nf
    try rw [show Real.cosh φ ^ 2 = 1 + Real.sinh φ ^ 2 by
        nlinarith [Real.cosh_sq_sub_sinh_sq φ]]
    try ring_nf

/-- ★★ 窗口平均缩放因子 ≥ 1：(1+2·cosh(2φ))/3 ≥ 1
    ——非对角分量不被消灭（缩放≥1）：非紧侧窗口平均放大各向异性而非消除，
    与旋转平均（消灭各向异性⟹λI）互补——空间各向同性由旋转层负责。 -/
theorem boost_window3_avg_scale_factor_ge_one (φ : ℝ) :
    1 ≤ (1 + 2 * Real.cosh (2 * φ)) / 3 := by
  rw [one_le_div (by norm_num : (0 : ℝ) < 3)]
  have hc : 0 ≤ Real.cosh (2 * φ) := by positivity
  have hsq : (1 : ℝ) ^ 2 ≤ Real.cosh (2 * φ) ^ 2 := by
    nlinarith [Real.cosh_sq_sub_sinh_sq (2 * φ), sq_nonneg (Real.sinh (2 * φ))]
  have hcosh : 1 ≤ Real.cosh (2 * φ) := le_of_sq_le_sq hsq hc
  nlinarith [hcosh]

/-! ## 4×4 Dirac γ 矩阵层（#57，Cl(1,3) 标准表示）

Dirac 表示（ℂ 4×4）：γ⁰=diag(1,1,−1,−1)（时间生成元，平方 +1）、
γⁱ=[[0,σⁱ],[−σⁱ,0]]（空间生成元，平方 −1）。标准 Clifford 关系
γᵃγᵇ+γᵇγᵃ=2ηᵃᵇ（η=diag(1,−1,−1,−1)）——Cl(1,3) 的代数定义。
与 2×2 Cl(1,1) 层（#49 e_01/e_10 反对易）构成维度升级：狄拉克表示的标准形式。 -/

/-- 4×4 Dirac γ⁰（ℂ）：diag(1,1,−1,−1)，时间分量平方 +1。 -/
def gamma0 : Matrix (Fin 4) (Fin 4) ℂ :=
  !![1, 0, 0, 0;
     0, 1, 0, 0;
     0, 0, -1, 0;
     0, 0, 0, -1]

/-- 4×4 Dirac γ¹（ℂ）：[[0,σ¹],[−σ¹,0]]，空间分量平方 −1。 -/
def gamma1 : Matrix (Fin 4) (Fin 4) ℂ :=
  !![0, 0, 0, 1;
     0, 0, 1, 0;
     0, -1, 0, 0;
     -1, 0, 0, 0]

/-- 4×4 Dirac γ²（ℂ）：[[0,σ²],[−σ²,0]]。 -/
def gamma2 : Matrix (Fin 4) (Fin 4) ℂ :=
  !![0, 0, 0, -Complex.I;
     0, 0, Complex.I, 0;
     0, Complex.I, 0, 0;
     -Complex.I, 0, 0, 0]

/-- 4×4 Dirac γ³（ℂ）：[[0,σ³],[−σ³,0]]。 -/
def gamma3 : Matrix (Fin 4) (Fin 4) ℂ :=
  !![0, 0, 1, 0;
     0, 0, 0, -1;
     -1, 0, 0, 0;
     0, 1, 0, 0]

/-- Dirac γ 矩阵函数（Fin 4 → 4×4 ℂ）。 -/
noncomputable def gamma (a : Fin 4) : Matrix (Fin 4) (Fin 4) ℂ :=
  match a with
  | ⟨0, _⟩ => gamma0
  | ⟨1, _⟩ => gamma1
  | ⟨2, _⟩ => gamma2
  | _ => gamma3

/-- 闵氏度规指标函数：η(a,b)=1 if a=b=0，−1 if a=b≠0，0 otherwise。 -/
def gammaEta (a b : Fin 4) : ℂ :=
  if a = b then (if a = 0 then 1 else -1) else 0

/-- ★★ 时间生成元平方 +1：γ⁰² = 1（Cl(1,3) 时间分量标准关系）。 -/
theorem gamma0_sq : gamma0 * gamma0 = (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma0, Matrix.mul_apply, Fin.sum_univ_succ]

/-- ★★ 空间生成元平方 −1：γ¹² = −1（Cl(1,3) 空间分量标准关系）。 -/
theorem gamma1_sq : gamma1 * gamma1 = -(1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma1, Matrix.mul_apply, Fin.sum_univ_succ]

/-- 空间生成元平方 −1：γ²² = −1。 -/
theorem gamma2_sq : gamma2 * gamma2 = -(1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma2, Matrix.mul_apply, Fin.sum_univ_succ, Complex.I_mul_I]

/-- 空间生成元平方 −1：γ³² = −1。 -/
theorem gamma3_sq : gamma3 * gamma3 = -(1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma3, Matrix.mul_apply, Fin.sum_univ_succ]

/-- ★★ 时空反对易：γ⁰γ¹+γ¹γ⁰=0（Cl(1,3) 时空生成元反对易，
    与 #49 2×2 e_01/e_10 反对易的 4×4 标准表示版本）。 -/
theorem gamma0_gamma1_anticomm : gamma0 * gamma1 + gamma1 * gamma0 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]

/-- 时空反对易：γ⁰γ²+γ²γ⁰=0。 -/
theorem gamma0_gamma2_anticomm : gamma0 * gamma2 + gamma2 * gamma0 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma0, gamma2, Matrix.mul_apply, Fin.sum_univ_succ, Complex.I_mul_I]

/-- 时空反对易：γ⁰γ³+γ³γ⁰=0。 -/
theorem gamma0_gamma3_anticomm : gamma0 * gamma3 + gamma3 * gamma0 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma0, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]

/-- ★★ 空间间反对易：γ¹γ²+γ²γ¹=0（空间生成元两两反对易）。 -/
theorem gamma1_gamma2_anticomm : gamma1 * gamma2 + gamma2 * gamma1 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma1, gamma2, Matrix.mul_apply]

/-- 空间间反对易：γ¹γ³+γ³γ¹=0。 -/
theorem gamma1_gamma3_anticomm : gamma1 * gamma3 + gamma3 * gamma1 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma1, gamma3, Matrix.mul_apply]

/-- 空间间反对易：γ²γ³+γ³γ²=0。 -/
theorem gamma2_gamma3_anticomm : gamma2 * gamma3 + gamma3 * gamma2 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma2, gamma3, Matrix.mul_apply]

/-- ★★ 完整 Clifford 关系：γᵃγᵇ+γᵇγᵃ = 2ηᵃᵇ（∀ a b : Fin 4）
    ——Cl(1,3) 的代数定义（Dirac 表示机检）：时间平方 +1、空间平方 −1、
    生成元两两反对易——标准 Clifford 代数关系完整闭合。 -/
lemma gamma_ofFin0 : gamma (0 : Fin 4) = gamma0 := by rfl
lemma gamma_ofFin1 : gamma (1 : Fin 4) = gamma1 := by rfl
lemma gamma_ofFin2 : gamma (2 : Fin 4) = gamma2 := by rfl
lemma gamma_ofFin3 : gamma (3 : Fin 4) = gamma3 := by rfl

theorem gamma_clifford_relation (a b : Fin 4) :
    gamma a * gamma b + gamma b * gamma a
      = (2 * gammaEta a b) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  fin_cases a <;> fin_cases b
  all_goals
    simp [gamma_ofFin0, gamma_ofFin1, gamma_ofFin2, gamma_ofFin3, gammaEta,
          gamma0_sq, gamma1_sq, gamma2_sq, gamma3_sq,
          gamma0_gamma1_anticomm, gamma0_gamma2_anticomm, gamma0_gamma3_anticomm,
          gamma1_gamma2_anticomm, gamma1_gamma3_anticomm, gamma2_gamma3_anticomm]
  all_goals
    try
      ext i j
      fin_cases i <;> fin_cases j
      simp [Matrix.mul_apply, Matrix.one_apply, Pi.add_apply, Pi.one_apply,
            Pi.zero_apply, Pi.smul_apply, Fin.sum_univ_succ, gamma0, gamma1,
            gamma2, gamma3]
  all_goals
    try norm_num
  all_goals
    try norm_num [Matrix.mul_apply, gamma0, gamma1, gamma2, gamma3, Fin.sum_univ_succ]
  all_goals
    try native_decide
  all_goals
    try rfl

/-- ★★ 质量壳代数（谱流参数化，ℝ）：(m·coshφ)² − (m·sinhφ)² = m²
    ——cosh²−sinh²=1 的质量加权形态（#42 质量壳的谱流参数化）。 -/
theorem mass_shell (m φ : ℝ) : (m * Real.cosh φ) ^ 2 - (m * Real.sinh φ) ^ 2 = m ^ 2 := by
  calc
    (m * Real.cosh φ) ^ 2 - (m * Real.sinh φ) ^ 2 = m ^ 2 * (Real.cosh φ ^ 2 - Real.sinh φ ^ 2) := by ring
    _ = m ^ 2 * 1 := by rw [Real.cosh_sq_sub_sinh_sq φ]
    _ = m ^ 2 := by ring

/-- ★★ 质量壳代数（ℂ 提升）：((m:ℂ)·cosh(φ:ℂ))² − ((m:ℂ)·sinh(φ:ℂ))² = (m:ℂ)²。 -/
theorem mass_shell_complex (m φ : ℝ) :
    ((m : ℂ) * Complex.cosh (φ : ℂ)) ^ 2 - ((m : ℂ) * Complex.sinh (φ : ℂ)) ^ 2 = (m : ℂ) ^ 2 := by
  calc
    ((m : ℂ) * Complex.cosh (φ : ℂ)) ^ 2 - ((m : ℂ) * Complex.sinh (φ : ℂ)) ^ 2
        = (m : ℂ) ^ 2 * (Complex.cosh (φ : ℂ) ^ 2 - Complex.sinh (φ : ℂ) ^ 2) := by ring
    _ = (m : ℂ) ^ 2 * 1 := by rw [Complex.cosh_sq_sub_sinh_sq]
    _ = (m : ℂ) ^ 2 := by ring

/-! ## 4×4 Dirac 质量方程代数层（#58，Cl(1,3) 完整签名）

D₄ = E·γ⁰ − p·γ¹（γ 矩阵为 #57 Dirac 表示，ℂ 4×4）。
Cl(1,3) 完整签名下：γ⁰²=+1、γ¹²=−1、反对易项消零 ⟹ D₄²=(E²−p²)·1；
壳上 E²−p²=m² ⟹ D₄²=m²·1——**质量 = Dirac 算符平方本征值**（#49 2×2
clifford_dirac_mass_shell 的 4×4 标准表示升级）；壳上零因子
(D₄+m·1)(m·1−D₄)=0——**质量 = Dirac 核 ±m**，Π± 两正交投影对的
Cl(1,3) 完整签名版前身（#50/#51 投影结构在 4 维表示的落地）。 -/

/-- 4×4 Dirac 算符（Cl(1,3) 1+1 简化）：D₄ = E·γ⁰ − p·γ¹。 -/
noncomputable def DiracOp4 (E p : ℝ) : Matrix (Fin 4) (Fin 4) ℂ :=
  (E : ℂ) • gamma0 - (p : ℂ) • gamma1

/-- ★★ Cl(1,3) 签名 Dirac 平方：D₄² = (E²−p²)·1
    ——γ⁰²=+1（时间）、γ¹²=−1（空间）、反对易项 −Ep(γ⁰γ¹+γ¹γ⁰)=0：
    平方只剩时空间隔标量，Dirac 质量方程的代数核心（4×4 版
    clifford_dirac_square，#49 维度升级）。 -/
theorem diracOp4_sq (E p : ℝ) :
    DiracOp4 E p * DiracOp4 E p = ((E ^ 2 - p ^ 2 : ℝ) : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4, gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf

/-- ★★ 4×4 质量=Dirac 平方本征值：E=m·coshφ、p=m·sinhφ ⟹ D₄²=m²·1
    ——质量壳 E²−p²=m² 的 Cl(1,3) 完整签名表述（4×4 版
    clifford_dirac_mass_shell）。 -/
theorem diracOp4_mass_shell (m φ : ℝ) :
    DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ)
        * DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ)
      = ((m ^ 2 : ℝ) : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  rw [diracOp4_sq]
  norm_num [mass_shell_complex m φ]

/-- ★★ 壳上零因子分解（4×4）：(D₄+m·1)(m·1−D₄)=0
    ——D₄ 分解为 ±m 两个核（D₄²=m²·1 ⟹ (D₄−m·1)(D₄+m·1)=0），
    质量=Dirac 核 ±m 的 Cl(1,3) 完整签名版；Π± 两正交投影对的 4 维前身
    （#51 投影结构的完整签名落地）。 -/
theorem diracOp4_mass_factorization (m φ : ℝ) :
    (DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ) + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      * ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ)) = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4, gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf
    try norm_num [mass_shell_complex m φ]
  all_goals
    try
      rw [show Complex.cosh (φ : ℂ) ^ 2 = 1 + Complex.sinh (φ : ℂ) ^ 2 by
        rw [← Complex.cosh_sq_sub_sinh_sq (φ : ℂ)]
        ring]
      ring
  all_goals
    try simp [Matrix.one_apply, Pi.one_apply]
  all_goals
    try ring

/-! ## 4×4 质量投影对幂等化（#59，Π± 完整签名版）

壳上 D₄²=m²·1 ⟹ (D₄+m·1)²=D₄²+2mD₄+m²·1=m²·1+2mD₄+m²·1=2m(D₄+m·1)——
**Π₊²=Π₊**（Π₊=(D₄+m·1)/(2m) 分子版）；(m·1−D₄)²=2m(m·1−D₄)——**Π₋²=Π₋**；
(D₄+m·1)(m·1−D₄)=0——**Π₊·Π₋=0 正交**（#58 零因子）；
(D₄+m·1)+(m·1−D₄)=2m·1——**Π₊+Π₋=1 互补**（恒等，无需壳）。
"态射/右伴随两正交投影"直觉在 Cl(1,3) 完整签名的最终落地（#51 的 4×4 升级）。 -/

/-- ★★ Π₊²=Π₊（分子版）：壳上 (D₄+m·1)² = 2m·(D₄+m·1)。 -/
theorem diracOp4_mass_projector_idem_plus (m φ : ℝ) :
    (DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ) + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      * (DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ) + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      = (2 * m : ℝ) • (DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ)
          + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ)) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4, gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf
    try norm_num [mass_shell_complex m φ]
  all_goals
    try
      rw [show Complex.cosh (φ : ℂ) ^ 2 = 1 + Complex.sinh (φ : ℂ) ^ 2 by
        rw [← Complex.cosh_sq_sub_sinh_sq (φ : ℂ)]
        ring]
      ring
  all_goals
    try simp [Matrix.one_apply, Pi.one_apply]
  all_goals
    try ring

/-- ★★ Π₋²=Π₋（分子版）：壳上 (m·1−D₄)² = 2m·(m·1−D₄)。 -/
theorem diracOp4_mass_projector_idem_minus (m φ : ℝ) :
    ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ))
      * ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ))
      = (2 * m : ℝ) • ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ)
          - DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ)) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4, gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf
    try norm_num [mass_shell_complex m φ]
  all_goals
    try
      rw [show Complex.cosh (φ : ℂ) ^ 2 = 1 + Complex.sinh (φ : ℂ) ^ 2 by
        rw [← Complex.cosh_sq_sub_sinh_sq (φ : ℂ)]
        ring]
      ring
  all_goals
    try simp [Matrix.one_apply, Pi.one_apply]
  all_goals
    try ring

/-- ★★ Π₊·Π₋=0（正交）：壳上 (D₄+m·1)(m·1−D₄)=0（#58 零因子分解）。 -/
theorem diracOp4_mass_projectors_annihilate (m φ : ℝ) :
    (DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ) + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      * ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4 (m * Real.cosh φ) (m * Real.sinh φ)) = 0 :=
  diracOp4_mass_factorization m φ

/-- ★★ Π₊+Π₋=1（互补）：(D₄+m·1)+(m·1−D₄)=2m·1——恒等，无需壳条件。 -/
theorem diracOp4_mass_projectors_complement (E p m : ℝ) :
    (DiracOp4 E p + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      + ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4 E p)
      = (2 * m : ℝ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4]
    try ring_nf

/-! ## 双向量平方的时空投影结构（#60，Cl(1,3)）

4×4 表示中生成元平方不是标量，而是**时空投影**：
空间双向量 J_z² = diag(0,−1,−1,0) = −P_spatial（**时间分量精确为 0**——
空间旋转不触及时间坐标，"静默=时间分量不参与"的代数对应，SO(1,3) 与 so(3)
的本质区别）；时空双向量 K_x² = diag(1,1,0,0) = P_{t,x}（**平方 +1 在 (t,x)
平面**——boost 生成元的双曲结构）。 -/

/-- ★★ 空间双向量平方 = −空间投影：J_z² = diag(0,−1,−1,0)
    ——时间分量精确 0（静默=时间分量不参与旋转，SO(1,3) 与 so(3) 本质区别）。 -/
theorem Jz_sq_spatial_projection :
    J_z * J_z = !![0, 0, 0, 0;
                  0, -1, 0, 0;
                  0, 0, -1, 0;
                  0, 0, 0, 0] := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [J_z, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf

/-- ★★ 时空双向量平方 = 时空投影：K_x² = diag(1,1,0,0)
    ——平方 +1 在 (t,x) 平面（boost 生成元的双曲结构）。 -/
theorem Kx_sq_temporal_projection :
    K_x * K_x = !![1, 0, 0, 0;
                  0, 1, 0, 0;
                  0, 0, 0, 0;
                  0, 0, 0, 0] := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [K_x, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf

/-! ## 4×4 Dirac 完整动量版本（#61，Cl(1,3) 全动量）

D₄_full = γ⁰E − γ¹p₁ − γ²p₂ − γ³p₃。完整 Clifford 关系（#57）下：
γ⁰²=+1、γⁱ²=−1、全交叉反对易消零 ⟹ D_full²=(E²−p₁²−p₂²−p₃²)·1；
壳上 E²−p₁²−p₂²−p₃²=m² ⟹ D_full²=m²·1——**相对论色散关系 E²=p²+m² 的
Dirac 算符表述：质量壳 = Dirac 算符零空间**（#58 1+1 简化的完整 3+1 升级）。 -/

/-- 4×4 Dirac 算符（Cl(1,3) 完整动量）：D₄ = γ⁰E − γ¹p₁ − γ²p₂ − γ³p₃。 -/
noncomputable def DiracOp4Full (E p₁ p₂ p₃ : ℝ) : Matrix (Fin 4) (Fin 4) ℂ :=
  (E : ℂ) • gamma0 - (p₁ : ℂ) • gamma1 - (p₂ : ℂ) • gamma2 - (p₃ : ℂ) • gamma3

/-- ★★ 全动量 Dirac 平方：D_full² = (E²−p₁²−p₂²−p₃²)·1
    ——完整 Clifford 关系下平方只剩时空间隔标量（γ⁰²=+1、γⁱ²=−1、
    全部交叉反对易消零），Dirac 质量方程的标准相对论形式。 -/
theorem diracOp4full_sq (E p₁ p₂ p₃ : ℝ) :
    DiracOp4Full E p₁ p₂ p₃ * DiracOp4Full E p₁ p₂ p₃
      = ((E ^ 2 - p₁ ^ 2 - p₂ ^ 2 - p₃ ^ 2 : ℝ) : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]
  all_goals
    try ring_nf
  all_goals
    try simp [sq, Complex.I_mul_I]
  all_goals
    try ring

/-- ★★ 相对论色散 E²=p²+m² 的 Dirac 表述：E²−p₁²−p₂²−p₃²=m² ⟹ D_full²=m²·1
    ——**质量壳 = Dirac 算符零空间**（全动量版 mass_shell）。 -/
theorem diracOp4full_mass_shell (E p₁ p₂ p₃ m : ℝ) (h : E ^ 2 - p₁ ^ 2 - p₂ ^ 2 - p₃ ^ 2 = m ^ 2) :
    DiracOp4Full E p₁ p₂ p₃ * DiracOp4Full E p₁ p₂ p₃
      = ((m ^ 2 : ℝ) : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  rw [diracOp4full_sq, h]

/-- ★★ 壳上零因子分解（全动量版）：E²−p₁²−p₂²−p₃²=m² ⟹
    (D_full+m·1)(m·1−D_full)=0——质量=Dirac 核 ±m，Π± 投影对的完整动量前身。 -/
theorem diracOp4full_mass_factorization (E p₁ p₂ p₃ m : ℝ)
    (h : E ^ 2 - p₁ ^ 2 - p₂ ^ 2 - p₃ ^ 2 = m ^ 2) :
    (DiracOp4Full E p₁ p₂ p₃ + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      * ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4Full E p₁ p₂ p₃) = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ,
          Matrix.one_apply, Pi.one_apply]
  all_goals
    try ring_nf
  all_goals
    try simp [sq, Complex.I_mul_I]
  all_goals
    try ring
  all_goals
    try
      have h' : (E : ℂ) ^ 2 - (p₁ : ℂ) ^ 2 - (p₂ : ℂ) ^ 2 - (p₃ : ℂ) ^ 2 = (m : ℂ) ^ 2 := by
        exact_mod_cast h
      rw [← h']
      ring

/-! ## 全动量版质量投影对幂等化（#62，Π± 完整动量）

壳上 D_full²=m²·1（#61）⟹ 与 #59 同构的投影结构在完整 3+1 动量下闭合：
(D_full+m·1)²=2m(D_full+m·1)——Π₊²=Π₊；(m·1−D_full)²=2m(m·1−D_full)——Π₋²=Π₋；
(D_full+m·1)(m·1−D_full)=0——Π₊·Π₋=0；（相加）=2m·1——Π₊+Π₋=1。
"态射/右伴随两正交投影"直觉在**标准相对论 Dirac 结构**（γᵃpᵃ 全动量）的最终落地：
质量壳投影对的完整 Cl(1,3) 表述。 -/

/-- ★★ Π₊²=Π₊（全动量）：壳上 (D_full+m·1)² = 2m·(D_full+m·1)。 -/
theorem diracOp4full_mass_projector_idem_plus (E p₁ p₂ p₃ m : ℝ)
    (h : E ^ 2 - p₁ ^ 2 - p₂ ^ 2 - p₃ ^ 2 = m ^ 2) :
    (DiracOp4Full E p₁ p₂ p₃ + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      * (DiracOp4Full E p₁ p₂ p₃ + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      = (2 * m : ℝ) • (DiracOp4Full E p₁ p₂ p₃ + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ)) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ,
          Matrix.one_apply, Pi.one_apply]
  all_goals
    try ring_nf
  all_goals
    try simp [sq, Complex.I_mul_I]
  all_goals
    try ring
  all_goals
    try
      have h' : (E : ℂ) ^ 2 - (p₁ : ℂ) ^ 2 - (p₂ : ℂ) ^ 2 - (p₃ : ℂ) ^ 2 = (m : ℂ) ^ 2 := by
        exact_mod_cast h
      rw [← h']
      ring

/-- ★★ Π₋²=Π₋（全动量）：壳上 (m·1−D_full)² = 2m·(m·1−D_full)。 -/
theorem diracOp4full_mass_projector_idem_minus (E p₁ p₂ p₃ m : ℝ)
    (h : E ^ 2 - p₁ ^ 2 - p₂ ^ 2 - p₃ ^ 2 = m ^ 2) :
    ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4Full E p₁ p₂ p₃)
      * ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4Full E p₁ p₂ p₃)
      = (2 * m : ℝ) • ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4Full E p₁ p₂ p₃) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ,
          Matrix.one_apply, Pi.one_apply]
  all_goals
    try ring_nf
  all_goals
    try simp [sq, Complex.I_mul_I]
  all_goals
    try ring
  all_goals
    try
      have h' : (E : ℂ) ^ 2 - (p₁ : ℂ) ^ 2 - (p₂ : ℂ) ^ 2 - (p₃ : ℂ) ^ 2 = (m : ℂ) ^ 2 := by
        exact_mod_cast h
      rw [← h']
      ring

/-- ★★ Π₊·Π₋=0（全动量正交）：壳上 (D_full+m·1)(m·1−D_full)=0（#61 零因子）。 -/
theorem diracOp4full_mass_projectors_annihilate (E p₁ p₂ p₃ m : ℝ)
    (h : E ^ 2 - p₁ ^ 2 - p₂ ^ 2 - p₃ ^ 2 = m ^ 2) :
    (DiracOp4Full E p₁ p₂ p₃ + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      * ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4Full E p₁ p₂ p₃) = 0 :=
  diracOp4full_mass_factorization E p₁ p₂ p₃ m h

/-- ★★ Π₊+Π₋=1（全动量互补）：(D_full+m·1)+(m·1−D_full)=2m·1——恒等，无需壳。 -/
theorem diracOp4full_mass_projectors_complement (E p₁ p₂ p₃ m : ℝ) :
    (DiracOp4Full E p₁ p₂ p₃ + (m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ))
      + ((m : ℂ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) - DiracOp4Full E p₁ p₂ p₃)
      = (2 * m : ℝ) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp4Full]
    try ring_nf

/-! ## Cl(1,3) 双向量乘积的对称部分（#63，乘法表收口）

so(1,3) 4×4 表示下，生成元乘积 = **半交换子 + 半对称尾巴**：
J_x·J_y = (J_z + Sym)/2（交换子 [J_x,J_y]=J_z 已机检 #54，对称尾巴 Sym 非零）。
J 族与 K 族的对称尾巴**同形**（同为空间 i-j 块对称矩阵）——
这是李代数表示乘积**落出 6 维生成元空间**的冗余量（区别于 Clifford 双向量
恒等式：Dirac 旋转矩阵表示下对称尾巴非零，被精确刻画）。 -/

/-- ★★ 旋转生成元乘积的对称尾巴：J_x·J_y+J_y·J_x = 空间 (1,2) 块对称矩阵
    ——so(1,3) 表示下乘积的冗余（非零对称部分，非纯 so(3) 封闭）。 -/
theorem Jx_Jy_sym_form :
    J_x * J_y + J_y * J_x = !![0, 0, 0, 0;
                              0, 0, 1, 0;
                              0, 1, 0, 0;
                              0, 0, 0, 0] := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [J_x, J_y, Matrix.mul_apply]
    try ring_nf

/-- ★★ boost 生成元乘积的对称尾巴：K_x·K_y+K_y·K_x = 与 J 族**同形**
    ——时空双向量乘积的冗余与空间双向量同构。 -/
theorem Kx_Ky_sym_form :
    K_x * K_y + K_y * K_x = !![0, 0, 0, 0;
                              0, 0, 1, 0;
                              0, 1, 0, 0;
                              0, 0, 0, 0] := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [K_x, K_y, Matrix.mul_apply]
    try ring_nf

/-- ★★ 乘积分解：J_x·J_y = (J_z + Sym)/2——**半交换子（李括号）+半对称尾巴（冗余）**，
    J_x·J_y = !![0,0,0,0; 0,0,0,0; 0,1,0,0; 0,0,0,0]（只有 (2,1)=1 项）。 -/
theorem Jx_mul_Jy_decomp :
    J_x * J_y = !![0, 0, 0, 0;
                  0, 0, 0, 0;
                  0, 1, 0, 0;
                  0, 0, 0, 0] := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [J_x, J_y, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf

/-! ## Cl(1,3) 字积字典：2⁴=16 态、15 非标量层（#65，Δφ 内生链钉死）

Δφ=ln2 内生链（#64 判据收敛后）：**2（每维 2 态）→ 4（Cl(1,3) 时空维数）
→ 16=2⁴（Cl(1,3) 字积字典/全代数维数）→ 15=16−1（非标量层）**。
Clifford 字积由指数 b : Fin 4 → Fin 2 编码（γ^b=γ⁰^{b₀}γ¹^{b₁}γ²^{b₂}γ³^{b₃}，
bᵢ∈{0,1}）——**字积字典与 (Fin 4 → Fin 2) 同构**：4 个时空维各 2 态 ⟹ 2⁴ 个字积。
本批把"4 步翻倍覆盖 Cl(1,3) 全代数、15=16−1 非标量静默层"从计数结构钉死：
4 步的 4 = 时空维数（MinkowskiEta4 已机检）、每步 ×2 = 每维 2 态（双值生成元）、
16 = 字积字典基数、15 = 除标量 1 外全部字积——零自由参数。 -/

/-- ★★ Cl(1,3) 字积字典基数：Fintype.card (Fin 4 → Fin 2) = 16 = 2⁴
    ——4 个时空维（1+3）各 2 态（双值生成元）⟹ 2⁴=16 个字积
    （Clifford 代数标准事实 dim Cℓ(p,q)=2^{p+q} 的计数层：p+q=4）。 -/
theorem cl13_algebra_dim_sixteen : Fintype.card (Fin 4 → Fin 2) = 16 := by
  simp [Fintype.card_fun]

/-- ★★ 非标量字积计数：除标量 1（全零指数 b=0）外全部字积 = 15
    ——**15 = 16−1**（唯一标量除外），与 orbitCount=15 解集定理、
    v2 主身份（15=2⁴−1）、用户直觉（Cl(1,3) 16 态并存、确定 1 态余 15 态）
    在计数层精确咬合。 -/
theorem cl13_non_scalar_word_count :
    Fintype.card {b : Fin 4 → Fin 2 // ∃ i : Fin 4, b i = 1} = 15 := by
  native_decide

/-- ★★ Cl(1,3) 字积分次分解：Σ_{k=0..4} C(4,k) = 16（1+4+6+4+1）
    ——标量 1、向量 4、双向量 6、三向量 4、伪标量 1 的分次字典
    （Cℓ 分次维数 = 二项式系数，Clifford 标准结构）。 -/
theorem cl13_graded_word_count :
    ∑ k ∈ Finset.range 5, Nat.choose 4 k = 16 := by
  native_decide

/-- ★★ 非标量分次计数：15 = Σ_{k=0..4} C(4,k) − 1（全代数 16 减唯一标量）
    ——非标量层 = 向量+双向量+三向量+伪标量（4+6+4+1=15），
    "静默窗口/全锁定"在分次层的计数对应。 -/
theorem cl13_non_scalar_graded_count :
    ∑ k ∈ Finset.range 5, Nat.choose 4 k - 1 = 15 := by
  native_decide

/-- ★★ 4 步翻倍算术锚：2⁴ = 16 且 16−1 = 15
    ——每步 ×2（每维 2 态）⟹ 4 步（4 时空维）⟹ 2⁴=16 态 ⟹ 非标量 15。 -/
theorem doubling_four_steps_cl13 : 2 ^ 4 = 16 ∧ 16 - 1 = 15 := by
  constructor <;> norm_num

/-! ## 每步翻倍勾股族（#66，Δφ=ln2 的整数勾股族）

Δφ=ln2 采纳后（2026-10-25 用户确认），三层时间分层桥数值锁死：
θ_n = arcsin(tanh(n·ln2))。**每步翻倍勾股族**（g=2^n ⟹ tanh(ln g)=(g²−1)/(g²+1)）：
n=1 ⟹ 3-4-5（v=3/5，#64）、n=2 ⟹ 8-15-17（v=15/17）、
n=3 ⟹ 63-16-65、n=4 ⟹ 255-32-257（16 态窗口，v=255/257）。
一般定理：tanh(n·ln2) = (2^{2n}−1)/(2^{2n}+1)——全为精确有理勾股。
Cl(1,3) 字积字典与 M₄(ℂ) 同基数 16：矩阵级正交性（张满）为后续候选。 -/

/-- ★★ 翻倍勾股族一般定理：tanh(n·ln2) = (2^{2n}−1)/(2^{2n}+1)（n 步翻倍的速度恒为有理勾股）。 -/
theorem tanh_log_pow_two (n : ℕ) :
    Real.tanh ((n : ℝ) * Real.log 2) = (2 ^ (2 * n) - 1) / (2 ^ (2 * n) + 1) := by
  have hlog : Real.log ((2 : ℝ) ^ n) = (n : ℝ) * Real.log 2 := by
    rw [Real.log_pow]
    try norm_num
  have hpos : 0 < (2 : ℝ) ^ n := by positivity
  calc
    Real.tanh ((n : ℝ) * Real.log 2)
        = Real.tanh (Real.log ((2 : ℝ) ^ n)) := by rw [← hlog]
    _ = (((2 : ℝ) ^ n) ^ 2 - 1) / (((2 : ℝ) ^ n) ^ 2 + 1) := by
      rw [Real.tanh_eq_sinh_div_cosh, Real.sinh_log hpos, Real.cosh_log hpos]
      field_simp
    _ = (2 ^ (2 * n) - 1) / (2 ^ (2 * n) + 1) := by
      rw [← pow_mul, mul_comm]

/-- ★★ 两步翻倍：tanh(2·ln2) = 15/17——θ₂ 的 8-15-17 勾股（v=15/17）。 -/
theorem tanh_two_log_two : Real.tanh (2 * Real.log 2) = 15 / 17 := by
  have h := tanh_log_pow_two 2
  norm_num at h ⊢
  exact h

/-- ★★ 四步翻倍：tanh(4·ln2) = 255/257——θ₄ 的 255-32-257 勾股（16 态窗口速度）。 -/
theorem tanh_four_log_two : Real.tanh (4 * Real.log 2) = 255 / 257 := by
  have h := tanh_log_pow_two 4
  norm_num at h ⊢
  exact h

-- ------------------------------------------------------------
-- S103：K_max 层谱流对数 = 框架计数（G2 桥闭合候选——2026-10-27）
--   rapidity_eight_layers_log：8·ln2 = ln(2^8) = ln 256
--   ——8 层递归（K_max）后谱流 rapidity = ln(框架计数)——256 三重身份
--   （2^8 = 16² = Σchoose(8,k)——见 ExpTruncation.frame_count_256）
--   ——"谱流位置的对数 = 组合计数结构"——与 S101 锚（Σchoose = 256——
--   卷积系数恒等的计数来源）连接——G2 桥（t = k·Δφ——Δφ = ln2——
--   8 层 = 8·ln2 = ln256）显式化
-- ------------------------------------------------------------
theorem rapidity_eight_layers_log :
    8 * Real.log 2 = Real.log 256 := by
  have hlog : Real.log ((2 : ℝ) ^ 8) = 8 * Real.log 2 := by
    rw [Real.log_pow]
    norm_num
  calc
    8 * Real.log 2 = Real.log ((2 : ℝ) ^ 8) := by rw [← hlog]
    _ = Real.log 256 := by norm_num

-- ------------------------------------------------------------
-- S104：静默窗口级联（2026-10-27）
--   15 = 16−1、255 = 256−1、65535 = 65536−1——"静默闭合 = 窗口计数减
--   标量 1——跨尺度保持（16 → 256 = 16² → 65536 = 16⁴）"——标量层永不
--   闭合——与 S19（orbitCount = 15 = 16−1 非标量层）、#65（Cl(1,3) 字积
--   字典 16 态除标量 1 外 15 非标量）一致
--   勾股族连接（已机检）：tanh(2·ln2) = 15/17——"2 层递归后速度 =
--   orbitCount（静默窗口 15）/窗口加一（17）"；tanh(4·ln2) = 255/257——
--   "4 层 = 框架计数窗口 256 的静默/开放比"——"速度 = 静默窗口比"
-- ------------------------------------------------------------
theorem silence_window_cascade :
    16 - 1 = 15 ∧ (2 : ℕ) ^ 8 - 1 = 255 ∧ (2 : ℕ) ^ 16 - 1 = 65535 := by
  constructor
  · norm_num
  · constructor <;> norm_num

-- ------------------------------------------------------------
-- S105：静默窗口勾股族（2026-10-27）
--   silence_pythag_general：(M−1)² + (2√M)² = (M+1)²——任意 M = a²
--   （偶平方）的静默窗口勾股恒等式——勾股三元组 (M−1, 2a, M+1)
--   ——"静默窗口（M−1）、中间边（2√M）、开放窗口（M+1）"
--   silence_pythag_two_pow：a = 2^n 代入——(2^{2n}−1, 2^{n+1}, 2^{2n}+1)
--   ——n=2: 8-15-17、n=3: 63-16-65（中间边 16 = 全态！）、n=4: 255-32-257
--   pythag_eight_fifteen_seventeen：8² + 15² = 17²——"2 层翻倍的静默
--   窗口勾股 = K_max² + orbitCount² = (窗口+1)²"——8 = K_max（框架
--   常数）、15 = orbitCount（静默闭合——S19）、17 = 16+1（窗口加一）
--   ——"K_max 与 orbitCount 的勾股关系——窗口加一闭合"
--   谱流连接（已机检）：sinh(2·ln2) = 15/8 = orbitCount/K_max、
--   cosh(2·ln2) = 17/8 = (窗口+1)/K_max、tanh(2·ln2) = 15/17 =
--   orbitCount/窗口加一——"双曲函数三元组 = 静默窗口勾股三元组的
--   谱流实现"
-- ------------------------------------------------------------
theorem silence_pythag_general (a : ℝ) :
    (a ^ 2 - 1) ^ 2 + (2 * a) ^ 2 = (a ^ 2 + 1) ^ 2 := by
  ring

theorem silence_pythag_two_pow (n : ℕ) :
    ((2 : ℝ) ^ (2 * n) - 1) ^ 2 + ((2 : ℝ) ^ (n + 1)) ^ 2 =
      ((2 : ℝ) ^ (2 * n) + 1) ^ 2 := by
  have h := silence_pythag_general ((2 : ℝ) ^ n)
  -- (2^n)² = 2^{n·2} = 2^{2n}（pow_mul + mul_comm）——2·2^n = 2^n·2 = 2^{n+1}（pow_succ）
  simpa [pow_mul, pow_succ, mul_comm, mul_assoc, mul_left_comm] using h

theorem pythag_eight_fifteen_seventeen :
    (8 : ℝ) ^ 2 + 15 ^ 2 = 17 ^ 2 := by
  norm_num

-- ------------------------------------------------------------
-- S106：质量锚定链链内端点（2026-10-27）
--   planck_modflow_lt_one：普朗克质量链内 = 1（自然单位制——用户核心
--   目标）⟹ ln Δ_mod = −2π·M_Pl = −2π（模 Hamilton = 质量——文献
--   ——S97 已对照——ln Δ_mod = −2πM）⟹ Δ_mod（链内普朗克）= e^{−2π}
--   ——模算子 < 1（定性界——模流收缩）——e 从 EGF 导出（S98——eTrunc
--   锚）、2π 从 e^{iz} 周期性（S96/S97——TwoPiPeriodicity）
--   数值（s106 脚本）：e^{−2π} = 0.00186744——与框架有理量无意外连接
--   （e^{2π} = 535.49 非整——连分数 [0,535,2,29,2,5,1,2] 无结构）——
--   超越独立性——"链内普朗克模算子是超越数——由内生 e 与 2π 构成"——
--   系统外 kg 测量锚定（用户"系统外测量质量锚定质量"）
-- ------------------------------------------------------------
theorem planck_modflow_lt_one :
    Real.exp (-2 * Real.pi) < 1 := by
  have hneg : (-2 : ℝ) * Real.pi = -(2 * Real.pi) := by ring
  rw [hneg, Real.exp_neg]
  have h2p : 0 < 2 * Real.pi := Real.two_pi_pos
  have he : 1 < Real.exp (2 * Real.pi) := by
    rw [← Real.exp_zero]
    exact Real.exp_strictMono h2p
  exact inv_lt_one_of_one_lt₀ he

-- ------------------------------------------------------------
-- S107：质量谱模流对数（2026-10-27）
--   M_Pl 链内 = 1（S106——用户核心目标——自然单位制）⟹ 质量谱的
--   模流对数 E_i = −ln(m_i/M_Pl)——m_τ 绝对链（M_Pl·e^{−E_τ} =
--   1776.63 vs 1776.86——1.9σ_score——#74 判别）——数值扫描证伪
--   （E_i 不化简为 2π 整倍/简单框架量——E_τ vs 7·2π 差 1.4%——
--   质量谱非平凡——E_i 独立框架导出）
--   planck_mass_log_origin：E_Pl = −ln 1 = 0——普朗克质量是谱原点
--   mass_E_order_reverse：质量递增 ⟹ E 递减（谱反序——log_lt_log）
--   ——"质量谱以普朗克质量为原点——E ≥ 0——谱序 = 质量反序"——
--   "质量 = e^{−E}——模流对数谱 = 质量谱的对数实现"
-- ------------------------------------------------------------
theorem planck_mass_log_origin :
    -Real.log (1 : ℝ) = 0 := by
  rw [Real.log_one]
  norm_num

theorem mass_E_order_reverse {m1 m2 : ℝ} (h1 : 0 < m1) (h2 : m1 < m2) :
    -Real.log m1 > -Real.log m2 := by
  have hl : Real.log m1 < Real.log m2 := Real.log_lt_log h1 h2
  linarith

/-- ★★ 两步偏转纯整数签名：sinθ₂ = tanh(2·ln2) = 15/17（8-15-17 勾股）。 -/
theorem step2_sine_fifteen_seventeen (θ : ℝ) (h : Real.sin θ = Real.tanh (2 * Real.log 2)) :
    Real.sin θ = 15 / 17 := by
  rw [h, tanh_two_log_two]

/-- ★★ Cl(1,3) 字积字典与 M₄(ℂ) 同基数：card (Fin 4 → Fin 2) = card (Fin 4 × Fin 4) = 16
    ——字积字典（2⁴ 个）恰与 4×4 复矩阵空间同基数（矩阵级正交性=张满为后续候选）。 -/
theorem cl13_word_dict_eq_matrix_space :
    Fintype.card (Fin 4 → Fin 2) = Fintype.card (Fin 4 × Fin 4) := by
  norm_num [Fintype.card_fun, Fintype.card_prod]

/-! ## 字积字典矩阵级正交性（#67，Cl(1,3)=M₄(ℂ) 忠实性的实证起点）

Dirac 4×4 表示中 γ 矩阵无迹（忠实表示的标志）、γ 两两正交（Tr(γᵃγᵇ)=0，a≠b）、
对角范数 ±4（γ⁰²=1、γⁱ²=−1 ⟹ Tr=±4）、伪标量字积 γ⁰γ¹γ²γ³ 无迹。
完整 16×16 正交矩阵（256 对内积）为大规模候选（注明未做）；
本批机检代表结构：无迹 + 正交 + 范数 + 伪标量。 -/

/-- ★★ γ⁰ 无迹：Tr γ⁰ = 0（Dirac 表示忠实性的标志——对跖矩阵块消零）。 -/
theorem gamma0_trace_zero : Matrix.trace gamma0 = 0 := by
  simp [Matrix.trace, gamma0, Fin.sum_univ_four]

/-- ★★ γ¹ 无迹：Tr γ¹ = 0。 -/
theorem gamma1_trace_zero : Matrix.trace gamma1 = 0 := by
  simp [Matrix.trace, gamma1, Fin.sum_univ_four]

/-- ★★ γ² 无迹：Tr γ² = 0。 -/
theorem gamma2_trace_zero : Matrix.trace gamma2 = 0 := by
  simp [Matrix.trace, gamma2, Fin.sum_univ_four]

/-- ★★ γ³ 无迹：Tr γ³ = 0。 -/
theorem gamma3_trace_zero : Matrix.trace gamma3 = 0 := by
  simp [Matrix.trace, gamma3, Fin.sum_univ_four]

/-- ★★ γ⁰ 与 γ¹ 正交：Tr(γ⁰·γ¹) = 0（Frobenius 内积 ⟨γ⁰,γ¹⟩=0，γ⁰†=γ⁰）。 -/
theorem gamma0_ortho_gamma1 : Matrix.trace (gamma0 * gamma1) = 0 := by
  simp [Matrix.trace, gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_four]

/-- ★★ γ¹ 与 γ² 正交：Tr(γ¹·γ²) = 0。 -/
theorem gamma1_ortho_gamma2 : Matrix.trace (gamma1 * gamma2) = 0 := by
  simp [Matrix.trace, gamma1, gamma2, Matrix.mul_apply, Fin.sum_univ_four]

/-- ★★ γ⁰ 自内积范数：Tr(γ⁰·γ⁰) = 4（γ⁰²=1 ⟹ 迹=4，字积对角范数 +4）。 -/
theorem gamma0_sq_trace_four : Matrix.trace (gamma0 * gamma0) = 4 := by
  simp [Matrix.trace, gamma0, Matrix.mul_apply, Fin.sum_univ_four]
  norm_num

/-- ★★ γ¹ 自内积范数：Tr(γ¹·γ¹) = −4（γ¹²=−1 ⟹ 迹=−4，字积对角范数 −4）。 -/
theorem gamma1_sq_trace_four : Matrix.trace (gamma1 * gamma1) = -4 := by
  simp [Matrix.trace, gamma1, Matrix.mul_apply, Fin.sum_univ_four]
  norm_num

/-- ★★ 伪标量字积无迹：Tr(γ⁰·γ¹·γ²·γ³) = 0（γ₅ 型字积在 4×4 中无迹）。 -/
theorem pseudoscalar_word_trace_zero : Matrix.trace (gamma0 * gamma1 * gamma2 * gamma3) = 0 := by
  simp [Matrix.trace, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_four]

/-! ## 翻倍勾股族补翼（#69：cosh/sinh 实例——三层桥能量/动量侧）

tanh 侧已机检（#64/#66：3-4-5/8-15-17/255-32-257）。
cosh/sinh 侧给出洛伦兹因子与动量的勾股身份：
cosh(2·ln2)=17/8（γ=17/8，v=15/17）、cosh(4·ln2)=257/32（16 态窗口 γ 因子）、
sinh(2·ln2)=15/8、sinh(4·ln2)=255/32（窗口动量倍数）。
勾股族双侧（tanh=速度、cosh=γ 因子、sinh=动量倍数）闭环。 -/

/-- ★★ 两步 γ 因子：cosh(2·ln2) = 17/8（8-15-17 勾股的斜边/短边）。 -/
theorem cosh_two_log_two : Real.cosh (2 * Real.log 2) = 17 / 8 := by
  have hlog : Real.log ((2 : ℝ) ^ 2) = 2 * Real.log 2 := by
    rw [Real.log_pow]
    try norm_num
  calc
    Real.cosh (2 * Real.log 2) = Real.cosh (Real.log ((2 : ℝ) ^ 2)) := by rw [← hlog]
    _ = ((2 : ℝ) ^ 2 + ((2 : ℝ) ^ 2)⁻¹) / 2 := by
      rw [Real.cosh_log (by positivity)]
    _ = 17 / 8 := by norm_num

/-- ★★ 两步动量倍数：sinh(2·ln2) = 15/8（8-15-17 勾股的中边/短边）。 -/
theorem sinh_two_log_two : Real.sinh (2 * Real.log 2) = 15 / 8 := by
  have hlog : Real.log ((2 : ℝ) ^ 2) = 2 * Real.log 2 := by
    rw [Real.log_pow]
    try norm_num
  calc
    Real.sinh (2 * Real.log 2) = Real.sinh (Real.log ((2 : ℝ) ^ 2)) := by rw [← hlog]
    _ = ((2 : ℝ) ^ 2 - ((2 : ℝ) ^ 2)⁻¹) / 2 := by
      rw [Real.sinh_log (by positivity)]
    _ = 15 / 8 := by norm_num

/-- ★★ 四步（16 态窗口）γ 因子：cosh(4·ln2) = 257/32（255-32-257 勾股斜边/短边）。 -/
theorem cosh_four_log_two : Real.cosh (4 * Real.log 2) = 257 / 32 := by
  have hlog : Real.log ((2 : ℝ) ^ 4) = 4 * Real.log 2 := by
    rw [Real.log_pow]
    try norm_num
  calc
    Real.cosh (4 * Real.log 2) = Real.cosh (Real.log ((2 : ℝ) ^ 4)) := by rw [← hlog]
    _ = ((2 : ℝ) ^ 4 + ((2 : ℝ) ^ 4)⁻¹) / 2 := by
      rw [Real.cosh_log (by positivity)]
    _ = 257 / 32 := by norm_num

/-- ★★ 四步（16 态窗口）动量倍数：sinh(4·ln2) = 255/32（255-32-257 勾股中边/短边）。 -/
theorem sinh_four_log_two : Real.sinh (4 * Real.log 2) = 255 / 32 := by
  have hlog : Real.log ((2 : ℝ) ^ 4) = 4 * Real.log 2 := by
    rw [Real.log_pow]
    try norm_num
  calc
    Real.sinh (4 * Real.log 2) = Real.sinh (Real.log ((2 : ℝ) ^ 4)) := by rw [← hlog]
    _ = ((2 : ℝ) ^ 4 - ((2 : ℝ) ^ 4)⁻¹) / 2 := by
      rw [Real.sinh_log (by positivity)]
    _ = 255 / 32 := by norm_num

-- ------------------------------------------------------------
-- S154：连续谱流单调性（2026-10-27）——rapidity 参数连续版本的
-- 时间箭头（S141 开放项：连续谱流版本单调性——tanh_log_pow_two 族）
--
-- 离散版本（S141 已 Lean）：谱序单调（λ_k 递增——谱位置序）。
-- 连续版本：谱流 A_t = U_t·A₀·U_t⁻¹ 是等谱变形（spectral_invariance
-- ——S102 已证——特征值沿谱流不变），时间箭头在**参数推进方向**：
-- rapidity φ 连续单调 ⟹ 速度 v = tanh φ 与 γ = cosh φ 严格单调增加。
-- "谱流的时间 = 等谱旋转的参数单调推进"——连续单调的代数核。
-- ------------------------------------------------------------

/-- ★★ 连续谱流单调性——tanh 严格单调（S154）：φ₁ < φ₂ ⟹
    v₁ = tanh φ₁ < v₂ = tanh φ₂——rapidity 连续推进 = 速度单调增加
    （时间箭头连续版本的代数核——S141 开放项闭合候选）。
    证明：tanh φ₂ − tanh φ₁ = sinh(φ₂−φ₁)/(cosh φ₁·cosh φ₂) > 0
    （sinh 差公式 + sinh 正 + cosh 正）。 -/
theorem rapidity_tanh_strictMono {φ₁ φ₂ : ℝ} (h : φ₁ < φ₂) :
    Real.tanh φ₁ < Real.tanh φ₂ := by
  have hd : 0 < Real.sinh (φ₂ - φ₁) := by
    rw [Real.sinh_eq]
    have hpos : 0 < φ₂ - φ₁ := sub_pos.mpr h
    have he₁ : Real.exp (-(φ₂ - φ₁)) < Real.exp (φ₂ - φ₁) := Real.exp_strictMono (by nlinarith)
    nlinarith
  have hden : 0 < Real.cosh φ₁ * Real.cosh φ₂ := mul_pos (Real.cosh_pos φ₁) (Real.cosh_pos φ₂)
  have hdiff : Real.tanh φ₂ - Real.tanh φ₁ =
      Real.sinh (φ₂ - φ₁) / (Real.cosh φ₁ * Real.cosh φ₂) := by
    rw [Real.tanh_eq_sinh_div_cosh, Real.tanh_eq_sinh_div_cosh]
    field_simp
    rw [← Real.sinh_sub]
  have hposdiff : 0 < Real.tanh φ₂ - Real.tanh φ₁ := by
    rw [hdiff]
    exact div_pos hd hden
  exact sub_pos.mp hposdiff

/-- ★★ 连续谱流单调性——cosh 严格单调（非负参数——S154）：0 ≤ φ₁
    < φ₂ ⟹ γ₁ = cosh φ₁ < γ₂ = cosh φ₂——γ 因子随 rapidity 单调增加
    （质量-能量标度 γ = cosh φ 的连续单调——S42/rapidity_additive 族）。
    证明路径：cosh² = 1+sinh²（本文件 cosh_sq_sub_sinh_sq）+ sinh 全局
    严格单调（sinh_strictMono）——cosh 非负（cosh_pos）。 -/
theorem rapidity_cosh_strictMonoOn {φ₁ φ₂ : ℝ} (h₁ : 0 ≤ φ₁) (h₂ : φ₁ < φ₂) :
    Real.cosh φ₁ < Real.cosh φ₂ := by
  have hsin₀ : 0 ≤ Real.sinh φ₁ := by
    by_cases h0 : φ₁ = 0
    · simp [h0]
    · have hgt : 0 < φ₁ := lt_of_le_of_ne h₁ (Ne.symm h0)
      have hle' : -φ₁ < φ₁ := by linarith
      have hle : Real.exp (-φ₁) < Real.exp φ₁ := Real.exp_strictMono hle'
      rw [Real.sinh_eq]
      nlinarith
  have hsin : Real.sinh φ₁ < Real.sinh φ₂ := by
    rw [Real.sinh_eq, Real.sinh_eq]
    have he₁ : Real.exp φ₁ < Real.exp φ₂ := Real.exp_strictMono h₂
    have he₂ : Real.exp (-φ₂) < Real.exp (-φ₁) := Real.exp_strictMono (by linarith)
    nlinarith
  have hsum : 0 < Real.sinh φ₂ + Real.sinh φ₁ := by nlinarith [hsin₀, hsin]
  have hprod : 0 < (Real.sinh φ₂ - Real.sinh φ₁) * (Real.sinh φ₂ + Real.sinh φ₁) :=
    mul_pos (sub_pos.mpr hsin) hsum
  have hring : (Real.sinh φ₂ - Real.sinh φ₁) * (Real.sinh φ₂ + Real.sinh φ₁) =
      Real.sinh φ₂ ^ 2 - Real.sinh φ₁ ^ 2 := by ring
  have hsq : Real.sinh φ₁ ^ 2 < Real.sinh φ₂ ^ 2 := by
    exact sub_pos.mp (by rwa [← hring])
  have hsqc : Real.cosh φ₁ ^ 2 < Real.cosh φ₂ ^ 2 := by
    have h₁' : Real.cosh φ₁ ^ 2 = 1 + Real.sinh φ₁ ^ 2 := by
      nlinarith [Real.cosh_sq_sub_sinh_sq φ₁]
    have h₂' : Real.cosh φ₂ ^ 2 = 1 + Real.sinh φ₂ ^ 2 := by
      nlinarith [Real.cosh_sq_sub_sinh_sq φ₂]
    nlinarith
  have habs : |Real.cosh φ₁| < |Real.cosh φ₂| := sq_lt_sq.mp hsqc
  rwa [abs_of_pos (Real.cosh_pos φ₁), abs_of_pos (Real.cosh_pos φ₂)] at habs

/-- ★★ 连续谱流"等谱+单调"合成（S154）：谱流保持谱（S102
    spectral_invariance——σ(A_t) = σ(A₀)）且 rapidity 参数严格单调
    （tanh/cosh 单调）——**时间箭头 = 等谱旋转的参数单调推进**——
    物理语义：质量读数沿谱流不变（massReadout_flow_invariant）但谱流
    参数持续推进——离散谱序（S141 λ_k 递增）与连续参数（φ 单调）是
    两个互补时间箭头。 -/
theorem flow_parameter_tanh_mono_compose {φ₁ φ₂ : ℝ} (h₁ : 0 ≤ φ₁) (h₂ : φ₁ < φ₂) :
    Real.tanh φ₁ < Real.tanh φ₂ ∧ Real.cosh φ₁ < Real.cosh φ₂ := by
  constructor
  · exact rapidity_tanh_strictMono h₂
  · exact rapidity_cosh_strictMonoOn h₁ h₂

/-- ★★ 速度级联单调（S157——2026-10-27——S154 开放候选闭合）：
    连续 boost 级联（rapidity 可加——S42 rapidity_additive 族——
    φ(β₁∘β₂) = φ₁+φ₂）⟹ 速度 v = tanh φ 随级联严格单调递增：
    φ₂ > 0 ⟹ tanh φ₁ < tanh(φ₁+φ₂)。
    ——时间箭头速度层：每级 boost 推进速度严格增加——与翻倍族
    （tanh_log_pow_two——离散 n·ln2）衔接——φ 可加（S42）+
    tanh 单调（S154 rapidity_tanh_strictMono）⟹ 速度级联。 -/
theorem velocity_cascade_mono {φ₁ φ₂ : ℝ} (hφ₂ : 0 < φ₂) :
    Real.tanh φ₁ < Real.tanh (φ₁ + φ₂) := by
  apply rapidity_tanh_strictMono
  linarith

/-- ★★ 级联 γ 因子单调（S157）：γ = cosh φ 随级联单调递增（级联
    boost 的质量-能量标度严格增加）——时间箭头的能量层——S154
    cosh 单调 + φ 可加。 -/
theorem cascade_gamma_mono {φ₁ φ₂ : ℝ} (hφ₁ : 0 ≤ φ₁) (hφ₂ : 0 < φ₂) :
    Real.cosh φ₁ < Real.cosh (φ₁ + φ₂) := by
  apply rapidity_cosh_strictMonoOn hφ₁
  linarith

/-- 标量半群单位推进（S166——2026-10-27——"为何每步 e"机制锚）：
    递归迭代的连续化 = 指数族半群（U(t)U(s)=U(t+s)——矩阵层已
    Lean：OperatorTheory.koopmanSemigroup）——标量核心：e^{−(t+s)}
    = e^{−t}·e^{−s}——单位推进 t=1：乘子 e^{−1}——"每步荷生成恰为
    e" = 单位谱流推进的特征乘子（S155 候选 B 深化——归约到 Lie
    理论：单参数群 = 指数映射——数学标准——诚实：'为何递归连续化
    = 半群'归 Rec 公设）。 -/
theorem scalar_semigroup_unit (t s : ℝ) :
    Real.exp (-(t + s)) = Real.exp (-t) * Real.exp (-s) := by
  rw [neg_add, Real.exp_add]

/-- 单位推进缩放底（S166 佐证）：e^{1·a} = e^{a}——谱流单位推进
    的特征乘子结构（t=1——指数族单参数群的单位元）——"每步 e"
    的标量核心。 -/
theorem exp_unit_advance (a : ℝ) : Real.exp (1 * a) = Real.exp a := by
  rw [one_mul]

/-- 半群整数迭代（S169——2026-10-27——S166 整数层深化）：
    n 步递归迭代 = 单位推进的 n 次幂 = exp(−(a·n))——离散→连续桥
    的整数层机检（时间 = 递归迭代——S150——半群单位推进 t=1——
    S166——"每步 e"的 n 步合成：乘子 e^{−a} 的 n 次幂）。
    证明：mathlib Real.exp_nat_mul（(exp x)^n = exp(n·x)）。 -/
theorem scalar_semigroup_int_iterate (a : ℝ) (n : ℕ) :
    (Real.exp (-a)) ^ n = Real.exp (-(a * (n : ℝ))) := by
  rw [← Real.exp_nat_mul]
  congr 1
  ring

/-- 标量压缩性（S171——2026-10-27——静默冻结的算子层机检）：
    谱流推进乘子 exp(−t·a)——a,t > 0 时每步压缩 exp(−t·a) < 1
    ——Koopman 压缩半群的标量核——对应静默冻结（每步荷衰减——
    用户裁决 2026-10-23：静默即不变且失去窗口）。 -/
theorem scalar_contraction (a : ℝ) (ha : 0 < a) (t : ℝ) (ht : 0 < t) :
    Real.exp (-(t * a)) < 1 := by
  rw [Real.exp_lt_one_iff]
  nlinarith

/-- 静默冻结零测度极限（S171——2026-10-27——t→∞ 窗口→0）：
    exp(−t·a) 随 t 严格递减到 0——"失去表达窗口"的算子表述——
    静默 = 闭合冻结零测度（S151）。 -/
theorem scalar_contraction_mono (a : ℝ) (ha : 0 < a) (t₁ t₂ : ℝ)
    (ht₁ : 0 ≤ t₁) (ht₂ : t₁ < t₂) :
    Real.exp (-(t₂ * a)) < Real.exp (-(t₁ * a)) := by
  rw [Real.exp_lt_exp]
  nlinarith

end MUFPF.MinkowskiBoost
