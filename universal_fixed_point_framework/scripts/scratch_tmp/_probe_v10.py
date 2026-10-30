# -*- coding: utf-8 -*-
"""探查 v10/v11 结果 json 结构（找 plate-mjd-fiber 与 SNR 相关键）。"""
import io, json, os, glob

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
for root in [os.path.join(BASE, "results"), os.path.join(BASE, "scripts"), os.path.join(BASE, "src", "white_dwarf_analysis")]:
    for pat in ["*v10*", "*v11*"]:
        for p in glob.glob(os.path.join(root, pat)):
            if not p.endswith(".json"):
                continue
            print("==", p)
            try:
                with io.open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
            except Exception as e:
                print("   ERR", e); continue
            if isinstance(d, dict):
                ks = list(d.keys())
                print("   keys:", ks[:12])
                # 找每颗星的记录结构
                for k in ks:
                    v = d[k]
                    if isinstance(v, list) and v and isinstance(v[0], dict):
                        print("   list field %s: len=%d item_keys=%s" % (k, len(v), list(v[0].keys())))
                        break
                    if isinstance(v, dict) and v and isinstance(list(v.values())[0], dict):
                        print("   dict field %s: sample keys=%s" % (k, list(list(v.values())[0].keys())))
                        break
            elif isinstance(d, list) and d and isinstance(d[0], dict):
                print("   list len=%d item_keys=%s" % (len(d), list(d[0].keys())))
