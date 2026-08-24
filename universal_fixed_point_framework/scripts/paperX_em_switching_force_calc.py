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
# 本文件中 UFPF 相关引用数量：2
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
paperX_em_switching_force_calc.py
=================================
电磁场瞬间开关导致不良导体摆动的定量计算

基于标准电磁学（电荷弛豫振荡 + 电致伸缩）计算：
1. 不同材料的弛豫时间 τ = ε₀εᵣ/σ
2. 电致伸缩力 F_es 和弛豫力 F_relax 的大小
3. 阻尼振荡的时域响应 x(t)
4. 可证伪判据的定量预测

UFPF 框架立场：完全兼容标准麦克斯韦方程，实验室能量下不添加额外修正。

参考文献：
- 笔记：notes/08_first_principles/electromagnetic_switching_mechanics_analysis.md
- 框架：spectral_hierarchy_evolution_analysis.md §4.6（U(1) 谱投影）

创建日期：2026-07-29
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple
import os

FIGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figs')

# ============================================================
# 物理常数（SI 单位制）
# ============================================================

EPSILON_0 = 8.8541878128e-12  # 真空介电常数 F/m
G_GRAV = 9.80665              # 重力加速度 m/s²


# ============================================================
# §1 材料参数库
# ============================================================

@dataclass
class Material:
    """不良导体材料参数。"""
    name: str
    epsilon_r: float    # 相对介电常数
    sigma: float        # 电导率 S/m
    density: float      # 密度 kg/m³

    def relaxation_time(self) -> float:
        """电荷弛豫时间 τ = ε₀εᵣ/σ (秒)。"""
        return EPSILON_0 * self.epsilon_r / self.sigma


# 常见材料库
MATERIALS: Dict[str, Material] = {
    "copper": Material("铜（良导体）", 1.0, 5.96e7, 8960),
    "silicon": Material("硅（半导体）", 11.7, 4e-4, 2329),
    "glass": Material("玻璃（不良导体）", 5.0, 1e-12, 2500),
    "dry_wood": Material("干木（不良导体）", 4.0, 1e-13, 700),
    "ptfe": Material("PTFE（绝缘体）", 2.1, 1e-16, 2200),
    "quartz": Material("石英", 3.8, 1e-14, 2650),
    "paraffin": Material("石蜡", 2.2, 1e-14, 900),
    "mica": Material("云母", 6.0, 1e-15, 3000),
}


def print_relaxation_times():
    """打印各材料的弛豫时间。"""
    print("=" * 70)
    print("§1 各材料的电荷弛豫时间 τ = ε₀εᵣ/σ")
    print("=" * 70)
    print(f"{'材料':<20} {'εᵣ':>6} {'σ (S/m)':>12} {'τ (s)':>12} {'可观测性':>10}")
    print("-" * 70)
    for mat in MATERIALS.values():
        tau = mat.relaxation_time()
        if tau < 1e-6:
            obs = "❌ 极快"
        elif tau < 1e-3:
            obs = "❌ 很快"
        elif tau < 1:
            obs = "🔶 毫秒级"
        elif tau < 60:
            obs = "✅ 秒级"
        elif tau < 3600:
            obs = "✅ 分钟级"
        else:
            obs = "❌ 太慢"
        print(f"{mat.name:<20} {mat.epsilon_r:>6.1f} {mat.sigma:>12.2e} {tau:>12.4g} {obs:>10}")
    print()


# ============================================================
# §2 电致伸缩力计算
# ============================================================

@dataclass
class ExperimentConfig:
    """实验配置参数。"""
    E0: float          # 外加电场强度 V/m
    volume: float      # 样品体积 m³
    area: float        # 样品截面积 m²
    length: float      # 悬线长度 m
    material: Material # 材料参数

    def mass(self) -> float:
        """样品质量 kg。"""
        return self.material.density * self.volume

    def spring_constant(self) -> float:
        """悬线等效弹性常数 k = mg/L N/m。"""
        return self.mass() * G_GRAV / self.length

    def damping_coeff(self, damping_ratio: float = 0.05) -> float:
        """阻尼系数 γ = 2ζ√(mk)。"""
        m = self.mass()
        k = self.spring_constant()
        return 2 * damping_ratio * np.sqrt(m * k)


