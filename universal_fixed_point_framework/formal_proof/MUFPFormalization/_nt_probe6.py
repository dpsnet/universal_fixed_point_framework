import numpy as np

m = 1.0
d = 1e-3

def vals(p):
    c = m - np.cos(p) - np.cos(d)
    s = np.sqrt(np.sin(p)**2 + np.sin(d)**2 + c**2)
    V = s*(s+c)
    sc2 = (s-c)**2 + np.sin(p)**2 + np.sin(d)**2
    return c, s, V, sc2

for p in [0.0, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.5, np.pi/2, 2.0, np.pi]:
    c,s,V,sc2 = vals(p)
    print(f"p={p:.6e} c={c:+.6e} s={s:.6e} V={V:+.6e} (s-c)^2+sig={sc2:+.6e} "
          f"1/V={1/V if V!=0 else float('inf'):+.4e} 2/sc2={2/sc2:+.4e}")

print()
# brute force trapezoid with fine grid near 0
for N in [100001, 1000001]:
    p = np.linspace(-np.pi, np.pi, N)
    c = m - np.cos(p) - np.cos(d)
    s = np.sqrt(np.sin(p)**2 + np.sin(d)**2 + c**2)
    V = s*(s+c)
    sc2 = (s-c)**2 + np.sin(p)**2 + np.sin(d)**2
    integ = np.cos(p)/V
    integ2 = 2*np.cos(p)/sc2
    dp = p[1]-p[0]
    print(f"N={N}: int cos p/V = {integ.sum()*dp:+.8e}   int 2cos p/sc2 = {integ2.sum()*dp:+.8e}")