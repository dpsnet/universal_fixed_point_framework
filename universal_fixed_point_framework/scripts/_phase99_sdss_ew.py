# -*- coding: utf-8 -*-
"""Phase 99 延伸-6：SDSS 全历元局部归一化 EW 重测（论文口径复核）
- 按论文表 5.2 的 plate-mjd-fiber 显式下载
- 局部连续谱（线中心±60/±20Å 旁瓣）归一化，积分 EW（负=发射）
"""
import numpy as np
from astroquery.sdss import SDSS

# (label, plate, mjd, fiber, 蓝端)
SPECS = [
    ("J233817 6161-56238-622", 6161, 56238, 622),
    ("J233817 2628-54326-171", 2628, 54326, 171),
    ("J233817 2622-54095-174", 2622, 54095, 174),
    ("J225828 6293-56561-264", 6293, 56561, 264),
    ("J225828 7768-58289-50",  7768, 58289, 50),
    ("J225828 7768-58289-44",  7768, 58289, 44),
    ("J101712 6458-56274-968", 6458, 56274, 968),
    ("J101712 6458-56274-962", 6458, 56274, 962),
    ("J101712 2346-53734-97",  2346, 53734, 97),
]

BAL = {"Hbeta": 4861.3, "Hgamma": 4340.5, "Hdelta": 4101.7,
       "Heps": 3970.1, "Hzeta": 3889.0, "Heta": 3835.4}

def ew_local(wl, fl, c):
    """局部连续谱归一化 + 积分 EW（Å，负=发射）"""
    core = (wl > c - 10) & (wl < c + 10)
    cont = ((wl > c - 60) & (wl < c - 20)) | ((wl > c + 20) & (wl < c + 60))
    if core.sum() < 3 or cont.sum() < 10:
        return None
    base = np.median(fl[cont])
    if base <= 0 or not np.isfinite(base):
        return None
    r = fl[core] / base - 1.0
    # 用波长差做积分步长
    dwl = np.diff(wl[core])
    ew = np.sum(r[:-1] * dwl)
    return ew, base

for label, plate, mjd, fiber in SPECS:
    try:
        sp = SDSS.get_spectra(plate=plate, fiberID=fiber, mjd=mjd)[0]
        wl = 10 ** sp[1].data["loglam"]
        fl = sp[1].data["flux"]
        wl0 = wl[0]
        out = []
        for lab, c in BAL.items():
            r = ew_local(wl, fl, c)
            if r is None:
                continue
            ew, base = r
            if ew > 1.5:
                tag = "ABS+%.1f" % ew
            elif ew < -1.0:
                tag = "EM-%.1f" % (-ew)
            elif ew > 0.3:
                tag = "abs+%.1f" % ew
            elif ew < -0.3:
                tag = "em-%.1f" % (-ew)
            else:
                tag = "flat(%.1f)" % ew
            out.append("%s %s" % (lab, tag))
        print("%s [蓝端 %.0f]:" % (label, wl0), " | ".join(out), flush=True)
    except Exception as e:
        print("%s ERR %s" % (label, str(e)[:90]), flush=True)
