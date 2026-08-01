module IFSFractal.IFSFractal where

{-
  B8: IFS 排序定理（IFS Fractal）
  ================================
  对应 Lean: IFSFractal.lean §5-§6

  物理 3-map IFS：3 个映射，收缩率来自 Cl(1,7) 谱静默结构。
    c1 = e^(-3-d)（对象静默 × 辫静默的联合压制）
    c2 = e^(-d)（辫静默）
    c3 = (1 - c1^d - c2^d)^(1/d)（Moran 方程唯一确定）

  O2 统一性定理（核心，§6）：三个收缩率严格相异且有序
    c1 < c2 < c3 < 1（d ≥ 1）。
  这是三条动力学路径（谱流 3 不动点 / IFS 3 簇 / 信息论最小化）
  共享的同一结构核心——三个"3"是同一个 3。

  说明：收缩率的解析性质（正性、<1、Moran 方程、排序）在 Lean 中
  由 exp/log/rpow 分析证明；Agda 在占位 ℝ 公理下以 postulate 声明。
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; _×_; _,_; sym; trans; cong; cong₂)
open import NatArith.NatArith
open import DHStructural.DHStructuralAnalysis

-- ==================================================================
-- §5 物理 3-map IFS
-- ==================================================================

-- 收缩率 c₁(d) = e^{-3-d}（对应 Lean: c1_physical）
c1-physical : ℝ → ℝ
c1-physical d = exp (negℝ (natℝ 3 +ℝ d))

-- 收缩率 c₂(d) = e^{-d}（对应 Lean: c2_physical）
c2-physical : ℝ → ℝ
c2-physical d = exp (negℝ d)

-- 收缩率 c₃(d) = (1 - c₁^d - c₂^d)^{1/d}（对应 Lean: c3_physical）
c3-physical : ℝ → ℝ
c3-physical d = ((oneℝ -ℝ ((c1-physical d) ^-ℝ d)) -ℝ ((c2-physical d) ^-ℝ d)) ^-ℝ (oneℝ /ℝ d)

-- c₁, c₂ 恒正（对应 Lean: c1_physical_pos / c2_physical_pos）
-- （**T3 阶段 4 闭合 2026-07-31**：exp-pos）
c1-physical-pos : (d : ℝ) → zeroℝ <ℝ c1-physical d
c1-physical-pos d = exp-pos (negℝ (natℝ 3 +ℝ d))

c2-physical-pos : (d : ℝ) → zeroℝ <ℝ c2-physical d
c2-physical-pos d = exp-pos (negℝ d)

-- c₁^d = e^{-d(3+d)}（rpow-exp + log-exp + 取负乘法）
c1d-exp : (d : ℝ) → (c1-physical d) ^-ℝ d ≡ exp (negℝ (d *ℝ (natℝ 3 +ℝ d)))
c1d-exp d =
  trans (rpow-exp (c1-physical d) d)
        (trans (cong (λ x → exp (d *ℝ x)) (log-exp (negℝ (natℝ 3 +ℝ d))))
               (cong exp neg-mul-3d))
  where
  -- d·(-(3+d)) = -(d·(3+d))（交换 + 取负乘法）
  neg-mul-3d : (d *ℝ negℝ (natℝ 3 +ℝ d)) ≡ negℝ (d *ℝ (natℝ 3 +ℝ d))
  neg-mul-3d =
    trans (*-comm-ℝ d (negℝ (natℝ 3 +ℝ d)))
          (trans (neg-mul-ℝ (natℝ 3 +ℝ d) d)
                 (cong negℝ (*-comm-ℝ (natℝ 3 +ℝ d) d)))

-- c₂^d = e^{-d²}（rpow-exp + log-exp + 取负乘法）
c2d-exp : (d : ℝ) → (c2-physical d) ^-ℝ d ≡ exp (negℝ (d *ℝ d))
c2d-exp d =
  trans (rpow-exp (c2-physical d) d)
        (trans (cong (λ x → exp (d *ℝ x)) (log-exp (negℝ d)))
               (cong exp neg-mul-d))
  where
  -- d·(-d) = -(d·d)（交换 + 取负乘法）
  neg-mul-d : (d *ℝ negℝ d) ≡ negℝ (d *ℝ d)
  neg-mul-d =
    trans (*-comm-ℝ d (negℝ d))
          (trans (neg-mul-ℝ d d)
                 (cong negℝ (*-comm-ℝ d d)))

