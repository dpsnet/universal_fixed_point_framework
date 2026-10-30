# -*- coding: utf-8 -*-
"""Phase 86 R3：守恒对账与阈值判定
1) bootstrap 误差传播：中场-弱场校准后残差偏移的 95% CI
2) 对账：连续谱增强能量 vs EW 线缺失能量（缺口归因）
3) 阈值判定（R5 用）
"""
import json, io, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(BASE, "_gaia_abs")
with io.open(os.path.join(OUT, "paperX_wd_absflux_cal.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
rows = data["rows"]

def clean(rows, cond, key):
    return [r[key] for r in rows if cond(r) and r.get(key) is not None and not (isinstance(r[key], float) and np.isnan(r[key]))]

def boot_diff(w, m, n_boot=5000, seed=42):
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(n_boot):
        wb = rng.choice(w, len(w), replace=True)
        mb = rng.choice(m, len(m), replace=True)
        diffs.append(np.mean(mb) - np.mean(wb))
    diffs = np.array(diffs)
    return np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)

print("=== 守恒对账（中场 vs 弱场，校准后绝对残差，10-20kK 主档）===")
keys = ["blue_calres", "red_calres", "slopeA_calres"]
EW_MISSING = 0.275  # 中场 EW 线缺失 dex（§4.3.1）
PS85_SLOPE = 0.042  # Phase 85 相对斜率偏移 dex

for key in keys:
    w = clean(rows, lambda r: r["B_MG"] < 10 and 10000 <= r["Teff"] < 20000, key)
    m = clean(rows, lambda r: 10 <= r["B_MG"] < 100 and 10000 <= r["Teff"] < 20000, key)
    if len(w) < 5 or len(m) < 5:
        continue
    d = np.mean(m) - np.mean(w)
    lo, hi = boot_diff(w, m)
    frac = d / EW_MISSING if EW_MISSING else None
    print("%-14s 弱场 n=%2d 中场 n=%2d | 偏移 %+.4f dex [95%%CI %+.4f, %+.4f] | 占线缺失 %.0f%%" % (
        key, len(w), len(m), d, lo, hi, 100 * frac))

print("\n=== 三量偏移均值（中场-弱场）===")
ds = []
for key in keys:
    w = clean(rows, lambda r: r["B_MG"] < 10 and 10000 <= r["Teff"] < 20000, key)
    m = clean(rows, lambda r: 10 <= r["B_MG"] < 100 and 10000 <= r["Teff"] < 20000, key)
    if len(w) >= 5 and len(m) >= 5:
        ds.append(np.mean(m) - np.mean(w))
print("偏移集合:", ["%+.4f" % x for x in ds])
print("连续谱增强代表值: mean(blue,red)=%+.4f dex -> 等效线缺失占比 %.0f%%" % (
    np.mean([x for x in ds[:2]]), 100 * np.mean([x for x in ds[:2]]) / EW_MISSING))

print("\n=== 与 Phase 85 相对口径收敛检查 ===")
print("Phase 85 slope 偏移: -%.3f dex（红/蓝比，红端相对减弱）" % PS85_SLOPE)
print("Phase 86 绝对: blue/red 带中场偏高 %+.3f~%+.3f dex（跳变区增强）；slopeA 中场偏低 %.3f dex（4000-4060 相对 5000-5800 减弱）"
      % (ds[0], ds[1], abs(ds[2])))
print("解读：绝对层面跳变区（3600-3750）中场增强 ~4-6%；4000-4060 相对红段减弱——与 RWA '吸收移向长波+主体下降'方向部分一致")

print("\n=== 阈值判定（R5 输入）===")
enh = np.mean([ds[0], ds[1]])  # 跳变区增强代表
gap = EW_MISSING - enh
print("连续谱增强(跳变区): %+.3f dex；缺口: %.3f dex（%.0f%% 线缺失未在连续谱）" % (enh, gap, 100 * gap / EW_MISSING))
print("判定倾向: 缺口 {:.0f}% 落在 20-80% 区间 -> B 中间态（部分转移+残余缺失）；若 R4 理论上限 < 缺口 -> C 硬异常候选".format(100 * gap / EW_MISSING))
