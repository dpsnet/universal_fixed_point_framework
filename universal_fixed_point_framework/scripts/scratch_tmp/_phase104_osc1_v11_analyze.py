import json, io
import numpy as np
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_osc_v10_disk.json"
d = json.load(io.open(p, "r", encoding="utf-8"))
rs = d["results"]
print("n =", len(rs))
print("--- det_syn（合成谱经论文阈值后检测失败率）---")
for nm in ("Hα","Hβ","Hγ","Hδ","Hε"):
    dets = [r["det_syn"][nm] for r in rs if nm in r["det_syn"]]
    if dets:
        fail = sum(1 for x in dets if not x)
        print("  %s: 检测失败 %d/%d (%.0f%%)" % (nm, fail, len(dets), 100*fail/len(dets)))
print("--- 残余（观测缺失 − 标准缺失，逐星近似：观测用 LAMOST 41MG 档固定值）---")
obs = {"Hα": 0.0, "Hβ": 27.0, "Hγ": 41.0, "Hδ": 12.0, "Hε": 2.0}
for lo, hi, tag in ((10, 41, "B 10-41"), (41, 100, "B 41-100")):
    sub = [r for r in rs if lo <= r["B_MG"] < hi]
    print(tag, "n=", len(sub))
    for nm in ("Hα","Hβ","Hγ","Hδ","Hε"):
        std = np.median([r["miss"][nm] for r in sub if nm in r["miss"] and np.isfinite(r["miss"][nm])])
        print("  %s: 标准 %.1f%% | 观测 %.1f%% | 残余(obs-std) %+.1fpp" % (nm, std, obs[nm], obs[nm]-std))
