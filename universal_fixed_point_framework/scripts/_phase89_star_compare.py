# -*- coding: utf-8 -*-
"""Phase 89 M89-4 逐星对照：η_sc(B) 束缚态衰减口径 vs DESI mid 单星 d_pure
锚：B_ref=0.005 a.u.（11.8 MG）→ N=49（本脚本 SA 计数全分波）
"""
import io, json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_eta_sc_B_bound.json"), "r", encoding="utf-8") as f:
    bound = json.load(f)
B_au = np.array([r["B_au"] for r in bound])
N = np.array([r["n_bound"] for r in bound])
# 锚：0.005 a.u. → 49（取全曲线最小 B 点）
i_ref = int(np.argmin(B_au))
N_ref = float(N[i_ref])
print("锚：B_ref=%.3f a.u. (%.1f MG) → N_bound=%d" % (B_au[i_ref], B_au[i_ref]*2350, N_ref))

def eta_bound_at_b_mg(b_mg):
    b_au = b_mg / 2350.0
    if b_au <= B_au[i_ref]:
        return 0.0
    if b_au >= B_au.max():
        n = N[-1]
    else:
        n = float(np.interp(b_au, B_au, N))
    return max(0.0, min(1.0, 1.0 - n / N_ref))

# DESI mid 逐星
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    ddata = json.load(f)
print("\nDESI mid 逐星（B_MG → η_sc → 理论深度比 vs 观测 d_pure）")
rows = []
for s in ddata["mid"]:
    b = s.get("B_MG") or (s.get("B_tesla", 0) / 100.0)
    dp = np.median([rec["d_pure"] for rec in s["lines"].values()])
    eta = eta_bound_at_b_mg(b)
    pred = 1.0 - eta
    rows.append((b, dp, eta, pred, s.get("id", "?")))
for b, dp, eta, pred, sid in sorted(rows):
    print("  B=%6.1f MG  eta_sc=%.2f  理论深度比=%.2f  obs d_pure=%.3f  (%s)" % (b, eta, pred, dp, sid))

# Kepler mid 逐星
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_kepler_reg.json"), "r", encoding="utf-8") as f:
    kdata = json.load(f)
print("\nKepler mid 逐星")
krows = []
for r in kdata["rows"]:
    if r["grp"] != "mid":
        continue
    b = r.get("B_MG") or (r.get("B_tesla", 0) / 100.0)
    eta = eta_bound_at_b_mg(b)
    krows.append((b, r["dep"], eta, 1.0 - eta, r.get("id", "?")))
for b, dep, eta, pred, sid in sorted(krows):
    print("  B=%6.1f MG  eta_sc=%.2f  理论深度比=%.2f  obs dep=%.3f  (%s)" % (b, eta, pred, dep, sid))

# 汇总判定
print("\n== 汇总 ==")
dm = [np.median([rec["d_pure"] for rec in s["lines"].values()]) for s in ddata["mid"]]
km = [r["dep"] for r in kdata["rows"] if r["grp"] == "mid"]
dw = [np.median([rec["d_pure"] for rec in s["lines"].values()]) for s in ddata["weak"]]
print("DESI mid obs 深度中位 %.3f / 弱场 %.3f → 缺失 %.0f%%" % (np.median(dm), np.median(dw), 100*(1-np.median(dm)/np.median(dw))))
print("Kepler mid obs 深度中位 %.3f / DESI weak %.3f → 缺失 %.0f%%" % (np.median(km), np.median(dw), 100*(1-np.median(km)/np.median(dw))))
# 理论：mid 中位 B → η
bm = [s.get("B_MG") or (s.get("B_tesla",0)/100.0) for s in ddata["mid"]]
bk = [r.get("B_MG") or (r.get("B_tesla",0)/100.0) for r in kdata["rows"] if r["grp"]=="mid"]
print("DESI mid B 中位 %.1f MG → η_sc %.2f → 理论缺失 %.0f%%" % (np.median(bm), eta_bound_at_b_mg(np.median(bm)), 100*eta_bound_at_b_mg(np.median(bm))))
print("Kepler mid B 中位 %.1f MG → η_sc %.2f → 理论缺失 %.0f%%" % (np.median(bk), eta_bound_at_b_mg(np.median(bk)), 100*eta_bound_at_b_mg(np.median(bk))))
# 强中场子集（>35 MG）
for tag, bs, deps in (("DESI mid>35MG", bm, dm), ("Kepler mid>35MG", bk, km)):
    idx = [i for i, b in enumerate(bs) if b > 35]
    if idx:
        print("%s: n=%d 观测缺失 %.0f%%（vs 弱场） | 理论 η_sc 中位 %.2f" % (
            tag, len(idx), 100*(1-np.median([deps[i] for i in idx])/np.median(dw)),
            np.median([eta_bound_at_b_mg(bs[i]) for i in idx])))
