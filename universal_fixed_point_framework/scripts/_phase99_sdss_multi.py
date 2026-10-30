# -*- coding: utf-8 -*-
"""Phase 99 延伸-5c：SDSS 多历元发射线（specObjID 方式 + 扩大窗口）"""
import numpy as np
from astroquery.sdss import SDSS

TARGETS = {
    "J233817.93+083732.6": (354.5747, 8.6257),
    "J225828.48+280828.8": (344.6187, 28.1413),
    "J101712.60+233646.6": (154.3025, 23.6129),
}

def check_emission(wl, fl, c, win=8.0, base=20.0):
    mc = (wl > c - win) & (wl < c + win)
    mb = ((wl > c - base) & (wl < c - win)) | ((wl > c + win) & (wl < c + base))
    if mc.sum() < 2 or mb.sum() < 4:
        return None
    pk = np.median(fl[mc])
    bg = np.median(fl[mb])
    return pk, bg

for name, (ra, dec) in TARGETS.items():
    print("== %s ==" % name, flush=True)
    sql = ("SELECT plate, mjd, fiberID, specObjID, ra, dec FROM specObj "
           "WHERE ra BETWEEN %.4f AND %.4f AND dec BETWEEN %.4f AND %.4f"
           % (ra - 0.02, ra + 0.02, dec - 0.02, dec + 0.02))
    try:
        res = SDSS.query_sql(sql)
        if res is None or len(res) == 0:
            print("  无 specObj（0.04° 方窗）", flush=True)
            continue
        print("  找到 %d 条光谱" % len(res), flush=True)
        for row in res:
            plate = int(row["plate"]); mjd = int(row["mjd"]); fiber = int(row["fiberID"])
            soid = int(row["specObjID"])
            try:
                sp = SDSS.get_spectra(plate=plate, fiberID=fiber, mjd=mjd)[0]
                wl = 10 ** sp[1].data["loglam"]
                fl = sp[1].data["flux"]
                mcont = (wl > 5000) & (wl < 5600)
                med = np.median(fl[mcont])
                if not np.isfinite(med) or med <= 0:
                    print("  %s-%s-%s 归一化失败" % (plate, mjd, fiber), flush=True)
                    continue
                fln = fl / med
                feats = []
                for lab, c in (("Hbeta", 4861.3), ("Hdelta", 4101.7), ("Hzeta", 3889.0), ("Heta", 3835.4)):
                    r = check_emission(wl, fln, c)
                    if r:
                        pk, bg = r
                        tag = "EM" if pk > bg * 1.05 else ("ABS" if pk < bg * 0.95 else "flat")
                        feats.append("%s=%.2f/%.2f(%s)" % (lab, pk, bg, tag))
                wl0 = wl[0]
                print("  %s-%s-%s (蓝端 %.0f): %s" % (plate, mjd, fiber, wl0, " | ".join(feats)), flush=True)
            except Exception as e:
                print("  %s-%s-%s ERR %s" % (plate, mjd, fiber, str(e)[:90]), flush=True)
    except Exception as e:
        print("  SQL ERR", str(e)[:100], flush=True)
