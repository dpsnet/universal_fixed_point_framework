# -*- coding: utf-8 -*-
"""入库：PLoS One 2024 青山口组 D86 井 16 样品 Rock-Eval 数据 + 初步三因素检验
来源：Ji et al. 2024, PLoS ONE 19(10):e0309346（PMC11488739），Table 1
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "data", "rockeval_qingshankou_d86")
os.makedirs(OUT_DIR, exist_ok=True)

# 从 PMC Table 1 转录（人工核对 D86-4 HI=718 = 12.76/1.78*100 ✓）
raw = [
    ("D86-4", 1971.2, 1.78, 448, 1.96, 12.76, 718),
    ("D86-6", 1974.2, 1.79, 445, 1.76, 9.79, 547),
    ("D86-8", 1976.9, 0.86, 445, 0.91, 4.64, 539),
    ("D86-11", 1979.6, 0.98, 439, 0.94, 4.87, 499),
    ("D86-12", 1982.2, 0.89, 441, 0.96, 4.24, 477),
    ("D86-22", 1984.3, 1.15, 438, 1.12, 3.84, 334),
    ("D86-25", 1985.7, 2.02, 449, 2.14, 10.49, 519),
    ("D86-26", 1987.6, 1.51, 445, 1.87, 6.74, 446),
    ("D86-27", 1989.7, 2.33, 450, 2.42, 9.64, 414),
    ("D86-28", 1990.8, 2.03, 435, 2.82, 9.06, 446),
    ("D86-31", 1993.9, 2.20, 452, 2.85, 11.71, 533),
    ("D86-32", 1996.3, 1.66, 452, 1.70, 8.41, 508),
    ("D86-34", 1999.5, 2.11, 452, 2.11, 12.48, 593),
    ("D86-36", 2001.8, 2.38, 452, 2.52, 11.79, 496),
    ("D86-37", 2003.7, 2.42, 454, 2.06, 13.55, 560),
    ("D86-38", 2007.0, 1.55, 451, 1.22, 6.90, 445),
]

csv_path = os.path.join(OUT_DIR, "qingshankou_d86_rockeval.csv")
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Sample_ID", "Depth_m", "TOC_wt", "Tmax_C", "S1_mgg", "S2_mgg", "HI"])
    for r in raw:
        w.writerow(r)
print("written:", csv_path, len(raw), "samples")

# 初步三因素检验
toc = np.array([r[2] for r in raw])
tm = np.array([r[3] for r in raw])
s1 = np.array([r[4] for r in raw])
s2 = np.array([r[5] for r in raw])
osi = s1 / toc * 100.0

# S1-TOC 线性回归
a, b = np.polyfit(toc, s1, 1)
yp = a * toc + b
ss = np.sum((s1 - yp) ** 2) / np.sum((s1 - s1.mean()) ** 2)
r2 = 1.0 - ss
print("\nS1 = %.3f·TOC %+.3f  R2=%.4f" % (a, b, r2))
med = np.median(toc)
lo_ratio = np.median(s1[toc < med]) / np.median(s1[toc >= med])
print("低/高半区 S1 比=%.3f   minS1=%.2f" % (lo_ratio, s1.min()))
print("Tmax 范围=%d-%d℃（窗宽 %d）  OSI 中位=%.1f  OSI 范围=[%.1f, %.1f]"
      % (tm.min(), tm.max(), tm.max() - tm.min(), np.median(osi), osi.min(), osi.max()))
# 零阈值三判据
z1 = r2 >= 0.90
z2 = lo_ratio < 0.35
z3 = s1.min() < 0.25
print("Z1 线性度 R2>=0.90: %s   Z2 低端趋零: %s   Z3 c->0: %s" % (z1, z2, z3))
print("分类：%s" % ("零阈值型" if (z1 and z2 and z3) else "非零阈值型（湖相富油页岩，S1 高背景）"))
