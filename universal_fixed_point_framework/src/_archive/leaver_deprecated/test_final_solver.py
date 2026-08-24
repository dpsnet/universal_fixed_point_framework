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

"""快速测试最终求解器"""
import sys
sys.path.insert(0, 'src')
from leaver_final_solver import LeaverFinalSolver

# 测试 Schwarzschild a=0, l=2, m=0
solver = LeaverFinalSolver(M=1.0, a=0.0, s=-2, max_iter=300)
result = solver.solve(l=2, m=0, n=0)

ref_re, ref_im = 0.373672, -0.088962

print('=== Schwarzschild a=0, l=2, m=0, n=0 ===')
print(f'求解: omega = {result["omega"].real:.6f} {result["omega"].imag:.6f}i')
print(f'参考: omega = {ref_re:.6f} {ref_im:.6f}i')
print(f'偏差: DeltaRe = {abs(result["omega"].real - ref_re):.2e}, DeltaIm = {abs(result["omega"].imag - ref_im):.2e}')
print(f'残差: {result["residual"]:.2e}')
print(f'LACI: {result["laci"]:.2f}')
print(f'物理性: {"OK" if result["physical"] else "NO"}')
print(f'候选根数: {result["n_candidates"]}')
