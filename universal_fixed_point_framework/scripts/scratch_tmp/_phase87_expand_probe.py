# -*- coding: utf-8 -*-
"""Phase 87 M87-7a：中场样本扩容探查——各目录中场（10-100 MG）可用星数"""
import io, json, os, sys, glob
import numpy as np
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)

# 1) DESI 137 全样本中场统计（不限 Teff）
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)
mid_all = [s for s in cat if 10 <= s["B_MG"] < 100]
mid_ok = [s for s in mid_all if str(s["gaia_int"]) in ew0 and ew0[str(s["gaia_int"])].get("ok")]
print("DESI137 中场(B 10-100)全部: %d | EW ok: %d" % (len(mid_all), len(mid_ok)))
for s in sorted(mid_all, key=lambda x: x["B_MG"]):
    ok = str(s["gaia_int"]) in ew0 and ew0[str(s["gaia_int"])].get("ok")
    print("  B=%6.1f Teff=%6.0f logg=%.2f ok=%s" % (s["B_MG"], s["Teff"], s["logg"], ok))

# 2) Amorim 目录（M83c）中场星——星表与光谱缓存
# 找 M83c 相关 json
for pat in ("paperX_wd_m83c*.json", "paperX_wd_amorim*.json", "*m83c*.json"):
    for f in glob.glob(os.path.join(BASE, pat)):
        print("found:", os.path.basename(f))
