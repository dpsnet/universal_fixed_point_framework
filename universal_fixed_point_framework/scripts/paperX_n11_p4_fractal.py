# -*- coding: utf-8 -*-
"""P4：蜂窝分形多尺度检验（Phase 78）
- A=0 孔洞占比随 n 的标度（非零率几何衰减——孔洞分形）
- 分形维数估算：log(非零率) vs n 斜率——测度维数
- 块长分布幂律：n=11 退化区（A=0）的因子块长分布（长块=大孔、短块=小孔）
"""
import os, sys, pickle, json
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name

# 非零率（n=3-8 实测 + n=9-11 估计）
RATES = {3: 1.00, 4: 0.602, 5: 0.309, 6: 0.155, 7: 0.0585, 8: 0.0260}

if __name__ == '__main__':
    # 1) 孔洞占比标度：hole(n) = 1 - rate(n)
    print('=== 孔洞占比标度 ===')
    holes = {n: 1 - r for n, r in RATES.items()}
    for n in sorted(holes):
        print(f'n={n}: 非零率 {RATES[n]:.4f}——孔洞占比 {holes[n]:.4f}')

    # 分形维数：每步 n+1 孔洞放大因子 = hole(n+1)/hole(n)——若恒定 = 1/2 标度 → 孔洞测度维数 d = 1 - log2(ratio)
    ratios = [holes[n+1]/holes[n] for n in range(4, 8)]
    import numpy as np
    mean_r = np.mean(ratios)
    # 连续标度：孔洞体积 ∝ 2^(-n·a)——a = -log2(mean_r)/1 每步
    alpha = -np.log2(mean_r)
    print(f'孔洞放大因子均值: {mean_r:.3f}（几何衰减 {alpha:.2f} bit/步）')
    # 测度维数类比：非零胞腔测度 ∝ 2^{-d·n} → d = -log2(rate 比值)
    ds = [-np.log2(RATES[n+1]/RATES[n]) for n in range(3, 8)]
    print(f'每步非零率减半指数 d_n: {[f"{x:.2f}" for x in ds]}——均值 {np.mean(ds):.2f}')
    print(f'→ 蜂窝孔洞分形：非零胞腔测度 ∝ 2^(-{np.mean(ds):.2f}n)——"孔洞体积"指数增长（多孔性随 n 增强）')

    # 2) 块长分布：n=11 阈值化缓存——A=0（孔洞）vs A≠0 的因子块长画像
    print('\n=== n=11 块长分布（孔洞 vs 非零）===')
    with open(os.path.join(SCRIPT_DIR, 'cache_n11_thr3x20000.pkl'), 'rb') as f:
        datas = pickle.load(f)
    samples = []
    for sd in ['77', '331', '777']:
        samples.extend(datas[sd])

    factors = adj_partition_factors(11)
    # 每个因子的块长（min(a 长, b 长)）
    fac_len = [min(len(a), len(b)) for a, b in factors]
    hole_blocks = Counter()
    nz_blocks = Counter()
    hole_n = 0
    nz_n = 0
    for facs, a in samples:
        if a == 0:
            hole_n += 1
            for i, L in enumerate(fac_len):
                if facs[i] != 0:   # 非零因子（活动块）——在孔洞内
                    hole_blocks[L] += 1
        else:
            nz_n += 1
            for i, L in enumerate(fac_len):
                if facs[i] != 0:
                    nz_blocks[L] += 1
    print(f'A=0 样本 {hole_n}（{hole_n/len(samples)*100:.1f}%）——非零 {nz_n}')
    print('块长分布（相对频率）:')
    print(f'{"块长":<6}{"孔洞内":<12}{"非零胞腔":<12}')
    for L in sorted(set(fac_len)):
        hp = hole_blocks[L] / (hole_n * 220)
        np_ = nz_blocks[L] / (nz_n * 220) if nz_n else 0
        print(f'{L:<6}{hp:<12.5f}{np_:<12.5f}')

    # 3) 幂律检验：孔洞内长块（≥5）占比 vs 短块（≤2）
    hl = sum(hole_blocks[L] for L in fac_len if L >= 5) / max(hole_n * 220, 1)
    hs = sum(hole_blocks[L] for L in fac_len if L <= 2) / max(hole_n * 220, 1)
    print(f'\n孔洞内长块(≥5)占比 {hl:.4f} vs 短块(≤2)占比 {hs:.4f}——长块主导 {hl/hs:.2f}x')

    out = {'rates': RATES, 'hole_ratios': ratios, 'alpha': round(float(alpha), 3),
           'dims': [round(float(x), 3) for x in ds],
           'hole_block_dist': {str(k): v for k, v in sorted(hole_blocks.items())},
           'nz_block_dist': {str(k): v for k, v in sorted(nz_blocks.items())}}
    with open(os.path.join(SCRIPT_DIR, 'paperX_n11_p4_fractal.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('\nDONE -> paperX_n11_p4_fractal.json')
