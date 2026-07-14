import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

class KerrGeodesic:
    def __init__(self, M=1.0, a=0.5):
        self.M = M
        self.a = a
        self.G = 1.0
        self.c = 1.0
    
    def schwarzschild_radius(self):
        return 2 * self.G * self.M / self.c**2
    
    def sigma(self, r, theta):
        return r**2 + self.a**2 * np.cos(theta)**2
    
    def delta(self, r):
        return r**2 - 2 * self.M * r + self.a**2
    
    def hamiltonian_system(self, z):
        t, r, theta, phi, pt, pr, ptheta, pphi = z
        
        sig = self.sigma(r, theta)
        deltas = self.delta(r)
        
        A = r**2 + self.a**2 + 2 * self.M * r * self.a**2 * np.sin(theta)**2 / sig
        
        dt_dtau = -(1 - 2 * self.M * r / sig) * pt + (2 * self.M * r / sig) * self.a * np.sin(theta)**2 * pphi
        
        dr_dtau = deltas / sig * pr
        
        dtheta_dtau = ptheta / sig
        
        dphi_dtau = A / (sig * np.sin(theta)**2) * pphi - (2 * self.M * r / sig) * self.a * pt
        
        dpt_dtau = 0.0
        
        dpr_dtau = -(self.M * (r**2 - self.a**2 * np.cos(theta)**2)) / (sig**2 * deltas) * pt**2 + \
                   self.M * (r**2 - self.a**2 * np.cos(theta)**2) / sig**2 * pr**2 + \
                   (r**2 + self.a**2) / sig**2 * ptheta**2 + \
                   (A * (r**2 + self.a**2) - self.a**2 * sig * np.sin(theta)**2) / (sig**2 * np.sin(theta)**2) * pphi**2
        
        dptheta_dtau = (2 * self.M * r * self.a**2 * np.sin(theta) * np.cos(theta)) / sig**3 * pt**2 - \
                       (2 * self.M * r * self.a**2 * np.sin(theta) * np.cos(theta)) / sig**3 * pphi**2 + \
                       (2 * r * np.cos(theta) * np.sin(theta)) / sig**2 * pr**2 - \
                       (2 * r * np.cos(theta) * np.sin(theta)) / sig**2 * ptheta**2 - \
                       (A * np.cos(theta) / np.sin(theta) + self.a**2 * 2 * self.M * r * np.sin(theta) * np.cos(theta) / sig) / (sig * np.sin(theta)**2) * pphi**2
        
        dpphi_dtau = 0.0
        
        return np.array([dt_dtau, dr_dtau, dtheta_dtau, dphi_dtau, dpt_dtau, dpr_dtau, dptheta_dtau, dpphi_dtau])
    
    def rk4_step(self, z, dtau):
        k1 = self.hamiltonian_system(z)
        k2 = self.hamiltonian_system(z + 0.5 * dtau * k1)
        k3 = self.hamiltonian_system(z + 0.5 * dtau * k2)
        k4 = self.hamiltonian_system(z + dtau * k3)
        return z + dtau * (k1 + 2*k2 + 2*k3 + k4) / 6
    
    def jacobian_matrix(self, z):
        t, r, theta, phi, pt, pr, ptheta, pphi = z
        
        sig = self.sigma(r, theta)
        deltas = self.delta(r)
        
        J = np.zeros((8, 8))
        
        d_sig_dr = 2 * r
        d_sig_dtheta = -2 * self.a**2 * np.cos(theta) * np.sin(theta)
        
        d_delta_dr = 2 * r - 2 * self.M
        
        J[0, 1] = (2 * self.M * pt) / sig**2 * (sig - r * d_sig_dr) + \
                  (2 * self.M * self.a * np.sin(theta)**2 * pphi) / sig**2 * (sig - r * d_sig_dr)
        J[0, 2] = (2 * self.M * r * self.a**2 * 2 * np.sin(theta) * np.cos(theta) * pphi) / sig**2
        J[0, 4] = -(1 - 2 * self.M * r / sig)
        J[0, 7] = (2 * self.M * r / sig) * self.a * np.sin(theta)**2
        
        J[1, 1] = (d_delta_dr * sig - deltas * d_sig_dr) / sig**2 * pr
        J[1, 2] = -deltas * d_sig_dtheta / sig**2 * pr
        J[1, 5] = deltas / sig
        
        J[2, 1] = -ptheta * d_sig_dr / sig**2
        J[2, 2] = -ptheta * d_sig_dtheta / sig**2
        J[2, 6] = 1 / sig
        
        A = r**2 + self.a**2 + 2 * self.M * r * self.a**2 * np.sin(theta)**2 / sig
        d_A_dr = 2 * r + 2 * self.M * self.a**2 * np.sin(theta)**2 / sig**2 * (sig - r * d_sig_dr)
        d_A_dtheta = 4 * self.M * r * self.a**2 * np.sin(theta) * np.cos(theta) / sig - \
                     2 * self.M * r * self.a**2 * np.sin(theta)**2 * d_sig_dtheta / sig**2
        
        J[3, 1] = (d_A_dr * sig * np.sin(theta)**2 - A * d_sig_dr * np.sin(theta)**2) / (sig**2 * np.sin(theta)**4) * pphi - \
                  (2 * self.M * pt) / sig**2 * (sig - r * d_sig_dr) * self.a
        J[3, 2] = (d_A_dtheta * sig * np.sin(theta)**2 - A * d_sig_dtheta * np.sin(theta)**2 - 2 * A * sig * np.sin(theta) * np.cos(theta)) / (sig**2 * np.sin(theta)**4) * pphi + \
                  (2 * self.M * r * self.a**2 * 2 * np.sin(theta) * np.cos(theta) * pt) / sig**2
        J[3, 4] = -(2 * self.M * r / sig) * self.a
        J[3, 7] = A / (sig * np.sin(theta)**2)
        
        return J
    
    def magnus_expansion_second_order(self, J0, J1, dtau):
        Omega1 = dtau * (J0 + J1) / 2
        Omega2 = (dtau**2 / 12) * (np.dot(J1, J0) - np.dot(J0, J1))
        return la.expm(Omega1 + Omega2)
    
    def operator_exp_solution_magnus(self, z0, dtau, n_steps):
        z_history = [z0.copy()]
        z = z0.copy()
        
        for i in range(n_steps):
            J0 = self.jacobian_matrix(z)
            z_mid = self.rk4_step(z, dtau / 2)
            J1 = self.jacobian_matrix(z_mid)
            
            exp_J = self.magnus_expansion_second_order(J0, J1, dtau)
            
            delta = z - z0
            delta_new = np.dot(exp_J, delta)
            z_new = z0 + delta_new
            
            z = z_new
            z_history.append(z.copy())
        
        return np.array(z_history)

