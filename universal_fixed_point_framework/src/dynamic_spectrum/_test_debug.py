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
"""调试 Kerr 求解器：检查初始猜测和 Newton 收敛。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leaver_unified_solver import LeaverUnifiedSolver

solver = LeaverUnifiedSolver(M=1.0, a=0.5, s=-2)

# 检查初始猜测
guesses = solver._initial_guesses(2, 2, 0)
print("Kerr a=0.5, l=2, m=2, n=0 的初始猜测:")
for i, g in enumerate(guesses):
    print(f"  [{i}] ω = {g.real:.6f} {g.imag:+.6f}i")

# 从每个猜测做 Newton 求解
print("\n从各猜测开始的 Newton 收敛结果:")
for i, guess in enumerate(guesses):
    try:
        omega, res = solver._newton_solve(guess, 2, 2, max_iter=30)
        # LACI
        laci = solver.laci.evaluate(omega, 2, 2, a=0.5)
        print(f"  [{i}] ω = {omega.real:.6f} {omega.imag:+.6f}i  ρ={res:.2e}  LACI={laci.laci:.1f}  ✓物理={laci.physical}")
    except Exception as e:
        print(f"  [{i}] 失败: {e}")

# 直接测试 Berti Kerr 初始猜测
print("\nBerti Kerr 公式计算:")
from leaver_unified_solver import LeaverUnifiedSolver
berti = LeaverUnifiedSolver._berti_kerr_fit(2, 2, 0.5)
print(f"  ω_berti = {berti.real:.6f} {berti.imag:+.6f}i")
print(f"  期望值  = 0.524581 -0.088274i")
print(f"  残差 f(ω) = {solver.residual.full_residual(berti, 2, 2):.6e}")
