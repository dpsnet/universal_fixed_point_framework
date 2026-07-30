"""
verify — UFPF 范畴理论绝对性验证套件。

一键运行::

    from verify.run_all import run_all
    results = run_all()

或命令行::

    python -m verify.run_all
"""

from . import checks
from .run_all import run_all, print_report
