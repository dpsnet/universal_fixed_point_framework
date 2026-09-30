import numpy as np

def alpha0(m, k0, k1):
    c = m + np.cos(k0) + np.cos(k1)
    s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
    V = s*(s+c)
    return -np.sin(k1)*np.cos(k0)/V

def G(m, k1, N=400000):
    k0 = np.linspace(0, 2*np.pi, N, endpoint=False)
    return alpha0(m, k0, k1).sum()*(2*np.pi/N)

m = 1.0
print("G(k1) for m=1:")
for k1 in [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.1, 3.14, np.pi]:
    print(f"  k1={k1:.3f}  G={G(m,k1):+.6f}")
print()
for k1 in [np.pi+0.01, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.2]:
    print(f"  k1={k1:.3f}  G={G(m,k1):+.6f}")
print()
# also m=0.5 and m=1.9
for mm in [0.5, 1.9, 0.01]:
    print(f"m={mm}: G(pi/2)={G(mm, np.pi/2):+.6f}  G(3pi/2)={G(mm, 3*np.pi/2):+.6f}")