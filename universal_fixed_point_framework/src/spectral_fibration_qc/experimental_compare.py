"""
experimental_compare.py — 实验数据对比模块
=============================================
将谱纤维拆分包各层的计算结果与实验观测数据对比，
提供偏差分析和一致性评估。
"""

import numpy as np

from .layer_base import FiberLayer, FibrationChain
from .layer_reac import ReacLayer
from .layer_corr import CorrLayer
from .layer_vib import VibLayer
from .layer_intraionic import IntraIonicLayer
from .layer_ionic import IonicLayer
from .layer_solv import SolvLayer
from .layer_spin import SpinLayer
from .utils import convert_numpy


def compare_with_experiment(layers, experimental_data, layer_name=None):
    """将纤维层计算结果与实验数据对比。

    对指定（或所有）层，将计算的谱间隙、耦合强度等
    与实验参考值进行比较，返回偏差统计。

    Parameters
    ----------
    layers : list of FiberLayer
        待比较的纤维层列表。
    experimental_data : dict
        实验参考数据，格式为：
        {
            "layer_name": {
                "observable": value,
                "observable_err": uncertainty,
            }
        }
    layer_name : str or None
        指定层名。为 None 时比较所有可匹配的层。

    Returns
    -------
    comparison : dict
        对比结果，包含每层的：
        - 理论值列表
        - 实验值列表
        - 偏差和 χ² 统计
    """
    results = {}

    for layer in layers:
        name = layer.name
        if layer_name is not None and name != layer_name:
            continue
        if name not in experimental_data:
            continue

        exp_dict = experimental_data[name]
        summary = layer.get_summary()

        layer_results = []
        for obs_key, exp_val in exp_dict.items():
            if obs_key in summary:
                theory_val = summary[obs_key]
                exp_err = exp_val.get("error", 0.0) if isinstance(
                    exp_val, dict) else 0.0
                exp_val_clean = exp_val.get("value", exp_val) if isinstance(
                    exp_val, dict) else exp_val

                deviation = float(theory_val) - float(exp_val_clean)
                chi2 = (deviation ** 2) / (exp_err ** 2 + 1e-30)

                layer_results.append({
                    "observable": obs_key,
                    "theory": float(theory_val),
                    "experiment": float(exp_val_clean),
                    "experiment_error": float(exp_err),
                    "deviation": float(deviation),
                    "chi_squared": float(chi2),
                })

        if layer_results:
            results[name] = layer_results

    return _summarize_comparison(results)


def _summarize_comparison(raw_comparison):
    """汇总对比结果为结构化报告。

    Parameters
    ----------
    raw_comparison : dict
        compare_with_experiment 的原始输出。

    Returns
    -------
    summary : dict
        包含总 χ²、每层 χ² 和偏差统计的结构化报告。
    """
    summary = {"layers": {}}
    total_chi2 = 0.0
    n_obs = 0

    for layer_name, obs_list in raw_comparison.items():
        layer_chi2 = sum(o["chi_squared"] for o in obs_list)
        n_obs += len(obs_list)
        total_chi2 += layer_chi2

        deviations = [o["deviation"] for o in obs_list]
        summary["layers"][layer_name] = {
            "n_observables": len(obs_list),
            "chi_squared": layer_chi2,
            "mean_deviation": float(np.mean(deviations)) if deviations else 0.0,
            "rmse": float(np.sqrt(np.mean(np.array(deviations) ** 2)))
            if deviations else 0.0,
            "details": convert_numpy(obs_list),
        }

    summary["total_chi_squared"] = total_chi2
    summary["n_total_observables"] = n_obs
    summary["reduced_chi_squared"] = (
        total_chi2 / max(n_obs, 1)
    )
    return summary


def build_default_experimental_data():
    """构建默认的实验参考数据集。

    包含来自文献的典型参考值，供快速对比使用。

    Returns
    -------
    data : dict
        按层名分组的实验参考数据。
    """
    return {
        "Reac": {
            "spectral_gap": {"value": 6.0, "error": 0.5},
        },
        "Corr": {
            "min_gap": {"value": 0.0, "error": 0.1},
        },
        "Vib": {
            "max_freq_eV": {"value": 0.37, "error": 0.02},
        },
        "IntraIonic": {
            "l_corr_angstrom": {"value": 0.8, "error": 0.15},
            "beta_per_site": {"value": 0.5, "error": 0.1},
        },
        "Ionic": {
            "J_CT_eq": {"value": 0.8, "error": 0.2},
        },
        "Solv": {
            "epsilon_r": {"value": 78.4, "error": 1.0},
        },
        "Spin": {
            "delta_SOC": {"value": 0.02, "error": 0.01},
        },
    }
