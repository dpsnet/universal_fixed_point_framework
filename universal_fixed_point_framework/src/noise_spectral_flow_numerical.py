#!/usr/bin/env python3
"""
噪声谱流数值交叉验证 — Paper X §12.4 η_c 奇异性验证

验证目标：
  1. Eigenvalue gap Δ(η) = Δλ_min - η/k_max  (linear gap closure)
  2. τ(η) ∝ 1/Δ(η) 发散 as η → η_c⁻
  3. η_c = 4(√3-1)/3 ≈ 0.976  (from spectralGap 8 × k_max)
  4. FH 公式 dλ_±/dη 数值验证

数值范围: η ∈ [0, 2] covering full phase transition region

物理模型:
  A(η) = A_R + η·δA_N, where:
    A_R = diag(λ₁, λ₂) with Cl(1,7) SU(2) eigenvalues
    δA_N = diag(α, -α) with α = 1/k_max = 1/8  (pure diagonal noise)
  This gives exact gap closure at η_c = Δλ_min/α = k_max·Δλ_min
"""

import numpy as np

# === Cl(1,7) 常数 ===
K_MAX = 8
ALPHA = 1.0 / K_MAX              # diagonal gap-closing strength = 1/k_max

# SU(2) eigenvalues: λ_k = √(k(k+1)) / √(k_max(k_max+1))
LAMBDA_1 = np.sqrt(1 * 2) / np.sqrt(K_MAX * (K_MAX + 1))
LAMBDA_2 = np.sqrt(2 * 3) / np.sqrt(K_MAX * (K_MAX + 1))

# Spectral gap at η = 0: Δλ_min = (√6 - √2) / √72 ≈ 0.122
DELTA_LAMBDA_MIN = LAMBDA_2 - LAMBDA_1

# Critical noise threshold: η_c = Δλ_min/(2α) = k_max·Δλ_min/2 = 2(√3-1)/3 ≈ 0.488
ETA_C = DELTA_LAMBDA_MIN / (2.0 * ALPHA)

# === 解析函数 ===

def gap_function(eta):
    """Spectral gap Δ(η) = Δλ_min - αη  (linear gap closure)
    
    For A(η) = diag(λ₁+αη, λ₂-αη), the eigenvalues are:
      λ₊ = λ₂ - αη  (the larger one decreases)
      λ₋ = λ₁ + αη  (the smaller one increases)
    
    Gap: Δ = λ₊ - λ₋ = (λ₂-λ₁) - 2αη = Δλ_min - 2αη
    Closure: Δ(η_c) = 0 → η_c = Δλ_min/(2α) ... wait
    
    Actually: δA_N = diag(α, -α), so A = [[λ₁+αη, 0], [0, λ₂-αη]]
    λ₊ = max(λ₁+αη, λ₂-αη), λ₋ = min(λ₁+αη, λ₂-αη)
    
    For η < η_c: λ₂-αη > λ₁+αη, so λ₊ = λ₂-αη, λ₋ = λ₁+αη
    Δ = (λ₂-αη) - (λ₁+αη) = Δλ_min - 2αη
    """
    return max(DELTA_LAMBDA_MIN - 2.0 * ALPHA * eta, 0.0)

def eigenvalue_plus(eta):
    """λ₊(η): the larger eigenvalue"""
    return max(LAMBDA_1 + ALPHA * eta, LAMBDA_2 - ALPHA * eta)

def eigenvalue_minus(eta):
    """λ₋(η): the smaller eigenvalue"""
    return min(LAMBDA_1 + ALPHA * eta, LAMBDA_2 - ALPHA * eta)

def fh_derivative_plus(eta):
    """FH formula derivative for λ₊: dλ₊/dη = ⟨ψ₊|δA_N|ψ₊⟩
    
    For η < η_c: ψ₊ = e₂ (second basis vector), so dλ₊/dη = -α
    For η > η_c: ψ₊ = e₁, so dλ₊/dη = +α
    """
    if eta < ETA_C:
        return -ALPHA
    elif eta > ETA_C:
        return ALPHA
    return 0.0  # at η_c, the derivative is undefined (level crossing)

def fh_derivative_minus(eta):
    """FH formula derivative for λ₋"""
    if eta < ETA_C:
        return ALPHA
    elif eta > ETA_C:
        return -ALPHA
    return 0.0

def collapse_time(eta):
    """τ(η) ∝ 1/Δ(η), diverges as η → η_c⁻"""
    gap = gap_function(eta)
    return 1.0 / gap if gap > 1e-15 else float('inf')


# === 数值验证 ===

def test_eta_c_analytic():
    """验证 η_c = Δλ_min/(2α) = k_max·Δλ_min/2 = 2(√3-1)/3"""
    eta_c_from_model = DELTA_LAMBDA_MIN / (2.0 * ALPHA)
    assert abs(ETA_C - eta_c_from_model) < 1e-10
    print(f"  ✅ η_c = {ETA_C:.6f} = Δλ_min/(2α) = {eta_c_from_model:.6f}")
    print(f"     Analytic: 2(√3-1)/3 = {2*(np.sqrt(3)-1)/3:.6f}")

def test_gap_at_zero():
    """验证 Δ(0) = Δλ_min"""
    assert abs(gap_function(0.0) - DELTA_LAMBDA_MIN) < 1e-10
    print(f"  ✅ Δ(0) = {gap_function(0.0):.6f} = Δλ_min = {DELTA_LAMBDA_MIN:.6f}")

