# -*- coding: utf-8 -*-
import sys, os
import importlib.util
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
for name, fname in [("p227", "_phase102_p7_5e227_dinf_final_shoot_ext.py"),
                    ("p230c", "_phase102_p7_5e230c_shoot_full_chain.py")]:
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print("== %s ==" % fname, flush=True)
    m = 33
    Bc = 1.0/mod.closed_1B(m)
    r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
    for i in range(7):
        B = Bc*(1-0.0265) + 2.0*0.0265*Bc*i/6.0
        try:
            e = mod.E0_shooting(B, m, r_lo, r_hi)
            print("  B[%d]=%.6f E0=%.6f" % (i, B, e), flush=True)
        except Exception as ex:
            print("  B[%d]=%.6f FAIL: %s" % (i, B, ex), flush=True)
