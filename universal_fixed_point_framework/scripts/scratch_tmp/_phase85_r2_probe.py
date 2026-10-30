# -*- coding: utf-8 -*-
"""Phase 85 R2 前置：探查 DESI 缓存光谱结构（波长覆盖、跳变可用性）"""
import os, json, numpy as np

D = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_desi_spec"
files = sorted(os.listdir(D))
print("DESI 缓存文件数:", len(files))

# 取样检查 npz 结构
if files:
    f0 = os.path.join(D, files[0])
    d = np.load(f0, allow_pickle=True)
    print("keys:", list(d.keys()))
    for k in d.keys():
        a = d[k]
        print("  ", k, type(a), getattr(a, "shape", None), getattr(a, "dtype", None))

# 统计波长覆盖
wmin, wmax = 1e9, -1e9
n_cover_3646 = 0
n_cover_4000 = 0
n_total = 0
meta = []
for fn in files:
    try:
        d = np.load(os.path.join(D, fn), allow_pickle=True)
        keys = list(d.keys())
        # 找波长数组
        wl = None
        for k in keys:
            a = d[k]
            if getattr(a, "ndim", 0) == 1 and a.size > 500:
                if a.min() > 100 and a.max() < 20000:  # 波长候选
                    wl = a
                    break
        if wl is None:
            print("  无波长数组:", fn)
            continue
        n_total += 1
        lo, hi = float(wl.min()), float(wl.max())
        wmin, wmax = min(wmin, lo), max(wmax, hi)
        if lo <= 3646:
            n_cover_3646 += 1
        if lo <= 4000:
            n_cover_4000 += 1
        meta.append((fn.split(".")[0], lo, hi))
    except Exception as e:
        print("  读取失败", fn, e)

print("样本数:", n_total)
print("波长范围: %.0f - %.0f Å" % (wmin, wmax))
print("覆盖 3646 Å(跳变): %d/%d" % (n_cover_3646, n_total))
print("覆盖 4000 Å: %d/%d" % (n_cover_4000, n_total))

# 保存清单
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_desi_spec\_wl_cover.json", "w") as f:
    json.dump({"n_total": n_total, "n_cover_3646": n_cover_3646, "n_cover_4000": n_cover_4000,
               "range": [wmin, wmax], "per_star": meta}, f, ensure_ascii=False, indent=1)
print("清单已存")
