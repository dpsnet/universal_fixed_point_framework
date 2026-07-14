import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

class IFSInvariantMeasure:
    def __init__(self, contractions, probabilities, iterations=1000000):
        self.contractions = contractions
        self.probabilities = probabilities
        self.iterations = iterations
        self.points = self.generate_points()
    
    def generate_points(self):
        points = []
        x = 0.5
        for _ in range(self.iterations):
            idx = np.random.choice(len(self.contractions), p=self.probabilities)
            x = self.contractions[idx](x)
            points.append(x)
        return np.array(points)
    
    def get_density(self, bins=100):
        hist, edges = np.histogram(self.points, bins=bins, density=True)
        centers = (edges[:-1] + edges[1:]) / 2
        return centers, hist

class FractalRKHSKernel:
    def __init__(self, measure, sigma=0.1):
        self.measure = measure
        self.sigma = sigma
    
    def gaussian_kernel(self, x, y):
        return np.exp(-(x - y)**2 / (2 * self.sigma**2))
    
    def cl_valued_kernel(self, x, y, gamma_matrices):
        return self.gaussian_kernel(x, y) * gamma_matrices[0]
    
    def construct_kernel_matrix(self, sample_points):
        n = len(sample_points)
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                K[i, j] = self.gaussian_kernel(sample_points[i], sample_points[j])
        return K
    
    def verify_positive_definite(self, K):
        eigenvalues = la.eigvalsh(K)
        min_eig = np.min(eigenvalues)
        is_positive = min_eig > -1e-10
        return is_positive, eigenvalues
    
    def compute_transfer_operator(self, K, sample_points, weights):
        n = len(sample_points)
        T = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                T[i, j] = K[i, j] * weights[j]
        return T
    
    def compute_eigenvalues(self, T, k=10):
        eigenvalues, eigenvectors = la.eig(T)
        eigenvalues = np.real(eigenvalues)
        idx = np.argsort(eigenvalues)[::-1]
        return eigenvalues[idx[:k]], eigenvectors[:, idx[:k]]

def standard_model_masses():
    masses = {
        'up': 2.2,
        'charm': 1270,
        'top': 173100,
        'down': 4.7,
        'strange': 95,
        'bottom': 4180,
        'electron': 0.511,
        'muon': 105.66,
        'tau': 1776.86
    }
    return masses

def main():
    print("=" * 60)
    print("Explicit Kernel Construction and Eigenvalue Calculation")
    print("=" * 60)
    
    contractions = [
        lambda x: 0.5 * x,
        lambda x: 0.5 * x + 0.5
    ]
    probabilities = [0.5, 0.5]
    
    print("\n1. Generating IFS invariant measure...")
    measure = IFSInvariantMeasure(contractions, probabilities, iterations=100000)
    
    centers, density = measure.get_density(bins=50)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.hist(measure.points, bins=50, density=True, alpha=0.7)
    plt.plot(centers, density, 'r-', label='Density')
    plt.xlabel('x')
    plt.ylabel('Density')
    plt.title('IFS Invariant Measure (Cantor set)')
    plt.legend()
    plt.grid(True)
    
    print("\n2. Constructing Gaussian-type kernel...")
    sigma_values = [0.05, 0.1, 0.2]
    all_eigenvalues = []
    
    for sigma in sigma_values:
        kernel = FractalRKHSKernel(measure, sigma=sigma)
        
        n_samples = 200
        sample_points = np.linspace(0, 1, n_samples)
        K = kernel.construct_kernel_matrix(sample_points)
        
        is_positive, eigenvalues = kernel.verify_positive_definite(K)
        
        print(f"   sigma={sigma}: Positive definite = {is_positive}, min eig = {np.min(eigenvalues):.6f}")
        
        all_eigenvalues.append(eigenvalues)
    
    plt.subplot(122)
    for i, sigma in enumerate(sigma_values):
        plt.plot(all_eigenvalues[i][:50], label=f'sigma={sigma}')
    plt.xlabel('Index')
    plt.ylabel('Eigenvalue')
    plt.title('Kernel Matrix Eigenvalues')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('kernel_eigenvalues.png', dpi=300)
    
    print("\n3. Computing transfer operator eigenvalues...")
    kernel = FractalRKHSKernel(measure, sigma=0.1)
    n_samples = 100
    sample_points = np.linspace(0, 1, n_samples)
    K = kernel.construct_kernel_matrix(sample_points)
    
    weights = np.ones(n_samples) / n_samples
    
    T = kernel.compute_transfer_operator(K, sample_points, weights)
    
    T_eigenvalues, _ = kernel.compute_eigenvalues(T, k=20)
    
    print(f"\n   Top 10 T_K eigenvalues:")
    for i, eig in enumerate(T_eigenvalues[:10]):
        print(f"     lambda_{i+1} = {eig:.6f}")
    
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.bar(range(1, len(T_eigenvalues)+1), T_eigenvalues)
    plt.xlabel('Index')
    plt.ylabel('Eigenvalue')
    plt.title('T_K Eigenvalues')
    plt.grid(True)
    
    masses = standard_model_masses()
    mass_values = np.array(sorted(masses.values()))
    
    log_masses = np.log10(mass_values)
    
    plt.subplot(122)
    plt.plot(log_masses, 'o-', label='Standard Model masses')
    plt.xlabel('Particle index')
    plt.ylabel('log10(mass) [MeV]')
    plt.title('Standard Model Mass Spectrum')
    plt.xticks(range(len(masses)), sorted(masses.keys()), rotation=45)
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('mass_spectrum_comparison.png', dpi=300)
    
    print("\n4. Comparing with Standard Model masses...")
    print("\n   Standard Model fermion masses (MeV):")
    for name, mass in sorted(masses.items(), key=lambda x: x[1]):
        print(f"     {name:>8s}: {mass:.2f}")
    
    print("\n   T_K eigenvalue-based mass estimates:")
    for i, eig in enumerate(T_eigenvalues[:9]):
        mass_est = -np.log(eig) * 10000
        print(f"     particle_{i+1}: {mass_est:.2f} MeV (lambda={eig:.6f})")
    
    with open('kernel_eigenvalue_results.txt', 'w') as f:
        f.write("=== Explicit Kernel Construction Results ===\n\n")
        f.write("1. IFS Invariant Measure Parameters:\n")
        f.write(f"   Contractions: {len(contractions)}\n")
        f.write(f"   Probabilities: {probabilities}\n")
        f.write(f"   Iterations: {measure.iterations}\n\n")
        f.write("2. Kernel Matrix Eigenvalues (sigma=0.1):\n")
        for i, eig in enumerate(all_eigenvalues[1][:20]):
            f.write(f"   lambda_{i+1} = {eig:.6f}\n")
        f.write("\n3. Transfer Operator T_K Eigenvalues:\n")
        for i, eig in enumerate(T_eigenvalues[:20]):
            f.write(f"   lambda_{i+1} = {eig:.6f}\n")
        f.write("\n4. Standard Model Masses (MeV):\n")
        for name, mass in sorted(masses.items(), key=lambda x: x[1]):
            f.write(f"   {name:>8s}: {mass:.2f}\n")
    
    print("\nResults saved to kernel_eigenvalue_results.txt")
    print("Plots saved to kernel_eigenvalues.png and mass_spectrum_comparison.png")

if __name__ == "__main__":
    main()