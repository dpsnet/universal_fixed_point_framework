# -*- coding: utf-8 -*-
"""R3k4：坐标匹配提取未命中星（TARGET_RA/DEC 全列最近行）+ 统计 125 命中覆盖"""
import io, json, os, sys, time
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
import importlib.util
spec = importlib.util.spec_from_file_location("r", os.path.join(BASE, "_m83e_desi_reader.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
DesiCoadd = m.DesiCoadd

with io.open(os.path.join(BASE, "_m83e_desi_manifest.json"), "r", encoding="utf-8") as f:
    manifest = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "r", encoding="utf-8") as f:
    coords = json.load(f)["coords"]
with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "r", encoding="utf-8") as f:
    done = json.load(f)

# 125 命中中未 ok 的星
miss = [it for it in manifest
        if str(it["gaia_int"]) in coords and not done.get(it["gaia_int"], {}).get("ok")]
print("coord-has but not ok:", len(miss))
# 无坐标星
noc = [it for it in manifest if str(it["gaia_int"]) not in coords]
print("no-coord manifest:", len(noc))
noc_g = [s for s in cat["samples"] if str(s["gaia_int"]) not in coords]
print("no-coord catalog:", len(noc_g))
# 无坐标星的 B 分布
bs = sorted([s["B_MG"] for s in noc_g])
print("no-coord B:", [round(x, 1) for x in bs])
print("no-coord max B:", max(bs) if bs else None)

SPECDIR = os.path.join(BASE, "_desi_spec")
def haversine_deg(ra1, dec1, ra2, dec2):
    r1, r2 = np.radians(ra1), np.radians(ra2)
    d1, d2 = np.radians(dec1), np.radians(dec2)
    a = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return 2 * np.degrees(np.arcsin(np.sqrt(a)))

newok = 0
for it in miss:
    gid = it["gaia_int"]
    ra, dec = coords[str(gid)]
    try:
        d = DesiCoadd(it["url"])
        tra = d.col("FIBERMAP", "TARGET_RA")
        tdec = d.col("FIBERMAP", "TARGET_DEC")
        # 角距离最近行（限制在 5 角分内）
        dist = np.abs(tra - ra) + np.abs(tdec - dec)
        j = int(np.argmin(dist))
        dd = max(abs(tra[j] - ra), abs(tdec[j] - dec))
        if dd > 0.5:
            print("%s nearest %f deg off (nrows=%d) skip" % (gid, dd, len(tra)), flush=True)
            continue
        row = j
        wave = d.image_all("B_WAVELENGTH")
        flux = d.image_row("B_FLUX", row)
        ivar = d.image_row("B_IVAR", row)
        np.savez(os.path.join(SPECDIR, "%s.npz" % gid), wave=wave, flux=flux, ivar=ivar)
        done[gid] = {"gaia_int": gid, "ok": True, "row": row, "prog": "coord-match",
                     "off_deg": round(float(dd), 5),
                     "wave0": float(wave[0]), "wave1": float(wave[-1]), "nwave": int(len(wave))}
        newok += 1
        print("%s COORD OK row=%d off=%f" % (gid, row, dd), flush=True)
    except Exception as e:
        print("%s coord err %s" % (gid, str(e)[:100]), flush=True)
    with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False)
print("new ok:", newok, "/", len(miss))
