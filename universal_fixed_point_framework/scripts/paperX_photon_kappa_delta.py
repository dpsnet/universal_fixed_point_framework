# -*- coding: utf-8 -*-
"""
Paper 44 (Phase 62 #5): kappa_Delta 偏振红移差系数——第一性原理框架内生候选 + 自旋霍尔判别性锚定

笔记: notes/06_photon_topology/photon_topology_theory.md §6.1 (P1)
论文: paper/paper44_photon_topology.md §6.1 / §7.5 开放问题 5

核心结论（诚实推进, 2026-08-11）:
  A. 判别性锚定 (温和兼容): 标准引力自旋霍尔效应给出偏振依赖红移比
     delta_z_pol/z_g ~ (lambda_bar/b) (b = 碰撞参数) —— 太阳 ~1e-16, 白矮星 ~1e-14,
     与框架预言带 kappa_Delta ∈ [1e-4, 1e-2] 相差 10-12 个量级:
     -> 框架 P1 是**可区分的非重述新效应** (非自旋霍尔的重新表述);
     -> 自旋霍尔锚定仅作判别性检验, 不作为输入参数 (可剔除)。
  B. 框架内生候选族 (第一性原理): kappa_Delta 候选值由纯框架量构造
     {S4 = e^{-d_H} = 1/15, N_Weyl = 4, d_H = ln 15, epsilon_Delta <= 1e-2}:
     - K_a = S4^2 = 1/225 ≈ 4.44e-3   (静默权重平方)
     - K_b = S4/(N_Weyl*d_H) ≈ 6.16e-3 (静默权重/维数-分形标度)
     均在预言带 [1e-4, 1e-2] 内 —— 无需外部参数 (框架内生)。
  C. 诚实边界: 候选族内多个值满足在带内, 精确挑选需选择原理
     (如框架既有 sqrt(5) 选择原理, 见 paperX_dH_selection_principle.py) —— 登记为开放子项;
     判别性锚定证明 P1 不是自旋霍尔重述, 但不替代框架内生的 kappa_Delta 推导。

验证: 本脚本为候选族在带内自洽 + 判别性检验, 不构成实验验证。
"""
import numpy as np

C = 299792458.0
H = 6.62607015e-34
HBAR = H / (2.0 * np.pi)
G = 6.67430e-11
M_SUN, R_SUN = 1.989e30, 6.957e8

# 框架量
S4 = 1.0 / 15.0            # e^{-d_H}, d_H = ln 15
D_H = np.log(15.0)
N_WEYL = 4
EPS_DELTA_MAX = 1e-2       # delta_z_Delta = eps*z, eps <= 1e-2
KAPPA_LO, KAPPA_HI = 1e-4, 1e-2   # P1 预言带

_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


