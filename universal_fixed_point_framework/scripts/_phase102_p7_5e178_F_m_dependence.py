# -*- coding: utf-8 -*-
"""
P7-5e-178: F(m) 弱 m 依赖判别（方向 2）
=========================================
目标：判别 δ 展开的 1/m^4 层系数 F 是常数（−1/32 候选）还是有真实 m 依赖。
动机：176 登记"F 弱 m 依赖"（33..128 段 F=−0.0351 差 12.4%）；177a 通道 A 分段 F
      = +0.0028（33..64）/ +0.0265（65..128）/ −0.83（129..256）/ −83（257+）——形态可疑。

方法：固定 C=13/128 与 D 镜像双项（176 锁定展开）后，残差
      r(m) = delta − 1/56 + 13/128/m + (41/2000)(1/m^2 − 1/m^3)  = F4/m^4 + F5/m^5 + F6/m^6 + ...
      w(m) = m^4 * r(m) = F4 + F5/m + F6/m^2 + ...
      拟合 {1, 1/m, 1/m^2} → F4（1/m^4 系数）、F5、F6。
      分段拟合得到 F4(m) 曲线：
        · 常数检验：各段 F4 是否一致（±0.5% → 常数候选 −1/32 或 +1/32 判定）
        · 漂移检验：F4_eff = F0 + G/m（1/m^5 层混入）的显著性
        · 判别力：常数 vs 漂移两模型差 vs 提取噪声的信噪比

符号说明：delta = cl − 1/B*（闭式残差恒正）；cl = n/2 + 1/7 + 1/(7*2^n)，n>=33 尾巴可忽略。
数据：175 json（62 点 m=33..1009 step16）+ 176 json（56 点 m=17..127 step2）。
"""
import json, numpy as np, os

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(SCRIPTS, "_phase102_p7_5e178_out.txt")

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
invB = cl - dl

lines = []
def P(s=""):
    lines.append(s); print(s)

P("="*100)
P("P7-5e-178: F(m) 弱 m 依赖判别（固定 C/D 镜像后 1/m^4 层形态）")
P(f"数据：175 {len(m1)} 点 + 176 {len(m2)} 点 = {len(m)} 点；判别窗口 m>=33：{(n>=33).sum()} 点")
P("固定展开：δ = 1/56 − 13/128/m − (41/2000)(1/m^2 − 1/m^3) + F4/m^4 + F5/m^5 + ...")
P("候选：F4 = −1/32 = −0.03125（176 口径）或 +1/32 = +0.03125（177a 符号）——符号经两通道交叉定")
P("="*100)

# 残差与 w 通道
r = dl - 1.0/56.0 + C128/n + D41*(1.0/n**2 - 1.0/n**3)
w = n**4 * r

# 分段拟合：w = F4 + F5/m + F6/m^2
seg = [("m=33..48", (n>=33)&(n<=48)), ("m=49..64", (n>=49)&(n<=64)),
       ("m=65..96", (n>=65)&(n<=96)), ("m=97..128", (n>=97)&(n<=128)),
       ("m=129..192", (n>=129)&(n<=192)), ("m=193..256", (n>=193)&(n<=256)),
       ("m=257..384", (n>=257)&(n<=384)), ("m=385..512", (n>=385)&(n<=512)),
       ("m=513..768", (n>=513)&(n<=768)), ("m=769..1009", (n>=769)&(n<=1009))]

P("\n[F4 分段提取]  w(m) = m^4*r(m) = F4 + F5/m + F6/m^2，拟合 {1,1/m,1/m^2}")
P("-"*100)
P(f"  {'段':12s} {'N':4s}  {'F4':>12s} {'F5':>12s} {'F6':>12s}  {'RMS':>10s}  F4 距 -1/32  距 +1/32")
rows = []
for label, mask in seg:
    ns = n[mask]; ws = w[mask]
    if ns.size < 5: continue
    A = np.vstack([np.ones_like(ns), 1.0/ns, 1.0/ns**2]).T
    c, _, _, _ = np.linalg.lstsq(A, ws, rcond=None)
    pred = A @ c
    rms = np.sqrt(np.mean((ws-pred)**2))
    rows.append((label, ns.size, c[0], c[1], c[2], rms))
    dneg = (c[0]+1.0/32.0)/(1.0/32.0)*100
    dpos = (c[0]-1.0/32.0)/(1.0/32.0)*100
    P(f"  {label:12s} {ns.size:4d}  {c[0]:+12.6f} {c[1]:+12.4f} {c[2]:+12.4f}  {rms:10.3e}  {dneg:+7.2f}%  {dpos:+7.2f}%")

