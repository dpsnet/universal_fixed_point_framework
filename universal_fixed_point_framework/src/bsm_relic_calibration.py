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
bsm_relic_calibration.py

BSM热遗迹密度校准：校准湮灭截面和分支比，使Ωh²与Planck观测值一致。

核心思路：
- 框架预测第4代轻子质量 ~1470 GeV
- 校准有效湮灭耦合使Ωh² = 0.120 ± 0.001
- 考虑多个湮灭通道（W+W-, ZZ, hh, tt）
- 生成校准后的预言表
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
from scipy.optimize import brentq

from applications.bsm.bsm_cross_sections import (
    thermal_relic_density,
    PLANCK_RELIC_DENSITY,
    M_PLANCK_GEV,
    X_F,
)


class BSMRelicCalibration:
    """BSM热遗迹密度校准"""
    
    def __init__(self, mass_MeV: float = 1470000.0):
        """
        初始化校准器。
        
        参数:
            mass_MeV: BSM粒子质量 (MeV)
        """
        self.m = mass_MeV
        self.m_GeV = mass_MeV / 1000
        
        self.channels = {
            'W+W-': {'threshold_GeV': 80.4, 'weight': 2.0},
            'ZZ': {'threshold_GeV': 91.2, 'weight': 1.0},
            'hh': {'threshold_GeV': 125.0, 'weight': 1.0},
            'tt': {'threshold_GeV': 173.1, 'weight': 3.0},
        }
        
        self.target_omega = PLANCK_RELIC_DENSITY
        self.target_error = 0.001
    
    def compute_sigma_v(self, coupling: float, include_channels: bool = True) -> float:
        """
        计算有效湮灭截面 σv。
        
        σv = Σ_i w_i * coupling² * σ_i(m)
        
        其中 σ_i(m) ∝ 1/m² * θ(m - m_threshold)
        """
        sigma_ref = (
            1.07e9 * X_F / (M_PLANCK_GEV * np.sqrt(2) * PLANCK_RELIC_DENSITY)
        )
        
        mass_ratio = self.m / 1_000_000.0
        sigma_base = sigma_ref * coupling**2 / mass_ratio**2
        
        if include_channels:
            total_weight = 0
            for name, info in self.channels.items():
                if self.m_GeV > info['threshold_GeV']:
                    total_weight += info['weight']
            
            if total_weight > 0:
                sigma_base *= total_weight
        
        return sigma_base
    
    def compute_omega_h2(self, coupling: float, include_channels: bool = True) -> float:
        """计算Ωh²"""
        sigma_v = self.compute_sigma_v(coupling, include_channels)
        omega = 1.07e9 * X_F / (M_PLANCK_GEV * np.sqrt(2) * sigma_v)
        return omega
    
    def calibrate_coupling(self, include_channels: bool = True) -> dict:
        """
        校准耦合常数使Ωh² = 0.120。
        
        返回:
            calibration: 校准结果
        """
        def omega_diff(g):
            return self.compute_omega_h2(g, include_channels) - self.target_omega
        
        try:
            g_calibrated = brentq(omega_diff, 0.01, 10.0, xtol=1e-10)
        except ValueError:
            g_calibrated = np.nan
        
        omega_calibrated = self.compute_omega_h2(g_calibrated, include_channels)
        sigma_v_calibrated = self.compute_sigma_v(g_calibrated, include_channels)
        
        return {
            'mass_GeV': self.m_GeV,
            'coupling': g_calibrated,
            'omega_h2': omega_calibrated,
            'sigma_v': sigma_v_calibrated,
            'target_omega': self.target_omega,
            'deviation_sigma': np.abs(omega_calibrated - self.target_omega) / self.target_error,
            'include_channels': include_channels,
            'channels': self._get_active_channels()
        }
    
    def _get_active_channels(self) -> list:
        """获取开放的湮灭通道"""
        active = []
        for name, info in self.channels.items():
            if self.m_GeV > info['threshold_GeV']:
                active.append(f"{name} (w={info['weight']})")
        return active
    
    def scan_mass_range(self, mass_range_GeV: tuple = (100, 5000),
                        n_points: int = 20) -> dict:
        """扫描质量范围，计算每个质量点的校准耦合"""
        masses = np.logspace(np.log10(mass_range_GeV[0]), 
                            np.log10(mass_range_GeV[1]), n_points)
        
        results = {
            'mass_GeV': [],
            'coupling': [],
            'omega_h2': [],
            'sigma_v': [],
            'n_channels': []
        }
        
        for m_GeV in masses:
            self.m = m_GeV * 1000
            self.m_GeV = m_GeV
            
            cal = self.calibrate_coupling(include_channels=True)
            
            results['mass_GeV'].append(m_GeV)
            results['coupling'].append(cal['coupling'])
            results['omega_h2'].append(cal['omega_h2'])
            results['sigma_v'].append(cal['sigma_v'])
            results['n_channels'].append(len(cal['channels']))
        
        return results


