# -*- coding: utf-8 -*-
"""
P7-5e-178d: F(m) 弱 m 依赖判别——自由四参滑动窗口（最终判别通道）
=================================================================
178c 结论：固定 C/D/E 后 w 通道非收敛幂律（F4 随基扩展漂移、E 偏差线性项污染）。
→ F 的判别只能在"全自由拟合"框架（176 口径：C/D/E/F 自由，污染被低阶自由度吸收）。

本版：δ(m) = 1/56 − C/m − D/m^2 + E/m^3 + F4/m^4 + F5/m^5
四参（C,D,E,F4）自由拟合，滑动窗口提取 F4，回答：
  ① F4 跨窗口是否稳定（→ 常数，与 −1/32 比）
  ② F4 随窗口漂移形态（→ 弱 m 依赖 or 高阶污染）
  ③ 判别力：F4 段间差 vs 提取误差
数据：175 + 176 json（112 点）。
"""
import json, numpy as np, os

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(SCRIPTS, "_phase102_p7_5e178d_out.txt")

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
delta = dl          # delta = cl - 1/B*，闭式残差

lines = []
def P(s=""):
    lines.append(s); print(s)

P("="*100)
P("P7-5e-178d: F(m) 弱 m 依赖判别——自由四参滑动窗口")
P(f"数据：{len(m)} 点；判别窗口 m>=33：{(n>=33).sum()} 点")
P("模型：δ = 1/56 − C/m − D/m^2 + E/m^3 + F4/m^4（C,D,E,F4 全自由）")
P("候选：F4 = −1/32 = −0.03125（176 口径）")
P("="*100)

def fit4(mask, label):
    ns = n[mask]; ds = delta[mask]
    A = np.vstack([1.0/ns, 1.0/ns**2, 1.0/ns**3, 1.0/ns**4]).T
    c, _, _, _ = np.linalg.lstsq(A, ds - 1.0/56.0, rcond=None)
    rms = np.sqrt(np.mean((ds - (1.0/56.0 + A@c))**2))
    C_, D_, E_, F4 = c
    dC = (C_ + 13.0/128.0)/(13.0/128.0)*100
    dD = (D_ + 41.0/2000.0)/(41.0/2000.0)*100
    dE = (E_ - 41.0/2000.0)/(41.0/2000.0)*100
    dF = (F4 + 1.0/32.0)/(1.0/32.0)*100
    P(f"  {label:14s} N={ns.size:4d}  C={C_:+.9f}({dC:+.3f}%)  D={D_:+.9f}({dD:+.3f}%)  E={E_:+.9f}({dE:+.3f}%)  F4={F4:+.9f}(距-1/32 {dF:+8.2f}%)  RMS={rms:.3e}")
    return (C_, D_, E_, F4), rms

P("\n[滑动窗口：终点滑动]  四参自由拟合")
P("-"*100)
res = {}
for hi in [64, 96, 128, 160, 192, 256, 384, 512]:
    mask = (n>=33)&(n<=hi)
    if mask.sum() < 8: continue
    res[("33", str(hi))] = fit4(mask, f"m=33..{hi}")

P("\n[滑动窗口：起点滑动]  终点 1009/512 固定")
P("-"*100)
for lo in [33, 49, 65, 97, 129, 257]:
    mask = (n>=lo)&(n<=1009)
    if mask.sum() < 8: continue
    res[(str(lo), "1009")] = fit4(mask, f"m={lo}..1009")

# 分段（非重叠）F4 提取——直接看 F4(m) 形态
P("\n[非重叠分段]  F4(m) 形态")
P("-"*100)
segs = [("m=33..64", (n>=33)&(n<=64)), ("m=65..128", (n>=65)&(n<=128)),
        ("m=129..256", (n>=129)&(n<=256)), ("m=257..512", (n>=257)&(n<=512)),
        ("m=513..1009", (n>=513)&(n<=1009))]
for label, mask in segs:
    if mask.sum() < 6: continue
    res[label] = fit4(mask, label)

# F4 弱 m 依赖拟合：F4(m_eff) = F0 + G/m_eff
P("\n[F4(m) 漂移检验]  F4 分段值 vs 段中点 m（F4 = F0 + G/m？）")
P("-"*100)
pts = []
for label, mask in segs:
    if label in res and mask.sum() >= 6:
        F4 = res[label][0][3]
        mid = np.mean(n[mask])
        pts.append((mid, F4))
        P(f"  {label}: 段中点 m={mid:.0f}  F4={F4:+.6f}")
if len(pts) >= 3:
    mids = np.array([p[0] for p in pts]); F4s = np.array([p[1] for p in pts])
    A = np.vstack([np.ones_like(mids), 1.0/mids]).T
    c, _, _, _ = np.linalg.lstsq(A, F4s, rcond=None)
    P(f"  拟合 F4 = F0 + G/m：F0={c[0]:+.4f}  G={c[1]:+.4f}  （若 G 显著 → F 有真实 1/m 漂移）")
    rms_lin = np.sqrt(np.mean((F4s - A@c)**2))
    P(f"  残差 RMS={rms_lin:.4f} vs 各段 F4 提取误差（见上）——G 显著性判定")

P("\n" + "="*100)
P("判定：")
P("  ① 若各窗口 F4 一致（|Δ|<2σ 提取误差）→ F 常数，与 -1/32 比")
P("  ② 若 F4 随窗口单调漂移且 G 显著 → F 弱 m 依赖（或低阶系数吸收了部分污染）")
P("  ③ 若 F4 段间摆动但无单调形态 → 判别不可达")
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
