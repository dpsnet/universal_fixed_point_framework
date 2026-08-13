#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EGDB 原始包 VitriniteReflectance（Ro）子集提取与 P1/P2 成熟度结构交叉验证（Paper XLIII，2026-08-09）
对应笔记：notes/05_condensed_matter/shale_data_inventory.md（EGDB 未利用字段潜力登记）

背景：EGDB 原始下载包 Analysis 表含 360 万条全分析记录（长表），处理产物 egdb_re_wide.csv 仅
提取了 Rock-Eval 型 46,599 条（TOC/S1/S2/TMAX/HI/PI），其余分析类型（VitriniteReflectance、
X-ray Diff、Isotopes、Biomarkers 等）未入库。本脚本提取 VitriniteReflectance 子集：

  源：rockeval_usgs_egdb/csv/EnergyGeoChemDB_csv/Analysis_*.csv（4 个分块）
      VitriniteReflectance 记录：Analysis_00003-99043.csv 21,066 条 + Analysis_BK-ERP-00063.csv 2,543 条
  关联：
      Samples.csv（OrderID+SampleNumber 主键）——补全 州/县/地层 FORMN/井 WELLN/API/岩性 LITHO1/深度
      egdb_re_wide.csv（OrderID+SampleNumber 主键）——补全 Rock-Eval TMAX，构成 Tmax-Ro 成对

检验（P1/P2 成熟度结构交叉验证通道）：
  R1 Ro 数据量：记录数 / 去重样品数 / 州覆盖
  R2 与 Rock-Eval 样品级重叠数：Tmax-Ro 成对可交叉验证样品数（f(M) 窗形轴的独立校验前提）
  R3 Tmax-Ro 秩相关（成对样品）：Ro 为独立成熟度轴——正相关强则 Tmax 窗形真实反映成熟度，
      f(M) 窗形轴（支撑 P1/P2 成熟度结构论证）可信
  R4 Ro 成熟度结构：按州/地层分组的 Ro 分布（P1/P2 跨体系成熟度结构独立视图）
