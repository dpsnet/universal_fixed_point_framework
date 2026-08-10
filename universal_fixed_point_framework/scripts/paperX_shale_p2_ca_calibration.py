#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t5-2 Ca 数标定：东营离心实验 c 窗口估计 + 毛细极限归属确认（→ P2-6j）。

判定链（三层）：
(1) 驱动模式论证（解析）：离心 = 逐台阶压力控制 + 平衡等待（标准协议）。
    平衡态流速→0 ⇒ 粘性压降→0 ⇒ DIP 有效 c_eff→0（= DIP c=0 毛细支）。
    S(ΔP) 即静态毛细曲线，ν=1 朗缪尔支归属由构造成立（前提自洽）。
    注意：微观 Ca≪1 不充分——相关控制参数是"全样品粘性压降/毛细阈"比
    （DIP 的 c·R_path），路径长度放大使未平衡瞬态 c_eff 可达 O(1)。
(2) 平衡时间要求（解析）：每台阶压力驱动排出 τ_relax ≈ φ·ΔS·μ·L²/(k·δP)；
    残余瞬态有效 c：c_eff(t) ≈ (δP/a)·exp(−t/τ_relax)；
    平衡判据 t_hold ≫ τ_relax 或 c_eff(t_hold) < c_lim。
(3) 经验约束（数值）：DIP 小 c 扫描 → 在东营数据点 Pdata 采样 S(P)，
    双倒数朗缪尔拟合 R²（与东营 R²=0.93–0.99 同口径）→ 存活窗 c_max；
    + 突破判据 P_c(c) ≤ 3.01（东营窗内含饱和）。
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_dyn_ip import run_dip

A_DP = 1.09          # 东营 ΔP_L (MPa)
PDATA = np.array([0.08, 0.33, 0.75, 1.34, 2.09, 2.78])  # P2-6b 逐点力值
R2_DATA_MIN = 0.93   # 东营三井双倒数 R² 下限（0.9935/0.9289/0.9259，well-2 最低）
PCAP_DATA = 3.01     # 东营窗口上限

# ---------------- Part 1/2 解析 ----------------
def relaxation_time(phi, dS, mu, L, k, dP):
    """每台阶压力驱动排出时间：τ = 排出体积/达西通量 = φ·ΔS·μ·L²/(k·δP)。"""
    return phi * dS * mu * L**2 / (k * dP)  # s

def c_eff_residual(dP, tau, a, t):
    """残余瞬态有效 c：未平衡驱动压/毛细阈（一阶松弛近似）。"""
    return (dP / a) * np.exp(-t / tau)

def main_analytic():
    print("=" * 78)
    print("Part 1/2 解析：平衡时间 + 残余瞬态 c_eff + 微观 Ca")
    print("=" * 78)
    mu = 1e-3          # Pa·s（水）；油相 ~1e-2 将 τ 放大 10×（敏感性另注）
    phi = 0.10         # 可动流体有效孔隙率（页岩典型量级）
    dP_rep = 0.75      # 东营中间台阶 δP 代表值（0.25/0.42/0.59/0.75/0.92 MPa）
    print(f"\n[A] 每台阶排出时间 τ_relax = φ·ΔS·μ·L²/(k·δP)  [φ={phi}, μ={mu:.0e}, δP={dP_rep}MPa]")
    print(f"{'k(m²)':>10} {'L(cm)':>6} {'ΔS=0.01':>12} {'ΔS=0.03':>12} {'ΔS=0.05':>12}   (h)")
    for k in (1e-19, 1e-18, 1e-17, 1e-16):
        for L in (0.01, 0.02, 0.03):
            row = [relaxation_time(phi, dS, mu, L, k, dP_rep*1e6) / 3600 for dS in (0.01, 0.03, 0.05)]
            print(f"{k:10.0e} {L*100:6.1f} {row[0]:12.2f} {row[1]:12.2f} {row[2]:12.2f}")
    print("\n[A] 基准行（k=10nD=1e-17, L=2cm, ΔS=0.03, δP=0.75MPa）: "
          f"τ={relaxation_time(phi,0.03,mu,0.02,1e-17,0.75e6)/3600:.2f} h")

    print(f"\n[B] 残余瞬态 c_eff(t) = (δP/a)·exp(−t/τ)  [a={A_DP}MPa, δP=0.75MPa, 前缀 δP/a={0.75/A_DP:.3f}]")
    print(f"{'k(m²)':>10} {'L(cm)':>6} {'τ(h)':>7} {'c@0.5h':>8} {'c@1h':>8} {'c@2h':>8} {'c@4h':>8} {'c@8h':>8} {'c@24h':>8}")
    for k in (1e-18, 1e-17, 1e-16):
        for L in (0.01, 0.02, 0.03):
            tau = relaxation_time(phi, 0.03, mu, L, k, dP_rep*1e6)
            cs = [c_eff_residual(0.75e6, tau, A_DP*1e6, t*3600) for t in (0.5, 1, 2, 4, 8, 24)]
            print(f"{k:10.0e} {L*100:6.1f} {tau/3600:7.2f} " + "".join(f"{c:8.4f}" for c in cs))
    print("  判据：c_eff < 0.3（ν 偏离起始，t4c）；c_eff < 0.1（保守，朗缪尔存活窗）")

    print(f"\n[C] 所需平衡等待时间 t_req（c_eff<0.1）：t_req = τ·ln(δP/(a·0.1))，ln 因子 = {np.log((0.75/1.09)/0.1):.3f}")
    ln_req = np.log((0.75/1.09)/0.1)
    for k in (1e-19, 1e-18, 1e-17, 1e-16):
        for L in (0.01, 0.02, 0.03):
            tau = relaxation_time(phi, 0.03, mu, L, k, dP_rep*1e6)
            print(f"  k={k:7.0e} L={L*100:.0f}cm: τ={tau/3600:8.2f}h → t_req={tau*ln_req/3600:8.2f}h")

    print(f"\n[D] 微观 Ca（顶台阶 ΔP=3.01MPa，体力梯度 b=ΔP/L，γ=0.03N/m）：Ca=k·b/γ")
    print(f"{'k(m²)':>10} {'L=1cm':>10} {'L=2cm':>10} {'L=3cm':>10}")
    for k in (1e-19, 1e-18, 1e-17, 1e-16):
        row = [k * (PCAP_DATA*1e6 / L) / 0.03 for L in (0.01, 0.02, 0.03)]
        print(f"{k:10.0e} " + "".join(f"{c:10.1e}" for c in row))
    print("  微观 Ca 恒 ≪ 1（k=10⁻¹⁶ 时 ~10⁻⁴）——但 c_eff 是路径积分的粘性压降/毛细阈比，"
          "路径长度放大使其在未平衡瞬态可达 O(1)；微观 Ca≪1 不充分，须用 c_eff 判据。")