-- 三个收缩率均 < 1（d ≥ 1）
-- （对应 Lean: c1_physical_lt_one / c2_physical_lt_one / c3_physical_lt_one）
-- （**T3 阶段 4 闭合 2026-07-31**：c₁/c₂ 经 exp-mono + 取负 + d≥1⟹0<d；c₃ 待 rpow 机制）
-- d ≥ 1 ⟹ 0 < d
≤-pos : {d : ℝ} → natℝ 1 ≤ℝ d → zeroℝ <ℝ d
≤-pos {d} h = lt-≤-trans-ℝ (subst (λ x → zeroℝ <ℝ x) (sym natℝ-one) zero-lt-one-ℝ) h

-- c₁ = e^{-(3+d)} 与 c₂ = e^{-d} 均 < 1（d ≥ 1）
c1-physical-lt-one : (d : ℝ) → natℝ 1 ≤ℝ d → c1-physical d <ℝ natℝ 1
c1-physical-lt-one d h =
  subst (λ y → exp (negℝ (natℝ 3 +ℝ d)) <ℝ y) (sym natℝ-one)
    (subst (λ y → exp (negℝ (natℝ 3 +ℝ d)) <ℝ y) (exp-zero)
           (exp-mono neg-3d-lt-zero))
  where
  3+d-pos : zeroℝ <ℝ (natℝ 3 +ℝ d)
  3+d-pos =
    subst (λ x → x <ℝ (natℝ 3 +ℝ d)) (+-ident-ℝ zeroℝ)
          (lt-+-mono-ℝ (natℝ-pos-embed z<s) (≤-pos h))
  neg-3d-lt-zero : negℝ (natℝ 3 +ℝ d) <ℝ zeroℝ
  neg-3d-lt-zero =
    subst (λ y → negℝ (natℝ 3 +ℝ d) <ℝ y) (neg-zero)
          (neg-<-ℝ (3+d-pos))

c2-physical-lt-one : (d : ℝ) → natℝ 1 ≤ℝ d → c2-physical d <ℝ natℝ 1
c2-physical-lt-one d h =
  subst (λ y → exp (negℝ d) <ℝ y) (sym natℝ-one)
    (subst (λ y → exp (negℝ d) <ℝ y) (exp-zero)
           (exp-mono (subst (λ y → negℝ d <ℝ y) (neg-zero) (neg-<-ℝ (≤-pos h)))))

-- c₁ < c₂（c-physical-strictly-ordered 的第一分量；**T3 阶段 4 闭合 2026-07-31**）
-- c₁ = e^{-(3+d)} < e^{-d} = c₂ ⟸ exp-mono + -(3+d) < -d ⟸ 3+d > d
c1-lt-c2-physical : (d : ℝ) → c1-physical d <ℝ c2-physical d
c1-lt-c2-physical d = exp-mono (neg-<-ℝ (d-lt-3+d))
  where
  d-lt-3+d : d <ℝ (natℝ 3 +ℝ d)
  d-lt-3+d =
    subst (λ x → x <ℝ (natℝ 3 +ℝ d)) (zero-add-ℝ d)
          (lt-+-mono-l-ℝ {a = zeroℝ} {b = natℝ 3} {c = d} (natℝ-pos-embed z<s))

-- Moran 方程对物理 3-map IFS 成立（d ≥ 1）：c₁^d + c₂^d + c₃^d = 1
-- （对应 Lean: moran_3map_holds）
-- （**T3 阶段 4 闭合 2026-07-31**：c₃^d = ((1-c₁^d)-c₂^d)^((1/d)·d) = 1-c₁^d-c₂^d
--   [rpow-pow + (1/d)·d=1 + rpow-one]，(c₁^d+c₂^d)+((1-c₁^d)-c₂^d) = 1 [cancel-sub]；
--   不再是 postulate）
moran-3map-holds : (d : ℝ) → natℝ 1 ≤ℝ d
  → (((c1-physical d) ^-ℝ d) +ℝ ((c2-physical d) ^-ℝ d)) +ℝ ((c3-physical d) ^-ℝ d) ≡ oneℝ
