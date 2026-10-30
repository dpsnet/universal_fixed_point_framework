# -*- coding: utf-8 -*-
"""Phase 104az-59 v5 ★★★ 决定性计算完整版：π + σ± 通道 S_win(n,B)（半解析固定 n 流形）
- π (m=0→0)：抗磁 l 混合（v4 已验）
- σ± (m=0→±1)：线性 Zeeman 位移 ±B/2 + 抗磁 l 混合
- 圆偏振偶极 <Y_l0|sinθ e^{±iφ}/√2|Y_l'±1> 角向因子（数值 Gaunt）
- S_win_total(n,B) = (π 窗内 + σ 窗内) / 全
- TRK 自检：全强度随 B 守恒
"""
import json, io, os
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, factorial, sph_harm_y

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def R_nl(n, l, r):
    rho = 2.0*r/n
    norm = np.sqrt((2.0/n)**3 * factorial(n-l-1) / (2.0*n*factorial(n+l)))
    L = genlaguerre(n-l-1, 2*l+1)(rho)
    return norm * np.exp(-r/n) * (2.0*r/n)**l * L

def radial_int(n, l, np_, lp, power, r_max=120.0, N=4000):
    r = np.linspace(1e-8, r_max, N)
    f = R_nl(n, l, r) * R_nl(np_, lp, r) * r**power * r*r
    return np.trapezoid(f, r) if hasattr(np, 'trapezoid') else np.trapz(f, r)

