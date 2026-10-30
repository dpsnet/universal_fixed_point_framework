# -*- coding: utf-8 -*-
"""
P7-5e-140b：双曲区 r(c) 判别——c=16,18,20,24（m=32..96）
================================================================
140 显示 r−2 非单调、峰值在 c=9,10（m=18..40=过渡尾迹区）——补双曲区列：
  P1 c≥16 列 r−2 是否收敛到 0（1/m 律在双曲区精确）
  P2 过渡区/双曲区分界：r−2 在 c=12..16 的转变
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
fa = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
fb = json.load(open(os.path.join(BASE, "_phase102_p7_5e117_m32_scan.json"), encoding="utf-8"))
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))

B = {}
for k, v in fa["out"].items():
    B[-int(k)] = v["R2"]
for k, v in fb["out"].items():
    B[-int(k)] = v["Bstar0"]
for k, v in fc["out"].items():
    B[-int(k)] = v["Bstar"]

def closed(m):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    if abs(m) == 1:
        cl += 1.0/65.0
    return cl

C_FIX = 0.1016

def Deff(m):
    return (closed(m) - 1.0/B[m]) - C_FIX/m

print("=== P7-5e-140b 双曲区 r(c) 判别 ===", flush=True)
cols = [7, 8, 9, 10, 12, 14, 16, 18, 20, 24, 28, 32]
prev = None
for c in cols:
    m2, m3, m4 = 2*c, 3*c, 4*c
    if m4 not in B:
        continue
    d2, d3, d4 = Deff(m2), Deff(m3), Deff(m4)
    D1a = d3 - d2
    D1b = d4 - d3
    r = D1a/D1b
    tag = ""
    if prev is not None and (r - 2.0) * prev < 0:
        tag = "  ← 过零/符号翻转"
    if r < 2.0:
        tag += "  ← r<2（方向反转）"
    print("  c=%2d（m=%d/%d/%d）：r=%.4f、r−2=%+.6f%s" % (c, m2, m3, m4, r, r-2.0, tag), flush=True)
    prev = r - 2.0
print("exit 0", flush=True)
