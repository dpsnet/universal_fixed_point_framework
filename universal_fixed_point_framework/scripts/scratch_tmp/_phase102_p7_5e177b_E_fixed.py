# -*- coding: utf-8 -*-
"""
P7-5e-177b: E 独立通道——固定 C/D 后 {1, 1/n} 近正交基提取（镜像假说检验）
================================================================================
delta = 1/56 - C/n - D/n^2 + E/n^3 - F/n^4 + O(1/n^5)   （D、E 独立的一般形式）

固定 C=13/128、D=41/2000（D 已由 177a 通道 A 以 +0.05% 命中锁定候选）后：
  v(n) = n^3 * (delta - 1/56 + C/n + D/n^2) = E - F/n + G/n^2 + ...
基 {1, 1/n} 在 n>=33 近乎正交——E（常数项）与 F（1/n 项）可干净分离。

判别目标：
  E = +41/2000（镜像假说 D=-E）  vs  E = +0.02017（176 自由拟合值）
对照：D 固定为通道 A 拟合值 -0.0205106 再提取 E（消除 D 残差影响）。

另加 Richardson 通道：
  n*(v(n) - v(2n)) = -F/2 + (3G/4)/n + O(1/n^2)   （消 E，检验 F=-1/32 候选）
  E_rich 用三点组合消 F、G。
"""
import json, numpy as np, os

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(SCRIPTS, "_phase102_p7_5e177b_out.txt")

def load_delta(fn):
    d = json.load(open(os.path.join(SCRIPTS, fn), encoding="utf-8"))
    return np.array(d["m"]), np.array(d["delta"])

m1, d1 = load_delta("_phase102_p7_5e175_delta63.json")
m2, d2 = load_delta("_phase102_p7_5e176_delta_lowm.json")
m = np.concatenate([m1, m2]); dl = np.concatenate([d1, d2])
order = np.argsort(m); m, dl = m[order], dl[order]
uniq = np.unique(m, return_index=True)[1]
m, dl = m[uniq], dl[uniq]

C128 = 13.0/128.0
D41 = 41.0/2000.0   # 0.0205（δ 展开 δ = 1/56 - C/n - D/n^2 + E/n^3，D 取正）
D_fitA = +0.0205106 # 177a 通道 A 拟合值（常数项 -D → D = +0.0205106）

lines = []
def P(s=""):
    lines.append(s); print(s)

P("="*100)
P("P7-5e-177b: E 独立通道——固定 C/D 后 {1,1/n} 正交基提取 E")
P(f"数据 {len(m)} 点；判别窗口 n>=33：{(m>=33).sum()} 点")
P(f"固定 C=13/128={C128:.10f}；D=41/2000={D41:.10f}（对照 D_fit=+{D_fitA:.8f}）")
P("口径：delta = cl - 1/B*（cl = n/2+1/7+1/(7*2^n)，n>=33 尾巴忽略）")
P("="*100)

def fitE(ns, dls, Dfix, label):
    """v = n^3*(delta - 1/56 + C/n + D/n^2) = E - F/n + G/n^2"""
    v = ns**3 * (dls - 1.0/56.0 + C128/ns + Dfix/ns**2)
    A = np.vstack([np.ones_like(ns), 1.0/ns, 1.0/ns**2]).T
    coeff, _, _, _ = np.linalg.lstsq(A, v, rcond=None)
    Ef, Ff, Gf = coeff
    pred = A @ coeff
    rms = np.sqrt(np.mean((v - pred)**2))
    return Ef, Ff, Gf, rms

segs = [("n=33..64",  (m>=33)&(m<=64)), ("n=65..128", (m>=65)&(m<=128)),
        ("n=129..256",(m>=129)&(m<=256)), ("n=257..512",(m>=257)&(m<=512)),
        ("n>=33", m>=33), ("n>=65", m>=65), ("n>=129", m>=129)]

