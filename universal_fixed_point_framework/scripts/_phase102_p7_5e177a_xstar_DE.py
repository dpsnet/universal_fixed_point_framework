# -*- coding: utf-8 -*-
"""
P7-5e-177a: E 独立通道精度提升（方向 1）
=========================================
两条独立通道判别 D=41/2000、E=+41/2000：

[通道 A] 残差重参数化（固定 C=13/128，D/E 近正交基）
  u(n) = n^2 * (delta - 1/56 + 13/128/n) = D - E/n + F/n^2 + O(1/n^3)
  基 {1, 1/n, 1/n^2} 在 n>=33 近似正交（区别于 176 的 C/D/E 强相关三参基）

[通道 B] 过零位移代数映射（完全不同的拟合路径与物理量）
  x*(n) = B* * n = n / (cl - delta)，幂展开
  x* = 2 + alpha/n + beta/n^2 + gamma/n^3 + delta4/n^4
  解析映射（来自 E0*|m| = f + g/n + h/n^2 + i/n^3 过零条件逐阶消去）：
    C = -beta/4 + alpha^2/8          （先验预测：alpha=-1/2, beta=-9/32 -> 13/128）
    D = -gamma/4 + alpha*beta/4 - alpha^3/16  = -gamma/4 + 5/256
    E = -delta4/4 + (beta^2+2*alpha*gamma)/8 + 3*alpha^2*beta/16 - alpha^4/32
  判别点：
    beta_pred = -9/32  （C=13/128 的第三独立通道预测，新数学资产）
    gamma_pred = 4*(5/256 - 41/2000) = -31/8000   （若 D = -41/2000）
    E_pred vs +41/2000

数据：175 (m=33..1009 step16, 62 点) + 176 (m=17..127 step2, 56 点) delta json
口径：delta = cl - 1/B*（闭式残差，cl = n/2 + 1/7 + 1/(7*2^n)，n>=33 尾巴忽略）
"""
import json, numpy as np, os

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(SCRIPTS, "_phase102_p7_5e177a_out.txt")
OUTJSON = os.path.join(SCRIPTS, "_phase102_p7_5e177a_xstar.json")

def load_delta(fn):
    d = json.load(open(os.path.join(SCRIPTS, fn), encoding="utf-8"))
    return np.array(d["m"]), np.array(d["delta"])

m1, d1 = load_delta("_phase102_p7_5e175_delta63.json")
m2, d2 = load_delta("_phase102_p7_5e176_delta_lowm.json")
m = np.concatenate([m1, m2]); dl = np.concatenate([d1, d2])
order = np.argsort(m); m, dl = m[order], dl[order]
# 去重
uniq = np.unique(m, return_index=True)[1]
m, dl = m[uniq], dl[uniq]

# 闭式与恢复
C128 = 13.0/128.0
D41 = 41.0/2000.0   # 0.0205
n = m
cl = n/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**n)   # 尾巴在 n>=33 时 ~1e-11 可忽略
invB = cl - dl                               # 1/B*
xstar = n / invB                             # B* * n（过零位置）

lines = []
def P(s=""):
    lines.append(s)
    print(s)

P("="*100)
P("P7-5e-177a: E 独立通道精度提升（通道 A 残差重参数化 + 通道 B 过零位移映射）")
P(f"数据：175 {len(m1)} 点 + 176 {len(m2)} 点 = {len(m)} 点（n>=17）；判别窗口 n>=33：{(n>=33).sum()} 点")
P("口径：delta = cl - 1/B*；x* = B* * n = n/(cl-delta)")
P(f"参考值：C=13/128={C128:.10f}  D=41/2000={D41:.10f}  E_mirror=+41/2000")
P("="*100)

# ============ 通道 A：残差重参数化 ============
P("\n[通道 A] 固定 C=13/128，u(n) = n^2*(delta - 1/56 + 13/128/n) = D - E/n + F/n^2 + O(1/n^3)")
P("-"*80)

def fitA(ns, dls, label):
    """u = a - b/n + c/n^2；a=D, b=E, c=F"""
    u = ns**2 * (dls - 1.0/56.0 + C128/ns)
    A = np.vstack([np.ones_like(ns), 1.0/ns, 1.0/ns**2]).T
    coeff, res, _, _ = np.linalg.lstsq(A, u, rcond=None)
    Df, Ef, Ff = coeff
    pred = A @ coeff
    rms = np.sqrt(np.mean((u - pred)**2))
    return Df, Ef, Ff, rms, u

segA = [("n=33..64", (n>=33)&(n<=64)), ("n=65..128", (n>=65)&(n<=128)),
        ("n=129..256", (n>=129)&(n<=256)), ("n=257..512", (n>=257)&(n<=512)),
        ("n>=33", n>=33), ("n>=129", n>=129)]
resA = {}
for label, mask in segA:
    if mask.sum() < 5: continue
    Df, Ef, Ff, rms, u = fitA(n[mask], dl[mask], label)
    resA[label] = (Df, Ef, Ff, rms)
    P(f"  {label:12s} N={mask.sum():4d}  D={Df:+.10f} (41/2000 距 {(Df-D41)/D41*100:+.3f}%)  "
      f"E={Ef:+.10f} (41/2000 距 {(Ef-D41)/D41*100:+.3f}%)  F={Ff:+.6f}  RMS={rms:.3e}")

