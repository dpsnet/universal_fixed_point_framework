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
EGDB Tmax-Ro 分层交叉验证（Paper XLIII，2026-08-09）
对应笔记：notes/05_condensed_matter/shale_data_inventory.md（§7.3 R3 诚实负结果的分层跟进）

背景：R3 全样本 Tmax-Ro Spearman ρ=0.278（n=4,583，p=7.6e-82）——Tmax 窗形轴为带噪成熟度代理。
但全样本由 57 州、数百地层体系混合构成：不同体系（干酪根类型、Tmax-Ro 标定差异）混合可能
模糊 Tmax-Ro 关系。本脚本按"州×地层"分层重算 ρ，剥离体系混合效应：

  T1 全样本基线复现：ρ≈0.278 且 n≥4,000（数据管道一致性）
  T2 分层内 ρ：≥n_min 的州×地层组内 Spearman ρ 分布——若中位数显著高于全样本 0.278，
     则弱相关主要来自体系混合（Tmax 在体系内仍是有效成熟度轴）；若持平或更低，则噪声为体系内固有
  T3 成熟度跨度组（组内 Ro 跨度≥ΔRo_min）：成熟度变化充分时 ρ 是否增强（Ro 范围太窄时 ρ 天然不可靠）
  T4 阿拉斯加 vs 非阿拉斯加：R4 警示 Ro 集中于阿拉斯加北坡——分组确认体系集中是否扭曲全样本 ρ
  T5 诚实登记：输出不可靠组（n 或 Ro 跨度不足）清单，避免过度解读

输入：
  egdb_ro_vitrinite.csv（Ro 子集，OrderID+SampleNumber 主键，含 Formation/State/TMAX）

输出：
  打印分层统计 + 写 egdb_tmaxro_split_summary.csv（各组 ρ/n/p/Ro 中位/跨度）
