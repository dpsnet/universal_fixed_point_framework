# -*- coding: utf-8 -*-
"""Phase 99 M99-4a：LAMOST 光谱线级分析
- 每颗 FITS：wl/flux 归一化（连续谱中值=1）
- Balmer 五线 d_pure：±8Å 窗中位深度（LAMOST ~1.4Å/px 适配），±20Å wing 中位基线
- DA 验证：Hβ 深度 + 蓝端斜率
- 中场 vs 弱场对照（同仪器 SNR 匹配对照）
"""
import json, os, glob, re
import numpy as np

SPEC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_lamost_spec"
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
from astropy.io import fits

BALMER = {"Hbeta": 4861.3, "Hgamma": 4340.5, "Hdelta": 4101.7, "Heps": 3970.1, "Hzeta": 3889.0}

def load_fits(path):
    hdul = fits.open(path)
    d = hdul[1].data
    wl = np.array(d["WAVELENGTH"]).ravel()
    fl = np.array(d["FLUX"]).ravel()
    iv = np.array(d["IVAR"]).ravel()
    hdul.close()
    return wl, fl, iv

def line_metrics(wl, fl, line_c, win=8.0, wing=20.0):
    """返回 (d_win, d_wing, d_pure)"""
    mc = (wl > line_c - win) & (wl < line_c + win)
    mw = ((wl > line_c - wing) & (wl < line_c - win)) | ((wl > line_c + win) & (wl < line_c + wing))
    if mc.sum() < 2 or mw.sum() < 4:
        return None
    dc = np.median(fl[mc])
    dw = np.median(fl[mw])
    return dc, dw, 1.0 - dc / dw if dw > 0 else np.nan

def analyze(path):
    try:
        wl, fl, iv = load_fits(path)
    except Exception as e:
        return {"err": str(e)}
    fln = np.array(fl, dtype=float)
    good = np.isfinite(fln) & (fln > 0)
    fln[~good] = np.nan
    # 连续谱归一化：Balmer 区外中值（4500-4700 与 5100-5400）
    mcont = ((wl > 4500) & (wl < 4700)) | ((wl > 5100) & (wl < 5400))
    med = np.nanmedian(fln[mcont])
    if not np.isfinite(med) or med <= 0:
        return {"err": "norm"}
    fln = fln / med
    lines = {}
    for lab, c in BALMER.items():
        m = line_metrics(wl, fln, c)
        if m:
            dc, dw, dp = m
            lines[lab] = {"d_win": dc, "d_wing": dw, "d_pure": dp,
                          "d_meas": 1.0 - dc}  # d_meas=窗内深度（对照 SDSS 口径概念）
    # DA 判据：Hbeta 吸收存在（d_win<0.97）且 Hdelta/Heps 深
    hb = lines.get("Hbeta", {}).get("d_meas")
    hd = lines.get("Hdelta", {}).get("d_meas")
    he = lines.get("Heps", {}).get("d_meas")
    da_like = bool(hb and hb > 0.03 and hd and he and hd > 0.1 and he > 0.1)
    return {"lines": lines, "da_like": da_like, "n_line": sum(1 for l in lines.values() if l["d_pure"] > 0.02)}

def main():
    j = json.load(open(BASE + r"\paperX_lamost_crossmatch_fixed.json", encoding="utf-8"))
    # (planid, spid, fiberid) -> 星信息（取 dist 最小行）
    key2star = {}
    for key in ("mid", "weak"):
        for g in j[key]:
            if not g["lamost"]:
                continue
            best = min(g["lamost"], key=lambda r: float(r.get("dist_arcsec", 1e9) or 1e9))
            k = (best.get("planid", ""), int(best.get("spid", 0) or 0), int(best.get("fiberid", 0) or 0))
            key2star[k] = {"name": g["name"], "B_MG": g["B_MG"], "grp": key,
                           "snrr": float(best.get("snrr", 0) or 0),
                           "dist": float(best.get("dist_arcsec", 0) or 0),
                           "obsid": best.get("obsid", "")}
    results = []
    files = glob.glob(os.path.join(SPEC, "*.fits"))
    matched = 0
    for f in files:
        base = os.path.basename(f).replace(".fits", "")
        # spec-{lmjd}-{planid}_sp{spid}-{fiberid}
        m = re.search(r"spec-\d+-(.+)_sp(\d+)-(\d+)$", base)
        res = analyze(f)
        rec = {"file": base}
        if res.get("err"):
            rec["err"] = res["err"]
        else:
            rec.update({k: v for k, v in res.items() if k != "err"})
        if m:
            k = (m.group(1), int(m.group(2)), int(m.group(3)))
            st = key2star.get(k)
            if st:
                rec["name"] = st["name"]
                rec["B_MG"] = st["B_MG"]
                rec["grp"] = st["grp"]
                rec["snrr"] = st["snrr"]
                rec["dist"] = st["dist"]
                rec["obsid"] = st["obsid"]
                matched += 1
        results.append(rec)
    print("总解析: %d, 匹配回星: %d" % (len(results), matched))
    n_err = sum(1 for r in results if "err" in r)
    n_da = sum(1 for r in results if r.get("da_like"))
    print("错误 %d, DA-like %d" % (n_err, n_da))
    json.dump(results, open(BASE + r"\paperX_lamost_linelevel_raw.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("saved paperX_lamost_linelevel_raw.json")

if __name__ == "__main__":
    main()
