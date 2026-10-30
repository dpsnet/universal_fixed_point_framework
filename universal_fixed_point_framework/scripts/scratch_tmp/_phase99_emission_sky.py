# -*- coding: utf-8 -*-
"""Phase 99 延伸-2：3 颗发射线星样本归属 + LAMOST 天区覆盖"""
import json, re, io, os, time
import requests

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
targets = {
    "J233817.93+083732.6": (354.5747, 8.6257, 12.0),
    "J225828.48+280828.8": (344.6187, 28.1413, 14.0),
    "J101712.60+233646.6": (154.3025, 23.6129, 14.0),
}

# 1) 检查是否在 mid_full_snr（Amorim 中场 SDSS 全样本）与 weak 样本
mid = json.load(open(BASE + r"\paperX_wd_linelevel_mid_full_snr.json", encoding="utf-8"))["mid_full"]
wk = json.load(open(BASE + r"\paperX_wd_linelevel_weak_sdss_snr.json", encoding="utf-8"))["weak_sdss"]
names_mid = [s["name"] for s in mid]
names_wk = [s["name"] for s in wk]
print("mid 样本 n=%d, weak 样本 n=%d" % (len(names_mid), len(names_wk)))
for t in targets:
    print("%s: mid=%s weak=%s" % (t, t in names_mid, t in names_wk))

# 2) LAMOST cone 覆盖查询
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
csrf = m.group(1) if m else None
print("\n== LAMOST cone 120\" 查询 3 颗发射线星 ==")
for t, (ra, dec, b) in targets.items():
    data = {"csrf_token": csrf, "pos_group": "ra,dec", "pos.type": "cone",
            "pos.racenter": "%.7f" % ra, "pos.deccenter": "%.7f" % dec,
            "pos.radius": "120", "output.fmt": "csv",
            "showcol": ["combined.obsid", "combined.planid", "combined.spid",
                        "combined.fiberid", "combined.class", "combined.snrr",
                        "combined.ra", "combined.dec"]}
    try:
        rr = S.post("https://www.lamost.org/dr11/v2.0/table/combined/q", data=data, timeout=45)
        lines = [l for l in rr.text.strip().splitlines() if l.strip()]
        if len(lines) < 2:
            print("%s: 无 LAMOST 命中" % t)
        else:
            hdr = [h.strip() for h in lines[0].replace("\ufeff", "").split(",")]
            for ln in lines[1:]:
                v = dict(zip(hdr, ln.split(",")))
                print("%s: obsid=%s snrr=%s class=%s ra=%s dec=%s" % (
                    t, v.get("combined.obsid", v.get("obsid", "?")), v.get("combined.snrr", v.get("snrr", "?")),
                    v.get("combined.class", v.get("class", "?")), v.get("combined.ra", v.get("ra", "?")),
                    v.get("combined.dec", v.get("dec", "?"))))
    except Exception as e:
        print(t, "ERR", str(e)[:100])
    time.sleep(0.5)