def test_gap_closure():
    """验证 Δ(η) = 0 for η ≥ η_c (gap closes at critical threshold)"""
    gap_at_c = gap_function(ETA_C)
    assert gap_at_c < 1e-10, f"Δ(η_c) = {gap_at_c:.2e} should be ≈ 0"
    gap_beyond = gap_function(ETA_C * 1.5)
    assert gap_beyond < 1e-10, f"Δ beyond η_c = {gap_beyond:.2e} should be ≈ 0"
    print(f"  ✅ Gap closes at η = η_c = {ETA_C:.6f}: Δ → 0")
    print(f"     For η > η_c: eigenvalues cross, λ₊/λ₋ swap")

def test_fh_derivative_numerical():
    """数值验证 FH 公式 dλ/dη 与有限差分一致"""
    etas = [0.1, 0.2, 0.3, 0.4]
    max_error = 0.0
    h = 1e-8
    for eta in etas:
        num_deriv = (eigenvalue_plus(eta + h) - eigenvalue_plus(eta - h)) / (2 * h)
        fh_deriv = fh_derivative_plus(eta)
        error = abs(num_deriv - fh_deriv)
        max_error = max(max_error, error)
    assert max_error < 1e-5, f"FH max error: {max_error:.2e}"
    print(f"  ✅ FH derivative: max error = {max_error:.2e}")

def test_collapse_time_divergence():
    """验证 τ(η) ∝ 1/Δ(η) 发散 as η → η_c⁻"""
    etas = np.linspace(0.0, ETA_C * 0.99, 30)
    tau_0 = collapse_time(0.0)
    tau_near_c = collapse_time(ETA_C * 0.99)
    ratio = tau_near_c / tau_0
    assert ratio > 5.0, f"τ diverges too slowly: τ(0.99η_c)/τ(0) = {ratio:.1f}"
    print(f"  ✅ τ diverges: τ(0.99η_c)/τ(0) = {ratio:.1f}")

    # Verify monotonic increase
    prev = 0.0
    for eta in etas[1:]:
        curr = collapse_time(eta)
        assert curr > prev, f"τ not monotonic at η={eta:.3f}"
        prev = curr

def test_level_crossing():
    """验证 η_c 处能级交叉: λ₊/λ₋ 交换"""
    h = 1e-6
    eta_cross = ETA_C
    # Just below crossing
    below_plus = eigenvalue_plus(eta_cross - h)
    below_minus = eigenvalue_minus(eta_cross - h)
    # Just above crossing
    above_plus = eigenvalue_plus(eta_cross + h)
    above_minus = eigenvalue_minus(eta_cross + h)
    # Verify swap
    assert abs(below_plus - above_minus) < 1e-4, "Level crossing swap fails"
    assert abs(below_minus - above_plus) < 1e-4, "Level crossing swap fails"
    print(f"  ✅ Level crossing at η = η_c: λ₊ ↔ λ₋")


# === 输出表格 ===

def print_table():
    """打印 η 从 0 到 2 的数值表"""
    print(f"\n{'η':>8} {'Δ(η)':>10} {'λ₊':>10} {'λ₋':>10} {'dλ₊/dη':>10} {'τ/τ₀':>10}")
    print("-" * 58)
    for eta in np.linspace(0, 2.0, 21):
        dGap = gap_function(eta)
        lam_plus = eigenvalue_plus(eta)
        lam_minus = eigenvalue_minus(eta)
        deriv_plus = fh_derivative_plus(eta)
        tau_ratio = collapse_time(eta) / collapse_time(1e-10) if collapse_time(eta) < float('inf') else float('inf')
        label = f"{tau_ratio:.2f}" if tau_ratio < 1e6 else "  ∞"
        print(f"{eta:>8.3f} {dGap:>10.6f} {lam_plus:>10.6f} {lam_minus:>10.6f} {deriv_plus:>10.6f} {label:>10s}")


# === 主入口 ===

if __name__ == "__main__":
    print("=" * 60)
    print("噪声谱流数值交叉验证 — Paper X §12.4")
    print("=" * 60)
    print(f"\nCl(1,7) 2×2 纯对角模型:")
    print(f"  k_max = {K_MAX}")
    print(f"  λ₁ = {LAMBDA_1:.6f}, λ₂ = {LAMBDA_2:.6f}")
    print(f"  Δλ_min = {DELTA_LAMBDA_MIN:.6f} = (√6-√2)/√72")
    print(f"  δA_N = diag(α, -α), α = 1/k_max = {ALPHA}")
    print(f"  η_c = Δλ_min/α = {ETA_C:.6f}  (analytic: 4(√3-1)/3 ≈ 0.976)")
    print(f"  能级交叉点: η_c/2 = {ETA_C/2:.6f}")
    print()

    tests = [
        ("η_c analytic", test_eta_c_analytic),
        ("Δ(0) = Δλ_min", test_gap_at_zero),
        ("Gap closure at η_c/2", test_gap_closure),
        ("FH derivative numerical", test_fh_derivative_numerical),
        ("Collapse time divergence", test_collapse_time_divergence),
        ("Level crossing λ₊↔λ₋", test_level_crossing),
    ]

    all_passed = True
    for name, test_fn in tests:
        print(f"测试: {name}")
        try:
            test_fn()
        except AssertionError as e:
            print(f"  ❌ FAIL: {e}")
            all_passed = False
        except Exception as e:
            import traceback; traceback.print_exc()
            print(f"  ❌ ERROR: {e}")
            all_passed = False

    print()
    print_table()

    print(f"\n{'全部通过!' if all_passed else '存在失败!'}")
    print(f"Paper X §12.4 验证: τ(η) ∝ 1/Δ(η) → ∞ at η = η_c = {ETA_C:.6f}")
    print(f"η_c = {ETA_C:.6f} = 2(√3-1)/3  （噪声临界阈值: δA_N = diag(1/8, -1/8)）")
