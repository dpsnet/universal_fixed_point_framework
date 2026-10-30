# -*- coding: utf-8 -*-
"""Phase 89b 续：v10_int 20 颗强场汇总统计 + 异常星甄别"""
import io, json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel_v10int.json"), "r", encoding="utf-8") as f:
    d = json.load(f)
stars = d["strong"]

# B 档：理论 η_sc（束缚态衰减，303 锚插值）
B_p = np.array([0.001, 0.01, 0.05, 0.1, 0.2]); N_p = np.array([303.0, 300.0, 152.0, 69.0, 33.0])
def eta(b):
    b = b / 2350.0
    n = float(np.interp(np.log10(b), np.log10(B_p), N_p))
    return max(0.0, min(1.0, 1.0 - n / 303.0))

print("=== 逐星 ===")
all_dp = []
for st in sorted(stars, key=lambda x: x["B_MG"]):
    dp = [r["d_pure"] for r in st["lines"].values()]
    med = float(np.median(dp)) if dp else None
    all_dp.extend(dp)
    print("%-20s B=%6.1f MG Teff=%7s 线数=%d 无线=%s d_pure中位=%s eta=%.2f" % (
        st["name"], st["B_MG"], st["Teff"], len(st["lines"]),
        "YES" if not dp else "", "%.3f" % med if med is not None else "—", eta(st["B_MG"])))
    for ln, r in st["lines"].items():
        print("    %s: d_meas=%.3f d_pure=%.3f sig=%.2f wpi=%.2f chi2=%.1f" % (
            ln, r["d_meas"], r["d_pure"], r["sig_obs"], r.get("wpi", -1), r.get("chi2_A", -1)))

print("\n=== 汇总 ===")
n0 = sum(1 for s in stars if not s["lines"])
print("总星数 %d | 无线 %d (%.0f%%) | 有线 %d" % (len(stars), n0, 100.0 * n0 / len(stars), len(stars) - n0))
print("有线星 d_pure 中位: %.3f (n=%d 线)" % (np.median(all_dp), len(all_dp)))

# B 档对比（剔除 385 异常星）
bins = [(100, 200), (200, 400), (400, 800)]
print("\n=== B 档对比 ===")
for lo, hi in bins:
    grp = [s for s in stars if lo <= s["B_MG"] < hi]
    dps = [r["d_pure"] for s in grp for r in s["lines"].values()]
    nz = sum(1 for s in grp if not s["lines"])
    print("%d-%d MG: n=%d 无线=%d(%.0f%%) 有线d_pure中位=%s (eta理论 %.2f-%.2f)" % (
        lo, hi, len(grp), nz, 100.0 * nz / max(1, len(grp)),
        "%.3f" % np.median(dps) if dps else "—", eta(lo), eta(hi)))

# 对照：DESI 弱/中/强（linelevel.json + linelevel_strong.json）
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    dl = json.load(f)
for grp in ("weak", "mid"):
    dps = [r["d_pure"] for s in dl[grp] for r in s["lines"].values()]
    nz = sum(1 for s in dl[grp] if not s["lines"])
    print("DESI %s: n=%d 无线=%d(%.0f%%) 有线d_pure中位=%.3f (n=%d线)" % (
        grp, len(dl[grp]), nz, 100.0 * nz / max(1, len(dl[grp])), np.median(dps), len(dps)))

# 异常星甄别：385 MG
print("\n=== 385 MG 异常星 ===")
for s in stars:
    if abs(s["B_MG"] - 385.0) < 1:
        for ln, r in s["lines"].items():
            print("%s: d_meas=%.3f d_pure=%.3f d_obs=%.3f sig=%.2f fwhm=%s wpi=%.2f chi2A=%.1f chi2B=%.1f" % (
                ln, r["d_meas"], r["d_pure"], r["d_obs"], r["sig_obs"], r.get("fwhm"), r.get("wpi", -1),
                r.get("chi2_A", -1), r.get("chi2_B", -1)))
