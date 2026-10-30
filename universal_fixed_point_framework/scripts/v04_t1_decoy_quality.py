# -*- coding: utf-8 -*-
"""104az-214c：T1（κΛ 家族）decoy 最优命中质量对比
口径：真实 κΛ 主诉 = (400,231) dev 3.6e-6（族内最优命中质量）。
若同域 decoy 的最优命中 dev 也达 1e-6 级 → "深命中唯一"同样不成立（深命中普遍）。
"""
import random

F = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105, 231, 320, 675, 400]
T = 401.73304855   # κΛ 定义值
FRAME_DEV = 3.6014423e-6

def scan_best(target):
    best = (1e9, None)
    for A in F:
        for n in range(1, 5001):
            v = A * (1 + 1.0 / n)
            dev = abs(v - target) / target
            if dev < best[0]:
                best = (dev, (A, n, v))
    return best

# 与 v04_significance_draft.py 同 seed（hash("kappa") % 10000）
rng = random.Random(hash("kappa") % 10000)
decoys = [T * (0.9 + 0.2 * rng.random()) for _ in range(10)]

print("真实 κΛ：最优命中 dev=%.2e（(400,231)，主诉 3.6e-6）" % FRAME_DEV, flush=True)
print("decoy 最优命中质量（对照：κΛ 3.6e-6）：", flush=True)
for i, dT in enumerate(decoys):
    best_dev, (A, n, v) = scan_best(dT)
    mark = " ◀ 同深度档（≤1e-5）" if best_dev <= 1e-5 else ""
    print("  decoy %d = %.6f：最优 dev=%.2e（A=%d, n=%d）%s" % (i, dT, best_dev, A, n, mark), flush=True)
