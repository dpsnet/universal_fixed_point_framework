import sympy as sp

k0, k1, m = sp.symbols('k0 k1 m', real=True)
a = sp.cos(k0); b = sp.cos(k1)
u = sp.sin(k0); v = sp.sin(k1)
c = m + a + b
rho2 = u**2 + v**2
s = sp.sqrt(rho2 + c**2)
# beta0 = -n_z * d0phi = c/s * (v*a/rho2)
beta0 = (c/s)*(v*a/rho2)
print("beta0 =", sp.simplify(beta0))
print()
I = sp.integrate(beta0, k0)
print("indef integral:")
print(sp.simplify(I))