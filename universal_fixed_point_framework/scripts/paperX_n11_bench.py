# -*- coding: utf-8 -*-
import sys, time, random
sys.path.insert(0, "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts")
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear

n = 11
rng = random.Random(1)
t0 = time.time()
for i in range(200):
    omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
    A_BG(n, omega, zbar)
dt = time.time() - t0
print(f"n=11: {dt:.1f}s / 200 samples = {dt/200*1000:.1f} ms/sample")
