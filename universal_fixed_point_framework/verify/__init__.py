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
