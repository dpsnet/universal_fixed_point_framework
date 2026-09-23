# -*- coding: utf-8 -*-
# RN-ENDO-010 v1.1: Δ 工作定义转译 + 交换偏差桥核验
from mpmath import mp, mpf, sqrt, pi, e
mp.dps = 40
import numpy as np

print("== A. Δ 现存工作定义（paper35 spExchangeLaw 偏差）==")
LAM_MIN = (mpf(3)**mpf('0.5') - 1) / 6      # (√3−1)/6  SU(2) 谱间隙 k_max=8
LAM2    = (2 - 3**mpf('0.5')) / 18
R_CAT = mpf('0.040404')
D2 = R_CAT * LAM2
print(f"  Δλ_min = (√3−1)/6 = {mp.nstr(LAM_MIN,8)}")
print(f"  ‖Δ‖_F² = r_cat·Δλ_min² = {mp.nstr(D2,6)}  (global 单标量)")
print(f"  [诚实] Δλ_min 已含 √3 → 若用 Δ 直接导出 √3 为循环；须用非循环桥")

print("\n== B. 非循环桥: Δ=交换律偏差 ⟹ 反称部分 Λ²(d)=d(d-1)/2 = 配对计数 ==")
print("  交换算子 τ 在 V⊗V 分裂为对称⊕反称; '交换偏差' = 反称部维数 dim Λ²(V)")
print("  dim Λ²(V_d) = d(d-1)/2；梯子 λ = √(2·dim Λ²) = √(d(d-1))")
d = [2,3,4]
lam = [sqrt(x*(x-1)) for x in d]
antisym = [x*(x-1)/2 for x in d]
print("  d | dimΛ²=d(d-1)/2 | λ=√(2dimΛ²)=√(d(d-1)) | λ 中项归一")
for dd, a, l in zip(d, antisym, lam):
    print(f"  {dd} | {mp.nstr(a,4):>7}        | {mp.nstr(l,6):>10}          | {mp.nstr(l/lam[1],6)}")
print("  dimΛ² 严格递增 (1<3<6) → 任意交换偏差的单调函数在 d 上单调 ⟹ 序 P 成立候选")
print("  归一比值:", [mp.nstr(x/lam[1],8) for x in lam])
print("  1/√3:1:√2 匹配:", "OK" if abs((lam[0]/lam[1])-1/mpf(3)**mpf('0.5'))<1e-30 else "FAIL")

print("\n== C. 静默平凡层排除 (U(1)→d=2 的解析) ==")
print("  d=1 (全交换, dimΛ²=0) = 完全对称/静默层 → 被谱静默排除（框架原生）")
print("  U(1)=最交换活性扇区 → 最小非平凡交换偏差 dimΛ²(d=2)=1 → 落 d=2")
print("  序: U(1)→d=2 (Λ²=1) < SU(2)→d=3 (Λ²=3=伴随) < SU(3)→d=4 (Λ²=6)")

print("\n== D. 循环告警 (Δλ_min 层面) ==")
import numpy as np
dlam_np = (np.sqrt(3)-1)/6
lam2_np = np.sqrt(2)
print(f"  Δλ_min={dlam_np:.4f}  双态 λ(d=2)={lam2_np:.4f}  → 不同标度，不宜混用")
print(f"  [结论] 用 Δ(λ_min) 直接推 √3 循环；用 Δ(Λ²=I_G) 反称-交换桥则非循环，待建 Δ_i(Λ²) 逐扇区表达式")