moran-3map-holds d h =
  trans (cong (λ u → (((c1-physical d) ^-ℝ d) +ℝ ((c2-physical d) ^-ℝ d)) +ℝ u) c3d-eq)
        (cancel-sub c1d c2d oneℝ)
  where
  c1d : ℝ
  c1d = (c1-physical d) ^-ℝ d
  c2d : ℝ
  c2d = (c2-physical d) ^-ℝ d
  -- (1/d)·d = 1（经交换 + 商消去）
  one-over-d-mul-d : (oneℝ /ℝ d) *ℝ d ≡ oneℝ
  one-over-d-mul-d = trans (*-comm-ℝ (oneℝ /ℝ d) d) (*-/cancel-ℝ d oneℝ)
  -- c₃^d = ((1-c₁^d)-c₂^d)^((1/d)·d) = ((1-c₁^d)-c₂^d)^1 = (1-c₁^d)-c₂^d
  c3d-eq : (c3-physical d) ^-ℝ d ≡ ((oneℝ -ℝ c1d) -ℝ c2d)
  c3d-eq =
    trans (rpow-pow ((oneℝ -ℝ c1d) -ℝ c2d) (oneℝ /ℝ d) d)
          (trans (cong (λ x → ((oneℝ -ℝ c1d) -ℝ c2d) ^-ℝ x) one-over-d-mul-d)
                 (rpow-one ((oneℝ -ℝ c1d) -ℝ c2d)))

-- ==================================================================
-- §6 O2 统一性定理：三相异收缩率
-- ==================================================================

-- 关键定量引理（d ≥ 1）：2·e^{-d²} + e^{-d(3+d)} < 1
-- （对应 Lean: two_exp_add_exp_lt_one）
-- （**T3 阶段 4 闭合 2026-07-31**：d² ≥ 1 ⟹ e^{-d²} < 37/100；
--   d(3+d) ≥ 4 ⟹ e^{-d(3+d)} < 13/100 [e⁻⁴ < 1/8 < 13/100]；
--   2e^{-d²} < 74/100 [乘 2 保序]，和 < 74/100 + 13/100 = 87/100 < 1；
--   不再是 postulate）
two-exp-add-exp-lt-one : (d : ℝ) → natℝ 1 ≤ℝ d
  → (((natℝ 2) *ℝ (exp (negℝ (d *ℝ d)))) +ℝ (exp (negℝ (d *ℝ (natℝ 3 +ℝ d))))) <ℝ oneℝ
