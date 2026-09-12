-- ============================================================
-- UFPF → MUFPF 更名通知（同 WeaveBCS.lean，本文件属于 UFPF/MUFPF）
-- ============================================================

/-
# SpectralInvariant.lean — paper14 G1：谱不变量在 Sp 同构下的保持（泛化核心）

背景：G1（远期核心）要求把 Paper XX 链（范畴 Δ → SU(2) Casimir → Cl(1,7) →
谱间隙，引力版 v0.5）泛化到凝聚态谱生成元。泛化的数学前提是：若两个谱生成元
由保持谱的映射（Sp 同构 = 可逆交织）联系，则它们共享全部谱不变量——尤其是
谱间隙。本模块证明这一前提的**迹刻画**：相似变换保持全部迹幂 tr(A^k)。

  §1 conj_pow_eq：相似幂公式 (Q·A·P)^k = Q·A^k·P（Q·P = 1 且 P·Q = 1）
  §2 trace_pow_similar：**G1 核心**——相似变换保持全部迹幂 tr(A^k)
  §3 开放登记：Newton 恒等式到谱间隙、凝聚态桥的具体构造、Paper XX 泛化

说明：迹幂 {tr(A^k)}_{k≥1} 经 Newton 恒等式生成特征值的初等对称多项式，即
完全决定谱（计重数）；故迹幂不变 ⟺ 谱不变 ⟹ 谱间隙不变。谱间隙的 Newton
恒等式翻译与 Paper XX 链对凝聚态生成元的具体桥构造属深层研究，登记开放。
-/

import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

namespace MUFPF

open Matrix Complex

/-- §1：相似幂公式——若 P·Q = 1 且 Q·P = 1（Q = P⁻¹），则 (Q·A·P)^k = Q·A^k·P。
    即相似变换与取幂交换。 -/
theorem conj_pow_eq {n : ℕ} (A P Q : Matrix (Fin n) (Fin n) ℂ)
    (hPQ : P * Q = 1) (hQP : Q * P = 1) (k : ℕ) :
    (Q * A * P) ^ k = Q * A ^ k * P := by
  induction k with
  | zero => rw [pow_zero, pow_zero, mul_one, hQP]
  | succ k ih =>
    rw [pow_succ, ih]
    -- (Q * A^k * P) * (Q * A * P) = Q * A^{k+1} * P
    have hrw : A ^ (k + 1) = A ^ k * A := pow_succ A k
    rw [hrw]
    have h1 : (Q * A ^ k * P) * (Q * A * P) = Q * A ^ k * (P * Q) * A * P := by
      noncomm_ring
    rw [h1, hPQ, mul_one]
    noncomm_ring

/-- §2：**G1 核心（谱不变量的相似不变性）**——若 B = Q·A·P 相似于 A
    （P·Q = 1 且 Q·P = 1，即 A 与 B 由可逆共轭联系——Sp 范畴同构的矩阵内容），
    则对任意 k，tr(B^k) = tr(A^k)。迹幂完全决定谱（计重数，经 Newton 恒等式），
    故相似（Sp 同构）保持谱、进而保持谱间隙。这是 Paper XX 链泛化到凝聚态
    谱生成元的前提：只要凝聚态生成元与 Paper XX 生成元之间存在 Sp 同构，
    二者即共享全部谱不变量（含谱间隙 dl_min 资产）。 -/
theorem trace_pow_similar {n : ℕ} (A P Q : Matrix (Fin n) (Fin n) ℂ)
    (hPQ : P * Q = 1) (hQP : Q * P = 1) (k : ℕ) :
    ((Q * A * P) ^ k).trace = (A ^ k).trace := by
  rw [conj_pow_eq A P Q hPQ hQP k, Matrix.trace_mul_comm (Q * A ^ k) P,
    ← mul_assoc, hPQ, one_mul]

/- §3 开放登记（paper14 G1 完整泛化，不占用 sorry，真证路径见下）：

  本模块建立了谱不变量相似不变性的迹刻画（迹幂保持）。以下完整内容属深层
  研究，登记为未来工作：

  1. **Newton 恒等式 → 谱间隙**：由 {tr(A^k)} 生成初等对称多项式 e_i（特征值
     的），谱间隙 = 相邻特征值最小间距是 e_i 的对称函数。需 Newton 恒等式的
     形式化 + 谱间隙的对称函数表达（中等，可分段闭合）。
  2. **酉共轭特例**：A 厄米时相似可取得 U 酉（Uᴴ U = 1），谱间隙不变在酉等价
     下是谱定理的直接推论（mathlib 有 Matrix.IsHermitian 谱定理基础设施）。
  3. **凝聚态桥的具体构造（G1 完整目标）**：证明凝聚态谱生成元
     （如 A_SC = ξ σ_z + Δ σ_x，paper14 §2.1）经由显式 Sp 同构与 Paper XX 的
     SU(2)/Cl(1,7) 生成元联系。需具体构造保持谱的映射并验证交织条件——
     这是「范畴 Δ 内生谱间隙对凝聚态同样适用」的核心论证，属框架级研究
     （与 notes/02_superconductivity 的 G1 缺口直接对应）。
  4. **范畴 Δ 的泛性质**：证明 SU(2) Casimir 谱 ∝ √(k(k+1)) 与 Cl(1,7) 谱间隙
     是 Δ（Sp 4-范畴交换律偏差）的泛性质结果，与引力/凝聚态无关——这是
     「同一范畴 Δ 对凝聚态生成元同样适用」的最终依据，需 Paper XX 链的
     完整重构。

  已闭合（本模块，零 sorry）：相似变换保持全部迹幂（谱不变量相似不变性的
  迹刻画）——Paper XX 链泛化的数学前提。-/

end MUFPF
