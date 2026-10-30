# -*- coding: utf-8 -*-
"""Phase 74 窗口扫描：Kepler 32 颗（B 10-105 MG）多窗口 EW + Koester 同窗口理论 EW
SDSS 光谱经 astroquery.sdss（备用直连 URL）；窗口 80/160/320 + half-gap 截断
输出 _m83d_window_scan.json（逐星 + 回归）
"""
import io, json, os, sys, time
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

WINDOWS = [80.0, 160.0, 320.0]

_BW = sorted(v10.BALMER.items(), key=lambda kv: kv[1])
def half_gaps():
    hg = {}
    for i, (nm, c) in enumerate(_BW):
        lo = _BW[i-1][1] if i > 0 else None
        hi = _BW[i+1][1] if i+1 < len(_BW) else None
        cand = [d for d in (None if lo is None else c-lo, None if hi is None else hi-c) if d]
        hg[nm] = min(cand) / 2.0 - 1.0
    return hg
HG = half_gaps()

def measure_ew_w(wl, fl, center, window):
    m = (wl >= center-window) & (wl <= center+window)
    if np.sum(m) < 5:
        return 0.0, False
    w, f = wl[m], fl[m]
    ew = float(np.trapezoid(1.0 - f, w))
    cm = np.abs(w-center) < 5
    depth = 1.0 - np.median(f[cm]) if np.sum(cm) > 0 else 0
    return ew, (ew > 0.5 and depth > 0.03)

def total_ew(wl, nf, window, protect=True):
    tew, nd, per = 0.0, 0, {}
    for nm, c in v10.BALMER.items():
        weff = min(window, HG[nm]) if protect else window
        ew, det = measure_ew_w(wl, nf, c, weff)
        per[nm] = {"ew": float(ew), "det": bool(det), "w": float(weff)}
        if det:
            tew += ew; nd += 1
    return tew, nd, per

# ---- Koester 网格 ----
with io.open(os.path.join(BASE, "paperX_wd_m83c_fid_table.json"), "r", encoding="utf-8") as f:
    fid_tbl = json.load(f)
grid = {}
for k, v in fid_tbl.items():
    t, g = k.split("_")
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid)); loggs = sorted(set(g for t, g in grid))
def nearest(teff, logg):
    return min(teffs, key=lambda x: abs(x-teff)), min(loggs, key=lambda x: abs(x-logg))

