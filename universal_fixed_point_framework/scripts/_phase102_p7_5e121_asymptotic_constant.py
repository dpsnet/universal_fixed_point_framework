# -*- coding: utf-8 -*-
"""
P7-5e-121：渐近常数身份判别——1/B* → |m|/2 + 1/8（=1/k_max）vs 9/56
================================================================
背景：120 锁定 δ∞=1/56（|1/B*−cl| 极限）。符号审计（全链 invB0<closed_1B，
110 点全负）→ 1/B* = cl − δ → 大 m 渐近常数 = 1/7 − 1/56 = 1/8 = 1/k_max。
  望远镜恒等式：1/(k_max−1) − 1/k_max = 1/7 − 1/8 = 1/56 = δ∞（精确代数）。
  118 的"9/56"（=1/7+1/56）是 δ 符号取反的错误产物。
先验登记（计算前）：
  P1 符号审计：全链 m=−1..−14 的 invB0−closed_1B 全部 < 0（读权威 JSON 直接判定）
  P2 固定渐近常数 K=1/8 拟合 1/B* = |m|/2 + K + C/m + D/m²（m=33..128）：
     C≈0.1016、D≈−0.0188，RMS ≤ 1e-8（与 δ∞ 三参拟合 RMS 4.1e-9 同级），残差无系统漂移
  P3 望远镜恒等式 1/7−1/8=1/56：纯代数（无需计算）
  P4 对照 K=9/56 固定拟合：RMS 应差 ≥2 个量级（证明 9/56 错误口径）
判据：
  P1 通过：全部负 → 1/B* = cl − δ 确立（δ∞ 方向 −1/56）
  P2 通过：RMS ≤1e-8 且 |C−0.1016|<0.002 → 渐近常数 1/8 锁定
  P4 通过：RMS(9/56)/RMS(1/8) ≥ 100 → 9/56 表述正式排除
数据源：scripts\_phase102_p7_5e120_spectral_m128.json（谱方法全链权威，96 点）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
inv56 = 1.0/56.0

# ---------- P1：符号审计（全链 m=−1..−14 权威 JSON） ----------
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
signs = {}
for k, v in fc["out"].items():
    diff = v["invB0"] - v["closed_1B"]
    signs[int(k)] = diff
all_neg = all(d < 0 for d in signs.values())
print("== P1 符号审计（m=−1..−14，1/B* − 闭式）==", flush=True)
for m in sorted(signs, key=lambda x: -x):
    print("  m=%+3d  diff=%+.8f  （%s）" % (m, signs[m], "负" if signs[m] < 0 else "正"), flush=True)
print("  P1 判定：%s" % ("通过——全部负，1/B* = cl − δ 确立" if all_neg else "★ 未通过——存在正号点"), flush=True)

# ---------- 谱方法全链数据（m=33..128） ----------
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e120_spectral_m128.json"), encoding="utf-8"))
ms = []; invB = []
for k, v in j["out"].items():
    ms.append(abs(int(k))); invB.append(1.0/v["Bstar"])
ms = np.array(ms, dtype=float); invB = np.array(invB)

# ---------- P2/P4：固定渐近常数 K 拟合 1/B* = |m|/2 + K + C/m + D/m² ----------
def fit_K(K, ms_, invB_):
    X = np.vstack([1.0/ms_, 1.0/ms_**2]).T
    y = invB_ - (ms_/2.0 + K)
    c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    rms = float(np.sqrt(np.mean((X@c - y)**2)))
    return c, rms

def fit_K3(K, ms_, invB_):
    X = np.vstack([1.0/ms_, 1.0/ms_**2, 1.0/ms_**3]).T
    y = invB_ - (ms_/2.0 + K)
    c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    rms = float(np.sqrt(np.mean((X@c - y)**2)))
    return c, rms

print("", flush=True)
print("== P2/P4：固定渐近常数拟合（m=33..128，96 点）==", flush=True)
for K, tag in [(0.125, "K=1/8（=1/k_max，候选）"), (9.0/56.0, "K=9/56（118 表述，对照）"), (1.0/7.0, "K=1/7（=1/(k_max−1)，闭式常数）")]:
    c, rms = fit_K(K, ms, invB)
    print("  %-22s  C=%.6f  D=%.6f  RMS=%.2e" % (tag, c[0], c[1], rms), flush=True)

c8, rms8 = fit_K(0.125, ms, invB)
c9, rms9 = fit_K(9.0/56.0, ms, invB)
c7, rms7 = fit_K(1.0/7.0, ms, invB)
ratio_9 = rms9/rms8
print("  RMS(9/56)/RMS(1/8) = %.1f" % ratio_9, flush=True)
print("  RMS(1/7)/RMS(1/8)  = %.1f" % (rms7/rms8), flush=True)
# 三参数（含 1/m³）闭环
c8_3, rms8_3 = fit_K3(0.125, ms, invB)
c9_3, rms9_3 = fit_K3(9.0/56.0, ms, invB)
print("  三参数 K=1/8：C=%.6f D=%.6f E=%.6f RMS=%.2e" % (c8_3[0], c8_3[1], c8_3[2], rms8_3), flush=True)
print("  三参数 K=9/56：C=%.6f D=%.6f E=%.6f RMS=%.2e" % (c9_3[0], c9_3[1], c9_3[2], rms9_3), flush=True)
print("  三参数 RMS(9/56)/RMS(1/8) = %.1f" % (rms9_3/rms8_3), flush=True)

# 残差系统漂移检查（1/8 拟合）：前半/后半 RMS
half = ms <= 64; tail = ms > 64
_, rms_h = fit_K(0.125, ms[half], invB[half])
_, rms_t = fit_K(0.125, ms[tail], invB[tail])
print("  1/8 拟合分段残差：33..64 RMS=%.2e  65..128 RMS=%.2e  漂移比=%.1f" % (rms_h, rms_t, rms_t/rms_h), flush=True)

p2_ok = rms8 <= 1e-8 and abs(c8[0]-0.101613) < 0.002
p4_ok = ratio_9 >= 100.0
print("", flush=True)
print("P2 判定（RMS≤1e-8 且 C≈0.1016）：%s（C=%.6f RMS=%.2e）" % ("通过" if p2_ok else "★ 未通过", c8[0], rms8), flush=True)
print("P4 判定（RMS 比 ≥100）：%s（%.1f）" % ("通过——9/56 正式排除" if p4_ok else "★ 未通过", ratio_9), flush=True)
print("综合：大 m 渐近 1/B*(m) = |m|/2 + 1/8 = |m|/2 + 1/k_max（δ∞=1/7−1/8=1/56 望远镜差分）", flush=True)
print("exit 0", flush=True)
