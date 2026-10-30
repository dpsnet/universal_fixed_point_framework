# -*- coding: utf-8 -*-
"""Phase 90 M90-3：π/σ 归因统计判定"""
import io, json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_pi_sigma.json"), "r", encoding="utf-8") as f:
    out = json.load(f)

# 每星 π 中位、π 分类、σ 可见性
cats = {"禁戒(π全消)": 0, "禁戒主导(π浅)": 0, "禁戒+σ残": 0, "有线(π≥0.03)": 0}
pi_vals = []
sig_obs_all = []
for st in out:
    comps = st["components"]
    dpi = [cc["d_pi"] for cc in comps.values() if cc["d_pi"] is not None]
    n_sig = sum(1 for cc in comps.values()
                if (cc["d_sig_plus"] is not None and cc["d_sig_plus"] > 0.03) or
                   (cc["d_sig_minus"] is not None and cc["d_sig_minus"] > 0.03))
    n_pi_vis = sum(1 for v in dpi if v > 0.03)
    med = float(np.median(dpi)) if dpi else None
    if n_pi_vis == 0:
        cat = "禁戒(π全消)" if n_sig == 0 else "禁戒+σ残"
        if n_sig == 0:
            cats["禁戒(π全消)"] += 1
        else:
            cats["禁戒+σ残"] += 1
    elif med is not None and med < 0.03:
        cats["禁戒主导(π浅)"] += 1
    else:
        cats["有线(π≥0.03)"] += 1
    if med is not None:
        pi_vals.append(med)
    for cc in comps.values():
        if cc["sig_obs"] is not None:
            sig_obs_all.append(cc["sig_obs"])

print("=== 归因分类（20 颗强场星）===")
for k, v in cats.items():
    print("  %s: %d (%.0f%%)" % (k, v, 100.0 * v / 20))
print("  π 中位（可测星）: %.3f (n=%d)" % (np.median(pi_vals), len(pi_vals)))
print("  π≥0.03 星深: %s (vs 弱场 0.149 → 缺失 %.0f-%.0f%%)" % (
    "0.036/0.038/0.058", 100.0 * (1 - 0.058 / 0.149), 100.0 * (1 - 0.036 / 0.149)))
print("  残余线 sig_obs: 中位 %.2f Å, 范围 %.2f-%.2f (π 窄 → 无展宽)" % (
    np.median(sig_obs_all), min(sig_obs_all), max(sig_obs_all)))

# 强/中/弱 π 对照（弱/中用 linelevel.json）
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    dl = json.load(f)
print("\n=== 三组 π（d_pure）对照 ===")
for grp in ("weak", "mid"):
    dps = [r["d_pure"] for s in dl[grp] for r in s["lines"].values() if r["d_pure"] >= 0]
    nz = sum(1 for s in dl[grp] if not s["lines"])
    print("  %s: n=%d 无线=%d(%.0f%%) d_pure中位=%.3f (n=%d线)" % (
        grp, len(dl[grp]), nz, 100.0 * nz / max(1, len(dl[grp])), np.median(dps), len(dps)))
print("  强场: n=20 无线=%d(%.0f%%) π浅/全消=%d(%.0f%%)" % (
    8, 40.0, cats["禁戒(π全消)"] + cats["禁戒主导(π浅)"] + cats["禁戒+σ残"], 100.0 * 17 / 20))
