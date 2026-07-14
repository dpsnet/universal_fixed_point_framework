import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

class SchwarzschildGeodesic:
    def __init__(self, M=1.0):
        self.M = M
        self.G = 1.0
        self.c = 1.0
    
    def schwarzschild_radius(self):
        return 2 * self.G * self.M / self.c**2
    
    def hamiltonian_system(self, z):
        t, r, phi, pt, pr, pphi = z
        rs = self.schwarzschild_radius()
        
        dt_dtau = -(1 - rs / r) * pt
        dr_dtau = (1 - rs / r) * pr
        dphi_dtau = pphi / r**2
        
        dpt_dtau = 0
        
        dpr_dtau = -(rs / (2 * r**2)) / (1 - rs / r)**2 * pt**2 + \
                   (rs / (2 * r**2)) * (1 - rs / r) * pr**2 + \
                   pphi**2 / r**3
        
        dpphi_dtau = 0
        
        return np.array([dt_dtau, dr_dtau, dphi_dtau, dpt_dtau, dpr_dtau, dpphi_dtau])
    
    def rk4_step(self, z, dtau):
        k1 = self.hamiltonian_system(z)
        k2 = self.hamiltonian_system(z + 0.5 * dtau * k1)
        k3 = self.hamiltonian_system(z + 0.5 * dtau * k2)
        k4 = self.hamiltonian_system(z + dtau * k3)
        return z + dtau * (k1 + 2*k2 + 2*k3 + k4) / 6
    
    def jacobian_matrix(self, z):
        t, r, phi, pt, pr, pphi = z
        rs = self.schwarzschild_radius()
        
        J = np.zeros((6, 6))
        
        J[0, 1] = rs * pt / r**2
        J[0, 3] = -(1 - rs / r)
        
        J[1, 1] = rs * pr / r**2
        J[1, 4] = (1 - rs / r)
        
        J[2, 1] = -2 * pphi / r**3
        J[2, 5] = 1 / r**2
        
        J[4, 1] = (rs / r**3) / (1 - rs / r)**2 * pt**2 - \
                   (3*rs / (2 * r**3)) * (1 - rs / r) * pr**2 - \
                   3 * pphi**2 / r**4
        J[4, 4] = rs * pr / r**2
        
        return J

