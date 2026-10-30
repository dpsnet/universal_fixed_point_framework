# -*- coding: utf-8 -*-
"""Phase 104az-49c：DESI mid_full 三线 41 MG 同位性验证"""
import json
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"

def med(v):
    v = [x for x in v if x is not None and np.isfinite(x)]
    return np.median(v) if v else float("nan")

midf = json.load(open(BASE + r"\paperX_wd_linelevel_mid_full_snr.json", encoding="utf-8"))["mid_full"]
desi = [r for r in midf if r.get("B_MG") is not None]

KEYS = [("Hbeta", "Hβ"), ("Hgamma", "Hγ"), ("Hdelta", "Hδ"), ("Heps", "Hε")]

print("=== DESI 四线 d_pure 场内分档（41 MG 同位性检验） ===")
for lo, hi in [(10, 20), (20, 41), (41, 60), (60, 1000)]:
    sub = [r for r in desi if lo <= r["B_MG"] < hi]
    if not sub:
        continue
    row = "B[%2d,%3d) n=%2d  " % (lo, hi, len(sub))
    for key, lbl in KEYS:
        yes = [r for r in sub if r.get("lines", {}).get(key)
               and np.isfinite(r["lines"][key].get("d_pure")) and r["lines"][key]["d_pure"] >= 0]
        if yes:
            ds = [r["lines"][key]["d_pure"] for r in yes]
            row += "  %s: %.4f(%d/%d)" % (lbl, med(ds), len(yes), len(sub))
        else:
            row += "  %s:  --  " % lbl
    print(row)

print("\n=== DESI 41 MG 切换点三线对比（B<41 vs B>=41） ===")
for key, lbl in KEYS:
    for lbl2, lo, hi in [("B<41", 10, 41), ("B>=41", 41, 1000)]:
        yes = [r for r in desi if lo <= r["B_MG"] < hi and r.get("lines", {}).get(key)
               and np.isfinite(r["lines"][key].get("d_pure")) and r["lines"][key]["d_pure"] >= 0]
        ds = [r["lines"][key]["d_pure"] for r in yes]
        allsub = [r for r in desi if lo <= r["B_MG"] < hi]
        print("  %s %s: d_pure 中位 %.4f (n=%d/%d, 有线率 %.0f%%)" %
              (lbl, lbl2, med(ds), len(yes), len(allsub), 100.0 * len(yes) / len(allsub)))
    print()