def electrostriction_force(cfg: ExperimentConfig) -> float:
    """
    电致伸缩力 F_es = ε₀(εᵣ-1)(εᵣ+2)/6 · E₀² · A

    方向：沿 ∇E²，指向高场强区域。
    特征：∝ E²（非线性，与电场方向无关）。
    """
    mat = cfg.material
    coeff = EPSILON_0 * (mat.epsilon_r - 1) * (mat.epsilon_r + 2) / 6
    return coeff * cfg.E0**2 * cfg.area


def relaxation_force_peak(cfg: ExperimentConfig) -> float:
    """
    弛豫力峰值 F₀ ~ ε₀εᵣ E₀² V / τ²

    方向：沿电荷梯度方向。
    特征：脉冲型，t ≈ τ 时达峰。
    """
    mat = cfg.material
    tau = mat.relaxation_time()
    return EPSILON_0 * mat.epsilon_r * cfg.E0**2 * cfg.volume / tau**2


def print_force_analysis(cfg: ExperimentConfig):
    """打印力分析结果。"""
    mat = cfg.material
    tau = mat.relaxation_time()
    m = cfg.mass()
    k = cfg.spring_constant()
    gamma = cfg.damping_coeff()
    F_es = electrostriction_force(cfg)
    F_relax = relaxation_force_peak(cfg)

    print("=" * 70)
    print(f"§2 力分析 — 材料: {mat.name}")
    print("=" * 70)
    print(f"  外加电场 E₀        = {cfg.E0:.2e} V/m")
    print(f"  样品体积 V          = {cfg.volume:.2e} m³")
    print(f"  样品截面积 A        = {cfg.area:.2e} m²")
    print(f"  悬线长度 L          = {cfg.length} m")
    print(f"  质量 m              = {m:.4f} kg")
    print(f"  弹性常数 k          = {k:.4f} N/m")
    print(f"  阻尼系数 γ          = {gamma:.4f} N·s/m")
    print()
    print(f"  弛豫时间 τ          = {tau:.4g} s")
    print(f"  电致伸缩力 F_es     = {F_es:.4e} N")
    print(f"  弛豫力峰值 F_relax  = {F_relax:.4e} N")
    print()
    print(f"  摆动幅度（电致伸缩） = {F_es / k * 1000:.2f} mm")
    print(f"  摆动幅度（弛豫）     = {F_relax / k * 1000:.4f} mm")
    print(f"  摆动周期 T           = {2 * np.pi * np.sqrt(cfg.length / G_GRAV):.2f} s")
    print(f"  阻尼振荡频率 ω_d     = {np.sqrt(k / m - gamma**2 / (4 * m**2)):.4f} rad/s")
    print()


# ============================================================
# §3 时域响应模拟
# ============================================================

