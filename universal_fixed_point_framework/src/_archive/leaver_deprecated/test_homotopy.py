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

"""精细同伦延拓测试"""
import numpy as np
from leaver_corrected_solver import CorrectedLeaverQNMSolver

print("=" * 70)
print("精细同伦延拓测试")
print("=" * 70)
print()

# 测试 a=0.5, l=2, m=0
a_target = 0.5
l, m, n = 2, 0, 0

print(f"目标: a={a_target}, l={l}, m={m}, n={n}")
print()

# 精细的同伦延拓
solver = CorrectedLeaverQNMSolver(M=1.0, a=a_target, s=-2, max_iter=300)

# 手动进行同伦延拓，记录每一步
n_steps = 200
a_vals = np.linspace(0.0, a_target, n_steps + 1)

omega_current = complex(0.373672, -0.0889623)  # Schwarzschild n=0

print("同伦延拓路径:")
print(f"  初始: a=0.0, ω = {omega_current.real:.6f} {omega_current.imag:+.6f}i")

for i, a_val in enumerate(a_vals[1:], 1):
    result = solver._newton_raphson(omega_current, l, m, a_val, n_inv=n, tol=1e-10)
    omega_current = result["omega"]
    
    if not result["converged"]:
        print(f"  第 {i} 步 (a={a_val:.3f}): 收敛失败!")
        break
    
    if i % 40 == 0 or i == n_steps:
        print(f"  第 {i} 步 (a={a_val:.3f}): ω = {omega_current.real:.6f} {omega_current.imag:+.6f}i, |CF|={result['residual']:.2e}")

print()
print(f"最终结果: ω = {omega_current.real:.6f} {omega_current.imag:+.6f}i")
print(f"参考值 (Berti): ω = 0.355051 -0.095299i")
print()

# 让我们试试从另一个初始猜测出发
print("--- 从另一个初始猜测出发 ---")
other_guesses = [
    complex(0.35, -0.095),
    complex(0.36, -0.10),
    complex(0.34, -0.09),
    complex(0.38, -0.08),
]

for guess in other_guesses:
    result = solver._newton_raphson(guess, l, m, a_target, n_inv=n, tol=1e-10)
    print(f"  初始猜测 {guess.real:.3f}{guess.imag:+.3f}i → {result['omega'].real:.6f}{result['omega'].imag:+.6f}i, |CF|={result['residual']:.2e}")

print()

# 测试 a=0.5, l=2, m=2
print("--- a=0.5, l=2, m=2 ---")
l, m, n = 2, 2, 0

# 从 Schwarzschild 出发（m=0）然后同伦 m
print("先同伦 a，再同伦 m:")
a_val = 0.5

# 第一步: a=0, m=0 → a=0.5, m=0
omega_a = complex(0.373672, -0.0889623)
n_steps_a = 100
a_steps = np.linspace(0.0, a_val, n_steps_a + 1)

for ai in a_steps[1:]:
    result = solver._newton_raphson(omega_a, l, 0, ai, n_inv=n, tol=1e-10)
    omega_a = result["omega"]
    if not result["converged"]:
        print(f"  a 同伦失败在 a={ai}")
        break

print(f"  a=0.5, m=0: ω = {omega_a.real:.6f} {omega_a.imag:+.6f}i")

# 第二步: m=0 → m=2
omega_m = omega_a
n_steps_m = 100
m_steps = np.linspace(0.0, 2.0, n_steps_m + 1)

for mi in m_steps[1:]:
    m_int = int(round(mi))
    result = solver._newton_raphson(omega_m, l, m_int, a_val, n_inv=n, tol=1e-10)
    omega_m = result["omega"]
    if not result["converged"]:
        print(f"  m 同伦失败在 m={mi}")
        break

print(f"  a=0.5, m=2: ω = {omega_m.real:.6f} {omega_m.imag:+.6f}i")
print(f"  参考值 (Berti): ω = 0.495007 -0.093885i")
