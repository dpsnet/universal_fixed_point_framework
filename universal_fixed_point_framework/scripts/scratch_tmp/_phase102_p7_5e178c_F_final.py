# -*- coding: utf-8 -*-
"""
P7-5e-178c: F(m) 弱 m 依赖判别（最终版——大窗口 + 基逐步扩展 + 窗口滑动）
=======================================================================
178/178b 教训：窄窗口(8~16 点)+高阶基近似线性相关 → 参数爆炸非物理。
本版：固定 C=13/128、D 双项（E=+41/2000 已并入 1/m^3），
  w(m) = m^4 * r(m) = F4 + F5/m + F6/m^2 + F7/m^3
用大窗口拟合，基逐步扩展 {1}→{1,1/m}→{1,1/m,1/m^2}→{1,1/m,1/m^2,1/m^3}，
观察 F4 的收敛与窗口滑动稳定性。

候选：F4 = -1/32 = -0.03125（176 口径"残差 1/m^4 项 F=-0.0312"）。
"""
import json, numpy as np, os

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(SCRIPTS, "_phase102_p7_5e178c_out.txt")

def load_delta(fn):
    d = json.load(open(os.path.join(SCRIPTS, fn), encoding="utf-8"))
    return np.array(d["m"]), np.array(d["delta"])

m1, d1 = load_delta("_phase102_p7_5e175_delta63.json")
m2, d2 = load_delta("_phase102_p7_5e176_delta_lowm.json")
m = np.concatenate([m1, m2]); dl = np.concatenate([d1, d2])
order = np.argsort(m); m, dl = m[order], dl[order]
uniq = np.unique(m, return_index=True)[1]; m, dl = m[uniq], dl[uniq]

C128 = 13.0/128.0
D41 = 41.0/2000.0
n = m
cl = n/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**n)
r = dl - 1.0/56.0 + C128/n + D41*(1.0/n**2 - 1.0/n**3)
w = n**4 * r

lines = []
def P(s=""):
    lines.append(s); print(s)

P("="*100)
P("P7-5e-178c: F(m) 弱 m 依赖判别最终版（大窗口 + 基逐步扩展 + 窗口滑动）")
P(f"数据：{len(m)} 点；判别窗口 m>=33：{(n>=33).sum()} 点")
P("w(m) = m^4·r = F4 + F5/m + F6/m^2 + F7/m^3；候选 F4 = -1/32 = -0.03125")
P("="*100)

# 基逐步扩展：对同一窗口，从 1 参到 4 参，看 F4 收敛
def fit_ext(ns, ws, kmax):
    cols = [np.ones_like(ns)]
    for k in range(1, kmax):
        cols.append(1.0/ns**k)
    A = np.vstack(cols).T
    c, _, _, _ = np.linalg.lstsq(A, ws, rcond=None)
    rms = np.sqrt(np.mean((ws - A@c)**2))
    return c, rms

P("\n[基逐步扩展]  m=33..128 窗口（48 点）")
P("-"*100)
ns = n[(n>=33)&(n<=128)]; ws = w[(n>=33)&(n<=128)]
for kmax in [1, 2, 3, 4]:
    c, rms = fit_ext(ns, ws, kmax)
    dneg = (c[0]+1.0/32.0)/(1.0/32.0)*100
    P(f"  基 {{1,..,1/m^{kmax-1}}}：F4={c[0]:+.8f}（距 -1/32 {dneg:+8.2f}%）  F5={c[1] if kmax>1 else 0:+.6f}  F6={c[2] if kmax>2 else 0:+.6f}  F7={c[3] if kmax>3 else 0:+.6f}  RMS={rms:.3e}")

P("\n[窗口滑动稳定性]  四参基 {1,1/m,1/m^2,1/m^3}，起点 33，终点滑动")
P("-"*100)
for hi in [64, 96, 128, 160, 192, 256]:
    mask = (n>=33)&(n<=hi)
    if mask.sum() < 8: continue
    c, rms = fit_ext(n[mask], w[mask], 4)
    dneg = (c[0]+1.0/32.0)/(1.0/32.0)*100
    P(f"  m=33..{hi:4d}  N={mask.sum():4d}  F4={c[0]:+.8f}（距 -1/32 {dneg:+8.2f}%）  F5={c[1]:+.6f}  F6={c[2]:+.6f}  F7={c[3]:+.6f}  RMS={rms:.3e}")

P("\n[起点滑动]  终点 256 固定，起点滑动（避开过渡带 m=17..32）")
P("-"*100)
for lo in [33, 41, 49, 57, 65]:
    mask = (n>=lo)&(n<=256)
    if mask.sum() < 8: continue
    c, rms = fit_ext(n[mask], w[mask], 4)
    dneg = (c[0]+1.0/32.0)/(1.0/32.0)*100
    P(f"  m={lo:4d}..256  N={mask.sum():4d}  F4={c[0]:+.8f}（距 -1/32 {dneg:+8.2f}%）  F5={c[1]:+.6f}  F6={c[2]:+.6f}  F7={c[3]:+.6f}  RMS={rms:.3e}")

# Richardson 配对消 F5：w(n) - w(2n)/16  (r 层：r=F4/m^4+F5/m^5+...; 16*r(2m) = F4/m^4+F5/2m^5+...; r(m)-16r(2m) = F5/2/m^5 + 3F6/4/m^6)
P("\n[Richardson 消 F5]  q(m) = m^5*[r(m) - 16*r(2m)] = F5/2 + (3F4?)... 直接用 w 配对：")
P("  w(n) - 16*w(2n)/16 = F4+F5/n+... - (F4+F5/(2n)+...) = F5/(2n) + 3F6/(4n^2) + ...")
P("-"*100)
maskL = (n>=33)&(n<=256)
ns_ = n[maskL]; ws_ = w[maskL]
pairs = []
for ni, wi in zip(ns_, ws_):
    if (ni*2) in ns_:
        pairs.append((ni, wi, ws_[ns_==ni*2][0]))
pairs = np.array(pairs)
if len(pairs) >= 4:
    qn = pairs[:,0]*(pairs[:,1] - pairs[:,2]/16.0)
    # q = F5/2 + 3F6/(4n) + 7F7/(8n^2)
    A = np.vstack([np.ones_like(pairs[:,0]), 1.0/pairs[:,0], 1.0/pairs[:,0]**2]).T
    c, _, _, _ = np.linalg.lstsq(A, qn, rcond=None)
    P(f"  {len(pairs)} 对 (33..256)：q 常数项={c[0]:+.6f}（=F5/2 → F5={2*c[0]:+.6f}）  1/n 项={c[1]:+.6f}（=3F6/4）  1/n^2 项={c[2]:+.6f}  RMS={np.sqrt(np.mean((qn-A@c)**2)):.3e}")

P("\n" + "="*100)
P("判定要点：")
P("  ① 若 F4 跨窗口稳定 → 常数（定符号与值，与 -1/32 比较）")
P("  ② 若 F4 随终点/起点单调漂移 → 真实 m 依赖 or 高阶污染未吸收")
P("  ③ Richardson F5 是否显著（决定 1/m^5 层存在性）")
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
