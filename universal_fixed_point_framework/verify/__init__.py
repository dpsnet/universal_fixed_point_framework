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
# 本文件中 UFPF 相关引用数量：4
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
verify — UFPF 范畴理论绝对性验证套件。

更名计划通知（2026-08-24）：
框架名称将从 UFPF (Universal Fixed Point Framework) 更名为
MUFPF (Meta-Universal Fixed-Point Functorial Framework)，
以解决与 IEEE 生物图像识别框架的命名冲突。
当前代码中的 UFPF 引用将在更名计划确认后统一修改。
详见 roadmap/mu_renaming_plan.md

一键运行::

    from verify.run_all import run_all
    results = run_all()

或命令行::

    python -m verify.run_all
"""

from . import checks
from .run_all import run_all, print_report
