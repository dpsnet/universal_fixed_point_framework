# -*- coding: utf-8 -*-
"""
P7-5e-165：C 终判高阶展开系统判别（13/128 vs 0.1016）
================================================================
背景（160/164）：三参 Richardson 三对不一致（散度 1.19%），C 终判未达成。
本步系统判别（数据 160 全链 480 点，数值面已饱和 164）：
  A. C_m 含 E/m² 高阶外推：C_m(m) = C + D/m + E/m² —— 三点/四点最小二乘解 C
  B. 全局 k 参拟合 delta：δ∞ + C/m + D/m² + E/m³（4 参）+ F/m⁴（5 参）—— C 收敛 vs 参数量
  C. 窗口扫描：C 三参拟合 vs m_min（33..200 步进）—— 窗口稳定性
  D. 大 m 加权：w=m²/m³ 加权最小二乘 —— C 收敛端
判别：多通道 C 一致收敛到 0.1015625±2e-5 → 13/128 锁定；0.1016±2e-5 → 维持；否则开放
注：delta(m) = cl − 1/B* = 1/56 − C/m − D/m² − ...（164b）；拟合模型 delta = δ∞ + C'/m + D'/m² 的
    C' 应为负（符号以数据为准，报告时标注通道符号约定）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
d160 = json.load(open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), encoding="utf-8"))
out = d160["out"]

# 480 点 delta 与 m（m=33..512）
ms = np.arange(33, 513, dtype=float)
ds = np.array([out[str(m)]["delta"] for m in range(-33, -513, -1)])
inv56 = 1.0/56.0
c13_128 = 13.0/128.0
c1016 = 0.1016
c10158 = 0.10158

print("== P7-5e-165：C 终判高阶展开系统判别（480 点全链）==", flush=True)

# ---------- A. C_m 含 E/m² 高阶外推 ----------
print("\n=== A) C_m 高阶外推（C_m = C + D/m + E/m²）===", flush=True)
inv8 = 1.0/8.0
def Cm(m):
    invB = 1.0/out[str(-m)]["Bstar"]
    return (invB - (abs(m)/2.0 + inv8)) * abs(m)
mm = np.array([128.0, 256.0, 384.0, 512.0])
cm = np.array([Cm(m) for m in [128, 256, 384, 512]])
X_A = np.vstack([np.ones(4), 1.0/mm, 1.0/mm**2]).T
cA, _, _, _ = np.linalg.lstsq(X_A, cm, rcond=None)
rA = float(np.sqrt(np.mean((X_A@cA - cm)**2)))
print("  四点拟合：C = %.8f  D = %.5f  E = %.4f  RMS = %.2e" % (cA[0], cA[1], cA[2], rA), flush=True)
# 三点（256,384,512）消 E 前的三参
X3p = np.vstack([np.ones(3), 1.0/mm[1:], 1.0/mm[1:]**2]).T
cA3, _, _, _ = np.linalg.lstsq(X3p, cm[1:], rcond=None)
print("  三点(256,384,512)：C = %.8f  D = %.5f  E = %.4f" % (cA3[0], cA3[1], cA3[2]), flush=True)
# 四点两参（消 E？不——两参会吸收 E）
X_A2 = np.vstack([np.ones(4), 1.0/mm]).T
cA2, _, _, _ = np.linalg.lstsq(X_A2, cm, rcond=None)
print("  四点两参：C = %.8f  D = %.5f（E 被吸收——参考）" % (cA2[0], cA2[1]), flush=True)
print("  A 判别：含 E 项后 C = %.8f" % cA[0], flush=True)

# ---------- B. 全局 k 参拟合 delta ----------
print("\n=== B) 全局 k 参拟合（delta = δ∞ + C/m + D/m² + E/m³ + F/m⁴）===", flush=True)
for k in [2, 3, 4, 5]:
    X = np.vstack([1.0/ms**j for j in range(k)]).T
    c, _, _, _ = np.linalg.lstsq(X, ds, rcond=None)
    r = float(np.sqrt(np.mean((X@c - ds)**2)))
    names = ["δ∞", "C", "D", "E", "F"]
    vals = ", ".join("%s=%.6f" % (names[j], c[j]) for j in range(k))
    print("  %d 参：%s  RMS=%.2e  δ∞dev=%+.5f pct" % (k, vals, r, (c[0]-inv56)/inv56*100), flush=True)

# ---------- C. 窗口扫描 ----------
print("\n=== C) C 三参拟合 vs m_min（窗口稳定性）===", flush=True)
prev_C = None
for mmin in [33, 64, 96, 128, 160, 192, 224, 256]:
    idx = ms >= mmin
    X = np.vstack([np.ones(idx.sum()), 1.0/ms[idx], 1.0/ms[idx]**2]).T
    c, _, _, _ = np.linalg.lstsq(X, ds[idx], rcond=None)
    r = float(np.sqrt(np.mean((X@c - ds[idx])**2)))
    drift = "" if prev_C is None else "  ΔC=%+.5f" % (c[1]-prev_C)
    print("  m≥%3d：δ∞=%.8f  C=%+.6f  D=%+.6f  RMS=%.1e%s" % (mmin, c[0], c[1], c[2], r, drift), flush=True)
    prev_C = c[1]

# ---------- D. 大 m 加权 ----------
print("\n=== D) 加权拟合（w = m² / m³，强调大 m）===", flush=True)
for wname, wf in [("m²", lambda m: m**2), ("m³", lambda m: m**3)]:
    w = wf(ms)
    X = np.vstack([np.ones(480), 1.0/ms, 1.0/ms**2]).T
    W = np.diag(w)
    c, _, _, _ = np.linalg.lstsq(np.sqrt(W)@X, np.sqrt(W)@ds, rcond=None)
    print("  w=%s：δ∞=%.8f  C=%+.6f  D=%+.6f" % (wname, c[0], c[1], c[2]), flush=True)

# ---------- 判别 ----------
print("\n=== 判别 ===", flush=True)
# 汇总各通道 C（注意 B 通道符号：拟合 C' 若为负则 C_true = -C'）
c_A = cA[0]                       # C_m 通道（正 C）
c_B3 = None
c_B4 = None
# 重新取 B 通道值
results_B = {}
for k in [2, 3, 4, 5]:
    X = np.vstack([1.0/ms**j for j in range(k)]).T
    c, _, _, _ = np.linalg.lstsq(X, ds, rcond=None)
    results_B[k] = c
c_B3 = results_B[3][1]
c_B4 = results_B[4][1]
c_B5 = results_B[5][1]
print("  通道汇总：", flush=True)
print("  A) C_m 四参外推：C = %+.8f" % c_A, flush=True)
print("  B) 全局三参 delta：C' = %+.8f → C_true = %+.8f（若 C'=−C_true）" % (c_B3, -c_B3), flush=True)
print("  B) 全局四参 delta：C' = %+.8f → C_true = %+.8f" % (c_B4, -c_B4), flush=True)
print("  B) 全局五参 delta：C' = %+.8f → C_true = %+.8f" % (c_B5, -c_B5), flush=True)

# 一致性判别（用 A 与 B 的 C_true 与候选比对）
cands = [c_A, -c_B3, -c_B4, -c_B5]
names_c = ["A(C_m四参)", "B3(-C')", "B4(-C')", "B5(-C')"]
spread = (max(cands)-min(cands))/abs(np.mean(cands))*100
print("  多通道散布：%.3f pct（max-min）/mean" % spread, flush=True)
for name, v in zip(names_c, cands):
    print("  %s：C=%+.8f  vs 13/128 差 %+.5f pct；vs 0.1016 差 %+.5f pct" %
          (name, v, (v-c13_128)/c13_128*100, (v-c1016)/c1016*100), flush=True)

# 终判
C_mean = float(np.mean(cands))
if abs(C_mean - c13_128) < 2.0e-5 and spread < 0.2:
    verdict = "★★★ C = 13/128 锁定（均值 %.8f，散布 %.3f pct）" % (C_mean, spread)
elif abs(C_mean - c1016) < 2.0e-5 and spread < 0.2:
    verdict = "★★★ C = 0.1016 维持（均值 %.8f，散布 %.3f pct）" % (C_mean, spread)
else:
    verdict = "★ C 仍开放（均值 {0:.8f}，散布 {1:.3f} pct——13/128 与 0.1016 差 0.037% 小于散布）".format(C_mean, spread)
print("  终判：%s" % verdict, flush=True)
print("  诚实边界：多通道符号约定不同（C_m 正 C；delta 拟合 C' 取 −C'）；散布反映高阶项未完全扣除", flush=True)

out_j = {"A_Cm_4pt_3p": {"C": float(cA[0]), "D": float(cA[1]), "E": float(cA[2]), "rms": rA},
         "A_Cm_3pt": {"C": float(cA3[0])},
         "B_global": {str(k): {"coef": results_B[k].tolist(), "C_true_if_minus": float(-results_B[k][1]) if k >= 3 else None} for k in [2,3,4,5]},
         "C_window": {}, "D_weighted": {},
         "channels": {n: float(v) for n, v in zip(names_c, cands)},
         "spread_pct": float(spread), "verdict": verdict}
with open(os.path.join(BASE, "_phase102_p7_5e165_c_final_higher.json"), "w", encoding="utf-8") as f:
    json.dump(out_j, f, indent=1, ensure_ascii=False)
print("JSON 落盘 OK exit 0", flush=True)