"""
import csv
import os
import numpy as np
from scipy.stats import spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
RO_CSV = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_ro_vitrinite.csv")
OUT_CSV = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_tmaxro_split_summary.csv")

RO_PARAMS = ("RMEAN", "RMODE", "Rmode", "RMode")
N_MIN = 30          # 组内样品数下限（Spearman 可靠）
RO_SPAN_MIN = 0.30  # 组内 Ro 跨度下限（%Ro，成熟度变化充分）
N_GROUP_MIN = 5     # 报告组数下限


def to_f(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def load_pairs():
    """逐样品去重（RMEAN 优先），物理范围 Ro∈[0.2,6]，须同时有 TMAX。"""
    by_sample = {}
    with open(RO_CSV, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not (r["TMAX"] and r["NumericResult"]):
                continue
            if r["Param"] not in RO_PARAMS:
                continue
            tmax, ro = to_f(r["TMAX"]), to_f(r["NumericResult"])
            if tmax is None or ro is None:
                continue
            if not (0.2 <= ro <= 6.0):
                continue
            key = (r["OrderID"], r["SampleNumber"])
            pref = 0 if r["Param"] == "RMEAN" else 1
            cur = by_sample.get(key)
            if cur is None or pref < cur[0]:
                by_sample[key] = (pref, tmax, ro, r["Formation"].strip(), r["State"].strip())
    pairs = []
    for _, (_, tmax, ro, fm, st) in sorted(by_sample.items()):
        pairs.append((tmax, ro, fm, st))
    return pairs


def rho_stats(rows):
    """rows: list of (tmax, ro)。返回 (ρ, p, n) 或 None。"""
    if len(rows) < 5:
        return None
    t = np.array([r[0] for r in rows], dtype=float)
    x = np.array([r[1] for r in rows], dtype=float)
    if np.all(t == t[0]) or np.all(x == x[0]):
        return (np.nan, 1.0, len(rows))
    rho, p = spearmanr(t, x)
    return (rho, p, len(rows))


def group_by(pairs, keys_fn):
    g = {}
    for p in pairs:
        k = keys_fn(p)
        if not k:
            continue
        g.setdefault(k, []).append(p)
    return g


def main():
    pairs = load_pairs()
    print("== EGDB Tmax-Ro 分层交叉验证 ==")
    print("成对样品（Ro∈[0.2,6] 且含 TMAX）：%d" % len(pairs))

    # T1 全样本基线
    base = rho_stats(pairs)
    rho0, p0, n0 = base
    print("\n[全样本基线] ρ=%.3f（p=%.3g，n=%d）" % (rho0, p0, n0))

    # 分层：州×地层
    g_se = group_by(pairs, lambda p: (p[3], p[2]) if p[3] and p[2] else None)
    # 分层：州
    g_s = group_by(pairs, lambda p: p[3])
    # 分层：地层
    g_f = group_by(pairs, lambda p: p[2])

    summaries = []  # (层级, 组名, ρ, p, n, Ro中位, Ro跨度)

    def collect(level, groups):
        for name, rows in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            st = rho_stats(rows)
            if st is None:
                continue
            rho, p, n = st
            ro_vals = [r[1] for r in rows]
            med, span = float(np.median(ro_vals)), float(np.max(ro_vals) - np.min(ro_vals))
            summaries.append((level, name, rho, p, n, med, span))

    collect("state", g_s)
    collect("formation", g_f)
    collect("state-formation", g_se)

    # 写汇总 CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["level", "group", "rho", "p", "n", "Ro_median", "Ro_span"])
        w.writerows(summaries)
    print("\n[汇总] %s（%d 组）" % (os.path.basename(OUT_CSV), len(summaries)))

    checks = []
    # T1 基线复现
    checks.append(("T1 全样本基线复现：ρ=%.3f（n=%d≥4000，p=%.3g）——管道一致性确认"
                   % (rho0, n0, p0),
                   0.20 <= rho0 <= 0.36 and n0 >= 4000))

    # T2 州×地层组内 ρ 中位数 vs 全样本（n≥N_MIN 且 Ro 跨度≥RO_SPAN_MIN 的组）
    se_ok = [(s[2], s[4], s[6]) for s in summaries
             if s[0] == "state-formation" and s[4] >= N_MIN and s[6] >= RO_SPAN_MIN]
    if se_ok:
        rhos = [r[0] for r in se_ok if not np.isnan(r[0])]
        med_rho = float(np.median(rhos)) if rhos else np.nan
        n_up = sum(1 for r in rhos if r > rho0)
        checks.append(("T2 州×地层组内 ρ（n≥%d 且 Ro 跨度≥%.2f，%d 组）：ρ 中位数 %.3f，"
                       "高于全样本 0.278 的组 %d/%d——体系混合剥离效应"
                       % (N_MIN, RO_SPAN_MIN, len(rhos), med_rho, n_up, len(rhos)),
                       med_rho > rho0 and n_up >= len(rhos) * 0.5))
    else:
        checks.append(("T2 州×地层分层组不足（n≥%d 且 Ro 跨度≥%.2f 无一组）" % (N_MIN, RO_SPAN_MIN), False))

    # T3 成熟度跨度组：Ro 跨度≥0.5 的强成熟度梯度组
    strong = [(s[1], s[2], s[4], s[6]) for s in summaries
              if s[0] == "state-formation" and s[4] >= N_MIN and s[6] >= 0.50 and not np.isnan(s[2])]
    if strong:
        rhos_s = [r[1] for r in strong]
        med_s = float(np.median(rhos_s))
        n_pos = sum(1 for r in rhos_s if r > 0.4)
        checks.append(("T3 成熟度跨度组（Ro 跨度≥0.50，n≥%d，%d 组）：ρ 中位数 %.3f，ρ>0.4 组 %d/%d"
                       "——成熟度变化充分时 Tmax-Ro 关系"
                       % (N_MIN, len(rhos_s), med_s, n_pos, len(rhos_s)),
                       med_s > 0.4 and n_pos >= len(rhos_s) * 0.5))
    else:
        checks.append(("T3 强成熟度梯度组不足（Ro 跨度≥0.50 且 n≥%d 无一组）" % N_MIN, False))

    # T4 阿拉斯加 vs 非阿拉斯加
    ak = [p for p in pairs if p[3] == "Alaska"]
    n_ak = [p for p in pairs if p[3] != "Alaska"]
    lines = []
    for nm, grp in (("阿拉斯加", ak), ("非阿拉斯加", n_ak)):
        st = rho_stats(grp)
        lines.append("%s：ρ=%.3f（n=%d）" % (nm, st[0], st[2]))
    checks.append(("T4 体系集中分离：" + "；".join(lines) + "——R4 覆盖警示的定量确认", True))

    # T5 诚实登记：不可靠组（n 或 Ro 跨度不足）计数
    se_all = [(s[4], s[6]) for s in summaries if s[0] == "state-formation"]
    n_small = sum(1 for n, sp in se_all if n < N_MIN)
    n_narrow = sum(1 for n, sp in se_all if n >= N_MIN and sp < RO_SPAN_MIN)
    checks.append(("T5（登记）州×地层组：共 %d 组，其中 n<%d 组 %d、n≥%d 但 Ro 跨度<%.2f 组 %d——"
                   "不可靠组已排除于 T2/T3 之外（诚实边界）"
                   % (len(se_all), N_MIN, n_small, N_MIN, RO_SPAN_MIN, n_narrow), True))

    print("\n[分层 Top 组（州×地层，按 n）]")
    print("%-22s %8s %8s %8s %8s %8s" % ("组", "ρ", "p", "n", "Ro中位", "Ro跨度"))
    se_sorted = sorted([s for s in summaries if s[0] == "state-formation"],
                       key=lambda s: -s[4])[:15]
    for s in se_sorted:
        rho_txt = "%.3f" % s[2] if not np.isnan(s[2]) else "  -  "
        print("%-22s %8s %8.1e %8d %8.2f %8.2f" % (s[1][:22], rho_txt, s[3], s[4], s[5], s[6]))

    print("\n[检验]")
    n_pass = 0
    for name, ok in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
        n_pass += int(ok)
    print("结果：%d/%d 通过（T5 为登记项）" % (n_pass, len(checks)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
