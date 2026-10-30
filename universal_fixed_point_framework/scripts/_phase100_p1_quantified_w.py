# -*- coding: utf-8 -*-
"""Phase 100 P1：拓扑禁戒频率的量化重构（w 判据可计算版）
目标：给出 η_forb(B) = 1 − W_rad(B)/W_rad(0) 的数值曲线
方法：
  Part 1  无场氢 Balmer 跃迁 n=2→n' 的偶极矩阵元按 Δm 通道分解（π:Δm=0, σ±:Δm=±1）
  Part 2  Landau 填充模型：强场下末态 m 分布 P_fill(m|B,T)（玻尔兹曼 × Landau 能级序）
  Part 3  辐射权重 W_rad(B) = Σ 通道 |径向|²·|角向|²·(末态 m 可及性)
  Part 4  η_forb(B,T) 曲线 + 对照观测 46.9% 与标准束缚态数衰减 ~12%
模型近似（显式标注）：末态 m 可及性 = 玻尔兹曼填充（白矮星 Teff~1e4 K）；π 通道假设保持、σ 通道按末态 m'=±1 填充率抑制
诚实边界：本脚本给出"σ 通道 Landau 填充抑制"这一子机制的量化；完整 w 判据（横向流环量）见笔记开放项
"""
import json, math
import numpy as np

# ---------- 氢径向函数（解析，原子单位） ----------
def fact(n):
    return math.factorial(n)

def laguerre(n, alpha, x):
    """associated Laguerre L_n^alpha(x)，数值（递推）"""
    L0 = 1.0
    if n == 0:
        return L0
    L1 = 1.0 + alpha - x
    if n == 1:
        return L1
    Lm1, L = L0, L1
    for k in range(1, n):
        Lk = ((2*k + 1 + alpha - x) * L - (k + alpha) * Lm1) / (k + 1)
        Lm1, L = L, Lk
    return L

def R_nl(n, l, r):
    """氢径向波函数（原子单位，实数归一化）"""
    if r <= 0:
        return 0.0
    rho = 2.0 * r / n
    norm = math.sqrt((2.0 / n) ** 3 * fact(n - l - 1) / (2.0 * n * fact(n + l)))
    return norm * math.exp(-r / n) * rho ** l * laguerre(n - l - 1, 2 * l + 1, rho)

def radial_matrix(n1, l1, n2, l2, rmax=120.0, npts=40000):
    """⟨n2 l2|r|n1 l1⟩ = ∫ R2 R1 r³ dr（梯形积分）"""
    r = np.linspace(1e-6, rmax, npts)
    R1 = np.array([R_nl(n1, l1, x) for x in r])
    R2 = np.array([R_nl(n2, l2, x) for x in r])
    integ = R1 * R2 * r ** 3
    return float(np.trapezoid(integ, r))

# ---------- 角向矩阵元 ⟨ℓ'm'|Y_1q|ℓm⟩（数值积分球谐） ----------
def Y_lm(l, m, th, ph):
    """球谐 Y_l^m（标准 Condon-Shortley），实参数数组"""
    # P_l^|m|(cosθ)：用递推
    mu = np.cos(th)
    m_abs = abs(m)
    if l == 0:
        P = np.ones_like(mu)
    else:
        Pmm = np.ones_like(mu)
        for i in range(1, m_abs + 1):
            Pmm = -Pmm * (2 * i - 1) * np.sin(th)  # P_m^m ∝ (−1)^m (2m−1)!! sin^m θ
        if l == m_abs:
            P = Pmm
        else:
            Pm1 = Pmm
            Pmm_prev = np.zeros_like(mu)
            for i in range(m_abs + 1, l + 1):
                P = ((2 * i - 1) * mu * Pm1 - (i + m_abs - 1) * Pmm_prev) / (i - m_abs)
                Pmm_prev, Pm1 = Pm1, P
    norm = math.sqrt((2 * l + 1) / (4 * math.pi) * fact(l - m_abs) / fact(l + m_abs))
    return norm * P * np.exp(1j * m * ph)

def angular_matrix(l1, m1, l2, m2, q):
    """⟨l2 m2|Y_1q|l1 m1⟩ 数值积分（Gauss-Legendre 风格 θ 网格 + 均匀 φ）"""
    nth, nph = 300, 60
    th = np.linspace(1e-4, math.pi - 1e-4, nth)
    ph = np.linspace(0, 2 * math.pi, nph, endpoint=False)
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    Y1 = Y_lm(1, q, TH, PH)
    Y2 = Y_lm(l2, m2, TH, PH).conj()
    Y1f = Y_lm(l1, m1, TH, PH)
    integ = Y2 * Y1 * Y1f * np.sin(TH)
    dth = th[1] - th[0]
    dph = ph[1] - ph[0]
    return float(np.trapezoid(np.trapezoid(integ, ph, axis=1), th))

def dipole_matrix(n1, l1, m1, n2, l2, m2, q):
    """⟨n2 l2 m2| r_q |n1 l1 m1⟩ = 径向 × 角向（r_q: q=0→z, ±1→(x±iy)/√2）"""
    rad = radial_matrix(n1, l1, n2, l2)
    ang = angular_matrix(l1, m1, l2, m2, q)
    return rad * ang

# ---------- Part 1：无场 Balmer 通道权重 ----------
def balmer_channel_weights(n_up):
    """n=2 → n_up 的 π/σ± 通道权重（下态 2s+2p 按简并度加权）
    返回 {q: 权重}，q=0→π, +1→σ+, −1→σ−"""
    lower = [(2, 0, 0)]                      # 2s
    lower += [(2, 1, m) for m in (-1, 0, 1)]  # 2p
    w_lower = {st: (1 if st[1] == 0 else 1) for st in lower}  # 简并等权
    W = {q: 0.0 for q in (0, 1, -1)}
    for (n1, l1, m1) in lower:
        for l2 in range(0, n_up):
            dl = l2 - l1
            if abs(dl) != 1:
                continue
            for m2 in range(-l2, l2 + 1):
                dm = m2 - m1
                if dm not in (0, 1, -1):
                    continue
                q = dm
                d = dipole_matrix(n1, l1, m1, n_up, l2, m2, q)
                W[q] += abs(d) ** 2
    return W

