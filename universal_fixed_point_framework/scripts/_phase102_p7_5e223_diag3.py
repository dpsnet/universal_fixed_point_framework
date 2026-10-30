# -*- coding: utf-8 -*-
"""P7-5e-223 诊断3：细扫 E 近零区间（落盘）"""
import sys, io
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from _phase102_p7_5e223_shooting_dinf_closure import shoot_wall, closed_1B

m = -384
B = 1.0/closed_1B(m) * 0.9735
r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
out = io.StringIO()
out.write("m=%d B=%.8f（窗口低端 0.9735·Bc） r=[%.1f, %.1f]\n" % (m, B, r_lo, r_hi))
prev = None
for i in range(61):
    E = -0.006 + 0.0002*i
    psi, nn = shoot_wall(E, r_lo, r_hi, B, m)
    flag = ""
    if prev is not None and prev*psi < 0:
        flag = "  ★FLIP"
    out.write("E=%+.4f psi=%+.6e nn=%2d%s\n" % (E, psi, nn, flag))
    prev = psi
open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e223_diag3.txt", "w", encoding="utf-8").write(out.getvalue())
print("done exit 0")