cache_dir = os.path.join(BASE, "_koester_spec")
def load_koester(teff, logg):
    t, g = nearest(teff, logg)
    fid = grid.get((t, g))
    if fid is None:
        return None
    fp = os.path.join(cache_dir, "fid%s_%s_%s.dat" % (fid, t, g))
    if not os.path.exists(fp):
        return None
    wl2, fl2 = [], []
    with io.open(fp, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if len(p) >= 2:
                try:
                    wl2.append(float(p[0])); fl2.append(float(p[1]))
                except ValueError:
                    pass
    if len(wl2) < 100:
        return None
    return np.array(wl2), np.array(fl2), (t, g)

# ---- 1) Kepler 样本 ----
with io.open(os.path.join(BASE, "paperX_wd_m83d_kepler_sample.json"), "r", encoding="utf-8") as f:
    sample = json.load(f)
todo = [s for s in sample if s.get("status") == "ok"]
print("kepler ok stars:", len(todo))

from astroquery.sdss import SDSS
import urllib.request

def get_spectrum(star, retries=3):
    parts = star["Sp-ID"].split("-")
    plate, mjd, fiber = int(parts[0]), int(parts[1]), int(parts[2])
    for attempt in range(retries):
        try:
            sp = SDSS.get_spectra(plate=plate, mjd=mjd, fiberID=fiber, timeout=60)
            if sp and len(sp) > 0:
                d = sp[0][1].data
                return 10.0 ** d["loglam"], np.array(d["flux"], dtype=float)
        except Exception as e:
            last = str(e)[:80]
        time.sleep(3 * (attempt + 1))
    # 备用直连
    try:
        url = "https://dr12.sdss.org/spectrum/redux/data/spectra/%d/%d/spec-%d-%d-%d.fits" % (plate, mjd, plate, mjd, fiber)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        import tempfile, fitsio  # noqa
        raise RuntimeError("fitsio not guaranteed; fallback astroquery only")
    except Exception as e2:
        return None, str(e2)[:80]

# ---- 2) 主循环 ----
star_ews = {}
fail = {}
for s in todo:
    nm = s["name"]
    wl, fl = get_spectrum(s)
    if wl is None:
        fail[nm] = fl
        continue
    good = np.isfinite(fl) & (fl > 0)
    if good.sum() < 500:
        fail[nm] = "flux_bad"
        continue
    w, f = wl[good], fl[good]
    nf = v10.normalize(w, f)
    rec = {"B_MG": s["B_MG"], "Teff": s["Teff"], "logg": s["logg"], "Sp-ID": s["Sp-ID"]}
    for prot in (True, False):
        rec["p" if prot else "n"] = {}
        for W in WINDOWS:
            tew, nd, per = total_ew(w, nf, W, protect=prot)
            rec["p" if prot else "n"][str(int(W))] = {"tew": tew, "nd": nd, "per": per}
    star_ews[nm] = rec
    print("ok", nm, "B=%.0f" % s["B_MG"])

print("downloaded:", len(star_ews), "fail:", len(fail))
for k, v in fail.items():
    print("FAIL", k, str(v)[:80])

# ---- 3) Koester 理论 ----
koester_ews = {}
for nm, st in star_ews.items():
    k = load_koester(st["Teff"], st["logg"])
    if k is None:
        continue
    wl_a, fl_a, key = k
    if key in koester_ews:
        continue
    nf2 = v10.normalize(wl_a, fl_a)
    koester_ews[key] = {}
    for prot in (True, False):
        koester_ews[key]["p" if prot else "n"] = {}
        for W in WINDOWS:
            tew, nd, _ = total_ew(wl_a, nf2, W, protect=prot)
            koester_ews[key]["p" if prot else "n"][str(int(W))] = {"tew": tew, "nd": nd}

# ---- 4) 回归 ----
from scipy.stats import spearmanr
regs = {}
for prot in (True, False):
    tag = "protect" if prot else "no_protect"
    for W in WINDOWS:
        recs = []
        for nm, st in star_ews.items():
            obs = st["p" if prot else "n"][str(int(W))]["tew"]
            if obs <= 0:
                continue
            kk = load_koester(st["Teff"], st["logg"])
            if kk is None:
                continue
            theo = koester_ews.get(kk[2], {}).get("p" if prot else "n", {}).get(str(int(W)), {}).get("tew", 0.0)
            if theo <= 0:
                continue
            recs.append({"name": nm, "B_MG": st["B_MG"], "Teff": st["Teff"],
                         "obs_EW": obs, "koester_EW": theo,
                         "resid": float(np.log10(obs/theo))})
        if len(recs) >= 5:
            X = np.array([[np.log10(r["B_MG"]*100.0), r["Teff"]] for r in recs], dtype=float)
            y = np.array([r["resid"] for r in recs], dtype=float)
            Xc = X - X.mean(axis=0)
            Xd = np.column_stack([np.ones(len(y)), Xc])
            beta = np.linalg.solve(Xd.T @ Xd, Xd.T @ y)
            resid = y - Xd @ beta
            s2 = resid @ resid / (len(y) - 3)
            se = np.sqrt(np.diag(s2 * np.linalg.inv(Xd.T @ Xd)))
            t = beta / se
            rho, p = spearmanr(Xc[:, 0], y)
            regs["%s_W%s" % (tag, int(W))] = {"n": len(recs), "log10B": float(beta[1]), "t_log10B": float(t[1]),
                                              "Teff": float(beta[2]), "rho": float(rho), "p": float(p)}
        else:
            regs["%s_W%s" % (tag, int(W))] = {"n": len(recs), "note": "too_few"}

with io.open(os.path.join(BASE, "_m83d_window_scan.json"), "w", encoding="utf-8") as f:
    json.dump({"star_ews": star_ews, "koester_ews": {("%s_%s" % (k[0], k[1])): v for k, v in koester_ews.items()},
               "regs": regs, "fail": fail, "windows": WINDOWS, "half_gaps": HG}, f, ensure_ascii=False, indent=1)
print("--- regressions ---")
for tag in ("protect", "no_protect"):
    for W in WINDOWS:
        r = regs["%s_W%d" % (tag, int(W))]
        print("%s W=%d: n=%d log10B=%.3f (t=%.2f) rho=%.3f p=%.3e" % (tag, W, r["n"], r.get("log10B", 0), r.get("t_log10B", 0), r.get("rho", 0), r.get("p", 0)))
