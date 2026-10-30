# -*- coding: utf-8 -*-
OUT = open(r'C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_117.txt', 'w', encoding='utf-8')
def P(*a):
    OUT.write(' '.join(map(str, a)) + '\n')

"""
Phase 104az-117（优化版）：静默分位一般化预言——四线交叉场强独立推导
方法：预计算加权密度 → cumsum CDF → 反插值分位（一次性全部分位，比二分重积分快 100 倍）
假说：交叉半径 = 每线 1/静默 分位半径 → B_cross(n) = ħC²/(e·r_n(0.2)²)
对照：C 定标四线（Hβ 81.1/Hγ 41.6/Hδ 19.8/Hε 9.5 MG）与观测（80/41/20/10 MG）
"""
import sys, math
import numpy as np
sys.path.insert(0, r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts')
from _phase100_p3b_compression import balmer_l_weights, radial_density

C2 = 4.0 * math.log(10.0)
HBAR, E_CH, A0 = 1.054571817e-34, 1.602176634e-19, 5.29177210903e-11

def cdf_array(n, npts=400000, rmax=800.0):
    wl = balmer_l_weights(n)
    r = np.linspace(1e-8, rmax, npts)
    dens = np.zeros(npts)
    for l, w in wl.items():
        dens += w * np.array([radial_density(n, l, x) for x in r])
    cdf = np.cumsum(dens)
    cdf /= cdf[-1]
    return r, cdf

def quantiles_from_cdf(r, cdf, qs):
    # CDF 反插值
    return {q: float(np.interp(q, cdf, r)) for q in qs}

def b_cross_mg(r_a0):
    return HBAR * C2 / (E_CH * (r_a0 * A0)**2) / 100.0

P("=== 静默分位一般化预言：四线交叉场强 ===")
lines = {4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}
obs = {4: 80.0, 5: 41.0, 6: 20.0, 7: 10.0}
cfit = {4: 81.1, 5: 41.6, 6: 19.8, 7: 9.5}

qs_all = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
res = {}
for n in [4, 5, 6, 7]:
    r, cdf = cdf_array(n)
    rq = quantiles_from_cdf(r, cdf, qs_all)
    res[n] = rq
    P("%s(n=%d)：r(0.2) = %.4f a₀ → B_pred = %.2f MG" % (lines[n], n, rq[0.2], b_cross_mg(rq[0.2])))
    P("    观测 %g MG（dev %+.2f%%）| C 定标 %g MG（dev %+.2f%%）" %
      (obs[n], 100.0*(b_cross_mg(rq[0.2])-obs[n])/obs[n], cfit[n], 100.0*(b_cross_mg(rq[0.2])-cfit[n])/cfit[n]))

P("\n=== 对照汇总 ===")
P("线 | 观测 | C定标(dev) | 静默分位(dev vs 观测) | dev vs C定标")
ws = []
for n in [4, 5, 6, 7]:
    rq = res[n][0.2]
    Bp = b_cross_mg(rq)
    dev_obs = 100.0 * (Bp - obs[n]) / obs[n]
    dev_c = 100.0 * (Bp - cfit[n]) / cfit[n]
    ws.append(abs(dev_obs))
    P("%s | %g | %g (%+.2f%%) | %g (%+.2f%%) | %+.2f%%" % (lines[n], obs[n], cfit[n], 100.0*(cfit[n]-obs[n])/obs[n], Bp, dev_obs, dev_c))
P("\n静默分位加权 |dev| vs 观测 = %.2f%%（C 定标加权 |dev| = 1.65%%）" % (sum(ws)/4.0))

P("\n=== 判别：q=0.2 是否唯一最优 ===")
for n in [4, 5, 6, 7]:
    devs = {}
    for q in qs_all:
        Bq = b_cross_mg(res[n][q])
        devs[q] = abs(100.0 * (Bq - obs[n]) / obs[n])
    best = min(devs, key=devs.get)
    rank = sorted(devs.values()).index(devs[0.2]) + 1
    P("%s：最优 q = %s（dev %.2f%%），q=0.2 dev %.2f%%（排名 %d/%d）" %
      (lines[n], best, devs[best], devs[0.2], rank, len(qs_all)))
