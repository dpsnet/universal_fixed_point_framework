# -*- coding: utf-8 -*-
import json
d = json.load(open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_n11_m31_cross_seed.json', encoding='utf-8'))
print('final_size =', d['final_size'])
print('c50_280k =', d['c50_280k'])
print('n_conf_groups =', d['n_conf_groups'])
print('added =', d['added'])
