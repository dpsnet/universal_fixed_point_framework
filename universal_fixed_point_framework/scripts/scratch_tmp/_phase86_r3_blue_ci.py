# -*- coding: utf-8 -*-
"""补跑 blue_calres bootstrap CI"""
import json, io
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
with io.open(BASE + r"\paperX_wd_absflux_cal.json", "r", encoding="utf-8") as f:
    data = json.load(f)
rows = data["rows"]

def clean(rows, cond, key):
    return [r[key] for r in rows if cond(r) and r.get(key) is not None and not (isinstance(r[key], float) and np.isnan(r[key]))]

w = clean(rows, lambda r: r["B_MG"] < 10 and 10000 <= r["Teff"] < 20000, "blue_calres")
m = clean(rows, lambda r: 10 <= r["B_MG"] < 100 and 10000 <= r["Teff"] < 20000, "blue_calres")
rng = np.random.default_rng(42)
diffs = []
for _ in range(5000):
    wb = rng.choice(w, len(w), replace=True)
    mb = rng.choice(m, len(m), replace=True)
    diffs.append(np.mean(mb) - np.mean(wb))
diffs = np.array(diffs)
print("blue_calres: 弱场 n=%d 中场 n=%d | 偏移 %+.4f dex [95%%CI %+.4f, %+.4f]" % (
    len(w), len(m), np.mean(m) - np.mean(w), np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)))