# ---------------- Part 3 数值：DIP 小 c 朗缪尔存活窗 ----------------
def langmuir_r2_fit(P, S):
    """双倒数线性化 1/S = 1/R_f + (a/R_f)(1/P) 的 R²（P2-6c 同口径）。
    仅判线性质量；不要求截距正（模型突破前低 P 点几何抑制使外推截距可负）。"""
    m = (S > 1e-3) & (S < 0.999)
    if m.sum() < 5:
        return None
    X = 1.0/P[m]; Y = 1.0/S[m]
    A_ = np.vstack([X, np.ones_like(X)]).T
    k_, b_ = np.linalg.lstsq(A_, Y, rcond=None)[0]
    if k_ <= 0:
        return None
    pred = k_*X + b_
    return 1 - np.sum((Y-pred)**2)/np.sum((Y-Y.mean())**2)

def sample_S_at_points(P, S, Pdata):
    """在东营数据点处插值模型 S（P=驱动压轴，S 单调）。越界用端点钳制。"""
    order = np.argsort(P)
    P_, S_ = P[order], S[order]
    return np.interp(Pdata, P_, S_)

def r2_on_points(Pdata, S_at):
    """6 点双倒数 R²（东营 5–6 点/井同权重口径）。仅判线性质量。"""
    m = (S_at > 1e-3) & (S_at < 0.999)
    if m.sum() < 5:
        return None
    X = 1.0/Pdata[m]; Y = 1.0/S_at[m]
    A_ = np.vstack([X, np.ones_like(X)]).T
    k_, b_ = np.linalg.lstsq(A_, Y, rcond=None)[0]
    if k_ <= 0:
        return None
    pred = k_*X + b_
    return 1 - np.sum((Y-pred)**2)/np.sum((Y-Y.mean())**2)

def main_numeric():
    print("\n" + "=" * 78)
    print("Part 3 数值：DIP 小 c 扫描 → 朗缪尔双倒数存活窗（东营同口径 R²≥0.93）")
    print("=" * 78)
    n, ncfg = 64, 8
    for phi in (0.31, 0.40):
        print(f"\n--- φ={phi:.2f}（{n}³ ncfg={ncfg}，朗缪尔阈值 a={A_DP}，阻力均匀）---")
        print(f"{'c':>6} {'P_c':>8} {'6点R²':>8} {'满窗R²':>8} {'存活率':>10}  P_c≤3.01?")
        for c in (0.0, 0.01, 0.03, 0.1, 0.3):
            Pcs, r6s, rfulls = [], [], []
            nok = 0
            nfit = 0
            for cfg in range(ncfg):
                rng = np.random.default_rng(cfg)
                binary = rng.random((n, n, n)) < phi
                P, S, Pc, Sc = run_dip(binary, c, seed=cfg, res_model=0)
                if Pc < 0:
                    continue
                Pcs.append(Pc)
                S_at = sample_S_at_points(P, S, PDATA)
                r2_6 = r2_on_points(PDATA, S_at)
                if r2_6 is not None:
                    r6s.append(r2_6)
                    nfit += 1
                    if r2_6 >= R2_DATA_MIN:
                        nok += 1
                mf = (S > 1e-3) & (S < 0.999) & (P >= PDATA.min()) & (P <= PCAP_DATA)
                if mf.sum() >= 10:
                    r2f = langmuir_r2_fit(P[mf], S[mf])
                    if r2f is not None:
                        rfulls.append(r2f)
            if not Pcs:
                print(f"{c:6.1f} 无突破")
                continue
            Pc_ = np.mean(Pcs)
            r6_ = np.mean(r6s) if r6s else float("nan")
            rfull_ = np.mean(rfulls) if rfulls else float("nan")
            rate = f"{nok}/{nfit}" if nfit else "—"
            ok = "OK" if Pc_ <= PCAP_DATA else "X"
            print(f"{c:6.2f} {Pc_:8.3f} {r6_:8.3f} {rfull_:8.3f} {rate:>10}  {ok}")

if __name__ == "__main__":
    main_analytic()
    main_numeric()
