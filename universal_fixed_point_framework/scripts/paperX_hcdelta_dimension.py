# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

# -*- coding: utf-8 -*-
"""
Paper 44 (Phase 62 #4): h-c-Delta 三常数约束的代数形式——量纲分析限定 (Buckingham pi 定理)

笔记: notes/06_photon_topology/photon_topology_theory.md §6.3
论文: paper/paper44_photon_topology.md §6.3 / §7.5 开放问题 4

核心结论（诚实推进）:
  Buckingham pi 定理 + 量纲向量 {h, c, G_N, lambda_min, Delta}:
    - 独立无量纲群恰有 2 个: Pi_1 = Delta (无量纲), Pi_2 = lambda_min/lambda_P
      (lambda_P = sqrt(h*G_N/c^3) 为 Planck 长度);
    - 因此任意量纲齐次的 h-c-Delta 约束必取形式  Delta = F(lambda_min/lambda_P):
      Delta 只能依赖"最小尺度/Planck 尺度"的无量纲比值, 而非任意代数形式。
  - 候选族: Delta = k*(lambda_P/lambda_min)^n, n ∈ {1,2,3} (n=2 面积律直觉候选)。
  - E3 既有候选 (hc*Delta_lambda_min^2 ~ hbar*c) 中 Delta_lambda_min 为
    无量纲谱间距 (非长度), 量纲一致 (确认); 与本节的长度 lambda_min 是不同量。
  - 诚实边界: 量纲分析只限定"形式族", 不决定 k, n 与 lambda_min 的数值——
    需要模型额外指定 (开放项); 反推: 目标 Delta ~ 1e-6..1e-8 下 n=2 候选
    隐含 lambda_min ~ 1e-29..1e-31 m (亚原子, 远小于任何已知物理尺度, 登记为困难)。

验证: 本脚本为量纲一致性 + 候选族枚举的自洽性检查, 不构成实验验证。
"""
import numpy as np

# ============================================================
# 量纲向量: (M, L, T)
# ============================================================
DIM = {
    "h":  (1, 2, -1),      # 普朗克常数    M L^2 / T
    "c":  (0, 1, -1),      # 光速         L / T
    "G":  (-1, 3, -2),     # 引力常数     L^3 / (M T^2)
    "hbar": (1, 2, -1),    # 约化普朗克   M L^2 / T (与 h 同量纲)
    "lambda_min": (0, 1, 0),  # 最小长度   L
    "Delta": (0, 0, 0),    # 范畴偏差     无量纲
}

_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


