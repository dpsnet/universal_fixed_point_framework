# -*- coding: utf-8 -*-
"""P3：层单值性检验（Phase 78——对齐谱维数链口径）
- 对象：cache_n11_thr3x20000.pkl（60000 阈值化权威）+ 26 因子名单（Φ 解析形式）
- 内容：26 因子模式下每个模式的 A 符号值分布——单值率——层奇异点量化
- 验收：26 名单 0 冲突 → 层单值性在谱维数链口径成立（奇异点 = 0）
"""
import os, sys, pickle, json
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name

BEST26 = ['s1_2', 's1_23', 's12_3', 's1_234', 's123_4', 's1_2345', 's1234_5', 's12345_6',
          's1_234567', 's1_2345678', 's1_2345678910', 's123_45678910', 's1234_5678910',
          's12345_678910', 's123456_78910', 's1234567_8910', 's12345678_910', 's2_3',
          's3_4', 's4_5', 's5_6', 's6_7', 's7_8', 's8_9', 's9_10', 's10_11']

if __name__ == '__main__':
    factors = adj_partition_factors(11)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in BEST26]

    with open(os.path.join(SCRIPT_DIR, 'cache_n11_thr3x20000.pkl'), 'rb') as f:
        datas = pickle.load(f)
    samples = []
    for sd in ['77', '331', '777']:
        samples.extend(datas[sd])
    print(f'样本: {len(samples)}——26 因子名单 {len(idx)}')

    # 层单值性：26 因子模式 → A 符号
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    npat = len(pat)
    conflicts = {k: v for k, v in pat.items() if len(set(v)) > 1}
    # A=0 单值（孔洞胞腔）
    zeros = sum(1 for v in pat.values() if set(v) == {0})
    nonzero = sum(1 for v in pat.values() if 0 not in v)
    mixed = sum(1 for v in pat.values() if len(set(v)) > 1)
    print(f'模式总数: {npat}')
    print(f'A=0 单值胞腔（孔洞）: {zeros} ({zeros/npat*100:.1f}%)')
    print(f'A≠0 单值胞腔: {nonzero} ({nonzero/npat*100:.1f}%)')
    print(f'混合（非单值——层奇异点）: {mixed}')
    if conflicts:
        print(f'奇异点密度: {mixed}/{npat} = {mixed/npat:.6f}')
        for k, v in list(conflicts.items())[:5]:
            print(f'  例: 模式 ...{k} -> {set(v)}')
    else:
        print('层单值性成立：0 冲突（奇异点 = 0）——26 因子覆盖内符号场为良定义层')

    out = {'n_samples': len(samples), 'n_factors': len(idx), 'n_patterns': npat,
           'zero_cells': zeros, 'nonzero_cells': nonzero, 'singular': mixed,
           'singular_density': round(mixed / npat, 6)}
    with open(os.path.join(SCRIPT_DIR, 'paperX_n11_p3_sheaf.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('\nDONE -> paperX_n11_p3_sheaf.json')
