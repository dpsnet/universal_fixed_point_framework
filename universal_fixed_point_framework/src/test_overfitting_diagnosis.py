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
test_overfitting_diagnosis.py

验证 overfitting_diagnosis.py 对 Rec/Spec 对象的统一诊断接口。
"""

from __future__ import annotations

import numpy as np

from rec_category import RecObject
from spec_category import PositiveSpectralObject
from overfitting_diagnosis import diagnose, report


def build_test_rec_object() -> RecObject:
    """构造一个简单的 Rec 对象用于诊断。"""
    K = np.array([[0.9, 0.9], [0.1, 0.1]])  # 列随机
    return RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=K,
        metadata={"test": True},
    )


def build_test_spectral_object() -> PositiveSpectralObject:
    """构造一个简单的 Spec 对象用于诊断。"""
    return PositiveSpectralObject(operator_A=np.diag([0.0, 0.5, 1.0]))


def test_diagnose_rec():
    print("\n[测试 1] 对 RecObject 诊断")
    rec = build_test_rec_object()
    result = diagnose(rec)
    assert result["object_type"] == "RecObject"
    assert "laci" in result
    assert result["risk_level"] in {"low", "medium", "high"}
    print(f"  LACI = {result['laci']:.4f}, risk = {result['risk_level']}")
    print("  通过")


def test_diagnose_spec():
    print("\n[测试 2] 对 PositiveSpectralObject 诊断")
    spec = build_test_spectral_object()
    result = diagnose(spec)
    assert result["object_type"] == "PositiveSpectralObject"
    assert "laci" in result
    assert result["risk_level"] in {"low", "medium", "high"}
    print(f"  LACI = {result['laci']:.4f}, risk = {result['risk_level']}")
    print("  通过")


def test_report():
    print("\n[测试 3] 生成可读报告")
    rec = build_test_rec_object()
    text = report(rec)
    assert "LACI" in text
    assert "风险等级" in text
    print(text)
    print("  通过")


def main():
    print("=" * 60)
    print("过拟合诊断模块验证")
    print("=" * 60)

    test_diagnose_rec()
    test_diagnose_spec()
    test_report()

    print("\n" + "=" * 60)
    print("所有过拟合诊断测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
