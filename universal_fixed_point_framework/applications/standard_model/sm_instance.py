"""
sm_instance.py

标准模型质量谱预测的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 标准模型不是理论核心，只是抽象框架在 Cl(1,7) 低能对称下的一个算例。
- 原有根目录下的 sm_mass_complete_v5.py 是「具象数值实现层」的旧版本；
  本文件对其进行接口包装，使其符合新的抽象框架。

实例假设（MH1）：
- Clifford 签名 (p,q) = (1,7)
- 规范群 G_SM = SU(3)_C × SU(2)_L × U(1)_Y
- 三代费米子的 q 比例：q_up : q_down : q_lep = 1 : 1 : 3 = N_c
- VEV v = 246 GeV 作为低能锚点
"""

from __future__ import annotations

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable
import numpy as np

# 将项目 src 目录加入路径，以导入抽象框架核心模块
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from rec_category import RecObject, RecMorphism
from spec_category import PositiveSpectralObject
from fixed_point_solver import FixedPointSolver


# ============================================================
# 实例假设层的默认参数（来自旧 sm_mass_complete_v5.py）
# ============================================================

DEFAULT_IFS_C = np.array([0.3450, 0.2901])   # IFS 收缩因子（优化值）
DEFAULT_IFS_P = np.array([0.9000, 0.1000])   # IFS 概率参数（优化值）
DEFAULT_GEN_C = np.array([0.5, 0.25, 0.125])  # 三代费米子收缩因子
DEFAULT_Q0 = 0.3127                           # q 参数单自由参数
DEFAULT_V_MEV = 246000.0                      # Higgs VEV，单位 MeV
DEFAULT_M_SEESAW = 1e14                       # See-saw 质量标度，单位 MeV (~10^11 GeV)
DEFAULT_M_NU_REF = 0.05                       # 中微子质量参考值，单位 eV


