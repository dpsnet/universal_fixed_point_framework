import numpy as np
from scipy import integrate

# ---------- 2D BZ integral of the curvature F (gives Chern number) ----------
def chern(m, N=6000):
    k = np.linspace(0, 2*np.pi, N, endpoint=False)
    K0, K1 = np.meshgrid(k, k, indexing='ij')
    c = m + np.cos(K0) + np.cos(K1)
    s = np.sqrt(np.sin(K0)**2 + np.sin(K1)**2 + c**2)
    Nn = np.cos(K0) + np.cos(K1) + m*np.cos(K0)*np.cos(K1)
    F = -0.5 * Nn / s**3
    return F.sum()*(2*np.pi/N)**2

print("=== Chern number C = (1/2pi) int int F ===")
for m in [1.9, 1.5, 1.0, 0.5, 0.1, -0.1, -0.5, -1.0, -1.5, -1.9]:
    I = chern(m)
    print(f"  m={m:+.2f}   int F = {I:+.8f}   C = {I/(2*np.pi):+.8f}")

# ---------- jump J = G(pi^-) - G(pi^+) with G(k1) = int alpha0 dk0 ----------
def alpha0(m, k0, k1):
    c = m + np.cos(k0) + np.cos(k1)
    s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
    V = s*(s+c)
    return -np.sin(k1)*np.cos(k0)/V

def G(m, k1, limit=4000):
    v,_ = integrate.quad(lambda k0: alpha0(m,k0,k1), 0, 2*np.pi,
                         limit=limit, points=[np.pi], epsabs=1e-13)
    return v

print()
print("=== jump J = G(pi-eps) - G(pi+eps)  (expect 4pi = %.8f) ===" % (4*np.pi))
for m in [1.9, 1.5, 1.0, 0.5, 0.1]:
    for eps in [1e-3, 1e-5]:
        J = G(m, np.pi-eps) - G(m, np.pi+eps)
        print(f"  m={m:+.2f} eps={eps:.0e}  J={J:+.8f}  J-4pi={J-4*np.pi:+.3e}")

print()
print("=== G(0) vs G(2pi) (periodicity check), m=1.0 ===")
print("  G(0)   =", G(1.0, 0.0))
print("  G(2pi) =", G(1.0, 2*np.pi))