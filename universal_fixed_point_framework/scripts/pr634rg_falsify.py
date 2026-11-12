# -*- coding: utf-8 -*-
"""第 55 批 模式 8 数值先证伪：
   命题 A：R1（Cauchy 复合乘性 ⇒ w_k = s^k）只锁定形式，s 自由
           —— 对任意 s ∈ (0,1)，w_k = s^k 满足 w(k+l) = w(k)w(l)
   命题 B：给定 B = 15，Moran 方程 15 * s^ln15 = 1 的 s 解唯一 = e^-1
           —— 即「要求 d_H = ln 15」⟺「s = e^-1」（不是两条独立信息）
   命题 C：s ↔ d 双射：d = ln15 / (-ln s)，s = exp(-ln15/d)
   命题 D：s ≠ e^-1 时 d ≠ ln 15，并给出偏离量（证明 s 的取值直接决定 d）
"""
import math

LN15 = math.log(15)
EINV = math.exp(-1)

print("== A. R1 只锁形式：任意 s in (0,1) 都给指数族 ==")
bad_a = []
for i in range(1, 200):
    s = i / 200.0
    for k in range(0, 8):
        for l in range(0, 8):
            wk = s ** k
            wl = s ** l
            wkl = s ** (k + l)
            if abs(wkl - wk * wl) > 1e-12:
                bad_a.append((s, k, l))
                break
print("CAUCHY_FAILS", bad_a[:5], "COUNT", len(bad_a))
print("A_FORM_FAMILY_FREE", len(bad_a) == 0)

print("== B. 给定 B=15，要求 d = ln15 ⇒ s 唯一 = e^-1 ==")
bad_b = []
for i in range(1, 400):
    s = i / 400.0
    ok = abs(15.0 * (s ** LN15) - 1.0) < 1e-9
    is_e = abs(s - EINV) < 1e-9
    if ok != is_e:
        bad_b.append((s, ok, is_e))
print("B_FAILS", bad_b[:5], "COUNT", len(bad_b))
print("B_PIN_UNIQUE", len(bad_b) == 0)
print("CHECK_AT_EINV", 15.0 * (EINV ** LN15))
print("EINV", EINV, "LN15", LN15)

print("== C. s <-> d 双射 ==")
bad_c = []
for i in range(1, 400):
    s = i / 400.0
    d = LN15 / (-math.log(s))
    s_back = math.exp(-LN15 / d)
    if abs(s_back - s) > 1e-12:
        bad_c.append((s, d, s_back))
print("C_FAILS", bad_c[:5], "COUNT", len(bad_c))
print("C_BIJECTION_OK", len(bad_c) == 0)

print("== D. s 的取值直接决定 d（偏离 e^-1 即偏离 ln15）==")
rows = []
for s in (math.exp(-2), 0.5, math.exp(-1), 0.36, math.exp(-0.5)):
    d = LN15 / (-math.log(s))
    rows.append((s, -math.log(s), d, d - LN15))
for s, nls, d, dev in rows:
    print("S %.9f  -LOGS %.6f  D %.9f  DEVIATION_FROM_LN15 %.9f" % (s, nls, d, dev))
print("S_AT_EINV_GIVES_LN15", abs(rows[2][3]) < 1e-12)

print("== E. 唯象对照：d_fit = 2.7095 反推 s，与 e^-1 比较 ==")
d_fit = 2.7095
s_from_fit = math.exp(-LN15 / d_fit)
print("S_FROM_DFIT %.9f" % s_from_fit)
print("S_EINV     %.9f" % EINV)
print("REL_DEV    %.6e" % ((s_from_fit - EINV) / EINV))
print("D_AT_EINV  %.9f  D_FIT %.6f  DELTA %.9f" % (LN15, d_fit, d_fit - LN15))

print("VERDICT_A", len(bad_a) == 0)
print("VERDICT_B", len(bad_b) == 0)
print("VERDICT_C", len(bad_c) == 0)
print("VERDICT_ALL_OK", len(bad_a) == 0 and len(bad_b) == 0 and len(bad_c) == 0)
