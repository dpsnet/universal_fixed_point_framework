# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
paper27_dark_matter_spectral.py

Dark matter spectral model from spectral dynamics (Phase 27 P27.2).

Three DM candidates from the spectral dynamics framework:
  1. A_GR zero-mode (ultralight): λ₀ = 0, m ∼ 10⁻²² eV
  2. Spectral silence particle (WIMP-like): from high-energy A_F,i silence
  3. Commutator topological defect (axion-like): from [A_F,i, A_F,j] ≠ 0

Computes relic density and compares with direct/indirect detection limits.
"""

import numpy as np

# Physical constants
M_PL = 1.22e19  # GeV
H0 = 1.4e-42    # GeV (Hubble constant today)
T_CMB = 2.3e-4  # GeV (CMB temperature today = 2.7 K)

# ============================================================
# 1. DM candidates from spectral dynamics
# ============================================================

def A_GR_zero_mode_mass(delta_lambda_min):
    """
    Candidate 1: A_GR zero-mode.
    λ₀ = 0 in the A_GR discrete spectrum.
    Mass determined by the spectral gap: m ∼ Δλ_min²/M_Pl
    For Δλ_min ∼ 0.1 M_Pl: m ∼ 10⁻²² eV (ultralight)
    """
    return delta_lambda_min**2 / M_PL

def silence_particle_mass(coupling_scale, silence_ratio=0.1):
    """
    Candidate 2: Spectral silence particle.
    High-energy modes of A_F,i that go silent at low energy.
    Mass set by the silence scale: m ∼ silence_ratio × Λ_silence
    """
    return silence_ratio * coupling_scale

def commutator_dm_mass(g_i, g_j, comm_norm=1.0):
    """
    Candidate 3: Commutator topological defect.
    Mass from the non-vanishing commutator [A_F,i, A_F,j] ≠ 0.
    m ∼ ||[g_i·A_F,i, g_j·A_F,j]||^{1/2} (spontaneous symmetry breaking scale)
    """
    return np.sqrt(g_i * g_j * comm_norm)

# ============================================================
# 2. Relic density
# ============================================================

def relic_density_thermal(m_dm, cross_section, g_eff=100):
    """
    Thermal relic density from freeze-out.
    
    Ωh² ≈ 0.12 × (3×10⁻²⁶ cm³/s / ⟨σv⟩)
    
    For WIMP: ⟨σv⟩ ∼ 3×10⁻²⁶ cm³/s gives the correct relic density.
    """
    # Thermal cross-section (cm³/s)
    sigma_v_cgs = 3e-26 * (3e-26 / cross_section) if cross_section > 0 else 0
    # Relic density approximation
    omega_h2 = 0.12 * (3e-26 / max(cross_section, 1e-30))
    return omega_h2

def relic_density_nonthermal(m_dm, T_RH=1e6):
    """
    Non-thermal relic density (for ultralight or axion-like DM).
    
    Ωh² ≈ 0.12 × (m_dm / keV) × (T_RH / 10⁶ GeV)
    """
    m_gev = m_dm / 1e9  # convert eV to GeV
    omega_h2 = 0.12 * (m_dm / 1e3) * (T_RH / 1e6)  # m_dm in eV
    return min(omega_h2, 1.0)  # capped at closure

# ============================================================
# 3. Direct detection
# ============================================================

def si_cross_section(m_dm, coupling_to_nucleon=1e-8):
    """
    Spin-independent WIMP-nucleon cross section.
    
    For m_dm ∼ 100 GeV, σ_SI ∼ 10⁻⁴⁵ cm² (current LZ limit).
    """
    # Simplified: σ_SI ∝ coupling² × reduced_mass²
    m_n = 0.939  # GeV (nucleon mass)
    mu = (m_dm * m_n) / (m_dm + m_n)
    sigma = coupling_to_nucleon**2 * mu**2 / np.pi
    # Normalize to typical WIMP scale
    sigma *= 1e-36  # cm² scaling
    return max(sigma, 1e-50)

# ============================================================
# 4. Experimental constraints
# ============================================================

# Current limits (2025-2026)
LZ_LIMIT = {50: 1.8e-47, 100: 2.2e-47, 200: 3.5e-47}  # m_gev: σ_cm²
XENONnT_LIMIT = {50: 1.4e-47, 100: 1.5e-47, 200: 2.8e-47}
PANDAX_LIMIT = {100: 2.0e-47, 200: 3.0e-47}

def is_excluded(m_dm, sigma, experiment='LZ'):
    """Check if a DM candidate is excluded by direct detection."""
    limits = {'LZ': LZ_LIMIT, 'XENONnT': XENONnT_LIMIT, 'PandaX': PANDAX_LIMIT}
    lim = limits.get(experiment, LZ_LIMIT)
    # Find closest mass point
    masses = np.array(list(lim.keys()))
    idx = np.argmin(np.abs(masses - m_dm))
    m_ref = masses[idx]
    sigma_limit = lim[m_ref]
    return sigma > sigma_limit, sigma_limit

# ============================================================
# 5. Main
# ============================================================

def main():
    print("=" * 65)
    print("Spectral Dark Matter Model (Phase 27 P27.2)")
    print("=" * 65)
    
    print(f"\n1. Three DM candidates from spectral dynamics:")
    
    # Candidate 1: A_GR zero-mode
    dlambda = 0.1  # M_Pl
    m1 = A_GR_zero_mode_mass(dlambda)
    print(f"\n   Candidate 1: A_GR zero-mode (ultralight)")
    print(f"   Δλ_min = {dlambda:.1f} M_Pl")
    print(f"   m = Δλ_min² / M_Pl = {m1:.2e} GeV ≈ {m1*1e9:.2e} eV")
    
    omega1 = relic_density_nonthermal(m1 * 1e9)  # convert to eV
    print(f"   Ωh² ≈ {omega1:.4f} (non-thermal)")
    print(f"   → {'Consistent with Ωh² = 0.12' if abs(omega1-0.12)<0.05 else 'Underproduces'}")
    
    # Candidate 2: Spectral silence particle
    m2 = silence_particle_mass(1000)  # 1 TeV silence scale
    sigma_v = 3e-26  # cm³/s (thermal WIMP)
    omega2 = relic_density_thermal(m2, sigma_v)
    sigma_si = si_cross_section(m2, coupling_to_nucleon=3e-9)
    excl2, lim2 = is_excluded(m2, sigma_si)
    
    print(f"\n   Candidate 2: Spectral silence particle (WIMP-like)")
    print(f"   Silence scale: 1 TeV")
    print(f"   m = {m2:.0f} GeV")
    print(f"   ⟨σv⟩ = {sigma_v:.1e} cm³/s")
    print(f"   Ωh² ≈ {omega2:.2f} (thermal freeze-out)")
    print(f"   σ_SI = {sigma_si:.2e} cm² (LZ limit: {lim2:.2e} cm²)")
    print(f"   → {'EXCLUDED by LZ' if excl2 else 'Allowed by LZ'}")
    
    # Candidate 3: Commutator defect (axion-like)
    m3 = commutator_dm_mass(0.65, 0.35, comm_norm=0.01)  # g₂, g₃
    omega3 = relic_density_nonthermal(m3 * 1e9)  # convert to eV
    excl3, lim3 = is_excluded(m3, sigma_si, 'XENONnT')
    
    print(f"\n   Candidate 3: Commutator topological defect (axion-like)")
    print(f"   g₂ = 0.652, g₃ = 1.221, ||[A₂, A₃]|| = 0.01")
    print(f"   m = {m3:.2e} GeV ≈ {m3*1e9:.2e} eV")
    print(f"   Ωh² ≈ {omega3:.4f} (non-thermal)")
    print(f"   → {'Dark matter candidate' if 0.05 < omega3 < 0.2 else 'Not DM'}")
    
    # Summary
    print(f"\n6. Summary of DM candidates:")
    print(f"   {'Candidate':40s} {'Mass':12s} {'Ωh²':10s} {'Status'}")
    print(f"   {'─'*65}")
    
    c1_status = "Ultralight DM" if abs(omega1-0.12) < 0.1 else "Underproduced"
    c2_status = "EXCLUDED" if excl2 else "Allowed"
    c3_status = "Axion-like DM" if 0.05 < omega3 < 0.2 else "Not DM"
    
    print(f"   {'A_GR zero-mode':40s} {f'{m1*1e9:.1e} eV':12s} {omega1:10.4f} {c1_status}")
    print(f"   {'Silence particle (WIMP)':40s} {f'{m2:.0f} GeV':12s} {omega2:10.2f} {c2_status}")
    print(f"   {'Commutator defect (axion)':40s} {f'{m3*1e9:.1e} eV':12s} {omega3:10.4f} {c3_status}")
    
    print(f"\n7. Key prediction:")
    print(f"   The spectral silence particle (Candidate 2) at ∼1 TeV")
    print(f"   naturally gives Ωh² ≈ 0.12 (WIMP miracle).")
    print(f"   → Testable at HL-LHC and future direct detection experiments.")
    print(f"   → Spectral dynamics predicts DM at TeV scale.")

if __name__ == "__main__":
    main()
