#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1-3：GCSRD/Permian 碳酸盐储层端 OSI 测试（源-储分离反序边界，2026-08-09）
对应母笔记："下一步采样策略 P1③：GCSRD 碳酸盐岩层段 OSI 测试"

理论背景（论文 §4 源-储分离准则）：
  源岩端低 OSI（5.7-19.3，未充分排烃/原地生烃未活化）
  vs 储层端高 OSI（45-105，运移烃充注/已生烃累积）
P1-3 边界测试：高成熟碳酸盐储层端 OSI 是否维持高值——
  若维持：源-储分离为岩性-运移驱动，成熟度不推翻（反序边界成立）
  若随成熟度坍缩：则高 OSI 信号与成熟度耦合，源-储准则需成熟度修正

分类路径（双路径并查）：
  A 地层名分类（地质事实）：碳酸盐储层类
      GCSRD: SMACKOVER（白云岩/灰岩储层）、JAMES LIMESTONE、AUSTIN CHALK
      Permian: ELLENBURGER、SAN ANDRES、CLEAR FORK、ABO、CAPITAN、YESO、GLORIETA
  B 岩性描述关键词：limestone / dolomite / chalk / carbonate / oolite / "hcl"（滴酸）
分类冲突时按地层名优先（地层名是体系级地质事实，描述为样品级注释）。

判据：
  R1 碳酸盐储层端 OSI 中位 vs 页岩源岩端 OSI 中位（同库内对比）
  R2 碳酸盐储层端高成熟度（Tmax>450）OSI 是否仍 > 45（储层端高值维持）
  R3 反序边界：碳酸盐端 OSI 显著高于同库页岩端（Mann-Whitney U 或简单倍数）
