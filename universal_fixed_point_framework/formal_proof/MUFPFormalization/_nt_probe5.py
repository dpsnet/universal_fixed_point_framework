import numpy as np
from scipy import integrate

# In shifted coords: k0 = pi + p, k1 = pi + d
# c = m - cos p - cos d ; s = sqrt(sin^2 p + sin^2 d + c^2) ; V = s(s+c)
# alpha0 = -sin k1 cos k0 / V = -sin d cos p / V
# G(pi+d) = -sin d * int_{-pi}^{pi} cos p / V dp

def Vfun(m, p, d):
    c = m - np.cos(p) - np.cos(d)
    s = np.sqrt(np.sin(p)**2 + np.sin(d)**2 + c**2)
    return s*(s+c)

def H(m, d, lim=4000):
    v,_ = integrate.quad(lambda p: np.cos(p)/Vfun(m,p,d), -np.pi, np.pi,
                         limit=lim, points=[0.0], epsabs=1e-13)
    return v

print("=== check: sin d * H  ->  -2pi ?  (G(pi+d)) ===")
for m in [1.0, 0.5, 1.5]:
    for d in [1e-2, 1e-3, 1e-4, 1e-5]:
        Hv = H(m, d)
        print(f"  m={m:.1f} d={d:.0e}  H={Hv:+.6e}  sin d*H={np.sin(d)*Hv:+.6f}  2pi={2*np.pi:.6f}")

print()
print("=== decomposition: int 2 cos p / sigma  and int 2 cos p/((s-c)^2+sigma) ===")
def sigma(p,d): return np.sin(p)**2 + np.sin(d)**2
def sc2(m,p,d):
    c = m - np.cos(p) - np.cos(d)
    s = np.sqrt(sigma(p,d) + c**2)
    return (s-c)**2 + sigma(p,d)

for m in [1.0]:
    for d in [1e-3, 1e-5]:
        I1,_ = integrate.quad(lambda p: 2*np.cos(p)/sigma(p,d), -np.pi, np.pi,
                              limit=4000, points=[-np.pi/2,0.0,np.pi/2], epsabs=1e-12)
        I2,_ = integrate.quad(lambda p: 2*np.cos(p)/sc2(m,p,d), -np.pi, np.pi,
                              limit=4000, points=[0.0], epsabs=1e-13)
        print(f"  m={m:.1f} d={d:.0e}  I1={I1:+.6e}  I2={I2:+.6e}  I1-I2={I1-I2:+.6e}  H={H(m,d):+.6e}")

print()
print("=== scaling of H vs 1/sin d ===")
for m in [1.0, 0.5, 1.5]:
    for d in [1e-3, 1e-4, 1e-5, 1e-6]:
        Hv = H(m, d)
        print(f"  m={m:.1f} d={d:.0e}  H*sin d={Hv*np.sin(d):+.6f}  H*d={Hv*d:+.6f}")