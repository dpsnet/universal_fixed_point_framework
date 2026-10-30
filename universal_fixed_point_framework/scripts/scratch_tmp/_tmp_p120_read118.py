# -*- coding: utf-8 -*-
"""读 118 权威 JSON 关键点，与谱方法收敛测试对照。"""
import json
d = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e118_m128_scan.json", encoding="utf-8"))
out = d["out"]
print("fit_2p:", {k: round(v, 8) if isinstance(v, float) else v for k, v in d["fit_2p"].items()})
print("fit_3p:", {k: round(v, 8) if isinstance(v, float) else v for k, v in d["fit_3p"].items()})
for m in ["-33", "-64", "-96", "-110", "-118", "-122", "-127", "-128"]:
    v = out.get(m)
    if v:
        print(m, "Bstar0=%.8f  delta=%.7f  pred=%.6f  dev=%+.3f pct" % (v["Bstar0"], v["delta"], v["pred_hyper"], v["dev_pct"]))
