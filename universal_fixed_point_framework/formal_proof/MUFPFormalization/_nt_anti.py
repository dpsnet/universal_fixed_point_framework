import numpy as np
from scipy import integrate

m = 1.5

def Fint(k0, k1):
    a = np.cos(k0); b = np.cos(k1)
    c = m + a + b
    s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
    N = a + b + m*a*b
    return -0.5*N/s**3

def Phi(k0, k1):
    b = np.cos(k1)
    Q = 2*(m+b)
    P = 2 + m*m + 2*m*b
    B = (1+m*b)/Q
    A = (2*B*P - b)/Q
    a = np.cos(k0)
    c = m + a + b
    s = np.sqrt(np.sin(k0)**2 + np.sin(k1)**2 + c**2)
    return (A + B*a)/s

for k1 in [0.5, 1.5, 3.0, 4.0, 5.0]:
    I,_ = integrate.quad(lambda k0: Fint(k0,k1), 0, 2*np.pi, limit=400, epsabs=1e-12)
    dPhi = Phi(2*np.pi,k1) - Phi(0.0,k1)
    print(f"k1={k1:+.2f}  int F dk0={I:+.8f}   Phi(2pi)-Phi(0)={dPhi:+.8f}")