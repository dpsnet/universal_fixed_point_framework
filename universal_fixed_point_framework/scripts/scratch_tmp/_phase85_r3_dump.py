# -*- coding: utf-8 -*-
"""Phase 85 R2+R3 结果落盘：paperX_wd_continuum_reg.json"""
import json, io, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
out = {
    "phase": "85",
    "stage": "R2+R3",
    "date": "2026-10-07",
    "n_obs": 91, "n_theo": 91, "n_rows": 91, "n_clean": 88,
    "bands": {
        "D_B": "(3600,3640)/(3700,3750) Balmer 跳变蓝/红",
        "slope": "log(5000-5800 / 4000-4060)/log(5400/4040) 连续谱斜率指数",
        "res_b1/b2/b3": "v10 normalize 后 (4000,4060)/(4800,4840)/(5000,5800) 带均值-1"
    },
    "R2_groups": {
        "D_B_res": {"weak_lt10MG": {"n": 68, "mean": 0.0216, "sd": 0.0359},
                     "mid_10_100MG": {"n": 18, "mean": 0.0260, "sd": 0.0240},
                     "strong_gt100MG": {"n": 2, "mean": -0.1935, "sd": 0.2192}},
        "slope_res": {"weak_lt10MG": {"n": 66, "mean": -0.0509, "sd": 0.0887},
                       "mid_10_100MG": {"n": 18, "mean": -0.0931, "sd": 0.0713},
                       "strong_gt100MG": {"n": 2, "mean": 0.0365, "sd": 0.0539}},
        "res_b3_diff": {"weak_lt10MG": {"n": 70, "mean": -0.0014, "sd": 0.0104},
                         "mid_10_100MG": {"n": 18, "mean": 0.0047, "sd": 0.0058},
                         "strong_gt100MG": {"n": 3, "mean": -0.3223, "sd": 0.4348}}
    },
    "R3_regression_vs_log10B": {
        "slope_res": {"n": 85, "rho": -0.350, "p_spearman": 0.00104, "beta": -0.0478, "p_ols": 0.0472},
        "D_B_res": {"n": 88, "rho": 0.106, "p_spearman": 0.326, "beta": -0.0366, "p_ols": 0.0111},
        "res_b3_diff": {"n": 88, "rho": 0.427, "p_spearman": 3.37e-05, "beta": 0.0023, "p_ols": 0.378}
    },
    "R3_teff_controlled": {
        "10_20kK_slope_res": {"weak_n": 44, "weak_mean": -0.0611, "mid_n": 11, "mid_mean": -0.1237,
                               "t": -2.43, "p": 0.0246},
        "10_20kK_D_B_res": {"weak_n": 45, "weak_mean": 0.0222, "mid_n": 11, "mid_mean": 0.0248,
                             "t": 0.24, "p": 0.8106},
        "gt20kK_slope_res": {"weak_n": 10, "weak_mean": -0.0335, "mid_n": 5, "mid_mean": -0.0495,
                              "t": -0.69, "p": 0.5210}
    },
    "conservation_comparison": {
        "slope_res_mid_minus_weak": -0.0422,
        "EW_mid_missing_dex": -0.275,
        "EW_total_residual_dex": -0.520,
        "fraction_of_EW_missing_in_slope": 0.0422 / 0.275,
        "note": "连续谱形状偏移仅为线缺失的 ~15%（全样本）/~23%（10-20kK 档）；方向与线->连续谱转移一致但不满足 1:1 守恒"
    },
    "outlier": {"gid": 1179907093365481088, "B_MG": 8.3, "res_b1_diff": 47.778,
                "reason": "归一化退化（<10 掩码点回退 median）", "action": "R3 剔除（|res_b1|>0.5）"}
}
with io.open(os.path.join(BASE, "paperX_wd_continuum_reg.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", os.path.join(BASE, "paperX_wd_continuum_reg.json"))