def run_verification():
    sg = SchwarzschildGeodesic(M=1.0)
    
    rs = sg.schwarzschild_radius()
    r0 = 10 * rs
    dr_dt0 = 0.0
    dphi_dt0 = np.sqrt(sg.G * sg.M) / r0**(3/2)
    dt_dt0 = 1.0 / (1 - rs / r0)
    
    pr0 = dr_dt0 / (1 - rs / r0)
    pphi0 = r0**2 * dphi_dt0
    pt0 = -dt_dt0 * (1 - rs / r0)
    
    z_ref_init = np.array([0.0, r0, 0.0, pt0, pr0, pphi0])
    z_pert_init = z_ref_init + np.array([0.0, 0.1, 0.0, 0.0, 0.0, 0.0])
    
    dtau = 0.001
    n_steps = 200
    
    ref_history = [z_ref_init.copy()]
    z = z_ref_init.copy()
    for _ in range(n_steps):
        z = sg.rk4_step(z, dtau)
        ref_history.append(z.copy())
    ref_history = np.array(ref_history)
    
    pert_history = [z_pert_init.copy()]
    z = z_pert_init.copy()
    for _ in range(n_steps):
        z = sg.rk4_step(z, dtau)
        pert_history.append(z.copy())
    pert_history = np.array(pert_history)
    
    delta_rk4 = pert_history - ref_history
    
    delta_op_history = [z_pert_init - z_ref_init]
    delta = delta_op_history[0].copy()
    for i in range(n_steps):
        J = sg.jacobian_matrix(ref_history[i])
        exp_J = la.expm(dtau * J)
        delta = np.dot(exp_J, delta)
        delta_op_history.append(delta.copy())
    delta_op_history = np.array(delta_op_history)
    
    plt.figure(figsize=(15, 6))
    
    plt.subplot(131)
    plt.plot(ref_history[:, 2], ref_history[:, 1], label='Reference')
    plt.plot(pert_history[:, 2], pert_history[:, 1], label='Perturbed', linestyle='--')
    plt.xlabel('$\phi$')
    plt.ylabel('$r$')
    plt.title('Schwarzschild Orbits')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(132)
    tau = np.linspace(0, n_steps * dtau, n_steps + 1)
    plt.plot(tau, delta_rk4[:, 1], label='RK4 $\delta r$')
    plt.plot(tau, delta_op_history[:, 1], label='Op Semigroup $\delta r$', linestyle='--')
    plt.xlabel('$\tau$')
    plt.ylabel('$\delta r$')
    plt.title('Radius Perturbation Comparison')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(133)
    plt.plot(tau, delta_rk4[:, 2], label='RK4 $\delta \phi$')
    plt.plot(tau, delta_op_history[:, 2], label='Op Semigroup $\delta \phi$', linestyle='--')
    plt.xlabel('$\tau$')
    plt.ylabel('$\delta \phi$')
    plt.title('Angle Perturbation Comparison')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('schwarzschild_geodesic_comparison.png', dpi=300)
    
    max_r_error = np.max(np.abs(delta_rk4[:, 1] - delta_op_history[:, 1]))
    mean_r_error = np.mean(np.abs(delta_rk4[:, 1] - delta_op_history[:, 1]))
    max_phi_error = np.max(np.abs(delta_rk4[:, 2] - delta_op_history[:, 2]))
    mean_phi_error = np.mean(np.abs(delta_rk4[:, 2] - delta_op_history[:, 2]))
    
    print("=== Schwarzschild Geodesic Perturbation Verification ===")
    print(f"Schwarzschild radius: rs = {rs:.6f}")
    print(f"Initial radius: r0 = {r0:.6f} ({r0/rs:.1f} rs)")
    print(f"Initial perturbation: delta_r = 0.1")
    print(f"Total steps: {n_steps}")
    print(f"Time step: dtau = {dtau}")
    print(f"\nMax delta_r error: {max_r_error:.6f}")
    print(f"Mean delta_r error: {mean_r_error:.6f}")
    print(f"Max delta_phi error: {max_phi_error:.6f}")
    print(f"Mean delta_phi error: {mean_phi_error:.6f}")
    print(f"\nFinal RK4 delta_r: {delta_rk4[-1, 1]:.6f}")
    print(f"Final Op Semigroup delta_r: {delta_op_history[-1, 1]:.6f}")
    print(f"Final RK4 delta_phi: {delta_rk4[-1, 2]:.6f}")
    print(f"Final Op Semigroup delta_phi: {delta_op_history[-1, 2]:.6f}")
    
    with open('schwarzschild_verification_results.txt', 'w') as f:
        f.write("=== Schwarzschild Geodesic Perturbation Verification Results ===\n")
        f.write(f"Schwarzschild radius: rs = {rs:.6f}\n")
        f.write(f"Initial radius: r0 = {r0:.6f} ({r0/rs:.1f} rs)\n")
        f.write(f"Initial perturbation: delta_r = 0.1\n")
        f.write(f"Total steps: {n_steps}\n")
        f.write(f"Time step: dtau = {dtau}\n")
        f.write(f"\nMax delta_r error: {max_r_error:.6f}\n")
        f.write(f"Mean delta_r error: {mean_r_error:.6f}\n")
        f.write(f"Max delta_phi error: {max_phi_error:.6f}\n")
        f.write(f"Mean delta_phi error: {mean_phi_error:.6f}\n")
        f.write(f"\nFinal RK4 delta_r: {delta_rk4[-1, 1]:.6f}\n")
        f.write(f"Final Op Semigroup delta_r: {delta_op_history[-1, 1]:.6f}\n")
        f.write(f"Final RK4 delta_phi: {delta_rk4[-1, 2]:.6f}\n")
        f.write(f"Final Op Semigroup delta_phi: {delta_op_history[-1, 2]:.6f}\n")
    
    print("\nResults saved to schwarzschild_verification_results.txt")
    print("Plot saved to schwarzschild_geodesic_comparison.png")

if __name__ == "__main__":
    run_verification()