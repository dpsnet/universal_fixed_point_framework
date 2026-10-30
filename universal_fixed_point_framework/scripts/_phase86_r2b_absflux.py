# -*- coding: utf-8 -*-
"""Phase 86 R2b：全量绝对 SED 标定与跳变区绝对吸收测量
DESI flux(1e-17 erg/cm2/s/A) 为绝对流量；模型 = Koester F_surf x (R/d)^2
输出 scripts/_gaia_abs/paperX_wd_absflux.json
"""
import json, io, os, re
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(BASE, "_gaia_abs")
os.makedirs(OUT, exist_ok=True)
FLUX_UNIT = 1e-17  # DESI flux 存储单位

with io.open(os.path.join(OUT, "gaia_parallax_phot.json"), "r", encoding="utf-8") as f:
    gai = json.load(f)["rows"]
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = {str(s["gaia_int"]): s for s in json.load(f)["samples"]}
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)

def load_koester(teff, logg):
    best = None
    for fn in os.listdir(os.path.join(BASE, "_koester_spec")):
        mm = re.match(r"fid\d+_([\d.]+)_([\d.]+)\.dat", fn)
        if not mm:
            continue
        t, g = float(mm.group(1)), float(mm.group(2))
        score = (t - teff) ** 2 + (g - logg) ** 2
        if best is None or score < best[0]:
            best = (score, os.path.join(BASE, "_koester_spec", fn))
    arr = np.loadtxt(best[1])
    return arr[:, 0], arr[:, 1], os.path.basename(best[1])

BANDS = {"blue": (3600, 3640), "red": (3700, 3750), "slopeA": (4000, 4060), "slopeB": (5000, 5800)}

def band_med(wl, fl, bd):
    m = (wl >= bd[0]) & (wl <= bd[1])
    return float(np.median(fl[m])) if np.sum(m) >= 2 else None

rows = []
for gid in sorted(cat):
    if gid not in gai or gid not in ew0 or not ew0[gid].get("ok"):
        continue
    g, s = gai[gid], cat[gid]
    par, perr = g["parallax"], g["parallax_error"]
    if not par or par <= 0:
        continue
    d_pc = 1000.0 / par
    # 质量-半径（v10 log_g 同口径）
    msun, rsun = 1.989e33, 6.96e10
    x = min(s["Mass"] / 1.44, 0.99)
    R_cm = 0.012 * (s["Mass"] / 0.6) ** (-1 / 3) * (1 - x ** (4 / 3)) ** 0.5 * rsun
    d_cm = d_pc * 3.086e18
    scale = (R_cm / d_cm) ** 2
    # 观测
    npz = os.path.join(BASE, "_desi_spec", gid + ".npz")
    if not os.path.exists(npz):
        continue
    d = np.load(npz, allow_pickle=True)
    wl, fl, iv = d["wave"], d["flux"], d["ivar"]
    # 模型
    wlk, fk, fid = load_koester(s["Teff"], s["logg"])
    row = {"gaia_int": int(gid), "B_MG": s["B_MG"], "Teff": s["Teff"], "logg": s["logg"],
           "parallax": par, "parallax_error": perr, "d_pc": d_pc, "koester": fid,
           "snr_blue": float(np.median(fl[(wl >= 3600) & (wl <= 3640)] * np.sqrt(iv[(wl >= 3600) & (wl <= 3640)]))),
           "snr_red": float(np.median(fl[(wl >= 3700) & (wl <= 3750)] * np.sqrt(iv[(wl >= 3700) & (wl <= 3750)])))}
    for nm, bd in BANDS.items():
        fo = band_med(wl, fl, bd)
        fm = band_med(wlk, fk, bd)
        if fo is not None and fm and fm > 0:
            f_obs = fo * FLUX_UNIT
            f_mod = fm * scale
            row[nm + "_obs"] = f_obs
            row[nm + "_mod"] = f_mod
            row[nm + "_res"] = float(np.log10(f_obs / f_mod))
        else:
            row[nm + "_res"] = None
    # 跳变绝对深度（red - blue，能量代理）
    if row.get("blue_obs") and row.get("red_obs") and row.get("blue_mod") and row.get("red_mod"):
        row["jump_obs"] = row["red_obs"] - row["blue_obs"]
        row["jump_mod"] = row["red_mod"] - row["blue_mod"]
        row["jump_res"] = float(np.log10(max(row["jump_obs"], 1e-30) / max(row["jump_mod"], 1e-30)))
    rows.append(row)

out = {"n": len(rows), "flux_unit": "1e-17 erg/cm2/s/A (DESI)", "rows": rows}
with io.open(os.path.join(OUT, "paperX_wd_absflux.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

# 分组汇总
def grp(rows, cond, key):
    vs = [r[key] for r in rows if cond(r) and r.get(key) is not None]
    return (len(vs), float(np.mean(vs)), float(np.std(vs))) if vs else (0, None, None)

print("n=%d" % len(rows))
for key in ["blue_res", "red_res", "slopeA_res", "slopeB_res", "jump_res"]:
    for nm, cond in [("弱场<10MG", lambda r: r["B_MG"] < 10),
                     ("中场10-100", lambda r: 10 <= r["B_MG"] < 100)]:
        n, mu, sd = grp(rows, cond, key)
        if n:
            print("%-10s %-12s n=%3d mean=%+.4f sd=%.4f" % (key, nm, n, mu, sd))