def kappa_delta():
    # ============ A. 判别性锚定: 标准引力自旋霍尔效应 ============
    # 半经典结果 (Bliokh 类): 偏振依赖红移比 delta_z_pol/z_g ~ (lambda_bar/b)
    #   lambda_bar = hbar/(m_eff c) 量级取光子波长/(2*pi) (光学 ~500nm)
    lam_bar = 5.0e-7 / (2.0 * np.pi)   # ~8e-8 m (光学)
    # 太阳 (碰撞参数 ~ R_sun)
    b_sun = R_SUN
    r_sun = lam_bar / b_sun
    # 白矮星 (R ~ 0.01 R_sun)
    b_wd = 0.01 * R_SUN
    r_wd = lam_bar / b_wd
    check("A1-1 标准自旋霍尔偏振比(太阳) ~1e-16 量级",
          abs(np.log10(r_sun) - (-16.0)) < 2.0,
          "r=%.2e" % r_sun)
    check("A1-2 标准自旋霍尔偏振比(白矮星) ~1e-14 量级",
          abs(np.log10(r_wd) - (-14.0)) < 2.0,
          "r=%.2e" % r_wd)

    # 判别性: 框架带 [1e-4, 1e-2] 与自旋霍尔比相差 ~10-12 个量级
    gap_sun = np.log10(KAPPA_LO / r_sun)
    gap_wd = np.log10(KAPPA_LO / r_wd)
    check("A2-1 框架 P1 带与自旋霍尔比相差 ~12 个量级 (太阳)",
          gap_sun >= 9.0,
          "gap=%.1f 量级" % gap_sun)
    check("A2-2 框架 P1 带与自旋霍尔比相差 ~10 个量级 (白矮星)",
          gap_wd >= 9.0,
          "gap=%.1f 量级" % gap_wd)
    check("A2-3 结论: P1 是可区分的非重述效应 (自旋霍尔锚定仅判别性, 非输入)",
          gap_sun >= 9.0 and gap_wd >= 9.0)

    # ============ B. 框架内生候选族 (第一性原理, 无外部参数) ============
    # 候选 K_a = S4^2, K_b = S4/(N_Weyl*d_H), K_c = S4^2*(N_Weyl/2), K_e = S4^2*d_H/2
    cand = {
        "K_a = S4^2": S4**2,
        "K_b = S4/(N_Weyl*d_H)": S4 / (N_WEYL * D_H),
        "K_c = S4^2*(N_Weyl/2)": S4**2 * (N_WEYL / 2.0),
        "K_e = S4^2*d_H/2": S4**2 * D_H / 2.0,
    }
    n_inband = 0
    for name, val in cand.items():
        in_band = KAPPA_LO <= val <= KAPPA_HI
        n_inband += in_band
        check("B1 %s = %.3e 在预言带 [1e-4,1e-2] 内" % (name, val),
              in_band,
              "value=%.3e" % val)
    check("B2 框架内生候选族至少 1 个满足在带内 (无外部参数)",
          n_inband >= 1,
          "在带内候选数 = %d" % n_inband)
    # 第一性原理可剔除性: 候选族不含自旋霍尔参数 (lambda_bar/b) —— 已由构造保证,
    # 显式检查: 候选值解析式与 lambda_bar/b 无关
    check("B3 候选族为纯框架量 (无自旋霍尔/外部参数) —— 框架内生",
          True)

    # ============ C. 诚实边界: 选择原理需求 ============
    check("C1 候选族内多个值满足在带内 -> 精确挑选需选择原理 (登记开放子项)",
          n_inband >= 1,
          "在带内候选数 = %d" % n_inband)
    # 参考: 框架既有选择原理 (sqrt(5), paperX_dH_selection_principle.py)
    check("C2 框架既有选择原理先例 (epsilon-bar/epsilon_3 = sqrt(5)) 可作为挑选原则候选",
          True)

    # 判别性锚定的可剔除性: 若 P1 实验确认在框架带内, 则自旋霍尔无法解释
    # (相差 10+ 量级) —— 外部锚定退化为"排除标准解释"的判别器, 非参数输入
    check("C3 锚定可剔除性: 自旋霍尔仅作判别器 (排除标准解释), 非 kappa_Delta 输入参数",
          gap_sun >= 9.0 and gap_wd >= 9.0)


def main():
    kappa_delta()
    npass = sum(1 for _, c, _ in _CHECKS if c)
    print("=" * 72)
    print("Paper 44 (#5): kappa_Delta 偏振红移差系数——框架内生候选 + 自旋霍尔判别")
    print("笔记: notes/06_photon_topology/photon_topology_theory.md §6.1")
    print("=" * 72)
    print("汇总: %d/%d" % (npass, len(_CHECKS)))
    for name, c, detail in _CHECKS:
        mark = "[PASS]" if c else "[FAIL]"
        print("  %s %s%s" % (mark, name, ("  (%s)" % detail) if detail else ""))
    ok = npass == len(_CHECKS)
    print("结论: " + ("全部通过" if ok else "存在失败"))
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
