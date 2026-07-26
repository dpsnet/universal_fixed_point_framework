#!/usr/bin/env python3
"""临时截断收敛性测试脚本。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dynamic_spectrum"))
from _dirac_polynomial_solver import DiracPolynomialSolver, verify_at_reference, verify_n_convergence, test_qnm_finding

verify_at_reference()
verify_n_convergence()
test_qnm_finding()
