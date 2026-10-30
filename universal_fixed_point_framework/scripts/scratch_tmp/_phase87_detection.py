# -*- coding: utf-8 -*-
"""Phase 87 M87-7c：检测阈值独立评估
检验：n_det 差异是否完全由 depth 差异解释（若弱/中在相同 depth 档检测率一致 → 检测机制无磁场特异性，非独立缺失来源）
"""
import io, json, os
import numpy as np
from scipy import stats
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel_reg.json"), "r", encoding="utf-8") as f:
    lvl = json.load(f)

# 主档 8-25kK
rows = []
for s in cat:
    gid = str(s["gaia_int"])
    if gid not in ew0 or not ew0[gid].get("ok"):
        continue
    if not (8000 <= s["Teff"] <= 25000):
        continue
    rows.append(s)
weak = [s for s in rows if s["B_MG"] < 10]
mid = [s for s in rows if 10 <= s["B_MG"] < 100]

# per-star depth（来自 linelevel 聚合）
per_star = {}
for r in lvl["rows"]:
    per_star[r["gid"]] = r

def ndet(gid):
    return ew0[gid].get("n_det", 0)

print("== n_det 分组比较 ==")
for grp, lst in (("weak", weak), ("mid", mid)):
    nd = [ndet(str(s["gaia_int"])) for s in lst]
    print("%-4s n=%d  n_det: 中位 %.1f 均值 %.2f±%.2f  分布 %s" % (
        grp, len(lst), np.median(nd), np.mean(nd), np.std(nd),
        {v: nd.count(v) for v in sorted(set(nd))}))

# n_det ~ log10B（全部主档）
B = np.array([s["B_MG"] for s in rows])
ND = np.array([ndet(str(s["gaia_int"])) for s in rows])
lb = np.log10(B)
rho, p = stats.spearmanr(lb, ND)
print("\nn_det ~ log10B: rho=%.3f p=%.4f" % (rho, p))

# depth 控制后：weak/mid 在相同 depth 档的 n_det 检测率
print("\n== depth 分档 × 组别：n_det（检测线数）==")
depths = np.array([per_star[str(s["gaia_int"])]["dep"] for s in rows if str(s["gaia_int"]) in per_star])
grps = np.array([("mid" if s["B_MG"] >= 10 else "weak") for s in rows if str(s["gaia_int"]) in per_star])
nd2 = np.array([ndet(str(s["gaia_int"])) for s in rows if str(s["gaia_int"]) in per_star])
for lo, hi in ((0.05, 0.2), (0.2, 0.35), (0.35, 0.6)):
    mm = (depths >= lo) & (depths < hi)
    if mm.sum() < 3:
        continue
    for g in ("weak", "mid"):
        sel = mm & (grps == g)
        if sel.sum() >= 2:
            print("[depth %.2f-%.2f] %-4s n=%d n_det %.1f±%.1f" % (
                lo, hi, g, sel.sum(), np.mean(nd2[sel]), np.std(nd2[sel])))

# 检测率 = n_det/7（7 根线满检测）
print("\n== 检测率（n_det/7）==")
for grp, lst in (("weak", weak), ("mid", mid)):
    dr = [ndet(str(s["gaia_int"])) / 7.0 for s in lst]
    print("%-4s 中位 %.2f 均值 %.2f±%.2f" % (grp, np.median(dr), np.mean(dr), np.std(dr)))

# 关键：n_det 与 depth 的相关（弱/中合并）——若 n_det 完全由 depth 决定 → 无独立机制
rho2, p2 = stats.spearmanr(depths, nd2)
print("\nn_det ~ depth（合并样本）: rho=%.3f p=%.4f" % (rho2, p2))
# 控制 depth 后 B 的偏相关
from scipy.stats import spearmanr
import numpy as np
def partial_corr(x, y, z):
    rx = spearmanr(x, z)[0]; ry = spearmanr(y, z)[0]
    rxy = spearmanr(x, y)[0]
    return (rxy - rx * ry) / np.sqrt((1 - rx ** 2) * (1 - ry ** 2))
pc = partial_corr(lb[np.array([str(s['gaia_int']) in per_star for s in rows])],
                  nd2, depths)
print("n_det ~ B 控制 depth 偏相关: r=%.3f" % pc)
