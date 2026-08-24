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
"""测试两弦法 Kerr 模式和效率优化。"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leaver_unified_solver import LeaverUnifiedSolver

def test(label, M, a, l, m, n, ref_re, ref_im, method='spectral_fast'):
    print(f'\n{"="*60}')
    print(f'  {label}')
    print(f'{"="*60}')
    solver = LeaverUnifiedSolver(M=M, a=a, s=-2)
    t0 = time.perf_counter()
    result = solver.solve(l=l, m=m, n=n, method=method)
    dt = time.perf_counter() - t0
    omega = result['omega']
    diff = abs(omega - complex(ref_re, -ref_im))
    print(f'  ω = {omega.real:.6f} {omega.imag:+.6f}i')
    print(f'  参考 = {ref_re:.6f} {ref_im:+.6f}i')
    print(f'  偏差 = {diff:.6f}')
    print(f'  残差 = {result["residual"]:.2e}')
    print(f'  LACI = {result.get("laci", "N/A"):.2f}')
    print(f'  物理 = {result.get("physical", "N/A")}')
    print(f'  方法 = {result.get("method", method)}')
    print(f'  耗时 = {dt*1000:.1f} ms')
    return omega, diff, dt

print('两弦法 (spectral_fast) Kerr 模式测试')
print('='*60)

# Test 1: Schwarzschild baseline
test('Schwarzschild 基模 (a=0, l=2,m=0,n=0)', 1.0, 0.0, 2, 0, 0, 0.373672, 0.088962)

# Test 2: Schwarzschild m=2
test('Schwarzschild 基模 (a=0, l=2,m=2,n=0)', 1.0, 0.0, 2, 2, 0, 0.373672, 0.088962)

# Test 3: Kerr a=0.5, m=0
test('Kerr (a=0.5, l=2,m=0,n=0)', 1.0, 0.5, 2, 0, 0, 0.355051, 0.095299)

# Test 4: Kerr a=0.5, m=2
test('Kerr (a=0.5, l=2,m=2,n=0)', 1.0, 0.5, 2, 2, 0, 0.524581, 0.088274)

# Test 5: Kerr a=0.9, m=2
test('Kerr (a=0.9, l=2,m=2,n=0)', 1.0, 0.9, 2, 2, 0, 0.584417, 0.087278)

# Test 6: Kerr a=0.7, m=2
test('Kerr (a=0.7, l=2,m=2,n=0)', 1.0, 0.7, 2, 2, 0, 0.532144, 0.080721)

print(f'\n{"="*60}')
print(f'  效率对比 (standard vs spectral_fast)')
print(f'{"="*60}')

for label, a, m in [('Kerr a=0.5,m=0', 0.5, 0), ('Kerr a=0.5,m=2', 0.5, 2),
                     ('Kerr a=0.9,m=2', 0.9, 2), ('Schwarz a=0,m=0', 0.0, 0)]:
    # Standard Newton
    s1 = LeaverUnifiedSolver(M=1.0, a=a, s=-2)
    t0 = time.perf_counter()
    r1 = s1.solve(l=2, m=m, n=0, method='auto')
    t1 = time.perf_counter() - t0

    # Spectral fast
    s2 = LeaverUnifiedSolver(M=1.0, a=a, s=-2)
    t0 = time.perf_counter()
    r2 = s2.solve(l=2, m=m, n=0, method='spectral_fast')
    t2 = time.perf_counter() - t0

    speedup = t1/t2 if t2 > 0 else float('inf')
    ratio = f'{speedup:.1f}x' if speedup >= 1 else f'{1/speedup:.1f}x (slower)'
    print(f'  {label:20s}: Newton={t1*1000:7.1f}ms  两弦法={t2*1000:7.1f}ms  ({ratio})')
