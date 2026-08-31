"""
白矮星光谱分析 v9b：扩大弱场样本（100 颗）
"""
import numpy as np
from astroquery.vizier import Vizier
from astroquery.sdss import SDSS
import warnings
warnings.filterwarnings('ignore')
import json
import time

Vizier.ROW_LIMIT = 1000
MAX_WEAK = 100

BALMER = {'Hα':6562.8,'Hβ':4861.3,'Hγ':4340.5,'Hδ':4101.7,'Hε':3970.1,'Hζ':3889.1,'Hη':3835.4}
OTHER = [3933.7,3968.5,4300.0,5175.0,5890.0,7600.0,7699.0]

def log(m): print(m, flush=True)

def load_cat():
    log("加载 VizieR 目录...")
    res = Vizier.get_catalogs('J/ApJ/944/56')
    t = res[0]
    data = []
    for i in range(len(t)):
        data.append({
            'name': str(t['SDSS'][i]),
            'B_tesla': float(t['B'][i])*100.0,
            'Teff': float(t['Teff'][i]) if t['Teff'][i]>0 else None,
            'Mstar': float(t['Mstar'][i]) if not np.isnan(t['Mstar'][i]) else None,
            'Sp-ID': str(t['Sp-ID'][i]),
            'zoff': float(t['zoff'][i]) if not np.isnan(t['zoff'][i]) else None,
        })
    weak = [d for d in data if d['B_tesla']<1e3 and d['Teff'] is not None]
    inter = [d for d in data if 1e4<=d['B_tesla']<1e5]
    log(f"  总数 {len(data)}, 弱场(有Teff) {len(weak)}, 中场 {len(inter)}")
    return data, inter, weak

def get_spec(star):
    parts = star['Sp-ID'].split('-')
    if len(parts)!=3: return None
    try:
        sp = SDSS.get_spectra(plate=int(parts[0]), mjd=int(parts[1]), fiberID=int(parts[2]))
        if sp and len(sp)>0:
            d = sp[0][1].data
            wl = 10**d['loglam']
            fl = np.array(d['flux'], dtype=float)
            if star.get('zoff') and abs(star['zoff'])>1e-5:
                wl = wl/(1+star['zoff'])
            return wl, fl
    except: pass
    return None

def normalize(wl, fl):
    mask = np.ones(len(wl), dtype=bool)
    for lw in list(BALMER.values())+OTHER:
        mask &= (np.abs(wl-lw)>50)
    mask &= (wl>=3800)&(wl<=7000)
    if np.sum(mask)<10: return fl/np.median(fl)
    try:
        c = np.polyfit(wl[mask], fl[mask], 4)
        return fl/np.polyval(c, wl)
    except: return fl/np.median(fl)

def measure_ew(wl, fl, center, window=80):
    m = (wl>=center-window)&(wl<=center+window)
    if np.sum(m)<5: return 0.0, False
    w, f = wl[m], fl[m]
    ew = float(np.trapezoid(1.0-f, w))
    cm = np.abs(w-center)<5
    depth = 1.0-np.median(f[cm]) if np.sum(cm)>0 else 0
    return ew, (ew>1.0 and depth>0.05)

def analyze(star):
    spec = get_spec(star)
    if not spec: return None
    wl, fl = spec
    nf = normalize(wl, fl)
    br = {}
    tew = 0.0
    nd = 0
    for ln, lw in BALMER.items():
        ew, det = measure_ew(wl, nf, lw)
        br[ln] = {'EW':ew, 'detected':det}
        if det: tew+=ew; nd+=1
    return {'name':star['name'],'B_tesla':star['B_tesla'],'Teff':star['Teff'],
            'Mstar':star['Mstar'],'total_EW':tew,'n_detected':nd,'balmer_results':br}

def log_g(m):
    if not m or m<=0: return 8.0
    x = min(m/1.44, 0.99)
    R = 0.012*(m/0.6)**(-1/3)*(1-x**(4/3))**0.5
    g = 6.674e-8*(m*1.989e33)/(R*6.96e10)**2
    return float(np.log10(g))

def theo_ew(teff, lg=8.0):
    t = (teff-15000)/5000
    gf = 1.0+0.15*(lg-8.0)
    coeffs = [[15,3,-2],[12,2.5,-1.5],[8,1.5,-1],[6,1,-0.8],[5,0.8,-0.6],[4,0.6,-0.5],[3,0.5,-0.4]]
    return sum(max(0.1,(c[0]+c[1]*t+c[2]*t**2)*gf) for c in coeffs)

