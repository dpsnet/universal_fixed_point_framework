import numpy as np
from scipy import integrate

m = 1.5

def alpha0(k0, k1):
    c = m + np.cos(k0) + np.cos(k1)
    s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
    V = s*(s+c)
    return -np.sin(k1)*np.cos(k0)/V

def A(q):
    # integral over p in [0,2pi] of alpha0(pi+p, pi+q)
    v,_ = integrate.quad(lambda p: alpha0(np.pi+p, np.pi+q), 0, 2*np.pi,
                         limit=4000, points=[np.pi], epsabs=1e-13)
    return v

print("target -2*pi*sgn(q):", -2*np.pi)
for q in [1e-1,1e-2,1e-3,1e-4,1e-5,1e-6]:
    print(f"q=+{q:.0e}  A={A(q):+.8f}   A+2pi={A(q)+2*np.pi:+.3e}")
for q in [1e-1,1e-2,1e-3,1e-4,1e-5,1e-6]:
    print(f"q=-{q:.0e}  A={A(-q):+.8f}   A-2pi={A(-q)-2*np.pi:+.3e}")

print()
# G(k1) = int_0^{2pi} alpha0(k0,k1) dk0 near k1=pi
def G(k1):
    v,_ = integrate.quad(lambda k0: alpha0(k0,k1), 0, 2*np.pi, limit=4000,
                         points=[np.pi], epsabs=1e-13)
    return v
for q in [1e-2,1e-3,1e-4]:
    print(f"G(pi-{q:.0e})={G(np.pi-q):+.8f}  G(pi+{q:.0e})={G(np.pi+q):+.8f}  diff={G(np.pi-q)-G(np.pi+q):+.8f}")
print("4pi=",4*np.pi)