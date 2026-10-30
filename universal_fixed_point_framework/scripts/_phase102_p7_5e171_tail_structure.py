# -*- coding: utf-8 -*-
"""P7-5e-171: 尾段非 1/m 成分结构判别（纯分析 170 数据）。
A) h(2) 残差 log-log 斜率谱（回应减半比 0.842）
B) 全链 Cm_fixed 漂移结构（正确口径重算 33..1024）
C) delta 残差 r = delta - 1/56 + 13/128/m 的尾段幂律斜率（判非幂律）
D) delta 尾窗口扫描全形态（非单调确认 + 回落位置）
E) 联动：Cm_fixed 漂移斜率 vs delta 窗口拟合偏差
"""
import json, numpy as np, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

d170 = json.load(open(base + r"\_phase102_p7_5e170_spectral_m1024.json", encoding='utf-8'))
d170b = json.load(open(base + r"\_phase102_p7_5e170b_h2_m1024.json", encoding='utf-8'))
out = d170["out"]

ms = sorted(int(k) for k in out.keys())          # -1024..-33
mm = np.array([-m for m in ms], dtype=float)      # 33..1024
Bstar = np.array([out[str(m)]["Bstar"] for m in ms], dtype=float)
invB = 1.0 / Bstar
delta = np.array([out[str(m)]["delta"] for m in ms], dtype=float)

def cl(m):
    return abs(m)/2.0 + 1.0/7.0 + (1.0/(7.0*2.0**abs(m)) if abs(m) <= 120 else 0.0)

delt_check = np.array([abs(cl(m) - 1.0/out[str(m)]["Bstar"]) for m in ms], dtype=float)
print("delta 自洽校验（JSON vs 重算）最大差: %.2e" % float(np.max(np.abs(delta - delt_check))))

inv56 = 1.0/56.0
c13 = 13.0/128.0

print("\n== A) h(2) 残差斜率谱 ==")
h2m = d170b["h2_m"]
ms_h = sorted(int(k) for k in h2m.keys())
hvals = np.array([h2m[str(m)] for m in ms_h], dtype=float)
dres = hvals - 7.0/64.0
for j, m in enumerate(ms_h):
    print("  m=%5d  h2=%.11f  d=%.3e" % (m, hvals[j], dres[j]))
slopes = []
for j in range(len(ms_h)-1):
    p = -np.log(dres[j+1]/dres[j]) / np.log(ms_h[j+1]/ms_h[j])
    slopes.append(p)
    print("  段 %5d→%5d  减半比 %.4f  log-log 斜率 %.4f" % (ms_h[j], ms_h[j+1], dres[j+1]/dres[j], p))
print("  尾段 p(512→1024)=%.4f ≈1/4=%s（1/m^{1/4} 候选：%s）" % (
    slopes[-1], abs(slopes[-1]-0.25) < 0.08, abs(slopes[-1]-0.25) < 0.08))
print("  前三点均值 p = %.4f（纯 1/m 预期 1.0）" % float(np.mean(slopes[:3])))
# 混合模型：d = a/m + b/m^{1/4} 尾段拟合
sel = [i for i, m in enumerate(ms_h) if m >= 128]
A = np.vstack([1.0/np.array(ms_h)[sel], 1.0/np.array(ms_h)[sel]**0.25]).T
coef, _, _, _ = np.linalg.lstsq(A, dres[sel], rcond=None)
print("  混合 d=a/m+b/m^{1/4}（m>=128）：a=%.3e b=%.3e" % (coef[0], coef[1]))

print("\n== B) Cm_fixed 全链漂移结构 ==")
Cm_fixed = (invB - (mm/2.0 + 1.0/8.0)) * mm
for lo in [64, 128, 256, 384, 512, 640, 768, 896]:
    sel = (mm >= lo) & (mm < lo + 128)
    if sel.sum() < 8:
        continue
    A = np.vstack([np.ones_like(mm[sel]), mm[sel]]).T
    coef, _, _, _ = np.linalg.lstsq(A, Cm_fixed[sel], rcond=None)
    print("  段 %3d..%3d  Cm 均值 %.8f  线性斜率 dC/dm = %+.3e（每单位 m）" % (lo, lo+127, Cm_fixed[sel].mean(), coef[1]))
