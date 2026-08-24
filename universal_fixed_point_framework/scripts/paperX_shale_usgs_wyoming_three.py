# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
怀俄明盆地三组美方海相数据入库与三因素标定（Paper XLIII，2026-08-09）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md（数据扩大计划：Niobrara/Mowry/Lewis）

数据源（USGS Wind River / Bighorn 盆地热解系列，已下载未入库）：
  N1 Niobrara（Bighorn Basin，BHB）：`rockeval_usgs_niobrara/BHB_RockEval_2017_2011_results.csv`
     目标组 Niobrara 47 样品（+chalk 1；另含 Sage Breaks 22 / chalk kick 31 邻近层）
  N2 Mowry（Wind River Basin，WRB）：`rockeval_usgs_mowry/WRB_2018_pyrolysis_LECO.csv`
     目标组 Mowry 100 样品（另含 Shell Creek 18 / Thermopolis 11）
  N3 Lewis（Wind River Basin，GRB）：`rockeval_usgs_lewis/Lewis_2021_results.csv`
     目标组 Lewis 51 样品（另含 Asquith 32 等；75 行无层段信息排除）

目的：
  1) 三组转标准 CSV（Sample_ID/Depth_m/TOC_wt/S1_mgg/S2_mgg/Tmax_C/HI/PI/Well/Formation）
  2) 三判据分类（Z1 线性度 / Z2 低端趋零 / Z3 c→0）
  3) c 项标定（截距 b + TOC<1 端 S1 底板）
  4) OSI 对照：与中方储层端锚点（长7段/沙海组/芦草沟组逐样品）+ Eagle Ford GC-2 源岩端
     ——检验"源岩低 OSI 生烃态 vs 储层高 OSI 注入富集态"源-储分离在怀俄明三组的归属

方法学：列名模糊匹配（三文件列名风格不同）；单位行跳过；OSI<300 过滤与既有口径一致；
  MWU 用真实逐样品数据（加载既有标准 CSV），不使用虚拟样本。
