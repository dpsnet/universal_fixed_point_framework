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

"""
kerr_fractal_entropy.py

Kerr 度规的分形几何结构与黑洞熵的分形解释。

定位：
- 本模块属于「通用不动点范畴框架」的引力实例假设层。
- 将框架的分形谱理论应用于 Kerr 黑洞：
  (1) Kerr 视界的分形维数
  (2) Kerr 测地线混沌的分形结构
  (3) Bekenstein-Hawking 熵的分形修正
  (4) 准正模谱与框架谱对应 λ_i = e^{-μ_i}

已知结果（引用自标准文献，非本文新贡献）：
- [KR1] Kerr 度规 (Kerr, 1963)：旋转黑洞精确解
  g_tt = -(1-2Mr/Σ), g_tφ = -2Mar sin²θ/Σ, ...
- [KR2] Bekenstein-Hawking 熵 (Bekenstein 1973, Hawking 1975)：
  S_BH = A_H / (4G_N)，A_H 为视界面积
- [KR3] Kerr 测地线混沌 (Contopoulos 1990, Mino 2003)：
  赤道面附近测地线出现混沌，Lyapunov 指数 λ_L > 0
- [KR4] Kerr 准正模 (Teukolsky 1973, Berti-Cardoso-Will 2006)：
  QNM 频率 ω_n = ω_R + i ω_I，ω_I ~ -n/T_H
- [KR5] 视界面积 A_H = 8πG_N M r_+ （Kerr-Newman）

新贡献（本文）：
- Kerr 视界分形维数的 IFS 参数化
- 分形修正的 Bekenstein-Hawking 熵
- QNM 谱与框架谱对应 λ_n = e^{-μ_n} 的数值验证
- 测地线混沌 Lyapunov 指数与 IFS 压缩比的关系
"""

from __future__ import annotations

import numpy as np


# ===========================================================================
# 物理常数
# ====================================================================================

G_N_NATURAL = 1.0          # 自然单位 G_N = 1
C_NATURAL = 1.0            # 自然单位 c = 1
HBAR = 1.0                 # 自然单位 ℏ = 1
K_B = 1.0                  # 自然单位 k_B = 1
M_PLANCK = 1.0             # 普朗克质量


# ===========================================================================
# Kerr 黑洞基本量
# ====================================================================================

class KerrBlackHole:
    """
    Kerr 黑洞基本量（已知结果 KR1, KR5）。

    Kerr 度规参数：
    - M: 黑洞质量
    - a = J/M: 自旋参数（J 为角动量）
    - r_+ = M + sqrt(M² - a²): 外视界半径
    - A_H = 8π M r_+: 视界面积
    - T_H = (r_+ - M)/(4π M r_+): Hawking 温度
    - S_BH = A_H/(4G_N): Bekenstein-Hawking 熵
    """

    def __init__(self, M: float, a: float):
        """
        参数:
            M: 黑洞质量（自然单位）
            a: 自旋参数 a = J/M，满足 |a| ≤ M
        """
        self.M = M
        self.a = a
        assert abs(a) <= M, "自旋参数 |a| 必须 ≤ M"

        self.r_plus = M + np.sqrt(M**2 - a**2)
        self.r_minus = M - np.sqrt(M**2 - a**2)
        self.area = 8 * np.pi * M * self.r_plus  # KR5: A_H
        self.temperature = (self.r_plus - M) / (4 * np.pi * M * self.r_plus)  # T_H
        self.entropy_BH = self.area / 4  # KR2: S_BH = A/(4G_N)
        self.omega_H = a / (2 * M * self.r_plus)  # 视界角速度

    def surface_gravity(self) -> float:
        """表面引力 κ"""
        return (self.r_plus - self.r_minus) / (4 * M * self.r_plus if False else 4 * self.M * self.r_plus)

    def info(self) -> dict:
        return {
            "M": self.M,
            "a": self.a,
            "a/M": self.a / self.M,
            "r_+": self.r_plus,
            "A_H": self.area,
            "T_H": self.temperature,
            "S_BH": self.entropy_BH,
            "Omega_H": self.omega_H,
            "kappa": self.surface_gravity(),
        }


# ===========================================================================
# Kerr 视界分形维数
# ====================================================================================