# 通道 A Richardson（E 消 F 层）
P("\n  通道 A Richardson（u(n)-u(2n) 消常数 D）：w(n) = n*(u(n)-u(2n)) = -E/2 + 3F/(4n) + O(1/n^2)")
maskL = (n>=33)&(n<=256)
u = n**2 * (dl - 1.0/56.0 + C128/n)
nu = u[np.isin(n*1.0, (n[maskL]*2.0))] if False else None
# 手动配 2n 对
nset = n[maskL]; uset = u[maskL]
pairs = []
for ni, ui in zip(nset, uset):
    if (ni*2) in nset:
        pairs.append((ni, ui, uset[nset==ni*2][0]))
pairs = np.array(pairs)
if len(pairs) >= 4:
    wn = pairs[:,0]*(pairs[:,1]-pairs[:,2])
    # w = -E/2 + (3F/4)/n
    A = np.vstack([np.ones_like(pairs[:,0]), 1.0/pairs[:,0]]).T
    c, _, _, _ = np.linalg.lstsq(A, wn, rcond=None)
    E_rich = -2.0*c[0]
    P(f"  Richardson 配对 {len(pairs)} 对 (33..256)：E_rich = {E_rich:+.10f}  (41/2000 距 {(E_rich-D41)/D41*100:+.3f}%)  截距斜率 {c[1]:+.3e}")

# ============ 通道 B：过零位移幂展开 ============
P("\n[通道 B] x* = 2 + alpha/n + beta/n^2 + gamma/n^3 + delta4/n^4")
P("解析映射：C = -beta/4 + alpha^2/8； D = -gamma/4 + 5/256； E = -delta4/4 + (beta^2+2*alpha*gamma)/8 + 3*alpha^2*beta/16 - alpha^4/32")
P("先验预测：alpha=-1/2 (142 锁定)； beta=-9/32 对应 C=13/128（新预测）； gamma=-31/8000 对应 D=-41/2000；")
P("-"*80)

def fitB(ns, xs, label):
    A = np.vstack([np.ones_like(ns), 1.0/ns, 1.0/ns**2, 1.0/ns**3]).T
    coeff, res, _, _ = np.linalg.lstsq(A, xs, rcond=None)
    a_, b_, g_, d4_ = coeff
    pred = A @ coeff
    rms = np.sqrt(np.mean((xs - pred)**2))
    Cp = -b_/4.0 + a_**2/8.0
    Dp = -g_/4.0 + a_*b_/4.0 - a_**3/16.0
    Ep = -d4_/4.0 + (b_**2 + 2.0*a_*g_)/8.0 + 3.0*a_**2*b_/16.0 - a_**4/32.0
    return a_, b_, g_, d4_, Cp, Dp, Ep, rms

resB = {}
for label, mask in segA:
    if mask.sum() < 5: continue
    a_, b_, g_, d4_, Cp, Dp, Ep, rms = fitB(n[mask], xstar[mask], label)
    resB[label] = (a_, b_, g_, d4_, Cp, Dp, Ep, rms)
    P(f"  {label:12s} N={mask.sum():4d}  alpha={a_:+.8f} (-1/2 距 {(a_+0.5)/0.5*100:+.4f}%)  beta={b_:+.8f} (-9/32 距 {(b_+9/32)/(9/32)*100:+.4f}%)")
    P(f"      gamma={g_:+.8f} (-31/8000 距 {(g_+31/8000)/(31/8000)*100:+.4f}%)  delta4={d4_:+.8f}  RMS={rms:.3e}")
    P(f"      C_map={Cp:+.10f} (13/128 距 {(Cp-C128)/C128*100:+.4f}%)  D_map={Dp:+.10f} (41/2000 距 {(Dp-D41)/D41*100:+.3f}%)  E_map={Ep:+.10f} (41/2000 距 {(Ep-D41)/D41*100:+.3f}%)")

# ============ 判别汇总 ============
P("\n" + "="*100)
P("判别汇总")
P("="*100)
P("通道 A（残差重参数化，固定 C=13/128）：")
Df, Ef, Ff, rms, _ = resA["n>=33"]
P(f"  全段 n>=33：D={Df:.8f}（41/2000 距 {(Df-D41)/D41*100:+.3f}%）  E={Ef:.8f}（41/2000 距 {(Ef-D41)/D41*100:+.3f}%）  RMS={rms:.3e}")
for lab in ["n=33..64","n=65..128","n=129..256","n=257..512"]:
    if lab in resA:
        Df, Ef, Ff, rms = resA[lab]
        P(f"  {lab}: D 距 {(Df-D41)/D41*100:+.3f}%  E 距 {(Ef-D41)/D41*100:+.3f}%")
P("通道 B（过零位移映射，全段 n>=33）：")
a_, b_, g_, d4_, Cp, Dp, Ep, rms = resB["n>=33"]
P(f"  alpha={a_:.8f}（-1/2 距 {(a_+0.5)/0.5*100:+.4f}%）  beta={b_:.8f}（-9/32 距 {(b_+9/32)/(9/32)*100:+.4f}%）")
P(f"  C_map={Cp:.8f}（13/128 距 {(Cp-C128)/C128*100:+.4f}%）  D_map={Dp:.8f}（41/2000 距 {(Dp-D41)/D41*100:+.3f}%）  E_map={Ep:.8f}（41/2000 距 {(Ep-D41)/D41*100:+.3f}%）")
P(f"  gamma={g_:.8f}（-31/8000 距 {(g_+31/8000)/(31/8000)*100:+.4f}%）")

# 保存 x* 数据
json.dump({"m": m.tolist(), "xstar": xstar.tolist(), "delta": dl.tolist(),
           "script": "P7-5e-177a",
           "note": "x* = B* * n = n/(cl-delta)；delta=cl-1/B* 闭式残差；cl=n/2+1/7+1/(7*2^n)"},
          open(OUTJSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
P(f"\n已保存：{OUTJSON}")
