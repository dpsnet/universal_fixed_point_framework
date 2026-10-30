# -*- coding: utf-8 -*-
"""Phase 104az-47b：检查线级 JSON 顶层结构"""
import json

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
for fn in ["paperX_wd_linelevel_v10int.json", "paperX_wd_linelevel_mid_full_snr.json",
           "paperX_wd_linelevel_weak_sdss_snr.json", "paperX_wd_kepler_linelevel.json",
           "paperX_wd_linelevel_strong.json", "paperX_wd_linelevel.json"]:
    try:
        d = json.load(open(BASE + "\\" + fn, encoding="utf-8"))
        if isinstance(d, dict):
            print("== %s : dict keys(%d) ==" % (fn, len(d)))
            ks = list(d.keys())[:12]
            print("   keys:", ks)
            k0 = ks[0] if ks else None
            if k0 is not None:
                v0 = d[k0]
                print("   first val type:", type(v0).__name__)
                print("   first val:", json.dumps(v0, ensure_ascii=False)[:250])
        else:
            print("== %s : list %d ==" % (fn, len(d)))
    except Exception as e:
        print("== %s : ERR %s" % (fn, e))
