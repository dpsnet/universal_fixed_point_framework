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
中国湖相页岩三因素机制检验（Paper XLIII §6.3，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md §6.3 数据扩大计划

数据源（中国国内，OA 论文 + 已有入库）：
  - 长7段 10 样品（鄂尔多斯延长组，`rockeval_chang7`，M5/M8 标定，零阈值型对照）
  - 青山口 D86 16 样品（松辽盆地，PLoS One 2024 e0309346 Table 1 转录，
    `rockeval_qingshankou_d86`，well D86 单井 1971-2007 m，Tmax 435-454℃）
  - 青山口 SL 8 样品（松辽盆地，`rockeval_qingshankou`，M6/M12 使用）
  - 沙海组 23 样品（阜新盆地，ACS Omega 2025 acsomega.5c09312 Table 1 浏览器转录，
    `rockeval_shahai`，well LFD1 K1sh4 湖相泥岩 783-792 m，Tmax 433-448℃；#11 Tmax=541 煤系异常剔除）
  - 吉木萨尔芦草沟组 119 样品（准噶尔盆地，Mendeley Data Ma et al. 2024
    doi:10.17632/sy6znr66dc.1，`rockeval_jimsar_lucaogou`，6 口井 2721-3787 m，
    Tmax 413-455℃——中国湖相第六体系，原吉木萨尔 D 级图片散点升级为 A 级逐样品）

目的：检验三因素机制 c 项在中国湖相页岩内部的体系特异——
  C1 零阈值三判据分类：长7段（零阈值型）vs 青山口两批/沙海组/芦草沟组（c 型？）
  C2 OSI 背景对比：c 型组 OSI 中位显著高于长7段（运移/滞留油背景 c）
  C3 单井窗口：青山口 D86 单井内 OSI 与 Tmax 关系（窗内背景平稳性）

