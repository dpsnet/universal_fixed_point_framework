# -*- coding: utf-8 -*-
"""Phase 90 M90-1/2：强场 π/σ 分量测量
对 20 颗 v10_int 强场星，每条 Balmer 线：
- π 分量深度（中心 ±5 Å，即 d_pure）
- σ± 分量深度（Δλ=4.67e-13 λ² B_G 位置 ±40 Å，若在谱覆盖内）
- 判据：π 窄浅=禁戒；σ 可见=Zeeman 残余；π 宽=展宽候选
"""
import io, json, os, sys
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

LINE_C = {'Hbeta': 4861.3, 'Hgamma': 4340.5, 'Hdelta': 4101.7, 'Hepsilon': 3970.1, 'Hzeta': 3889.1}

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel_v10int.json"), "r", encoding="utf-8") as f:
    d = json.load(f)
stars = d["strong"]

def depth_at(wl, nf, center, half):
    m = (wl >= center - half) & (wl <= center + half)
    if np.sum(m) < 5:
        return None, 0
    return float(np.median(1.0 - nf[m])), int(np.sum(m))

out = []
for st in sorted(stars, key=lambda x: x["B_MG"]):
    gid = st["gid"]
    fp = os.path.join(BASE, "_desi_spec", gid + ".npz")
    if not os.path.exists(fp):
        continue
    npz = np.load(fp)
    wl = npz["wave"]; fl = npz["flux"]
    good = np.isfinite(fl) & (fl > 0)
    if good.sum() < 500:
        continue
    w, f = wl[good], fl[good]
    nf = v10.normalize(w, f)
    B_G = st["B_MG"] * 1e6
    star = {"name": st["name"], "B_MG": st["B_MG"], "Teff": st["Teff"], "components": {}}
    for ln, c in LINE_C.items():
        dL = 4.67e-13 * c ** 2 * B_G
        # π 分量（中心）
        dp, _ = depth_at(w, nf, c, 5.0)
        # σ± 分量（Δλ 位置）
        ds_p, np_p = depth_at(w, nf, c + dL, 40.0)
        ds_m, np_m = depth_at(w, nf, c - dL, 40.0)
        # 已有线级记录（sig/wpi）
        rec = st["lines"].get(ln, {})
        star["components"][ln] = {
            "dL": dL,
            "d_pi": dp,
            "d_sig_plus": ds_p, "d_sig_minus": ds_m,
            "sig_obs": rec.get("sig_obs"), "wpi": rec.get("wpi"),
            "d_meas": rec.get("d_meas")}
    out.append(star)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_pi_sigma.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

# ---- 汇总：每星判据 ----
print("%-20s %7s %5s | %-14s | %-14s | %-10s" % ("星", "B_MG", "线数", "π深(中位)", "σ±可见线", "判定"))
for st in out:
    comps = st["components"]
    # 仅统计 σ 在谱内的线
    dpi = []
    n_sig_vis = 0
    n_det = 0
    for ln, cc in comps.items():
        if cc["d_pi"] is not None:
            dpi.append(cc["d_pi"])
        c = LINE_C[ln]
        if cc["d_sig_plus"] is not None and cc["d_sig_plus"] > 0.03:
            n_sig_vis += 1
        if cc["d_sig_minus"] is not None and cc["d_sig_minus"] > 0.03:
            n_sig_vis += 1
        if cc["d_pi"] is not None and cc["d_pi"] > 0.03:
            n_det += 1
    med_pi = float(np.median(dpi)) if dpi else None
    if n_det == 0:
        judge = "禁戒(π全消)" if n_sig_vis == 0 else "禁戒+σ残"
    elif med_pi is not None and med_pi < 0.03:
        judge = "禁戒主导(π浅)"
    else:
        judge = "有线(π≥0.03)"
    print("%-20s %7.1f %5d | %-14s | %-14s | %-10s" % (
        st["name"], st["B_MG"], len(comps),
        "%.3f" % med_pi if med_pi is not None else "—",
        str(n_sig_vis), judge))
print("written paperX_wd_pi_sigma.json")
