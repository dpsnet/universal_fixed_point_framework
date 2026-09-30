import numpy as np
from scipy import integrate

m = 1.5
kappa = 2 - m

def V(p, eps):
    c = m - np.cos(p) - np.cos(eps)
    s = np.sqrt(np.sin(p)**2 + np.sin(eps)**2 + c**2)
    return s*(s+c)

def h(p, eps):
    return 2*np.sin(eps)*np.cos(p)/V(p, eps)

def model(p, eps):
    return 4*np.sin(eps)*np.cos(p)/(np.sin(p)**2 + np.sin(eps)**2)

for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
    Ih,_ = integrate.quad(lambda p: h(p,eps), 0, np.pi, limit=2000,
                          points=[np.pi/2], epsabs=1e-13)
    Im,_ = integrate.quad(lambda p: model(p,eps), 0, np.pi, limit=2000,
                          points=[np.pi/2], epsabs=1e-13)
    Id,_ = integrate.quad(lambda p: h(p,eps)-model(p,eps), 0, np.pi, limit=2000,
                          points=[np.pi/2], epsabs=1e-13)
    print(f"eps={eps:.0e}  int_0^pi h={Ih:+.8f}  2*Ih={2*Ih:+.8f}  int model={Im:+.3e}  int diff={Id:+.8f}")

print()
print("check: 2*int_0^pi h should -> 4pi =", 4*np.pi)
print("kappa =", kappa)
# value of h at p=0
for eps in [1e-1,1e-2,1e-3]:
    print(f"  eps={eps:.0e}  h(0)={h(0,eps):.4f}  model(0)={model(0,eps):.4f}  ratio={h(0,eps)/model(0,eps):.6f}")