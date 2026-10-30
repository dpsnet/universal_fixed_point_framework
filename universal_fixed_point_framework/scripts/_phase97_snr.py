# -*- coding: utf-8 -*-
"""Phase 97 M97-1：SDSS 光谱 SNR 估算（142 中场 + 99 弱场）
相邻像素差法：连续谱区（避开 Balmer ±50 Å）噪声 = std(diff)/sqrt(2)，SNR = median(fl)/noise
"""
import json, io, os, sys, time
import numpy as np
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
from white_dwarf_analysis_v10 import get_spec, BALMER, OTHER, normalize

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"

def estimate_snr(wl, fl):
    """连续谱区噪声：相邻像素差法"""
    mask = np.ones(len(wl), dtype=bool)
    for lw in list(BALMER.values()) + OTHER:
        mask &= (np.abs(wl - lw) > 50)
    mask &= (wl >= 4000) & (wl <= 6800)
    if np.sum(mask) < 20:
        return None
    f = fl[mask]
    diff = np.diff(f)
    noise = np.std(diff) / np.sqrt(2.0)
    if noise <= 0:
        return None
    return float(np.median(np.abs(f)) / noise)

def main():
    mid = json.load(open(os.path.join(BASE, "paperX_wd_linelevel_mid_full.json"), encoding="utf-8"))["mid_full"]
    wk = json.load(open(os.path.join(BASE, "paperX_wd_linelevel_weak_sdss.json"), encoding="utf-8"))["weak_sdss"]
    out_mid, out_wk = [], []
    for grp, out in ((mid, out_mid), (wk, out_wk)):
        for s in grp:
            spec = get_spec(s, max_retries=2)
            snr = None
            if spec is not None:
                wl, fl = spec
                fn = normalize(wl, fl)
                snr = estimate_snr(wl, fn)
            s2 = dict(s)
            s2["snr_approx"] = snr
            out.append(s2)
            print("  %s B=%.1f MG snr=%s" % (s["name"], s["B_MG"], "%.1f" % snr if snr else "None"), flush=True)
            time.sleep(0.2)
    json.dump({"mid_full": out_mid}, io.open(os.path.join(BASE, "paperX_wd_linelevel_mid_full_snr.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"weak_sdss": out_wk}, io.open(os.path.join(BASE, "paperX_wd_linelevel_weak_sdss_snr.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 汇总
    for label, grp in (("中场", out_mid), ("弱场", out_wk)):
        snrs = [s["snr_approx"] for s in grp if s["snr_approx"]]
        print("%s: 有SNR %d/%d, SNR中位=%.1f" % (label, len(snrs), len(grp), np.median(snrs) if snrs else 0), flush=True)
    print("written *_snr.json")

if __name__ == "__main__":
    main()
