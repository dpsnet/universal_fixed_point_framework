# -*- coding: utf-8 -*-
"""Phase 89 M89-4 定稿对照：束缚态衰减口径（论文表态数锚 303@0.001）
η_sc(B) = 1 - N_bound(B)/303；N_bound: 0.001→303, 0.01→300, 0.05→152, 0.1→69, 0.2→33（logB 插值）
观测：DESI weak/mid 纯线深、Kepler mid；对照理论缺失区间 vs 观测缺失
"""
import io, json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

B_p = np.array([0.001, 0.01, 0.05, 0.1, 0.2])
N_p = np.array([303, 300, 152, 69, 33])
N_ref = 303.0

def eta_at_b_au(b):
    if b <= 0.001:
        return 0.0
    if b >= 0.2:
        n = 33.0
    else:
        n = float(np.interp(np.log10(b), np.log10(B_p), N_p.astype(float)))
    return max(0.0, min(1.0, 1.0 - n / N_ref))

def eta_at_b_mg(b_mg):
    return eta_at_b_au(b_mg / 2350.0)  # 1 MG = 100 T；1 a.u. = 2.35e5 T

print("理论 η_sc(B)（束缚态衰减，锚 303@0.001 a.u.=0.235 MG）")
for bmg in [1, 5, 10, 15, 20, 23.5, 30, 40, 47, 51, 70, 100, 200, 470]:
    print("  B=%6.1f MG (%.4f a.u.)  η_sc=%.3f  深度比=%.3f  缺失=%.0f%%" % (
        bmg, bmg / 2350.0, eta_at_b_mg(bmg), 1 - eta_at_b_mg(bmg), 100 * eta_at_b_mg(bmg)))

# 观测
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    ddata = json.load(f)
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_kepler_reg.json"), "r", encoding="utf-8") as f:
    kdata = json.load(f)

def med_dep(s_list):
    v = [np.median([rec["d_pure"] for rec in s["lines"].values()]) for s in s_list]
    v = [x for x in v if x == x]
    return float(np.median(v)) if v else float("nan")

dw = med_dep(ddata["weak"]); dm = med_dep(ddata["mid"])
km = float(np.median([r["dep"] for r in kdata["rows"] if r["grp"] == "mid"]))

bm = [s.get("B_MG") or (s.get("B_tesla", 0) / 100.0) for s in ddata["mid"]]
bk = [r.get("B_MG") or (r.get("B_tesla", 0) / 100.0) for r in kdata["rows"] if r["grp"] == "mid"]

print("\n== 对照 ==")
print("观测：DESI weak d_pure=%.3f | DESI mid=%.3f (缺失 %.0f%%) | Kepler mid=%.3f (缺失 %.0f%%)" % (
    dw, dm, 100 * (1 - dm / dw), km, 100 * (1 - km / dw)))
for tag, bs in (("DESI mid", bm), ("Kepler mid", bk)):
    etas = [eta_at_b_mg(b) for b in bs]
    print("%s: B 中位 %.1f MG (%.1f-%.1f) → η_sc 中位 %.2f (%.2f-%.2f) → 理论缺失 %.0f%% (%.0f-%.0f%%)" % (
        tag, np.median(bs), min(bs), max(bs), np.median(etas), min(etas), max(etas),
        100 * np.median(etas), 100 * min(etas), 100 * max(etas)))

print("\n== 判定 ==")
print("理论中场缺失中位 vs 观测：DESI mid 理论 %.0f%% vs 观测 %.0f%% | Kepler mid 理论 %.0f%% vs 观测 %.0f%%" % (
    100 * np.median([eta_at_b_mg(b) for b in bm]), 100 * (1 - dm / dw),
    100 * np.median([eta_at_b_mg(b) for b in bk]), 100 * (1 - km / dw)))