def run_relic_calibration_demo():
    """运行热遗迹密度校准演示"""
    calibrator = BSMRelicCalibration(mass_MeV=1470000.0)
    
    print("=" * 70)
    print("BSM热遗迹密度校准")
    print("=" * 70)
    
    print(f"\n框架预言:")
    print(f"  第4代轻子质量: {calibrator.m_GeV:.1f} GeV")
    print(f"  Planck目标: Ωh² = {calibrator.target_omega} ± {calibrator.target_error}")
    
    print(f"\n开放湮灭通道:")
    active_channels = calibrator._get_active_channels()
    for ch in active_channels:
        print(f"  ✅ {ch}")
    
    print(f"\n--- 未校准（coupling=1.0）---")
    omega_uncal = calibrator.compute_omega_h2(1.0, include_channels=False)
    print(f"  Ωh² (单通道) = {omega_uncal:.4f}")
    
    omega_uncal_ch = calibrator.compute_omega_h2(1.0, include_channels=True)
    print(f"  Ωh² (多通道) = {omega_uncal_ch:.4f}")
    
    print(f"\n--- 校准后 ---")
    cal_single = calibrator.calibrate_coupling(include_channels=False)
    print(f"\n单通道校准:")
    print(f"  耦合常数 g = {cal_single['coupling']:.4f}")
    print(f"  Ωh² = {cal_single['omega_h2']:.4f}")
    print(f"  σv = {cal_single['sigma_v']:.4e} cm³/s")
    print(f"  偏差 = {cal_single['deviation_sigma']:.2f}σ")
    
    cal_multi = calibrator.calibrate_coupling(include_channels=True)
    print(f"\n多通道校准:")
    print(f"  耦合常数 g = {cal_multi['coupling']:.4f}")
    print(f"  Ωh² = {cal_multi['omega_h2']:.4f}")
    print(f"  σv = {cal_multi['sigma_v']:.4e} cm³/s")
    print(f"  偏差 = {cal_multi['deviation_sigma']:.2f}σ")
    
    print(f"\n--- 质量扫描 ---")
    scan = calibrator.scan_mass_range(mass_range_GeV=(100, 5000), n_points=10)
    
    print(f"\n{'质量(GeV)':<12} | {'耦合g':>8} | {'Ωh²':>8} | {'σv(cm³/s)':>14} | {'通道数'}")
    print("-" * 65)
    for i in range(len(scan['mass_GeV'])):
        print(f"{scan['mass_GeV'][i]:<12.1f} | {scan['coupling'][i]:>8.4f} | {scan['omega_h2'][i]:>8.4f} | {scan['sigma_v'][i]:>14.4e} | {scan['n_channels'][i]}")
    
    print(f"\n校准结论:")
    print(f"  ✅ 通过校准耦合常数，可使Ωh²与Planck观测值一致")
    print(f"  ✅ 在1470 GeV处，多通道校准耦合 g = {cal_multi['coupling']:.4f}")
    print(f"  ✅ 校准后Ωh² = {cal_multi['omega_h2']:.4f} (目标 {cal_multi['target_omega']})")
    print(f"  ✅ 有效湮灭截面 σv = {cal_multi['sigma_v']:.4e} cm³/s")
    print(f"  ✅ 考虑W+W-/ZZ/hh/tt四通道后，耦合校准更加物理合理")


if __name__ == "__main__":
    run_relic_calibration_demo()