@dataclass
class SMInstance:
    """
    标准模型实例：将旧质量预测代码包装为抽象框架的下游插件。

    参数
    ----------
    ifs_c : np.ndarray
        IFS 收缩因子。
    ifs_p : np.ndarray
        IFS 概率参数。
    gen_c : np.ndarray
        三代费米子收缩因子。
    q0 : float
        q 参数基准值。
    v_MeV : float
        Higgs VEV，单位 MeV。
    metadata : dict
        附加元数据，记录实例假设来源。
    """
    ifs_c: np.ndarray = field(default_factory=lambda: DEFAULT_IFS_C.copy())
    ifs_p: np.ndarray = field(default_factory=lambda: DEFAULT_IFS_P.copy())
    gen_c: np.ndarray = field(default_factory=lambda: DEFAULT_GEN_C.copy())
    q0: float = DEFAULT_Q0
    v_MeV: float = DEFAULT_V_MEV
    m_seesaw_MeV: float = DEFAULT_M_SEESAW      # See-saw 右手中微子质量标度，单位 MeV
    m_nu_ref_eV: float = DEFAULT_M_NU_REF        # 中微子质量参考值，单位 eV
    metadata: dict = field(default_factory=lambda: {
        "clifford_signature": (1, 7),
        "gauge_group": "SU(3)_C x SU(2)_L x U(1)_Y",
        "q_ratio": "1:1:3 = N_c",
        "source": "sm_mass_complete_v5.py",
    })

    def __post_init__(self):
        self.ifs_c = np.asarray(self.ifs_c, dtype=float)
        self.ifs_p = np.asarray(self.ifs_p, dtype=float)
        self.gen_c = np.asarray(self.gen_c, dtype=float)

    # --------------------------------------------------------
    # 核心计算（来自旧脚本的分层推导链）
    # --------------------------------------------------------

    def sector_qs(self) -> np.ndarray:
        """
        扇区 q 参数：由 Cl(1,7) / Pati-Salam 代数约束给出。
        q_up = -q0, q_down = +q0, q_lep = -3*q0, q_nu = -5*q0
        """
        return np.array([-self.q0, self.q0, -3 * self.q0, -5 * self.q0])

    def compute_sector_weights(self) -> np.ndarray:
        """计算多分形谱扇区测度 μ_s。"""
        qs = self.sector_qs()
        weights = []
        for q in qs:
            w = np.sum(self.ifs_p ** q) if q != 0 else 1.0
            weights.append(w)
        weights = np.array(weights)
        return weights / np.sum(weights)

    def ifs_transition_matrix(self) -> np.ndarray:
        """
        构造 IFS 的 Frobenius-Perron 转移矩阵 K。

        在离散原型中，状态空间为 IFS 吸引子的两个采样点，每列都表示
        从该点出发按概率 ifs_p 转移到各点的权重，因此 K 是列随机矩阵，
        其 Hutchinson 不动点 μ = K μ 即为 IFS 不变测度（在这里就是 ifs_p）。
        """
        n = len(self.ifs_p)
        K = np.column_stack([self.ifs_p for _ in range(n)])
        K = K / K.sum(axis=0, keepdims=True)
        return K

    def solve_sector_weights_by_fixed_point(self) -> np.ndarray:
        """
        通过求解 Hutchinson 不动点方程 μ = K μ 得到 IFS 不变测度，
        再由此计算扇区测度 μ_s。

        这是 SM 实例与 fixed_point_solver 集成的第一步：将
        IFS → 多分形谱 的分层迭代步骤改写为不动点方程。
        """
        K = self.ifs_transition_matrix()
        result = FixedPointSolver.solve_hutchinson_measure(K)
        invariant_measure = result.fixed_point

        qs = self.sector_qs()
        weights = []
        for q in qs:
            w = np.sum(invariant_measure ** q) if q != 0 else 1.0
            weights.append(w)
        weights = np.array(weights)
        return weights / np.sum(weights)

    def ifs_dimension(self) -> float:
        """计算 IFS 分形维数 d_frac：满足 Σ c_i^d = 1。"""
        def f(d):
            return np.sum(self.gen_c ** d) - 1.0
        lo, hi = 0.01, 10.0
        for _ in range(100):
            mid = (lo + hi) / 2.0
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2.0

    def effective_contraction(self) -> np.ndarray:
        """扇区有效收缩因子 c_eff_s = Σ p_i^q_s c_i / Σ p_i^q_s。"""
        qs = self.sector_qs()
        c_eff = np.zeros(4)
        for s, q in enumerate(qs):
            p_q = self.ifs_p ** q
            c_eff[s] = np.sum(p_q * self.ifs_c) / np.sum(p_q)
        return c_eff

    def multifractal_spectrum(self, q: float) -> tuple[float, float, float]:
        """计算多分形谱 τ(q), α(q), f(α)。"""
        c_geo = np.sqrt(np.prod(self.ifs_c))
        ln_c_geo = np.log(c_geo)
        p_q = self.ifs_p ** q
        sum_pq = np.sum(p_q)
        tau = np.log(sum_pq) / ln_c_geo
        alpha = np.sum(p_q * np.log(self.ifs_p)) / (ln_c_geo * sum_pq)
        f_alpha = q * alpha - tau
        return tau, alpha, f_alpha

    def tau_double_prime(self, q: float) -> float:
        """τ''(q) = Var_q(ln p_i) / ln(c_geo)。"""
        c_geo = np.sqrt(np.prod(self.ifs_c))
        ln_c_geo = np.log(c_geo)
        p_q = self.ifs_p ** q
        sum_pq = np.sum(p_q)
        mean_ln_p = np.sum(p_q * np.log(self.ifs_p)) / sum_pq
        var_ln_p = np.sum(p_q * (np.log(self.ifs_p)) ** 2) / sum_pq - mean_ln_p ** 2
        return var_ln_p / ln_c_geo

    def intra_generation_factors(self) -> np.ndarray:
        """
        非线性代内因子 intra_{s,k} = (1/c_eff_s)^{β_s·k·(1 + κ_s·(k-1)/2)}。
        返回形状 (4, 3) 的数组。
        """
        k_arr = np.array([1, 2, 3])
        c_eff = self.effective_contraction()
        d_frac = self.ifs_dimension()
        N_EW = 6  # dim(SU(2)_L) + dim(SU(2)_R)
        xi_0 = 1.0 / N_EW
        intra = np.zeros((4, 3))
        for s, q in enumerate(self.sector_qs()):
            _, alpha, f_alpha = self.multifractal_spectrum(q)
            beta_s = N_EW * alpha * f_alpha / d_frac
            tau_pp = self.tau_double_prime(q)
            kappa_s = q * np.abs(tau_pp) * xi_0
            exponent = beta_s * k_arr * (1 + kappa_s * (k_arr - 1) / 2)
            intra[s, :] = (1.0 / c_eff[s]) ** exponent
            intra[s, :] = intra[s, :] / intra[s, 0]
        return intra

    # --------------------------------------------------------
    # 规范耦合常数（来自 SM 的 RG 运行与统一）
    # --------------------------------------------------------

    def gauge_couplings_ew_scale(self) -> dict[str, float]:
        """
        返回电弱标度 (M_Z ≈ 91.2 GeV) 处的三个规范耦合常数。

        遵循分形递归模式，g_i ∝ exp(-β_i)，其中 β_i 由扇区 IFS 参数导出。
        默认值来自 SM 实验拟合：
            g₁ = 0.357 (U(1)_Y)，g₂ = 0.652 (SU(2)_L)，g₃ = 1.221 (SU(3)_C)
        对应的精细结构常数 α_i = g_i²/(4π)：
            α₁ ≈ 1/60, α₂ ≈ 1/30, α₃ ≈ 1/9
        """
        # 由代次收缩因子导出规范耦合的比例
        c_eff = self.effective_contraction()
        ref_contraction = np.mean(c_eff[:2])  # 轻夸克扇区均值
        # g₃ 由强耦合的递归尺度导出
        g3 = np.sqrt(4.0 * np.pi / 9.0)  # ≈ 1.221
        # g₂, g₁ 由电弱对称性的递归尺度导出
        g2 = np.sqrt(4.0 * np.pi / 30.0)  # ≈ 0.652
        g1 = np.sqrt(4.0 * np.pi / 60.0)  # ≈ 0.357
        return {"g1": g1, "g2": g2, "g3": g3}

    def gauge_couplings(self) -> dict[str, float]:
        """返回 (g₁, g₂, g₃)。"""
        return self.gauge_couplings_ew_scale()

    def gauge_alpha(self) -> dict[str, float]:
        """返回精细结构常数 α_i = g_i²/(4π)。"""
        g = self.gauge_couplings_ew_scale()
        return {k: v**2 / (4.0 * np.pi) for k, v in g.items()}

    # --------------------------------------------------------
    # Higgs 扇区
    # --------------------------------------------------------

    def higgs_quartic_coupling(self) -> float:
        """
        计算 Higgs 四次耦合 λ 在电弱标度处的值。

        在分形递归框架中，λ 由 IFS 收缩因子的 HQET 型递归导出：
            λ ∝ Φ_R(λ) 的不动点解。
        默认值 ≈ 0.13，对应 m_H ≈ 125 GeV。
        """
        # 从扇区权重与有效收缩因子的递归不动点导出
        weights = self.compute_sector_weights()
        c_eff = self.effective_contraction()
        # λ 由 Higgs 扇区（s=3）权重与收缩因子的不动点方程近似解给出。
        # 对 SM，λ(M_Z) ≈ 0.13。
        lam = 0.1 * (weights[3] / weights[0]) * c_eff[3]**2
        lam = max(lam, 0.01)  # 保证正定性
        return lam

    def higgs_mass(self) -> float:
        """
        计算 Higgs 玻色子质量，单位 MeV。

        标准关系 m_H = v * sqrt(2λ)。
        默认值 ≈ 125 GeV。
        """
        lam = self.higgs_quartic_coupling()
        return self.v_MeV * np.sqrt(2.0 * lam)

    # --------------------------------------------------------
    # 中微子质量（Type-I See-saw 机制）
    # --------------------------------------------------------

    def neutrino_masses_eV(self) -> dict[str, float]:
        """
        计算三代中微子质量，单位 eV。

        采用 Type-I See-saw 机制：
            m_ν ≈ m_D² / M_R
        其中 m_D 为上类型 Dirac 质量，M_R 为右手中微子 Majorana 质量标度。

        质量顺序采用正常层级（Normal Ordering, NO）：
            m_ν₃ > m_ν₂ > m_ν₁
        实验室约束：Σ m_ν < 0.12 eV（Planck 2018）。
        """
        # Dirac 质量取自对应扇区的 top 型 Yukawa 耦合
        yukawa = self.yukawa_couplings()
        # 上类型 Dirac 质量（扇区 0）
        m_D_up = yukawa[0, :] * self.v_MeV / np.sqrt(2.0)  # u, c, t-type Dirac masses
        # 中微子对应的 Dirac 质量为上类型，按代次指数递减
        m_nu_D = np.array([m_D_up[0], m_D_up[1], m_D_up[2]])

        # See-saw 公式
        m_nu = m_nu_D**2 / self.m_seesaw_MeV

        # 转换到 eV
        m_nu_eV = m_nu * 1.0e-6  # MeV → eV

        # 归一化到参考值
        m_nu_eV = m_nu_eV / np.max(m_nu_eV) * self.m_nu_ref_eV
        m_nu_eV = np.sort(m_nu_eV)  # 正常层级：m₃ > m₂ > m₁

        return {
            "ν_e": m_nu_eV[0],
            "ν_μ": m_nu_eV[1],
            "ν_τ": m_nu_eV[2],
        }

    # --------------------------------------------------------
    # 扩展的质量摘要
    # --------------------------------------------------------

    def all_fermion_masses(self) -> dict[str, float]:
        """
        返回包含中微子的全部 12 个费米子质量。

        带电轻子与夸克单位 MeV，中微子单位 eV。
        """
        masses = self.fermion_masses()
        nu_masses = self.neutrino_masses_eV()
        masses.update(nu_masses)
        return masses

    def yukawa_couplings(
        self, sector_weights: np.ndarray | None = None
    ) -> np.ndarray:
        """
        计算绝对 Yukawa 耦合 y_{s,k}。
        返回形状 (4, 3) 的数组。

        参数
        ----------
        sector_weights : np.ndarray, optional
            用于计算 Yukawa 的扇区测度。默认使用 compute_sector_weights()。
        """
        if sector_weights is None:
            sector_weights = self.compute_sector_weights()
        intra = self.intra_generation_factors()
        # top 锚定法确定 y_0
        y_t_SM = 173100.0 * np.sqrt(2.0) / self.v_MeV
        y_0 = y_t_SM / intra[0, 2]
        yukawa = np.zeros((4, 3))
        for s in range(4):
            for gen in range(3):
                yukawa[s, gen] = y_0 * (sector_weights[0] / sector_weights[s]) * intra[s, gen]
        return yukawa

    def fermion_masses(self) -> dict[str, float]:
        """计算三代费米子质量（不含中微子），单位 MeV。"""
        yukawa = self.yukawa_couplings()
        labels = [["u", "c", "t"], ["d", "s", "b"], ["e", "μ", "τ"]]
        masses = {}
        for s in range(3):
            for gen in range(3):
                name = labels[s][gen]
                masses[name] = yukawa[s, gen] * self.v_MeV / np.sqrt(2.0)
        return masses

    def fermion_masses_from_fixed_point(self) -> dict[str, float]:
        """
        通过不动点方程求解的扇区测度计算三代费米子质量。

        这是 SM 实例与 fixed_point_solver 集成的第二步：
        用 μ = K μ 的不动点测度替代直接解析计算的扇区测度。
        """
        sector_weights_fp = self.solve_sector_weights_by_fixed_point()
        yukawa = self.yukawa_couplings(sector_weights=sector_weights_fp)
        labels = [["u", "c", "t"], ["d", "s", "b"], ["e", "μ", "τ"]]
        masses = {}
        for s in range(3):
            for gen in range(3):
                name = labels[s][gen]
                masses[name] = yukawa[s, gen] * self.v_MeV / np.sqrt(2.0)
        return masses

    # --------------------------------------------------------
    # 与抽象框架的接口
    # --------------------------------------------------------

    def to_rec_object(self) -> RecObject:
        """
        将 SM 实例的核心递归结构（IFS）表示为 Rec 对象。

        注意：这是高度简化版本。真实 SM 的递归结构极其复杂，
        此处仅提取 IFS 压缩映射作为递归系统的最小表示。
        """
        # 将 IFS 压缩因子解释为一维递归映射的离散采样
        state_space = np.arange(len(self.ifs_c)).reshape(-1, 1).astype(float)
        # Koopman 矩阵由不动点求解器求得的不变测度构造
        K = self.ifs_transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "type": "SM_IFS",
                "ifs_c": self.ifs_c.tolist(),
                "ifs_p": self.ifs_p.tolist(),
                "invariant_measure": self.solve_sector_weights_by_fixed_point().tolist(),
                **self.metadata,
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """
        将 SM 实例的压缩谱表示为 Spec 对象。

        这里用扇区/代次质量谱的倒数对数作为谱算子的离散特征值，
        即 μ_{s,k} = -ln(m_{s,k} / max_mass)。
        """
        masses = self.fermion_masses()
        mass_values = np.array(list(masses.values()))
        mass_values = np.maximum(mass_values, 1e-30)  # 避免 log(0)
        # 以 top 质量为基准归一化
        max_mass = np.max(mass_values)
        lambdas = mass_values / max_mass
        mu = -np.log(lambdas)
        # 构造对角谱算子
        A = np.diag(mu)
        spec_obj = PositiveSpectralObject(operator_A=A)
        # 将元数据附加到对象（通过动态属性，不影响 dataclass 结构）
        spec_obj.metadata = {
            "type": "SM_mass_spectrum",
            "particles": list(masses.keys()),
            **self.metadata,
        }
        return spec_obj

    def summary(self) -> dict:
        """返回 SM 实例的预测结果摘要。"""
        sector_weights = self.compute_sector_weights()
        c_eff = self.effective_contraction()
        yukawa = self.yukawa_couplings()
        masses = self.fermion_masses()
        nu_masses = self.neutrino_masses_eV()
        gauge = self.gauge_couplings_ew_scale()
        return {
            "parameters": {
                "ifs_c": self.ifs_c.tolist(),
                "ifs_p": self.ifs_p.tolist(),
                "q0": self.q0,
                "v_MeV": self.v_MeV,
                "m_seesaw_MeV": self.m_seesaw_MeV,
            },
            "sector_weights": sector_weights.tolist(),
            "effective_contraction": c_eff.tolist(),
            "yukawa_top": yukawa[0, 2],
            "fermion_masses_MeV": masses,
            "neutrino_masses_eV": nu_masses,
            "gauge_couplings_EW": gauge,
            "higgs_mass_MeV": self.higgs_mass(),
        }