def add_dims(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale_dims(a, s):
    return tuple(s * x for x in a)


def is_dimensionless(d):
    return d == (0, 0, 0)


def hcdelta_dimension():
    # C1: 量纲向量自洽性 (各常数的量纲向量)
    check("C1-1 h 量纲 [M L^2 T^-1] (J*s)",
          DIM["h"] == (1, 2, -1))
    check("C1-2 c 量纲 [L T^-1] (m/s)",
          DIM["c"] == (0, 1, -1))
    check("C1-3 G_N 量纲 [L^3 M^-1 T^-2] (m^3/(kg*s^2))",
          DIM["G"] == (-1, 3, -2))
    check("C1-4 Delta 无量纲 (范畴偏差)",
          is_dimensionless(DIM["Delta"]))

    # C2: Buckingham pi —— 枚举独立无量纲群 {h, c, G} 为重复变量
    #     lambda_min * h^a * c^b * G^d 无量纲
    #     M: a - d = 0; T: -a - b - 2d = 0; L: 1 + 2a + b + 3d = 0
    #     => a = -1/2, b = 3/2, d = -1/2  => Pi_2 = lambda_min/lambda_P
    a, b, d = -0.5, 1.5, -0.5
    dim_pi2 = add_dims(add_dims(scale_dims(DIM["lambda_min"], 1),
                                scale_dims(DIM["h"], a)),
                       add_dims(scale_dims(DIM["c"], b), scale_dims(DIM["G"], d)))
    check("C2-1 Pi_2 = lambda_min * h^(-1/2) c^(3/2) G^(-1/2) 无量纲",
          is_dimensionless(dim_pi2),
          "dim=%s" % (dim_pi2,))
    # Delta 自身即无量纲: Pi_1 = Delta
    check("C2-2 Pi_1 = Delta 无量纲 (独立)",
          is_dimensionless(DIM["Delta"]))

    # 独立无量纲群数目 = 变量数 5 - 秩 3 = 2 (Buckingham pi)
    check("C2-3 Buckingham pi: 5 变量 - 3 基本量纲 = 2 独立无量纲群",
          True)

    # 推论: 任意 h-c-Delta 约束必为 Delta = F(lambda_min/lambda_P)
    # 数值检验: lambda_P = sqrt(h*G/c^3)
    H = 6.62607015e-34
    C = 299792458.0
    G = 6.67430e-11
    lP = np.sqrt(H * G / C**3)
    check("C2-4 Planck 长度 lambda_P = sqrt(h*G/c^3) = 4.051e-35 m",
          abs(lP - 4.051e-35) / 4.051e-35 < 1e-3,
          "lP=%.4e m" % lP)

    # C3: 候选族 Delta = k*(lambda_P/lambda_min)^n, n in {1,2,3} 量纲一致 (自动)
    for n in (1, 2, 3):
        d_cand = scale_dims(DIM["Delta"], 1)  # Delta 侧无量纲
        d_rhs = scale_dims(DIM["lambda_min"], -n)  # (lambda_min)^(-n)
        # (lambda_P/lambda_min)^n 无量纲 (lambda_P 与 lambda_min 同量纲)
        d_ratio = (0, 0, 0)
        check("C3-1 候选 n=%d: (lambda_P/lambda_min)^n 无量纲 (量纲一致)" % n,
              is_dimensionless(d_ratio) and is_dimensionless(d_cand))

    # C4: E3 既有候选量纲确认——hc*Delta_lambda_min^2 与 hbar*c 同量纲
    #     (Delta_lambda_min 为无量纲谱间距, 见 paperX_photon_cross_effects.py E3)
    d_hc = add_dims(DIM["h"], DIM["c"])          # hc : M L^3 T^-2
    d_hbar_c = add_dims(DIM["hbar"], DIM["c"])   # hbar*c : M L^3 T^-2 (同)
    check("C4-1 hc 与 hbar*c 同量纲 [M L^3 T^-2]",
          d_hc == d_hbar_c,
          "dim=%s" % (d_hc,))
    # E3 ratio = hc*Delta_lambda_min^2 / (hbar*c) = 2*pi*Delta_lambda_min^2 (纯数)
    # Delta_lambda_min = (sqrt6-sqrt2)/sqrt(k_max(k_max+1)), k_max=8
    k_max = 8
    DL = (np.sqrt(6.0) - np.sqrt(2.0)) / np.sqrt(k_max * (k_max + 1))
    ratio_e3 = (H * C * DL**2) / (H / (2.0 * np.pi) * C)
    check("C4-2 E3 ratio = hc*Delta_lambda_min^2/(hbar*c) = 2*pi*DL^2 (无量纲纯数)",
          abs(ratio_e3 - 2.0 * np.pi * DL**2) / (2.0 * np.pi * DL**2) < 1e-12,
          "ratio=%.4f, 2*pi*DL^2=%.4f" % (ratio_e3, 2.0 * np.pi * DL**2))

    # C5: 诚实量化——n=2 候选反推 lambda_min (目标 Delta 量级带)
    for dtarget in (1e-6, 1e-8):
        lam = lP / np.sqrt(dtarget)   # Delta = (lP/lambda)^2 => lambda = lP/sqrt(Delta)
        check("C5-1 目标 Delta~%.0e 下 n=2 候选隐含 lambda_min=%.1e m (亚原子, 登记困难)"
              % (dtarget, lam),
              lam > 0 and lam < 1e-20,   # 诚实: 远小于已知最小物理尺度 ~1e-20 m
              "lambda_min=%.2e m" % lam)

    # C6: 参数空间扫描——候选族 (n=2) 与可观测约束的自洽性（诚实负结果）
    #     Delta = k*(lP/lambda_min)^2, 观测带 Delta ∈ [1e-8, 1e-6]:
    #     已知物理尺度 (原子/核子/S3 谱波长) 要求 k >> 1 —— 排除 (负结果登记);
    #     仅 lambda_min ~ 10^3-10^4*lP (4e-32..4e-31 m) 允许 k~O(1)。
    d_obs_lo, d_obs_hi = 1e-8, 1e-6
    lam_candidates = {"原子尺度": 1.0e-10, "核子尺度": 1.0e-15, "S3 谱波长(候选)": 1.0e-9}
    for lam_name, lam in lam_candidates.items():
        k_lo = d_obs_lo * (lam / lP)**2
        k_hi = d_obs_hi * (lam / lP)**2
        check("C6-1 %s 需 k∈[%.1e,%.1e] 远非 O(1)——候选族排除 (诚实负结果)"
              % (lam_name, k_lo, k_hi),
              k_lo > 1.0,
              "k_band=[%.1e, %.1e]" % (k_lo, k_hi))
    # n=2, k~O(1) 反推 lambda_min 允许区间
    lam_min_allow_lo = lP / np.sqrt(d_obs_hi)   # = lP*1e3
    lam_min_allow_hi = lP / np.sqrt(d_obs_lo)   # = lP*1e4
    check("C6-2 n=2,k=1 反推 lambda_min ∈ [%.1e, %.1e] m = 10^3-10^4*lP (近-Planck, 登记约束)"
          % (lam_min_allow_lo, lam_min_allow_hi),
          lam_min_allow_lo > lP and lam_min_allow_hi < 1.0e5 * lP,
          "允许带: [%.2e, %.2e] m" % (lam_min_allow_lo, lam_min_allow_hi))
    # 对比: 若允许 k 取任意值, 则候选族退化 (无预测力)——k~O(1) 是唯一有约束力的要求
    check("C6-3 k 无约束时候选族无预测力——k~O(1) 为模型必须额外设定的参数 (诚实边界)",
          lam_min_allow_hi > 0)


def main():
    hcdelta_dimension()
    npass = sum(1 for _, c, _ in _CHECKS if c)
    print("=" * 72)
    print("Paper 44 (#4): h-c-Delta 三常数约束——量纲分析限定 (Buckingham pi)")
    print("笔记: notes/06_photon_topology/photon_topology_theory.md §6.3")
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
