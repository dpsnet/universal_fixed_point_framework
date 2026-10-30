# -*- coding: utf-8 -*-
import io, json, os
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
print("groups:", list(data.keys()))
for grp in data:
    print(grp, "n_stars:", len(data[grp]))
    nl = []
    for st in data[grp]:
        nl.append(len(st["lines"]))
    print("  lines-per-star:", sorted(set(nl)), "total lines:", sum(nl))
    if data[grp]:
        st0 = data[grp][0]
        print("  sample star gid=%s B=%.1f lines=%s" % (st0["gid"], st0["B_MG"], list(st0["lines"].keys())))
        if st0["lines"]:
            k0 = list(st0["lines"].keys())[0]
            print("  sample rec:", st0["lines"][k0])
