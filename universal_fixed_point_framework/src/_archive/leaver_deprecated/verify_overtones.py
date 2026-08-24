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

"""验证 Schwarzschild 不同泛音数"""
import numpy as np
from leaver_corrected_solver import CorrectedLeaverQNMSolver

print("=" * 70)
print("验证 Schwarzschild 不同泛音数")
print("=" * 70)
print()

solver = CorrectedLeaverQNMSolver(M=1.0, a=0.0, s=-2, max_iter=300)

# Berti 参考值
berti_ref = {
    (2, 0, 0): complex(0.373672, -0.0889623),
    (2, 0, 1): complex(0.346711, -0.273915),
    (2, 0, 2): complex(0.301057, -0.478277),
    (3, 0, 0): complex(0.599443, -0.092703),
    (3, 0, 1): complex(0.582644, -0.281303),
}

for (l, m, n), ref in berti_ref.items():
    result = solver.solve(l=l, m=m, n=n, tol=1e-8)
    omega = result["omega"]
    rel_err = abs(omega - ref) / abs(ref)
    
    print(f"l={l}, m={m}, n={n}:")
    print(f"  我们: ω = {omega.real:.6f} {omega.imag:+.6f}i")
    print(f"  参考: ω = {ref.real:.6f} {ref.imag:+.6f}i")
    print(f"  相对误差: {rel_err:.6f}")
    print(f"  残差: {result['residual']:.2e}")
    print(f"  物理性: {'✅' if result['is_physical'] else '❌'}")
    print()

# 测试 n_inv 对结果的影响
print("--- n_inv 对结果的影响 (l=2, m=0) ---")
l, m = 2, 0
omega_guess = complex(0.37, -0.09)
for n_inv in range(5):
    result = solver._newton_raphson(omega_guess, l, m, 0.0, n_inv=n_inv, tol=1e-10)
    print(f"  n_inv={n_inv}: ω = {result['omega'].real:.6f} {result['omega'].imag:+.6f}i, |CF|={result['residual']:.2e}")
