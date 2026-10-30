# -*- coding: utf-8 -*-
"""R3f：HEAD 探测 114 颗星的 coadd 文件（bright/dark），生成下载清单"""
import io, json, os, requests

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_hp.json"), "r", encoding="utf-8") as f:
    hp_map = json.load(f)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
manifest = []   # {gaia_int, hp, prog, size, url}
miss_any = []
for k, hp in hp_map.items():
    prog = None
    size = None
    for p in ["bright", "dark"]:
        url = ("https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/%s/%d/%d/coadd-main-%s-%d.fits"
               % (p, hp // 100, hp, p, hp))
        try:
            r = requests.head(url, headers=UA, timeout=20)
            if r.status_code == 200:
                prog = p
                size = int(r.headers.get("Content-Length", 0))
                manifest.append({"gaia_int": k, "hp": hp, "prog": p, "size": size, "url": url})
                break
        except Exception as e:
            print("ERR", k, str(e)[:80])
    if prog is None:
        miss_any.append(k)
        print("NOFILE", k, "hp", hp)

print("manifest:", len(manifest), "of", len(hp_map), "| missing:", len(miss_any))
tot = sum(m["size"] for m in manifest) / 1e9
print("total size ~%.2f GB" % tot)
with io.open(os.path.join(BASE, "_m83e_desi_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False)
print("saved manifest")