def gaunt_cos(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    y1 = sph_harm_y(l1, 0, th, 0.0); y2 = sph_harm_y(l2, 0, th, 0.0)
    return float(np.real(np.sum(w * np.conj(y1) * np.cos(th) * y2 * np.sin(th))))

def gaunt_sin2(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    y1 = sph_harm_y(l1, 0, th, 0.0); y2 = sph_harm_y(l2, 0, th, 0.0)
    return float(np.real(np.sum(w * np.conj(y1) * np.sin(th)**2 * y2 * np.sin(th))))

def gaunt_sigma(l1, l2):
    """<Y_l1,0| sinθ e^{±iφ}/√2 |Y_l2,±1>——σ± 角向因子（φ 积分给 δ 符号，取模）
    = sqrt(2π) * <Y_l1,0| sinθ |Y_l2,1> 归一化因子处理：
    Y_l2,±1 = sqrt((2l+1)/(4π) (l-1)!/(l+1)!) P_l^1(cosθ) e^{±iφ}
    sinθ e^{±iφ} ∝ (l' 耦合)——直接数值：∫ Y*_l1,0 sinθ Y_l2,1 dΩ × (1/√2 e^{±iφ} 因子)
    """
    th, w = leggauss(96); th = np.arccos(th)
    y1 = sph_harm_y(l1, 0, th, 0.0)
    y2 = sph_harm_y(l2, 1, th, 0.0)   # m=+1 的 θ 部分
    integrand = np.conj(y1) * np.sin(th) * y2 * np.sin(th)
    # φ 积分：∫ e^{-i0φ} e^{iφ} e^{-iφ} dφ / 2π... σ± 算符含 e^{±iφ}/√2：
    # <Y_l0| σ± |Y_l±1> = (1/√2) ∫ Y*_l0 sinθ e^{±iφ} Y_l±1 dΩ
    # Y_l±1 含 e^{±iφ} → e^{±iφ}·e^{±iφ} = e^{±2iφ} → φ 积分 = 0？！
    # 修正：σ± 算符 = ∓(x±iy)/√2 = ∓r sinθ e^{±iφ}/√2
    # <Y_l0|σ±|Y_l'±1>: Y_l'±1 = f(θ) e^{±iφ}——e^{±iφ}·e^{±iφ}=e^{±2iφ}——∫dφ=0 除非...
    # 正确：σ± 选 Δm=±1——下态 m=0 → 上态 m=±1——算符 e^{±iφ} 作用：e^{±iφ}·Y_l'±1 = e^{±iφ}·e^{±iφ}=e^{±2iφ}？错！
    # 标准：x±iy = r sinθ e^{±iφ}——<m'|e^{±iφ}|m> ∝ δ_{m', m±1}——m'=±1, m=0：需要 e^{±iφ} 提 m 从 0 到 ±1 ✓
    # 所以：Y_l'^{±1} e^{±iφ} → 相位 e^{±iφ}·e^{±iφ}=e^{±2iφ}?? —— 不对！e^{±iφ} 是算符，作用后末态相位 = m'φ + (±1)φ？
    # 积分：∫ e^{-im'φ} e^{±iφ} e^{imφ} dφ = 2π δ_{m', m±1}——m'=±1, m=0, 算符+1: δ_{1,1}=1 ✓
    # 所以正确积分：∫Y*_l1,0(θ) sinθ Y_l2,1(θ) sinθ dθ × 2π（φ 部分已 δ）
    # Y_l2,1 含 e^{iφ}——上态相位 m=+1——算符 σ+（+1）→ 末态 m=+1 ✓（π 从 m=0）
    val = np.sum(w * integrand) * (2.0*np.pi) / np.sqrt(2.0)
    return float(np.real(val))

LMAX = 8
GC, GS, GSIG = {}, {}, {}
for l1 in range(LMAX):
    for l2 in range(LMAX):
        if abs(l1-l2) == 1:
            GC[(l1,l2)] = gaunt_cos(l1, l2)
        if abs(l1-l2) in (0, 2):
            GS[(l1,l2)] = gaunt_sin2(l1, l2)
        if abs(l1-l2) == 1:
            GSIG[(l1,l2)] = gaunt_sigma(l1, l2)

E2 = -1.0/8.0
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
W_ANG = 80.0

def run(B_au):
    B2 = B_au*B_au
    out = {"B_au": B_au, "B_MG": B_au*2350.0, "lines": {}}
    for n, (lam, Eph) in LINES.items():
        dE = Eph * 2.0*W_ANG / lam
        ls = list(range(n))
        # ---- π 通道（m=0 上下）----
        M = np.zeros((len(ls), len(ls)))
        for a, l in enumerate(ls):
            for b, lp in enumerate(ls):
                if abs(l-lp) in (0, 2):
                    g = GS.get((l, lp), GS.get((lp, l), 0.0))
                    if abs(g) > 1e-12:
                        M[a, b] = radial_int(n, l, n, lp, 2) * g
        M *= 0.125 * B2
        evals, evecs = np.linalg.eigh(M)
        n2_states = [(0, 1.0), (1, 1.0)]
        f_pi = []
        for a in range(len(ls)):
            amp = 0.0 + 0.0j
            for b, l in enumerate(ls):
                tot = 0.0 + 0.0j
                for l2, coeff in n2_states:
                    if abs(l2-l) == 1:
                        g = GC.get((l2, l), GC.get((l, l2), 0.0))
                        if abs(g) > 1e-12:
                            ri = radial_int(2, l2, n, l, 1)
                            tot += coeff * ri * g
                amp += evecs[b, a] * tot
            f_pi.append((Eph + evals[a], abs(amp)**2))
        # ---- σ 通道（下 m=0 → 上 m=+1 与 m=-1；Zeeman 线性 ±B/2）----
        # σ± 强度相同（|m|=1），位移不同——分别处理
        f_sig = []
        for sgn in (+1, -1):
            # 上态 m=sgn：每 l 一个态——同 ls——抗磁矩阵同（ρ² 对角化只依赖 m²）——m=±1 的 ρ² 角向因子不同！
            # m=±1: <Y_l±1|sin²θ|Y_l'±1>——另一个 Gaunt（用 m=1）
            M2 = np.zeros((len(ls), len(ls)))
            for a, l in enumerate(ls):
                for b, lp in enumerate(ls):
                    if abs(l-lp) in (0, 2):
                        g = gaunt_sin2_m1(l, lp)
                        if abs(g) > 1e-12:
                            M2[a, b] = radial_int(n, l, n, lp, 2) * g
            M2 *= 0.125 * B2
            ev2, evc2 = np.linalg.eigh(M2)
            for a in range(len(ls)):
                amp = 0.0 + 0.0j
                for b, l in enumerate(ls):
                    tot = 0.0 + 0.0j
                    for l2, coeff in n2_states:
                        if abs(l2-l) == 1:
                            g = GSIG.get((l2, l), GSIG.get((l, l2), 0.0))
                            if abs(g) > 1e-12:
                                ri = radial_int(2, l2, n, l, 1)
                                tot += coeff * ri * g
                    amp += evc2[b, a] * tot
                E_sig = Eph + sgn*B_au/2.0 + ev2[a]
                f_sig.append((E_sig, abs(amp)**2))
        # ---- 汇总 ----
        all_f = f_pi + f_sig
        total = sum(f for _, f in all_f)
        s_win = sum(f for Ea, f in all_f if abs(Ea - Eph) < dE)
        out["lines"][str(n)] = {"s_win": float(s_win), "total": float(total),
                                "frac": float(s_win/total) if total > 1e-30 else 0.0,
                                "n_alpha": len(all_f), "n_pi": len(f_pi), "n_sig": len(f_sig)}
    return out

def gaunt_sin2_m1(l1, l2):
    """<Y_l1,±1|sin²θ|Y_l2,±1>（m=1）"""
    th, w = leggauss(96); th = np.arccos(th)
    y1 = sph_harm_y(l1, 1, th, 0.0); y2 = sph_harm_y(l2, 1, th, 0.0)
    return float(np.real(np.sum(w * np.conj(y1) * np.sin(th)**2 * y2 * np.sin(th))))

print("=== v5 决定性计算：π+σ 通道 S_win(n,B) ±80 Å（标准 l 混合+Zeeman 基线）===", flush=True)
B_list = (0.0001, 0.005, 0.01, 0.02, 0.05)
results = []
for B in B_list:
    print("B=%.4f a.u. (%.1f MG)..." % (B, B*2350), flush=True)
    out = run(B)
    results.append(out)
    ln = out["lines"]
    print("  Hα %6.1f%% Hβ %6.1f%% Hγ %6.1f%% Hδ %6.1f%% Hε %6.1f%%  (窗内份额)" % (
        100*ln["3"]["frac"], 100*ln["4"]["frac"], 100*ln["5"]["frac"],
        100*ln["6"]["frac"], 100*ln["7"]["frac"]), flush=True)
    print("  total: Hα %.3e Hβ %.3e Hγ %.3e Hδ %.3e Hε %.3e" % (
        ln["3"]["total"], ln["4"]["total"], ln["5"]["total"],
        ln["6"]["total"], ln["7"]["total"]), flush=True)

# TRK 自检
ref = results[0]
print("\n=== TRK 守恒自检（total/0.2MG 参考）===", flush=True)
for res in results:
    line = "B=%6.1f MG |" % res["B_MG"]
    for n in (3,4,5,6,7):
        line += " %s %.3f" % ({3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ",7:"Hε"}[n],
                              res["lines"][str(n)]["total"]/ref["lines"][str(n)]["total"])
    print(line, flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_sigma_v5.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_osc_pi_sigma_v5.json")
