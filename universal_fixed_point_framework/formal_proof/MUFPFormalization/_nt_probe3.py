import numpy as np
from scipy import integrate

m = 1.5

def alpha0N(k0, k1):
    c = m + np.cos(k0) + np.cos(k1)
    s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
    V = s*(s+c)
    return -np.sin(k1)*np.cos(k0)/V

eps = 1e-3
k1m = np.pi - eps
k1p = np.pi + eps

# G at k1=pi-eps and pi+eps via scipy quad with points
def G(k1):
    # split at pi (near singularity)
    f = lambda k0: alpha0N(k0, k1)
    v1,_ = integrate.quad(f, 0, np.pi-1e-6, limit=400, points=[np.pi-1e-6])
    v2,_ = integrate.quad(f, np.pi-1e-6, 2*np.pi, limit=400, points=[np.pi+1e-6])
    return v1+v2

print("G(pi-eps) =", G(k1m))
print("G(pi+eps) =", G(k1p))
print("jump =", G(k1m)-G(k1p))
print()
# direct integral of h = alpha0N(k0,pi-eps)-alpha0N(k0,pi+eps)
h = lambda k0: alpha0N(k0, k1m) - alpha0N(k0, k1p)
v,_ = integrate.quad(h, 0, 2*np.pi, limit=800, points=[np.pi])
print("int h dk0 =", v)
print("4*pi =", 4*np.pi)