def main():
    log("="*70)
    log("白矮星 v9b：扩大弱场样本（100颗）")
    log("="*70)
    
    data, inter, weak_pool = load_cat()
    weak_pool.sort(key=lambda x: x['Teff'])
    if len(weak_pool)>MAX_WEAK:
        idx = np.linspace(0, len(weak_pool)-1, MAX_WEAK, dtype=int)
        weak_sel = [weak_pool[i] for i in idx]
    else:
        weak_sel = weak_pool
    log(f"选择: 中场 {len(inter)}, 弱场 {len(weak_sel)}/{len(weak_pool)}")
    
    log("\n分析中场...")
    int_res = []
    for i, s in enumerate(inter):
        log(f"  [{i+1}/{len(inter)}] {s['name']}")
        r = analyze(s)
        if r: int_res.append(r)
        time.sleep(0.1)
    log(f"  成功 {len(int_res)}/{len(inter)}")
    
    log("\n分析弱场...")
    weak_res = []
    for i, s in enumerate(weak_sel):
        if (i+1)%10==0 or i==0:
            log(f"  [{i+1}/{len(weak_sel)}] {s['name']}")
        r = analyze(s)
        if r: weak_res.append(r)
        time.sleep(0.05)
    log(f"  成功 {len(weak_res)}/{len(weak_sel)}")
    
    log("\n计算残差...")
    for res in [int_res, weak_res]:
        for r in res:
            lg = log_g(r['Mstar'])
            r['log_g'] = lg
            if r['Teff']:
                r['theo_EW'] = theo_ew(r['Teff'], lg)
                if r['total_EW']>0:
                    r['ratio'] = r['total_EW']/r['theo_EW']
                    r['resid'] = float(np.log10(r['ratio']))
                else:
                    r['ratio']=0.0; r['resid']=-3.0
            else:
                r['theo_EW']=None; r['resid']=None
    
    log("\n"+"="*70)
    log("统计分析")
    log("="*70)
    iv = [r for r in int_res if r.get('resid') is not None and r['total_EW']>0]
    wv = [r for r in weak_res if r.get('resid') is not None and r['total_EW']>0]
    log(f"有效: 中场 {len(iv)}/{len(int_res)}, 弱场 {len(wv)}/{len(weak_res)}")
    
    if iv and wv:
        ir = np.array([r['resid'] for r in iv])
        wr = np.array([r['resid'] for r in wv])
        ie = np.array([r['total_EW'] for r in iv])
        we = np.array([r['total_EW'] for r in wv])
        log(f"\n总EW: 中场 {np.mean(ie):.1f} Å, 弱场 {np.mean(we):.1f} Å, 比值 {np.mean(ie)/np.mean(we):.3f}")
        log(f"残差: 中场 {np.mean(ir):.3f} dex, 弱场 {np.mean(wr):.3f} dex")
        diff = np.mean(ir)-np.mean(wr)
        log(f"差异: {diff:.3f} dex, EW比值 {10**diff:.3f}, 缺失 {(1-10**diff)*100:.1f}%")
        try:
            from scipy import stats
            t,p = stats.ttest_ind(ir, wr, equal_var=False)
            log(f"t检验: t={t:.3f}, p={p:.6f}")
            if p<0.001: log("  → 极显著 p<0.001")
            elif p<0.01: log("  → 非常显著 p<0.01")
            elif p<0.05: log("  → 显著 p<0.05")
        except: pass
        idet = np.mean([r['n_detected']/7 for r in iv])
        wdet = np.mean([r['n_detected']/7 for r in wv])
        log(f"检测率: 中场 {idet*100:.1f}%, 弱场 {wdet*100:.1f}%")
    
    out = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v9b_results.json"
    def ser(o):
        if isinstance(o,(np.floating,np.integer)): return float(o)
        if isinstance(o,np.ndarray): return o.tolist()
        return o
    with open(out,'w',encoding='utf-8') as f:
        json.dump({'n_int':len(int_res),'n_weak':len(weak_res),
                   'int':[{k:ser(v) for k,v in r.items()} for r in int_res],
                   'weak':[{k:ser(v) for k,v in r.items()} for r in weak_res]},
                  f, indent=2, ensure_ascii=False, default=str)
    log(f"\n保存: {out}")
    log("完成")

if __name__=="__main__":
    main()