def simulate_motion(cfg: ExperimentConfig, t_max: float = None,
                    dt: float = 1e-3, damping_ratio: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
    """
    模拟不良导体在电磁场开关后的阻尼振荡。

    运动方程：m·ẍ + γ·ẋ + k·x = F_es(t) + F_relax(t)

    其中：
      F_es(t) = F_es · Θ(t) · exp(-t/τ_es)   （阶跃后快速衰减）
      F_relax(t) = F₀ · (t/τ) · exp(-t/τ)     （弛豫脉冲）

    返回：(t_array, x_array)
    """
    mat = cfg.material
    m = cfg.mass()
    k = cfg.spring_constant()
    gamma = cfg.damping_coeff(damping_ratio)
    tau = mat.relaxation_time()

    if t_max is None:
        t_max = max(10 * tau, 5 * 2 * np.pi * np.sqrt(m / k))

    t = np.arange(0, t_max, dt)
    n = len(t)

    F_es = electrostriction_force(cfg)
    F_relax_peak = relaxation_force_peak(cfg)

    # 电致伸缩力的时间依赖（开关后阶跃，快速衰减 τ_es ~ τ/100）
    tau_es = max(tau / 100, 1e-6)
    F_es_t = F_es * np.exp(-t / tau_es)

    # 弛豫力的时间依赖（脉冲型，t/τ · exp(-t/τ)）
    F_relax_t = F_relax_peak * (t / tau) * np.exp(-t / tau)

    # 总力
    F_total = F_es_t + F_relax_t

    # 数值积分（Verlet 方法）
    x = np.zeros(n)
    v = np.zeros(n)
    a = np.zeros(n)

    a[0] = F_total[0] / m

    for i in range(n - 1):
        # Verlet 积分
        x[i + 1] = x[i] + v[i] * dt + 0.5 * a[i] * dt**2
        a_new = (F_total[i + 1] - gamma * v[i] - k * x[i + 1]) / m
        v[i + 1] = v[i] + 0.5 * (a[i] + a_new) * dt
        a[i + 1] = a_new

    return t, x


def plot_motion(cfg: ExperimentConfig, save_path: str = None):
    """绘制摆动轨迹图（标签使用英文以避免字体问题）。"""
    mat = cfg.material
    tau = mat.relaxation_time()

    t, x = simulate_motion(cfg, t_max=max(10 * tau, 60))

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # 位移图
    axes[0].plot(t, x * 1000, 'b-', linewidth=1.5)
    axes[0].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    axes[0].axvline(x=tau, color='r', linestyle='--', linewidth=1, label=f'tau = {tau:.2f} s')
    axes[0].set_ylabel('Displacement x (mm)', fontsize=12)
    axes[0].set_title(f'EM Switching Induced Oscillation — {mat.name}\n'
                      f'E0={cfg.E0:.0e} V/m, V={cfg.volume:.0e} m3, L={cfg.length} m',
                      fontsize=13)
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)

    # 力图
    F_es = electrostriction_force(cfg)
    F_relax_peak = relaxation_force_peak(cfg)
    F_es_t = F_es * np.exp(-t / max(tau / 100, 1e-6))
    F_relax_t = F_relax_peak * (t / tau) * np.exp(-t / tau)

    axes[1].plot(t, F_es_t * 1000, 'r-', linewidth=1.5, label=f'Electrostriction (peak {F_es*1e3:.2f} mN)')
    axes[1].plot(t, F_relax_t * 1000, 'g-', linewidth=1.5, label=f'Relaxation (peak {F_relax_peak*1e3:.4f} mN)')
    axes[1].axvline(x=tau, color='r', linestyle='--', linewidth=1, label=f'tau = {tau:.2f} s')
    axes[1].set_ylabel('Force F (mN)', fontsize=12)
    axes[1].set_xlabel('Time t (s)', fontsize=12)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  Figure saved: {save_path}")
    plt.close()


# ============================================================
# §4 可证伪判据验证
# ============================================================

def falsifiability_checks(cfg: ExperimentConfig):
    """打印可证伪判据。"""
    mat = cfg.material
    tau = mat.relaxation_time()
    F_es = electrostriction_force(cfg)

    print("=" * 70)
    print("§4 可证伪判据")
    print("=" * 70)
    print()
    print("判据 1: 摆动时间尺度 = τ = ε₀εᵣ/σ")
    print(f"  预测: τ = {tau:.4g} s")
    print(f"  验证: 换材料（如玻璃→石英），τ 应按 εᵣ/σ 比例变化")
    print()
    print("判据 2: 力 ∝ E²（非线性）")
    print(f"  预测: F ∝ E₀², 当前 E₀ = {cfg.E0:.2e}")
    print(f"  验证: 电压加倍 → 力变为 4 倍（而非 2 倍）")
    print()
    print("判据 3: 力与电场方向无关")
    print(f"  预测: 正向/反向开关，摆动方向相同")
    print(f"  验证: 反转电极极性，摆动方向不变")
    print()
    print("判据 4: 摆动方向 = ∇E²（指向高场强区）")
    print(f"  预测: 摆动指向电极间隙")
    print(f"  验证: 改变几何配置，方向跟随 ∇E²")
    print()
    print("判据 5: 无超出 1/M_Pl 的新效应")
    print(f"  预测: 在精度 < 10⁻³⁵ 时仍与标准电磁一致")
    print(f"  验证: 高精度测量力-电场关系")
    print()