def run_kerr_verification(a_over_M=0.5):
    a = a_over_M
    kg = KerrGeodesic(M=1.0, a=a)
    
    rs = kg.schwarzschild_radius()
    r0 = 10 * rs
    theta0 = np.pi / 2
    dtheta_dt0 = 0.0
    
    E = 1.0
    Lz = 3.0 * np.sqrt(kg.M * r0)
    Q = 0.0
    
    sig0 = kg.sigma(r0, theta0)
    delta0 = kg.delta(r0)
    
    pt0 = -E / (1 - 2 * kg.M * r0 / sig0)
    pphi0 = (Lz + 2 * kg.M * r0 * kg.a * E / sig0) / (r0**2 + kg.a**2 + 2 * kg.M * r0 * kg.a**2 / sig0)
    pr0 = np.sqrt(delta0 / sig0 * (E**2 - (1 - 2 * kg.M * r0 / sig0) * (-1)))
    ptheta0 = 0.0
    
    z_ref_init = np.array([0.0, r0, theta0, 0.0, pt0, pr0, ptheta0, pphi0])
    z_pert_init = z_ref_init + np.array([0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    
    dtau = 0.001
    n_steps = 200
    
    ref_history = [z_ref_init.copy()]
    z = z_ref_init.copy()
    for _ in range(n_steps):
        z = kg.rk4_step(z, dtau)
        ref_history.append(z.copy())
    ref_history = np.array(ref_history)
    
    pert_history = [z_pert_init.copy()]
    z = z_pert_init.copy()
    for _ in range(n_steps):
        z = kg.rk4_step(z, dtau)
        pert_history.append(z.copy())
    pert_history = np.array(pert_history)
    
    delta_rk4 = pert_history - ref_history
    
    delta_magnus_history = [z_pert_init - z_ref_init]
    delta = delta_magnus_history[0].copy()
    for i in range(n_steps):
        J0 = kg.jacobian_matrix(ref_history[i])
        J1 = kg.jacobian_matrix(ref_history[min(i+1, n_steps)])
        
        exp_J = kg.magnus_expansion_second_order(J0, J1, dtau)
        delta = np.dot(exp_J, delta)
        delta_magnus_history.append(delta.copy())
    delta_magnus_history = np.array(delta_magnus_history)
    
    delta_first_order_history = [z_pert_init - z_ref_init]
    delta = delta_first_order_history[0].copy()
    for i in range(n_steps):
        J = kg.jacobian_matrix(ref_history[i])
        exp_J = la.expm(dtau * J)
        delta = np.dot(exp_J, delta)
        delta_first_order_history.append(delta.copy())
    delta_first_order_history = np.array(delta_first_order_history)
    
    plt.figure(figsize=(18, 8))
    
    plt.subplot(131)
    plt.plot(ref_history[:, 3], ref_history[:, 1], label='Reference')
    plt.plot(pert_history[:, 3], pert_history[:, 1], label='Perturbed', linestyle='--')
    plt.xlabel('$\phi$')
    plt.ylabel('$r$')
    plt.title(f'Kerr Orbits (a/M={a_over_M})')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(132)
    tau = np.linspace(0, n_steps * dtau, n_steps + 1)
    plt.plot(tau, delta_rk4[:, 1], label='RK4 $\delta r$')
    plt.plot(tau, delta_first_order_history[:, 1], label='1st order $\delta r$', linestyle='--')
    plt.plot(tau, delta_magnus_history[:, 1], label='Magnus $\delta r$', linestyle=':')
    plt.xlabel('$\tau$')
    plt.ylabel('$\delta r$')
    plt.title('Radius Perturbation Comparison')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(133)
    plt.plot(tau, delta_rk4[:, 2], label='RK4 $\delta \\theta$')
    plt.plot(tau, delta_first_order_history[:, 2], label='1st order $\delta \\theta$', linestyle='--')
    plt.plot(tau, delta_magnus_history[:, 2], label='Magnus $\delta \\theta$', linestyle=':')
    plt.xlabel('$\tau$')
    plt.ylabel('$\delta \\theta$')
    plt.title('Theta Perturbation Comparison')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'kerr_geodesic_comparison_a{int(a_over_M*10)}.png', dpi=300)
    
    max_r_error_first = np.max(np.abs(delta_rk4[:, 1] - delta_first_order_history[:, 1]))
    max_r_error_magnus = np.max(np.abs(delta_rk4[:, 1] - delta_magnus_history[:, 1]))
    max_theta_error_first = np.max(np.abs(delta_rk4[:, 2] - delta_first_order_history[:, 2]))
    max_theta_error_magnus = np.max(np.abs(delta_rk4[:, 2] - delta_magnus_history[:, 2]))
    
    print(f"\n=== Kerr Geodesic Verification (a/M={a_over_M}) ===")
    print(f"Schwarzschild radius: rs = {rs:.6f}")
    print(f"Initial radius: r0 = {r0:.6f} ({r0/rs:.1f} rs)")
    print(f"Initial perturbation: delta_r = 0.1")
    print(f"Total steps: {n_steps}")
    print(f"Time step: dtau = {dtau}")
    print(f"\n--- First Order Operator Semigroup ---")
    print(f"Max delta_r error: {max_r_error_first:.6f}")
    print(f"Max delta_theta error: {max_theta_error_first:.6f}")
    print(f"\n--- Second Order Magnus Expansion ---")
    print(f"Max delta_r error: {max_r_error_magnus:.6f}")
    print(f"Max delta_theta error: {max_theta_error_magnus:.6f}")
    
    with open(f'kerr_verification_results_a{int(a_over_M*10)}.txt', 'w') as f:
        f.write(f"=== Kerr Geodesic Verification Results (a/M={a_over_M}) ===\n")
        f.write(f"Schwarzschild radius: rs = {rs:.6f}\n")
        f.write(f"Initial radius: r0 = {r0:.6f} ({r0/rs:.1f} rs)\n")
        f.write(f"Initial perturbation: delta_r = 0.1\n")
        f.write(f"Total steps: {n_steps}\n")
        f.write(f"Time step: dtau = {dtau}\n")
        f.write(f"\n--- First Order Operator Semigroup ---\n")
        f.write(f"Max delta_r error: {max_r_error_first:.6f}\n")
        f.write(f"Max delta_theta error: {max_theta_error_first:.6f}\n")
        f.write(f"\n--- Second Order Magnus Expansion ---\n")
        f.write(f"Max delta_r error: {max_r_error_magnus:.6f}\n")
        f.write(f"Max delta_theta error: {max_theta_error_magnus:.6f}\n")
    
    print(f"\nResults saved to kerr_verification_results_a{int(a_over_M*10)}.txt")
    print(f"Plot saved to kerr_geodesic_comparison_a{int(a_over_M*10)}.png")
    
    return max_r_error_first, max_r_error_magnus

if __name__ == "__main__":
    print("=" * 60)
    print("Kerr Geodesic Verification with Magnus Expansion")
    print("=" * 60)
    
    errors_05 = run_kerr_verification(a_over_M=0.5)
    errors_09 = run_kerr_verification(a_over_M=0.9)
    
    print("\n" + "=" * 60)
    print("Summary of Results")
    print("=" * 60)
    print(f"a/M=0.5:")
    print(f"  First order max error: {errors_05[0]:.6f}")
    print(f"  Magnus max error: {errors_05[1]:.6f}")
    print(f"  Improvement factor: {errors_05[0]/errors_05[1]:.2f}x")
    print(f"\na/M=0.9:")
    print(f"  First order max error: {errors_09[0]:.6f}")
    print(f"  Magnus max error: {errors_09[1]:.6f}")
    print(f"  Improvement factor: {errors_09[0]/errors_09[1]:.2f}x")