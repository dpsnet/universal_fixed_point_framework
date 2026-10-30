# -*- coding: utf-8 -*-
"""下载 237 颗有效样本 SDSS 光谱，读 FITS 头 SNR（SN_MEDIAN 等），增量落盘 _snr_results.json。
用 astroquery.sdss.SDSS（同 v10 通道）。"""
import io, json, os, sys, time

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
LIST = os.path.join(BASE, "_snr_dl_list.json")
OUT = os.path.join(BASE, "_snr_results.json")
LOG = os.path.join(BASE, "_snr_log.txt")

def log(msg):
    with io.open(LOG, "a", encoding="utf-8") as f:
        f.write("%s %s\n" % (time.strftime("%H:%M:%S"), msg))

with io.open(LIST, "r", encoding="utf-8") as f:
    items = json.load(f)

done = {}
if os.path.exists(OUT):
    with io.open(OUT, "r", encoding="utf-8") as f:
        done = json.load(f)

import numpy as np
import warnings
warnings.filterwarnings('ignore')
from astroquery.sdss import SDSS

keys_try = ["SN_MEDIAN", "MEDIAN", "SNR", "SN", "Z", "PLATE", "MJD", "FIBERID"]
todo = [it for it in items if it["name"] not in done]
log("start n_todo=%d done=%d" % (len(todo), len(done)))

for i, it in enumerate(todo):
    try:
        parts = it["spid"].strip().split("-")
        if len(parts) != 3:
            log("skip %s bad spid" % it["name"]); continue
        plate, mjd, fiber = int(parts[0]), int(parts[1]), int(parts[2])
        sp = SDSS.get_spectra(plate=plate, mjd=mjd, fiberID=fiber, timeout=60)
        hdr = sp[0][0].header
        rec = {"name": it["name"], "spid": it["spid"], "B": it["B"], "Teff": it["Teff"], "logg": it["logg"], "obs_EW": it["obs_EW"], "src": it["src"]}
        for k in keys_try:
            if k in hdr:
                rec[k] = str(hdr[k])
        if "SN_MEDIAN" not in rec:
            # 自算 SNR：归一化连续谱区噪声
            try:
                d = sp[0][1].data
                lam = 10.0 ** d["loglam"]
                fl = np.array(d["flux"], dtype=float)
                m = (lam >= 5400) & (lam <= 5600) & np.isfinite(fl)
                if m.sum() > 20:
                    med = np.median(fl[m])
                    noise = np.std(fl[m])
                    rec["SNR_est"] = float(med / noise) if noise > 0 else None
            except Exception as e2:
                rec["SNR_est_err"] = str(e2)[:80]
        done[it["name"]] = rec
        if (i + 1) % 10 == 0:
            with io.open(OUT, "w", encoding="utf-8") as f:
                json.dump(done, f, ensure_ascii=False)
            log("progress %d/%d" % (i + 1, len(todo)))
    except Exception as e:
        log("FAIL %s %s" % (it["name"], str(e)[:120]))
        done[it["name"]] = {"name": it["name"], "spid": it["spid"], "error": str(e)[:120]}

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(done, f, ensure_ascii=False)
log("DONE total=%d" % len(done))
print("DONE", len(done))