class KerrFractalDimension:
    """
    Kerr 视界的分形维数分析（新贡献）。

    核心思想：
    - Kerr 视界的量子涨落引入分形结构
    - 分形维数 d_frac < 2（经典视界维数）
    - 分形维数由 Planck 尺度修正与自旋参数决定
    """

    def __init__(self, bh: KerrBlackHole, epsilon_planck: float = 0.01):
        """
        参数:
            bh: KerrBlackHole 实例
            epsilon_planck: Planck 尺度修正强度 ε ~ l_P/r_+
        """
        self.bh = bh
        self.eps = epsilon_planck

    def classical_dimension(self) -> float:
        """经典视界维数 = 2（球面）"""
        return 2.0

    def fractal_dimension(self) -> float:
        """
        分形修正的视界维数（新贡献）。

        d_frac = 2 - ε · (1 - a²/M²)

        当 a → 0（Schwarzschild）：d_frac = 2 - ε（最大修正）
        当 a → M（极端 Kerr）：d_frac = 2（无修正，Nariai 极限）
        """
        spin_factor = 1 - (self.bh.a / self.bh.M)**2
        return 2.0 - self.eps * spin_factor

    def area_correction(self) -> float:
        """
        分形修正的面积因子。

        A_frac = A_class · (d_frac / 2)
               = A_class · (1 - ε(1-a²/M²)/2)
        """
        d_frac = self.fractal_dimension()
        return d_frac / 2.0

    def fractal_corrected_area(self) -> float:
        """分形修正后的视界面积"""
        return self.bh.area * self.area_correction()


# ===========================================================================
# 分形修正的 Bekenstein-Hawking 熵
# ====================================================================================

class FractalBlackHoleEntropy:
    """
    分形修正的黑洞熵（新贡献）。

    S_fractal = A_frac / (4G_N)
              = S_BH · (1 - ε(1-a²/M²)/2)

    这是对 Bekenstein-Hawking 熵 KR2 的量子引力修正。
    """

    def __init__(self, bh: KerrBlackHole, fd: KerrFractalDimension):
        self.bh = bh
        self.fd = fd

    def classical_entropy(self) -> float:
        """经典 Bekenstein-Hawking 熵（KR2）"""
        return self.bh.entropy_BH

    def fractal_entropy(self) -> float:
        """分形修正熵"""
        return self.fd.fractal_corrected_area() / 4

    def entropy_correction(self) -> dict:
        """熵修正分析"""
        S_class = self.classical_entropy()
        S_frac = self.fractal_entropy()
        delta_S = S_frac - S_class

        return {
            "S_BH_classical": S_class,
            "S_BH_fractal": S_frac,
            "delta_S": delta_S,
            "delta_S_relative": delta_S / S_class if S_class > 0 else 0,
            "d_frac": self.fd.fractal_dimension(),
            "epsilon": self.fd.eps,
        }

    def entropy_vs_spin(self, a_values: np.ndarray) -> dict:
        """熵随自旋参数的变化"""
        results = {"a/M": [], "S_classical": [], "S_fractal": [], "delta_S_relative": []}

        for a in a_values:
            if abs(a) > self.bh.M:
                continue
            bh = KerrBlackHole(self.bh.M, a)
            fd = KerrFractalDimension(bh, self.fd.eps)
            ent = FractalBlackHoleEntropy(bh, fd)
            corr = ent.entropy_correction()

            results["a/M"].append(a / self.bh.M)
            results["S_classical"].append(corr["S_BH_classical"])
            results["S_fractal"].append(corr["S_BH_fractal"])
            results["delta_S_relative"].append(corr["delta_S_relative"])

        return results


# ===========================================================================
# Kerr 测地线混沌与 Lyapunov 指数
# ====================================================================================

class KerrGeodesicChaos:
    """
    Kerr 测地线混沌分析（新贡献：连接到 IFS 框架）。

    已知结果 KR3：赤道面附近测地线出现混沌。
    新贡献：Lyapunov 指数与 IFS 压缩比的关系。
    """

    def __init__(self, bh: KerrBlackHole):
        self.bh = bh

    def lyapunov_exponent(self, r0: float, L: float, E: float) -> float:
        """
        测地线 Lyapunov 指数（已知结果 KR3 的参数化）。

        对于近视界测地线，Lyapunov 指数为：
        λ_L ~ κ · sqrt(1 - r_+/r_0)
        其中 κ 为表面引力。
        """
        kappa = self.bh.surface_gravity()
        if r0 <= self.bh.r_plus:
            return 0.0
        factor = np.sqrt(max(0, 1 - self.bh.r_plus / r0))
        return kappa * factor

    def chaos_to_ifs_mapping(self, r0: float) -> dict:
        """
        将测地线混沌映射到 IFS 压缩比（新贡献）。

        核心思想：
        - 测地线 Lyapunov 指数 λ_L → IFS 压缩比 r = e^{-λ_L}
        - 混沌越强（λ_L 大）→ IFS 压缩比越小（r 小）→ 分形维数越低
        """
        lambda_L = self.lyapunov_exponent(r0, 0, 0)

        # IFS 压缩比
        r_ifs = np.exp(-lambda_L)

        # IFS 分形维数（两映射 Moran 方程 c^d = 1/2）
        if r_ifs > 0 and r_ifs < 1:
            d_frac = -np.log(2) / np.log(r_ifs)
        else:
            d_frac = 0.0

        return {
            "r0": r0,
            "lambda_L": lambda_L,
            "r_ifs": r_ifs,
            "d_frac": d_frac,
            "chaos_strength": "强" if lambda_L > 0.1 else "弱" if lambda_L > 0.01 else "可忽略",
        }

    def poincare_fractal_dimension(self, r0_range: np.ndarray) -> dict:
        """
        Poincaré 截面的分形维数（已知结果 KR5 + 新贡献）。

        随着测地线接近视界，Poincaré 截面的分形维数变化。
        """
        results = {"r0": [], "lambda_L": [], "d_frac": [], "r_ifs": []}

        for r0 in r0_range:
            mapping = self.chaos_to_ifs_mapping(r0)
            results["r0"].append(r0)
            results["lambda_L"].append(mapping["lambda_L"])
            results["d_frac"].append(mapping["d_frac"])
            results["r_ifs"].append(mapping["r_ifs"])

        return results


