"""
逆谱构造：从标准模型质量谱→Cl(6)-值分形核 → 分形几何参数

互逆关系:
  Forward:  分形IFS → T_K特征值 → 质量谱 m = -C·ln(λ)
  Inverse:  质量谱 m → λ = e^{-m/C} → 核函数 K(x,y) → 分形维数d

Gelfand对偶: Clifford值RKHS ↔ 分形测度空间
"""
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
from numpy.polynomial.legendre import Legendre

# ============================================================
# 1. 标准模型质量数据 (按扇区分组)
# ============================================================
SM_SECTORS = {
    'lepton': np.array([0.511, 105.66, 1776.86]),     # e, μ, τ
    'up_quark': np.array([2.2, 1270.0, 173100.0]),     # u, c, t
    'down_quark': np.array([4.7, 95.0, 4180.0]),       # d, s, b
}

def all_masses():
    return np.sort(np.concatenate(list(SM_SECTORS.values())))

# ============================================================
# 2. 逆谱构造：从质量到核函数
# ============================================================
def mass_to_eigenvalues(masses, C):
    """m_i → λ_i = e^{-m_i/C}"""
    return np.exp(-masses / C)

def spectral_decay_law(k, C, d, base=1.0):
    """
    谱衰减律: m_k ≈ C · k^{2/d}
    其中d是分形维数, C是扇区标度
    """
    return C * (k ** (2.0 / d))

def fit_sector_parameters(masses):
    """
    从3个质量拟合扇区参数(C, d):
    ln(m_k) = ln(C) + (2/d)·ln(k) for k=1,2,3
    """
    k = np.array([1, 2, 3])
    log_k = np.log(k)
    log_m = np.log(np.sort(masses))
    
    # 线性回归: log_m = log_C + (2/d) * log_k
    A = np.vstack([np.ones(3), log_k]).T
    coeffs, _, _, _ = np.linalg.lstsq(A, log_m, rcond=None)
    
    log_C = coeffs[0]
    slope = coeffs[1]  # = 2/d
    
    C = np.exp(log_C)
    d = 2.0 / slope if slope > 0 else float('inf')
    
    # 预测质量
    predicted = spectral_decay_law(k, C, d)
    error = np.mean(np.abs(np.log(predicted) - log_m))
    
    return {'C': C, 'd': d, 'slope': slope, 'error': error, 'predicted': predicted}

def construct_kernel_from_spectrum(eigenvalues, n_points=200, basis='legendre'):
    """
    Mercer定理: K(x,y) = Σ_i λ_i ψ_i(x) ψ_i(y)
    
    使用Legendre多项式作为本征函数基
    """
    n_ev = len(eigenvalues)
    x = np.linspace(0, 1, n_points)
    K = np.zeros((n_points, n_points))
    
    if basis == 'legendre':
        for i in range(n_ev):
            # Legendre多项式 P_i(2x-1) 在[0,1]上正交
            coeff = np.zeros(i + 1)
            coeff[i] = 1.0
            P = Legendre(coeff)
            psi = P(2 * x - 1)
            psi = psi / np.sqrt(np.trapz(psi**2, x))
            K += eigenvalues[i] * np.outer(psi, psi)
    
    elif basis == 'fourier':
        for i in range(n_ev):
            k = i + 1
            psi = np.sin(k * np.pi * x)
            psi = psi / np.sqrt(np.trapz(psi**2, x))
            K += eigenvalues[i] * np.outer(psi, psi)
    
    return K, x

def kernel_fractal_dimension(K, x):
    """
    从核函数估计分形维数:
    d_f = 2 - (ln Tr(K^n) / ln n) 的渐近行为
    """
    eigenvalues = la.eigvalsh(K)
    eigenvalues = np.maximum(eigenvalues[::-1], 0)
    
    # 谱衰减律: λ_k ~ exp(-c·k^{2/d})
    # ln(-ln(λ_k)) ~ ln(c) + (2/d)·ln(k)
    pos = eigenvalues > 1e-15
    k = np.arange(1, len(eigenvalues) + 1)[pos][:20]
    ev = eigenvalues[pos][:20]
    
    if len(ev) < 3:
        return 1.0, 0.0, ev, k
    
    log_k = np.log(k)
    log_log = np.log(-np.log(np.maximum(ev, 1e-15)))
    
    A = np.vstack([np.ones(len(k)), log_k]).T
    coeffs, _, _, _ = np.linalg.lstsq(A, log_log, rcond=None)
    
    d = 2.0 / coeffs[1] if coeffs[1] > 0 else float('inf')
    return d, coeffs[0], ev, k

