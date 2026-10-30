# -*- coding: utf-8 -*-
"""解析 Amorim 全表 Sp-ID；筛 236 有效集（obs_EW>0 且有 koester_EW）；输出待下载清单。"""
import io, json, os, re

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
TSV = os.path.join(BASE, "_amorim_full.tsv")

# 1) 解析 TSV：找到数据行（以 "J" 开头？）——列：SDSS | Sp-ID | Mstar | Teff | TSDSS | B ...
rows = []
with io.open(TSV, "r", encoding="utf-8") as f:
    for ln in f:
        if ln.startswith("#") or not ln.strip():
            continue
        parts = ln.rstrip("\n").split("\t")
        rows.append(parts)

print("data rows:", len(rows))
for r in rows[:2]:
    print("SAMPLE:", r[:8])
# 确认列序
print("first row len:", len(rows[0]))

# 建 SDSS 名 -> Sp-ID 映射
name2spid = {}
for r in rows:
    if len(r) < 2:
        continue
    nm = r[0].strip()
    sp = r[1].strip() if len(r) > 1 else ""
    if nm.startswith("J") and sp:
        name2spid[nm] = sp
print("name2spid size:", len(name2spid))

# 2) 236 有效集：obs_EW>0 且有 koester_EW
with io.open(os.path.join(BASE, "paperX_wd_m83c_sample_list.json"), "r", encoding="utf-8") as f:
    lst = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83c_koester_ew.json"), "r", encoding="utf-8") as f:
    ko = json.load(f)

ko_by_name = {}
for s in ko.get("samples", []):
    nm = s.get("name") or s.get("sdss")
    if nm:
        ko_by_name[nm] = s

valid = []
for r in lst:
    if r.get("obs_EW", 0) > 0 and r["name"] in ko_by_name:
        valid.append(r)
print("valid(236?) n =", len(valid))

# 3) 输出待下载清单（name, Sp-ID, B, Teff, logg, obs_EW, src）
out = []
miss = 0
for r in valid:
    sp = name2spid.get(r["name"], "")
    if not sp:
        miss += 1
    out.append({"name": r["name"], "spid": sp, "B": r["B_tesla"], "Teff": r["Teff"], "logg": r["logg"], "obs_EW": r["obs_EW"], "src": r["src"]})
print("with Sp-ID:", len(out) - miss, "missing Sp-ID:", miss)

with io.open(os.path.join(BASE, "_snr_dl_list.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved _snr_dl_list.json n=", len(out))
