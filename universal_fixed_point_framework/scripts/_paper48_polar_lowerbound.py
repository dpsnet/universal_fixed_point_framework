# -*- coding: utf-8 -*-
"""
Paper 48 偏振选择因子刚性下界——正确的偶极盘平均数值计算
========================================================
目的：替代外部提供的错误证明（0.835 下界代数不自洽、面平均冒充盘平均），
给出物理正确的偏振盘平均 EW 压低因子区间。

物理模型（弱线极限，纯吸收，无磁光近似）：
- 全局偶极磁场；磁轴与视线夹角 alpha（磁倾角）
- 盘面上每个面元 (theta, phi)：mu = cos(theta)，面元法线 = 视线方向 r-hat
- 局部磁场方向由偶极几何决定：B ∝ 2cos(theta_m) r_hat + sin(theta_m) theta_m_hat
- Unno 本征模分解：I 通道线吸收系数
    eta_I^L(psi) = (3/2)[ g_pi * sin^2(psi) + (1-g_pi)/2 * (1+cos^2(psi)) ] * eta_L
  其中 g_pi = f_pi/f_0 为 π 分量振子强度占比（TRK: g_pi + g_sigma = 1），
  psi 为局部磁场与视线夹角。
- 弱线极限 EW ∝ ∫ eta_I^L dnu，故
    x(alpha, g_pi) = EW_obs/EW_total = <eta_I^L>_disk / eta_L
  = 1 + (3*S(alpha)-2)*(3*g_pi-1)/4,  S(alpha) = <sin^2(psi)>_disk (mu 加权)

要点（与外部证明的根本差异）：
1) 面平均 S=2/3 时 x≡1（能量守恒/消偏振真定理），偏振效应完全来自
   (a) 盘平均偏离面平均（mu 权重）与 (b) 振子强度重分配 g_pi != 1/3。
2) g_pi=1/3（正常 Zeeman 线性区）时 x≡1 对任意 alpha 恒成立——偏振零影响。
3) 只有 g_pi != 1/3（强场氢原子流形重分配）才有非零效应，且方向依赖 S 与 g_pi。

输出：
- S(alpha) 曲线（0-90 度）
- x(alpha, g_pi) 区间表
- 与观测 46.9% 总 EW 缺失 / §4.9 线序梯度的对比判定
"""
import json
import math

# ---------------------------------------------------------------- 偶极盘平均 S(alpha)
def dipole_sin2_psi_disk(alpha_deg, n_mu=400, n_phi=400):
    """数值 mu 加权盘平均 <sin^2(psi)>，偶极场，磁轴与 LOS 夹角 alpha。"""
    alpha = math.radians(alpha_deg)
    m = (math.sin(alpha), 0.0, math.cos(alpha))  # 磁轴单位向量（LOS = +z）
    num = 0.0
    den = 0.0
    for i in range(1, n_mu + 1):
        mu = (i - 0.5) / n_mu
        st = math.sqrt(max(0.0, 1.0 - mu * mu))
        for j in range(n_phi):
            phi = 2.0 * math.pi * (j + 0.5) / n_phi
            cp = math.cos(phi)
            sp = math.sin(phi)
            # 面元位置（观测者坐标）
            r = (st * cp, st * sp, mu)
            # 磁轴系极角
            cm = r[0]*m[0] + r[1]*m[1] + r[2]*m[2]  # cos(theta_m)
            sm2 = max(0.0, 1.0 - cm*cm)
            sm = math.sqrt(sm2)
            # 磁场方向：2 cos(theta_m) r_hat + sin(theta_m) theta_m_hat
            # theta_m_hat（极角增大方向）= (cos(theta_m) r - m)/sin(theta_m)
            if sm > 1e-12:
                th_hat = ((cm*r[0]-m[0])/sm, (cm*r[1]-m[1])/sm, (cm*r[2]-m[2])/sm)
            else:
                th_hat = (0.0, 0.0, 0.0)  # 极区退化，B 沿 r
            bx = 2.0*cm*r[0] + sm*th_hat[0]
            by = 2.0*cm*r[1] + sm*th_hat[1]
            bz = 2.0*cm*r[2] + sm*th_hat[2]
            bnorm = math.sqrt(bx*bx + by*by + bz*bz)
            cos_psi = bz / bnorm if bnorm > 1e-12 else 1.0
            sin2_psi = 1.0 - cos_psi*cos_psi
            w = mu
            num += w * sin2_psi
            den += w
    return num / den

