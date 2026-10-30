# -*- coding: utf-8 -*-
"""R3k5：剩余星补提取
A) 14 颗新坐标命中（错 ID 修正后，不在 manifest）：算 hp → HEAD 探测 → 提取
B) 6 颗超阈值星：坐标重算 hp → 新文件 → 提取（TARGETID 匹配优先，坐标兜底）"""
import io, json, os, sys, time
import numpy as np
import requests

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
import importlib.util
spec = importlib.util.spec_from_file_location("r", os.path.join(BASE, "_m83e_desi_reader.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
DesiCoadd = m.DesiCoadd

try:
    import astropy_healpix as ah
    import astropy.units as u
    HAS_AH = True
except Exception as e:
    HAS_AH = False
    print("no astropy_healpix:", e)

def hp_of(ra, dec):
    if HAS_AH:
        return int(ah.lonlat_to_healpix(ra * u.deg, dec * u.deg, nside=64, order="nested"))
    # 兜底：nested nside=64 计算（ring->nested）
    import math
    nside = 64
    # ring 编号
    theta = math.radians(90.0 - dec)
    phi = math.radians(ra)
    z = math.cos(theta)
    nside2 = 2 * nside
    if z >= 1:
        ipring = 0
    elif z <= -1:
        ipring = 12 * nside * nside - 1
    else:
        tt = math.acos(z)
        jp = int(math.floor(nside * (0.5 + phi / (2 * math.pi))))
        jm = int(math.floor(nside * (0.5 - tt / math.pi)))
        k = (jp + jm) % (2 * nside)
        jr = (jp - jm) // 2 + nside
        if k >= nside:
            if (jr & 1) == 0:
                ip = 2 * nside * (2 * nside - 1) - (k - nside) * (2 * jr + 1) + jp - jr
            else:
                ip = 2 * nside * (2 * nside - 1) - (k - nside) * (2 * jr + 1) + jp
        else:
            if (jr & 1) == 0:
                ip = 2 * nside * jr + k * (2 * jr + 1) + jp
            else:
                ip = 2 * nside * (jr - nside) + k * (2 * jr - 1) + jp
        ipring = int(ip)
    # ring -> nested（反向比特交织，简化：用内置转换不可用时的查表法不做，直接返回 ring 兜底）
    return ipring

with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "r", encoding="utf-8") as f:
    coords = json.load(f)["coords"]
with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "r", encoding="utf-8") as f:
    done = json.load(f)
with io.open(os.path.join(BASE, "_m83e_desi_manifest.json"), "r", encoding="utf-8") as f:
    manifest = json.load(f)
man_gids = {it["gaia_int"] for it in manifest}

SPECDIR = os.path.join(BASE, "_desi_spec")

def head_ok(url):
    try:
        r = requests.head(url, timeout=30)
        return r.status_code == 200
    except Exception:
        return False

def url_for(hp, prog="bright"):
    g = hp // 100
    return ("https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/%s/%d/%d/coadd-main-%s-%d.fits"
            % (prog, g, hp, prog, hp))

# A) 新命中且未在 manifest 的星
newok = 0
targets = []
for s in cat["samples"]:
    gid = str(s["gaia_int"])
    if gid not in coords:
        continue
    if gid in man_gids:
        continue  # 已在 manifest
    targets.append((gid, s["desi_name"], coords[gid]))
print("A) new-hit no-manifest:", len(targets))
for gid, desi, (ra, dec) in targets:
    hp = hp_of(ra, dec)
    url = None
    for prog in ("bright", "dark"):
        u0 = url_for(hp, prog)
        if head_ok(u0):
            url = u0
            break
    if url is None:
        print("A %s no file hp=%d" % (gid, hp), flush=True)
        continue
    try:
        d = DesiCoadd(url)
        tid = d.col("FIBERMAP", "TARGETID")
        rows = np.where(tid == int(desi))[0]
        if len(rows) == 0:
            tra = d.col("FIBERMAP", "TARGET_RA")
            tdec = d.col("FIBERMAP", "TARGET_DEC")
            dist = np.abs(tra - ra) + np.abs(tdec - dec)
            j = int(np.argmin(dist))
            if max(abs(tra[j] - ra), abs(tdec[j] - dec)) > 0.3:
                print("A %s no match in hp %d (nrows=%d)" % (gid, hp, len(tra)), flush=True)
                continue
            row = j
        else:
            row = int(rows[0])
        wave = d.image_all("B_WAVELENGTH")
        flux = d.image_row("B_FLUX", row)
        ivar = d.image_row("B_IVAR", row)
        np.savez(os.path.join(SPECDIR, "%s.npz" % gid), wave=wave, flux=flux, ivar=ivar)
        done[gid] = {"gaia_int": gid, "ok": True, "row": row, "prog": prog, "hp": hp,
                     "wave0": float(wave[0]), "wave1": float(wave[-1]), "nwave": int(len(wave))}
        newok += 1
        print("A %s OK hp=%d row=%d" % (gid, hp, row), flush=True)
    except Exception as e:
        print("A %s err %s" % (gid, str(e)[:100]), flush=True)
    with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False)

# B) manifest 中仍未 ok 且有坐标的（超阈值）
bmiss = [it for it in manifest
         if str(it["gaia_int"]) in coords and not done.get(it["gaia_int"], {}).get("ok")]
print("B) still-miss with coord:", len(bmiss))
g2n = {str(s["gaia_int"]): s["desi_name"] for s in cat["samples"]}
for it in bmiss:
    gid = it["gaia_int"]
    desi = g2n[gid]
    ra, dec = coords[str(gid)]
    hp = hp_of(ra, dec)
    if hp == it.get("hp", -1):
        print("B %s same hp skip" % gid, flush=True)
        continue
    url = None
    for prog in ("bright", "dark"):
        u0 = url_for(hp, prog)
        if head_ok(u0):
            url = u0
            break
    if url is None:
        print("B %s no file hp=%d" % (gid, hp), flush=True)
        continue
    try:
        d = DesiCoadd(url)
        tid = d.col("FIBERMAP", "TARGETID")
        rows = np.where(tid == int(desi))[0]
        if len(rows) == 0:
            tra = d.col("FIBERMAP", "TARGET_RA")
            tdec = d.col("FIBERMAP", "TARGET_DEC")
            dist = np.abs(tra - ra) + np.abs(tdec - dec)
            j = int(np.argmin(dist))
            if max(abs(tra[j] - ra), abs(tdec[j] - dec)) > 0.3:
                print("B %s no match hp %d" % (gid, hp), flush=True)
                continue
            row = j
        else:
            row = int(rows[0])
        wave = d.image_all("B_WAVELENGTH")
        flux = d.image_row("B_FLUX", row)
        ivar = d.image_row("B_IVAR", row)
        np.savez(os.path.join(SPECDIR, "%s.npz" % gid), wave=wave, flux=flux, ivar=ivar)
        done[gid] = {"gaia_int": gid, "ok": True, "row": row, "prog": prog, "hp": hp,
                     "wave0": float(wave[0]), "wave1": float(wave[-1]), "nwave": int(len(wave))}
        newok += 1
        print("B %s OK hp=%d row=%d" % (gid, hp, row), flush=True)
    except Exception as e:
        print("B %s err %s" % (gid, str(e)[:100]), flush=True)
    with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False)

print("A+B new ok:", newok)
# 最终统计
with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "r", encoding="utf-8") as f:
    done = json.load(f)
ok = sum(1 for v in done.values() if v.get("ok"))
print("total ok:", ok)
