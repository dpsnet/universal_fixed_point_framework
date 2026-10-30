# -*- coding: utf-8 -*-
"""P7-5e-171 step 0: probe 170 JSON structure."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
for fn in ["_phase102_p7_5e170_spectral_m1024.json",
           "_phase102_p7_5e170b_h2_m1024.json",
           "_phase102_p7_5e160_spectral_m512.json"]:
    try:
        d = json.load(open(base + "\\" + fn, encoding='utf-8'))
        print("="*70)
        print("FILE:", fn)
        print("TOP KEYS:", list(d.keys()))
        for k, v in d.items():
            if isinstance(v, dict):
                print("  dict[%s] keys: %s" % (k, list(v.keys())[:15]))
            elif isinstance(v, list):
                print("  list[%s] len=%d first=%s" % (k, len(v), str(v[:5])[:200]))
            else:
                print("  scalar[%s] = %s" % (k, str(v)[:120]))
    except Exception as e:
        print("ERR", fn, e)
