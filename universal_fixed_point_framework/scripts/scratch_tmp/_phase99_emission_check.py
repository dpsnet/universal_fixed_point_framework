# -*- coding: utf-8 -*-
"""Phase 99 延伸-1：查 3 颗反常发射线星在 LAMOST 的命中 + 中场场强分档对照"""
import json
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"

j = json.load(open(BASE + r"\paperX_lamost_crossmatch_fixed.json", encoding="utf-8"))
raw = json.load(open(BASE + r"\paperX_lamost_linelevel_raw.json", encoding="utf-8"))

targets = ["J233817.93+083732.6", "J225828.48+280828.8", "J101712.60+233646.6"]
print("== 3 颗反常发射线星（附录 B，B~12-14 MG）在 LAMOST 命中 ==")
found = {}
for key in ("mid", "weak"):
    for g in j[key]:
        if g["name"] in targets:
            found[g["name"]] = (key, g["B_MG"], len(g["lamost"]))
            if g["lamost"]:
                best = sorted(g["lamost"], key=lambda r: float(r.get("dist_arcsec", 1e9)))[0]
                print("%s B=%.1f MG 命中 %d 条 -> obsid=%s dist=%.1f\" snrr=%.1f class=%s" % (
                    g["name"], g["B_MG"], len(g["lamost"]), best["obsid"],
                    float(best.get("dist_arcsec", 0)), float(best.get("snrr", 0)), best.get("class")))
            else:
                print("%s B=%.1f MG 无 LAMOST 命中" % (g["name"], g["B_MG"]))
for t in targets:
    if t not in found:
        print("%s 不在 mid/weak 样本中（检查其 B 档）" % t)

# 中场场强分档对照（LAMOST Balmer 检测样本）
print("\n== LAMOST 中场内部场强分档（η_sc 单调性检验）==")
def hb(r):
    return r.get("lines", {}).get("Hbeta", {}).get("d_meas")
def dmean(r):
    ds = [l["d_pure"] for l in r.get("lines", {}).values() if l.get("d_pure") is not None and np.isfinite(l["d_pure"])]
    return float(np.mean(ds)) if ds else np.nan

rows = [r for r in raw if r.get("grp") == "mid" and r.get("name") and hb(r) is not None and hb(r) > 0.05]
for lo, hi, lab in ((10, 20, "10-20 MG"), (20, 50, "20-50 MG"), (50, 100, "50-100 MG")):
    sub = [r for r in rows if lo <= r["B_MG"] < hi]
    if sub:
        print("%s: n=%d  Hbeta d_meas 中位 %.3f  五线 d_pure 中位 %.3f  snrr 中位 %.1f" % (
            lab, len(sub), np.median([hb(r) for r in sub]),
            np.nanmedian([dmean(r) for r in sub]), np.median([r.get("snrr", 0) for r in sub])))
    else:
        print("%s: n=0" % lab)
