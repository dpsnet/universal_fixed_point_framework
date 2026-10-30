# -*- coding: utf-8 -*-
"""Phase 86 R4：振子求和理论上限（解析量级估算 + 文献锚点）
中场 B=10-100 MG，Balmer 线系 n=2 高层态溶解 -> 连续谱注入 f 的上限
对账：观测连续谱增强 vs 理论上限 vs 缺口
输出 scripts/_gaia_abs/paperX_wd_oscsum.json
"""
import json, io, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(BASE, "_gaia_abs")

# ---- 1) Balmer 线系振子强度（氢原子，零场标准值）----
# n=2 -> n'：f(2->3)=0.641, 4:0.119, 5:0.045, 6:0.022, 7:0.012, 8:0.0075, 9:0.005, >=10:0.004
BALMER_F = {3: 0.641, 4: 0.119, 5: 0.045, 6: 0.022, 7: 0.012, 8: 0.0075, 9: 0.005, 10: 0.004}
F_TOTAL_LINE = sum(BALMER_F.values())  # ~0.855
F_TOTAL_TRK = 1.0  # n=2 态 TRK 求和（线+连续谱）

# ---- 2) 磁场能与束缚能对比（B=10/50/100 MG）----
muB = 9.274e-24  # J/T
ryd = 13.6  # eV
def binding(n, Z=1):
    return ryd / n ** 2

rows = []
for B_mg in [10, 50, 100]:
    B_t = B_mg * 1e6 * 1e-4  # MG -> G -> T (1 T = 1e4 G)
    E_mag = muB * B_t / 1.602e-19  # eV
    # 溶解判据：束缚能 < E_mag 的态视为强扰动（部分溶解）；< 2*E_mag 视为中度扰动
    n_diss = None
    for n in range(3, 12):
        if binding(n) < E_mag:
            n_diss = n
            break
    # 溶解态贡献的线 f（Hε=2->7 起对应 n'=7）
    f_diss_half = 0.0  # 50% 溶解转移
    f_diss_full = 0.0  # 完全溶解转移
    for np_ in BALMER_F:
        if np_ >= 7:  # Hζ 起（n'=7,8,9,10）高层态
            f_diss_half += BALMER_F[np_] * 0.5
            f_diss_full += BALMER_F[np_]
    # 中等扰动（Hδ/Hε，n'=6/7）的 20%
    f_mid = 0.2 * (BALMER_F[6] + BALMER_F[7])
    f_lo = f_diss_half  # 保守下限
    f_hi = f_diss_full + f_mid  # 乐观上限
    rows.append({"B_MG": B_mg, "E_mag_eV": E_mag, "n_dissolve_first": n_diss,
                 "f_low": f_lo, "f_high": f_hi,
                 "frac_low_pct": 100 * f_lo / F_TOTAL_LINE,
                 "frac_high_pct": 100 * f_hi / F_TOTAL_LINE})

print("Balmer 线系总 f = {:.3f}；TRK 上限 = 1.0（线 85pct + 连续谱 15pct）".format(F_TOTAL_LINE))
print("\n=== 振子注入理论上限（中场）===")
for r in rows:
    print("B=%4d MG | 磁场能 %.3f eV | 首个溶解态 n=%s | 注入 f: %.3f-%.3f (%.1f%%-%.1f%% 线 f)" % (
        r["B_MG"], r["E_mag_eV"], r["n_dissolve_first"], r["f_low"], r["f_high"],
        r["frac_low_pct"], r["frac_high_pct"]))

# ---- 3) 对账：观测增强 vs 理论上限 ----
OBS_ENH_DEX = 0.058  # R3 跳变区增强（10-20kK 主档）
EW_MISSING_DEX = 0.275
# 观测连续谱增强的等效 f：EW 缺失 0.275 dex -> 线 f 缺失比例；增强 5.8% 缺失 -> 等效 f
# EW 缺失比例 = 1 - 10^(-0.275) = 0.469（§4.3.1 46.9%）；增强占缺失 21% -> 等效 f 转移
F_MISSED = 1 - 10 ** (-EW_MISSING_DEX)  # 0.469
f_obs_enh = F_MISSED * (OBS_ENH_DEX / EW_MISSING_DEX)  # 观测转移等效 f
print("\n=== 对账（观测 vs 理论上限）===")
print("观测: 连续谱增强 %+.3f dex = 等效 f 转移 %.3f（Balmer 线 f 的 %.1f%%）" % (
    OBS_ENH_DEX, f_obs_enh, 100 * f_obs_enh / F_TOTAL_LINE))
for r in rows:
    cover = "覆盖" if r["f_low"] <= f_obs_enh <= r["f_high"] else ("低于下限" if f_obs_enh < r["f_low"] else "超上限")
    print("B=%d MG 理论上限 %.3f-%.3f -> 观测 %.3f：%s" % (r["B_MG"], r["f_low"], r["f_high"], f_obs_enh, cover))

# ---- 4) 缺口归因 ----
gap_f = F_MISSED - f_obs_enh
print("\n=== 缺口归因 ===")
print("线缺失 f 总计 %.3f；连续谱响应 %.3f；缺口 %.3f（%.0f%%）" % (F_MISSED, f_obs_enh, gap_f, 100 * gap_f / F_MISSED))
print("高层态溶解可解释上限 ~{:.1f}pct 线 f -> 缺口超出传统注入上限 -> 需 B（拓扑禁戒）或 C（模型缺陷）".format(rows[1]["frac_high_pct"]))

out = {"method": "解析量级估算（Landau 束缚能比 + Balmer f 分布 + TRK 求和）；严格量子数字表（Zhao 2021/RWA 图 3/4）待下载",
       "balmer_f": BALMER_F, "F_total_line": F_TOTAL_LINE,
       "obs_enh_dex": OBS_ENH_DEX, "obs_equiv_f": f_obs_enh,
       "gap_f": gap_f, "gap_frac": gap_f / F_MISSED,
       "theory_bounds": rows}
with io.open(os.path.join(OUT, "paperX_wd_oscsum.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\nwritten:", os.path.join(OUT, "paperX_wd_oscsum.json"))
