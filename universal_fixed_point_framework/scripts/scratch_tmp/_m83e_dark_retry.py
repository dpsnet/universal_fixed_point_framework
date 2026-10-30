# -*- coding: utf-8 -*-
"""R3k3：not_found 星 → 探测同 hp dark 版本 coadd 并提取"""
import io, json, os, sys, time
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
import importlib.util
spec = importlib.util.spec_from_file_location("r", os.path.join(BASE, "_m83e_desi_reader.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
DesiCoadd = m.DesiCoadd

import requests
with io.open(os.path.join(BASE, "_m83e_desi_manifest.json"), "r", encoding="utf-8") as f:
    manifest = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)
g2n = {str(s["gaia_int"]): s["desi_name"] for s in cat["samples"]}
with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "r", encoding="utf-8") as f:
    done = json.load(f)

SPECDIR = os.path.join(BASE, "_desi_spec")
miss = [it for it in manifest if not done.get(it["gaia_int"], {}).get("ok")]
print("missing:", len(miss))

def head_ok(url):
    try:
        r = requests.head(url, timeout=30)
        return r.status_code == 200
    except Exception:
        return False

newok = 0
for it in miss:
    gid = it["gaia_int"]
    desi = g2n[gid]
    # 构造 dark 版本（bright->dark；若已是 dark 跳过）
    url = it["url"]
    if "/bright/" in url:
        dark_url = url.replace("/bright/", "/dark/")
    else:
        dark_url = url
    if dark_url == url or not head_ok(dark_url):
        # 尝试 sv1 版本（iron 之外）? 先记录
        print("%s no dark alt" % gid, flush=True)
        continue
    try:
        d = DesiCoadd(dark_url)
        tid = d.col("FIBERMAP", "TARGETID")
        rows = np.where(tid == int(desi))[0]
        if len(rows) == 0:
            print("%s dark also no match (nrows=%d)" % (gid, len(tid)), flush=True)
            continue
        row = int(rows[0])
        wave = d.image_all("B_WAVELENGTH")
        flux = d.image_row("B_FLUX", row)
        ivar = d.image_row("B_IVAR", row)
        np.savez(os.path.join(SPECDIR, "%s.npz" % gid), wave=wave, flux=flux, ivar=ivar)
        done[gid] = {"gaia_int": gid, "ok": True, "row": row, "prog": "dark",
                     "wave0": float(wave[0]), "wave1": float(wave[-1]), "nwave": int(len(wave))}
        newok += 1
        print("%s DARK OK row=%d" % (gid, row), flush=True)
    except Exception as e:
        print("%s dark err %s" % (gid, str(e)[:100]), flush=True)
    with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False)

print("new ok:", newok, "/", len(miss))