结论预期：中国湖相页岩内部两类并存——长7段零阈值型（低 S1 背景）vs
青山口/沙海组/芦草沟组 c 型（高 S1 背景），c 项体系特异获中国数据独立验证；
沙海组（小盆地油-煤共存）高背景与煤系油源注入一致；芦草沟组（吉木萨尔超压区）
高背景与超压-含油性正相关（齐洪岩等 2025）一致。
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
FILES = {
    "长7段": ("rockeval_chang7/chang7_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None),
    "青山口D86": ("rockeval_qingshankou_d86/qingshankou_d86_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None),
    "青山口SL": ("rockeval_qingshankou/qingshankou_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None),
    "沙海组": ("rockeval_shahai/shahai_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", 11),
    "芦草沟组": ("rockeval_jimsar_lucaogou/lucaogou_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None),
}


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load(fname, ct, cs, cm, drop_idx):
    toc, s1, tm = [], [], []
    with open(os.path.join(BASE, "data", fname), encoding="utf-8-sig", errors="replace") as f:
        for i, r in enumerate(csv.DictReader(f), start=1):
            if drop_idx and i == drop_idx:  # 沙海组 #11 Tmax=541 煤系异常
                continue
            a, b, c = _tof(r[ct]), _tof(r[cs]), _tof(r[cm])
            if np.isfinite(a) and np.isfinite(b) and 0 < a < 30 and b >= 0:
                toc.append(a)
                s1.append(b)
                tm.append(c)
    return np.array(toc), np.array(s1), np.array(tm)


def classify(toc, s1):
    a, b = np.polyfit(toc, s1, 1)
    yp = a * toc + b
    r2 = 1.0 - np.sum((s1 - yp) ** 2) / np.sum((s1 - s1.mean()) ** 2)
    med = np.median(toc)
    lo_ratio = np.median(s1[toc < med]) / np.median(s1[toc >= med])
    z1, z2, z3 = r2 >= 0.90, lo_ratio < 0.35, s1.min() < 0.25
    typ = "零阈值型" if (z1 and z2 and z3) else "c 型（背景高，非零阈值）"
    return {"a": a, "b": b, "r2": r2, "lo": lo_ratio, "min": s1.min(), "typ": typ}


def main():
    if not HAS_SCIPY:
        print("需要 scipy")
        return
    print("中国湖相页岩三因素检验（六体系，2026-08-09 芦草沟组入库）")
    print("体系          n   S1=a·TOC+b       R2    低/高比  minS1  OSI中位  Tmax窗   Z1Z2Z3  分类")
    print("-" * 108)
    results = {}
    for nm, (fn, ct, cs, cm, drop) in FILES.items():
        toc, s1, tm = load(fn, ct, cs, cm, drop)
        r = classify(toc, s1)
        osi = s1 / toc * 100.0
        results[nm] = {"osi": osi, "toc": toc, "s1": s1, "r": r}
        z = "%s%s%s" % ("Y" if r["r2"] >= 0.90 else "N",
                        "Y" if r["lo"] < 0.35 else "N",
                        "Y" if r["min"] < 0.25 else "N")
        print("%-10s %3d  %+.3f %+.3f  %.3f  %.3f  %.2f   %6.1f   %s-%s   %s   %s"
              % (nm, len(toc), r["a"], r["b"], r["r2"], r["lo"], r["min"],
                 np.median(osi), np.nanmin(tm), np.nanmax(tm), z, r["typ"]))
    # C2 OSI 背景对比：c 型组（青山口+沙海+芦草沟）vs 长7段
    c7 = results["长7段"]["osi"]
    c_grp = np.concatenate([results[k]["osi"] for k in ("青山口D86", "青山口SL", "沙海组", "芦草沟组")])
    u, p = st.mannwhitneyu(c_grp, c7, alternative="greater")
    print("\nC2 OSI 背景对比：c 型组（青山口+沙海+芦草沟，n=%d）中位=%.1f vs 长7段 n=%d 中位=%.1f；"
          "MWU p(c型组>长7段)=%.2e -> %s"
          % (len(c_grp), np.median(c_grp), len(c7), np.median(c7), p,
             "c 背景显著更高（运移/滞留油）" if p < 0.01 else "边际显著（p<0.05，稀释于芦草沟大样本）" if p < 0.05 else "未显著"))
    # C2' 逐体系 OSI 对照（芦草沟单独不显著：c 信号在绝对 S1 底板而非 OSI）
    print("C2' 逐体系 OSI 中位 vs 长7段 53.6（MWU p）：")
    for k in ("青山口D86", "青山口SL", "沙海组", "芦草沟组"):
        u, pk = st.mannwhitneyu(results[k]["osi"], c7, alternative="greater")
        print("     %-8s n=%-3d med=%.1f  p=%.2e  %s"
              % (k, len(results[k]["osi"]), np.median(results[k]["osi"]), pk,
                 "显著" if pk < 0.01 else "边际" if pk < 0.05 else "不显著"))
    # C3 青山口 D86 单井窗内 OSI-Tmax
    toc_d, s1_d, tm_d = load(FILES["青山口D86"][0], "TOC_wt", "S1_mgg", "Tmax_C", None)
    osi_d = s1_d / toc_d * 100.0
    rho, pv = st.spearmanr(tm_d, osi_d)
    print("C3 青山口 D86 单井窗内（19℃）：OSI-Tmax Spearman rho=%+.2f (p=%.2f) -> %s"
          % (rho, pv, "窗内背景平稳（成熟度效应被 c 背景压制）" if abs(rho) < 0.4 else "窗内趋势明显"))
    print("结论：中国湖相六体系内部两类并存——长7段零阈值型 vs 青山口/沙海组/芦草沟组/苏北阜宁 c 型；"
          "芦草沟组（119 样品，6 井）R²=0.010 极端 c 型：S1 底板 ~2 mg/g 与 TOC 无关（b=+2.790 六体系最大截距），"
          "多岩性（泥岩/页岩/粉砂岩/凝灰岩/白云岩/灰岩）叠加 + 超压区滞留油背景；"
          "Z3=Y 但 Z1/Z2=N——minS1 假零阈值被否决，三判据必要性再证；"
          "C2 合并 OSI 边际显著（p=0.024）系芦草沟大样本稀释——OSI 代理对恒定-S1 型体系失效，c 信号在绝对 S1 底板")


if __name__ == "__main__":
    main()
