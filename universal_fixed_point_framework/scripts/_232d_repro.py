# -*- coding: utf-8 -*-
import sys, os, time
import importlib.util
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
spec = importlib.util.spec_from_file_location("p230c", os.path.join(BASE, "_phase102_p7_5e230c_shoot_full_chain.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print("== 重跑 230c worker_sh(-33) ==", flush=True)
t0 = time.time()
try:
    r = mod.worker_sh(-33)
    print("OK:", r, " 耗时 %.1fs" % (time.time()-t0), flush=True)
except Exception as ex:
    print("FAIL:", ex, " 耗时 %.1fs" % (time.time()-t0), flush=True)
# 尝试加宽 E0 网格
print("== 加宽 E0 网格探测（-1.0 起）==", flush=True)
def E0_wide(B, m, r_lo, r_hi):
    for (E_low, E_hi, step) in [(-0.01, 0.011, 0.0001), (-0.1, 0.101, 0.001), (-1.0, 1.001, 0.01)]:
        nE = int((E_hi - E_low)/step) + 1
        prev_psi = None; prev_E = None
        for i in range(nE):
            E = E_low + step*i
            psi, nn = mod.shoot_wall(E, r_lo, r_hi, B, m)
            if prev_psi is not None and prev_psi*psi < 0.0:
                from scipy.optimize import brentq
                Eroot = brentq(lambda e: mod.shoot_wall(e, r_lo, r_hi, B, m)[0],
                               prev_E, E, xtol=1e-12, rtol=1e-12)
                _, nn2 = mod.shoot_wall(Eroot, r_lo, r_hi, B, m)
                if nn2 == 0:
                    return Eroot
            prev_psi, prev_E = psi, E
    raise RuntimeError("wide 未定位基态 m=%d B=%.6f" % (m, B))

m = -33
Bc = 1.0/mod.closed_1B(m)
r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
for i in range(7):
    B = Bc*(1-0.0265) + 2.0*0.0265*Bc*i/6.0
    try:
        e = E0_wide(B, m, r_lo, r_hi)
        print("  B[%d]=%.6f E0(wide)=%.6f" % (i, B, e), flush=True)
    except Exception as ex:
        print("  B[%d]=%.6f FAIL(wide): %s" % (i, B, ex), flush=True)
