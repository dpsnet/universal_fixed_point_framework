# -*- coding: utf-8 -*-
"""R3k2：targetid_not_found 诊断——检查 COADD_TARGETID / 其他列匹配"""
import io, json, os, sys
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
g2n = {str(s["gaia_int"]): s["desi_name"] for s in cat["samples"]}
with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "r", encoding="utf-8") as f:
    done = json.load(f)

# 找 targetid_not_found 星
miss = [(it, g2n[it["gaia_int"]]) for it in manifest if done.get(it["gaia_int"], {}).get("why") == "targetid_not_found"]
print("not_found:", len(miss))
for it, desi in miss[:3]:
    print("---", it["gaia_int"], "desi=", desi, it["url"][:80])
    try:
        d = DesiCoadd(it["url"])
        tid = d.col("FIBERMAP", "TARGETID")
        print("nrows:", len(tid), "TARGETID contains desi:", bool(np.any(tid == int(desi))))
        try:
            ctid = d.col("FIBERMAP", "COADD_TARGETID")
            print("COADD_TARGETID contains desi:", bool(np.any(ctid == int(desi))))
        except Exception as e:
            print("COADD_TARGETID col fail:", str(e)[:80])
        # 打印前 3 个 TARGETID 和 COADD_TARGETID 样本
        print("sample TARGETID:", tid[:3].tolist())
        try:
            print("sample COADD:", ctid[:3].tolist())
        except Exception:
            pass
    except Exception as e:
        print("open fail:", str(e)[:120])