"""
import csv
import os
import numpy as np
from scipy.stats import spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "data", "rockeval_usgs_egdb", "csv", "EnergyGeoChemDB_csv")
ANALYSIS_CHUNKS = [
    os.path.join(RAW, "Analysis_00003-99043.csv"),
    os.path.join(RAW, "Analysis_AA-BJ.csv"),
    os.path.join(RAW, "Analysis_BK-ERP-00063.csv"),
    os.path.join(RAW, "Analysis_ERP-00064-X1812.csv"),
]
SAMPLES_CSV = os.path.join(RAW, "Samples.csv")
WIDE_CSV = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv")
OUT_CSV = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_ro_vitrinite.csv")


def load_ro_rows():
    """遍历 4 个 Analysis 分块，保留 AnalysisGroup == VitriniteReflectance 行。"""
    rows = []
    for path in ANALYSIS_CHUNKS:
        n_group = 0
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f)
            header = next(reader)  # 12 列
            for rec in reader:
                if len(rec) < 12:
                    continue
                if rec[2].strip() == "VitriniteReflectance":
                    n_group += 1
                    rows.append({
                        "OrderID": rec[0].strip(), "SampleNumber": rec[1].strip(),
                        "AnalysisGroup": rec[2].strip(), "Matrix": rec[3].strip(),
                        "Delineation": rec[4].strip(), "Analysis": rec[5].strip(),
                        "Method": rec[6].strip(), "Param": rec[7].strip(),
                        "Result": rec[8].strip(), "NumericResult": rec[9].strip(),
                        "Units": rec[10].strip(), "Comments": rec[11].strip(),
                    })
        print("  %s：VitriniteReflectance %d 条" % (os.path.basename(path), n_group))
    return rows


def load_samples():
    """Samples.csv（36 列，引号包裹）→ {（OrderID, SampleNumber）: 元数据}"""
    meta = {}
    with open(SAMPLES_CSV, encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        for rec in reader:
            key = (rec.get("OrderID", "").strip(), rec.get("SampleNumber", "").strip())
            meta[key] = rec
    print("  Samples.csv：%d 条样品元数据" % len(meta))
    return meta


def load_wide_tmax():
    """egdb_re_wide.csv → {（OrderID, SampleNumber）: TMAX}（Rock-Eval 成对）"""
    tmax = {}
    with open(WIDE_CSV, encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        for rec in reader:
            key = (rec.get("OrderID", "").strip(), rec.get("SampleNumber", "").strip())
            tmax[key] = rec.get("TMAX", "").strip()
    print("  egdb_re_wide.csv：%d 条 Rock-Eval" % len(tmax))
    return tmax


def to_float(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def main():
    print("== EGDB VitriniteReflectance 子集提取 ==")
    print("[读取 Analysis 分块]")
    ro = load_ro_rows()
    print("[读取样品元数据]")
    samples = load_samples()
    print("[读取 Rock-Eval 宽表 TMAX]")
    wide_tmax = load_wide_tmax()

    # 参数视图（去重）
    params = {}
    for r in ro:
        params.setdefault(r["Param"], {"n": 0, "units": set(), "vals": []})
        params[r["Param"]]["n"] += 1
        params[r["Param"]]["units"].add(r["Units"])
        v = to_float(r["NumericResult"])
        if v is not None:
            params[r["Param"]]["vals"].append(v)

    print("\n[Ro 参数分布]")
    for p, d in sorted(params.items(), key=lambda kv: -kv[1]["n"]):
        vals = d["vals"]
        rng = "[%.3f, %.3f] n=%d" % (min(vals), max(vals), len(vals)) if vals else "无数值"
        print("  %-10s n=%6d units=%s %s" % (p, d["n"], sorted(d["units"]), rng))

    # 组装输出：Ro 行 + Samples 元数据 + TMAX（仅保留输出字段）
    fieldnames = ["OrderID", "SampleNumber", "Analysis", "Method", "Param", "NumericResult",
                  "Units", "Matrix", "Delineation", "Comments", "State", "County", "Formation",
                  "Well", "API", "Lithology", "TopDepth_ft", "TMAX"]
    out_rows = []
    n_meta = 0
    n_tmax = 0
    n_numeric = 0
    n_physical = 0
    for r in ro:
        key = (r["OrderID"], r["SampleNumber"])
        s = samples.get(key)
        if s is not None:
            n_meta += 1
        tmx = wide_tmax.get(key)
        if tmx:
            n_tmax += 1
        v = to_float(r["NumericResult"])
        if v is not None:
            n_numeric += 1
            if 0.2 <= v <= 6.0 and r["Param"] in ("RMEAN", "RMODE", "Rmode", "RMode"):
                n_physical += 1
        # 2026-08-13 修复：dict | dict 合并（PEP 584）需 Python 3.9+，项目为 3.8，改用 {**a, **b}
        out_rows.append({**{k: r[k] for k in fieldnames if k in r}, **{
            "State": (s or {}).get("STATE/Province", "").strip(),
            "County": (s or {}).get("COUNTY", "").strip(),
            "Formation": (s or {}).get("FORMN", "").strip(),
            "Well": (s or {}).get("WELLN", "").strip(),
            "API": (s or {}).get("API", "").strip(),
            "Lithology": (s or {}).get("LITHO1", "").strip(),
            "TopDepth_ft": (s or {}).get("TOPDEPTH", "").strip(),
            "TMAX": tmx or "",
        }})

    # 写输出
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)
    print("\n[输出] %s（%d 条；数值结果 %d 条；物理范围 Ro∈[0.2,6] 且为 RMEAN/RMODE 类 %d 条）"
          % (os.path.basename(OUT_CSV), len(out_rows), n_numeric, n_physical))

    # R 检验
    ro_uniq = len(set((r["OrderID"], r["SampleNumber"]) for r in ro))
    states = set(r["State"] for r in out_rows if r["State"])
    checks = [
        ("R1 Ro 数据量：%d 条记录 / %d 个去重样品 / %d 个州（%d 条数值结果）"
         % (len(ro), ro_uniq, len(states), n_numeric), ro_uniq >= 1000 and n_numeric >= 1000),
        ("R2 与 Rock-Eval 重叠：%d 个样品同时有 Ro 与 TMAX（Tmax-Ro 成对交叉验证前提）" % n_tmax,
         n_tmax >= 100),
    ]

    # Tmax-Ro 成对（RMEAN 优先；仅物理范围 Ro∈[0.2,6]）
    RO_PARAMS = ("RMEAN", "RMODE", "Rmode", "RMode")
    pair = []
    ro_by_sample = {}
    for r in out_rows:
        if r["TMAX"] and r["NumericResult"]:
            key = (r["OrderID"], r["SampleNumber"])
            tmax = to_float(r["TMAX"])
            v = to_float(r["NumericResult"])
            if (tmax is not None and v is not None and r["Param"] in RO_PARAMS
                    and 0.2 <= v <= 6.0):
                # RMEAN 优先（镜质体反射率均值最常用），否则保留首条
                pref = 0 if r["Param"] == "RMEAN" else 1
                cur = ro_by_sample.get(key)
                if cur is None or (pref < cur[0]):
                    ro_by_sample[key] = (pref, tmax, v, r["Formation"], r["State"])
    pair = list(ro_by_sample.values())
    if len(pair) >= 5:
        t_arr = np.array([p[1] for p in pair], dtype=float)
        r_arr = np.array([p[2] for p in pair], dtype=float)
        rho, pval = spearmanr(t_arr, r_arr)
        checks.append(("R3 Tmax-Ro 秩相关（n=%d，Ro∈[0.2,6]）：ρ=%.3f（p=%.3g）——Ro 独立成熟度轴对 Tmax 窗形轴的交叉验证%s"
                       % (len(pair), rho, pval,
                          "；诚实负结果登记（ρ≤0.3 弱相关，Tmax 为带噪成熟度代理，f(M) 轴使用须保留 Ro 独立校验）"
                          if rho <= 0.3 else ""),
                       rho > 0.3 and pval < 0.05))
    else:
        checks.append(("R3 Tmax-Ro 成对不足（n=%d <5），交叉验证待扩展" % len(pair), False))

    # R4 按州/地层 Ro 结构（Top 体系，物理范围）
    fm_ro = {}
    for r in out_rows:
        v = to_float(r["NumericResult"])
        if v is None or not r["Formation"] or r["Param"] not in RO_PARAMS:
            continue
        if not (0.2 <= v <= 6.0):
            continue
        fm_ro.setdefault(r["Formation"], []).append(v)
    top = sorted(fm_ro.items(), key=lambda kv: -len(kv[1]))[:6]
    checks.append(("R4 Ro 成熟度结构：Top 体系 %s（首个 %s n=%d Ro中位 %.2f）"
                   % ("/".join(t[0][:14] for t in top),
                      top[0][0][:14] if top else "-",
                      len(top[0][1]) if top else 0,
                      np.median(top[0][1]) if top else 0),
                   len(fm_ro) >= 10))

    print("\n[检验]")
    n_pass = 0
    for name, ok in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
        n_pass += int(ok)
    print("结果：%d/%d 通过" % (n_pass, len(checks)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
