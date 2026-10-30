# -*- coding: utf-8 -*-
"""Phase 99 M99-4b：LAMOST 中场 vs 弱场线级对照 + SNR 匹配
判据：Balmer 检测样本（Hbeta d_meas>0.05）内比较
"""
import json
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
raw = json.load(open(BASE + r"\paperX_lamost_linelevel_raw.json", encoding="utf-8"))

def hb(r):
    return r.get("lines", {}).get("Hbeta", {}).get("d_meas")

def dmean(r):
    """五线 d_pure 均值（仅检测线）"""
    ds = [l["d_pure"] for l in r.get("lines", {}).values() if l.get("d_pure") is not None and np.isfinite(l["d_pure"])]
    return float(np.mean(ds)) if ds else np.nan

def grp_stats(rows):
    rows = [r for r in rows if r.get("name") and hb(r) is not None]
    bal = [r for r in rows if hb(r) > 0.05]
    print("  总 %d, Balmer 检测 %d (%.0f%%)" % (len(rows), len(bal), 100 * len(bal) / max(len(rows), 1)))
    if not bal:
        return
    print("  Hbeta d_meas: 中位 %.3f (P25 %.3f P75 %.3f)" % (
        np.median([hb(r) for r in bal]),
        np.percentile([hb(r) for r in bal], 25),
        np.percentile([hb(r) for r in bal], 75)))
    print("  五线 d_pure 均值: 中位 %.3f (P25 %.3f P75 %.3f)" % (
        np.median([dmean(r) for r in bal]),
        np.percentile([dmean(r) for r in bal], 25),
        np.percentile([dmean(r) for r in bal], 75)))
    print("  Hdelta d_meas: 中位 %.3f" % np.median([r.get("lines", {}).get("Hdelta", {}).get("d_meas", 0) for r in bal]))
    snrs = [r.get("snrr", 0) for r in bal]
    print("  snrr: 中位 %.1f (P25 %.1f P75 %.1f)" % (np.median(snrs), np.percentile(snrs, 25), np.percentile(snrs, 75)))

mid = [r for r in raw if r.get("grp") == "mid"]
wk = [r for r in raw if r.get("grp") == "weak"]
print("== LAMOST 中场（B 10-100 MG）==")
grp_stats(mid)
print("== LAMOST 弱场（B <10 MG）==")
grp_stats(wk)

# SNR 匹配对照：weak 子样本 snrr >= mid Balmer 中位
bal_mid = [r for r in mid if r.get("name") and hb(r) is not None and hb(r) > 0.05]
bal_wk = [r for r in wk if r.get("name") and hb(r) is not None and hb(r) > 0.05]
if bal_mid and bal_wk:
    med_mid_snr = np.median([r.get("snrr", 0) for r in bal_mid])
    print("\n== SNR 匹配对照（weak 子样本 snrr>=%.1f）==" % med_mid_snr)
    wk_m = [r for r in bal_wk if r.get("snrr", 0) >= med_mid_snr]
    print("weak 匹配子样本 n=%d" % len(wk_m))
    if wk_m:
        print("  weak snrr 中位 %.1f vs mid %.1f" % (
            np.median([r.get("snrr", 0) for r in wk_m]), np.median([r.get("snrr", 0) for r in bal_mid])))
        print("  Hbeta d_meas: weak %.3f vs mid %.3f  (比值 %.2f)" % (
            np.median([hb(r) for r in wk_m]), np.median([hb(r) for r in bal_mid]),
            np.median([hb(r) for r in wk_m]) / max(np.median([hb(r) for r in bal_mid]), 1e-6)))
        print("  五线 d_pure: weak %.3f vs mid %.3f  (比值 %.2f)" % (
            np.median([dmean(r) for r in wk_m]), np.median([dmean(r) for r in bal_mid]),
            np.median([dmean(r) for r in wk_m]) / max(np.median([dmean(r) for r in bal_mid]), 1e-6)))
        # 单侧检验（Mann-Whitney U：weak > mid 的线深）
        from scipy import stats
        u, p = stats.mannwhitneyu([dmean(r) for r in wk_m], [dmean(r) for r in bal_mid], alternative="greater")
        print("  Mann-Whitney U: p=%.4f (弱场线更深方向)" % p)
        u2, p2 = stats.mannwhitneyu([hb(r) for r in wk_m], [hb(r) for r in bal_mid], alternative="greater")
        print("  Hbeta MWU: p=%.4f" % p2)
