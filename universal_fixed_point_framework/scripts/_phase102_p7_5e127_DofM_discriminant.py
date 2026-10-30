# -*- coding: utf-8 -*-
"""
P7-5e-127：D 是否真是 m 的函数——判别实验（用户先验，2026-10-14）
================================================================
P1 滑动窗口 D 形态：129..256 段窗 48 步 16 滑扫——平滑趋势=真实 D(m)；阶跃=窗口效应
P2 残差谱：全链 33..256 三参拟合残差 vs m 分段——白噪声=模型完整（D 常数）；结构=缺项
P3 条件数诊断 + 固定 δ∞=1/56 隔离后 D 漂移形态（隔离 δ∞↔D 相关）
数据源：_phase102_p7_5e124_spectral_m256.json（224 点权威）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))
out = j["out"]

def get_data(lo, hi):
    ms = np.array([abs(int(k)) for k in out if lo <= -int(k) <= hi], dtype=float)
    invB = np.array([1.0/out[k]["Bstar"] for k in out if lo <= -int(k) <= hi])
    order = np.argsort(ms); ms = ms[order]; invB = invB[order]
    cl = ms/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**ms)
    delta = cl - invB
    return ms, delta

def fit3(ms, delta):
    X = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
    c, _, _, _ = np.linalg.lstsq(X, delta, rcond=None)
    rms = float(np.sqrt(np.mean((X@c-delta)**2)))
    return c[0], -c[1], -c[2], rms

print("=== P1 滑动窗口 D 形态（129..256，窗 48 步 16）===", flush=True)
starts = list(range(129, 256-48+1, 16))
Ds = []
for s in starts:
    ms, delta = get_data(s, s+47)
    d, C, D, rms = fit3(ms, delta)
    Ds.append(D)
    print("  m=%d..%d  D=%+.6f  δ∞=%.8f  C=%+.6f  RMS=%.1e" % (s, s+47, D, d, C, rms), flush=True)
print("  D 序列 = %s" % ("、".join("%+.4f" % d for d in Ds)), flush=True)
if len(Ds) >= 2:
    dd = np.diff(Ds)
    print("  D 相邻差 = %s（平滑趋势→小差连续；窗口效应→大差跳变）" % ("、".join("%+.4f" % x for x in dd)), flush=True)
    print("  D 极差 = %.4f（窗 48 内 D 变化幅度）" % (max(Ds)-min(Ds)), flush=True)

print("=== P2 全链三参拟合残差谱（33..256，RMS/结构）===", flush=True)
ms, delta = get_data(33, 256)
X = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
c, _, _, _ = np.linalg.lstsq(X, delta, rcond=None)
res = delta - X@c
print("  全链 RMS = %.2e、|max| = %.2e（机器精度级=模型完整；>1e-6 有结构）" % (np.sqrt(np.mean(res**2)), np.max(np.abs(res))), flush=True)
for lo, hi in [(33,96),(97,128),(129,192),(193,256)]:
    msk = (ms>=lo)&(ms<=hi)
    r = res[msk]
    ac = np.corrcoef(r[:-1], r[1:])[0,1] if len(r) > 2 else float('nan')
    print("  段 %d..%d：残差均值 %+.2e、|max| %.2e、lag-1 自相关 %+.2f" % (lo, hi, r.mean(), np.max(np.abs(r)), ac), flush=True)

print("=== P3 条件数诊断 + 固定 δ∞ 隔离 ===", flush=True)
for lo, hi in [(129,192),(193,256),(129,256),(33,128)]:
    ms, delta = get_data(lo, hi)
    X = np.vstack([np.ones_like(ms), 1.0/ms, 1.0/ms**2]).T
    cond = np.linalg.cond(X)
    # 固定 δ∞=1/56：delta - 1/56 = -C/m - D/m² → 两参
    X2 = np.vstack([1.0/ms, 1.0/ms**2]).T
    c2, _, _, _ = np.linalg.lstsq(X2, delta - 1.0/56.0, rcond=None)
    print("  段 %d..%d：条件数 %.1e；固定 δ∞=1/56 后 C=%+.6f D=%+.6f" % (lo, hi, cond, -c2[0], -c2[1]), flush=True)
print("exit 0", flush=True)
