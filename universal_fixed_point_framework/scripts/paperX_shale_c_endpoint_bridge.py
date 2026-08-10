# -*- coding: utf-8 -*-
"""
c 项线 · 跨源相桥（endpoint bridge）可复用函数模块
==================================================
逻辑（见 shale_data_inventory.md §9.7 [D]，2026-08-10 登记）：
  1. 用源体系（如古龙原位端元：无运移/分馏/混合）的"成熟度-金刚烷指标"对建立校准线
  2. 将目标体系（如乌马营煤系凝析油）的指标值代入校准线，外推"等效成熟度"
  3. 与目标体系实测成熟度（如 Rc）对比：偏差 = 跨源相/体系差异对指标换算的影响上界
  4. 诚实登记：校准线 R² 低、样本少、外推越界时自动降级为粗略估计并在 summary 标注

用法示例（后续其他样品直接调用）：
    from paperX_shale_c_endpoint_bridge import endpoint_bridge
    res = endpoint_bridge(
        cal_maturity=gulong["Ro_pct"],          # 源体系实测成熟度（如源岩 Ro）
        cal_index=gulong["MDI"],                # 源体系金刚烷指标（逐样品）
        target_index=np.array([0.46, 0.49]),    # 目标体系指标值（标量或数组）
        target_maturity=np.array([1.25, 1.25]), # 目标体系实测成熟度（可选）
        index_name="MDI", maturity_name="Ro(%)",
    )
    print(res["summary"])
"""
import numpy as np
from scipy import stats

__all__ = ["fit_calibration", "endpoint_bridge"]


def fit_calibration(cal_maturity, cal_index, index_name="index", maturity_name="maturity"):
    """源体系校准线拟合：index = slope * maturity + intercept（正向 OLS）。

    参数
    ----
    cal_maturity : array-like  源体系实测成熟度（如源岩 Ro，%）
    cal_index    : array-like  源体系金刚烷指标（逐样品，如 MDI 比值 0-1）

    返回 dict：
        n, slope, intercept, r2（正向 OLS），rho_s/p_s（Spearman），
        maturity_min/max, index_min/max（校准适用范围，供外推检查）
    """
    m = np.asarray(cal_maturity, dtype=float)
    idx = np.asarray(cal_index, dtype=float)
    keep = np.isfinite(m) & np.isfinite(idx)
    m, idx = m[keep], idx[keep]
    if len(m) < 3:
        raise ValueError(f"校准样本不足（n={len(m)}，至少 3 个有效对）")

    slope, intercept, r_val, p_val, _ = stats.linregress(m, idx)
    rho_s, p_s = stats.spearmanr(m, idx)
    return {
        "n": len(m),
        "slope": slope, "intercept": intercept, "r2": r_val ** 2,
        "p_ols": p_val, "rho_s": rho_s, "p_s": p_s,
        "maturity_min": float(m.min()), "maturity_max": float(m.max()),
        "index_min": float(idx.min()), "index_max": float(idx.max()),
        "index_name": index_name, "maturity_name": maturity_name,
    }


