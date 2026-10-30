# -*- coding: utf-8 -*-
"""Phase 104f: 原脚本 _phase86_r4b_rwa.py 网格诊断——eps 物理位置核实"""
import numpy as np
import math

RYD = 13.605693

# 复刻原脚本网格构造
wl = np.linspace(3400, 6200, 561)
eps_orig = 13.605693 / (1240.0 / wl) / RYD

# 正确 Balmer 带（Å → eV → Ry）
eps_correct = (12400.0 / wl) / RYD

print('=== 原脚本网格 eps = wl/1240 ===')
print('wl=3400 → eps_orig = %.4f Ry = %.2f eV（原脚本）' % (eps_orig[0], eps_orig[0]*RYD))
print('wl=6200 → eps_orig = %.4f Ry = %.2f eV（原脚本）' % (eps_orig[-1], eps_orig[-1]*RYD))
print('正确 Balmer 带（12400/wl）：3600Å → %.4f Ry = %.4f eV；3750Å → %.4f Ry = %.4f eV'
      % (eps_correct[200], eps_correct[200]*RYD, eps_correct[350], eps_correct[350]*RYD))
print()
print('Balmer 连续谱阈（n=2 电离）= 0.25 Ry = 3.40 eV')
print('原脚本带选择：blue(3600-3640) → wl 数组 3600-3640 → eps = %.3f-%.3f Ry = %.1f-%.1f eV'
      % (3600/1240, 3640/1240, 3600/1240*RYD, 3640/1240*RYD))
print('slopeB(5000-5800) → eps = %.3f-%.3f Ry = %.1f-%.1f eV' % (5000/1240, 5800/1240, 5000/1240*RYD, 5800/1240*RYD))
print()
print('=== 判定 ===')
print('原脚本在 %.1f-%.1f eV（非 Balmer 3.4 eV）——n=2 阈值位移 ±0.116 eV 相对 %.0f eV 光子 = %.2f%%'
      % (eps_orig[0]*RYD, eps_orig[-1]*RYD, eps_orig[0]*RYD, 0.116/(eps_orig[0]*RYD)*100))