# ---------------------------------------------------------------- x(alpha, g_pi)
def x_factor(S, g_pi):
    """EW 比值 x = 1 + (3S-2)(3g_pi-1)/4。"""
    return 1.0 + (3.0*S - 2.0) * (3.0*g_pi - 1.0) / 4.0

# ---------------------------------------------------------------- 主流程
def main():
    alphas = list(range(0, 91, 10))
    S_vals = {}
    for a in alphas:
        S_vals[a] = dipole_sin2_psi_disk(a)
        print(f"alpha={a:3d} deg : S=<sin^2(psi)>_disk = {S_vals[a]:.4f}")

    # g_pi 扫描：1/3（正常 Zeeman）→ 0.5 → 0.6 → 0.7（强场 π 集中）
    g_pis = [1.0/3.0, 0.40, 0.50, 0.60, 0.70]
    print("\n--- x = EW_obs/EW_total = 1 + (3S-2)(3g_pi-1)/4 ---")
    header = "alpha\\g_pi | " + " | ".join(f"g={g:.3f}" for g in g_pis)
    print(header)
    x_table = {}
    for a in alphas:
        S = S_vals[a]
        row = [x_factor(S, g) for g in g_pis]
        x_table[a] = {f"g_{g:.3f}": r for g, r in zip(g_pis, row)}
        print(f"  {a:3d}     | " + " | ".join(f"{r:.4f}" for r in row))

    # 判定：与观测 46.9% 总缺失（x_obs = 0.531）对比
    x_obs = 0.531  # 1 - 0.469
    print(f"\n--- 观测基准：总 EW 比值 x_obs = {x_obs}（缺失 46.9%）---")
    # 随机磁倾角分布（各向同性：P(alpha) ∝ sin(alpha)，峰值在 90°）
    # 用 5° 步长数值积分 P(alpha)*x(alpha, g_pi)
    results = {}
    for g in g_pis:
        # 各向同性平均
        tot = 0.0
        wsum = 0.0
        for a_deg in range(0, 91, 5):
            S = dipole_sin2_psi_disk(a_deg, n_mu=200, n_phi=200)
            w = math.sin(math.radians(a_deg)) if a_deg > 0 else 0.0
            tot += w * x_factor(S, g)
            wsum += w
        x_avg = tot / wsum
        results[f"g_{g:.3f}"] = {
            "x_iso_avg": x_avg,
            "x_min": min(x_factor(dipole_sin2_psi_disk(a, n_mu=200, n_phi=200), g) for a in range(0, 91, 5)),
            "x_max": max(x_factor(dipole_sin2_psi_disk(a, n_mu=200, n_phi=200), g) for a in range(0, 91, 5)),
            "can_explain_469": x_avg <= x_obs,
        }
        print(f"g_pi={g:.3f}: x_iso_avg={x_avg:.4f}  (缺失 {(1-x_avg)*100:.1f}%), "
              f"区间 [{results[f'g_{g:.3f}']['x_min']:.4f}, {results[f'g_{g:.3f}']['x_max']:.4f}], "
              f"可解释 46.9%? {'是' if results[f'g_{g:.3f}']['can_explain_469'] else '否'}")

    out = {
        "model": "dipole disk-average, weak-line limit, pure absorption, no magneto-optical",
        "x_formula": "1 + (3S-2)(3g_pi-1)/4, S=<sin^2(psi)>_disk(mu-weighted)",
        "S_alpha": S_vals,
        "x_table": x_table,
        "g_pi_summary": results,
        "x_obs_total_ew": x_obs,
        "note": "g_pi 中场真实值需由 RWA/Zhao 分支比代入；随机 alpha 各向同性平均",
    }
    outpath = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paper48_polar_lowerbound.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nSaved -> {outpath}")

if __name__ == "__main__":
    main()
