"""使用 qnm 包获取参考 QNM 频率"""
import numpy as np

print("=" * 70)
print("使用 qnm 包获取参考 QNM 频率")
print("=" * 70)
print()

try:
    import qnm
    from qnm import spinsequence
    
    # 下载缓存数据
    print("正在下载缓存数据...")
    qnm.download_data()
    print()
    
    # 测试用例
    test_cases = [
        (0.0, 2, 0, 0),
        (0.5, 2, 2, 0),
        (0.5, 2, 0, 0),
        (0.7, 2, 1, 0),
    ]
    
    print("--- qnm 包的 QNM 频率 ---")
    for a, l, m, n in test_cases:
        try:
            # 创建模式序列
            seq = spinsequence(s=-2, l=l, m=m, n=n)
            omega, A, C = seq(a, store_all=True)
            print(f"a={a}, l={l}, m={m}, n={n}:")
            print(f"  ω = {omega.real:.6f} {omega.imag:+.6f}i")
            print(f"  A = {A.real:.6f} {A.imag:+.6f}i")
            print()
        except Exception as e:
            print(f"a={a}, l={l}, m={m}, n={n}: 失败 - {e}")
            print()
    
    print()
    print("--- 手动使用径向连分数求根 ---")
    from qnm.radial import leaver_cf_inv_lentz
    from qnm.angular import C_and_sep_const_closest
    
    for a, l, m, n in test_cases[:2]:
        print(f"\na={a}, l={l}, m={m}, n={n}:")
        
        # 用近似方法找初始猜测
        omega_guess = complex(0.4, -0.1)
        if a == 0.0 and l == 2 and n == 0:
            omega_guess = complex(0.373672, -0.088962)
        elif a == 0.5 and l == 2 and m == 2 and n == 0:
            omega_guess = complex(0.5, -0.1)
        
        # Newton-Raphson
        omega = omega_guess
        for i in range(50):
            A0 = l*(l+1) - (-2)*(-2+1)
            A, _ = C_and_sep_const_closest(A0, s=-2, c=a*omega, m=m, l_max=20)
            cf, err, n_frac = leaver_cf_inv_lentz(omega=omega, a=a, s=-2, m=m, A=A, n_inv=n)
            
            if abs(cf) < 1e-10:
                print(f"  收敛于第 {i+1} 步")
                break
            
            delta = 1e-6
            A2, _ = C_and_sep_const_closest(A0, s=-2, c=a*(omega+delta), m=m, l_max=20)
            cf2, err2, _ = leaver_cf_inv_lentz(omega=omega+delta, a=a, s=-2, m=m, A=A2, n_inv=n)
            dcf = (cf2 - cf) / delta
            
            if abs(dcf) > 1e-15:
                omega -= cf / dcf
        
        A_final, _ = C_and_sep_const_closest(A0, s=-2, c=a*omega, m=m, l_max=20)
        cf_final, _, _ = leaver_cf_inv_lentz(omega=omega, a=a, s=-2, m=m, A=A_final, n_inv=n)
        print(f"  ω = {omega.real:.6f} {omega.imag:+.6f}i")
        print(f"  |CF| = {abs(cf_final):.2e}")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
