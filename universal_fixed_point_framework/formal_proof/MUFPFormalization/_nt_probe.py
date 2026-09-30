import numpy as np

# QWZ: d = (sin k0, sin k1, m + cos k0 + cos k1)
# F = -1/2 * N / s^3, N = cos k0 + cos k1 + m cos k0 cos k1
# C = (1/2pi) * int int F dk0 dk1

def Fgrid(m, N=4000):
    k = np.linspace(0, 2*np.pi, N, endpoint=False)
    K0, K1 = np.meshgrid(k, k, indexing='ij')
    c = m + np.cos(K0) + np.cos(K1)
    s = np.sqrt(np.sin(K0)**2 + np.sin(K1)**2 + c**2)
    Nn = np.cos(K0) + np.cos(K1) + m*np.cos(K0)*np.cos(K1)
    F = -0.5 * Nn / s**3
    dk = (2*np.pi/N)**2
    return F.sum()*dk

def alpha0(m, k0, k1):
    c = m + np.cos(k0) + np.cos(k1)
    s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
    V = s*(s+c)
    return -np.sin(k1)*np.cos(k0)/V

def G(m, k1, N=200000):
    k0 = np.linspace(0, 2*np.pi, N, endpoint=False)
    return alpha0(m, k0, k1).sum()*(2*np.pi/N)

for m in [3.0, 1.5, 1.0, 0.5, -0.5, -1.0, -1.5, -3.0]:
    I = Fgrid(m)
    C = I/(2*np.pi)
    print(f"m={m:+.2f}  int F = {I:+.6f}   C = {C:+.6f}")

print()
for m in [1.5, 1.0, 0.5]:
    # jump of G at k1 = pi
    eps = 1e-3
    Gminus = G(m, np.pi - eps)
    Gplus  = G(m, np.pi + eps)
    print(f"m={m}: G(pi-eps)={Gminus:+.5f}  G(pi+eps)={Gplus:+.5f}  jump={Gminus-Gplus:+.5f}  half={0.5*(Gminus-Gplus):+.5f}  intF={Fgrid(m):+.5f}")