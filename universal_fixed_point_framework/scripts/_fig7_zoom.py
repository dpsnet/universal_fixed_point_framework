#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""高倍裁剪图 7 刻度标签与图例区域。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
# 绘图区边框：col 112/964, row 13/590
regions = {
    # x 轴刻度数字（底边框下方）
    "xlabel_0":  (90, 590, 250, 660),
    "xlabel_1":  (250, 590, 420, 660),
    "xlabel_2":  (420, 590, 600, 660),
    "xlabel_3":  (600, 590, 800, 660),
    "xlabel_4":  (800, 590, 982, 660),
    "xlabel_all":(60, 580, 982, 690),
    # y 轴刻度数字（左边框左侧）
    "ylabel_all":(0, 0, 130, 708),
    # 图例
    "legend":    (690, 30, 982, 280),
    # 右下角红点(808,538)附近
    "r6":        (760, 480, 860, 590),
}
for name, box in regions.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 5, c.height * 5), Image.LANCZOS)
    p = r"C:\Users\dps_n\Desktop\fig7z_" + name + ".png"
    c2.save(p)
    print("saved:", p, c2.size)
