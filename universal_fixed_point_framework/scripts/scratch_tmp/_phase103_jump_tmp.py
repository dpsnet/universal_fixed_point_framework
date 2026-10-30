# -*- coding: utf-8 -*-
"""Phase 103w: 从 Koester 网格谱提取 A(T)——Balmer 跳变幅度 → n2/背景分账
跳变带：blue 3600-3640（n=2 光电离吸收）vs red 3700-3750（背景）
流量比 J = log10(F_red/F_blue)（吸收强→流量低→J 大→n2 占比高→A 小）
A_model = 1/(1+10^J) 检验；对照 A_fit = 0.10×(kT/1.03)³（12/15/20kK: 0.10/0.20/0.47）
"""
import os, io, math, glob

CACHE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_koester_spec"

def load_spec(fp):
    wl, fl = [], []
    with io.open(fp, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if len(p) >= 2:
                try:
                    wl.append(float(p[0])); fl.append(float(p[1]))
                except ValueError:
                    pass
    return wl, fl

def band_flux(wl, fl, lo, hi):
    s = 0.0; n = 0
    for w, f in zip(wl, fl):
        if lo <= w <= hi:
            s += f; n += 1
    return s/n if n else None

def jump_for(teff, logg):
    """找最近温度档 + 该 logg 谱 → 跳变"""
    files = glob.glob(os.path.join(CACHE, "*_%.0f.0_*.dat" % teff))
    # 优先 logg=8.5（主档），其次 8.0
    best = None
    for g_pri in (8.5, 8.0, 8.25, 9.0):
        for fp in files:
            if "_%.1f.dat" % g_pri in fp or ("_%s.dat" % g_pri) in fp:
                best = fp; break
        if best: break
    if not best and files:
        best = files[0]
    if not best: return None
    wl, fl = load_spec(best)
    if len(wl) < 100: return None
    fb = band_flux(wl, fl, 3600.0, 3640.0)
    fr = band_flux(wl, fl, 3700.0, 3750.0)
    if fb is None or fr is None or fb <= 0: return None
    J = math.log10(fr / fb)
    A_model = 1.0 / (1.0 + 10.0 ** J)
    return os.path.basename(best), J, A_model, fb, fr

print('=== Koester 网格 Balmer 跳变 → A(T) ===')
print('%-7s | %-24s | %-8s | %-8s | %-8s | %-8s' % ('T(kK)', '谱文件', 'J(log比)', 'A模型', 'A_fit', 'F_blue'))
for T in (12000, 15000, 20000):
    r = jump_for(T, 8.5)
    if r is None:
        print('%-7d | 无缓存' % (T/1000)); continue
    fn, J, A, fb, fr = r
    kT = 8.617e-5 * T
    Afit = 0.10 * (kT / 1.03) ** 3
    print('%-7d | %-24s | %+.4f | %.4f | %.4f | %.3e' % (T/1000, fn, J, A, Afit, fb))

print()
print('--- 形状对照（归一化到 15kK）---')
for T in (12000, 15000, 20000):
    r = jump_for(T, 8.5)
    if r is None: continue
    _, J, A, _, _ = r
    kT = 8.617e-5 * T
    print('T=%dkK: A模型=%.4f (归一 %.2f), A_fit=%.3f (归一 %.2f)'
          % (T/1000, A, A/(jump_for(15000,8.5)[2] if jump_for(15000,8.5) else 1),
             (0.10*(kT/1.03)**3), ((kT/1.29)**3)))
