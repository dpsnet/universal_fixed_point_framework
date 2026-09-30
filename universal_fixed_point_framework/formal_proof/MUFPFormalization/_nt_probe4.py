import numpy as np
from scipy import integrate

m = 1.5
def jump(eps):
    def h(k0):
        c = m + np.cos(k0) - np.cos(eps)
        s = np.sqrt(np.sin(k0)**2 + np.sin(eps)**2 + c**2)
        return -2*np.sin(eps)*np.cos(k0)/(s*(s+c))
    v,_ = integrate.quad(h, 0, 2*np.pi, limit=2000, points=[np.pi], epsabs=1e-12)
    return v

print("4pi =", 4*np.pi)
for eps in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
    print(f"eps={eps:.0e}  J={jump(eps):.10f}   J-4pi={jump(eps)-4*np.pi:+.3e}")

print()
# G(pi-eps) accuracy
def G(k1):
    def f(k0):
        c = m + np.cos(k0) + np.cos(k1)
        s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
        return -np.sin(k1)*np.cos(k0)/(s*(s+c))
    v,_ = integrate.quad(f, 0, 2*np.pi, limit=2000, points=[np.pi], epsabs=1e-12)
    return v
print("2pi =", 2*np.pi)
for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
    print(f"eps={eps:.0e}  G(pi-eps)={G(np.pi-eps):.10f}  G(pi+eps)={G(np.pi+eps):.10f}")