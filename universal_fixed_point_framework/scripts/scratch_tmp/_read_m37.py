# -*- coding: utf-8 -*-
import json
d = json.load(open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_n6_m37_analytic.json', encoding='utf-8'))
for k in ['c35', 'N', 'split61', 'id_s61_neg_sum', 'id_sk1_neg_sum', 'id_s61_pair_sum', 'sign_agree']:
    print(k, '=', d[k])
