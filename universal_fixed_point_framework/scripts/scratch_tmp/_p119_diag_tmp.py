# -*- coding: utf-8 -*-
import numpy as np
import sys
sys.path.insert(0, r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts')
from _phase102_p7_5e119_shooting_validate import V, qL_at_rm, qR_at_rm
B = 0.150537; m = -13; E = -0.05; r_max = 120.0
for r_m in [13.0, 20.0, 30.0, 52.0]:
    qL = qL_at_rm(B, m, E, r_m)
    qR = qR_at_rm(B, m, E, r_max, r_m)
    print('r_m=%5.1f  qL=%.6f qR=%.6f F=%.6f  V(r_m)=%.4f' % (r_m, qL, qR, qL-qR, V(r_m,B,m)))
print('r_min ~ sqrt(2*13/0.150537)=%.3f' % np.sqrt(2*13/0.150537))