two-exp-add-exp-lt-one d h =
  trans-<ℝ (subst (λ y → (((natℝ 2) *ℝ (exp (negℝ (d *ℝ d)))) +ℝ
                          (exp (negℝ (d *ℝ (natℝ 3 +ℝ d))))) <ℝ y) sum-87
                  (lt-+-mono-ℝ two-lt neg-lt))
           87-100-lt-1
  where
  -- 2·(37/100) = 74/100
  two-37-74 : (natℝ 2 *ℝ (natℝ 37 /ℝ natℝ 100)) ≡ (natℝ 74 /ℝ natℝ 100)
  two-37-74 = trans (*-/ℝ (natℝ 2) (natℝ 37) (natℝ 100)) (cong₂ _/ℝ_ (sym (natℝ-* 2 37)) refl)
  -- 2·e^{-d²} < 2·37/100 = 74/100（乘 2 保序 + 分子并入）
  two-lt : ((natℝ 2) *ℝ (exp (negℝ (d *ℝ d)))) <ℝ (natℝ 74 /ℝ natℝ 100)
  two-lt =
    subst (λ y → ((natℝ 2) *ℝ (exp (negℝ (d *ℝ d)))) <ℝ y) two-37-74
          (*-pos-mono-ℝ {a = exp (negℝ (d *ℝ d))} {b = (natℝ 37 /ℝ natℝ 100)} {c = natℝ 2}
                        (natℝ-pos-embed z<s) (exp-neg-d2-lt-37-100 d h))
  -- e^{-d(3+d)} < 13/100
  neg-lt : exp (negℝ (d *ℝ (natℝ 3 +ℝ d))) <ℝ (natℝ 13 /ℝ natℝ 100)
  neg-lt = exp-neg-d3d-lt-13-100 d h
  -- 74/100 + 13/100 = 87/100（同分母加法）
  sum-87 : (natℝ 74 /ℝ natℝ 100) +ℝ (natℝ 13 /ℝ natℝ 100) ≡ (natℝ 87 /ℝ natℝ 100)
  sum-87 = trans (/-add-same-ℝ (natℝ 74) (natℝ 13) (natℝ 100))
                 (cong₂ _/ℝ_ (sym (natℝ-+ 74 13)) refl)
  -- 87/100 < 1（87 < 100 同分母比较 + 100/100 = 1）
  87-lt-100 : 87 <ℕ 100
  87-lt-100 = <-trans (<-suc 87) (<-trans (<-suc 88) (<-trans (<-suc 89) (<-trans (<-suc 90) (<-trans (<-suc 91) (<-trans (<-suc 92) (<-trans (<-suc 93) (<-trans (<-suc 94) (<-trans (<-suc 95) (<-trans (<-suc 96) (<-trans (<-suc 97) (<-trans (<-suc 98) (<-suc 99))))))))))))
  100-over-100 : (natℝ 100 /ℝ natℝ 100) ≡ oneℝ
  100-over-100 =
    trans (/-cross-ℝ (trans (cong₂ _*ℝ_ refl natℝ-one)
                            (trans (*-ident-ℝ (natℝ 100))
                                   (trans (sym (one-mul-ℝ (natℝ 100)))
                                          (sym (cong₂ _*ℝ_ natℝ-one refl))))))
          (trans (cong₂ _/ℝ_ natℝ-one natℝ-one) (div-one-ℝ oneℝ))
  87-100-lt-1 : (natℝ 87 /ℝ natℝ 100) <ℝ oneℝ
  87-100-lt-1 =
    subst (λ y → (natℝ 87 /ℝ natℝ 100) <ℝ y) 100-over-100
          (/-lt-same-den-ℝ {natℝ 87} {natℝ 100} {natℝ 100} (natℝ-<-embed 87-lt-100))

-- c₃ 的底数严格为正（d ≥ 1）
-- （对应 Lean: one_sub_c1d_c2d_pos；2/e < 1 控制）
-- （**T3 阶段 4 闭合 2026-07-31**：c₁^d+c₂^d < 2e^{-d²}+e^{-d(3+d)} < 1
--   [c₂^d = e^{-d²} > 0 ⟹ c₂^d < 2c₂^d；two-exp-add-exp-lt-one]，
--   pos-sub 得 0 < (1-c₁^d)-c₂^d；不再是 postulate）
one-sub-c1d-c2d-pos : (d : ℝ) → natℝ 1 ≤ℝ d
  → zeroℝ <ℝ ((oneℝ -ℝ ((c1-physical d) ^-ℝ d)) -ℝ ((c2-physical d) ^-ℝ d))
