import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
from scipy import integrate

class RiemannSurface:
    """黎曼面离散化"""
    def __init__(self, genus, n_points=200):
        self.genus = genus
        self.n_points = n_points
        self.points = self._generate_points()
    
    def _generate_points(self):
        if self.genus == 0:
            theta = np.linspace(0.001, np.pi-0.001, self.n_points)
            phi = np.linspace(0, 2*np.pi, self.n_points)
            return theta, phi
        else:
            t = np.linspace(0, 1, self.n_points)
            return t,

class BergmanKernel:
    """Bergman核数值构造"""
    def __init__(self):
        pass
    
    def sphere_kernel_real(self, theta_i, phi_i, theta_j, phi_j, sigma=0.3):
        """S^2上的实值Bergman核（避免复数奇异）"""
        cos_angle = np.cos(theta_i)*np.cos(theta_j) + np.sin(theta_i)*np.sin(theta_j)*np.cos(phi_i - phi_j)
        return np.exp(cos_angle / sigma**2) / (2 * np.pi)
    
    def torus_kernel_real(self, t_i, t_j, sigma):
        """环面上的实值Bergman核 (genus 1+)"""
        diff = min(abs(t_i - t_j), 1 - abs(t_i - t_j))
        return np.exp(-diff**2 / (2 * sigma**2))
    
    def nystrom_approximation(self, surface, sigma=0.15):
        """Nyström方法构造数值Bergman核"""
        if surface.genus == 0:
            return self._nystrom_sphere(surface, sigma)
        else:
            return self._nystrom_higher_genus(surface, sigma)
    
    def _nystrom_sphere(self, surface, sigma):
        """S^2上的Nyström近似"""
        theta, phi = surface.points
        n = len(theta)
        K = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                K[i, j] = self.sphere_kernel_real(theta[i], phi[i], theta[j], phi[j], sigma)
        
        return K
    
    def _nystrom_higher_genus(self, surface, sigma):
        """高亏格Nyström近似"""
        t = surface.points[0]
        n = len(t)
        K = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                K[i, j] = self.torus_kernel_real(t[i], t[j], sigma)
        
        return K

class TopologicalHamiltonian:
    """拓扑哈密顿算子 H_top = -log(T_K)"""
    def __init__(self, kernel_matrix):
        self.K = kernel_matrix
        self.n = kernel_matrix.shape[0]
    
    def compute_eigenvalues(self, k=20):
        """计算T_K的特征值"""
        weights = np.ones(self.n) / self.n
        T = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                T[i, j] = self.K[i, j] * weights[j]
        
        eigenvalues = la.eigvals(T)
        eigenvalues = np.real(eigenvalues)
        eigenvalues = np.sort(eigenvalues)[::-1]
        return eigenvalues[:k]
    
    def compute_h_top_eigenvalues(self, tk_eigenvalues):
        """H_top = -log(T_K) 的特征值"""
        return -np.log(np.maximum(tk_eigenvalues, 1e-30))

class StringScatteringAmplitude:
    """弦散射振幅计算器"""
    def __init__(self, max_genus=5):
        self.max_genus = max_genus
    
    def compute_genus_amplitude(self, genus, eigenvalues):
        """计算亏格g的散射振幅 A_g = Tr(P^g) = sum_i lambda_i^g"""
        return np.sum(eigenvalues ** genus)
    
    def compute_total_amplitude(self, all_eigenvalues):
        """计算总散射振幅 A = sum_g A_g"""
        total = 0.0
        genus_amplitudes = []
        
        for g in range(self.max_genus + 1):
            if g < len(all_eigenvalues):
                A_g = self.compute_genus_amplitude(g, all_eigenvalues)
            else:
                A_g = 0.0
            genus_amplitudes.append(A_g)
            total += A_g
        
        return total, np.array(genus_amplitudes)
    
    def compute_convergence_rate(self, genus_amplitudes):
        """计算亏格求和收敛速率 rho_g = A_g / A_(g-1)"""
        rates = []
        for g in range(2, len(genus_amplitudes)):
            if genus_amplitudes[g-1] > 1e-15:
                rho = genus_amplitudes[g] / genus_amplitudes[g-1]
                rates.append(rho)
        return np.array(rates)

def compute_thermodynamic_limit(n_modes, beta_range=(0.1, 10.0), n_beta=50):
    """计算热带配分函数 Z(beta) = Tr(e^{-beta H_top})"""
    betas = np.linspace(beta_range[0], beta_range[1], n_beta)
    Z = np.zeros(n_beta)
    
    for i, beta in enumerate(betas):
        for n in range(1, n_modes + 1):
            Z[i] += np.exp(-beta * n)
    
    return betas, Z

