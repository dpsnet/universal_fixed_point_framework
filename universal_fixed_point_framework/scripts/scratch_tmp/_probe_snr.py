# -*- coding: utf-8 -*-
"""探查 SNR 数据可得性：json 键结构 + 观测光谱缓存位置。"""
import io, json, os, glob

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
SC = os.path.join(BASE, "scripts")

def keys_of(path):
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        return "ERR %s" % e
    if isinstance(d, dict):
        ks = list(d.keys())
        # 取第一个元素的键作为结构样例
        sample = None
        for k in ks[:2]:
            v = d[k]
            if isinstance(v, dict):
                sample = list(v.keys())
                break
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                sample = list(v[0].keys())
                break
        return "keys=%s sample_keys=%s" % (ks[:8], sample)
    if isinstance(d, list):
        if d and isinstance(d[0], dict):
            return "list len=%d item_keys=%s" % (len(d), list(d[0].keys()))
        return "list len=%d" % len(d)
    return "type=%s" % type(d)

targets = [
    os.path.join(SC, "paperX_wd_m83c_sample_list.json"),
    os.path.join(SC, "paperX_wd_m83c_samples.json"),
    os.path.join(SC, "paperX_wd_m83c_koester_ew.json"),
    os.path.join(SC, "paperX_wd_m83d_kepler2013.json"),
    os.path.join(SC, "paperX_wd_m83d_kepler_sample.json"),
    os.path.join(SC, "paperX_wd_m83c_regression.json"),
    os.path.join(SC, "paperX_wd_m83c_tmap_reg.json"),
]
for p in targets:
    print("==", os.path.basename(p))
    print("  ", keys_of(p) if os.path.exists(p) else "MISSING")

# 找 v10/v11 观测结果 json（含 SNR 的可能）
for pat in ["results*.json", "v10*", "v11*", "wd*"]:
    hits = glob.glob(os.path.join(SC, pat))
    if hits:
        print("GLOB", pat, "->", [os.path.basename(h) for h in hits][:10])

# 观测光谱缓存目录
for d in glob.glob(os.path.join(SC, "*")):
    if os.path.isdir(d) and ("spec" in os.path.basename(d).lower() or "sdss" in os.path.basename(d).lower()):
        n = len(glob.glob(os.path.join(d, "*")))
        print("DIR", os.path.basename(d), "files=", n)
