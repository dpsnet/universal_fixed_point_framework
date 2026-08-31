"""
白矮星分析 v11-gap：补全 B 梯度缺口（10^3-10^4 T）

复用 v10 完全相同的光谱处理管线（normalize/measure_ew/log_g/theo_ew），
对目录中 10^3-10^4 T、有 Teff 的 116 颗星测量 Balmer 线 EW 并计算残差，
用于完成全场 B-残差梯度（选择效应证伪的决定性测试）。
"""

import numpy as np
import warnings, json, time, os, sys

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from white_dwarf_analysis_v10 import get_spec, analyze as _analyze_core, log_g, theo_ew, measure_ew, normalize, BALMER

GAP_FILE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\gap_stars_1e3_1e4.json'
OUT_FILE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v11_gap_results.json'

def analyze(star):
    spec = get_spec(star)
    if not spec:
        return None
    wl, fl = spec
    nf = normalize(wl, fl)
    br = {}
    tew = 0.0
    nd = 0
    for ln, lw in BALMER.items():
        ew, det = measure_ew(wl, nf, lw)
        br[ln] = {'EW': float(ew), 'detected': bool(det)}
        if det:
            tew += ew
            nd += 1
    r = {'name': star['SDSS'], 'B_tesla': float(star['B'])*100.0,
         'Teff': float(star['Teff']) if star.get('Teff') else None,
         'Mstar': float(star['Mstar']) if star.get('Mstar') else None,
         'total_EW': float(tew), 'n_detected': nd, 'balmer_results': br}
    lg = log_g(r['Mstar'])
    r['log_g'] = float(lg)
    if r['Teff']:
        r['theo_EW'] = float(theo_ew(r['Teff'], lg))
        if r['total_EW'] > 0:
            r['ratio'] = float(r['total_EW']/r['theo_EW'])
            r['resid'] = float(np.log10(r['ratio']))
        else:
            r['ratio'] = 0.0
            r['resid'] = -3.0
    else:
        r['theo_EW'] = None
        r['resid'] = None
    return r

def main():
    with open(GAP_FILE, 'r', encoding='utf-8') as f:
        stars = json.load(f)
    print(f'缺口星总数: {len(stars)}', flush=True)

    results = []
    t0 = time.time()
    for i, s in enumerate(stars):
        parts = s['Sp-ID'].split('-')
        r = analyze(s)
        if r:
            results.append(r)
        status = f'[{i+1}/{len(stars)}] {s["SDSS"]} B={float(s["B"])*100:.0f} T Teff={s["Teff"]:.0f} -> {"OK" if r else "FAIL"}'
        if (i+1) % 10 == 0 or not r:
            print(f'{status} ({(time.time()-t0)/60:.1f} min)', flush=True)
        time.sleep(0.05)

    eff = [r for r in results if r.get('resid') is not None and r['total_EW'] > 0]
    print(f'\n完成: 成功 {len(results)}/{len(stars)}, 有效(EW>0) {len(eff)}', flush=True)
    if eff:
        print(f'缺口带残差: 均值 {np.mean([r["resid"] for r in eff]):+.3f} dex, n={len(eff)}', flush=True)

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({'n_total': len(stars), 'n_success': len(results), 'results': results},
                  f, indent=2, ensure_ascii=False, default=str)
    print(f'保存: {OUT_FILE}', flush=True)

if __name__ == '__main__':
    main()
