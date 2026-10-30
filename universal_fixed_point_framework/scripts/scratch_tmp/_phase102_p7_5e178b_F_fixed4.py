# -*- coding: utf-8 -*-
"""
P7-5e-178b: F(m) 弱 m 依赖判别（修正版——E 偏差免疫）
=====================================================
修正 178 的设计缺陷：w = m^4 * r(m) 中残留 E 偏差项 δE·m（线性），
178 的 {1,1/m,1/m^2} 基缺 {m} 项 → E 未锁的 ±0.0005 在 m=33..128 产生
0.0165~0.064 线性项，与 F4 同量级，扭曲 F4 提取。

本版：拟合基 {m, 1, 1/m, 1/m^2}（四参），线性项吸收 E 偏差：
  w(m) = δE·m + F4 + F5/m + F6/m^2
F4 提取对 E 偏差免疫；δE 拟合值可交叉检验 E（177c：E≈0.0203±0.0005）。

r(m) = delta − 1/56 + 13/128/m + (41/2000)(1/m^2 − 1/m^3)  （C/D 双项固定，E=+41/2000 已并入 1/m^3）
候选：F4 = −1/32（176 口径）。
数据：175 + 176 json（112 点）。
"""
import json, numpy as np, os

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(SCRIPTS, "_phase102_p7_5e178b_out.txt")

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

lines = []
def P(s=""):
    lines.append(s); print(s)

P("="*100)
P("P7-5e-178b: F(m) 弱 m 依赖判别（修正版——四参基 {m,1,1/m,1/m^2}，E 偏差免疫）")
P(f"数据：{len(m)} 点；判别窗口 m>=33：{(n>=33).sum()} 点")
P("r(m) = delta − 1/56 + 13/128/m + (41/2000)(1/m^2 − 1/m^3)；w = m^4·r = δE·m + F4 + F5/m + F6/m^2")
P("候选：F4 = −1/32 = −0.03125")
P("="*100)

r = dl - 1.0/56.0 + C128/n + D41*(1.0/n**2 - 1.0/n**3)
w = n**4 * r

def fit4(mask, label):
    ns = n[mask]; ws = w[mask]
    A = np.vstack([ns, np.ones_like(ns), 1.0/ns, 1.0/ns**2]).T
    c, _, _, _ = np.linalg.lstsq(A, ws, rcond=None)
    rms = np.sqrt(np.mean((ws - A@c)**2))
    dE, F4, F5, F6 = c
    dneg = (F4 + 1.0/32.0)/(1.0/32.0)*100
    P(f"  {label:12s} N={ns.size:4d}  δE={dE:+.6f} (E_fit={0.0205+dE:.6f})  F4={F4:+10.6f}  F5={F5:+10.4f}  F6={F6:+12.3f}  RMS={rms:.3e}  F4距-1/32 {dneg:+8.2f}%")
    return c, rms

seg = [("m=33..48", (n>=33)&(n<=48)), ("m=49..64", (n>=49)&(n<=64)),
       ("m=65..96", (n>=65)&(n<=96)), ("m=97..128", (n>=97)&(n<=128)),
       ("m=129..160", (n>=129)&(n<=160)), ("m=161..256", (n>=161)&(n<=256))]

P("\n[四参分段拟合]")
P("-"*100)
for label, mask in seg:
    if mask.sum() >= 5:
        fit4(mask, label)

P("-"*100)
fit4((n>=33)&(n<=128), "m=33..128")
fit4((n>=33)&(n<=256), "m=33..256")
fit4(n>=33, "m>=33")

# 判别力：F4 常数（-1/32） vs 漂移——用 33..128 段四参 RMS 作噪声
c_lo, rms_lo = fit4((n>=33)&(n<=128), "m=33..128")
P("\n[判别力]  F4 候选差（-1/32 vs 漂移模型）= 各段 F4 与 -1/32 的差；噪声 = 33..128 四参 RMS")
err_lo = rms_lo/np.sqrt((n>=33).sum())
P(f"  m>=33 全段 F4 提取误差≈{err_lo:.4f}")
for label, mask in seg[:4]:
    ns = n[mask]
    F4seg = fit4(mask, label)[0][1]
    err = rms_lo/np.sqrt(ns.size)
    P(f"  {label}: F4={F4seg:+.4f} vs -1/32={-1/32:+.4f}  差={F4seg+1/32:+.4f}  误差≈{err:.4f}  SNR≈{abs(F4seg+1/32)/err:.2f}")

P("\n" + "="*100)
P("判定：")
P("  ① F4 各段是否一致（|Δ|<2σ）→ 常数 or 漂移")
P("  ② δE 拟合值是否接近 0（E 偏差应 <±0.0005 且稳定）")
P("  ③ F4 距 -1/32 的显著性与方向")
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
