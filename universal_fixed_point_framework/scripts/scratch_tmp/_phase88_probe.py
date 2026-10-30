# -*- coding: utf-8 -*-
"""Phase 88 规划探查：Amorim 目录中场星（10-100 MG）+ Kepler + 其他目录可用性"""
import io, json, os
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# Amorim 518 全目录（M83c 样本）
for fn in ("paperX_wd_m83c_samples.json", "paperX_wd_m83c_sample_list.json"):
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        print(fn, "不存在")
        continue
    with io.open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 结构探查
    if isinstance(data, dict):
        keys = list(data.keys())[:5]
        print(fn, "dict keys:", keys)
        # 样本可能在 data['samples'] 或 data 本身
        lst = data.get("samples", data.get("data", None))
    else:
        lst = data
    if isinstance(lst, list) and lst:
        s0 = lst[0]
        print(fn, "n =", len(lst), "| 字段:", list(s0.keys()) if isinstance(s0, dict) else type(s0))
        if isinstance(s0, dict):
            bkey = [k for k in s0 if "B" in k or "field" in k.lower()]
            print("   B 字段候选:", bkey)
            # 中场统计
            mids = [s for s in lst if isinstance(s.get(bkey[0]), (int, float)) and 10 <= s[bkey[0]] < 100] if bkey else []
            print("   中场(10-100 MG): %d 颗" % len(mids))
            for s in mids[:15]:
                print("    B=%s Teff=%s logg=%s src=%s" % (s.get(bkey[0]), s.get("Teff", s.get("T_eff", "?")), s.get("logg", "?"), s.get("src", "?")))
    else:
        print(fn, "结构:", type(data), str(data)[:200])
