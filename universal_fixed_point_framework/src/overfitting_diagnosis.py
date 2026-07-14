"""
overfitting_diagnosis.py

对任意 RecObject 或 PositiveSpectralObject 输出统一的 LACI 过拟合诊断报告。

本模块是 `attractor_distance.py` 的高层包装，将局部吸引子捕获指数（LACI）
转化为面向用户的诊断信息。它属于 P1 阶段「框架可用性」工具链的一部分。
"""

from __future__ import annotations

from typing import Union

from rec_category import RecObject
from spec_category import PositiveSpectralObject
from attractor_distance import (
    diagnose_rec_object_from_instance,
    diagnose_spectral_object,
)


Diagnosable = Union[RecObject, PositiveSpectralObject]


def diagnose(obj: Diagnosable) -> dict:
    """
    对给定的 RecObject 或 PositiveSpectralObject 计算 LACI 诊断。

    参数
    ----------
    obj : RecObject | PositiveSpectralObject
        待诊断的抽象框架对象。

    返回
    -------
    dict
        包含 LACI 各分量、风险等级与解释的诊断报告。
    """
    if isinstance(obj, RecObject):
        metrics = diagnose_rec_object_from_instance(obj)
        obj_type = "RecObject"
    elif isinstance(obj, PositiveSpectralObject):
        metrics = diagnose_spectral_object(obj)
        obj_type = "PositiveSpectralObject"
    else:
        raise TypeError(
            "diagnose 仅支持 RecObject 或 PositiveSpectralObject，"
            f"收到 {type(obj).__name__}"
        )

    risk = metrics["risk_level"]
    interpretation = _interpret_risk(risk)

    return {
        "object_type": obj_type,
        "laci": metrics["laci"],
        "residual": metrics["residual"],
        "dispersion": metrics["dispersion"],
        "spectral_gap": metrics["spectral_gap"],
        "perturbation_sensitivity": metrics["perturbation_sensitivity"],
        "risk_level": risk,
        "interpretation": interpretation,
    }


def report(obj: Diagnosable) -> str:
    """
    生成可读的 LACI 诊断报告字符串。
    """
    result = diagnose(obj)
    lines = [
        "=" * 50,
        "局部吸引子捕获（LACI）诊断报告",
        "=" * 50,
        f"对象类型: {result['object_type']}",
        f"LACI 指数: {result['laci']:.6f}",
        f"风险等级: {result['risk_level'].upper()}",
        "-" * 50,
        "分量详情:",
        f"  残差 ρ           = {result['residual']:.6e}",
        f"  分散度 Δ         = {result['dispersion']:.6e}",
        f"  谱间隙 γ         = {result['spectral_gap']:.6e}",
        f"  扰动敏感度 χ    = {result['perturbation_sensitivity']:.6e}",
        "-" * 50,
        "解释:",
        f"  {result['interpretation']}",
        "=" * 50,
    ]
    return "\n".join(lines)


def _interpret_risk(risk: str) -> str:
    """根据风险等级返回人类可读解释。"""
    interpretations = {
        "low": (
            "LACI 较低，数值解接近唯一不动点，局部吸引子捕获风险小，"
            "模型泛化能力较好。"
        ),
        "medium": (
            "LACI 中等，存在多个吸引子盆地或吸引子边界较敏感，"
            "建议增加初始点多样性或约束参数空间。"
        ),
        "high": (
            "LACI 较高，数值解很可能被困在局部吸引子，过拟合风险高，"
            "建议重新抽象到全域不动点方程。"
        ),
    }
    return interpretations.get(risk, "未知风险等级。")
