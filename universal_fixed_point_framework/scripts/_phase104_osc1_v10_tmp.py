# -*- coding: utf-8 -*-
"""Phase 104az-64 v10：同管线前向对比 A2 v1（单点 Zeeman 谱 → 论文测量管线）
- 合成谱：Koester 零场谱 + 振子强度重分配（多流形 Zeeman+抗磁分量组替换零场线剖面）
- 管线：论文同款 normalize（±50Å 掩蔽 4 次多项式）→ measure_ew（EW=∫(1−f)、depth=±5Å、det=ew>0.5∧depth>0.03、半距窗）
- 输出：逐星逐线缺失 % → 分档缺失序 vs 观测（LAMOST 41MG 档 Hγ−41/Hβ−27/Hδ−12/Hε−2%）
- 自检：B→0 时合成谱 = Koester 谱 → 缺失 0%
"""
import json, io, os, sys
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, factorial, lpmv

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

# ---------- 多流形对角化（复用 v9b 组件）----------
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
print("总态数:", NS, " 初态 n=2:", len(N2), flush=True)

E2_0 = -1.0/8.0
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
LIN_IDX = {n: [i for i, (nn, l) in enumerate(STATES) if nn == n] for n in LINES}

def components(B_amp, B_z):
    """返回每线分量组 {(Δλ_Å, w)}——w=振子强度份额（盘面/单点共用）"""
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

# ---------- Koester fid 网格 ----------
with io.open(os.path.join(BASE, "paperX_wd_m83c_fid_table.json"), "r", encoding="utf-8") as f:
    fid_tbl = json.load(f)
grid = {}
for k, v in fid_tbl.items():
    t, g = k.split("_")
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid)); loggs = sorted(set(g for t, g in grid))
def nearest(teff, logg):
    return min(teffs, key=lambda x: abs(x-teff)), min(loggs, key=lambda x: abs(x-logg))
cache_dir = os.path.join(BASE, "_koester_spec")
def load_koester(teff, logg):
    t, g = nearest(teff, logg)
    fid = grid.get((t, g))
    if fid is None:
        return None
    fp = os.path.join(cache_dir, "fid%s_%s_%s.dat" % (fid, t, g))
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

# ---------- 合成谱 + 管线 ----------
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
NM2KEY = {"Hα":3, "Hβ":4, "Hγ":5, "Hδ":6, "Hε":7, "Hζ":8, "Hη":9}

def synth_spectrum(wl, fl_koest_norm, comps_by_n, interp_wl):
    """振子强度重分配合成：每条线窗口内替换为分量组剖面
    fl_koest_norm：normalize 后的 Koester 谱（在 wl 网格）
    返回 interp_wl 网格上的合成谱"""
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
        # 零场剖面（normalize 空间 1−f）
        prof = 1.0 - np.interp(interp_wl, wl, fl_koest_norm)
        syn = np.zeros_like(interp_wl)
        for dlam, w in comps:
            if abs(dlam) > weff:
                continue  # 窗外的分量不进窗（但会进 EW 窗口？——先只放窗内，边界登记）
            syn += w * np.interp(interp_wl, interp_wl + dlam, prof, left=0, right=0)
        fl[m] = 1.0 - syn[m]
    return fl

def per_line_ews(fl_syn, fl_ref, wl):
    """同管线逐线 EW（det 阈值同论文）——缺失 % = 1 − EW_syn/EW_ref"""
    out = {}
    for nm, c in v10.BALMER.items():
        weff = min(W_ANG, HG[nm])
        ews, dets = [], []
        for fl in (fl_syn, fl_ref):
            m = (wl >= c-weff) & (wl <= c+weff)
            if np.sum(m) < 5:
                ews.append(0.0); dets.append(False); continue
            w, f = wl[m], fl[m]
            ew = float(np.trapezoid(1.0 - f, w))
            cm = np.abs(w-c) < 5
            depth = 1.0 - np.median(f[cm]) if np.sum(cm) > 0 else 0
            ews.append(ew); dets.append(bool(ew > 0.5 and depth > 0.03))
        out[nm] = {"ew_syn": ews[0], "ew_ref": ews[1], "det_syn": dets[0], "det_ref": dets[1]}
    return out

print("=== v10 自检：B=0 合成还原 ===", flush=True)
wl0, fl0 = load_koester(12000, 8.0)
nf0 = v10.normalize(wl0, fl0)
iwl = np.arange(3800.0, 7000.0, 0.5)
comp0 = components(0.0001, 0.0001)
fsyn0 = synth_spectrum(wl0, nf0, comp0, iwl)
e0 = per_line_ews(fsyn0, np.interp(iwl, wl0, nf0), iwl)
for nm in ("Hα","Hβ","Hγ","Hδ","Hε"):
    print("  %s: ew_syn %.2f ew_ref %.2f 缺失 %.2f%%" % (nm, e0[nm]["ew_syn"], e0[nm]["ew_ref"],
         100*(1-e0[nm]["ew_syn"]/max(e0[nm]["ew_ref"],1e-9))), flush=True)

# ---------- 主循环：DESI137 中场星 ----------
print("\n=== v10 主循环：逐星合成 → 管线 → 缺失 ===", flush=True)
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]

results = []
for s in cat:
    B = s["B_MG"]; T = s["Teff"]; g = s["logg"]; inc = s.get("Incl")
    if B < 10 or B > 100:
        continue
    k = load_koester(T, g)
    if k is None:
        continue
    wl_k, fl_k = k
    nf_k = v10.normalize(wl_k, fl_k)
    # 单点：B_z = B·cos(i)——i null 用 60°（B 单位：MG → au，1 au = 2350 MG）
    i_rad = np.radians(inc if inc is not None else 60.0)
    B_z = B * abs(np.cos(i_rad))
    comps = components(B/2350.0, B_z/2350.0)
    fsyn = synth_spectrum(wl_k, nf_k, comps, iwl)
    el = per_line_ews(fsyn, np.interp(iwl, wl_k, nf_k), iwl)
    miss = {}
    for nm, r in el.items():
        if r["ew_ref"] > 1e-9:
            miss[nm] = 100.0 * (1.0 - r["ew_syn"]/r["ew_ref"])
    results.append({"gid": str(s["gaia_int"]), "B_MG": B, "Teff": T, "Incl": inc,
                    "miss": miss, "det_syn": {nm: r["det_syn"] for nm, r in el.items()}})

print("合成星数:", len(results), flush=True)
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_v10_pipeline.json"), "w", encoding="utf-8") as f:
    json.dump({"results": results, "note": "A2 v1 单点（B_z=B·cos i）——同管线前向对比"}, f, ensure_ascii=False, indent=1)

# 41 MG 分档统计
for lo, hi, tag in ((10, 41, "B 10-41"), (41, 100, "B 41-100")):
    sub = [r for r in results if lo <= r["B_MG"] < hi]
    if not sub:
        print("%s: n=0" % tag, flush=True); continue
    print("\n%s (n=%d):" % (tag, len(sub)), flush=True)
    for nm in ("Hα","Hβ","Hγ","Hδ","Hε"):
        ms = [r["miss"][nm] for r in sub if nm in r["miss"] and np.isfinite(r["miss"][nm])]
        if ms:
            print("  %s 缺失: 中位 %.1f%% (P25 %.1f P75 %.1f, n=%d)" % (
                nm, np.median(ms), np.percentile(ms,25), np.percentile(ms,75), len(ms)), flush=True)
        else:
            print("  %s: 无数据" % nm, flush=True)
print("\ndone")
