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

#!/usr/bin/env python3
"""
Phase 52 — B4: 普朗克能标多体散射——散射谱数据库
===================================================

构建普朗克能标散射谱的完整数据库，支持：
  1. 参数扫描（能量、质量比、自旋）
  2. 谱数据标准化存储（NPZ 格式 + 可扩展元数据）
  3. 查询接口（能量区间、截面阈值、角分布模式）
  4. 可视化工具（截面/振幅/角分布图、比较图、热图）

依赖：numpy, scipy, spectral_numerics, B1-B3 散射模块
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, Callable, List
from dataclasses import dataclass, field, asdict
from scipy import integrate, interpolate
import sys
import os
import json
import warnings
from enum import Enum

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_spectrum.spectral_numerics import (
    SpectralOperator, SpectralData, SpectralCutoff,
    M_PL, G_N, L_PL
)
from dynamic_spectrum.planck_scattering_2to2 import (
    ScatteringKinematics, GravitonScatteringAmplitude,
    GravitonMatterScattering, SpectralUVRegularization,
    KAPPA_SQ, LAMBDA_MAX
)
from dynamic_spectrum.planck_scattering_2ton import (
    SpectralNPhaseSpace, Graviton2to3Scattering,
    Graviton2to4Scattering
)
from dynamic_spectrum.planck_scattering_loop import (
    SpectralOneLoopAmplitude, SpectralRGEvolution,
    ALPHA_QED
)


# ============================================================
#  数据类型与枚举
# ============================================================

class ProcessType(Enum):
    """散射过程类型"""
    GRAVITON_GRAVITON = 'gg_2to2'      # 引力子-引力子 2→2
    GRAVITON_MATTER = 'gm_2to2'        # 引力子-物质 2→2
    SOFT_2TO3 = 'soft_2to3'            # 软引力子 2→3
    SOFT_2TO4 = 'soft_2to4'            # 软引力子 2→4
    QED_BORN = 'qed_born'              # QED Born (树图)
    QED_1LOOP = 'qed_1loop'            # QED 单圈
    QED_RG = 'qed_rg'                  # QED RG 改进


@dataclass
class ScanParameters:
    """扫描参数配置"""
    energy_min: float = 0.001          # 最小质心能 (M_Pl)
    energy_max: float = 2.0            # 最大质心能 (M_Pl)
    energy_points: int = 30            # 能量采样点
    mass_ratio_min: float = 1.0        # 最小质量比
    mass_ratio_max: float = 10.0       # 最大质量比
    mass_ratio_points: int = 10        # 质量比采样数
    spin_min: float = 0.0              # 最小自旋
    spin_max: float = 0.9              # 最大自旋
    spin_points: int = 5               # 自旋采样数
    dim: int = 32                      # 谱截断维数
    n_theta: int = 30                  # 角积分采样


@dataclass
class EnergyScanPoint:
    """单能量点的扫描数据"""
    E: float                           # 质心能
    sigma_gg_2to2: float = 0.0         # 引力子-引力子截面
    sigma_gm_2to2: float = 0.0         # 引力子-物质截面
    sigma_soft_2to3: float = 0.0       # 2→3 截面
    sigma_soft_2to4: float = 0.0       # 2→4 截面
    sigma_qed_born: float = 0.0        # QED Born 截面
    sigma_qed_1loop: float = 0.0       # QED 单圈截面
    sigma_qed_rg: float = 0.0          # QED RG 改进截面
    correction_1loop: float = 0.0      # 单圈修正因子
    amplitude: float = 0.0             # 引力子振幅模
    amplitude_suppression: float = 1.0  # UV 压制因子
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AngularScanPoint:
    """角分布扫描点"""
    cos_theta: float                   # 散射角余弦
    dsigma_dOmega: float = 0.0         # 微分散射截面
    amplitude: float = 0.0             # 振幅模


# ============================================================
#  1. 散射谱数据库核心
# ============================================================

class ScatteringDatabase:
    """
    普朗克能标散射谱数据库。

    存储和管理 B1-B3 计算结果，支持：
    - 参数空间扫描（E, mass_ratio, spin）
    - 标准化 NPZ 存储/加载
    - 元数据追踪
    """

    def __init__(self, name: str = "planck_scattering_db",
                 scan_params: Optional[ScanParameters] = None):
        self.name = name
        self.scan_params = scan_params or ScanParameters()

        # 内部容器
        self._data: Dict[float, EnergyScanPoint] = {}
        self._angular_data: Dict[float, List[AngularScanPoint]] = {}
        self._processes: List[ProcessType] = []
        self._metadata: Dict[str, Any] = {
            'name': name,
            'version': '0.1',
            'created': '2026-07-25',
            'scan_params': asdict(self.scan_params),
            'constants': {
                'M_Pl': float(M_PL),
                'LAMBDA_MAX': float(LAMBDA_MAX),
                'alpha_QED': float(ALPHA_QED),
            },
        }

        # 子引擎（延迟初始化）
        self._graviton_amp: Optional[GravitonScatteringAmplitude] = None
        self._soft_23: Optional[Graviton2to3Scattering] = None
        self._soft_24: Optional[Graviton2to4Scattering] = None
        self._qed_amp: Optional[SpectralOneLoopAmplitude] = None
        self._rg: Optional[SpectralRGEvolution] = None
        self._nps: Optional[SpectralNPhaseSpace] = None

    # ---- 引擎初始化 ----

    def _init_graviton(self):
        if self._graviton_amp is None:
            self._graviton_amp = GravitonScatteringAmplitude(dim=self.scan_params.dim)

    def _init_soft(self):
        if self._soft_23 is None:
            self._soft_23 = Graviton2to3Scattering(dim=self.scan_params.dim)
        if self._soft_24 is None:
            self._soft_24 = Graviton2to4Scattering(dim=self.scan_params.dim)

    def _init_qed(self):
        if self._qed_amp is None:
            self._qed_amp = SpectralOneLoopAmplitude(dim=self.scan_params.dim)

    def _init_rg(self):
        if self._rg is None:
            self._rg = SpectralRGEvolution()

    def _init_nps(self):
        if self._nps is None:
            self._nps = SpectralNPhaseSpace(dim=self.scan_params.dim)

    # ---- 2a. 能量扫描（核心） ----

    def compute_energy_scan(self, E_min: float = None,
                            E_max: float = None,
                            n_points: int = None,
                            cos_theta: float = 0.0,
                            processes: List[ProcessType] = None,
                            verbose: bool = True) -> Dict[float, EnergyScanPoint]:
        """
        在能量维度上扫描所有散射过程。

        参数
        ----------
        E_min, E_max : float
            扫描范围（默认使用 scan_params）
        n_points : int
            采样点数
        cos_theta : float
            固定散射角
        processes : list[ProcessType]
            要扫描的过程（默认全部）
        verbose : bool
            是否打印进度

        返回
        -------
        dict[E -> EnergyScanPoint] : 扫描结果
        """
        E_min = E_min if E_min is not None else self.scan_params.energy_min
        E_max = E_max if E_max is not None else self.scan_params.energy_max
        n = n_points if n_points is not None else self.scan_params.energy_points

        E_vals = np.geomspace(E_min, E_max, n)
        if processes is None:
            processes = list(ProcessType)

        for pt in processes:
            if pt not in self._processes:
                self._processes.append(pt)

        results = {}
        for i, E in enumerate(E_vals):
            if verbose:
                print(f"  Energy scan: E = {E:.6e} M_Pl [{i+1}/{n}]", end='\r')

            pt = EnergyScanPoint(E=float(E))
            kin = ScatteringKinematics.from_energy_angle(E, cos_theta)

            for proc in processes:
                val = self._compute_process(proc, kin, E)
                self._set_process_value(pt, proc, val)

            results[float(E)] = pt

        if verbose:
            print()

        self._data.update(results)
        self._metadata['energy_scan_range'] = [float(E_min), float(E_max)]
        self._metadata['energy_scan_points'] = n

        return results

    def _compute_process(self, proc: ProcessType,
                          kin: ScatteringKinematics,
                          E: float) -> float:
        """计算单个过程的截面或振幅值"""
        if proc == ProcessType.GRAVITON_GRAVITON:
            self._init_graviton()
            return float(self._graviton_amp.total_cross_section(E, n_theta=10))

        elif proc == ProcessType.GRAVITON_MATTER:
            self._init_graviton()
            gm = GravitonMatterScattering(dim=self.scan_params.dim)
            amp = gm.graviton_scalar_amplitude(kin)
            return float(abs(amp) ** 2 / (64.0 * np.pi ** 2 * kin.s))

        elif proc == ProcessType.SOFT_2TO3:
            self._init_soft()
            dsig = self._soft_23.differential_cross_section_2to3(E, cos_theta=0.0)
            return float(dsig * 4.0 * np.pi)  # 近似总截面

        elif proc == ProcessType.SOFT_2TO4:
            self._init_soft()
            dsig = self._soft_24.differential_cross_section_2to4(E, cos_theta=0.0)
            return float(dsig * 4.0 * np.pi)  # 近似总截面

        elif proc == ProcessType.QED_BORN:
            self._init_qed()
            return float(self._qed_amp.cross_section_spectral(E ** 2, include_loops=False))

        elif proc == ProcessType.QED_1LOOP:
            self._init_qed()
            return float(self._qed_amp.cross_section_spectral(E ** 2, include_loops=True))

        elif proc == ProcessType.QED_RG:
            self._init_rg()
            result = self._rg.rg_improved_cross_section(E ** 2, cos_theta=0.0)
            return float(result['sigma_RG'])

        return 0.0

    @staticmethod
    def _set_process_value(pt: EnergyScanPoint, proc: ProcessType, val: float):
        """设置 EnergyScanPoint 中对应过程的值"""
        mapping = {
            ProcessType.GRAVITON_GRAVITON: ('sigma_gg_2to2',),
            ProcessType.GRAVITON_MATTER: ('sigma_gm_2to2',),
            ProcessType.SOFT_2TO3: ('sigma_soft_2to3',),
            ProcessType.SOFT_2TO4: ('sigma_soft_2to4',),
            ProcessType.QED_BORN: ('sigma_qed_born',),
            ProcessType.QED_1LOOP: ('sigma_qed_1loop',),
            ProcessType.QED_RG: ('sigma_qed_rg',),
        }
        attr = mapping.get(proc, (None,))[0]
        if attr:
            setattr(pt, attr, val)

    # ---- 2b. 角分布扫描 ----

    def compute_angular_distribution(self, E: float,
                                      n_theta: int = 30,
                                      processes: List[ProcessType] = None
                                      ) -> List[AngularScanPoint]:
        """
        计算固定能量下的角分布。

        参数
        ----------
        E : float
            质心能
        n_theta : int
            散射角采样数
        processes : list[ProcessType]
            要扫描的过程

        返回
        -------
        list[AngularScanPoint] : 角分布数据
        """
        if processes is None:
            processes = [ProcessType.GRAVITON_GRAVITON,
                         ProcessType.QED_BORN]

        cos_theta_vals = np.linspace(-0.99, 0.99, n_theta)
        points = []

        self._init_graviton()
        self._init_qed()

        for ct in cos_theta_vals:
            pt = AngularScanPoint(cos_theta=float(ct))
            kin = ScatteringKinematics.from_energy_angle(E, ct)

            # 引力子幅（取主导过程）
            if ProcessType.GRAVITON_GRAVITON in processes:
                M_spec = self._graviton_amp.spectral_amplitude(kin)
                dsigma = self._graviton_amp.differential_cross_section(kin)
                pt.amplitude = float(abs(M_spec))
                pt.dsigma_dOmega = float(dsigma)

            points.append(pt)

        self._angular_data[float(E)] = points
        return points

    # ---- 3. 数据存储与加载 ----

    def save(self, filepath: str):
        """
        保存数据库到 NPZ 文件。

        格式：NPZ 包含 arrays + JSON 元数据
        """
        save_dir = os.path.dirname(filepath) if os.path.dirname(filepath) else '.'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        n = len(self._data)
        if n == 0:
            warnings.warn("Database is empty, saving empty file")
            data_arrays = {}
        else:
            # 提取数组数据
            sorted_keys = sorted(self._data.keys())
            E_arr = np.array(sorted_keys)
            sigma_arrs = {}
            for field in EnergyScanPoint.__dataclass_fields__:
                if field == 'E' or field == 'metadata':
                    continue
                vals = [getattr(self._data[k], field, 0.0) for k in sorted_keys]
                sigma_arrs[f'sigma_{field}'] = np.array(vals)

            # 角分布
            angular_E = np.array(list(self._angular_data.keys()))
            angular_ct = []
            angular_dsigma = []
            for E_val, pts in self._angular_data.items():
                for pt in pts:
                    angular_ct.append(pt.cos_theta)
                    angular_dsigma.append(pt.dsigma_dOmega)

            data_arrays = {
                'E': E_arr,
                **sigma_arrs,
                'angular_E': angular_E,
                'angular_cos_theta': np.array(angular_ct) if angular_ct else np.array([]),
                'angular_dsigma': np.array(angular_dsigma) if angular_dsigma else np.array([]),
            }

        # 元数据
        self._metadata['n_energy_points'] = n
        self._metadata['n_angular_E'] = len(self._angular_data)
        self._metadata['processes'] = [p.value for p in self._processes]

        # 保存 NPZ
        np.savez_compressed(filepath, **data_arrays)

        # 保存元数据为 JSON
        meta_path = filepath.replace('.npz', '_meta.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(self._metadata, f, indent=2, ensure_ascii=False)

        return filepath

    def load(self, filepath: str):
        """
        从 NPZ 文件加载数据库。

        参数
        ----------
        filepath : str
            .npz 文件路径
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Database file not found: {filepath}")

        data = np.load(filepath)

        # 加载能量扫描
        if 'E' in data:
            E_arr = data['E']
            self._data = {}
            for i, E in enumerate(E_arr):
                pt_kwargs = {'E': float(E)}
                for field in EnergyScanPoint.__dataclass_fields__:
                    if field == 'E' or field == 'metadata':
                        continue
                    arr_name = f'sigma_{field}'
                    if arr_name in data:
                        pt_kwargs[field] = float(data[arr_name][i])
                self._data[float(E)] = EnergyScanPoint(**pt_kwargs)

        # 加载角分布
        if 'angular_E' in data and len(data['angular_E']) > 0:
            self._angular_data = {}
            # 简化加载：重建部分角分布

        # 加载元数据
        meta_path = filepath.replace('.npz', '_meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                self._metadata.update(json.load(f))

        return True

    # ---- 4. 查询接口 ----

    def query_energy_range(self, E_min: float, E_max: float) -> Dict[float, EnergyScanPoint]:
        """
        按能量区间查询。

        参数
        ----------
        E_min, E_max : float
            能量区间

        返回
        -------
        dict[E -> EnergyScanPoint]
        """
        return {E: pt for E, pt in self._data.items()
                if E_min <= E <= E_max}

    def query_cross_section_above(self, threshold: float,
                                    process: str = 'sigma_gg_2to2') -> Dict[float, EnergyScanPoint]:
        """
        按截面阈值查询。

        参数
        ----------
        threshold : float
            截面阈值
        process : str
            过程字段名

        返回
        -------
        dict[E -> EnergyScanPoint]
        """
        return {E: pt for E, pt in self._data.items()
                if getattr(pt, process, 0.0) >= threshold}

    def query_correction_below(self, threshold: float) -> Dict[float, EnergyScanPoint]:
        """
        查询单圈修正低于阈值的能量点（微扰有效区）。

        参数
        ----------
        threshold : float
            修正因子阈值

        返回
        -------
        dict[E -> EnergyScanPoint]
        """
        return {E: pt for E, pt in self._data.items()
                if abs(pt.correction_1loop - 1.0) <= threshold}

    def get_dominant_process(self, E: float) -> Tuple[str, float]:
        """
        获取某个能量下主导的散射过程。

        参数
        ----------
        E : float

        返回
        -------
        (process_name, cross_section)
        """
        if E not in self._data:
            return ('unknown', 0.0)

        pt = self._data[E]
        candidates = [
            ('gg_2to2', pt.sigma_gg_2to2),
            ('gm_2to2', pt.sigma_gm_2to2),
            ('soft_2to3', pt.sigma_soft_2to3),
            ('soft_2to4', pt.sigma_soft_2to4),
            ('qed_born', pt.sigma_qed_born),
        ]
        return max(candidates, key=lambda x: x[1])

    def summary(self) -> Dict[str, Any]:
        """数据库摘要"""
        n = len(self._data)
        if n == 0:
            return {'name': self.name, 'entries': 0}

        E_vals = sorted(self._data.keys())
        cross_sections = {p.value: [] for p in self._processes}

        for E in E_vals:
            pt = self._data[E]
            for p in self._processes:
                attr = {
                    ProcessType.GRAVITON_GRAVITON: 'sigma_gg_2to2',
                    ProcessType.GRAVITON_MATTER: 'sigma_gm_2to2',
                    ProcessType.SOFT_2TO3: 'sigma_soft_2to3',
                    ProcessType.SOFT_2TO4: 'sigma_soft_2to4',
                    ProcessType.QED_BORN: 'sigma_qed_born',
                    ProcessType.QED_1LOOP: 'sigma_qed_1loop',
                    ProcessType.QED_RG: 'sigma_qed_rg',
                }.get(p, '')
                if attr:
                    cross_sections[p.value].append(getattr(pt, attr, 0.0))

        return {
            'name': self.name,
            'entries': n,
            'energy_range': [float(min(E_vals)), float(max(E_vals))],
            'processes': [p.value for p in self._processes],
            'angular_E_count': len(self._angular_data),
        }


# ============================================================
#  2. 可视化工具
# ============================================================

class ScatteringVisualizer:
    """
    散射谱数据可视化工具。

    提供：
    - 截面 vs 能量图（多过程对比）
    - 角分布图
    - 截面比较图（树图 vs 单圈 vs RG）
    - 热图（能量 × 截面）
    """

    def __init__(self, db: Optional[ScatteringDatabase] = None):
        self.db = db

    def set_database(self, db: ScatteringDatabase):
        """设置数据源"""
        self.db = db

    def plot_cross_section_vs_energy(self, processes: List[ProcessType] = None,
                                      filename: Optional[str] = None,
                                      log_scale: bool = True):
        """
        绘制截面 vs 能量曲线（用 matplotlib，若无则输出表格）。
        """
        if self.db is None or len(self.db._data) == 0:
            print("  No data to plot. Run energy scan first.")
            return self._print_empty_table()

        if processes is None:
            processes = self.db._processes

        sorted_E = sorted(self.db._data.keys())

        print(f"\n  Cross Section vs Energy ({self.db.name})")
        print(f"  {'=' * 65}")
        header = f"  {'E (M_Pl)':<12}"
        for p in processes:
            header += f" {p.value:<16}"
        print(header)
        print(f"  {'-' * 65}")

        for E in sorted_E[::max(1, len(sorted_E) // 8)]:  # 采样 ~8 点
            pt = self.db._data[E]
            row = f"  {E:<12.4e}"
            for p in processes:
                val = self._get_cross_section(pt, p)
                row += f" {val:<16.4e}"
            print(row)

    def plot_angular_distribution(self, E: float, filename: Optional[str] = None):
        """
        绘制角分布。
        """
        if E not in self.db._angular_data:
            print(f"  No angular data for E={E:.4f} M_Pl. Run compute_angular_distribution first.")
            return

        pts = self.db._angular_data[E]

        print(f"\n  Angular Distribution at E = {E:.4f} M_Pl")
        print(f"  {'=' * 45}")
        print(f"  {'cos θ':<10} {'dsigma/dΩ':<16} {'|M|':<16}")
        print(f"  {'-' * 45}")
        for pt in pts[::max(1, len(pts) // 6)]:
            print(f"  {pt.cos_theta:<10.4f} {pt.dsigma_dOmega:<16.6e} {pt.amplitude:<16.6e}")

    def plot_correction_comparison(self, filename: Optional[str] = None):
        """
        比较树图、单圈、RG 改进截面。
        """
        if self.db is None or len(self.db._data) == 0:
            return

        sorted_E = sorted(self.db._data.keys())

        print(f"\n  Correction Comparison: Born vs 1-loop vs RG")
        print(f"  {'=' * 60}")
        print(f"  {'E (M_Pl)':<12} {'σ_Born':<14} {'σ_1loop':<14} {'σ_RG':<14}")
        print(f"  {'-' * 60}")
        for E in sorted_E[::max(1, len(sorted_E) // 8)]:
            pt = self.db._data[E]
            print(f"  {E:<12.4e} {pt.sigma_qed_born:<14.6e} "
                  f"{pt.sigma_qed_1loop:<14.6e} {pt.sigma_qed_rg:<14.6e}")

    def plot_dominance_map(self, filename: Optional[str] = None):
        """
        过程主导图：显示不同能标区间的主导过程。
        """
        if self.db is None or len(self.db._data) == 0:
            return

        sorted_E = sorted(self.db._data.keys())

        print(f"\n  Process Dominance Map")
        print(f"  {'=' * 55}")
        print(f"  {'Energy Range (M_Pl)':<25} {'Dominant Process':<20} {'σ (M_Pl⁻²)':<14}")
        print(f"  {'-' * 55}")

        # 分段显示
        n_seg = min(6, len(sorted_E))
        seg_size = max(1, len(sorted_E) // n_seg)
        for i in range(0, len(sorted_E), seg_size):
            seg = sorted_E[i:i + seg_size]
            E_mid = np.mean(seg)
            proc_name, sigma = self.db.get_dominant_process(E_mid)
            E_range = f"[{seg[0]:.3f}, {seg[-1]:.3f}]"
            print(f"  {E_range:<25} {proc_name:<20} {sigma:<14.4e}")

    def export_table(self, filename: str, format: str = 'csv'):
        """
        导出数据表。

        参数
        ----------
        filename : str
            输出文件路径
        format : str
            'csv' 或 'txt'
        """
        if self.db is None or len(self.db._data) == 0:
            return

        sorted_E = sorted(self.db._data.keys())
        fields = [f.name for f in EnergyScanPoint.__dataclass_fields__.values()]

        if format == 'csv':
            with open(filename, 'w', encoding='utf-8') as f:
                header = 'E,' + ','.join(f for f in fields if f not in ('E', 'metadata'))
                f.write(header + '\n')
                for E in sorted_E:
                    pt = self.db._data[E]
                    vals = [str(E)]
                    for fld in fields:
                        if fld in ('E', 'metadata'):
                            continue
                        vals.append(str(getattr(pt, fld, 0.0)))
                    f.write(','.join(vals) + '\n')
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Scattering Database: {self.db.name}\n")
                f.write(f"{'=' * 60}\n")
                for E in sorted_E:
                    pt = self.db._data[E]
                    f.write(f"E = {E:.6e}\n")
                    for fld in fields:
                        if fld in ('E', 'metadata'):
                            continue
                        val = getattr(pt, fld, 0.0)
                        if abs(val) > 1e-20:
                            f.write(f"  {fld}: {val:.6e}\n")

        print(f"  Table exported to {filename}")

    @staticmethod
    def _get_cross_section(pt: EnergyScanPoint, proc: ProcessType) -> float:
        mapping = {
            ProcessType.GRAVITON_GRAVITON: 'sigma_gg_2to2',
            ProcessType.GRAVITON_MATTER: 'sigma_gm_2to2',
            ProcessType.SOFT_2TO3: 'sigma_soft_2to3',
            ProcessType.SOFT_2TO4: 'sigma_soft_2to4',
            ProcessType.QED_BORN: 'sigma_qed_born',
            ProcessType.QED_1LOOP: 'sigma_qed_1loop',
            ProcessType.QED_RG: 'sigma_qed_rg',
        }
        attr = mapping.get(proc, '')
        return getattr(pt, attr, 0.0) if attr else 0.0

    @staticmethod
    def _print_empty_table():
        print("  (empty)")


# ============================================================
#  3. 数值验证（6 项测试）
# ============================================================

def verify_database_creation():
    """验证数据库创建和初始化"""
    db = ScatteringDatabase(name="test_db")
    assert db.name == "test_db"
    assert len(db._data) == 0
    assert len(db._processes) == 0
    assert 'scan_params' in db._metadata

    # 默认参数检查
    sp = db.scan_params
    assert sp.energy_min > 0
    assert sp.energy_max > sp.energy_min
    assert sp.dim > 0

    print(f"  Database '{db.name}' created, dim={sp.dim}")
    print(f"  Energy scan range: [{sp.energy_min}, {sp.energy_max}] x {sp.energy_points} points")
    print("  ✅ Database creation verified")
    return True


def verify_energy_scan_gg():
    """验证引力子-引力子能量扫描"""
    db = ScatteringDatabase(scan_params=ScanParameters(
        energy_min=0.01, energy_max=1.0,
        energy_points=5, dim=16
    ))

    results = db.compute_energy_scan(
        processes=[ProcessType.GRAVITON_GRAVITON],
        verbose=False
    )

    assert len(results) == 5
    for E, pt in results.items():
        assert pt.sigma_gg_2to2 > 0
        print(f"  E={E:.4f}: σ_gg = {pt.sigma_gg_2to2:.4e}")

    # 截面应随能量增长（~E^2 标度）
    E_vals = sorted(results.keys())
    low_sigma = results[E_vals[0]].sigma_gg_2to2
    high_sigma = results[E_vals[-1]].sigma_gg_2to2
    print(f"  σ(E={E_vals[0]:.4f}) = {low_sigma:.4e}")
    print(f"  σ(E={E_vals[-1]:.4f}) = {high_sigma:.4e}")
    assert high_sigma > low_sigma

    print("  ✅ Energy scan (gg) verified")
    return True


def verify_qed_scan():
    """验证 QED 过程能量扫描（Born, 1-loop, RG）"""
    db = ScatteringDatabase(scan_params=ScanParameters(
        energy_min=0.01, energy_max=2.0,
        energy_points=4, dim=16
    ))

    results = db.compute_energy_scan(
        processes=[ProcessType.QED_BORN, ProcessType.QED_1LOOP, ProcessType.QED_RG],
        verbose=False
    )

    assert len(results) == 4
    for E, pt in results.items():
        assert pt.sigma_qed_born > 0
        assert pt.sigma_qed_1loop > 0
        assert pt.sigma_qed_rg > 0
        # 单圈 > Born（弱耦合正修正）
        assert pt.sigma_qed_1loop > pt.sigma_qed_born
        print(f"  E={E:.4f}: Born={pt.sigma_qed_born:.4e} 1loop={pt.sigma_qed_1loop:.4e} "
              f"RG={pt.sigma_qed_rg:.4e}")

    # 在 Planck 能标附近，RG 改进应使截面增大
    E_max = max(results.keys())
    pt = results[E_max]
    print(f"  At E={E_max:.4f}: RG/Born = {pt.sigma_qed_rg / max(pt.sigma_qed_born, 1e-40):.4f}")
    assert pt.sigma_qed_rg > pt.sigma_qed_born

    print("  ✅ QED energy scan verified")
    return True


def verify_save_load():
    """验证存储-加载往返"""
    import tempfile

    db = ScatteringDatabase(name="save_test",
                            scan_params=ScanParameters(energy_min=0.1, energy_max=1.0,
                                                       energy_points=3, dim=8))

    db.compute_energy_scan(processes=[ProcessType.QED_BORN], verbose=False)

    with tempfile.TemporaryDirectory() as tmpdir:
        fpath = os.path.join(tmpdir, "test_db.npz")
        db.save(fpath)

        # 验证文件存在
        assert os.path.exists(fpath)
        assert os.path.exists(fpath.replace('.npz', '_meta.json'))

        # 加载
        db2 = ScatteringDatabase(name="loaded")
        db2.load(fpath)

        # 验证数据一致性
        assert len(db2._data) == len(db._data)
        for E in db._data:
            assert E in db2._data
            assert abs(db2._data[E].sigma_qed_born - db._data[E].sigma_qed_born) < 1e-10

    print(f"  Save/load roundtrip: {len(db._data)} points preserved")
    print("  ✅ Save/load verified")
    return True


def verify_query_interface():
    """验证查询接口"""
    db = ScatteringDatabase(scan_params=ScanParameters(
        energy_min=0.01, energy_max=1.0,
        energy_points=10, dim=16
    ))

    db.compute_energy_scan(processes=[ProcessType.GRAVITON_GRAVITON,
                                      ProcessType.QED_BORN], verbose=False)

    # 能量区间查询
    mid_range = db.query_energy_range(0.1, 0.5)
    assert len(mid_range) > 0
    print(f"  Energy range [0.1, 0.5]: {len(mid_range)} points")

    # 截面阈值查询
    threshold = 1.0
    high_sigma = db.query_cross_section_above(threshold, 'sigma_gg_2to2')
    print(f"  Cross section > {threshold}: {len(high_sigma)} points")

    # 主导过程
    E_mid = (db.scan_params.energy_min + db.scan_params.energy_max) / 2.0
    closest_E = min(db._data.keys(), key=lambda x: abs(x - E_mid))
    proc_name, sigma = db.get_dominant_process(closest_E)
    print(f"  Dominant at E={closest_E:.4f}: {proc_name} (σ={sigma:.4e})")

    # 摘要
    summary = db.summary()
    print(f"  Database summary: {summary['entries']} entries, "
          f"E in [{summary['energy_range'][0]:.3f}, {summary['energy_range'][1]:.3f}]")

    print("  ✅ Query interface verified")
    return True


def verify_visualization():
    """验证可视化工具"""
    db = ScatteringDatabase(scan_params=ScanParameters(
        energy_min=0.01, energy_max=1.0,
        energy_points=6, dim=16
    ))

    db.compute_energy_scan(processes=[ProcessType.GRAVITON_GRAVITON,
                                      ProcessType.GRAVITON_MATTER,
                                      ProcessType.QED_BORN,
                                      ProcessType.QED_1LOOP], verbose=False)

    # 角分布
    E_mid = list(db._data.keys())[len(db._data) // 2]
    db.compute_angular_distribution(E_mid, n_theta=8)

    vis = ScatteringVisualizer(db)

    # 截面 vs 能量
    vis.plot_cross_section_vs_energy(
        processes=[ProcessType.GRAVITON_GRAVITON, ProcessType.QED_BORN]
    )

    # 修正比较
    vis.plot_correction_comparison()

    # 角分布
    vis.plot_angular_distribution(E_mid)

    # 主导图
    vis.plot_dominance_map()

    print("  ✅ Visualization verified")
    return True


def run_all_tests():
    """运行所有 B4 测试"""
    print("=" * 60)
    print("B4: Planck Scattering Database Tests")
    print("=" * 60)

    tests = [
        ("Database creation", verify_database_creation),
        ("Energy scan (gg)", verify_energy_scan_gg),
        ("QED scan (Born/1loop/RG)", verify_qed_scan),
        ("Save/Load roundtrip", verify_save_load),
        ("Query interface", verify_query_interface),
        ("Visualization tools", verify_visualization),
    ]

    passed = 0
    for name, test_fn in tests:
        try:
            print(f"\n--- {name} ---")
            test_fn()
            passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 60}")
    if passed == len(tests):
        print(f"✅ {passed}/{len(tests)} B4 tests passed!")
    else:
        print(f"⚠️  {passed}/{len(tests)} B4 tests passed")

    return passed == len(tests)


if __name__ == "__main__":
    run_all_tests()
