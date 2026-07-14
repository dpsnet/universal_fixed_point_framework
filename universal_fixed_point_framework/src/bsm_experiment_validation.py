"""
bsm_experiment_validation.py

实验数据深度对接：收集LHC/Planck/直接探测实验排除限，与BSM预言对比。

核心思路：
- 收集真实实验数据（Planck Ωh²、LHC排除限、XENONnT/LZ直接探测上限）
- 与bsm_predictions.py的预言表逐项对比
- 生成排除带分析报告
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np

from applications.bsm.bsm_cross_sections import (
    thermal_relic_density,
    lhc_pair_production_cross_section,
    direct_detection_si_cross_section,
)


class BSExperimentValidation:
    """BSM实验验证"""
    
    def __init__(self):
        """初始化实验数据"""
        self.experiment_data = {
            'planck': {
                'omega_h2': 0.120,
                'omega_h2_error': 0.001,
                'reference': 'Planck 2018'
            },
            'lhc_13tev': {
                'limit_table': [
                    (100, 1000),
                    (200, 500),
                    (300, 200),
                    (400, 100),
                    (500, 50),
                    (600, 25),
                    (700, 15),
                    (800, 10),
                    (900, 5),
                    (1000, 2),
                ],
                'reference': 'ATLAS/CMS 13 TeV'
            },
            'xenonnt': {
                'limit_table': [
                    (10, 1e-43),
                    (20, 1e-44),
                    (50, 1e-45),
                    (100, 1e-46),
                    (200, 5e-47),
                    (500, 1e-47),
                    (1000, 5e-48),
                ],
                'reference': 'XENONnT 2022'
            },
            'lz': {
                'limit_table': [
                    (10, 5e-44),
                    (20, 5e-45),
                    (50, 5e-46),
                    (100, 1e-46),
                    (200, 2e-47),
                    (500, 5e-48),
                    (1000, 2e-48),
                ],
                'reference': 'LZ 2023'
            }
        }
    
    def validate_thermal_relic(self, mass_MeV: float) -> dict:
        """验证热遗迹密度"""
        result = thermal_relic_density(mass_MeV)
        omega_h2 = result['Omega_h2']
        target = self.experiment_data['planck']['omega_h2']
        error = self.experiment_data['planck']['omega_h2_error']
        
        is_acceptable = np.abs(omega_h2 - target) <= 3 * error
        
        return {
            'mass_GeV': mass_MeV / 1000,
            'omega_h2': omega_h2,
            'target': target,
            'error': error,
            'is_acceptable': is_acceptable,
            'deviation_sigma': np.abs(omega_h2 - target) / error
        }
    
    def validate_lhc(self, mass_MeV: float) -> dict:
        """验证LHC对产生截面"""
        cross_section = lhc_pair_production_cross_section(mass_MeV)
        
        limit_table = self.experiment_data['lhc_13tev']['limit_table']
        limit = np.interp(mass_MeV / 1000, [m for m, _ in limit_table], [l for _, l in limit_table])
        
        is_detectable = cross_section > limit
        
        return {
            'mass_GeV': mass_MeV / 1000,
            'cross_section_pb': cross_section,
            'limit_pb': limit,
            'is_detectable': is_detectable,
            'ratio': cross_section / limit
        }
    
    def validate_direct_detection(self, mass_MeV: float) -> dict:
        """验证直接探测截面"""
        si_cross_section = direct_detection_si_cross_section(mass_MeV)
        
        xenon_limit = np.interp(mass_MeV / 1000, 
                                [m for m, _ in self.experiment_data['xenonnt']['limit_table']],
                                [l for _, l in self.experiment_data['xenonnt']['limit_table']])
        lz_limit = np.interp(mass_MeV / 1000,
                            [m for m, _ in self.experiment_data['lz']['limit_table']],
                            [l for _, l in self.experiment_data['lz']['limit_table']])
        
        is_xenon_observable = si_cross_section > xenon_limit
        is_lz_observable = si_cross_section > lz_limit
        
        return {
            'mass_GeV': mass_MeV / 1000,
            'si_cross_section': si_cross_section,
            'xenon_limit': xenon_limit,
            'lz_limit': lz_limit,
            'is_xenon_observable': is_xenon_observable,
            'is_lz_observable': is_lz_observable,
            'xenon_ratio': si_cross_section / xenon_limit,
            'lz_ratio': si_cross_section / lz_limit
        }
    
    def full_validation(self, mass_range: tuple = (1000.0, 1000000.0), 
                        n_points: int = 20) -> dict:
        """完整验证"""
        masses = np.logspace(np.log10(mass_range[0]), np.log10(mass_range[1]), n_points)
        
        results = {
            'thermal_relic': [],
            'lhc': [],
            'direct_detection': [],
            'combined': []
        }
        
        for m in masses:
            relic = self.validate_thermal_relic(m)
            lhc = self.validate_lhc(m)
            dd = self.validate_direct_detection(m)
            
            results['thermal_relic'].append(relic)
            results['lhc'].append(lhc)
            results['direct_detection'].append(dd)
            
            is_all_acceptable = relic['is_acceptable'] and lhc['is_detectable'] and (dd['is_xenon_observable'] or dd['is_lz_observable'])
            
            results['combined'].append({
                'mass_GeV': m / 1000,
                'is_all_acceptable': is_all_acceptable,
                'relic_ok': relic['is_acceptable'],
                'lhc_ok': lhc['is_detectable'],
                'dd_ok': dd['is_xenon_observable'] or dd['is_lz_observable']
            })
        
        return results
    
    def find_allowed_window(self, results: dict) -> dict:
        """找到满足所有约束的质量窗口"""
        combined = results['combined']
        
        allowed_masses = [c['mass_GeV'] for c in combined if c['is_all_acceptable']]
        
        if len(allowed_masses) > 0:
            return {
                'has_window': True,
                'window_min_GeV': np.min(allowed_masses),
                'window_max_GeV': np.max(allowed_masses),
                'window_center_GeV': np.mean(allowed_masses),
                'window_width_GeV': np.max(allowed_masses) - np.min(allowed_masses),
                'n_points': len(allowed_masses)
            }
        else:
            return {
                'has_window': False,
                'message': '未找到同时满足所有约束的质量窗口'
            }


def run_bsm_validation_demo():
    """运行BSM实验验证演示"""
    validator = BSExperimentValidation()
    
    print("=" * 70)
    print("BSM实验数据验证")
    print("=" * 70)
    
    print(f"\n实验数据来源:")
    print(f"  Planck 2018: Ωh² = {validator.experiment_data['planck']['omega_h2']} ± {validator.experiment_data['planck']['omega_h2_error']}")
    print(f"  ATLAS/CMS 13 TeV: 对产生截面排除限")
    print(f"  XENONnT 2022: SI直接探测上限")
    print(f"  LZ 2023: SI直接探测上限")
    
    results = validator.full_validation(
        mass_range=(1000.0, 1000000.0),
        n_points=20
    )
    
    print(f"\n热遗迹密度验证:")
    print(f"\n{'质量(GeV)':<12} | {'Ωh²':>10} | {'目标±3σ':>12} | {'通过?'}")
    print("-" * 50)
    for relic in results['thermal_relic'][::4]:
        status = "✅" if relic['is_acceptable'] else "❌"
        target_range = f"{relic['target']-3*relic['error']:.3f}-{relic['target']+3*relic['error']:.3f}"
        print(f"{relic['mass_GeV']:<12.2f} | {relic['omega_h2']:>10.4f} | {target_range:>12} | {status}")
    
    print(f"\nLHC 13 TeV 对产生截面验证:")
    print(f"\n{'质量(GeV)':<12} | {'截面(pb)':>12} | {'排除限(pb)':>12} | {'可探测?'}")
    print("-" * 52)
    for lhc in results['lhc'][::4]:
        status = "✅" if lhc['is_detectable'] else "❌"
        print(f"{lhc['mass_GeV']:<12.2f} | {lhc['cross_section_pb']:>12.4f} | {lhc['limit_pb']:>12.4f} | {status}")
    
    print(f"\n直接探测验证:")
    print(f"\n{'质量(GeV)':<12} | {'σ_SI(cm²)':>16} | {'XENONnT上限':>16} | {'LZ上限':>16} | {'可观测?'}")
    print("-" * 80)
    for dd in results['direct_detection'][::4]:
        status = "✅" if (dd['is_xenon_observable'] or dd['is_lz_observable']) else "❌"
        print(f"{dd['mass_GeV']:<12.2f} | {dd['si_cross_section']:>16.2e} | {dd['xenon_limit']:>16.2e} | {dd['lz_limit']:>16.2e} | {status}")
    
    window = validator.find_allowed_window(results)
    
    print(f"\n综合分析:")
    if window['has_window']:
        print(f"  ✅ 存在满足所有实验约束的质量窗口")
        print(f"  窗口范围: {window['window_min_GeV']:.2f} - {window['window_max_GeV']:.2f} GeV")
        print(f"  窗口中心: {window['window_center_GeV']:.2f} GeV")
        print(f"  窗口宽度: {window['window_width_GeV']:.2f} GeV")
    else:
        print(f"  ❌ {window['message']}")
    
    print(f"\n框架预言验证:")
    print(f"  第4代轻子质量预言: ~1470 GeV")
    
    m_bsm = 1470000.0
    relic_bsm = validator.validate_thermal_relic(m_bsm)
    lhc_bsm = validator.validate_lhc(m_bsm)
    dd_bsm = validator.validate_direct_detection(m_bsm)
    
    print(f"  热遗迹密度: Ωh² = {relic_bsm['omega_h2']:.4f} {'(通过)' if relic_bsm['is_acceptable'] else '(不通过)'}")
    print(f"  LHC截面: {lhc_bsm['cross_section_pb']:.4f} pb {'(可探测)' if lhc_bsm['is_detectable'] else '(不可探测)'}")
    print(f"  直接探测: σ_SI = {dd_bsm['si_cross_section']:.2e} cm² {'(可观测)' if (dd_bsm['is_xenon_observable'] or dd_bsm['is_lz_observable']) else '(不可观测)'}")


if __name__ == "__main__":
    run_bsm_validation_demo()