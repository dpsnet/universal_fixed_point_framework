# -*- coding: utf-8 -*-
"""Phase 104az-65：LAMOST B≥41 MG 21 星同样本标准合成（B-only，i=60°，Teff=12000 默认）
输出：每星标准 EW 缺失 + 深度（±5Å）+ 检测率 vs LAMOST 观测 d_pure
口径声明：标准合成 = 多流形混合本征态振子强度重分配（含抗磁跨 n 非对角元 + Zeeman 对角）→ Koester 零场谱替换 → 论文同管线"""
import json, io, os, sys
import numpy as np
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

# ---- 复用 v11 的核心函数（复制最小集，避免 import 触发 v10 主循环）----
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, factorial, lpmv

def Ylm(l, m, th):
    th = np.asarray(th, dtype=float)
    P = lpmv(abs(m), l, np.cos(th))
    CS = (-1.0)**m if m >= 0 else 1.0
    if abs(m) > l:
        return np.zeros_like(th)
    norm = np.sqrt((2*l+1)/(4*np.pi) * factorial(l-abs(m)) / factorial(l+abs(m)))
    return CS * norm * P

def R_nl(n, l, r):
    rho = 2.0*r/n
    norm = np.sqrt((2.0/n)**3 * factorial(n-l-1) / (2.0*n*factorial(n+l)))
    L = genlaguerre(n-l-1, 2*l+1)(rho)
    return norm * np.exp(-r/n) * (2.0*r/n)**l * L

def radial_int(n, l, np_, lp, power, r_max=140.0, N=10000):
    r = np.linspace(1e-8, r_max, N)
    f = R_nl(n, l, r) * R_nl(np_, lp, r) * r**power * r*r
    return float(np.trapezoid(f, r) if hasattr(np, 'trapezoid') else np.trapz(f, r))