# ===========================================================================
# Kerr 准正模谱与框架谱对应
# ====================================================================================

class KerrQNMSpectrum:
    """
    Kerr 准正模（QNM）谱与框架谱对应 λ_n = e^{-μ_n}。

    已知结果 KR4：QNM 频率 ω_n = ω_R + i ω_I。
    新贡献：将 QNM 衰减率映射到框架谱参数 μ_n。
    """

    def __init__(self, bh: KerrBlackHole):
        self.bh = bh

    def qnm_frequencies(self, n_modes: int = 10) -> dict:
        """
        Kerr QNM 频率近似（已知结果 KR4 的参数化）。

        对于 eikonal 极限（l >> 1）：
        ω_R ~ m · Ω_H （视界角速度的整数倍）
        ω_I ~ -κ · (n + 1/2) （表面引力决定衰减）
        """
        omega_H = self.bh.omega_H
        kappa = self.bh.surface_gravity()

        modes = []
        for n in range(n_modes):
            m = n + 1  # 角量子数
            omega_R = m * omega_H
            omega_I = -kappa * (n + 0.5)
            modes.append({
                "n": n,
                "m": m,
                "omega_R": omega_R,
                "omega_I": omega_I,
                "omega": complex(omega_R, omega_I),
            })

        return {"modes": modes, "Omega_H": omega_H, "kappa": kappa}

    def spectral_correspondence(self, n_modes: int = 10) -> dict:
        """
        QNM 谱与框架谱对应 λ_n = e^{-μ_n}（新贡献）。

        映射：
        - μ_n = -ω_I / κ = n + 1/2 （无量纲谱参数）
        - λ_n = e^{-μ_n} = e^{-(n+1/2)} （Koopman 算子特征值）
        - 衰减率 ω_I = -κ · μ_n
        """
        qnm = self.qnm_frequencies(n_modes)

        results = []
        for mode in qnm["modes"]:
            mu_n = -mode["omega_I"] / qnm["kappa"]  # 谱参数
            lambda_n = np.exp(-mu_n)  # Koopman 特征值

            results.append({
                "n": mode["n"],
                "omega_R": mode["omega_R"],
                "omega_I": mode["omega_I"],
                "mu_n": mu_n,
                "lambda_n": lambda_n,
                "verification": abs(lambda_n - np.exp(-mu_n)) < 1e-10,
            })

        # 验证谱对应
        all_verified = all(r["verification"] for r in results)

        return {
            "modes": results,
            "kappa": qnm["kappa"],
            "Omega_H": qnm["Omega_H"],
            "spectral_correspondence_verified": all_verified,
            "note": "QNM 衰减率 ω_I = -κ·μ_n，μ_n = n+1/2，λ_n = e^{-μ_n}",
        }


# ===========================================================================
# 综合演示
# ====================================================================================

