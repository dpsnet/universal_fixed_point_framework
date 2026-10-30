# -*- coding: utf-8 -*-
import io, json, os, sys
import numpy as np
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
with io.open(os.path.join(BASE, "paperX_wd_m83c_fid_table.json"), "r", encoding="utf-8") as f:
    fid_tbl = json.load(f)
grid = {}
for k, v in fid_tbl.items():
    t, g = k.split("_")
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid)); loggs = sorted(set(g for t, g in grid))

cache = os.path.join(BASE, "_koester_spec")
fnames = set(os.listdir(cache))
def load_koester(teff, logg):
    t = min(teffs, key=lambda x: abs(x - teff))
    g = min(loggs, key=lambda x: abs(x - logg))
    fid = grid.get((t, g))
    if fid is None:
        return None
    fp = os.path.join(cache, "fid%s_%s_%s.dat" % (fid, t, g))
    return fp if os.path.exists(fp) else None

with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)

ok = [s for s in cat if str(s["gaia_int"]) in ew0 and ew0[str(s["gaia_int"])].get("ok")]
main = [s for s in ok if 10000 <= s["Teff"] <= 20000]
weak = [s for s in main if s["B_MG"] < 10]
mid = [s for s in main if 10 <= s["B_MG"] < 100]
print("ok=%d main=%d weak=%d mid=%d" % (len(ok), len(main), len(weak), len(mid)))

ko = sum(1 for s in main if load_koester(s["Teff"], s["logg"]))
print("main Koester cache hit: %d/%d" % (ko, len(main)))
for s in mid:
    fp = os.path.join(BASE, "_desi_spec", str(s["gaia_int"]) + ".npz")
    kp = load_koester(s["Teff"], s["logg"])
    print("mid star gid=%s B=%.1f Teff=%.0f logg=%.2f | npz=%s koester=%s" % (
        s["gaia_int"], s["B_MG"], s["Teff"], s["logg"],
        os.path.exists(fp), kp is not None))
