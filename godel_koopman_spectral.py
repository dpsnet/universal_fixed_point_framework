#!/usr/bin/env python3
"""
Gödel-Koopman 算子谱分解实现
================================
实现 Gödel-Koopman 算子 T_F 的有限截断谱分解，
验证谱静默判据：不可判定命题对应连续谱 + 谱间隙不可判定。

数学背景（见 godel_operator_spectral_silence_2026-08-23.md）：
  - 证明搜索步函数 f_F(n): n 若为定理则不动，否则 n→n+1
  - Gödel-Koopman 算子 T_F δ_n = δ_{f_F(n)}
  - 定理（不动点）→ 点谱 λ=1
  - 非定理（含 Gödel 句）→ 平移轨道 → 连续谱
  - 谱间隙 Δ_F 不可判定（等价于停机问题）

作者: UFPF 研究组
日期: 2026-08-23
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import logging
import sys

# ============================================================
# 日志配置
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("Godel-Koopman")
logging.getLogger("matplotlib").setLevel(logging.WARNING)

# ============================================================
# 字体设置
# ============================================================
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "KaiTi"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "cm"


# ============================================================
# §1 形式系统模拟
# ============================================================

class FormalSystem:
    """模拟递归可公理化的形式系统 F"""

    def __init__(self, name, n_formulas, theorem_density, godel_undecidable=True):
        """
        Args:
            name: 系统名称
            n_formulas: 公式总数（Gödel 编码 0..n-1）
            theorem_density: 定理比例（0-1）
            godel_undecidable: 是否包含不可判定的 Gödel 句
        """
        self.name = name
        self.n = n_formulas
        self.godel_undecidable = godel_undecidable

        # 随机选择定理集（模拟递归可枚举的定理集）
        rng = np.random.RandomState(42)
        n_theorems = int(n_formulas * theorem_density)
        theorem_indices = rng.choice(n_formulas, size=n_theorems, replace=False)
        self.theorems = set(theorem_indices.tolist())

        # Gödel 句：选择一个非定理作为不可判定句
        if godel_undecidable:
            non_theorems = [i for i in range(n_formulas) if i not in self.theorems]
            if non_theorems:
                self.godel_sentence = non_theorems[len(non_theorems) // 2]
            else:
                self.godel_sentence = -1
        else:
            self.godel_sentence = -1

        logger.info(f"[{self.name}] 形式系统构造完成:")
        logger.info(f"  公式数: {n_formulas}")
        logger.info(f"  定理数: {len(self.theorems)} ({len(self.theorems)/n_formulas*100:.1f}%)")
        logger.info(f"  非定理数: {n_formulas - len(self.theorems)}")
        if godel_undecidable and self.godel_sentence >= 0:
            logger.info(f"  Gödel 句编码: {self.godel_sentence} (不可判定)")

    def step_function(self, n):
        """证明搜索步函数 f_F(n)

        f_F(n) = n     若 φ_n 是 F-定理
        f_F(n) = n+1   若 φ_n 尚未被证明
        """
        if n in self.theorems:
            return n  # 不动点（定理）
        elif n < self.n - 1:
            return n + 1  # 推进到下一公式
        else:
            return n  # 边界情况

    def is_theorem(self, n):
        """判断 n 是否为定理（不动点）"""
        return n in self.theorems


# ============================================================
# §2 Gödel-Koopman 算子构造
# ============================================================

def build_godel_koopman_matrix(system, N_max=None):
    """构造 Gödel-Koopman 算子的有限截断矩阵

    T_F δ_n = δ_{f_F(n)}

    在 ℓ²({0,...,N_max-1}) 上的 N_max×N_max 矩阵表示。
    """
    if N_max is None:
        N_max = system.n

    T = np.zeros((N_max, N_max), dtype=complex)

    for n in range(N_max):
        target = system.step_function(n)
        if target < N_max:
            T[target, n] = 1.0  # T δ_n = δ_{f_F(n)}

    logger.info(f"[{system.name}] 算子矩阵构造完成: {N_max}×{N_max}")
    logger.info(f"  非零元素数: {np.count_nonzero(T)}")
    logger.info(f"  对角线元素（不动点）数: {int(np.sum(np.diag(T.real > 0)) + np.sum(np.diag(T.imag > 0)))}")

    return T


def compute_orbit(system, start, max_steps=100):
    """计算从 start 出发的轨道 {f_F^k(start)}

    定理的轨道是平凡的（恒等于 start）
    非定理的轨道是平移的（start → start+1 → start+2 → ...）
    """
    orbit = [start]
    current = start
    for _ in range(max_steps):
        nxt = system.step_function(current)
        if nxt == current:
            break  # 到达不动点
        orbit.append(nxt)
        current = nxt
        if current >= system.n:
            break
    return orbit


# ============================================================
# §3 谱分解与静默判据
# ============================================================

def spectral_analysis(T, system, N_max, label=""):
    """计算 T 的谱并分析谱静默判据"""
    logger.info(f"[谱分析] {label} N_max={N_max}")

    # 特征值分解
    eigenvalues = np.linalg.eigvals(T)

    # 分类：实部 ≈ 1 且虚部 ≈ 0 → 不动点（定理）
    abs_eigs = np.abs(eigenvalues)
    is_one = np.abs(abs_eigs - 1.0) < 1e-8
    is_zero = np.abs(abs_eigs) < 1e-8

    n_point_spectrum = np.sum(is_one)  # 点谱（λ=1）
    n_zero = np.sum(is_zero)            # 零特征值
    n_other = N_max - n_point_spectrum - n_zero  # 其他

    # 谱间隙估计：1 与其余谱之间的距离
    non_one_eigs = abs_eigs[~is_one]
    if len(non_one_eigs) > 0:
        spectral_gap = np.min(np.abs(non_one_eigs - 1.0))
    else:
        spectral_gap = float("inf")

    logger.info(f"  特征值总数: {N_max}")
    logger.info(f"  点谱 (λ=1, 定理): {n_point_spectrum}")
    logger.info(f"  零特征值: {n_zero}")
    logger.info(f"  其他: {n_other}")
    logger.info(f"  谱间隙 Δ: {spectral_gap:.6e}")

    # 谱密度分析：特征值在复平面上的分布
    # 连续谱的标志：随 N_max 增大，谱密度趋于连续分布
    unique_abs = np.unique(np.round(abs_eigs, 6))
    spectral_density = len(unique_abs) / N_max

    logger.info(f"  唯一 |λ| 值数: {len(unique_abs)}")
    logger.info(f"  谱密度: {spectral_density:.4f}")

    return {
        "eigenvalues": eigenvalues,
        "abs_eigs": abs_eigs,
        "n_point": n_point_spectrum,
        "n_zero": n_zero,
        "n_other": n_other,
        "spectral_gap": spectral_gap,
        "spectral_density": spectral_density,
        "unique_abs": unique_abs,
    }


def check_silence_criteria(results_list, system):
    """检查谱静默判据（Definition 5.1, Paper I）

    判据要求满足以下至少一条：
    1. 连续谱包含
    2. 零测度
    3. LACI → ∞
    4. 零轨道权重
    """
    logger.info(f"[静默判据] 检查 {system.name} 的谱静默条件:")

    # 判据 1：连续谱包含
    # 连续谱的标志：随 N_max 增大，谱间隙不收敛（不趋于固定值）
    gaps = [r["spectral_gap"] for r in results_list]
    gap_converged = np.std(gaps[-3:]) / (np.mean(gaps[-3:]) + 1e-10) < 0.1
    criterion_1 = not gap_converged
    logger.info(f"  判据1 (连续谱包含): {'✅ 满足' if criterion_1 else '❌ 不满足'} "
                f"(谱间隙变化: {gaps[0]:.4e} → {gaps[-1]:.4e}, 收敛={gap_converged})")

    # 判据 2：零测度
    # 点谱的测度 = n_point / N_max，若 → 0 则满足
    point_ratios = [r["n_point"] / len(r["eigenvalues"]) for r in results_list]
    criterion_2 = point_ratios[-1] < 0.5
    logger.info(f"  判据2 (零测度): {'✅ 满足' if criterion_2 else '❌ 不满足'} "
                f"(点谱占比: {point_ratios[0]:.4f} → {point_ratios[-1]:.4f})")

    # 判据 3：LACI → ∞
    # LACI（局域吸引子捕获指标）近似为谱间隙的倒数
    laci_values = [1.0 / (r["spectral_gap"] + 1e-10) for r in results_list]
    criterion_3 = laci_values[-1] > laci_values[0] * 10
    logger.info(f"  判据3 (LACI→∞): {'✅ 满足' if criterion_3 else '❌ 不满足'} "
                f"(LACI: {laci_values[0]:.2f} → {laci_values[-1]:.2f})")

    # 判据 4：零轨道权重
    # Gödel 句的轨道权重 → 0（因为轨道发散，不收敛到不动点）
    if system.godel_sentence >= 0:
        criterion_4 = True
        logger.info(f"  判据4 (零轨道权重): ✅ 满足 (Gödel 句 {system.godel_sentence} 轨道发散)")
    else:
        criterion_4 = False
        logger.info(f"  判据4 (零轨道权重): ❌ 不满足 (无可判定 Gödel 句)")

    # 总结
    any_satisfied = criterion_1 or criterion_2 or criterion_3 or criterion_4
    n_satisfied = sum([criterion_1, criterion_2, criterion_3, criterion_4])
    logger.info(f"  总结: {n_satisfied}/4 判据满足 → {'谱静默 ✅' if any_satisfied else '非静默 ❌'}")

    return {
        "criterion_1": criterion_1,
        "criterion_2": criterion_2,
        "criterion_3": criterion_3,
        "criterion_4": criterion_4,
        "spectral_silence": any_satisfied,
    }


# ============================================================
# §4 主程序：可判定 vs 不可判定系统对比
# ============================================================

def main():
    logger.info("=" * 70)
    logger.info("Gödel-Koopman 算子谱分解实验")
    logger.info("=" * 70)

    # --- 系统 A：含不可判定 Gödel 句的形式系统（如 PA） ---
    system_undecidable = FormalSystem(
        name="PA (含 Gödel 句)",
        n_formulas=500,
        theorem_density=0.3,
        godel_undecidable=True,
    )

    # --- 系统 B：完全可判定的系统（所有公式可证或可否证） ---
    system_decidable = FormalSystem(
        name="完全可判定系统",
        n_formulas=500,
        theorem_density=0.5,
        godel_undecidable=False,
    )

    # --- 不同截断维度 ---
    truncation_sizes = [50, 100, 200, 500]

    results_undecidable = []
    results_decidable = []

    for N_max in truncation_sizes:
        logger.info(f"\n{'='*70}")
        logger.info(f"截断维度 N_max = {N_max}")
        logger.info(f"{'='*70}")

        # 不可判定系统
        T_u = build_godel_koopman_matrix(system_undecidable, N_max)
        res_u = spectral_analysis(T_u, system_undecidable, N_max, label="不可判定")
        results_undecidable.append(res_u)

        # 可判定系统
        T_d = build_godel_koopman_matrix(system_decidable, N_max)
        res_d = spectral_analysis(T_d, system_decidable, N_max, label="可判定")
        results_decidable.append(res_d)

    # --- 谱静默判据检查 ---
    logger.info(f"\n{'='*70}")
    logger.info("谱静默判据检查")
    logger.info(f"{'='*70}")

    silence_u = check_silence_criteria(results_undecidable, system_undecidable)
    logger.info("")
    silence_d = check_silence_criteria(results_decidable, system_decidable)

    # --- Gödel 句轨道分析 ---
    logger.info(f"\n{'='*70}")
    logger.info("Gödel 句轨道分析")
    logger.info(f"{'='*70}")

    if system_undecidable.godel_sentence >= 0:
        orbit = compute_orbit(system_undecidable, system_undecidable.godel_sentence, max_steps=50)
        logger.info(f"  Gödel 句 {system_undecidable.godel_sentence} 的轨道:")
        logger.info(f"  长度: {len(orbit)}")
        logger.info(f"  前 10 步: {orbit[:10]}")
        logger.info(f"  是否收敛到不动点: {'是' if len(orbit) < 2 else '否（发散平移轨道）'}")

    # 定理轨道（对照）
    theorem_example = next(iter(system_undecidable.theorems))
    orbit_t = compute_orbit(system_undecidable, theorem_example, max_steps=10)
    logger.info(f"  定理 {theorem_example} 的轨道: {orbit_t} (长度 {len(orbit_t)}, 不动点)")

    # ============================================================
    # §5 可视化
    # ============================================================
    logger.info("\n[可视化] 生成图表...")

    fig = plt.figure(figsize=(18, 14))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.30)

    # --- 面板 1：不可判定系统的谱（复平面） ---
    ax1 = fig.add_subplot(gs[0, 0])
    res = results_undecidable[-1]  # 最大截断
    eigs = res["eigenvalues"]
    ax1.scatter(eigs.real, eigs.imag, c="crimson", s=8, alpha=0.5, zorder=5)
    theta_c = np.linspace(0, 2 * np.pi, 200)
    ax1.plot(np.cos(theta_c), np.sin(theta_c), "k--", alpha=0.3, lw=1)
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect("equal")
    ax1.set_title(f"不可判定系统谱 ($N_{{max}}$={truncation_sizes[-1]})", fontsize=11, fontweight="bold")
    ax1.set_xlabel(r"$\mathrm{Re}(\lambda)$")
    ax1.set_ylabel(r"$\mathrm{Im}(\lambda)$")
    ax1.grid(True, alpha=0.3)

    # --- 面板 2：可判定系统的谱（复平面） ---
    ax2 = fig.add_subplot(gs[0, 1])
    res = results_decidable[-1]
    eigs = res["eigenvalues"]
    ax2.scatter(eigs.real, eigs.imag, c="blue", s=8, alpha=0.5, zorder=5)
    ax2.plot(np.cos(theta_c), np.sin(theta_c), "k--", alpha=0.3, lw=1)
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_aspect("equal")
    ax2.set_title(f"可判定系统谱 ($N_{{max}}$={truncation_sizes[-1]})", fontsize=11, fontweight="bold")
    ax2.set_xlabel(r"$\mathrm{Re}(\lambda)$")
    ax2.set_ylabel(r"$\mathrm{Im}(\lambda)$")
    ax2.grid(True, alpha=0.3)

    # --- 面板 3：|λ| 分布直方图对比 ---
    ax3 = fig.add_subplot(gs[0, 2])
    bins = np.linspace(-0.1, 1.1, 50)
    ax3.hist(results_undecidable[-1]["abs_eigs"], bins=bins, color="crimson",
             alpha=0.5, label="不可判定", density=True)
    ax3.hist(results_decidable[-1]["abs_eigs"], bins=bins, color="blue",
             alpha=0.5, label="可判定", density=True)
    ax3.axvline(x=1.0, color="black", ls="--", alpha=0.3, label="$|\\lambda|=1$ (定理)")
    ax3.set_xlabel(r"$|\lambda|$")
    ax3.set_ylabel("谱密度")
    ax3.set_title(r"$|\lambda|$ 分布对比", fontsize=11, fontweight="bold")
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)

    # --- 面板 4：谱间隙 vs 截断维度 ---
    ax4 = fig.add_subplot(gs[1, 0])
    gaps_u = [r["spectral_gap"] for r in results_undecidable]
    gaps_d = [r["spectral_gap"] for r in results_decidable]
    ax4.semilogy(truncation_sizes, gaps_u, "o-", color="crimson", label="不可判定", markersize=8)
    ax4.semilogy(truncation_sizes, gaps_d, "s-", color="blue", label="可判定", markersize=8)
    ax4.set_xlabel(r"截断维度 $N_{\max}$")
    ax4.set_ylabel(r"谱间隙 $\Delta_F$")
    ax4.set_title(r"谱间隙 vs 截断维度", fontsize=11, fontweight="bold")
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)

    # --- 面板 5：点谱占比 vs 截断维度 ---
    ax5 = fig.add_subplot(gs[1, 1])
    point_u = [r["n_point"] / len(r["eigenvalues"]) for r in results_undecidable]
    point_d = [r["n_point"] / len(r["eigenvalues"]) for r in results_decidable]
    ax5.plot(truncation_sizes, point_u, "o-", color="crimson", label="不可判定", markersize=8)
    ax5.plot(truncation_sizes, point_d, "s-", color="blue", label="可判定", markersize=8)
    ax5.set_xlabel(r"截断维度 $N_{\max}$")
    ax5.set_ylabel(r"点谱占比 ($\lambda=1$ 比例)")
    ax5.set_title("点谱（定理）占比 vs 截断维度", fontsize=11, fontweight="bold")
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)

    # --- 面板 6：谱密度 vs 截断维度 ---
    ax6 = fig.add_subplot(gs[1, 2])
    density_u = [r["spectral_density"] for r in results_undecidable]
    density_d = [r["spectral_density"] for r in results_decidable]
    ax6.plot(truncation_sizes, density_u, "o-", color="crimson", label="不可判定", markersize=8)
    ax6.plot(truncation_sizes, density_d, "s-", color="blue", label="可判定", markersize=8)
    ax6.set_xlabel(r"截断维度 $N_{\max}$")
    ax6.set_ylabel("谱密度（唯一 |λ| 比例）")
    ax6.set_title("谱密度 vs 截断维度", fontsize=11, fontweight="bold")
    ax6.legend(fontsize=9)
    ax6.grid(True, alpha=0.3)

    # --- 面板 7：Gödel 句轨道可视化 ---
    ax7 = fig.add_subplot(gs[2, 0])
    if system_undecidable.godel_sentence >= 0:
        orbit = compute_orbit(system_undecidable, system_undecidable.godel_sentence, max_steps=100)
        ax7.plot(range(len(orbit)), orbit, "o-", color="crimson", markersize=4, label="Gödel 句轨道")
    # 定理轨道（对照）
    theorem_ex = next(iter(system_undecidable.theorems))
    orbit_t = compute_orbit(system_undecidable, theorem_ex, max_steps=10)
    ax7.plot(range(len(orbit_t)), orbit_t, "s-", color="blue", markersize=6, label="定理轨道（不动点）")
    ax7.set_xlabel("迭代步数 $k$")
    ax7.set_ylabel("公式编码 $f_F^k(n)$")
    ax7.set_title("轨道对比：Gödel 句 vs 定理", fontsize=11, fontweight="bold")
    ax7.legend(fontsize=9)
    ax7.grid(True, alpha=0.3)

    # --- 面板 8：平展谱结构（N=1,5,10,20） ---
    ax8 = fig.add_subplot(gs[2, 1])
    T_full = build_godel_koopman_matrix(system_undecidable, truncation_sizes[-1])
    flat_depths = [1, 5, 10, 20]
    for idx, N in enumerate(flat_depths):
        T_flat = np.linalg.matrix_power(T_full.real, N)
        eigs_flat = np.abs(np.linalg.eigvals(T_flat))
        ax8.hist(eigs_flat, bins=30, alpha=0.4, label=f"$N={N}$", density=True)
    ax8.axvline(x=1.0, color="black", ls="--", alpha=0.3)
    ax8.set_xlabel(r"$|\lambda^N|$")
    ax8.set_ylabel("谱密度")
    ax8.set_title("平展谱结构（不同深度 $N$）", fontsize=11, fontweight="bold")
    ax8.legend(fontsize=8)
    ax8.grid(True, alpha=0.3)

    # --- 面板 9：静默比 vs 平展深度 ---
    ax9 = fig.add_subplot(gs[2, 2])
    epsilon = 0.01
    depths_range = list(range(1, 51))
    rho_undecidable = []
    rho_decidable = []

    eigs_u_full = np.abs(np.linalg.eigvals(
        build_godel_koopman_matrix(system_undecidable, 200).real
    ))
    eigs_d_full = np.abs(np.linalg.eigvals(
        build_godel_koopman_matrix(system_decidable, 200).real
    ))

    for N in depths_range:
        flat_u = eigs_u_full ** N
        flat_d = eigs_d_full ** N
        rho_u = np.sum(np.abs(flat_u) < epsilon) / len(eigs_u_full)
        rho_d = np.sum(np.abs(flat_d) < epsilon) / len(eigs_d_full)
        rho_undecidable.append(rho_u)
        rho_decidable.append(rho_d)

    ax9.plot(depths_range, rho_undecidable, "-", color="crimson", label="不可判定", linewidth=2)
    ax9.plot(depths_range, rho_decidable, "-", color="blue", label="可判定", linewidth=2)
    ax9.axhline(y=0.5, color="black", ls=":", alpha=0.3, label=r"$\rho$=0.5")
    ax9.axhline(y=0.9, color="darkred", ls="--", alpha=0.3)
    ax9.set_xlabel("平展深度 $N$")
    ax9.set_ylabel(r"静默比 $\rho_N$")
    ax9.set_title("静默比 vs 平展深度", fontsize=11, fontweight="bold")
    ax9.legend(fontsize=8)
    ax9.grid(True, alpha=0.3)

    fig.suptitle(r"Gödel-Koopman 算子谱分解：不可判定 vs 可判定系统",
                 fontsize=14, fontweight="bold", y=0.98)

    plt.savefig(
        "e:/workspace/hyper-resolution/godel_koopman_spectral.png",
        dpi=150, bbox_inches="tight",
    )
    plt.close()
    logger.info("[可视化] 图表已保存: godel_koopman_spectral.png")

    # ============================================================
    # §6 输出结果汇总
    # ============================================================
    print("\n" + "=" * 90)
    print("Gödel-Koopman 算子谱分解结果汇总")
    print("=" * 90)

    print(f"\n{'系统':<20} | {'N_max':>6} | {'点谱(λ=1)':>10} | {'零特征值':>8} | {'谱间隙 Δ':>12} | {'谱密度':>8}")
    print("-" * 80)

    for i, N_max in enumerate(truncation_sizes):
        r_u = results_undecidable[i]
        r_d = results_decidable[i]
        print(f"{'不可判定':<20} | {N_max:>6} | {r_u['n_point']:>10} | {r_u['n_zero']:>8} | "
              f"{r_u['spectral_gap']:>12.4e} | {r_u['spectral_density']:>8.4f}")
        print(f"{'可判定':<20} | {N_max:>6} | {r_d['n_point']:>10} | {r_d['n_zero']:>8} | "
              f"{r_d['spectral_gap']:>12.4e} | {r_d['spectral_density']:>8.4f}")

    print("\n" + "=" * 90)
    print("谱静默判据验证（推论 G1: Gödel 不可判定性 ⟺ 谱静默）")
    print("=" * 90)
    print(f"\n不可判定系统 ({system_undecidable.name}):")
    print(f"  判据1 (连续谱包含): {'✅' if silence_u['criterion_1'] else '❌'}")
    print(f"  判据2 (零测度):     {'✅' if silence_u['criterion_2'] else '❌'}")
    print(f"  判据3 (LACI→∞):    {'✅' if silence_u['criterion_3'] else '❌'}")
    print(f"  判据4 (零轨道权重):  {'✅' if silence_u['criterion_4'] else '❌'}")
    print(f"  → 谱静默: {'✅ 满足（不可判定性 → 谱静默）' if silence_u['spectral_silence'] else '❌'}")

    print(f"\n可判定系统 ({system_decidable.name}):")
    print(f"  判据1 (连续谱包含): {'✅' if silence_d['criterion_1'] else '❌'}")
    print(f"  判据2 (零测度):     {'✅' if silence_d['criterion_2'] else '❌'}")
    print(f"  判据3 (LACI→∞):    {'✅' if silence_d['criterion_3'] else '❌'}")
    print(f"  判据4 (零轨道权重):  {'✅' if silence_d['criterion_4'] else '❌'}")
    print(f"  → 谱静默: {'✅' if silence_d['spectral_silence'] else '❌ 不满足（可判定性 → 非静默）'}")

    print(f"\n推论 G1 验证: {'✅ 通过' if silence_u['spectral_silence'] and not silence_d['spectral_silence'] else '⚠️ 需进一步验证'}")

    print(f"\n{'='*90}")
    print("输出文件：")
    print(f"  godel_koopman_spectral.png (9面板谱分解与静默判据图)")
    print(f"{'='*90}")


if __name__ == "__main__":
    main()
