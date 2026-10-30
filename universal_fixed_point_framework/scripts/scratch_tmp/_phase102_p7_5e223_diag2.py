# -*- coding: utf-8 -*-
"""P7-5e-223 诊断2：细扫 E 近零区间，检查束缚态根"""
import sys
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from _phase102_p7_5e223_shooting_dinf_closure import shoot_wall, closed_1B

m = -384
B = 1.0/closed_1B(m) * 0.9735
r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
print("m=%d B=%.8f（窗口低端 0.9735·Bc）" % (m, B))
prev = None
for i in range(61):
    E = -0.006 + 0.0002*i
    psi, nn = shoot_wall(E, r_lo, r_hi, B, m)
    flag = ""
    if prev is not None and prev*psi < 0:
        flag = " ★翻转"
    if i % 10 == 0 or flag:
        print("  E=%+.4f psi=%+.6e nn=%2d%s" % (E, psi, nn, flag))
    prev = psi
