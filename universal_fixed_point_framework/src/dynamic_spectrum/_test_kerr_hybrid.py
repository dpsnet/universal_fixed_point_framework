#!/usr/bin/env python3
"""测试两弦法混合策略 Kerr 模式。"""
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
    ok = diff < 0.03
    print(f'  ω = {omega.real:.6f} {omega.imag:+.6f}i')
    print(f'  参考 = {ref_re:.6f} {ref_im:+.6f}i')
    print(f'  偏差 = {diff:.6f}  {"✅" if ok else "❌"}')
    print(f'  残差 = {result["residual"]:.2e}')
    print(f'  方法 = {result.get("method", method)}')
    print(f'  两弦法验证 = {"✅" if result.get("fast_validated") else "❌"}')
    print(f'  耗时 = {dt*1000:.1f} ms')
    return omega, diff, dt, ok

print('两弦法混合策略 Kerr 模式综合测试')
print('='*60)

results = []
results.append(test('Schwarzschild (a=0, l=2,m=0,n=0)', 1.0, 0.0, 2, 0, 0, 0.373672, 0.088962))
results.append(test('Schwarzschild (a=0, l=2,m=2,n=0)', 1.0, 0.0, 2, 2, 0, 0.373672, 0.088962))
results.append(test('Kerr (a=0.5, l=2,m=0,n=0)', 1.0, 0.5, 2, 0, 0, 0.355051, 0.095299))
results.append(test('Kerr (a=0.5, l=2,m=2,n=0)', 1.0, 0.5, 2, 2, 0, 0.524581, 0.088274))
results.append(test('Kerr (a=0.9, l=2,m=2,n=0)', 1.0, 0.9, 2, 2, 0, 0.584417, 0.087278))
results.append(test('Kerr (a=0.7, l=2,m=2,n=0)', 1.0, 0.7, 2, 2, 0, 0.532144, 0.080721))
results.append(test('Kerr (a=0.5, l=3,m=3,n=0)', 1.0, 0.5, 3, 3, 0, 0.760664, 0.089024))

print(f'\n{"="*60}')
print(f'  总结')
print(f'{"="*60}')
passed = sum(1 for _, _, _, ok in results if ok)
total = len(results)
print(f'  通过: {passed}/{total}')
for i, (label, *_) in enumerate([('Schwarz (a=0,m=0)',), ('Schwarz (a=0,m=2)',),
                                  ('Kerr (a=0.5,m=0)',), ('Kerr (a=0.5,m=2)',),
                                  ('Kerr (a=0.9,m=2)',), ('Kerr (a=0.7,m=2)',),
                                  ('Kerr (a=0.5,m=3)',)]):
    _, _, _, ok = results[i]
    print(f'  {label[0]:20s}: {"✅" if ok else "❌"}')

print(f'\n{"="*60}')
print(f'  效率对比 (标准 vs 两弦法混合)')
print(f'{"="*60}')

for label, a, m in [('Schwarz a=0,m=0', 0.0, 0), ('Kerr a=0.5,m=0', 0.5, 0),
                     ('Kerr a=0.5,m=2', 0.5, 2), ('Kerr a=0.9,m=2', 0.9, 2)]:
    # Standard Newton
    s1 = LeaverUnifiedSolver(M=1.0, a=a, s=-2)
    t0 = time.perf_counter()
    r1 = s1.solve(l=2, m=m, n=0, method='auto')
    t1 = time.perf_counter() - t0

    # Hybrid
    s2 = LeaverUnifiedSolver(M=1.0, a=a, s=-2)
    t0 = time.perf_counter()
    r2 = s2.solve(l=2, m=m, n=0, method='spectral_fast')
    t2 = time.perf_counter() - t0

    speedup = t1/t2 if t2 > 0 else float('inf')
    ratio = f'{speedup:.1f}x' if speedup >= 1 else f'{1/speedup:.1f}x (slower)'
    print(f'  {label:20s}: Newton={t1*1000:7.1f}ms  两弦法={t2*1000:7.1f}ms  ({ratio})')
