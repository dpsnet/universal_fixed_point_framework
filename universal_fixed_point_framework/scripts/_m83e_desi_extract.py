# -*- coding: utf-8 -*-
"""R3i：DESI 137 目录光谱批量提取（HTTP Range 按需读取）
- 对 manifest 中每颗：读 FIBERMAP TARGETID → 定位行号 → 读 B_WAVELENGTH + B_FLUX[row] + B_IVAR[row]
- 保存每颗 (wave, flux, ivar) 到 _desi_spec/{gaia_int}.npz + 汇总 json
- 先小批量验证（--test N 颗）
用法: python _m83e_desi_extract.py [--test N]"""
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
# gaia_int -> desi_name
g2n = {str(s["gaia_int"]): s["desi_name"] for s in cat["samples"]}
# 已提取记录（增量）
rec_path = os.path.join(BASE, "_m83e_desi_extracted.json")
done = {}
if os.path.exists(rec_path):
    with io.open(rec_path, "r", encoding="utf-8") as f:
        done = json.load(f)

SPECDIR = os.path.join(BASE, "_desi_spec")
os.makedirs(SPECDIR, exist_ok=True)

def extract_one(item):
    gid = item["gaia_int"]
    url = item["url"]
    target = int(g2n[gid])
    t0 = time.time()
    d = DesiCoadd(url)
    hdr_t = time.time() - t0
    tid = d.col("FIBERMAP", "TARGETID")
    rows = np.where(tid == target)[0]
    if len(rows) == 0:
        return {"gaia_int": gid, "ok": False, "why": "targetid_not_found",
                "nrows": len(tid), "sample_tid": int(tid[0]) if len(tid) else None}
    row = int(rows[0])
    wave = d.image_all("B_WAVELENGTH")
    flux = d.image_row("B_FLUX", row)
    ivar = d.image_row("B_IVAR", row)
    np.savez(os.path.join(SPECDIR, "%s.npz" % gid), wave=wave, flux=flux, ivar=ivar)
    return {"gaia_int": gid, "ok": True, "row": row, "nrows": len(tid),
            "wave0": float(wave[0]), "wave1": float(wave[-1]), "nwave": int(len(wave)),
            "t": round(hdr_t, 2)}

def main():
    test = None
    if "--test" in sys.argv:
        test = int(sys.argv[sys.argv.index("--test") + 1])
    items = manifest[:test] if test else manifest
    ok_n = 0
    for i, item in enumerate(items):
        gid = item["gaia_int"]
        if gid in done and done[gid].get("ok"):
            continue
        try:
            r = extract_one(item)
        except Exception as e:
            r = {"gaia_int": gid, "ok": False, "why": "err:" + str(e)[:120]}
        done[gid] = r
        if r["ok"]:
            ok_n += 1
        print("%d/%d %s ok=%s %s" % (i + 1, len(items), gid, r["ok"], r.get("why", "")), flush=True)
        if not r["ok"]:
            continue
        # 每 5 颗增量落盘
        if (i + 1) % 5 == 0:
            with io.open(rec_path, "w", encoding="utf-8") as f:
                json.dump(done, f, ensure_ascii=False)
    with io.open(rec_path, "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False)
    print("DONE ok=%d/%d" % (ok_n, len(items)))

if __name__ == "__main__":
    main()
