# -*- coding: utf-8 -*-
"""Phase 71 阶段2 翻译检验 T5v2（命题2.2 精确验证）：
断言：剥离振幅的连续依赖性完全通过 sg 符号结构介导——无独立连续自由度。
方法：微扰 zbar（保持动量守恒）后，振幅变 ⇔ 全部子块对符号结构变（一一对应）。
"""
import sys, random
sys.path.insert(0, 'E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts')
import paperX_single_minus_numerics as num
import paperX_single_minus_bg_recursion as bg

def sign_of(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)

def all_block_signs(om, zb, n):
    """全部非空子块对的 [Σλ_A, Σλ_B] 符号（完备符号结构）"""
    signs = []
    # 所有非空、不相交、A 在 B 前的子块对（覆盖 sg 出现的所有组合）
    for a in range(1, n):
        for b in range(a+1, n+1):
            A = list(range(a, b))
            for c in range(b, n+1):
                B = list(range(b, c))
                if not B: continue
                s = sum(om[i]*om[j]*(zb[i]-zb[j]) for i in A for j in B)
                signs.append(sign_of(s))
    # 单块 vs 单块相邻对（sg_pair 用）
    for i in range(n-1):
        s = om[i]*om[i+1]*(zb[i]-zb[i+1])
        signs.append(sign_of(s))
    return tuple(signs)

def run_T5v2(n, samples=600):
    rng = random.Random(777 + n*1000)
    n_agree = 0      # 振幅变⇔符号变 一致
    n_amp_changed = 0
    n_sig_changed = 0
    for _ in range(samples):
        om, zb = num.gen_R1_momentum(n)
        a0 = bg.A_BG(n, om, zb)
        s0 = all_block_signs(om, zb, n)
        # 微扰 zbar_{0..n-2}，重解最后一个满足动量守恒
        gaps = [abs(zb[i+1]-zb[i]) for i in range(n-2)]
        if not gaps: continue
        dmax = 0.25 * min(gaps)
        zb2 = list(zb)
        for i in range(n-1):
            zb2[i] += rng.uniform(-dmax, dmax)
        S = sum(om[i]*zb2[i] for i in range(n-1))
        zb2[n-1] = -S/om[n-1]
        a1 = bg.A_BG(n, om, zb2)
        s1 = all_block_signs(om, zb2, n)
        amp_changed = (abs(a0-a1) > 1e-9)
        sig_changed = (s0 != s1)
        if amp_changed: n_amp_changed += 1
        if sig_changed: n_sig_changed += 1
        if amp_changed == sig_changed: n_agree += 1
    return n_agree, n_amp_changed, n_sig_changed

print("="*70)
print("T5v2: 振幅变 ⇔ 符号结构变（一一对应，命题2.2强验证）")
print("="*70)
for n in (3,4,5,6):
    agree, amp_ch, sig_ch = run_T5v2(n)
    print(f"n={n}: 一致={agree}/600  振幅变={amp_ch}  符号变={sig_ch}")