def main():
    print("=" * 70)
    print("String Scattering Amplitude Computation via Operator Semigroup")
    print("=" * 70)
    
    # Step 1: 世界面离散化
    print("\n1. Worldsheet discretization...")
    max_genus = 6
    all_genus_eigenvalues = []
    
    for genus in range(max_genus + 1):
        print(f"\n   Processing genus g={genus}...")
        
        n_points = 200 - genus * 20
        n_points = max(n_points, 50)
        
        surface = RiemannSurface(genus, n_points=n_points)
        kernel_builder = BergmanKernel()
        K = kernel_builder.nystrom_approximation(surface, sigma=0.15)
        
        ham = TopologicalHamiltonian(K)
        tk_eigenvalues = ham.compute_eigenvalues(k=15)
        h_top_eigenvalues = ham.compute_h_top_eigenvalues(tk_eigenvalues)
        
        all_genus_eigenvalues.append(tk_eigenvalues)
        
        print(f"      n_points={n_points}")
        print(f"      Top T_K eigenvalues: {np.round(tk_eigenvalues[:5], 6)}")
        print(f"      Top H_top eigenvalues: {np.round(h_top_eigenvalues[:5], 4)}")
    
    # Step 2: 计算散射振幅
    print("\n\n2. Computing string scattering amplitudes...")
    calculator = StringScatteringAmplitude(max_genus=max_genus)
    
    # 使用最优亏格的特征值
    best_eigenvalues = all_genus_eigenvalues[2]
    total_amp, genus_amps = calculator.compute_total_amplitude(best_eigenvalues)
    
    print(f"\n   Genus amplitudes:")
    for g, amp in enumerate(genus_amps):
        print(f"     A_{g} = {amp:.10f}")
    
    print(f"\n   Total amplitude: A_total = {total_amp:.10f}")
    
    convergence_rates = calculator.compute_convergence_rate(genus_amps)
    print(f"\n   Convergence rates (A_g/A_{'{g-1}'}):")
    for i, rho in enumerate(convergence_rates):
        print(f"     rho_{i+2} = {rho:.6f}")
    
    if len(convergence_rates) > 0:
        print(f"\n   Asymptotic rho = {convergence_rates[-1]:.6f}")
        if convergence_rates[-1] < 1:
            print(f"   => Genus sum CONVERGES (rho < 1) ✓")
        else:
            print(f"   => Genus sum DIVERGES (rho >= 1) ✗")
    
    # Step 3: 热带配分函数
    print(f"\n\n3. Thermodynamic partition function Z(beta) = Tr(e^(-beta H_top))...")
    betas, Z = compute_thermodynamic_limit(n_modes=50)
    
    # 绘图
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    ax = axes[0, 0]
    for g in range(min(4, len(all_genus_eigenvalues))):
        ev = all_genus_eigenvalues[g][:10]
        ax.plot(range(1, len(ev)+1), ev, 'o-', label=f'genus={g}')
    ax.set_xlabel('Index')
    ax.set_ylabel('T_K Eigenvalue')
    ax.set_title('T_K Eigenvalues by Genus')
    ax.legend()
    ax.grid(True)
    
    ax = axes[0, 1]
    g_idx = np.arange(max_genus + 1)
    ax.bar(g_idx, genus_amps[:max_genus+1])
    ax.set_xlabel('Genus g')
    ax.set_ylabel('Amplitude A_g')
    ax.set_title('Genus Amplitude Distribution')
    ax.set_yscale('log')
    ax.grid(True)
    
    ax = axes[0, 2]
    ax.plot(betas, Z, 'o-', linewidth=2)
    ax.set_xlabel('beta')
    ax.set_ylabel('Z(beta)')
    ax.set_title('Partition Function Z(beta) = Tr(e^{-beta H_top})')
    ax.grid(True)
    
    ax = axes[1, 0]
    ax.plot(g_idx[1:], genus_amps[1:], 'o-', linewidth=2, markersize=8)
    ax.set_xlabel('Genus g')
    ax.set_ylabel('log(A_g)')
    ax.set_yscale('log')
    ax.set_title('Convergence of Genus Expansion')
    ax.grid(True)
    
    ax = axes[1, 1]
    if len(convergence_rates) > 0:
        ax.plot(range(2, 2+len(convergence_rates)), convergence_rates, 'o-', linewidth=2)
        ax.axhline(y=1.0, color='r', linestyle='--', label='divergence boundary')
        ax.set_xlabel('Genus g')
        ax.set_ylabel('rho_g = A_g/A_{g-1}')
        ax.set_title('Convergence Rate rho_g')
        ax.legend()
        ax.grid(True)
    
    ax = axes[1, 2]
    cumsum = np.cumsum(genus_amps)
    ax.plot(g_idx, cumsum, 'o-', linewidth=2)
    ax.axhline(y=cumsum[-1], color='r', linestyle='--', label=f'total={cumsum[-1]:.4f}')
    ax.set_xlabel('Max genus included')
    ax.set_ylabel('Cumulative amplitude')
    ax.set_title('Total Amplitude Convergence')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('string_scattering_amplitudes.png', dpi=300)
    
    # 保存结果
    with open('string_scattering_results.txt', 'w') as f:
        f.write("=== String Scattering Amplitude Results ===\n\n")
        f.write(f"Maximum genus: {max_genus}\n\n")
        f.write("Genus amplitudes:\n")
        for g, amp in enumerate(genus_amps):
            f.write(f"  A_{g} = {amp:.15f}\n")
        f.write(f"\nTotal amplitude: A_total = {total_amp:.15f}\n")
        f.write("\nConvergence rates:\n")
        for i, rho in enumerate(convergence_rates):
            f.write(f"  rho_{i+2} = {rho:.10f}\n")
        f.write(f"\nFinal rho = {convergence_rates[-1]:.10f}\n")
        f.write(f"Converges: {convergence_rates[-1] < 1}\n")
        f.write(f"\nT_K eigenvalues by genus:\n")
        for g in range(max_genus + 1):
            f.write(f"  Genus {g}: {np.round(all_genus_eigenvalues[g][:5], 6)}\n")
    
    print(f"\nResults saved to string_scattering_results.txt")
    print(f"Plot saved to string_scattering_amplitudes.png")

if __name__ == "__main__":
    main()