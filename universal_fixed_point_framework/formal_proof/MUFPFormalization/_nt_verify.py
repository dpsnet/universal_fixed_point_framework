import numpy as np
from scipy import integrate

def alpha0(m, k0, k1):
    c = m + np.cos(k0) + np.cos(k1)
    s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
    V = s*(s+c)
    return -np.sin(k1)*np.cos(k0)/V

def G(m, k1):
    v,_ = integrate.quad(lambda p: alpha0(m, np.pi+p, k1), 0, 2*np.pi,
                         limit=4000, points=[np.pi], epsabs=1e-13)
    return v

m = 1.5
print("=== G(pi+q) for m=1.5 ; 2pi =", 2*np.pi, " 4pi =", 4*np.pi)
for q in [-1.5,-1.0,-0.5,-0.3,-0.1,-0.01,-0.001, 0.001,0.01,0.1,0.3,0.5,1.0,1.5,2.0,3.0]:
    print(f"  q={q:+.4f}  G={G(m, np.pi+q):+.8f}   G/(2pi)={G(m,np.pi+q)/(2*np.pi):+.6f}")

print()
print("=== G(k1) as function of k1 in [0,2pi] for m=1.5")
for k1 in [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.10,3.14,3.1416]:
    print(f"  k1={k1:.4f}  G={G(m, k1):+.8f}")
for k1 in [3.1416,3.15,3.20,3.5,4.0,4.5,5.0,5.5,6.0,6.2832]:
    print(f"  k1={k1:.4f}  G={G(m, k1):+.8f}")

print()
print("=== Chern number via BZ integral of F")
def chern(m, N=6000):
    k = np.linspace(0, 2*np.pi, N, endpoint=False)
    K0, K1 = np.meshgrid(k, k, indexing='ij')
    c = m + np.cos(K0) + np.cos(K1)
    s = np.sqrt(np.sin(K0)**2 + np.sin(K1)**2 + c**2)
    Nn = np.cos(K0) + np.cos(K1) + m*np.cos(K0)*np.cos(K1)
    F = -0.5 * Nn / s**3
    return F.sum()*(2*np.pi/N)**2

for mm in [0.5, 1.0, 1.5, 1.9, -0.5, -1.0, -1.5, -1.9]:
    I = chern(mm)
    print(f"  m={mm:+.2f}  BZint(F)={I:+.6f}   C=I/(2pi)={I/(2*np.pi):+.6f}")