"""
import csv
import os
import numpy as np
try:
    from scipy import stats as st
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

DATASETS = [
    {
        "name": "Niobrara", "tag": "N1", "basin": "Bighorn（怀俄明）",
        "src": os.path.join(DATA, "rockeval_usgs_niobrara", "BHB_RockEval_2017_2011_results.csv"),
        "out": os.path.join(DATA, "rockeval_usgs_niobrara", "niobrara_rockeval.csv"),
        "fm_filter": lambda f: "niobrara" in f.lower(),
    },
    {
        "name": "Mowry", "tag": "N2", "basin": "Wind River（怀俄明）",
        "src": os.path.join(DATA, "rockeval_usgs_mowry", "WRB_2018_pyrolysis_LECO.csv"),
        "out": os.path.join(DATA, "rockeval_usgs_mowry", "mowry_rockeval.csv"),
        "fm_filter": lambda f: f.strip().lower() == "mowry",
    },
    {
        "name": "Lewis", "tag": "N3", "basin": "Wind River（怀俄明）",
        "src": os.path.join(DATA, "rockeval_usgs_lewis", "Lewis_2021_results.csv"),
        "out": os.path.join(DATA, "rockeval_usgs_lewis", "lewis_rockeval.csv"),
        "fm_filter": lambda f: f.strip().lower() == "lewis",
    },
]


def _tof(x):
    x = (x or "").strip()
    if not x or x.startswith("<"):
        return np.nan
    try:
        return float(x.replace(",", ""))
    except (ValueError, TypeError):
        return np.nan


def find_col(headers, *keys):
    """模糊列名匹配：任一关键词命中的第一个列。"""
    for h in headers:
        hl = h.strip().lower()
        if all(k in hl for k in keys):
            return h
    return None


def find_toc(headers):
    """TOC 主列：优先 LECO TOC，排除含 carbonate（TC-TOC）的碳酸盐衍生列与 TC 全碳列。"""
    for h in headers:
        hl = h.strip().lower()
        if "leco" in hl and "toc" in hl and "carbonate" not in hl and "s1/toc" not in hl:
            return h
    for h in headers:
        hl = h.strip().lower()
        if "toc" in hl and "carbonate" not in hl and "s1/toc" not in hl and "tc-toc" not in hl:
            return h
    return None


def find_pi(headers):
    """PI 主列：排除 API（含 'api'）与含 s2 的派生列。"""
    for h in headers:
        hl = h.strip().lower()
        if "pi" in hl and "api" not in hl:
            return h
    return None


def find_s1s2(headers, n):
    """S1/S2 主列：精确词/下划线/空格开头，排除 S2/S3、PI 等派生列。"""
    for h in headers:
        hl = h.strip().lower()
        if hl == n or hl.startswith(n + "_") or hl.startswith(n + " ") or hl.startswith(n + "　"):
            return h
    return None


def load_and_clean(ds):
    rows = []
    fm_cnt = {}
    with open(ds["src"], encoding="utf-8-sig", errors="replace") as f:
        rd = csv.DictReader(f)
        h = rd.fieldnames
        c_tmax, c_s1, c_s2 = find_col(h, "tmax"), find_s1s2(h, "s1"), find_s1s2(h, "s2")
        c_toc = find_toc(h)
        c_hi, c_pi = find_col(h, "hi"), find_pi(h)
        c_fm, c_well = find_col(h, "formation"), find_col(h, "well")
        c_samp = find_col(h, "sample")
        c_top, c_bot = find_col(h, "top"), find_col(h, "bottom")
        for r in rd:
            s1 = _tof(r.get(c_s1) if c_s1 else None)
            # 单位行（Tmax/S1 不可解析）自动跳过
            if not np.isfinite(s1):
                continue
            toc, tm, s2 = _tof(r.get(c_toc) if c_toc else None), _tof(r.get(c_tmax) if c_tmax else None), _tof(r.get(c_s2) if c_s2 else None)
            fm = (r.get(c_fm) or "").strip() if c_fm else ""
            fm_cnt[fm or "(none)"] = fm_cnt.get(fm or "(none)", 0) + 1
            if not (np.isfinite(toc) and np.isfinite(tm) and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600):
                continue
            if not ds["fm_filter"](fm):
                continue
            top = _tof(r.get(c_top) if c_top else None)
            bot = _tof(r.get(c_bot) if c_bot else None)
            depth_m = ((top + bot) / 2.0 * 0.3048) if np.isfinite(top) and np.isfinite(bot) else np.nan
            rows.append({
                "Sample_ID": (r.get(c_samp) or "").strip() if c_samp else "",
                "Depth_m": depth_m,
                "TOC_wt": toc, "S1_mgg": s1, "S2_mgg": s2, "Tmax_C": tm,
                "HI": _tof(r.get(c_hi) if c_hi else None),
                "PI": _tof(r.get(c_pi) if c_pi else None),
                "Well": (r.get(c_well) or "").strip() if c_well else "",
                "Formation": fm,
            })
    return rows, fm_cnt


def write_std(rows, out):
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("    标准 CSV 已写入：%s（%d 样品）" % (out, len(rows)))


def classify(toc, s1, tag=""):
    if len(toc) < 8:
        print("  %-28s n 过小（%d），跳过分类" % (tag, len(toc)))
        return None
    a, b = np.polyfit(toc, s1, 1)
    yp = a * toc + b
    r2 = 1.0 - np.sum((s1 - yp) ** 2) / np.sum((s1 - s1.mean()) ** 2)
    med = np.median(toc)
    lo = np.median(s1[toc < med]) / np.median(s1[toc >= med]) if np.median(s1[toc >= med]) > 0 else np.inf
    z1, z2, z3 = r2 >= 0.90, lo < 0.35, s1.min() < 0.25
    typ = "零阈值型" if (z1 and z2 and z3) else "非零阈值型(c型)"
    print("  %-28s n=%-4d S1=%+.3f·TOC%+.3f  R2=%.3f  低/高比=%.3f  minS1=%.3f  "
          "OSI中位=%.1f  Z1Z2Z3=%s%s%s  -> %s"
          % (tag, len(toc), a, b, r2, lo, s1.min(), np.median(s1 / toc * 100),
             "Y" if z1 else "N", "Y" if z2 else "N", "Y" if z3 else "N", typ))
    return a, b, r2, lo, s1.min()


def load_anchor(name, path):
    """加载既有标准 CSV 的 OSI（OSI<300 一致性过滤）。"""
    toc, s1 = [], []
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            t, s = _tof(r.get("TOC_wt")), _tof(r.get("S1_mgg"))
            if np.isfinite(t) and np.isfinite(s) and t > 0:
                osi = s / t * 100
                if osi < 300:
                    toc.append(t); s1.append(s)
    return np.array(s1) / np.array(toc) * 100 if len(toc) else np.array([])


def main():
    anchors = {
        "长7段（中方储层，零阈值型）": load_anchor("chang7", os.path.join(DATA, "rockeval_chang7", "chang7_rockeval.csv")),
        "沙海组（中方储层，煤系注入）": load_anchor("shahai", os.path.join(DATA, "rockeval_shahai", "shahai_rockeval.csv")),
        "芦草沟组（中方储层，c型超压）": load_anchor("lucaogou", os.path.join(DATA, "rockeval_jimsar_lucaogou", "lucaogou_rockeval.csv")),
        "Eagle Ford GC-2（美方源岩，低熟）": load_anchor("ef", os.path.join(DATA, "rockeval_usgs_eagleford_gc2", "eagleford_gc2_rockeval.csv")),
    }
    for nm, osi in anchors.items():
        print("  锚点 %-30s n=%3d  OSI 中位=%5.1f" % (nm, len(osi), np.median(osi) if len(osi) else float("nan")))

    for ds in DATASETS:
        rows, fm_cnt = load_and_clean(ds)
        print("\n===== %s（%s）=====" % (ds["name"], ds["basin"]))
        print("  原始层段分布:", {k: v for k, v in sorted(fm_cnt.items())})
        if len(rows) < 30:
            print("  目标组有效样品不足：%d，跳过" % len(rows))
            continue
        write_std(rows, ds["out"])
        toc = np.array([r["TOC_wt"] for r in rows])
        s1 = np.array([r["S1_mgg"] for r in rows])
        tm = np.array([r["Tmax_C"] for r in rows])
        osi = s1 / toc * 100
        osi = osi[osi < 300] if len(osi[osi < 300]) > 20 else osi  # 一致性过滤（防异常值）
        print("  %s 目标组 %d 样品：TOC [%.2f, %.2f] 中位 %.2f | Tmax [%.0f, %.0f] 中位 %.0f | "
              "OSI 中位 %.1f"
              % (ds["name"], len(toc), toc.min(), toc.max(), np.median(toc),
                 tm.min(), tm.max(), np.median(tm), np.median(osi)))

        print("  三判据分类：")
        classify(toc, s1, "全窗（%s）" % ds["name"])

        print("  c 项标定：")
        c1 = s1[toc < 1.0]
        print("    c 代理（TOC<1.0 端 S1 中位）: %.3f mg/g (n=%d)" % (np.median(c1), len(c1)))
        a, b, *_ = classify(toc, s1, "回归（截距=体系 S1 底板）")

        print("  OSI 对照（源-储分离归属）：")
        if HAS_SCIPY:
            for nm, aos in anchors.items():
                if len(aos) >= 10:
                    u, p_less = st.mannwhitneyu(osi, aos, alternative="less")
                    u2, p_greater = st.mannwhitneyu(osi, aos, alternative="greater")
                    p_min = min(p_less, p_greater)
                    dirn = "显著低于" if p_less < 0.05 else ("显著高于" if p_greater < 0.05 else "无显著差异")
                    print("    %s(OSI 中位 %.1f) vs %s(%.1f)：单边 MWU p_less=%.3g / p_greater=%.3g -> %s"
                          % (ds["name"], np.median(osi), nm, np.median(aos), p_less, p_greater, dirn))
        else:
            print("    （scipy 不可用，跳过 MWU；中位数对比见上）")

        print("  诚实边界：%s 为 %s 盆地单井/多井剖面，Tmax 中位 %.0f℃（%s），成熟度集中"
              "——不作 f(M) 窗形动力学判断；目标组过滤后 n=%d。"
              % (ds["name"], ds["basin"], np.median(tm),
                 "低熟-油窗早期" if np.median(tm) < 435 else "油窗",
                 len(toc)))


if __name__ == "__main__":
    main()
