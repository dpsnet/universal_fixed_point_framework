# -*- coding: utf-8 -*-
"""Phase 104az-47：检查各线级 JSON 结构（DESI/Kepler/强场 v10int）"""
import json

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
for fn in ["paperX_wd_linelevel_v10int.json", "paperX_wd_linelevel_mid_full_snr.json",
           "paperX_wd_linelevel_weak_sdss_snr.json", "paperX_wd_kepler_linelevel.json",
           "paperX_wd_linelevel_strong.json"]:
    try:
        d = json.load(open(BASE + "\\" + fn, encoding="utf-8"))
        print("== %s : %d recs ==" % (fn, len(d)))
        if d:
            r0 = d[0]
            print("   keys:", list(r0.keys()))
            # 找含线的记录
            import collections
            n_hasline = 0
            for r in d:
                if isinstance(r, dict) and any(k.startswith("H") and "d_pure" in str(v) for k, v in r.items()):
                    n_hasline += 1
                elif isinstance(r, dict) and "lines" in r:
                    n_hasline += 1
            print("   has lines:", n_hasline)
            s = json.dumps(r0, ensure_ascii=False)[:300]
            print("   sample:", s)
    except Exception as e:
        print("== %s : ERR %s" % (fn, e))