# 低段（33..128 合并）与中段
def fit_seg(mask, label):
    ns = n[mask]; ws = w[mask]
    A = np.vstack([np.ones_like(ns), 1.0/ns, 1.0/ns**2]).T
    c, _, _, _ = np.linalg.lstsq(A, ws, rcond=None)
    rms = np.sqrt(np.mean((ws - A@c)**2))
    dneg = (c[0]+1.0/32.0)/(1.0/32.0)*100
    dpos = (c[0]-1.0/32.0)/(1.0/32.0)*100
    P(f"  {label:12s} {ns.size:4d}  {c[0]:+12.6f} {c[1]:+12.4f} {c[2]:+12.4f}  {rms:10.3e}  {dneg:+7.2f}%  {dpos:+7.2f}%")
    return c

P("-"*100)
fit_seg((n>=33)&(n<=128), "m=33..128")
fit_seg((n>=33)&(n<=256), "m=33..256")
fit_seg(n>=33, "m>=33")

# 漂移检验：F4_eff(m) = F0 + G/m？——用 w 拟合 {1, 1/m} 两参（丢弃 1/m^2），看 G 是否显著
P("\n[漂移检验]  w 两参拟合 {1, 1/m}（F5 显式吸收 1/m 漂移）：F4_eff = F0 + G/m")
P("-"*100)
for label, mask in seg[:6]:
    ns = n[mask]; ws = w[mask]
    A = np.vstack([np.ones_like(ns), 1.0/ns]).T
    c, _, _, _ = np.linalg.lstsq(A, ws, rcond=None)
    rms2 = np.sqrt(np.mean((ws - A@c)**2))
    P(f"  {label:12s}  F0={c[0]:+10.5f}  G={c[1]:+10.4f}  RMS={rms2:.3e}")

# 判别力：F 常数（-1/32） vs 漂移（F0+G/m）——模型差 vs 噪声
P("\n[判别力论证]  F4 候选差（-1/32 vs +1/32）= 1/16 = 0.0625 → 在 w 层是常数差 0.0625")
P("  提取噪声 = 低段拟合 RMS（33..128 段 {1,1/m,1/m^2} 残差）")
rms_lo = np.sqrt(np.mean((w[(n>=33)&(n<=128)] - (np.vstack([np.ones_like(n[(n>=33)&(n<=128)]), 1.0/n[(n>=33)&(n<=128)], 1.0/n[(n>=33)&(n<=128)]**2]).T @ np.linalg.lstsq(np.vstack([np.ones_like(n[(n>=33)&(n<=128)]), 1.0/n[(n>=33)&(n<=128)], 1.0/n[(n>=33)&(n<=128)]**2]).T, w[(n>=33)&(n<=128)], rcond=None)[0]))**2))
P(f"  33..128 段三参拟合 RMS = {rms_lo:.3e}")
P("  · 若 F4 真值为常数 ±1/32：段间 F4 差应 < 噪声水平（~1e-2 级）；实际 33..64 vs 65..128 差 ~0.02")
P("  · F4 候选差 0.0625 vs 噪声：SNR 由分段点数决定——分段拟合 F4 的误差 ≈ RMS/sqrt(N)")
for label, mask in seg[:4]:
    ns = n[mask]
    err = rms_lo/np.sqrt(ns.size)
    P(f"  {label:12s} N={ns.size:4d}  F4 提取误差≈{err:.4f}  两候选差 0.0625 的 SNR={0.0625/err:.2f}")

# 结论判定
P("\n" + "="*100)
P("判定逻辑：")
P("  ① 若各段 F4 一致（|ΔF4| < 2σ）→ F 为常数，定符号（-1/32 or +1/32）")
P("  ② 若 F4 随 m 单调变化且 G 显著 → F 有真实弱 m 依赖（1/m^5 层混入或真结构）")
P("  ③ 若 F4 段间随机摆动且 SNR<1 → F 判别不可达（数据精度限制）")
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
