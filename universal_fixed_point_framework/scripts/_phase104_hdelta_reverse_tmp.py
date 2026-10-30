# -*- coding: utf-8 -*-
"""Phase 104az-47：LAMOST Hδ 反例核查 + v10_int 强场饱和 + DESI 线间对照"""
import json
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"

def med(v):
    v = [x for x in v if np.isfinite(x)]
    return np.median(v) if v else float("nan")

# ---------- 1. LAMOST Hδ 反例核查 ----------
lam = json.load(open(BASE + r"\paperX_lamost_linelevel_raw.json", encoding="utf-8"))
mid = [r for r in lam if r.get("grp") == "mid" and r.get("B_MG") is not None]
print("=== 1. LAMOST mid Hδ vs Hγ：测量质量 + B 分档 ===")
# 每线失败率（无 d_pure 或 nan）
for lab in ("Hbeta", "Hgamma", "Hdelta", "Heps"):
    n_ok = sum(1 for r in mid if r.get("lines", {}).get(lab) and
               np.isfinite(r["lines"][lab].get("d_pure")))
    print("  %-7s 有效 %2d/90 (%.0f%%)  失败率 %.0f%%" %
          (lab, n_ok, 100.0 * n_ok / 90, 100.0 * (90 - n_ok) / 90))

# Hδ 逐 B 档详细（含散布）
print("\n  Hdelta B 分档（含散布）:")
for lo, hi in [(10, 20), (20, 41), (41, 80), (80, 1000)]:
    sub = [r["lines"]["Hdelta"]["d_pure"] for r in mid
           if lo <= r["B_MG"] < hi and r.get("lines", {}).get("Hdelta")
           and np.isfinite(r["lines"]["Hdelta"].get("d_pure")) and r["lines"]["Hdelta"]["d_pure"] >= 0]
    if sub:
        a = np.array(sub)
        print("    B[%2d,%3d) n=%2d  中位=%.4f  均值=%.4f  std=%.4f  min=%.4f max=%.4f" %
              (lo, hi, len(a), np.median(a), np.mean(a), np.std(a), a.min(), a.max()))
    else:
        print("    B[%2d,%3d) n= 0" % (lo, hi))

# Hδ 深线嫌疑：d_pure>0.15 的星（可能 DA 特征或污染）
print("\n  Hdelta d_pure>0.15 的 mid 星（深线嫌疑）:")
deep = [r for r in mid if r.get("lines", {}).get("Hdelta")
        and np.isfinite(r["lines"]["Hdelta"].get("d_pure")) and r["lines"]["Hdelta"]["d_pure"] > 0.15]
print("    n=%d" % len(deep))
for r in deep[:8]:
    print("    %s B=%.1f MG Hd=%.3f Hb=%.3f Hg=%.3f" %
          (r.get("name", "?"), r.get("B_MG", 0),
           r["lines"]["Hdelta"]["d_pure"],
           r["lines"].get("Hbeta", {}).get("d_pure", -1),
           r["lines"].get("Hgamma", {}).get("d_pure", -1)))

# ---------- 2. v10_int 强场场内 B 分档（饱和预言 P5） ----------
print("\n=== 2. v10_int 强场（109-778 MG）场内 B 分档 d_pure ===")
v10 = json.load(open(BASE + r"\paperX_wd_linelevel_v10int.json", encoding="utf-8"))["strong"]
strong = [r for r in v10 if r.get("B_MG") is not None]
print("  n=%d  B 范围 %.0f–%.0f MG" % (len(strong), min(r["B_MG"] for r in strong),
                                       max(r["B_MG"] for r in strong)))
for lab in ("Halpha", "Hbeta", "Hgamma", "Hdelta", "Heps"):
    print("  --- %s ---" % lab)
    for lo, hi in [(100, 200), (200, 400), (400, 1000)]:
        sub = [r["lines"][lab]["d_pure"] for r in strong
               if lo <= r["B_MG"] < hi and r.get("lines", {}).get(lab)
               and np.isfinite(r["lines"][lab].get("d_pure")) and r["lines"][lab]["d_pure"] >= 0]
        if sub:
            a = np.array(sub)
            print("    B[%3d,%3d) n=%2d  d_pure中位=%.4f  均值=%.4f" %
                  (lo, hi, len(a), np.median(a), np.mean(a)))
        else:
            print("    B[%3d,%3d) n= 0（无线）" % (lo, hi))

# 无线率（无 d_pure 记录 = 未检测）
print("\n  强场无线率（无有效线记录）:")
for lab in ("Halpha", "Hbeta", "Hgamma", "Hdelta", "Heps"):
    n_ok = sum(1 for r in strong if r.get("lines", {}).get(lab) and
               np.isfinite(r["lines"][lab].get("d_pure")))
    print("    %-7s 有线 %2d/%2d (%.0f%%)  无线 %.0f%%" %
          (lab, n_ok, len(strong), 100.0 * n_ok / len(strong), 100.0 * (len(strong) - n_ok) / len(strong)))

# ---------- 3. DESI mid/weak 线间对照复算 ----------
print("\n=== 3. DESI mid/weak 线间 d_pure 对照 ===")
midf = json.load(open(BASE + r"\paperX_wd_linelevel_mid_full_snr.json", encoding="utf-8"))["mid_full"]
weaks = json.load(open(BASE + r"\paperX_wd_linelevel_weak_sdss_snr.json", encoding="utf-8"))["weak_sdss"]
print("  mid n=%d, weak n=%d" % (len(midf), len(weaks)))
print("  mid B 分布:", "中位 %.1f" % np.median([r["B_MG"] for r in midf if r.get("B_MG") is not None]),
      "范围 %.1f–%.1f" % (min(r["B_MG"] for r in midf if r.get("B_MG") is not None),
                          max(r["B_MG"] for r in midf if r.get("B_MG") is not None)))
for lab in ("Halpha", "Hbeta", "Hgamma", "Hdelta", "Heps"):
    mv = [r["lines"][lab]["d_pure"] for r in midf if r.get("lines", {}).get(lab)
          and np.isfinite(r["lines"][lab].get("d_pure")) and r["lines"][lab]["d_pure"] >= 0]
    wv = [r["lines"][lab]["d_pure"] for r in weaks if r.get("lines", {}).get(lab)
          and np.isfinite(r["lines"][lab].get("d_pure")) and r["lines"][lab]["d_pure"] >= 0]
    if mv and wv:
        loss = 1.0 - np.median(mv) / np.median(wv)
        print("  %-7s mid中位=%.4f(n=%2d)  weak中位=%.4f(n=%2d)  缺失=%.0f%%" %
              (lab, np.median(mv), len(mv), np.median(wv), len(wv), 100.0 * loss))
    else:
        print("  %-7s mid n=%d weak n=%d" % (lab, len(mv), len(wv)))
