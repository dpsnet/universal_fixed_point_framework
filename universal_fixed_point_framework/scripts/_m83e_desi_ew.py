# -*- coding: utf-8 -*-
"""R4：DESI 提取光谱 → 归一化 + Balmer EW 测量（与 M83c/d 同口径）
- 读 _desi_spec/{gaia_int}.npz（wave/flux/ivar）
- normalize：Balmer 线外 50Å 掩膜 + 4 阶多项式拟合
- measure_ew：window=80Å 数值积分（等值宽度）
- 输出 _m83e_desi_ew.json"""
import io, json, os, glob
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
SPECDIR = os.path.join(BASE, "_desi_spec")

BALMER = {"Ha": 6562.79, "Hb": 4861.33, "Hg": 4340.46, "Hd": 4101.73, "He": 3969.95}
WINDOW = 80.0
MASK_HALF = 50.0
EW_MIN = 0.5
DEPTH_MIN = 0.03

def normalize(wave, flux, ivar=None):
    """Balmer 外掩膜 polyfit4 归一化"""
    mask = np.ones(len(wave), dtype=bool)
    for c in BALMER.values():
        mask &= ~((wave > c - MASK_HALF) & (wave < c + MASK_HALF))
    m = mask & np.isfinite(flux)
    if m.sum() < 20:
        return None, None
    p = np.polynomial.polynomial.polyfit(wave[m], flux[m], 4)
    cont = np.polynomial.polynomial.polyval(wave, p)
    return flux / cont, cont

def measure_ew(wave, norm):
    """window=80 数值积分 EW（Å）"""
    out = {}
    for name, c in BALMER.items():
        m = (wave > c - WINDOW / 2) & (wave < c + WINDOW / 2)
        if m.sum() < 5:
            out[name] = None
            continue
        dw = np.gradient(wave[m])
        # EW = ∫(1 - flux/cont) dλ；norm 已含 /cont
        ew = float(np.trapezoid(1.0 - norm[m], wave[m]))
        depth = 1.0 - norm[m].min()
        if ew > EW_MIN and depth > DEPTH_MIN:
            out[name] = ew
        else:
            out[name] = None
    return out

def main():
    rec = {}
    if os.path.exists(os.path.join(BASE, "_m83e_desi_extracted.json")):
        with io.open(os.path.join(BASE, "_m83e_desi_extracted.json"), "r", encoding="utf-8") as f:
            rec = json.load(f)
    files = glob.glob(os.path.join(SPECDIR, "*.npz"))
    results = {}
    for fp in files:
        gid = os.path.basename(fp)[:-4]
        if not rec.get(gid, {}).get("ok"):
            continue
        d = np.load(fp)
        wave, flux, ivar = d["wave"], d["flux"], d["ivar"]
        # 有限值掩膜 + 正流量
        good = np.isfinite(flux) & (flux > 0)
        if good.sum() < 500:
            results[gid] = {"ok": False, "why": "flux_bad"}
            continue
        w, f = wave[good], flux[good]
        norm, cont = normalize(w, f)
        if norm is None:
            results[gid] = {"ok": False, "why": "norm_fail"}
            continue
        ews = measure_ew(w, norm)
        n_det = sum(1 for v in ews.values() if v is not None)
        results[gid] = {"ok": n_det >= 2, "n_det": n_det, "ews": ews,
                        "wave0": float(w[0]), "wave1": float(w[-1]), "n": int(len(w))}
    with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)
    ok = sum(1 for v in results.values() if v.get("ok"))
    print("EW done:", ok, "/", len(results), "files")
    # 打印几个样本
    for gid, v in list(results.items())[:5]:
        print(gid, v["ok"], v["n_det"], {k: round(x, 2) if x else None for k, x in v["ews"].items()})

if __name__ == "__main__":
    main()
