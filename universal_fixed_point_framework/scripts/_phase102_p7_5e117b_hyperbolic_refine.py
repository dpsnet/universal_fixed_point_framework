# -*- coding: utf-8 -*-
"""
P7-5e-117b：双曲渐近形态精化——δ(m) = δ∞ − C/m 检验
====================================================
117 发现：三次外推在 m≥15 系统性失败（m=32 −47%），但 δ 平滑增长减速——
手算提示双曲形式 δ = δ∞ − C/m（δ·m 线性、C=(δ(m)−δ(m'))/(1/m−1/m')≈0.103 稳定）。
本脚本：系统拟合验证双曲形态 + δ∞ 身份候选（1/56 = 1/(7·8)）+ 过渡带定位。
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
p117 = json.load(open(os.path.join(BASE, "_phase102_p7_5e117_m32_scan.json"), encoding="utf-8"))
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
deltas = {int(k): v for k, v in fc["deltas"].items()}
for k, v in p117["out"].items():
    deltas[int(k)] = v["delta"]

# m=9..32 全序列（|m|）
mm = np.arange(9, 33, dtype=float)
dd = np.array([deltas[-k] for k in range(9, 33)])

print("== 双曲拟合 δ(m) = δ∞ − C/m ==", flush=True)
for m0 in [13, 14, 15, 16]:
    idx = np.where(mm >= m0)[0]
    X = np.vstack([np.ones(len(idx)), 1.0/mm[idx]]).T
    coef, res, _, _ = np.linalg.lstsq(X, dd[idx], rcond=None)
    d_inf, C = coef
    rms = float(np.sqrt(np.mean((X@coef - dd[idx])**2)))
    print("  m≥%d 拟合：δ∞=%.6f  C=%.6f  RMS=%.2e" % (m0, d_inf, C, rms), flush=True)

# 三参数：δ∞ − C/m − D/m²
print("", flush=True)
print("== 三参数（δ∞ − C/m − D/m²）m≥15 ==", flush=True)
idx = np.where(mm >= 15)[0]
X3 = np.vstack([np.ones(len(idx)), 1.0/mm[idx], 1.0/mm[idx]**2]).T
coef3, res3, _, _ = np.linalg.lstsq(X3, dd[idx], rcond=None)
rms3 = float(np.sqrt(np.mean((X3@coef3-dd[idx])**2)))
print("  δ∞=%.6f  C=%.6f  D=%.6f  RMS=%.2e" % (coef3[0], coef3[1], coef3[2], rms3), flush=True)

# δ∞ 身份候选：1/56 = 1/(7·8)
print("", flush=True)
d_inf_best = coef3[0]
print("  δ∞ vs 1/56 = %.8f（1/(7·8)，7=k_max−1）——偏差 %+.3f pct" % (1/56.0, (d_inf_best-1/56.0)/(1/56.0)*100), flush=True)

# 双曲 vs 三次：逐 m 预测残差对比（m=15..32）
print("", flush=True)
print("== 双曲 vs 三次外推预测（m=15..32 残差）==", flush=True)
# 三次（9..14 六点拟合）
m9 = np.arange(9, 15, dtype=float)
d9 = np.array([deltas[-k] for k in range(9, 15)])
A3 = np.vstack([np.ones(6), m9, m9**2, m9**3]).T
c3, _, _, _ = np.linalg.lstsq(A3, d9, rcond=None)
# 双曲（15..32 两参数）
m15 = np.arange(15, 33, dtype=float)
d15 = np.array([deltas[-k] for k in range(15, 33)])
Xh = np.vstack([np.ones(len(m15)), 1.0/m15]).T
ch, _, _, _ = np.linalg.lstsq(Xh, d15, rcond=None)
pred_cubic = c3[0] + c3[1]*m15 + c3[2]*m15**2 + c3[3]*m15**3
pred_hyper = ch[0] + ch[1]/m15
dev_c = np.abs(pred_cubic - d15)/d15*100
dev_h = np.abs(pred_hyper - d15)/d15*100
print("  m    实测δ      三次外推    偏差%%   双曲拟合    偏差%%", flush=True)
for i, m in enumerate(m15):
    print("  %2d  %.6f  %.6f  %+7.2f  %.6f  %+7.2f"
          % (m, d15[i], pred_cubic[i], (pred_cubic[i]-d15[i])/d15[i]*100,
             pred_hyper[i], (pred_hyper[i]-d15[i])/d15[i]*100), flush=True)
print("  三次外推 RMS = %.2e（m=15..32）——双曲拟合 RMS = %.2e" % (
    float(np.sqrt(np.mean((pred_cubic-d15)**2))),
    float(np.sqrt(np.mean((pred_hyper-d15)**2)))), flush=True)

# C 身份候选（框架量组合扫描）
print("", flush=True)
print("== C 身份候选扫描（C≈0.103）==", flush=True)
C_best = ch[1]
cands = {
    "1/56·5.78": 1/56.0*5.78,
    "κ/18.5": (6.0/np.pi)/18.5,
    "σ·1.55": (1/15.0)*1.55,
    "(1−σ)/8.6": (1-1/15.0)/8.6,
    "1/9.7": 1/9.7,
    "1/(7·√2)": 1/(7*np.sqrt(2)),
}
for name, val in cands.items():
    print("  %s = %.6f——偏差 %+.2f pct" % (name, val, (val-C_best)/C_best*100), flush=True)
print("  （全部为后验候选——诚实不立——仅登记）", flush=True)

# 过渡带：双曲残差在 m<15 的表现
print("", flush=True)
print("== 过渡带定位（双曲模型回代 m=9..14）==", flush=True)
for k in range(9, 15):
    pred = ch[0] + ch[1]/k
    dev = (pred - deltas[-k])/deltas[-k]*100
    print("  m=%2d  实测 %.6f  双曲回代 %.6f  偏差 %+.2f pct" % (k, deltas[-k], pred, dev), flush=True)

print("", flush=True)
print("exit 0", flush=True)