for Dfix, dlab in [(D41, "D=41/2000"), (D_fitA, "D=D_fitA(+0.0205106)")]:
    P(f"\n[D 固定 {dlab}]  v = n^3*(delta-1/56+13/128/n+D/n^2) = E - F/n + G/n^2")
    P("-"*90)
    for label, mask in segs:
        if mask.sum() < 5: continue
        Ef, Ff, Gf, rms = fitE(m[mask], dl[mask], Dfix, label)
        P(f"  {label:12s} N={mask.sum():4d}  E={Ef:+.10f} (41/2000 距 {(Ef-D41)/D41*100:+.3f}%; 0.02017 距 {(Ef-0.02017)/0.02017*100:+.3f}%)"
          f"  F={Ff:+.8f} (-1/32 距 {(Ff+1/32)/(1/32)*100:+.2f}%)  G={Gf:+.5f}  RMS={rms:.3e}")

# Richardson 通道（配对 n 与 2n）
P("\n[Richardson] n*(v(n)-v(2n)) = -F/2 + (3G/4)/n + O(1/n^2)（消 E 检验 F）")
Dfix = D41
v = m**3 * (dl - 1.0/56.0 + C128/m + Dfix/m**2)
nset = m[(m>=33)&(m<=512)]
pairs = []
for ni in nset:
    if (ni*2) in nset:
        pairs.append((ni, v[nset==ni][0], v[nset==ni*2][0]))
pairs = np.array(pairs)
if len(pairs) >= 3:
    wn = pairs[:,0]*(pairs[:,1]-pairs[:,2])
    A = np.vstack([np.ones_like(pairs[:,0]), 1.0/pairs[:,0]]).T
    c, _, _, _ = np.linalg.lstsq(A, wn, rcond=None)
    F_rich = -2.0*c[0]
    P(f"  配对 {len(pairs)} 对：F_rich = {F_rich:+.8f}  (-1/32 距 {(F_rich+1/32)/(1/32)*100:+.2f}%)  G 斜率 {c[1]:+.4f}")

# E 的 Richardson 消 F、G：三点组合 E = v(n) + F/n - G/n^2，用最小二乘直接在 {1,1/n,1/n^2} 已做。
# 补充：固定 F=-1/32（候选）后单参 E 提取（干净零相关基）
P("\n[固定 F=-1/32 单参]  w(n) = v(n) + (1/32)/n = E + G/n^2 + ...")
for label, mask in segs:
    if mask.sum() < 5: continue
    ns = m[mask]
    w = ns**3*(dl[mask] - 1.0/56.0 + C128/ns + D41/ns**2) + (1.0/32.0)/ns
    A = np.vstack([np.ones_like(ns), 1.0/ns**2]).T
    coeff, _, _, _ = np.linalg.lstsq(A, w, rcond=None)
    Ef, Gf = coeff
    pred = A @ coeff
    rms = np.sqrt(np.mean((w-pred)**2))
    P(f"  {label:12s} N={mask.sum():4d}  E_fixF={Ef:+.10f} (41/2000 距 {(Ef-D41)/D41*100:+.3f}%)  G={Gf:+.6f}  RMS={rms:.3e}")

# 判别汇总
P("\n" + "="*100)
P("判别汇总")
P("="*100)
Ef1, Ff1, Gf1, rms1 = fitE(m[(m>=33)&(m<=128)], dl[(m>=33)&(m<=128)], D41, "33..128")
Ef2, Ff2, Gf2, rms2 = fitE(m[(m>=33)], dl[(m>=33)], D41, ">=33")
P(f"D=41/2000 固定：33..128 段 E={Ef1:.8f}（距 +41/2000 {(Ef1-D41)/D41*100:+.3f}%、距 0.02017 {(Ef1-0.02017)/0.02017*100:+.3f}%）F={Ff1:.6f}")
P(f"           全段 E={Ef2:.8f}（距 +41/2000 {(Ef2-D41)/D41*100:+.3f}%）F={Ff2:.6f}")
P("E 判别：|E - 41/2000|/41/2000 < 1% -> 镜像假说 E=+41/2000 升格锁定；否则保持 176 口径（方向支持未锁）")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
P(f"\n已保存：{OUT}")