def endpoint_bridge(cal_maturity, cal_index, target_index, target_maturity=None, *,
                    index_name="index", maturity_name="maturity",
                    mode="inverse", n_boot=0, ci_level=0.95, seed=0):
    """跨源相桥主函数：目标体系指标 → 源体系校准线外推等效成熟度 → 与实测对比。

    参数
    ----
    cal_maturity, cal_index : 源体系校准对（见 fit_calibration）
    target_index    : 目标体系指标值（标量或 array）
    target_maturity : 目标体系实测成熟度（可选，标量或 array，与 target_index 同形）
    mode            : "inverse"=正向校准线反解 maturity=(index-intercept)/slope
                        （与 §9.7 [D] 原口径一致）
                      "direct" = 直接回归 maturity = a + b*index（预测目标更标准）
    n_boot          : >0 时对预测成熟度做 bootstrap 置信区间（默认 0 不做）
    ci_level        : bootstrap 置信水平

    返回 dict：
        calibration（fit_calibration 结果）
        target_index, ro_pred（预测等效成熟度，array）
        extrapolate（bool，目标指标是否越出校准范围）
        maturity_observed, deviation（预测-实测，None 若未提供实测）
        ci_low/ci_high（bootstrap 区间，n_boot=0 时为 None）
        confidence_note（诚实登记文本：校准弱/外推越界提示）
        summary（多行文本报告）
    """
    cal = fit_calibration(cal_maturity, cal_index, index_name, maturity_name)
    t_idx = np.atleast_1d(np.asarray(target_index, dtype=float))

    if mode == "inverse":
        ro_pred = (t_idx - cal["intercept"]) / cal["slope"]
    elif mode == "direct":
        # maturity = a + b*index：用独立变量 index 对 maturity 回归
        m = np.asarray(cal_maturity, dtype=float)
        idx = np.asarray(cal_index, dtype=float)
        keep = np.isfinite(m) & np.isfinite(idx)
        b, a, _, _, _ = stats.linregress(idx[keep], m[keep])
        ro_pred = a + b * t_idx
    else:
        raise ValueError(f"未知 mode={mode!r}，可选 'inverse'/'direct'")

    # 外推检查：目标指标是否越出校准指标范围
    extrapolate = bool(((t_idx < cal["index_min"]) | (t_idx > cal["index_max"])).any())

    # bootstrap 预测 CI（可选）
    ci_low = ci_high = None
    if n_boot > 0 and len(np.unique(cal_maturity)) >= 5:
        rng = np.random.default_rng(seed)
        m = np.asarray(cal_maturity, dtype=float)
        idx = np.asarray(cal_index, dtype=float)
        keep = np.isfinite(m) & np.isfinite(idx)
        m, idx = m[keep], idx[keep]
        n = len(m)
        boots = np.empty((n_boot, len(t_idx)))
        for b_i in range(n_boot):
            s = rng.integers(0, n, n)
            if mode == "inverse":
                sl, ic, *_ = stats.linregress(m[s], idx[s])
                boots[b_i] = (t_idx - ic) / sl
            else:
                bb, aa, *_ = stats.linregress(idx[s], m[s])
                boots[b_i] = aa + bb * t_idx
        lo = (1 - ci_level) / 2
        ci_low = np.percentile(boots, lo * 100, axis=0)
        ci_high = np.percentile(boots, (1 - lo) * 100, axis=0)

    # 偏差
    obs = None
    dev = None
    if target_maturity is not None:
        obs = np.atleast_1d(np.asarray(target_maturity, dtype=float))
        if len(obs) == 1 and len(t_idx) > 1:
            obs = np.repeat(obs, len(t_idx))
        if len(obs) != len(t_idx):
            raise ValueError("target_maturity 与 target_index 长度不一致")
        dev = ro_pred - obs

    # 诚实登记
    notes = []
    if cal["r2"] < 0.3:
        notes.append(f"校准线 R²={cal['r2']:.2f} 较弱——偏差仅作粗略估计")
    if extrapolate:
        notes.append("目标指标越出校准范围——外推，误差可能放大")
    if len(cal_maturity) and cal["n"] < 5:
        notes.append(f"校准样本少（n={cal['n']}）——统计功效有限")
    confidence_note = "；".join(notes) if notes else "校准可用"

    # 报告文本
    lines = [
        "=" * 70,
        "跨源相桥（endpoint bridge）",
        f"源体系校准：{cal['index_name']} = {cal['slope']:.4f}*{cal['maturity_name']} "
        f"{cal['intercept']:+.4f}  (R²={cal['r2']:.3f}, n={cal['n']}, "
        f"Spearman ρ={cal['rho_s']:.3f}, p={cal['p_s']:.2e})",
        f"校准适用范围：{cal['maturity_name']} {cal['maturity_min']:.2f}–{cal['maturity_max']:.2f}，"
        f"{cal['index_name']} {cal['index_min']:.3f}–{cal['index_max']:.3f}",
    ]
    for i, t in enumerate(t_idx):
        line = (f"  目标 {cal['index_name']}={t:.3f} -> 等效 {cal['maturity_name']} "
                f"{ro_pred[i]:.2f}")
        if ci_low is not None:
            line += f"  [{ci_low[i]:.2f}, {ci_high[i]:.2f}]"
        if obs is not None:
            line += f"  (实测 {obs[i]:.2f}；偏差 {dev[i]:+.2f})"
        lines.append(line)
    lines.append(f"跨源相偏差上界：{np.abs(dev).max():+.2f} {cal['maturity_name']}" if dev is not None
                 else "（未提供目标实测成熟度，仅外推）")
    lines.append(f"诚实登记：{confidence_note}")
    lines.append("=" * 70)

    return {
        "calibration": cal,
        "target_index": t_idx,
        "ro_pred": ro_pred,
        "extrapolate": extrapolate,
        "maturity_observed": obs,
        "deviation": dev,
        "deviation_upper_bound": float(np.abs(dev).max()) if dev is not None else None,
        "ci_low": ci_low, "ci_high": ci_high,
        "confidence_note": confidence_note,
        "summary": "\n".join(lines),
    }


# ---------------- demo：复现 §9.7 [D]（乌马营 × 古龙） ----------------
if __name__ == "__main__":
    import os
    import pandas as pd

    _BASE = os.path.dirname(os.path.abspath(__file__))
    _CSV = os.path.join(_BASE, "data", "gulong_bai2025", "bai2025_gulong_table3.csv")
    if not os.path.exists(_CSV):
        print("[demo] 数据文件缺失，仅演示函数接口；请确认路径：", _CSV)
    else:
        df = pd.read_csv(_CSV)
        for c in ["MD1", "MD3", "MD4"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df["MDI"] = df["MD4"] / (df["MD1"] + df["MD3"] + df["MD4"])
        g = df.dropna(subset=["MDI", "Ro_pct"])

        # 乌马营煤系凝析油：MDI 46-51%（均值 49%），实测 Rc≈1.2-1.3% Ro
        res = endpoint_bridge(
            cal_maturity=g["Ro_pct"], cal_index=g["MDI"],
            target_index=np.array([0.46, 0.49, 0.51]),
            target_maturity=np.array([1.25, 1.25, 1.25]),
            index_name="MDI", maturity_name="Ro(%)",
            mode="inverse", n_boot=500,
        )
        print(res["summary"])
