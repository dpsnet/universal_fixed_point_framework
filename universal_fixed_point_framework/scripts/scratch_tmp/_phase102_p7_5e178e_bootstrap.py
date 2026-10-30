# -*- coding: utf-8 -*-
"""
P7-5e-178e: F4/E 联合提取的 bootstrap 不确定度（定案检验）
=============================================================
178d 发现：33..128 段四参自由拟合 F4≈+0.004（E 自由）vs 176b 固定 E 后 F4=−0.035。
本版用 bootstrap（重采样 33..128 段 48 点）给出 F4/E 的统计误差条，判定：
  ① F4 是否与 0 区分（|F4| vs 误差）
  ② F4 是否与 −1/32=−0.03125 区分
  ③ E 是否与 +41/2000=+0.0205 区分（E 假设的统计状态）
"""
import json, numpy as np, os

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(SCRIPTS, "_phase102_p7_5e178e_out.txt")

def load_delta(fn):
    d = json.load(open(os.path.join(SCRIPTS, fn), encoding="utf-8"))
    return np.array(d["m"]), np.array(d["delta"])

m1, d1 = load_delta("_phase102_p7_5e175_delta63.json")
m2, d2 = load_delta("_phase102_p7_5e176_delta_lowm.json")
m = np.concatenate([m1, m2]); dl = np.concatenate([d1, d2])
order = np.argsort(m); m, dl = m[order], dl[order]
uniq = np.unique(m, return_index=True)[1]; m, dl = m[uniq], dl[uniq]

n = m
cl = n/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**n)
delta = dl

lines = []
def P(s=""):
    lines.append(s); print(s)

P("="*100)
P("P7-5e-178e: F4/E bootstrap 不确定度（33..128 段四参自由拟合）")
P(f"数据：{len(m)} 点；窗口 m=33..128（48 点）")
P("模型：δ = 1/56 − C/m − D/m^2 + E/m^3 + F4/m^4（四参自由）")
P("="*100)

mask = (n>=33)&(n<=128)
ns = n[mask]; ds = delta[mask]

def fit(ns_, ds_):
    A = np.vstack([1.0/ns_, 1.0/ns_**2, 1.0/ns_**3, 1.0/ns_**4]).T
    c, _, _, _ = np.linalg.lstsq(A, ds_ - 1.0/56.0, rcond=None)
    return c  # C, D, E, F4

# 点估计
c0 = fit(ns, ds)
P(f"点估计：C={c0[0]:+.9f}  D={c0[1]:+.9f}  E={c0[2]:+.9f}  F4={c0[3]:+.9f}")
P(f"  C 距 13/128：{(c0[0]+13/128)/(13/128)*100:+.3f}%  D 距 41/2000：{(c0[1]+41/2000)/(41/2000)*100:+.3f}%")
P(f"  E 距 +41/2000：{(c0[2]-41/2000)/(41/2000)*100:+.3f}%  F4 距 -1/32：{(c0[3]+1/32)/(1/32)*100:+.2f}%")

# bootstrap
rng = np.random.default_rng(20261015)
NBOOT = 2000
Cb = np.zeros(NBOOT); Db = np.zeros(NBOOT); Eb = np.zeros(NBOOT); Fb = np.zeros(NBOOT)
for i in range(NBOOT):
    idx = rng.integers(0, len(ns), len(ns))
    c = fit(ns[idx], ds[idx])
    Cb[i], Db[i], Eb[i], Fb[i] = c

def stats(x, name):
    lo, med, hi = np.percentile(x, [2.5, 50, 97.5])
    sd = x.std()
    P(f"  {name}: 中位={med:+.8f}  σ={sd:.2e}  95%CI=[{lo:+.8f}, {hi:+.8f}]")
    return med, sd, lo, hi

P("\n[bootstrap 2000 次]")
P("-"*100)
mC, sC, lC, hC = stats(Cb, "C")
mD, sD, lD, hD = stats(Db, "D")
mE, sE, lE, hE = stats(Eb, "E")
mF, sF, lF, hF = stats(Fb, "F4")

P("\n[判定]")
P("-"*100)
# F4 vs 0
zF0 = mF/sF
P(f"  F4 = {mF:+.6f} ± {sF:.4f}：F4 vs 0 的 z={zF0:+.2f}（{'与 0 不显著区分（≈0）' if abs(zF0)<2 else '显著非零'}）")
# F4 vs -1/32
zFneg = (mF + 1.0/32.0)/sF
P(f"  F4 vs −1/32=−0.03125：差={mF+1/32:+.6f}，z={zFneg:+.2f}（{'−1/32 在 95%CI 内' if lF<-1/32<hF else '−1/32 排除'}）")
# E vs 41/2000
zE = (mE - 41.0/2000.0)/sE
P(f"  E = {mE:+.6f} ± {sE:.4f}：E vs +41/2000 的 z={zE:+.2f}（{'与 41/2000 不显著区分' if abs(zE)<2 else '显著偏离 41/2000'}）")
P(f"  E 的 95%CI=[{lE:+.6f},{hE:+.6f}]，41/2000={41/2000:.6f} {'在 CI 内' if lE<41/2000<hE else '在 CI 外'}")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
