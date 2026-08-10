#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨源相桥模块（paperX_shale_c_endpoint_bridge.py）单元测试
========================================================
覆盖：
  1. 校准线拟合正确性（精确线性恢复 slope/intercept/R²/Spearman，NaN 过滤，样本不足报错）
  2. 不同成熟度范围：低熟窗（Ro 0.5-0.9）/ 中熟窗（1.0-1.4）/ 高熟窗（1.4-2.0）
  3. 不同指标范围：窄范围（MDI 0.40-0.50）/ 宽范围（0.10-0.90）
  4. inverse / direct 两种外推模式；标量与数组输入
  5. 偏差与偏差上界、外推越界标记、R²<0.3 诚实登记、bootstrap CI
  6. 长度不匹配报错；真实数据集成测试（复现 §9.7 [D] 乌马营数值）

运行：python scripts/paperX_shale_c_endpoint_bridge_test.py
"""
import os
import sys
import unittest

import numpy as np

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from paperX_shale_c_endpoint_bridge import fit_calibration, endpoint_bridge

# ---------------- 合成数据工厂 ----------------
def exact_line(ro_min, ro_max, n=12, slope=0.30, intercept=-0.10, noise=0.0, seed=0):
    """ro（成熟度）均匀网格 + 精确线性 mdi = slope*ro + intercept（可选噪声）。"""
    ro = np.linspace(ro_min, ro_max, n)
    mdi = slope * ro + intercept
    if noise > 0:
        rng = np.random.default_rng(seed)
        mdi = mdi + rng.normal(0, noise, n)
    return ro, mdi


class TestFitCalibration(unittest.TestCase):
    """校准线拟合（源体系）"""

    def test_exact_linear_recovers_slope_intercept(self):
        ro, mdi = exact_line(0.5, 2.0)
        cal = fit_calibration(ro, mdi, index_name="MDI", maturity_name="Ro")
        self.assertAlmostEqual(cal["slope"], 0.30, places=6)
        self.assertAlmostEqual(cal["intercept"], -0.10, places=6)
        self.assertGreater(cal["r2"], 0.9999)
        self.assertAlmostEqual(cal["rho_s"], 1.0, places=6)
        self.assertEqual(cal["n"], 12)

    def test_nan_filtering(self):
        ro, mdi = exact_line(0.5, 2.0)
        ro_nan = np.where(np.arange(len(ro)) % 3 == 0, np.nan, ro)
        mdi_nan = np.where(np.arange(len(mdi)) % 5 == 0, np.nan, mdi)
        cal_clean = fit_calibration(ro, mdi)
        cal_nan = fit_calibration(ro_nan, mdi_nan)
        # 任一位置被 NaN 剔除后，剩余样本应一致
        keep = np.isfinite(ro_nan) & np.isfinite(mdi_nan)
        self.assertEqual(cal_nan["n"], int(keep.sum()))
        self.assertAlmostEqual(cal_nan["slope"], cal_clean["slope"], places=9)
        self.assertAlmostEqual(cal_nan["intercept"], cal_clean["intercept"], places=9)

    def test_too_few_samples_raises(self):
        with self.assertRaises(ValueError):
            fit_calibration([0.6, 0.8], [0.08, 0.14])  # n=2 < 3

    def test_all_nan_raises(self):
        with self.assertRaises(ValueError):
            fit_calibration([np.nan] * 5, [0.1] * 5)


class TestMaturityWindows(unittest.TestCase):
    """不同成熟度范围"""

    def _check_window(self, ro_min, ro_max, target_mdi, expect_ro):
        # 带噪数据：拟合 slope/intercept 与解析值有 ~0.02 级偏差，断言用 atol=0.03
        ro, mdi = exact_line(ro_min, ro_max, noise=0.02, seed=1)
        res = endpoint_bridge(ro, mdi, target_mdi, index_name="MDI",
                              maturity_name="Ro", mode="inverse")
        self.assertAlmostEqual(res["ro_pred"][0], expect_ro, delta=0.03)
        self.assertFalse(res["extrapolate"], "目标指标应在校准范围内")
        return res

    def test_low_maturity_window(self):
        # 低熟窗 Ro 0.5-0.9：mdi=0.30*ro-0.10 → 0.05~0.17
        self._check_window(0.5, 0.9, 0.12, (0.12 + 0.10) / 0.30)

    def test_mid_maturity_window(self):
        # 中熟窗 Ro 1.0-1.4：mdi=0.20~0.32
        self._check_window(1.0, 1.4, 0.26, (0.26 + 0.10) / 0.30)

    def test_high_maturity_window(self):
        # 高熟窗 Ro 1.4-2.0：mdi=0.32~0.50
        self._check_window(1.4, 2.0, 0.46, (0.46 + 0.10) / 0.30)


class TestIndexRanges(unittest.TestCase):
    """不同指标范围"""

    def test_narrow_index_range(self):
        # 窄范围（STGL 型 MDI 0.40-0.50）：精确线性内预测
        ro = np.linspace(1.35, 1.65, 10)
        mdi = 0.30 * ro - 0.10          # 0.305~0.395
        mdi_narrow = mdi + 0.10         # 平移至 0.405~0.495
        res = endpoint_bridge(ro, mdi_narrow, 0.46, mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        self.assertAlmostEqual(res["ro_pred"][0], (0.46 - 0.00) / 0.30, places=2)
        self.assertFalse(res["extrapolate"])
        self.assertEqual(len(res["ro_pred"]), 1)

    def test_wide_index_range(self):
        # 宽范围 MDI 0.10-0.90：两端均能预测
        ro = np.linspace(0.7, 3.3, 20)
        mdi = 0.30 * ro - 0.10          # 0.11~0.89
        res = endpoint_bridge(ro, mdi, [0.15, 0.85], mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        np.testing.assert_allclose(res["ro_pred"], [(0.15 + 0.10) / 0.30,
                                                    (0.85 + 0.10) / 0.30], atol=1e-9)
        self.assertFalse(res["extrapolate"])


class TestBridgeModes(unittest.TestCase):
    """inverse / direct 两种外推模式 + 输入形态"""

    def test_inverse_matches_analytic(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, 0.46, mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        self.assertAlmostEqual(res["ro_pred"][0], (0.46 + 0.10) / 0.30, places=9)

    def test_direct_matches_analytic(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, 0.46, mode="direct",
                              index_name="MDI", maturity_name="Ro")
        # 精确线性下 direct 与 inverse 等价：ro = (mdi+0.10)/0.30
        self.assertAlmostEqual(res["ro_pred"][0], (0.46 + 0.10) / 0.30, places=9)

    def test_scalar_input(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, 0.46, mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        self.assertEqual(res["target_index"].ndim, 1)
        self.assertEqual(res["target_index"].shape, (1,))

    def test_array_input(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, [0.40, 0.46, 0.50], mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        self.assertEqual(len(res["ro_pred"]), 3)

    def test_invalid_mode_raises(self):
        ro, mdi = exact_line(0.5, 2.0)
        with self.assertRaises(ValueError):
            endpoint_bridge(ro, mdi, 0.46, mode="bogus")

    def test_mismatched_maturity_length_raises(self):
        ro, mdi = exact_line(0.5, 2.0)
        with self.assertRaises(ValueError):
            endpoint_bridge(ro, mdi, [0.40, 0.46], target_maturity=[1.2, 1.3, 1.4])

    def test_scalar_observed_repeats(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, [0.40, 0.46], target_maturity=1.25,
                              mode="inverse", index_name="MDI", maturity_name="Ro")
        self.assertEqual(len(res["maturity_observed"]), 2)
        np.testing.assert_array_equal(res["maturity_observed"], [1.25, 1.25])


class TestBridgeSemantics(unittest.TestCase):
    """偏差、越界、诚实登记、bootstrap"""

    def test_deviation_and_upper_bound(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, [0.46, 0.49, 0.51],
                              target_maturity=[1.25, 1.25, 1.25], mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        ro_true = (np.array([0.46, 0.49, 0.51]) + 0.10) / 0.30
        np.testing.assert_allclose(res["ro_pred"], ro_true, atol=1e-9)
        np.testing.assert_allclose(res["deviation"], ro_true - 1.25, atol=1e-9)
        self.assertAlmostEqual(res["deviation_upper_bound"],
                               float(np.abs(ro_true - 1.25).max()), places=9)

    def test_no_observed_gives_no_deviation(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, 0.46, mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        self.assertIsNone(res["maturity_observed"])
        self.assertIsNone(res["deviation"])
        self.assertIsNone(res["deviation_upper_bound"])

    def test_extrapolate_flag(self):
        ro, mdi = exact_line(0.5, 2.0)   # mdi 范围 0.05~0.50
        inside = endpoint_bridge(ro, mdi, 0.40, mode="inverse",
                                 index_name="MDI", maturity_name="Ro")
        outside = endpoint_bridge(ro, mdi, 0.80, mode="inverse",
                                  index_name="MDI", maturity_name="Ro")
        self.assertFalse(inside["extrapolate"])
        self.assertTrue(outside["extrapolate"])
        self.assertIn("越出校准范围", outside["confidence_note"])
        self.assertIn("外推", outside["summary"])

    def test_low_r2_honesty_note(self):
        # 高噪声 → R²<0.3 → 诚实登记"粗略"
        rng = np.random.default_rng(7)
        ro = np.linspace(1.0, 1.5, 20)
        mdi = 0.05 * ro + rng.normal(0, 0.08, 20)   # 信号弱、噪声大
        res = endpoint_bridge(ro, mdi, 0.40, mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        self.assertLess(res["calibration"]["r2"], 0.3)
        self.assertIn("粗略", res["confidence_note"])

    def test_strong_calibration_no_note(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, 0.46, mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        self.assertGreater(res["calibration"]["r2"], 0.99)
        self.assertEqual(res["confidence_note"], "校准可用")

    def test_bootstrap_ci(self):
        # 低噪声精确线性：bootstrap CI 应窄且包含精确预测值
        ro, mdi = exact_line(0.5, 2.0, noise=0.01, seed=3)
        res = endpoint_bridge(ro, mdi, 0.46, mode="inverse", n_boot=300, seed=0,
                              index_name="MDI", maturity_name="Ro")
        self.assertIsNotNone(res["ci_low"])
        self.assertIsNotNone(res["ci_high"])
        truth = (0.46 + 0.10) / 0.30
        self.assertLessEqual(res["ci_low"][0], res["ro_pred"][0])
        self.assertGreaterEqual(res["ci_high"][0], res["ro_pred"][0])
        self.assertLessEqual(res["ci_low"][0], truth)
        self.assertGreaterEqual(res["ci_high"][0], truth)

    def test_no_bootstrap_by_default(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, 0.46, mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        self.assertIsNone(res["ci_low"])

    def test_summary_contains_key_values(self):
        ro, mdi = exact_line(0.5, 2.0)
        res = endpoint_bridge(ro, mdi, [0.46, 0.49, 0.51],
                              target_maturity=[1.25] * 3, mode="inverse",
                              index_name="MDI", maturity_name="Ro")
        for token in ["MDI = 0.3000*Ro -0.1000", "R²=", "偏差"]:
            self.assertIn(token, res["summary"])


class TestRealDataReproduction(unittest.TestCase):
    """集成：真实古龙数据复现 §9.7 [D] 乌马营数值"""

    CSV = os.path.join(_SCRIPT_DIR, "data", "gulong_bai2025", "bai2025_gulong_table3.csv")

    @unittest.skipUnless(os.path.exists(CSV), "古龙数据文件缺失，跳过集成测试")
    def test_wumaying_bridge_values(self):
        import pandas as pd
        df = pd.read_csv(self.CSV)
        for c in ["MD1", "MD3", "MD4"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df["MDI"] = df["MD4"] / (df["MD1"] + df["MD3"] + df["MD4"])
        g = df.dropna(subset=["MDI", "Ro_pct"])

        res = endpoint_bridge(
            cal_maturity=g["Ro_pct"], cal_index=g["MDI"],
            target_index=np.array([0.46, 0.49, 0.51]),
            target_maturity=np.array([1.25, 1.25, 1.25]),
            index_name="MDI", maturity_name="Ro(%)",
            mode="inverse", n_boot=0,
        )
        # 复现 §9.7 [D]：MDI 0.46/0.49/0.51 -> Ro 1.75/1.83/1.89%，偏差 +0.50/+0.58/+0.64
        np.testing.assert_allclose(res["ro_pred"], [1.75, 1.83, 1.89], atol=0.01)
        np.testing.assert_allclose(res["deviation"], [0.50, 0.58, 0.64], atol=0.01)
        self.assertEqual(res["calibration"]["n"], len(g))
        self.assertIn("粗略", res["confidence_note"])   # 真实校准线 R²≈0.21 < 0.3


if __name__ == "__main__":
    unittest.main(verbosity=2)
