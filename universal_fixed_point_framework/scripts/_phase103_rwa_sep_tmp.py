# -*- coding: utf-8 -*-
"""Phase 103q: 拓扑禁闭 vs RWA 分量分离
途径①（B 形状分离）：低场（2.5/5MG）calres ≈ RWA（拓扑在低场≈0，η_comp 弱）
   → logB 外推 RWA 基线 → 中场超出 = 拓扑分量
途径②（v5b 预言上限）：拓扑 calres 预言 = |线缺失|×转移份额 vs 观测 calres → 拓扑占比上限
途径③（dex 比对照）：v5b 转移/缺失（0.316）vs 观测 0.21 → 同口径拓扑占比
"""
import math

# 观测（论文/26.10 分档中位 blue_calres dex）
OBS = [(2.5, 0.039), (5.0, 0.055), (20.0, 0.084), (45.0, 0.126), (100.0, 0.140)]
# 论文账本
LOSS_DEX = 0.275   # 线缺失 46.9%
OBS_RATIO = 0.21   # 论文：calres/|缺失| dex 比
# v5b 转移份额（T=12000K, K=10, 出发 n=4）
V5B = {5.0: 0.176, 10.0: 0.213, 20.0: 0.269, 45.0: 0.316, 100.0: 0.337}   # 转移/缺失 比

print('=== 途径①：低场 RWA 基线外推（logB 线性，2.5-5MG 段）===')
b0, c0 = 2.5, 0.039
b1, c1 = 5.0, 0.055
slope = (c1 - c0) / (math.log10(b1) - math.log10(b0))
print('logB 斜率 = %.4f dex/logB' % slope)
print('%-7s | %-8s | %-10s | %-10s' % ('B(MG)', '观测', 'RWA 外推', '拓扑=观测−RWA'))
for B, obs in OBS:
    rwa = c0 + slope * (math.log10(B) - math.log10(b0))
    top = obs - rwa
    print('%-7.1f | %+.4f | %+.4f    | %+.4f%s' % (B, obs, rwa, top,
          '   ← 外推基准段' if B <= 5.0 else ('  ✓ 拓扑>0' if top > 0 else '  ✗ 负')))

print()
print('=== 途径②：v5b 拓扑 calres 预言（|缺失|×转移份额，dex 口径）===')
print('线缺失 46.9%（0.275 dex）——观测 calres +0.058 dex')
top_pred = LOSS_DEX * V5B[45.0]
print('45MG 拓扑 calres 预言 = 0.275 × %.3f = %+.3f dex' % (V5B[45.0], top_pred))
print('观测 calres = +0.058 dex → 拓扑占比上限 f ≤ 0.058/%.3f = %.2f' % (top_pred, 0.058/top_pred))
print('→ RWA 至少占 calres 的 %.0f%%' % ((1 - 0.058/top_pred)*100))

print()
print('=== 途径③：dex 比对照（同口径）===')
print('观测 calres/|缺失| = 0.21（论文账本）')
print('v5b 转移/缺失 = %.3f（45MG）' % V5B[45.0])
f = 0.21 / V5B[45.0]
print('若观测 0.21 = 拓扑份额×%.3f → 拓扑占 calres = %.2f、RWA = %.2f' % (V5B[45.0], f, 1-f))

print()
print('=== 三条途径汇总 ===')
print('途径①（B 形状）：45MG RWA=%+.4f、拓扑=%+.4f（占 calres %.0f%%）'
      % (c0 + slope*(math.log10(45)-math.log10(b0)), 0.126 - (c0 + slope*(math.log10(45)-math.log10(b0))),
         (0.126 - (c0 + slope*(math.log10(45)-math.log10(b0))))/0.126*100))
print('途径②（v5b 上限）：拓扑 ≤ %.2f、RWA ≥ %.2f' % (0.058/top_pred, 1-0.058/top_pred))
print('途径③（dex 比）：拓扑 %.2f、RWA %.2f' % (f, 1-f))
