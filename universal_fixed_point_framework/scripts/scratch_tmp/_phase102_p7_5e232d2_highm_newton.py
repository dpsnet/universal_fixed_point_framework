# -*- coding: utf-8 -*-
"""232d 补跑：打靶 Newton 高 m 段（512/768/1024 3 点）——增强确认"""
import time, sys, os
import numpy as np
import importlib.util
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
spec = importlib.util.spec_from_file_location("p230c", os.path.join(BASE, "_phase102_p7_5e230c_shoot_full_chain.py"))
m230c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m230c)
C13 = 13.0/128.0; D41 = 41.0/2000.0; E39 = 39.0/2000.0; INV56 = 1.0/56.0; EPS_W = 0.215e-6

def Bstar_shoot_newton(mm, steps=1, h_rel=1e-5):
    m = -abs(mm)
    cl = m230c.closed_1B(m)
    r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
    B, Bs, Es = m230c.Bstar_shooting(m)
    for _ in range(steps):
        h = h_rel*abs(B)
        e_p = m230c.E0_shooting(B+h, m, r_lo, r_hi)
        e_m = m230c.E0_shooting(B-h, m, r_lo, r_hi)
        e_0 = m230c.E0_shooting(B, m, r_lo, r_hi)
        de = (e_p - e_m)/(2.0*h)
        if not np.isfinite(de) or de == 0.0:
            break
        dB = -e_0/de
        B = B + dB
        if abs(dB) < 1e-14*abs(B):
            break
    return B

if __name__ == "__main__":
    t0 = time.time()
    print("== 232d 补跑：打靶 Newton 高 m 段（512/768/1024）==", flush=True)
    for mm in [512, 768, 1024]:
        cl = m230c.closed_1B(-mm)
        Bc, _, _ = m230c.Bstar_shooting(-mm)
        Bn = Bstar_shoot_newton(mm)
        dc = cl - 1.0/Bc
        dn = cl - 1.0/Bn
        mod = INV56 + EPS_W - C13/mm - D41/mm**2 + E39/mm**3
        rn = dn - mod
        print("  m=%4d δ(三次拟合)=%.10f δ(Newton)=%.10f Δ=%+.2e r(Newton)=%+.2e（%.1fs）" %
              (mm, dc, dn, dn-dc, rn, time.time()-t0), flush=True)
    print("补跑完成 exit 0", flush=True)