one-sub-c1d-c2d-pos d h =
  subst (λ x → zeroℝ <ℝ ((oneℝ -ℝ x) -ℝ c2d)) (sym (c1d-exp d))
    (subst (λ y → zeroℝ <ℝ ((oneℝ -ℝ e1) -ℝ y)) (sym (c2d-exp d))
           (pos-sub sum-lt))
  where
  e1 : ℝ
  e1 = exp (negℝ (d *ℝ (natℝ 3 +ℝ d)))
  e2 : ℝ
  e2 = exp (negℝ (d *ℝ d))
  c2d : ℝ
  c2d = (c2-physical d) ^-ℝ d
  -- e₂ < 2·e₂（1 < 2 乘正保序）
  e2-lt-2e2 : e2 <ℝ (natℝ 2 *ℝ e2)
  e2-lt-2e2 =
    subst (λ u → u <ℝ (natℝ 2 *ℝ e2)) (*-ident-ℝ e2)
          (subst (λ y → (e2 *ℝ oneℝ) <ℝ y) (*-comm-ℝ e2 (natℝ 2))
                 (*-pos-mono-ℝ {a = oneℝ} {b = natℝ 2} {c = e2}
                               (exp-pos (negℝ (d *ℝ d)))
                               one-lt-2-ℝ))
  -- e₁ + e₂ < e₁ + 2e₂
  sum-lt-sum : (e1 +ℝ e2) <ℝ (e1 +ℝ (natℝ 2 *ℝ e2))
  sum-lt-sum = lt-+-mono-r-ℝ e2-lt-2e2
  -- e₁ + 2e₂ < 1（two-exp：2e₂ + e₁ < 1，交换两项）
  sum-2-lt-1 : (e1 +ℝ (natℝ 2 *ℝ e2)) <ℝ oneℝ
  sum-2-lt-1 =
    subst (λ x → x <ℝ oneℝ) (sym (+-comm-ℝ e1 (natℝ 2 *ℝ e2)))
          (two-exp-add-exp-lt-one d h)
  -- e₁ + e₂ < 1
  sum-lt : (e1 +ℝ e2) <ℝ oneℝ
  sum-lt = trans-<ℝ sum-lt-sum sum-2-lt-1

-- c₃ 恒正（d ≥ 1）（对应 Lean: c3_physical_pos）
-- （**T3 阶段 4 闭合 2026-07-31**：c₃ = ((1-c₁^d)-c₂^d)^{1/d}，
--   底数正 [one-sub-c1d-c2d-pos] + rpow-pos（a^b = exp(b·log a) > 0）；
--   不再是 postulate）
c3-physical-pos : (d : ℝ) → natℝ 1 ≤ℝ d → zeroℝ <ℝ c3-physical d
c3-physical-pos d h =
  rpow-pos {a = (oneℝ -ℝ ((c1-physical d) ^-ℝ d)) -ℝ ((c2-physical d) ^-ℝ d)}
           {b = oneℝ /ℝ d} (one-sub-c1d-c2d-pos d h)

-- c₃^d = (1-c₁^d)-c₂^d（rpow 幂合成 + (1/d)·d=1 + rpow-one）
c3d-base : (d : ℝ) → (c3-physical d) ^-ℝ d ≡ ((oneℝ -ℝ ((c1-physical d) ^-ℝ d)) -ℝ ((c2-physical d) ^-ℝ d))
c3d-base d =
  trans (rpow-pow ((oneℝ -ℝ c1d) -ℝ c2d) (oneℝ /ℝ d) d)
        (trans (cong (λ x → ((oneℝ -ℝ c1d) -ℝ c2d) ^-ℝ x) one-over-d-mul-d)
               (rpow-one ((oneℝ -ℝ c1d) -ℝ c2d)))
  where
  c1d : ℝ
  c1d = (c1-physical d) ^-ℝ d
  c2d : ℝ
  c2d = (c2-physical d) ^-ℝ d
  -- (1/d)·d = 1（经交换 + 商消去）
  one-over-d-mul-d : (oneℝ /ℝ d) *ℝ d ≡ oneℝ
  one-over-d-mul-d = trans (*-comm-ℝ (oneℝ /ℝ d) d) (*-/cancel-ℝ d oneℝ)