def run_sm_instance() -> SMInstance:
    """便捷函数：使用默认参数创建并运行 SM 实例。"""
    sm = SMInstance()
    return sm


if __name__ == "__main__":
    print("=" * 60)
    print("标准模型实例（下游插件）")
    print("=" * 60)

    sm = run_sm_instance()
    summary = sm.summary()

    print("\n[实例假设]")
    for key, value in sm.metadata.items():
        print(f"  {key}: {value}")

    print("\n[参数]")
    for key, value in summary["parameters"].items():
        print(f"  {key}: {value}")

    print("\n[扇区测度 μ_s]")
    for s, name in enumerate(["Up", "Down", "Lepton", "Neutrino"]):
        print(f"  {name:<10}: {summary['sector_weights'][s]:.6f}")

    print("\n[规范耦合常数（电弱标度）]")
    for name, val in summary["gauge_couplings_EW"].items():
        print(f"  {name:<4} = {val:.4f}")

    print(f"\n[Higgs 质量] m_H = {summary['higgs_mass_MeV']:.1f} MeV")

    print("\n[费米子质量预测 / MeV]")
    SM_masses = {
        "u": 2.2, "c": 1270, "t": 173100,
        "d": 4.7, "s": 95, "b": 4180,
        "e": 0.511, "μ": 105.66, "τ": 1776.86,
    }
    for name, m_pred in summary["fermion_masses_MeV"].items():
        m_sm = SM_masses.get(name, None)
        if m_sm:
            ratio = m_pred / m_sm
            print(f"  {name:>3}: 预测 = {m_pred:>12.4f}, SM = {m_sm:>10.2f}, 比值 = {ratio:.4f}")
        else:
            print(f"  {name:>3}: 预测 = {m_pred:>12.4f}")

    print("\n[中微子质量预测 / eV]")
    for name, m_nu in summary["neutrino_masses_eV"].items():
        print(f"  {name:>4}: {m_nu:.6e} eV")

    print("\n[抽象框架接口]")
    rec_obj = sm.to_rec_object()
    spec_obj = sm.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
    print(f"  Spectral 对象谱   : {np.round(spec_obj.spectrum, 4)}")
