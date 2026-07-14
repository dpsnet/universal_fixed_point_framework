import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def standard_model_masses():
    return np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))

def pauli_matrices():
    """Pauli矩阵作为Cl(3)的生成元"""
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [sigma1, sigma2, sigma3]

def gamma_matrices_cl6():
    """Cl(6)的6个Gamma矩阵 (8x8)"""
    sigma = pauli_matrices()
    gamma = []
    for k in range(3):
        gamma_k = np.kron(np.kron(sigma[k], np.eye(2)), np.eye(2))
        gamma.append(gamma_k)
    for k in range(3):
        gamma_k = np.kron(np.kron(np.eye(2), sigma[k]), np.eye(2))
        gamma.append(gamma_k)
    return gamma

def chirality_operator(gamma):
    """Cl(6)的手征算子 gamma_7 = (-i)^3 gamma_0*...*gamma_5"""
    n = len(gamma)
    g7 = np.eye(8, dtype=complex)
    for k in range(n):
        g7 = g7 @ gamma[k] * 1j
    return g7

class CliffordValuedKernel:
    """
    Clifford-valued kernel K(x,y) = sum_k exp(-(x-y)^2/(2*sigma_k^2)) * Gamma_k
    每个Gamma_k是Cl(6)的生成元，对应不同费米子扇形
    """
    def __init__(self, n_samples=200):
        self.gamma = gamma_matrices_cl6()
        self.gamma_7 = chirality_operator(self.gamma)
        self.n_samples = n_samples
        self.sample_points = np.linspace(0, 1, n_samples)
        
        # 不同尺度对应不同扇形
        self.sigma_sectors = [0.5, 0.1, 0.05, 0.02, 0.01]
        self.sector_labels = ['light', 'light+', 'medium', 'heavy-', 'heavy']
    
    def gaussian(self, x, y, sigma):
        return np.exp(-(x - y)**2 / (2 * sigma**2))
    
    def construct_cl_kernel_matrix(self, x_idx, y_idx):
        """构造Cl(6)-值核矩阵的 (i,j) 块"""
        x = self.sample_points[x_idx]
        y = self.sample_points[y_idx]
        
        K_block = np.zeros((8, 8), dtype=complex)
        for s_idx, sigma in enumerate(self.sigma_sectors):
            factor = self.sigma_sectors[s_idx]
            K_block += self.gaussian(x, y, sigma) * self.gamma[s_idx % 6]
        
        return K_block
    
    def construct_full_cl_kernel(self):
        """构造完整的Cl(6)-值核矩阵"""
        n = self.n_samples
        K_full = np.zeros((8*n, 8*n), dtype=complex)
        
        for i in range(n):
            K_full[8*i:8*i+8, 8*i:8*i+8] = self.construct_cl_kernel_matrix(i, i)
        
        return K_full
    
    def compute_projectors(self):
        """计算手征投影算子 P_L 和 P_R"""
        P_L = (np.eye(8) - self.gamma_7) / 2
        P_R = (np.eye(8) + self.gamma_7) / 2
        return P_L, P_R
    
    def sector_decomposition(self):
        """Cl(6)代数扇形分解 - 对应三代费米子"""
        P_L, P_R = self.compute_projectors()
        
        # 构建每个扇形的代表性矩阵
        sectors = []
        sector_names = []
        
        # 扇形1: e-μ-τ 带电轻子 (handed + 1st gamma)
        s1 = P_L @ (np.eye(8) + self.gamma[0]) @ P_L
        sectors.append(s1)
        sector_names.append('charged leptons')
        
        # 扇形2: u-c-t 上型夸克 (handed + 2nd gamma)
        s2 = P_L @ (np.eye(8) + self.gamma[1]) @ P_L
        sectors.append(s2)
        sector_names.append('up-type quarks')
        
        # 扇形3: d-s-b 下型夸克 (handed + 3rd gamma)
        s3 = P_L @ (np.eye(8) + self.gamma[2]) @ P_L
        sectors.append(s3)
        sector_names.append('down-type quarks')
        
        return sectors, sector_names
    
    def compute_mass_ratios(self):
        """计算Cl(6)代数结构给出的理论质量比"""
        sectors, names = self.sector_decomposition()
        
        ratios = []
        for s in sectors:
            eigvals = la.eigvalsh(s)
            # 取三个最大的特征值作为三代
            top3 = np.sort(eigvals)[-3:]
            ratio = top3[2] / top3[0] if top3[0] > 0 else 1
            ratios.append(ratio)
        
        return ratios, names

