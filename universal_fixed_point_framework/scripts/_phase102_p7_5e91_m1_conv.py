# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-91：m=-1 网格收敛判别 + B=1.5 au 单通道先验 + 通道数 8/8 确认
================================================================
P7-5e-90 统一闭式：1/B* = |m|/2 + 1/7 + 1/(7·2^|m|)——10 m 全 <0.16%、m=-1 先验 2.0%
开放判别：
  (1) m=-1 的 2% 残余——r_max 100/120 收敛检查（高场区数值伪影 or 真实修正缺口）
  (2) 通道数闭式 8/8（统一闭式修正 0.85 失败）——手算验证 + 脚本确认
  (3) ★★★ 新先验：B*(−1) = 1.4 au → B > 1.4 时负 m 全死 → 通道数 = 1（m=0 单通道）
      ——B=1.5 au 验证（此前无 >1.3 数据）
"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def e0_m(N_r, r_max, m, B, k=20):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
              offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return float(np.real(vals[0]))
    except Exception:
        return None

def bisect(m, r_max, lo, hi, iters=16):
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        E = e0_m(1500, r_max, m, mid)
        if E is not None and E > 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)

def count_channels(B, closed_func):
    """通道数 = 存活负 m 数 + m=0 通道（m=0 永存）——闭式 B*(m) > B 判定"""
    n = 0
    for m in range(-1, -12, -1):
        if closed_func(m) > B:
            n += 1
    return n + 1

print("="*104)
print("P7-5e-91：m=-1 收敛判别 + B=1.5 单通道先验 + 通道数 8/8")
print("="*104)

KMAX = 8
def closed(m):
    return 1.0/(abs(m)/2.0 + 1.0/(KMAX-1) + 1.0/((KMAX-1) * 2.0**abs(m)))

# (1) m=-1 收敛
print("【(1) m=-1 过零 r_max 收敛检查】（2% 残余判别：数值伪影 or 真实修正缺口）")
bs = {}
for rmax in [60, 80, 100, 120]:
    b = bisect(-1, rmax, 1.0, 2.0)
    bs[rmax] = b
    print("  r_max=%d: B* = %.4f au——1/B = %.6f——闭式差 %+.2f%%"
          % (rmax, b, 1.0/b, (1.0/b - closed(-1))/closed(-1)*100), flush=True)
spread = max(bs.values()) - min(bs.values())
print("  跨度 %.4f au——%s" % (spread, "稳定（2% 残余 = 真实修正缺口）" if spread < 0.01 else "漂移（数值伪影嫌疑）"))

# (2) 通道数 8/8
print()
print("【(2) 通道数闭式 8/8 确认】（统一闭式 B*(m) 判定——修正 0.85 失败）")
obs = {0.25: 8, 0.30: 7, 0.35: 6, 0.40: 5, 0.50: 4, 0.65: 3, 0.85: 2, 1.30: 2}
all_hit = True
for B in sorted(obs):
    n = count_channels(B, closed)
    hit = n == obs[B]
    all_hit &= hit
    print("  B=%.2f：观测 %d vs 统一闭式 %d %s" % (B, obs[B], n, "✓" if hit else "✗"))
print("  8/8 全命中：%s" % all_hit)

# (3) B=1.5 单通道先验
print()
print("【(3) B=1.5 au 单通道先验】（B*(−1)=1.4 → B>1.4 负 m 全死 → 通道=1）")
for m in [-1, 0]:
    E = e0_m(1500, 80, m, 1.5)
    print("  m=%+d @ B=1.5: E_0 = %.6f %s" % (m, E, "（存活）" if E is not None and E < 0 else "（已死/异常）"), flush=True)

json.dump({"m-1_rmax": {str(k): v for k, v in bs.items()},
           "channels": {str(B): count_channels(B, closed) for B in obs}},
          open(os.path.join(BASE, "_phase102_p7_5e91_m1_conv.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