-- c₂ < c₃（d ≥ 1）（对应 Lean: c2_lt_c3_physical）
-- （**T3 阶段 4 闭合 2026-07-31**：c₂^d = e^{-d²} < (1-c₁^d)-c₂^d = c₃^d
--   [two-exp：2e^{-d²}+e^{-d(3+d)}<1 移项]，rpow-mono-inv-ℝ（正底数、正指数）
--   ⟹ c₂ < c₃；不再是 postulate）
c2-lt-c3-physical : (d : ℝ) → natℝ 1 ≤ℝ d → c2-physical d <ℝ c3-physical d
c2-lt-c3-physical d h =
  rpow-mono-inv-ℝ {a = c2-physical d} {b = c3-physical d} {c = d}
                  (c2-physical-pos d) (c3-physical-pos d h) (≤-pos h)
                  (subst (λ x → ((c2-physical d) ^-ℝ d) <ℝ x) (sym (c3d-base d)) e2-lt-a)
  where
  e1 : ℝ
  e1 = exp (negℝ (d *ℝ (natℝ 3 +ℝ d)))
  e2 : ℝ
  e2 = exp (negℝ (d *ℝ d))
  -- 2e₂ < 1 - e₁（two-exp 移项：2e₂+e₁<1）
  sub-1 : (natℝ 2 *ℝ e2) <ℝ (oneℝ -ℝ e1)
  sub-1 = sub-elim (two-exp-add-exp-lt-one d h)
  -- e₂ < 1 - e₁ - e₂（移项两次：2e₂ < 1-e₁ ⟹ e₂ < (1-e₁)-e₂）
  e2-lt-sub : e2 <ℝ ((oneℝ -ℝ e1) -ℝ e2)
  e2-lt-sub = sub-elim (subst (λ x → x <ℝ (oneℝ -ℝ e1)) (two-mul-add e2) sub-1)
  -- c₂^d < (1-c₁^d)-c₂^d（替换 e₁→c₁^d、e₂→c₂^d）
  e2-lt-a : ((c2-physical d) ^-ℝ d) <ℝ ((oneℝ -ℝ ((c1-physical d) ^-ℝ d)) -ℝ ((c2-physical d) ^-ℝ d))
  e2-lt-a =
    subst (λ x → x <ℝ ((oneℝ -ℝ c1d) -ℝ c2d)) (sym (c2d-exp d))
      (subst (λ y → e2 <ℝ ((oneℝ -ℝ y) -ℝ c2d)) (sym (c1d-exp d))
        (subst (λ z → e2 <ℝ ((oneℝ -ℝ e1) -ℝ z)) (sym (c2d-exp d)) e2-lt-sub))
    where
    c1d : ℝ
    c1d = (c1-physical d) ^-ℝ d
    c2d : ℝ
    c2d = (c2-physical d) ^-ℝ d

-- **O2 统一性定理（核心）**：c₁ < c₂ < c₃（d ≥ 1）
-- （对应 Lean: c_physical_strictly_ordered）
-- （**T3 阶段 4 闭合 2026-07-31**：c₁<c₂ [c1-lt-c2-physical] ×
--   c₂<c₃ [c2-lt-c3-physical]；不再是 postulate）
c-physical-strictly-ordered : (d : ℝ) → natℝ 1 ≤ℝ d
  → (c1-physical d <ℝ c2-physical d) × (c2-physical d <ℝ c3-physical d)
c-physical-strictly-ordered d h = c1-lt-c2-physical d , c2-lt-c3-physical d h

-- 物理 3-map IFS（简化记录：映射数 + 三个收缩率）
-- （对应 Lean: physicalIFS）
record PhysicalIFS : Set where
  field
    n : ℕ
    ratio0 : ℝ
    ratio1 : ℝ
    ratio2 : ℝ

physicalIFS : {d : ℝ} → PhysicalIFS
physicalIFS {d} = record
  { n = 3
  ; ratio0 = c1-physical d
  ; ratio1 = c2-physical d
  ; ratio2 = c3-physical d
  }

-- physicalIFS 的映射数 = 3（对应 Lean: physicalIFS_n）
physicalIFS-n : {d : ℝ} → PhysicalIFS.n (physicalIFS {d}) ≡ 3
physicalIFS-n = refl

-- O2 路径 B 的形式化核心：三个收缩率严格递增
-- （对应 Lean: physicalIFS_ratios_ordered）
-- （**T3 阶段 4 闭合 2026-07-31**：ratio0=c₁ < ratio1=c₂ < ratio2=c₃
--   [c-physical-strictly-ordered]；不再是 postulate）
physicalIFS-ratios-ordered : {d : ℝ} → natℝ 1 ≤ℝ d
  → (PhysicalIFS.ratio0 (physicalIFS {d}) <ℝ PhysicalIFS.ratio1 (physicalIFS {d}))
      × (PhysicalIFS.ratio1 (physicalIFS {d}) <ℝ PhysicalIFS.ratio2 (physicalIFS {d}))
physicalIFS-ratios-ordered {d} h = c-physical-strictly-ordered d h