def run_analysis():
    print("=" * 70)
    print("Clifford-valued Kernel Analysis for Standard Model Masses")
    print("=" * 70)
    
    sm_masses = standard_model_masses()
    
    print("\n1. Standard Model fermion masses (MeV):")
    for i, m in enumerate(sm_masses):
        print(f"   {i+1}: {m:.4f}")
    print(f"\n   Log range: {np.log10(sm_masses[0]):.2f} to {np.log10(sm_masses[-1]):.2f}")
    print(f"   This spans {np.log10(sm_masses[-1]) - np.log10(sm_masses[0]):.2f} orders of magnitude")
    
    print("\n2. Constructing Cl(6)-valued kernel...")
    cl_kernel = CliffordValuedKernel(n_samples=200)
    
    print("\n3. Sector analysis from Clifford algebra decomposition...")
    ratios, names = cl_kernel.compute_mass_ratios()
    
    print("\n   Clifford sector mass ratios (top/bottom):")
    total_ratio = 1.0
    for i, (r, name) in enumerate(zip(ratios, names)):
        print(f"   Sector {i+1} ({name}): internal ratio = {r:.4f}")
        total_ratio *= r
    
    # SM三代间质量比
    print(f"\n4. Standard Model inter-generational mass ratios:")
    # 轻子: e=0.511, μ=105.66, τ=1776.86
    lepton_ratios = [1776.86/0.511, 105.66/0.511]
    print(f"   Leptons (τ/μ/e): ratios = {lepton_ratios[0]:.0f}, {lepton_ratios[1]:.0f}")
    # 上型夸克: u=2.2, c=1270, t=173100
    up_ratios = [173100/2.2, 1270/2.2]
    print(f"   Up-type quarks (t/c/u): ratios = {up_ratios[0]:.0f}, {up_ratios[1]:.0f}")
    # 下型夸克: d=4.7, s=95, b=4180
    down_ratios = [4180/4.7, 95/4.7]
    print(f"   Down-type quarks (b/s/d): ratios = {down_ratios[0]:.0f}, {down_ratios[1]:.0f}")
    
    print(f"\n5. Multi-scale sigma analysis:")
    print(f"   To span {np.log10(sm_masses[-1]) - np.log10(sm_masses[0]):.2f} orders of magnitude,")
    print(f"   the kernel requires sigma spanning sqrt(ratio) in scale:")
    print(f"   sigma_min ~ 0.01 for electron mass")
    print(f"   sigma_max ~ 10.0 for top mass")
    
    # 计算多尺度σ的质量覆盖
    print(f"\n6. Mass coverage per sigma scale:")
    sigmas = np.logspace(-2, 1, 10)
    mass_scale = 1000 * np.exp(-1 / (2 * sigmas**2))  # 在距离1处
    for s, m in zip(sigmas, mass_scale):
        print(f"   sigma={s:.4f}: mass scale ~ {m:.0f} MeV")
    
    # 绘图
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    ax = axes[0, 0]
    ax.bar(range(1, 10), np.log10(sm_masses))
    ax.set_xlabel('Particle index')
    ax.set_ylabel('log10(mass) [MeV]')
    ax.set_title('Standard Model Fermion Mass Spectrum')
    ax.grid(True)
    
    ax = axes[0, 1]
    ax.semilogy(sigmas, mass_scale, 'o-', linewidth=2)
    ax.axhline(y=sm_masses[0], color='r', linestyle='--', label=f'electron ({sm_masses[0]:.1f} MeV)')
    ax.axhline(y=sm_masses[-1], color='g', linestyle='--', label=f'top ({sm_masses[-1]:.0f} MeV)')
    ax.set_xlabel('Kernel width sigma')
    ax.set_ylabel('Mass scale [MeV]')
    ax.set_title('Mass Coverage vs Sigma')
    ax.legend()
    ax.grid(True)
    
    ax = axes[1, 0]
    ax.plot(range(1, 10), np.log10(sm_masses), 'o-', linewidth=2, markersize=8, label='SM')
    for i in range(3):
        base = np.log10(sm_masses[i*3]) if i*3 < 9 else 0
        predicted = base + np.array([0, 1.5, 3.0])
        idx = [i*3 + j for j in range(3) if i*3+j < 9]
        if len(idx) > 0:
            ax.plot([x+1 for x in idx], np.log10(sm_masses[np.array(idx)]), 's--', 
                   label=f'Generation {i+1}', markersize=8)
    ax.set_xlabel('Particle index')
    ax.set_ylabel('log10(mass)')
    ax.set_title('Generational Structure')
    ax.legend()
    ax.grid(True)
    
    ax = axes[1, 1]
    # 展示Clifford代数结构
    gen_masses = sm_masses.reshape(3, 3).T
    for g in range(3):
        ax.plot([1, 2, 3], np.log10(gen_masses[g]), 'o-', linewidth=2, markersize=8, 
                label=f'Gen {g+1}: {gen_masses[g,0]:.1f}, {gen_masses[g,1]:.0f}, {gen_masses[g,2]:.0f} MeV')
    ax.set_xlabel('Sector index')
    ax.set_ylabel('log10(mass)')
    ax.set_title('Three Generations × Three Sectors')
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Lepton', 'Up-quark', 'Down-quark'])
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('clifford_valued_kernel_analysis.png', dpi=300)
    
    with open('clifford_kernel_analysis_results.txt', 'w') as f:
        f.write("=== Clifford-valued Kernel Analysis ===\n\n")
        f.write("1. SM Mass Span:\n")
        f.write(f"   Min: {sm_masses[0]:.4f} MeV (electron)\n")
        f.write(f"   Max: {sm_masses[-1]:.0f} MeV (top)\n")
        f.write(f"   Orders of magnitude: {np.log10(sm_masses[-1]) - np.log10(sm_masses[0]):.2f}\n\n")
        f.write("2. Required sigma range for Gaussian kernel:\n")
        for s, m in zip(sigmas, mass_scale):
            f.write(f"   sigma={s:.4f}: mass scale ~ {m:.0f} MeV\n")
        f.write("\n3. Clifford algebra sector ratios:\n")
        for r, name in zip(ratios, names):
            f.write(f"   {name}: ratio = {r:.4f}\n")
        f.write("\n4. Inter-generational ratios:\n")
        f.write(f"   Leptons: {lepton_ratios}\n")
        f.write(f"   Up quarks: {up_ratios}\n")
        f.write(f"   Down quarks: {down_ratios}\n")
    
    print(f"\nAnalysis saved to clifford_kernel_analysis_results.txt")
    print(f"Plot saved to clifford_valued_kernel_analysis.png")

if __name__ == "__main__":
    run_analysis()