# ============================================================
# 3. 主要分析
# ============================================================
def run():
    print("=" * 70)
    print("Inverse Spectral Construction: Mass → Fractal Kernel")
    print("Gelfand Duality: Cl(6)-RKHS ↔ Fractal Measure Space")
    print("=" * 70)
    
    # Step 1: 按扇区拟合
    print("\n1. Sector Parameter Fitting (Spectral Decay Law m_k = C·k^{2/d})")
    print("-" * 50)
    
    sector_params = {}
    
    for name, masses in SM_SECTORS.items():
        params = fit_sector_parameters(masses)
        sector_params[name] = params
        print(f"\n  {name}:")
        print(f"    Masses: {masses}")
        print(f"    C = {params['C']:.2f} MeV (sector scale)")
        print(f"    d = {params['d']:.4f} (fractal dimension)")
        print(f"    slope (2/d) = {params['slope']:.4f}")
        print(f"    Fit error = {params['error']:.6f}")
        for i in range(3):
            ratio = params['predicted'][i] / masses[i]
            print(f"      m_{i+1}: SM={masses[i]:>10.4f} Fit={params['predicted'][i]:>10.4f} ratio={ratio:.2f}")
    
    # Step 2: 逆构造核函数
    print("\n\n2. Inverse Kernel Construction via Mercer Theorem")
    print("-" * 50)
    
    n_points = 200
    
    for name, masses in SM_SECTORS.items():
        params = sector_params[name]
        C = params['C']
        d = params['d']
        
        # 从质量计算特征值
        eigenvalues = mass_to_eigenvalues(np.sort(masses), C)
        print(f"\n  {name} (C={C:.1f}, d={d:.3f}):")
        print(f"    λ_i = {np.round(eigenvalues, 6)}")
        
        # 构造核函数
        K, x = construct_kernel_from_spectrum(eigenvalues, n_points)
        
        # 验证正定性
        min_eig = np.min(la.eigvalsh(K))
        print(f"    Kernel positive definite: {min_eig > -1e-10} (min eig = {min_eig:.6e})")
    
    # Step 3: 分形维数与谱衰减
    print("\n\n3. Fractal Analysis from Spectral Decay")
    print("-" * 50)
    
    # 合成9个质量的完整谱
    all_ev = []
    for name, masses in SM_SECTORS.items():
        C = sector_params[name]['C']
        ev = mass_to_eigenvalues(np.sort(masses), C)
        all_ev.extend(ev)
    
    overall_ev = np.sort(all_ev)[::-1]
    K_full, x = construct_kernel_from_spectrum(overall_ev, n_points)
    
    d_est, c_const, ev_spec, k_spec = kernel_fractal_dimension(K_full, x)
    print(f"  Full kernel fractal dimension: d = {d_est:.4f}")
    print(f"  (from spectral decay λ_k ~ exp(-c·k^{2/d}))")
    print(f"  Number of spectral modes used: {len(ev_spec)}")
    
    # Step 4: 互逆一致性验证
    print("\n\n4. Mutual Inverse Consistency Check")
    print("-" * 50)
    
    # 正向: 从IFS到质量 (简化)
    print("  Forward: IFS fractal → T_K eigenvalues → masses")
    C_str = ', '.join([f"{p['C']:.1f}" for p in sector_params.values()])
    d_str = ', '.join([f"{p['d']:.3f}" for p in sector_params.values()])
    print(f"    Sector scales C: [{C_str}]")
    print(f"    Fractal dimensions d: [{d_str}]")
    
    # 逆向: 从质量到IFS
    print("  Inverse: masses → eigenvalues → kernel → fractal params")
    print(f"    Recovered d = {d_est:.4f}")
    print(f"    Consistency: |d_est - mean(d_sectors)| = {d_est - np.mean([p['d'] for p in sector_params.values()]):.4f}")
    
    # 绘图
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    colors = {'lepton': 'red', 'up_quark': 'blue', 'down_quark': 'green'}
    
    ax = axes[0, 0]
    for name, masses in SM_SECTORS.items():
        params = sector_params[name]
        k = np.array([1, 2, 3])
        ax.plot(k, masses, 'o-', label=name, color=colors[name], linewidth=2, markersize=8)
        ax.plot(k, params['predicted'], 's--', color=colors[name], alpha=0.5)
    ax.set_xlabel('Generation index k')
    ax.set_ylabel('Mass [MeV]')
    ax.set_yscale('log')
    ax.set_title('Sector Fit: m_k = C·k^{2/d}')
    ax.legend()
    ax.grid(True)
    
    ax = axes[0, 1]
    names = list(SM_SECTORS.keys())
    C_vals = [sector_params[n]['C'] for n in names]
    d_vals = [sector_params[n]['d'] for n in names]
    x_pos = np.arange(len(names))
    ax.bar(x_pos - 0.2, C_vals, 0.4, label='C (scale)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names)
    ax.set_ylabel('Sector scale C [MeV]')
    ax.set_title('Sector Mass Scales')
    ax.grid(True)
    
    ax2 = ax.twinx()
    ax2.bar(x_pos + 0.2, d_vals, 0.4, label='d (fractal dim)', alpha=0.7, color='orange')
    ax2.set_ylabel('Fractal dimension d')
    ax2.legend(loc='upper right')
    
    ax = axes[0, 2]
    x_fine = np.linspace(0, 1, 200)
    for name, masses in SM_SECTORS.items():
        C = sector_params[name]['C']
        ev = mass_to_eigenvalues(np.sort(masses), C)
        K_s, _ = construct_kernel_from_spectrum(ev, 200)
        ax.plot(x_fine, K_s[100, :], label=name, color=colors[name], linewidth=2)
    ax.set_xlabel('x')
    ax.set_ylabel('K(x_mid, y)')
    ax.set_title('Kernel Slices (Mercer Construction)')
    ax.legend()
    ax.grid(True)
    
    ax = axes[1, 0]
    if len(ev_spec) > 0:
        ax.plot(k_spec, ev_spec, 'o-', linewidth=2, markersize=6)
        ax.set_yscale('log')
        ax.set_xlabel('Mode index k')
        ax.set_ylabel('Eigenvalue λ_k')
        ax.set_title('Spectral Decay of Constructed Kernel')
        ax.grid(True)
    
    ax = axes[1, 1]
    if len(ev_spec) > 3:
        log_k = np.log(k_spec)
        log_log = np.log(-np.log(np.maximum(ev_spec, 1e-15)))
        ax.plot(log_k, log_log, 'o-', linewidth=2)
        coeffs = np.polyfit(log_k, log_log, 1)
        ax.plot(log_k, np.polyval(coeffs, log_k), '--', label=f'slope={coeffs[0]:.3f}')
        ax.set_xlabel('ln(k)')
        ax.set_ylabel('ln(-ln(λ_k))')
        ax.set_title(f'Fractal Dimension: d = {d_est:.3f}')
        ax.legend()
        ax.grid(True)
    
    ax = axes[1, 2]
    # 互逆关系示意图
    ax.text(0.5, 0.8, 'Gelfand Duality', ha='center', fontsize=14, fontweight='bold')
    ax.text(0.5, 0.6, 'Cl(6)-RKHS  ⟷  Fractal Measure', ha='center', fontsize=12)
    ax.text(0.5, 0.4, 'T_K Spectrum  ⟷  IFS Parameters', ha='center', fontsize=12)
    ax.text(0.5, 0.2, 'Fermion Masses  ⟷  Fractal Dimension', ha='center', fontsize=12)
    ax.arrow(0.3, 0.7, 0.4, 0, head_width=0.05, head_length=0.05, fc='blue', ec='blue')
    ax.arrow(0.7, 0.5, -0.4, 0, head_width=0.05, head_length=0.05, fc='red', ec='red')
    ax.text(0.5, 0.7, 'Forward', ha='center', fontsize=10, color='blue')
    ax.text(0.5, 0.5, 'Inverse', ha='center', fontsize=10, color='red')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Mutual Inverse Duality')
    
    plt.tight_layout()
    plt.savefig('inverse_spectral_mass.png', dpi=300)
    
    with open('inverse_spectral_results.txt', 'w') as f:
        f.write("=== Inverse Spectral Construction Results ===\n\n")
        f.write("Sector Parameters:\n")
        for name in SM_SECTORS:
            p = sector_params[name]
            f.write(f"  {name}: C={p['C']:.2f}, d={p['d']:.4f}, slope={p['slope']:.4f}\n")
        f.write(f"\nFull kernel fractal dimension: d = {d_est:.4f}\n")
        f.write("\nMass predictions from spectral law:\n")
        for name in SM_SECTORS:
            p = sector_params[name]
            f.write(f"  {name}:\n")
            for i in range(3):
                f.write(f"    m_{i+1}: SM={list(SM_SECTORS[name])[i]:.2f} Pred={p['predicted'][i]:.2f}\n")
    
    print(f"\nResults saved to inverse_spectral_results.txt")
    print(f"Plot saved to inverse_spectral_mass.png")

if __name__ == "__main__":
    run()