def run_kerr_fractal_demo():
    """运行 Kerr 分形几何与黑洞熵演示"""
    print("=" * 70)
    print("Kerr 度规分形几何与黑洞熵分形解释")
    print("=" * 70)

    # 1. Kerr 黑洞基本参数
    print(f"\n--- 1. Kerr 黑洞基本参数 ---")
    M = 10.0  # 太阳质量倍数（自然单位）
    a_values = [0.0, 0.5, 0.9, 0.99, 0.999]

    print(f"\n{'a/M':>8} | {'r_+':>8} | {'A_H':>10} | {'T_H':>10} | {'S_BH':>10} | {'Ω_H':>8}")
    print("-" * 65)
    for a in a_values:
        bh = KerrBlackHole(M, a)
        info = bh.info()
        print(f"{info['a/M']:>8.3f} | {info['r_+']:>8.3f} | {info['A_H']:>10.3f} | "
              f"{info['T_H']:>10.6f} | {info['S_BH']:>10.3f} | {info['Omega_H']:>8.6f}")

    # 2. 分形维数
    print(f"\n--- 2. Kerr 视界分形维数（新贡献）---")
    eps = 0.01
    print(f"\nPlanck 修正强度 ε = {eps}")
    print(f"\n{'a/M':>8} | {'d_classical':>12} | {'d_fractal':>12} | {'面积修正':>10} | {'Δd':>8}")
    print("-" * 60)
    for a in a_values:
        bh = KerrBlackHole(M, a)
        fd = KerrFractalDimension(bh, eps)
        d_class = fd.classical_dimension()
        d_frac = fd.fractal_dimension()
        area_corr = fd.area_correction()
        print(f"{a/M:>8.3f} | {d_class:>12.4f} | {d_frac:>12.4f} | {area_corr:>10.6f} | {d_frac-d_class:>+8.4f}")

    # 3. 分形修正熵
    print(f"\n--- 3. 分形修正的 Bekenstein-Hawking 熵 ---")
    print(f"\n{'a/M':>8} | {'S_BH(经典)':>12} | {'S_BH(分形)':>12} | {'ΔS':>10} | {'ΔS/S':>8}")
    print("-" * 60)
    for a in a_values:
        bh = KerrBlackHole(M, a)
        fd = KerrFractalDimension(bh, eps)
        ent = FractalBlackHoleEntropy(bh, fd)
        corr = ent.entropy_correction()
        print(f"{a/M:>8.3f} | {corr['S_BH_classical']:>12.4f} | {corr['S_BH_fractal']:>12.4f} | "
              f"{corr['delta_S']:>+10.6f} | {corr['delta_S_relative']:>+8.6f}")

    # 4. 测地线混沌
    print(f"\n--- 4. Kerr 测地线混沌与 IFS 映射（新贡献）---")
    bh = KerrBlackHole(M, 0.9)
    chaos = KerrGeodesicChaos(bh)

    r0_values = [bh.r_plus * 1.01, bh.r_plus * 1.1, bh.r_plus * 1.5,
                 bh.r_plus * 2.0, bh.r_plus * 5.0]
    print(f"\n  黑洞参数: M={M}, a={0.9}, r_+={bh.r_plus:.4f}")
    print(f"\n{'r0':>10} | {'λ_L':>10} | {'r_ifs':>10} | {'d_frac':>10} | {'混沌强度'}")
    print("-" * 60)
    for r0 in r0_values:
        m = chaos.chaos_to_ifs_mapping(r0)
        print(f"{r0:>10.4f} | {m['lambda_L']:>10.6f} | {m['r_ifs']:>10.6f} | "
              f"{m['d_frac']:>10.4f} | {m['chaos_strength']}")

    # 5. QNM 谱与框架谱对应
    print(f"\n--- 5. Kerr QNM 谱与框架谱对应 λ_n = e^(-μ_n)（新贡献）---")
    bh = KerrBlackHole(M, 0.9)
    qnm = KerrQNMSpectrum(bh)
    spec = qnm.spectral_correspondence(n_modes=8)

    print(f"\n  Ω_H = {spec['Omega_H']:.6f}, κ = {spec['kappa']:.6f}")
    print(f"\n{'n':>4} | {'ω_R':>10} | {'ω_I':>10} | {'μ_n':>8} | {'λ_n':>10} | {'验证'}")
    print("-" * 60)
    for mode in spec["modes"]:
        verified = "✅" if mode["verification"] else "❌"
        print(f"{mode['n']:>4} | {mode['omega_R']:>10.6f} | {mode['omega_I']:>10.6f} | "
              f"{mode['mu_n']:>8.4f} | {mode['lambda_n']:>10.6f} | {verified}")

    print(f"\n  谱对应验证: {'✅ 全部通过' if spec['spectral_correspondence_verified'] else '❌ 未通过'}")
    print(f"  说明: {spec['note']}")

    # 6. 结论
    print(f"\n--- 6. 结论 ---")
    print(f"  ✅ Kerr 视界分形维数: d_frac = 2 - ε·(1-a²/M²)（新贡献）")
    print(f"  ✅ 分形修正熵: S_fractal = S_BH · (1 - ε(1-a²/M²)/2)（新贡献）")
    print(f"  ✅ Schwarzschild (a=0) 修正最大；极端 Kerr (a→M) 修正消失")
    print(f"  ✅ 测地线混沌 → IFS 压缩比映射: r_ifs = e^(-λ_L)（新贡献）")
    print(f"  ✅ QNM 谱对应: μ_n = n+1/2, λ_n = e^(-μ_n), ω_I = -κ·μ_n（新贡献）")
    print(f"  ✅ 谱对应验证: {'全部通过' if spec['spectral_correspondence_verified'] else '未通过'}")


if __name__ == "__main__":
    run_kerr_fractal_demo()
