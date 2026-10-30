# -*- coding: utf-8 -*-
"""Phase 104az-48：Hδ 冲突溯源——DESI vs LAMOST Hδ 测量星特征 + 选择性"""
import json
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"

def med(v):
    v = [x for x in v if x is not None and np.isfinite(x)]
    return np.median(v) if v else float("nan")

midf = json.load(open(BASE + r"\paperX_wd_linelevel_mid_full_snr.json", encoding="utf-8"))["mid_full"]
desi = [r for r in midf if r.get("B_MG") is not None]
lam = json.load(open(BASE + r"\paperX_lamost_linelevel_raw.json", encoding="utf-8"))
lamost = [r for r in lam if r.get("grp") == "mid" and r.get("B_MG") is not None]

def hd_meas(r):
    return r.get("lines", {}).get("Hdelta") and np.isfinite(r["lines"]["Hdelta"].get("d_pure")) and r["lines"]["Hdelta"]["d_pure"] >= 0

print("=== 1. Hδ 有测量星特征（DESI vs LAMOST） ===")
for name, stars in [("DESI", desi), ("LAMOST", lamost)]:
    hd = [r for r in stars if hd_meas(r)]
    hb = [r for r in stars if r.get("lines", {}).get("Hbeta")
          and np.isfinite(r["lines"]["Hbeta"].get("d_pure")) and r["lines"]["Hbeta"]["d_pure"] >= 0]
    print("--- %s: 总 n=%d, Hδ n=%d, Hβ n=%d ---" % (name, len(stars), len(hd), len(hb)))
    if hd:
        print("  Hδ星: B 中位 %.1f (%.1f–%.1f) | Teff 中位 %s (n=%d) | d_pure 中位 %.4f | >0.15 占比 %.0f%%" %
              (med([r["B_MG"] for r in hd]), min(r["B_MG"] for r in hd), max(r["B_MG"] for r in hd),
               ("%.0f" % med([r.get("Teff") for r in hd])) if any(r.get("Teff") for r in hd) else "  --",
               sum(1 for r in hd if r.get("Teff") is not None),
               med([r["lines"]["Hdelta"]["d_pure"] for r in hd]),
               100.0 * sum(1 for r in hd if r["lines"]["Hdelta"]["d_pure"] > 0.15) / len(hd)))
    if hb:
        print("  Hβ星: B 中位 %.1f | Teff 中位 %s (n=%d) | d_pure 中位 %.4f" %
              (med([r["B_MG"] for r in hb]),
               ("%.0f" % med([r.get("Teff") for r in hb])) if any(r.get("Teff") for r in hb) else "  --",
               sum(1 for r in hb if r.get("Teff") is not None),
               med([r["lines"]["Hbeta"]["d_pure"] for r in hb])))

print("\n=== 2. Hδ 无测量星选择性（B 分布） ===")
for name, stars in [("DESI", desi), ("LAMOST", lamost)]:
    no = [r for r in stars if not hd_meas(r)]
    yes = [r for r in stars if hd_meas(r)]
    print("--- %s: 无测量 n=%d, 有测量 n=%d ---" % (name, len(no), len(yes)))
    if no:
        bs = [r["B_MG"] for r in no]
        print("  无测量星 B: 中位 %.1f (%.1f–%.1f), B>=20 占比 %.0f%%" %
              (med(bs), min(bs), max(bs), 100.0 * sum(1 for x in bs if x >= 20) / len(bs)))
        ts = [r.get("Teff") for r in no if r.get("Teff") is not None]
        if ts:
            print("  无测量星 Teff: 中位 %.0f (n=%d)" % (med(ts), len(ts)))
    if yes:
        bs = [r["B_MG"] for r in yes]
        print("  有测量星 B: 中位 %.1f (%.1f–%.1f), B>=20 占比 %.0f%%" %
              (med(bs), min(bs), max(bs), 100.0 * sum(1 for x in bs if x >= 20) / len(bs)))

print("\n=== 3. Hδ 测量可检测性 vs B/Teff（缺失=线消失还是检测门槛？） ===")
for name, stars in [("DESI", desi), ("LAMOST", lamost)]:
    print("--- %s ---" % name)
    for lo, hi in [(10, 20), (20, 41), (41, 80), (80, 1000)]:
        sub = [r for r in stars if lo <= r["B_MG"] < hi]
        if not sub:
            continue
        n_ok = sum(1 for r in sub if hd_meas(r))
        ts = [r.get("Teff") for r in sub if r.get("Teff") is not None]
        print("  B[%2d,%3d) 星=%2d  Hδ有线=%2d (%.0f%%)  无线率 %.0f%%  Teff中位%s" %
              (lo, hi, len(sub), n_ok, 100.0 * n_ok / len(sub), 100.0 * (len(sub) - n_ok) / len(sub),
               ("%.0f" % med(ts)) if ts else "  --"))
