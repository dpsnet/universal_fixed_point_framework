# -*- coding: utf-8 -*-
"""Phase 87 M87-7d 修正版：按 nearest 网格点检查/下载缺失 Koester 模型谱"""
import io, json, os, glob, time, urllib.request
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
SPEC = os.path.join(BASE, "_koester_spec")

with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83c_fid_table.json"), "r", encoding="utf-8") as f:
    fid_tbl = json.load(f)
grid = {}
for k, v in fid_tbl.items():
    t, g = k.split("_")
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid)); loggs = sorted(set(g for t, g in grid))
def nearest(teff, logg):
    return min(teffs, key=lambda x: abs(x - teff)), min(loggs, key=lambda x: abs(x - logg))

have = set(os.path.basename(p) for p in glob.glob(os.path.join(SPEC, "fid*.dat")))

# 主档 8-25kK 中场星
mid = []
for s in cat:
    gid = str(s["gaia_int"])
    if gid not in ew0 or not ew0[gid].get("ok"):
        continue
    if not (8000 <= s["Teff"] <= 25000):
        continue
    if 10 <= s["B_MG"] < 100:
        mid.append(s)

missing = []
for s in mid:
    t, g = nearest(s["Teff"], s["logg"])
    fid = grid.get((t, g))
    fname = "fid%s_%s_%s.dat" % (fid, t, g)
    if fname in have:
        continue
    missing.append((s, t, g, fid, fname))

print("中场: %d | 缓存缺: %d" % (len(mid), len(missing)))
for s, t, g, fid, fname in missing:
    print("  缺 fid=%s Teff=%d(网格%s) logg=%s B=%.1f MG -> %s" % (fid, s["Teff"], t, g, s["B_MG"], fname))

def get(url, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

ok = 0
for s, t, g, fid, fname in missing:
    url = 'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=koester2&fid=%s&format=ascii' % fid
    try:
        st, body = get(url)
        if st != 200 or len(body) < 1000:
            print("!! 下载失败 fid=%s st=%d len=%d" % (fid, st, len(body)))
            continue
        with io.open(os.path.join(SPEC, fname), "w", encoding="utf-8") as f:
            f.write(body)
        ok += 1
        print("ok %s (%d bytes)" % (fname, len(body)))
        time.sleep(1.5)
    except Exception as e:
        print("!! 下载异常 fid=%s: %r" % (fid, e))
print("downloaded %d" % ok)
