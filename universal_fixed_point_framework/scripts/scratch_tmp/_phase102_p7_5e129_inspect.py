# -*- coding: utf-8 -*-
import json
j = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e117_m32_scan.json", encoding="utf-8"))
print(type(j).__name__)
if isinstance(j, dict):
    ks = list(j.keys())[:10]
    print("keys:", ks)
    k = ks[0]
    print("first value type:", type(j[k]).__name__)
    if isinstance(j[k], dict):
        print("first value keys:", list(j[k].keys())[:10])
        print(json.dumps(j[k], ensure_ascii=False)[:400])
    else:
        print(j[k])
else:
    print("len:", len(j))
    print(json.dumps(j[0], ensure_ascii=False)[:400] if j else "empty")
print("exit 0")