# ---------- Part 2：Landau 填充模型 ----------
def landau_fill_m(B_T, m, T_K):
    """强场末态 m 层的玻尔兹曼填充权重（相对 m=0 基态 Landau 层）
    E_m(B) − E_0(B) ≈ |m|·ω_c/2（对称规范 Landau 序，最低层 m=0,N=0）
    ω_c = ℏeB/m_e，eV：1.16e-4·B_T/2（每单位 |m|）"""
    kB_T = 8.617333262e-5          # eV/K
    omega_c = 1.16e-4 * B_T        # eV（ω_c=ℏeB/m_e）
    dE = abs(m) * omega_c / 2.0    # |m| 阶 Landau 间隔（最低层 m=0）
    if dE <= 0:
        return 1.0
    return math.exp(-dE / (kB_T * T_K))

# ---------- Part 3/4：η_forb(B) ----------
def eta_forbidden(B_T, T_K, W0):
    """W0 = {q: 无场权重}
    假设：末态 m'=±1 层按填充率抑制（σ 通道），m'=0 层保持（π 通道）
    η_forb = 1 − W(B)/W(0)"""
    W = {q: 0.0 for q in (0, 1, -1)}
    # 通道可及性：σ 通道（Δm=±1）需要末态 m' 层填充
    # 简化：σ⁺ 通道末态 m' = m_i + 1，σ⁻ 末态 m' = m_i − 1；加权填充率
    for q, w0 in W0.items():
        if q == 0:
            W[q] = w0 * 1.0                 # π 假设保持
        else:
            m_req = 1                       # 末态 Landau 层 |m'|≥1
            fill = landau_fill_m(B_T, m_req, T_K)
            W[q] = w0 * fill
    Wtot = sum(W.values())
    W0tot = sum(W0.values())
    return 1.0 - Wtot / W0tot, W, W0tot

def main():
    B_fields = [100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0]  # T
    T_K = 12000.0
    results = {"model": "σ 通道 Landau 填充抑制（π 保持）", "T_K": T_K,
               "levels": {}, "eta_curve": [], "conclusions": {}}
    w0_total = {"W_pi0": 0.0, "W_sigma0": 0.0, "sigma_fraction": 0.0}
    for n_up in (3, 4, 5):
        W0 = balmer_channel_weights(n_up)
        w0_total["W_pi0"] += W0[0]
        w0_total["W_sigma0"] += W0[1] + W0[-1]
        level = {"n_up": n_up, "W_pi0": W0[0], "W_sig_plus0": W0[1], "W_sig_minus0": W0[-1], "B_curve": []}
        for B in B_fields:
            eta, W, W0tot = eta_forbidden(B, T_K, W0)
            level["B_curve"].append({"B_T": B, "eta_forb": eta, "W_rad(B)/W_rad(0)": 1.0 - eta})
        results["levels"][f"n={n_up}"] = level
    sf = w0_total["W_sigma0"] / (w0_total["W_pi0"] + w0_total["W_sigma0"])
    w0_total["sigma_fraction"] = sf
    results["baseline"] = w0_total
    # 总曲线（三线上态等权平均）
    for B in B_fields:
        etas = []
        for n_up in (3, 4, 5):
            etas.append(eta_forbidden(B, T_K, balmer_channel_weights(n_up))[0])
        results["eta_curve"].append({"B_T": B, "eta_forb_avg": float(np.mean(etas)),
                                     "per_line": {f"n={n}": float(e) for n, e in zip((3, 4, 5), etas)}})
    # 对照
    mid = results["eta_curve"][3] if len(results["eta_curve"]) > 3 else results["eta_curve"][-1]
    results["conclusions"] = {
        "obs_mid_field_46.9pct": 0.469,
        "model_mid_field_eta": mid["eta_forb_avg"],
        "model_reaches_46.9pct": bool(mid["eta_forb_avg"] >= 0.469 - 0.05),
        "std_bound_state_decay_12pct": 0.12,
        "sigma_fraction_baseline": sf,
        "note": "η_forb = σ 通道份额 × (1 − 末态 m=±1 层填充率)。若 σ 份额≈2/3 且强场末态全部 Landau 到 m=0 层，则 η_forb→σ 份额上限。"
                "π 通道保持假设是关键简化；完整 w 判据（横向流环量）与 π 悖论见笔记开放项。",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase100_p1_quantified_w.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=float)
    print("=" * 70)
    print("Phase 100 P1：σ 通道 Landau 填充抑制（量化初步）")
    print(f"基线 σ 份额 = {sf:.4f}（π 保持假设下 η_forb 上限）")
    print("B(T)    η_forb(Hα)  η_forb(Hβ)  η_forb(Hγ)  平均")
    for row in results["eta_curve"]:
        print(f"{row['B_T']:7.0f}  {row['per_line']['n=3']:.4f}      {row['per_line']['n=4']:.4f}      "
              f"{row['per_line']['n=5']:.4f}      {row['eta_forb_avg']:.4f}")
    print(f"中场(3000 T)模型 η = {mid['eta_forb_avg']:.4f} vs 观测 0.469 | 标准束缚态衰减 0.12")
    print(f"结果已写入 _phase100_p1_quantified_w.json")

if __name__ == "__main__":
    main()