def gaunt_cos(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    return float(np.sum(w * Ylm(l1,0,th) * np.cos(th) * Ylm(l2,0,th)) * (2*np.pi))
def gaunt_sin2(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    return float(np.sum(w * Ylm(l1,0,th) * np.sin(th)**2 * Ylm(l2,0,th)) * (2*np.pi))
def gaunt_sigma(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    return float(-np.sum(w * Ylm(l1,0,th) * np.sin(th) * Ylm(l2,1,th)) * (2*np.pi) / np.sqrt(2.0))
def gaunt_sin2_m1(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    return float(np.sum(w * Ylm(l1,1,th) * np.sin(th)**2 * Ylm(l2,1,th)) * (2*np.pi))

LMAX = 9
GC, GS, GSIG, GSM1 = {}, {}, {}, {}
for l1 in range(LMAX):
    for l2 in range(LMAX):
        if abs(l1-l2) == 1:
            GC[(l1,l2)] = gaunt_cos(l1, l2)
            GSIG[(l1,l2)] = gaunt_sigma(l1, l2)
        if abs(l1-l2) in (0, 2):
            GS[(l1,l2)] = gaunt_sin2(l1, l2)
            GSM1[(l1,l2)] = gaunt_sin2_m1(l1, l2)

NMAX = 8
STATES = [(n, l) for n in range(2, NMAX+1) for l in range(n)]
NS = len(STATES)
print("预计算径向积分...", flush=True)
R2 = np.zeros((NS, NS)); DIP = np.zeros((NS, NS)); R2m1 = np.zeros((NS, NS)); DIPsig = np.zeros((NS, NS))
for i, (n1, l1) in enumerate(STATES):
    for j, (n2, l2) in enumerate(STATES):
        if abs(l1-l2) in (0, 2):
            g = GS.get((l1,l2), GS.get((l2,l1), 0.0))
            R2[i, j] = radial_int(n1, l1, n2, l2, 2) * g
            if l1 >= 1 and l2 >= 1:
                gm = GSM1.get((l1,l2), GSM1.get((l2,l1), 0.0))
                R2m1[i, j] = radial_int(n1, l1, n2, l2, 2) * gm
        if n1 == 2 and abs(l1-l2) == 1:
            DIP[i, j] = radial_int(2, l1, n2, l2, 1) * GC.get((l1,l2), GC.get((l2,l1), 0.0))
            DIPsig[i, j] = radial_int(2, l1, n2, l2, 1) * GSIG.get((l1,l2), GSIG.get((l2,l1), 0.0))
N2 = [i for i, (n, l) in enumerate(STATES) if n == 2]

E2_0 = -1.0/8.0
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
LIN_IDX = {n: [i for i, (nn, l) in enumerate(STATES) if nn == n] for n in LINES}

def components(B_amp, B_z):
    M0f = R2.copy() * (0.125 * B_amp**2)
    M0g = M0f[np.ix_(N2, N2)]
    e0, v0 = np.linalg.eigh(M0g)
    init_states = [(E2_0 + e0[a], v0[:, a]) for a in range(len(N2))]
    ev0, _ = np.linalg.eigh(M0f)
    M1f = R2m1.copy() * (0.125 * B_amp**2)
    for i in range(NS):
        if STATES[i][1] >= 1:
            M1f[i, i] += B_z / 2.0
    ev1, _ = np.linalg.eigh(M1f)
    M_1f = M1f.copy()
    for i in range(NS):
        if STATES[i][1] >= 1:
            M_1f[i, i] -= B_z
    evm1, _ = np.linalg.eigh(M_1f)
    out = {}
    for n, (lam, Eph) in LINES.items():
        comps = []
        for a0, (E_i, amp_i) in enumerate(init_states):
            for i in LIN_IDX[n]:
                nf, lf = STATES[i]
                En0 = -0.5 / (nf * nf)
                amp = 0.0
                for ja, j in enumerate(N2):
                    l0 = STATES[j][1]
                    if abs(l0-lf) == 1 and abs(DIP[j, i]) > 1e-12:
                        amp += amp_i[ja] * DIP[j, i]
                amp_s = 0.0
                for ja, j in enumerate(N2):
                    l0 = STATES[j][1]
                    if abs(l0-lf) == 1 and abs(DIPsig[j, i]) > 1e-12:
                        amp_s += amp_i[ja] * DIPsig[j, i]
                for E_f, am in ((En0+ev0[i], amp), (En0+ev1[i], amp_s), (En0+evm1[i], amp_s)):
                    dEa = E_f - E_i
                    dlam = lam * (Eph - dEa) / Eph
                    comps.append((dlam, am**2))
        tot = sum(c[1] for c in comps)
        if tot > 1e-30:
            out[n] = [(c[0], c[1]/tot) for c in comps if c[1] > 1e-9*tot]
        else:
            out[n] = []
    return out

def build_grid(B_d_au):
    amps = np.linspace(0.5*B_d_au, B_d_au, 6)
    zs = np.linspace(-B_d_au, B_d_au, 13)
    grid = {}
    for a in amps:
        for z in zs:
            grid[(round(a, 6), round(z, 6))] = components(a, z)
    return amps, zs, grid

def disk_components(B_d_au, i_deg, amps, zs, grid, Nt=20, Np=40):
    i = np.radians(i_deg)
    nz = np.cos(i); nx = np.sin(i)
    agg = {n: {} for n in LINES}
    for at in range(Nt):
        thp = np.pi*(at+0.5)/Nt
        cost = np.cos(thp); sint = np.sin(thp)
        B_amp = B_d_au * np.sqrt(1.0 + 3.0*cost**2) / 2.0
        for ap in range(Np):
            php = 2*np.pi*(ap+0.5)/Np
            cosp = np.cos(php)
            cosg = sint*cosp*nx + cost*nz
            if cosg <= 0:
                continue
            bdn = (3.0*cost*cosg - nz) / np.sqrt(1.0 + 3.0*cost**2)
            B_z = B_amp * bdn
            aq = min(amps, key=lambda x: abs(x-round(B_amp,6)))
            zq = min(zs, key=lambda x: abs(x-round(B_z,6)))
            c = grid[(round(aq,6), round(zq,6))]
            for n, comps in c.items():
                d = agg[n]
                for dlam, w in comps:
                    key = round(dlam, 2)
                    d[key] = d.get(key, 0.0) + cosg * w
    out = {}
    for n, d in agg.items():
        tot = sum(d.values())
        out[n] = [(k, v/tot) for k, v in d.items()] if tot > 1e-30 else []
    return out

# ---- Koester fid ----
with io.open(os.path.join(BASE, "paperX_wd_m83c_fid_table.json"), "r", encoding="utf-8") as f:
    fid_tbl = json.load(f)
grid_t = {}
for k, v in fid_tbl.items():
    t, g = k.split("_")
    grid_t[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid_t)); loggs = sorted(set(g for t, g in grid_t))
def nearest(teff, logg):
    return min(teffs, key=lambda x: abs(x-teff)), min(loggs, key=lambda x: abs(x-logg))
def load_koester(teff, logg):
    t, g = nearest(teff, logg)
    fid = grid_t.get((t, g))
    if fid is None:
        return None
    fp = os.path.join(BASE, "_koester_spec", "fid%s_%s_%s.dat" % (fid, t, g))
    if not os.path.exists(fp):
        return None
    wl2, fl2 = [], []
    with io.open(fp, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if len(p) >= 2:
                try:
                    wl2.append(float(p[0])); fl2.append(float(p[1]))
                except ValueError:
                    pass
    if len(wl2) < 100:
        return None
    return np.array(wl2), np.array(fl2)

W_ANG = 80.0
_BW = sorted(v10.BALMER.items(), key=lambda kv: kv[1])
def half_gaps():
    hg = {}
    for i, (nm, c) in enumerate(_BW):
        lo = _BW[i-1][1] if i > 0 else None
        hi = _BW[i+1][1] if i+1 < len(_BW) else None
        cand = [d for d in (None if lo is None else c-lo, None if hi is None else hi-c) if d]
        hg[nm] = min(cand) / 2.0 - 1.0
    return hg
HG = half_gaps()
NM2KEY = {"Hα":3, "Hβ":4, "Hγ":5, "Hδ":6, "Hε":7}

def synth_spectrum(wl, fl_koest_norm, comps_by_n, interp_wl):
    fl = np.interp(interp_wl, wl, fl_koest_norm)
    for nm, c in v10.BALMER.items():
        n = NM2KEY.get(nm)
        if n not in comps_by_n or not comps_by_n[n]:
            continue
        comps = comps_by_n[n]
        weff = min(W_ANG, HG[nm])
        m = (interp_wl >= c-weff) & (interp_wl <= c+weff)
        if np.sum(m) < 5:
            continue
        prof = 1.0 - np.interp(interp_wl, wl, fl_koest_norm)
        syn = np.zeros_like(interp_wl)
        for dlam, w in comps:
            if abs(dlam) > weff:
                continue
            syn += w * np.interp(interp_wl, interp_wl + dlam, prof, left=0, right=0)
        fl[m] = 1.0 - syn[m]
    return fl

def per_line_ews(fl_syn, fl_ref, wl):
    out = {}
    for nm, c in v10.BALMER.items():
        weff = min(W_ANG, HG[nm])
        ews, dets, depths = [], [], []
        for fl in (fl_syn, fl_ref):
            m = (wl >= c-weff) & (wl <= c+weff)
            if np.sum(m) < 5:
                ews.append(0.0); dets.append(False); depths.append(0.0); continue
            w, f = wl[m], fl[m]
            ew = float(np.trapezoid(1.0 - f, w))
            cm = np.abs(w-c) < 5
            depth = 1.0 - np.median(f[cm]) if np.sum(cm) > 0 else 0
            ews.append(ew); dets.append(bool(ew > 0.5 and depth > 0.03)); depths.append(depth)
        out[nm] = {"ew_syn": ews[0], "ew_ref": ews[1], "det_syn": dets[0], "det_ref": dets[1],
                   "depth_syn": depths[0], "depth_ref": depths[1]}
    return out

# ---- LAMOST B≥41 21 星 ----
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_lamost_linelevel_raw.json"), "r", encoding="utf-8") as f:
    lam = json.load(f)
lam = lam if isinstance(lam, list) else lam.get("mid", [])
ge41 = [r for r in lam if r.get("B_MG") is not None and r["B_MG"] >= 41]
print("LAMOST B≥41 星 n=%d" % len(ge41), flush=True)

wl_k, fl_k = load_koester(12000, 8.0)
nf_k = v10.normalize(wl_k, fl_k)
iwl = np.arange(3800.0, 7000.0, 0.5)

results = []
for r in ge41:
    B = r["B_MG"]; name = r.get("name", "?")
    B_d_au = B / 2350.0
    amps, zs, grid = build_grid(B_d_au)
    dc = disk_components(B_d_au, 60.0, amps, zs, grid)
    fsyn = synth_spectrum(wl_k, nf_k, dc, iwl)
    el = per_line_ews(fsyn, np.interp(iwl, wl_k, nf_k), iwl)
    rec = {"name": name, "B_MG": B}
    for nm, x in el.items():
        miss = 100.0*(1.0 - x["ew_syn"]/x["ew_ref"]) if x["ew_ref"] > 1e-9 else 100.0
        rec[nm] = {"miss": miss, "depth_syn": x["depth_syn"], "depth_ref": x["depth_ref"], "det_syn": x["det_syn"]}
    results.append(rec)
    obs = {}
    for k, v in r["lines"].items():
        if isinstance(v, dict):
            obs[k] = v.get("d_pure") if v.get("d_pure") == v.get("d_pure") else None
        else:
            obs[k] = v if v == v else None
    print("B=%.1f %s | 标准缺失 " % (B, name) + " ".join("%s %.0f%%" % (nm, rec[nm]["miss"]) for nm in ("Hβ","Hγ","Hδ","Hε")) + " | 观测d_pure " + str({k: obs[k] for k in ("Hbeta","Hgamma","Hdelta","Heps")}), flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_v12_lamost.json"), "w", encoding="utf-8") as f:
    json.dump({"results": results, "note": "v12 LAMOST B>=41 同样本标准合成（B-only i=60 T=12000 默认）+ 同管线"}, f, ensure_ascii=False, indent=1)

print("\n=== LAMOST B≥41 21 星：标准 vs 观测 ===", flush=True)
for nm, obs_key in (("Hβ","Hbeta"), ("Hγ","Hgamma"), ("Hδ","Hdelta"), ("Hε","Heps")):
    std_miss = np.median([r[nm]["miss"] for r in results])
    std_det_fail = sum(1 for r in results if not r[nm]["det_syn"])
    obs_vals = []
    for r in ge41:
        v = r["lines"].get(obs_key)
        if isinstance(v, dict):
            v = v.get("d_pure")
        if v is not None and v == v:
            obs_vals.append(v)
    obs_dp = np.median(obs_vals) if obs_vals else float("nan")
    print("  %s: 标准缺失中位 %.1f%% | 标准检测失败 %d/21 | 观测 d_pure 中位 %.3f (n=%d)" % (
        nm, std_miss, std_det_fail, obs_dp, len(obs_vals)), flush=True)
print("\ndone")
