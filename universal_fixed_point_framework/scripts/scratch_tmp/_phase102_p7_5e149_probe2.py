# -*- coding: utf-8 -*-
"""P7-5e-149 续：探明 tridiag/m32 数据结构并提取 B*"""
import json

base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
for fn in ["_phase102_p7_5e_fullchain_tridiag.json", "_phase102_p7_5e117_m32_scan.json"]:
    with open(base + "\\" + fn, "r", encoding="utf-8") as f:
        d = json.load(f)
    print("=== %s ===" % fn, flush=True)
    for k, v in d.items():
        if isinstance(v, dict):
            print("  %s：dict 键 %s" % (k, list(v.keys())[:6]), flush=True)
            for k2, v2 in list(v.items())[:2]:
                print("      %s：%s" % (k2, str(v2)[:80]), flush=True)
        elif isinstance(v, list):
            print("  %s：list len %d，首元素 %s" % (k, len(v), str(v[0])[:80]), flush=True)
        else:
            print("  %s：%s" % (k, str(v)[:80]), flush=True)
