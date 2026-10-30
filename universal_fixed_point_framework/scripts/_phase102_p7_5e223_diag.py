# -*- coding: utf-8 -*-
"""P7-5e-223 诊断：m=-384, B=0.005067 打靶粗扫行为"""
import sys
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from _phase102_p7_5e223_shooting_dinf_closure import shoot_wall, V_eff, closed_1B

m = -384
B = 1.0/closed_1B(m) * 0.9735
r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
print("m=%d B=%.8f r=[%.1f, %.1f]" % (m, B, r_lo, r_hi))
# V 剖面
for r in [r_lo, 200, 390, 600, 900, r_hi]:
    print("  V(%.0f)=%.4f" % (r, V_eff(r, B, m)))
# 粗扫符号
print("== 粗扫 E∈[-1.05,0.5] 步长 0.011 ==")
prev = None
for i in range(140):
    E = -1.05 + 1.55*i/139.0
    psi, nn = shoot_wall(E, r_lo, r_hi, B, m)
    if prev is not None and prev*psi < 0:
        print("  ★ 翻转于 E≈%.4f: prev=%+.3e psi=%+.3e nn=%d" % (E, prev, psi, nn))
    prev = psi
    if i % 14 == 0:
        print("  E=%.3f psi=%+.3e nn=%d" % (E, psi, nn))