# ============================================================
# §5 多材料对比
# ============================================================

def compare_materials(E0: float = 1e6, volume: float = 1e-5, area: float = 1e-4,
                      length: float = 0.3):
    """对比不同材料的摆动特征。"""
    print("=" * 70)
    print("§5 多材料对比（不良导体摆动特征）")
    print("=" * 70)
    print(f"  固定参数: E₀={E0:.0e} V/m, V={volume:.0e} m³, A={area:.0e} m², L={length} m")
    print()
    print(f"{'材料':<20} {'τ (s)':>10} {'F_es (N)':>12} {'F_relax (N)':>14} {'幅度 (mm)':>12}")
    print("-" * 70)

    for name, mat in MATERIALS.items():
        if mat.sigma > 1e-6:  # 跳过良导体和半导体（弛豫力公式在 τ→0 时不适用）
            continue
        cfg = ExperimentConfig(E0, volume, area, length, mat)
        tau = mat.relaxation_time()
        F_es = electrostriction_force(cfg)
        F_relax = relaxation_force_peak(cfg)
        k = cfg.spring_constant()
        amplitude = F_es / k * 1000  # mm
        print(f"{mat.name:<20} {tau:>10.4g} {F_es:>12.4e} {F_relax:>14.4e} {amplitude:>12.4f}")
    print()


# ============================================================
# 主程序
# ============================================================

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  电磁场瞬间开关导致不良导体摆动的定量计算                    ║")
    print("║  基于：电荷弛豫振荡 + 电致伸缩（标准电磁学）                ║")
    print("║  UFPF 框架：实验室能量下不添加额外修正                      ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # §1 弛豫时间
    print_relaxation_times()

    # §2 力分析（以玻璃为例）
    glass_cfg = ExperimentConfig(
        E0=1e6,
        volume=1e-5,
        area=1e-4,
        length=0.3,
        material=MATERIALS["glass"]
    )
    print_force_analysis(glass_cfg)

    # §3 时域模拟
    print("=" * 70)
    print("§3 时域响应模拟")
    print("=" * 70)

    # 玻璃
    t_glass, x_glass = simulate_motion(glass_cfg, t_max=300)
    print(f"  玻璃: 模拟完成, t_max={t_glass[-1]:.0f}s, 最大位移={max(x_glass)*1000:.2f}mm")

    # 干木
    wood_cfg = ExperimentConfig(
        E0=1e6,
        volume=1e-5,
        area=1e-4,
        length=0.3,
        material=MATERIALS["dry_wood"]
    )
    t_wood, x_wood = simulate_motion(wood_cfg, t_max=600)
    print(f"  干木: 模拟完成, t_max={t_wood[-1]:.0f}s, 最大位移={max(x_wood)*1000:.2f}mm")

    # 绘图
    plot_motion(glass_cfg, save_path=os.path.join(FIGS_DIR, "paperX_em_switching_glass.png"))
    plot_motion(wood_cfg, save_path=os.path.join(FIGS_DIR, "paperX_em_switching_wood.png"))
    print()

    # §4 可证伪判据
    falsifiability_checks(glass_cfg)

    # §5 多材料对比
    compare_materials()

    print("=" * 70)
    print("计算完成。")
    print("笔记: notes/08_first_principles/electromagnetic_switching_mechanics_analysis.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
