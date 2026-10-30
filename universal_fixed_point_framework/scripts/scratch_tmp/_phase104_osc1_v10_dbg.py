# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
import _phase104_osc1_v10_tmp as M
c = M.components(0.0001, 0.0001)
for n in (3, 4, 5):
    print("B=0 n=", n, " ncomp=", len(c[n]))
    for d, w in c[n][:5]:
        print("   dlam=%.3f w=%.4f" % (d, w))
c2 = M.components(10.0, 10.0)
for n in (3, 4, 5):
    print("B=10 n=", n, " ncomp=", len(c2[n]))
    for d, w in c2[n][:8]:
        print("   dlam=%.1f w=%.4f" % (d, w))