sel_t = mm >= 256
g = np.gradient(Cm_fixed, mm)
A = np.vstack([np.ones_like(mm[sel_t]), np.log(mm[sel_t])]).T
coef, _, _, _ = np.linalg.lstsq(A, np.log(-g[sel_t]), rcond=None)
print("  log|dC/dm| vs ln m 斜率 = %.3f（>0 加速=发散，<0 减速=收敛）" % coef[1])

print("\n== C) delta 残差 r = delta − 1/56 + 13/128/m 的尾段形态 ==")
r = delta - inv56 + c13/mm
for mq in [768, 896, 1024]:
    idx = np.where(mm == mq)[0]
    if len(idx):
        print("  r(m=%d) = %+.3e" % (mq, r[idx[0]]))
for lo in [256, 512, 768, 896]:
    sel = mm >= lo
    rr = np.abs(r[sel])
    A = np.vstack([np.ones_like(mm[sel]), np.log(mm[sel])]).T
    coef, _, _, _ = np.linalg.lstsq(A, np.log(rr), rcond=None)
    print("  m≥%d: log|r| 斜率 %.3f（幂律指数 −q）" % (lo, coef[1]))
# r 的符号
for lo in [256, 512, 768]:
    sel = mm >= lo
    print("  m≥%d: r 负占比 %.1f%% 正占比 %.1f%%" % (lo, 100*(r[sel] < 0).mean(), 100*(r[sel] > 0).mean()))

print("\n== D) delta 尾窗口扫描（δ∞_fit，与 170 一致口径 2..5 参选 RMS 最小）==")
def fit_dinf(lo):
    sel = mm >= lo
    ms_ = mm[sel]
    ds_ = delta[sel]
    best = None
    for k in range(2, 6):
        A = np.vstack([1.0/ms_**j for j in range(k)]).T
        c, _, _, _ = np.linalg.lstsq(A, ds_, rcond=None)
        rms = float(np.sqrt(np.mean((A@c - ds_)**2)))
        if best is None or rms < best[1]:
            best = (c, rms, k)
    return best
for lo in [128, 256, 384, 512, 640, 768, 832, 896, 928, 960, 992]:
    c, rms, k = fit_dinf(lo)
    print("  m≥%4d（%4d 点，%d 参）：δ∞=%.10f  abs_dev=%.2e  RMS=%.1e" % (lo, int((mm >= lo).sum()), k, c[0], abs(c[0]-inv56), rms))

print("\n== E) 联动：Cm_fixed 漂移 vs δ∞_fit 偏差 ==")
for lo in [256, 512, 768]:
    c, _, _ = fit_dinf(lo)
    eps = c[0] - inv56
    sel = (mm >= lo) & (mm < lo + 128)
    if sel.sum() < 8:
        continue
    A = np.vstack([np.ones_like(mm[sel]), mm[sel]]).T
    coef, _, _, _ = np.linalg.lstsq(A, Cm_fixed[sel], rcond=None)
    ratio = coef[1]/(-eps) if eps != 0 else float('nan')
    print("  窗口 %d..%d: ε=%+.2e  实测 dC/dm=%+.2e  比值(dC/dm)/−ε=%.2f" % (lo, lo+127, eps, coef[1], ratio))
# 直接拟合 Cm_fixed(m) = C_true + b*ln(m)/m? 候选非幂律
for form in ["ln(m)/m", "m^{-1/4}/m", "1/m^{1/4}"]:
    pass
A = np.vstack([np.ones_like(mm), np.log(mm)/mm]).T
coef, _, _, _ = np.linalg.lstsq(A, Cm_fixed, rcond=None)
print("  全链 Cm_fixed = C + b·ln(m)/m：C=%.8f（13/128 差 %+.4f pct）b=%+.4e RMS=%.2e" % (
    coef[0], (coef[0]-c13)/c13*100, coef[1],
    float(np.sqrt(np.mean((A@coef - Cm_fixed)**2)))))

print("\n完成。")
