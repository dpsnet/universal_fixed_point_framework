# -*- coding: utf-8 -*-
"""
chain_audit_147_dh_rarity.py — d_H 0.01% 级判别：7-平滑分母空间最优有理近似 + 框架身份检查
目标：d_H* = 137.035999084/24 − 3 = 2.709833295（CODATA 口径）
"""
import math, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

T = 137.035999084/24 - 3
print(f"目标 d_H* = {T:.10f}")

# ---- 7-平滑数生成（素因子⊂{2,3,5,7}，≤ 50000）----
smooth = set()
for i2 in range(17):      # 2^16 = 65536 超限，取 2^15=32768
    for i3 in range(11):  # 3^10 = 59049
        for i5 in range(7):
            for i7 in range(6):
                n = 2**i2 * 3**i3 * 5**i5 * 7**i7
                if 0 < n <= 50000:
                    smooth.add(n)
smooth = sorted(smooth)
print(f"7-平滑数 ≤50000：{len(smooth)} 个")

# ---- 最优有理近似 ----
hits = []
for b in smooth:
    a = round(T * b)
    v = a / b
    err = abs(v - T)
    hits.append((err, a, b, v))
hits.sort()
print("\n=== Top 15 有理近似 ===")
for err, a, b, v in hits[:15]:
    print(f"  {a}/{b} = {v:.10f}  err={err:.3e}  dev={(v-T)/T*100:+.5f}%")

# ---- 框架身份检查：分子是否框架量组合 ----
def frame_comb(n):
    """n ∈ {k·d ± k', k^e ± k', 平滑积...} 粗查"""
    FR = {2,3,4,5,7,8,16,25,49,64}
    for k in FR:
        for kp in FR:
            if n in (k*45+kp, k*45-kp, k*64+kp, k*64-kp, k*15+kp, k*15-kp):
                return f"{n} = {k}·45±{kp} 或 {k}·64±{kp} 或 {k}·15±{kp}"
    for k in FR:
        if n == k**2+1 or n == k**2-1 or n == k**3+1 or n == k**3-1:
            return f"{n} = {k}^e±1"
    return None

print("\n=== Top 10 框架身份检查 ===")
for err, a, b, v in hits[:10]:
    f = frame_comb(a)
    print(f"  {a}/{b}  err={err:.3e}  分子身份: {f if f else '无'}")
