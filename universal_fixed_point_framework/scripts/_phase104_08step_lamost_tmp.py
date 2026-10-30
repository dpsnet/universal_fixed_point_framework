# -*- coding: utf-8 -*-
"""Phase 104az-46：0.8 阶跃判别 + LAMOST 有效线分布检验"""
import json, collections
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"

# ---------- 1. LAMOST 线级数据：有效线分布 ----------
d = json.load(open(BASE + r"\paperX_lamost_linelevel_raw.json", encoding="utf-8"))
print("total recs:", len(d))
withl = [r for r in d if "lines" in r and r.get("grp")]
print("with lines & grp:", len(withl))

grp_counter = collections.Counter(r.get("grp") for r in withl)
print("grp:", dict(grp_counter))

# 每线有效统计（d_pure 有限且 >=0）
lines_of = ["Hbeta", "Hgamma", "Hdelta", "Heps", "Hzeta"]
for grp in ("mid", "weak"):
    sub = [r for r in withl if r.get("grp") == grp]
    n = len(sub)
    print("\n=== grp=%s n=%d ===" % (grp, n))
    for lab in lines_of:
        vals = []
        for r in sub:
            ln = r.get("lines", {}).get(lab)
            if ln and np.isfinite(ln.get("d_pure")) and ln["d_pure"] >= 0:
                vals.append(ln["d_pure"])
        if vals:
            print("  %-7s 有效=%2d/%2d  d_pure中位=%.4f  均值=%.4f" %
                  (lab, len(vals), n, np.median(vals), np.mean(vals)))
        else:
            print("  %-7s 有效= 0/%2d" % (lab, n))

# ---------- 2. LAMOST SNR 匹配子样本（snrr>=21 weak）的线组成 ----------
print("\n=== SNR匹配子样本（weak snrr>=21）线组成 ===")
weak_hi = [r for r in withl if r.get("grp") == "weak" and r.get("snrr", 0) >= 21]
mid_all = [r for r in withl if r.get("grp") == "mid"]
print("weak snrr>=21 n=%d, mid n=%d" % (len(weak_hi), len(mid_all)))
for lab in lines_of:
    wv = [r["lines"][lab]["d_pure"] for r in weak_hi
          if r.get("lines", {}).get(lab) and np.isfinite(r["lines"][lab]["d_pure"])]
    mv = [r["lines"][lab]["d_pure"] for r in mid_all
          if r.get("lines", {}).get(lab) and np.isfinite(r["lines"][lab]["d_pure"])]
    if wv or mv:
        wm = np.median(wv) if wv else float("nan")
        mm = np.median(mv) if mv else float("nan")
        print("  %-7s weak有效=%2d(中位%.4f)  mid有效=%2d(中位%.4f)  比值=%.3f" %
              (lab, len(wv), wm, len(mv), mm, (wm / mm if mm > 0 else float("nan"))))

# ---------- 3. 0.8 阶跃判别（DESI 线间 + 强场饱和 + 弱场基线） ----------
print("\n=== 0.8 阶跃判别（η_comp vs 缺失率） ===")
# 数据点：(η_comp, 缺失率, 标签, 源)
pts = [
    (0.161, 0.00, "Hα 弱场基线", "desi/零场模型"),
    (0.600, 0.45, "Hβ η<0.8 保留区", "desi 纯线深"),
    (0.806, 0.84, "Hγ η>0.8 缺口区", "desi 纯线深"),
    (0.905, 0.98, "Hδ η>0.8 缺口区", "desi 纯线深"),
    (0.953, None, "Hε η>0.8 预言", "预言 95.3% 待数据"),
    (1.000, 0.92, "强场饱和(109-778MG)", "amorim d_pure中位"),
]
for p in pts:
    print("  η=%.3f  缺失=%s  %s  [%s]" % (p[0], "%.3f" % p[1] if p[1] is not None else "待测", p[2], p[3]))

# 阶跃检验：跨 0.8 跳变量 vs 0.8 以上平台散布
below = [0.00, 0.45]   # Hα, Hβ
above = [0.84, 0.98]   # Hγ, Hδ
sat = [0.92]           # 强场饱和
jump = np.mean(above) - np.mean(below)
print("\n  <0.8 平均缺失: %.3f   >0.8 平均缺失: %.3f   跨0.8跳变: %.3f (%.1fpp)" %
      (np.mean(below), np.mean(above), jump, jump * 100))
print("  0.8以上平台散布(84/98/92): std=%.3f  平台均值=%.3f" %
      (np.std(above + sat), np.mean(above + sat)))
print("  阶跃 vs 渐变: 3 数据点(Hβ/Hγ/Hδ)跨0.8跳变%.1fpp；0.8以上三点近似平台(std=%.3f) → 方向性支持阶跃；判别力受限(线数3)" %
      (jump * 100, np.std(above + sat)))
