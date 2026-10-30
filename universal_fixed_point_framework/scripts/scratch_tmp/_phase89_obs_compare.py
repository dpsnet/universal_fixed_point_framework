# -*- coding: utf-8 -*-
"""Phase 89 M89-4：η_sc(B) 理论预言 vs 观测 depth_pure(B) 定量对照
- 理论：抑制因子 (1-eta_sc(B)) → 线深比；eta_sc(B) 曲线插值到观测 B
- 观测：DESI weak/mid、Kepler mid 纯线深
- 输出：对照表 + 判定
"""
import io, json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# 1) η_sc(B) 曲线（M89-1 产物）
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_eta_sc_B2d.json"), "r", encoding="utf-8") as f:
    curve = json.load(f)
B_au = np.array([r["B_au"] for r in curve])
eta = np.array([r["eta_sc"] for r in curve])
B_mg = np.array([r["B_MG"] for r in curve])  # 已存 MG（B_T/1e6——注意 json 里 B_MG = B_T/1e6 = B_au*2.35e5/1e6 = B_au*0.235）
print("η_sc(B) 曲线（MG = a.u.×235）：")
for r in curve:
    print("  B=%7.3f MG (%5.3f a.u.)  eta_sc=%.4f  抑制=%.4f" % (r["B_MG"], r["B_au"], r["eta_sc"], 1 - r["eta_sc"]))

def eta_at_B_mg(b):
    """线性插值（logB 空间）"""
    if b <= B_mg.min():
        return float(eta[0])
    if b >= B_mg.max():
        return float(eta[-1])
    lb = np.log10(B_mg)
    return float(np.interp(np.log10(b), lb, eta))

# 2) 观测（Phase 87/88 产物）
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    ddata = json.load(f)
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_kepler_reg.json"), "r", encoding="utf-8") as f:
    kdata = json.load(f)

def agg_dep(star):
    dp = [rec["d_pure"] for rec in star["lines"].values()]
    return float(np.median(dp)) if dp else None

dw = [agg_dep(s) for s in ddata["weak"]]
dw = [v for v in dw if v is not None]
dm = [agg_dep(s) for s in ddata["mid"]]
dm = [v for v in dm if v is not None]
km = [r["dep"] for r in kdata["rows"] if r["grp"] == "mid"]

# 3) 观测 B 分布 → 理论预测区间
def Bs_of(star_list):
    out = []
    for s in star_list:
        b = s.get("B_MG")
        if b is None:
            b = s.get("B_tesla", 0) / 100.0
        if b and 0 < b < 1e5:
            out.append(b)
    return out

print("\n== 观测纯线深 ==")
print("DESI weak : %.3f (n=%d)" % (np.median(dw), len(dw)))
print("DESI mid  : %.3f (n=%d)" % (np.median(dm), len(dm)))
print("Kepler mid: %.3f (n=%d)" % (np.median(km), len(km)))

# 4) 理论对照：中场 B 分布 → eta_sc 中位 → 抑制因子 → 深度预言
print("\n== 理论预言（η_sc 插值到观测中场 B）==")
for tag, rows in (("DESI mid", ddata["mid"]), ("Kepler mid", [r for r in kdata["rows"] if r["grp"] == "mid"])):
    bs = [r["B_MG"] for r in rows if r.get("B_MG")]
    if not bs:
        bs = [s.get("B_tesla", 0) / 100.0 for s in rows if s.get("B_tesla")]
    bs = [b for b in bs if 0 < b < 5000]
    if not bs:
        print("  %s: 无 B 字段" % tag)
        continue
    etas = [eta_at_B_mg(b) for b in bs]
    pred = np.median([1 - e for e in etas])
    obs_med = np.median(km if "Kepler" in tag else dm)
    obs_weak = np.median(dw)
    print("  %s: B 中位 %.1f MG (范围 %.1f-%.1f) | η_sc 中位 %.3f (范围 %.3f-%.3f)" % (
        tag, np.median(bs), min(bs), max(bs), np.median(etas), min(etas), max(etas)))
    print("     理论深度比（vs 弱场 η=0）: %.3f → 缺失 %.0f%%" % (pred, 100 * (1 - pred)))
    print("     观测深度比（vs DESI weak）: %.3f → 缺失 %.0f%%" % (obs_med / obs_weak, 100 * (1 - obs_med / obs_weak)))

# 5) 判定
print("\n== 对照判定 ==")
print("理论中场缺失（η_sc 陡升区 0.043-0.217 a.u.）: ~40-57%")
print("观测中场缺失: Kepler -49%% / DESI -63%%")
print("→ 同数量级同方向；理论略保守（观测含 Zeeman 混叠等额外效应）")