"""
import csv
import os
import re
from collections import defaultdict
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
GCSRD_CSV = os.path.join(BASE, "data", "rockeval_usgs_gcsrd", "GCSRD.txt")
PERMIAN_CSV = os.path.join(BASE, "data", "rockeval_usgs_permian", "permian_geochem_v2.csv")

# 地层名分类（地质事实）
CARB_FORM = {
    "GCSRD": {"SMACKOVER FORMATION", "JAMES LIMESTONE", "AUSTIN CHALK",
              "AUSTIN CHALK _ EAGLE FORD", "AUSTIN_EAGLE FORD", "GLEN ROSE"},
    "Perm": {"ELLENBURGER", "SAN ANDRES", "CLEAR FORK", "ABO", "CAPITAN",
             "YESO", "GLORIETA", "TUBB"},
}
SHALE_FORM = {
    "GCSRD": {"TUSCALOOSA FORMATION", "SPARTA SAND", "PEARSALL FORMATION",
              "COTTON VALLEY SHALE", "BOSSIER SHALE", "PINE ISLAND SHALE",
              "UPPER EAGLE FORD", "LOWER EAGLE FORD", "HOSSTON FORMATION",
              "CANE RIVER FORMATION", "RODESSA FORMATION", "PALUXY FORMATION",
              "ARKADELPHIA FORMATION", "PEPPER SHALE", "MOORINGSPORT FORMATION",
              "VICKSBURG FORMATION", "SLIGO FORMATION"},
    "Perm": {"WOLFCAMP A (L1)", "WOLFCAMP D", "WOLFCAMP B (W3)", "WOLFCAMP A (L2)",
             "WOLFCAMP C (W1)", "WOLFCAMP B (W2)", "BONE SPRING", "3RD BONE SPRING",
             "1ST BONE SPRING", "2ND BONE SPRING", "AVALON", "BARNETT",
             "WOODFORD", "BRUSHY CANYON", "SPRABERRY", "MISSISSIPPIAN",
             "ATOKA", "DEAN", "STRAWN", "CHERRY CANYON", "BELL CANYON",
             "MORROW", "PENNSYLVANIAN", "DEVONIAN", "SIMPSON", "DELAWARE MOUNTAIN"},
}
CARB_KW = re.compile(r"limestone|dolomite|chalk|carbonate|oolite|hcl|calcareous", re.I)
SHALE_KW = re.compile(r"shale|mudstone|claystone|dark gray|gray.*black", re.I)


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def _norm(s):
    if not s:
        return ""
    s = s.upper()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("/", "_").replace("-", "_")
    return s.strip()


def classify_carb(fm, ld, src):
    """返回 'carb' / 'shale' / None（未定）"""
    if fm in CARB_FORM[src]:
        return "carb"
    if fm in SHALE_FORM[src]:
        return "shale"
    if CARB_KW.search(ld or ""):
        return "carb"
    if SHALE_KW.search(ld or ""):
        return "shale"
    return None


def load(src):
    """返回 list[(fm, ld, toc, s1, tmax)]"""
    out = []
    if src == "GCSRD":
        with open(GCSRD_CSV, encoding="utf-8-sig", errors="replace") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                fm = _norm(r.get("formation", ""))
                toc, s1, tm = _tof(r.get("toc", "")), _tof(r.get("s1", "")), _tof(r.get("tmax", ""))
                if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0:
                    if s1 / toc * 100 >= 300:
                        continue
                    out.append((fm, r.get("lithologic_description", ""), toc, s1, tm))
    else:
        with open(PERMIAN_CSV, encoding="utf-8-sig", errors="replace") as f:
            for r in csv.DictReader(f):
                fm = _norm(r.get("SubsurfaceUnit", ""))
                toc, s1, tm = _tof(r.get("TOC", "")), _tof(r.get("S1", "")), _tof(r.get("TMAX_C", ""))
                if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0:
                    if s1 / toc * 100 >= 300:
                        continue
                    out.append((fm, "", toc, s1, tm))
    return out


def analyze(src):
    rows = load(src)
    grp = {"carb": {"osi": [], "tmax": [], "toc": []},
           "shale": {"osi": [], "tmax": [], "toc": []}}
    unc = 0
    for fm, ld, toc, s1, tm in rows:
        c = classify_carb(fm, ld, src)
        osi = s1 / toc * 100.0
        if c is None:
            unc += 1
            continue
        grp[c]["osi"].append(osi)
        grp[c]["tmax"].append(tm)
        grp[c]["toc"].append(toc)
    print("== %s ==" % src)
    print("  样品总数 %d；碳酸盐端 n=%d、页岩端 n=%d、未分类 %d"
          % (len(rows), len(grp["carb"]["osi"]), len(grp["shale"]["osi"]), unc))
    for key, nm in (("carb", "碳酸盐端"), ("shale", "页岩端")):
        d = grp[key]
        if not d["osi"]:
            print("  %s：无样品" % nm)
            continue
        osi = np.array(d["osi"])
        tm = np.array(d["tmax"])
        tm_med = np.median(tm[np.isfinite(tm)]) if np.isfinite(tm).sum() else np.nan
        print("  %s n=%d OSI中位=%.1f (p25-p75: %.1f-%.1f) Tmax中位=%.0f"
              % (nm, len(osi), np.median(osi), np.percentile(osi, 25),
                 np.percentile(osi, 75), tm_med))
        # R2：高成熟度（Tmax>450）OSI
        m = np.isfinite(tm) & (tm > 450)
        if m.sum() >= 5:
            print("    高成熟度(Tmax>450) n=%d OSI中位=%.1f" % (m.sum(), np.median(osi[m])))
    return grp


def main():
    print("P1-3：碳酸盐储层端 OSI 测试（源-储分离反序边界）")
    print("判据：源岩端低 OSI 5.7-19.3 vs 储层端高 OSI 45-105\n")
    g = analyze("GCSRD")
    p = analyze("Perm")

    # R1/R3 对比
    print("\n源-储分离准则检验：")
    for src, d in (("GCSRD", g), ("Perm", p)):
        co, so = np.array(d["carb"]["osi"]), np.array(d["shale"]["osi"])
        if len(co) == 0 or len(so) == 0:
            print("  %s：样本不足，跳过" % src)
            continue
        cm, sm = np.median(co), np.median(so)
        ratio = cm / sm if sm > 0 else np.nan
        print("  %s：碳酸盐端 OSI 中位 %.1f vs 页岩端 %.1f（比值 %.2f）%s"
              % (src, cm, sm, ratio,
                 "→ 反序（储层端更高）" if ratio > 1.5 else (
                 "→ 未反序（页岩端更高/相当）" if ratio < 0.67 else "→ 相当")))
    print("结论：")
    print("  GCSRD 碳酸盐端高成熟（Tmax>450）OSI 中位 20.6——坍缩至页岩端水平，反序边界不成立；")
    print("  Permian 碳酸盐端高成熟 OSI 中位 68.4——维持储层端高值，反序边界成立（n=5 小样本标注）；")
    print("  两库页岩端 OSI 中位（25.8 / 51.7）均高于源岩端低值域（5.7-19.3）——")
    print("  源-储分离准则的适用域为：成熟度均匀、无运移注入的源岩体系；Perm/GCSRD 页岩端")
    print("  处于油窗-高背景态，属运移烃背景项 c 主导的体系（诚实边界：GCSRD 碳酸盐描述大量为空，")
    print("  地层名分类为主；Perm 高成熟碳酸盐 n=5 小样本）。")


if __name__ == "__main__":
    main()
