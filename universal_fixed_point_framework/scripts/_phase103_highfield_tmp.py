# -*- coding: utf-8 -*-
"""Phase 103c: 高场样本（B>=48 MG）详细清单 + 全目录高场盘点"""
import json, math

P = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_wd_absflux_cal.json'
with open(P, encoding='utf-8') as f:
    data = json.load(f)
rows = data['rows']

print('=== absflux 91 颗中 B>=48 MG 样本 ===')
hi = sorted([r for r in rows if r['B_MG'] >= 48], key=lambda r: r['B_MG'])
print('n =', len(hi))
for r in hi:
    print('gaia_int=%s  B=%.2f MG  Teff=%.0f  logg=%.1f  snr_blue=%.2f snr_red=%.2f'
          % (r['gaia_int'], r['B_MG'], r['Teff'], r['logg'], r['snr_blue'], r['snr_red']))
    print('   blue: obs=%.3e mod=%.3e res=%+.4f calres=%+.4f | red: res=%+.4f calres=%+.4f | slopeA: res=%+.4f calres=%+.4f'
          % (r['blue_obs'], r['blue_mod'], r['blue_res'], r['blue_calres'],
             r['red_res'], r['red_calres'], r['slopeA_res'], r['slopeA_calres']))

print()
print('=== absflux B>=10 MG 全部（中场+高场）===')
mid_hi = sorted([r for r in rows if r['B_MG'] >= 10], key=lambda r: r['B_MG'])
print('n =', len(mid_hi))
for r in mid_hi:
    print('gaia_int=%-20s B=%7.2f MG Teff=%6.0f logg=%.1f snr_b=%.1f snr_r=%.1f | blue_cal %+.4f red_cal %+.4f slopeA_cal %+.4f'
          % (r['gaia_int'], r['B_MG'], r['Teff'], r['logg'], r['snr_blue'], r['snr_red'],
             r['blue_calres'], r['red_calres'], r['slopeA_calres']))
