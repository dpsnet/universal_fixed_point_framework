# -*- coding: utf-8 -*-
"""Phase 99 M99-3c：全量下载 LAMOST 光谱（152 颗命中，每组 10 颗）
从 crossmatch_fixed.json 取每星最近（dist 最小）obsid
解包到 scripts\_lamost_spec\{obsid}.fits
"""
import json, io, os, re, time, tarfile, gzip
import requests

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
SPEC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_lamost_spec"
os.makedirs(SPEC, exist_ok=True)
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def get_csrf():
    r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    return m.group(1) if m else None

def pick(grp):
    """每星最近命中 -> (obsid, snrr, dist)"""
    out = {}
    for g in grp:
        if not g["lamost"]:
            continue
        best = min(g["lamost"], key=lambda r: float(r.get("dist_arcsec", 1e9) or 1e9))
        out[g["name"]] = {"obsid": best["obsid"], "snrr": float(best.get("snrr", 0) or 0),
                          "dist": float(best.get("dist_arcsec", 0) or 0),
                          "cls": best.get("class", "?"), "B_MG": g["B_MG"]}
    return out

def download_batch(csrf, obsids):
    url = "https://www.lamost.org/dr11/v2.0/spectrum/tar?type=fits"
    r = S.post(url, data={"obsid": ",".join(obsids), "csrf_token": csrf}, timeout=120)
    if r.headers.get("Content-Type", "").startswith("application/x-tar"):
        return r.content
    print("  batch ERR:", r.content[:150].decode("utf-8", "replace"), flush=True)
    return None

if __name__ == "__main__":
    j = json.load(open(BASE + r"\paperX_lamost_crossmatch_fixed.json", encoding="utf-8"))
    picks = {}
    for key in ("mid", "weak"):
        picks.update(pick(j[key]))
    print("总命中（最近匹配）: %d" % len(picks), flush=True)
    items = list(picks.items())
    csrf = get_csrf()
    n_ok = 0
    for i in range(0, len(items), 10):
        chunk = items[i:i + 10]
        obsids = [v["obsid"] for _, v in chunk]
        tar = download_batch(csrf, obsids)
        if tar:
            tf = tarfile.open(fileobj=io.BytesIO(tar))
            for nm in tf.getnames():
                if nm.endswith(".fits.gz"):
                    base = os.path.basename(nm).replace(".fits.gz", "")
                    data = tf.extractfile(nm).read()
                    try:
                        raw = gzip.decompress(data)
                        with open(os.path.join(SPEC, base + ".fits"), "wb") as fh:
                            fh.write(raw)
                        n_ok += 1
                    except Exception as e:
                        print("  gunzip ERR", nm, e, flush=True)
        print("批 %d/%d 完成（累计 OK=%d）" % (i // 10 + 1, (len(items) + 9) // 10, n_ok), flush=True)
        time.sleep(0.5)
    print("全部完成: 有效 FITS %d/%d" % (n_ok, len(items)), flush=True)
