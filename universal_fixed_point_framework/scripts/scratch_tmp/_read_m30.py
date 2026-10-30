# -*- coding: utf-8 -*-
import json
d = json.load(open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_n11_m30_reverse.json', encoding='utf-8'))
print('c55_5seed =', d['c55_5seed'])
print('reverse_size =', d['reverse_size'])
print('rev_minus_55 n =', len(d['diff_rev_minus_55']))
print('55_minus_rev n =', len(d['diff_55_minus_rev']))
