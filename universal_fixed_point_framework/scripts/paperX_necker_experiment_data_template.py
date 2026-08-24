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
"""
Necker 立方体临界慢化实验：数据记录模板
===========================================

对应 notes/04_lorentz_gravity/sensory_integration_time_ruler.md §7.8.5 的
综合实验流程。提供 pandas DataFrame 字段定义、示例数据生成、数据验证与
基础描述统计函数。

字段覆盖四类信息：
  1. 试次元数据（subject, session, block, trial, stimulus_id, ambiguity）
  2. 行为反应（rt, choice, correct/w congruent with manipulation）
  3. 生理/眼动指标（pupil, gaze, heart_rate, eeg_segment_id）
  4. 预处理/质控（excluded, exclude_reason, valid）

运行命令：
    python scripts/paperX_necker_experiment_data_template.py
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

import numpy as np
import pandas as pd


# -----------------------------------------------------------------------------
# 1. 字段定义（schema）
# -----------------------------------------------------------------------------

SCHEMA: Dict[str, Dict[str, Any]] = {
    # --- 试次元数据 ---
    "subject_id": {
        "dtype": "str",
        "description": "被试唯一标识",
        "example": "S001",
    },
    "session_id": {
        "dtype": "str",
        "description": "实验会话标识（同一被试可有多 session）",
        "example": "S001_01",
    },
    "block_id": {
        "dtype": "str",
        "description": "区块标识，用于平衡顺序效应",
        "example": "B03",
    },
    "trial_id": {
        "dtype": "str",
        "description": "试次唯一标识（UUID 或全局递增编号）",
        "example": "a1b2c3d4",
    },
    "trial_number": {
        "dtype": "int",
        "description": "当前 session 内的试次序号",
        "example": 42,
    },
    "stimulus_id": {
        "dtype": "str",
        "description": "刺激文件/参数集标识",
        "example": "necklace_012",
    },
    "ambiguity": {
        "dtype": "float",
        "description": "刺激模糊度等级 δ，范围建议 [-1, 1] 或 [0, 1]；0 为边界",
        "example": 0.15,
        "valid_range": (-1.0, 1.0),
    },
    "ambiguity_signed": {
        "dtype": "float",
        "description": "带符号模糊度（正=A 占优，负=B 占优），等于 signed distance to boundary",
        "example": 0.15,
    },
    "condition": {
        "dtype": "str",
        "description": "实验条件标签，如 'adaptation', 'control', 'high_arousal'",
        "example": "control",
    },
    "timestamp_onset": {
        "dtype": "datetime64[ns]",
        "description": "刺激呈现 onset 时间（UTC 或本地时间）",
        "example": "2026-08-20T14:30:01.123456",
    },
    "timestamp_offset": {
        "dtype": "datetime64[ns]",
        "description": "被试反应或刺激消失 offset 时间",
        "example": "2026-08-20T14:30:02.456789",
    },

    # --- 行为反应 ---
    "choice": {
        "dtype": "str",
        "description": "被试报告：'A' 或 'B'；缺失为 NaN",
        "example": "A",
        "categories": ["A", "B"],
    },
    "choice_encoded": {
        "dtype": "float",
        "description": "choice 的数值编码：A=+1, B=-1, 缺失=NaN",
        "example": 1.0,
    },
    "rt_ms": {
        "dtype": "float",
        "description": "反应时，单位毫秒（ms）",
        "example": 850.0,
        "valid_range": (150.0, 5000.0),
    },
    "is_correct": {
        "dtype": "boolean",
        "description": "对于偏向性刺激，choice 是否与真实占优方向一致；中性刺激为 NaN",
        "example": True,
    },
    "timed_out": {
        "dtype": "boolean",
        "description": "是否超过最大反应时限未做反应",
        "example": False,
    },
    "response_device": {
        "dtype": "str",
        "description": "反应设备，如 'keyboard', 'button_box', 'mouse'",
        "example": "keyboard",
    },

    # --- 眼动指标 ---
    "gaze_x": {
        "dtype": "float",
        "description": "刺激呈现期间平均注视点 X 坐标（屏幕像素或归一化）",
        "example": 0.02,
    },
    "gaze_y": {
        "dtype": "float",
        "description": "刺激呈现期间平均注视点 Y 坐标",
        "example": -0.01,
    },
    "fixation_duration_ms": {
        "dtype": "float",
        "description": "刺激呈现期间注视持续时间（ms），用于注意力控制",
        "example": 780.0,
    },
    "blinks_count": {
        "dtype": "int",
        "description": "刺激呈现期间眨眼次数",
        "example": 0,
    },
    "saccades_count": {
        "dtype": "int",
        "description": "刺激呈现期间眼跳次数",
        "example": 1,
    },

    # --- 瞳孔指标 ---
    "pupil_baseline_mm": {
        "dtype": "float",
        "description": "刺激前 500 ms 基线瞳孔直径（mm 或任意单位）",
        "example": 3.5,
    },
    "pupil_mean_mm": {
        "dtype": "float",
        "description": "刺激呈现期间平均瞳孔直径",
        "example": 3.62,
    },
    "pupil_peak_mm": {
        "dtype": "float",
        "description": "刺激呈现期间瞳孔直径峰值",
        "example": 3.75,
    },
    "pupil_auc": {
        "dtype": "float",
        "description": "刺激呈现期间瞳孔直径曲线下面积（AUC），作为唤醒度 proxy",
        "example": 1200.0,
    },
    "pupil_quality": {
        "dtype": "float",
        "description": "瞳孔数据质量比例（0–1），低于阈值需标记 excluded",
        "example": 0.96,
    },

    # --- 心血管/唤醒度指标 ---
    "hr_baseline_bpm": {
        "dtype": "float",
        "description": "刺激前基线心率（次/分）",
        "example": 72.0,
    },
    "hr_mean_bpm": {
        "dtype": "float",
        "description": "刺激呈现期间平均心率",
        "example": 74.5,
    },
    "hrv_rmssd_ms": {
        "dtype": "float",
        "description": "刺激间期心率变异性 RMSSD（ms），作为副交感神经指标",
        "example": 45.0,
    },

    # --- EEG/MEG 元数据 ---
    "eeg_segment_id": {
        "dtype": "str",
        "description": "对应 EEG/MEG 分段标识，用于后续谱分析",
        "example": "seg_001_042",
    },
    "eeg_epoch_quality": {
        "dtype": "float",
        "description": "EEG epoch 质量评分（0–1）",
        "example": 0.92,
    },
    "alpha_power_pre": {
        "dtype": "float",
        "description": "刺激前 8–13 Hz alpha 波段功率（对数变换后）",
        "example": 1.23,
    },

    # --- 适应/先验控制 ---
    "previous_choice": {
        "dtype": "str",
        "description": "前一有效试次的 choice，用于分析序列效应/适应",
        "example": "B",
    },
    "run_length": {
        "dtype": "int",
        "description": "当前知觉态连续重复的次数（用于双稳态任务）",
        "example": 3,
    },
    "adaptation_duration_ms": {
        "dtype": "float",
        "description": "若使用适应范式，适应刺激持续时间（ms）；无适应为 0",
        "example": 0.0,
    },

    # --- 预处理/质控 ---
    "excluded": {
        "dtype": "boolean",
        "description": "该试次是否被排除出分析",
        "example": False,
    },
    "exclude_reason": {
        "dtype": "str",
        "description": "排除原因，如 'timeout', 'too_fast', 'bad_eye', 'missing_eeg'",
        "example": "",
    },
    "valid": {
        "dtype": "boolean",
        "description": "是否通过所有质控且可用于主分析",
        "example": True,
    },
}

# 推荐输出列顺序
COLUMN_ORDER: List[str] = [
    "subject_id",
    "session_id",
    "block_id",
    "trial_id",
    "trial_number",
    "stimulus_id",
    "ambiguity",
    "ambiguity_signed",
    "condition",
    "timestamp_onset",
    "timestamp_offset",
    "choice",
    "choice_encoded",
    "rt_ms",
    "is_correct",
    "timed_out",
    "response_device",
    "gaze_x",
    "gaze_y",
    "fixation_duration_ms",
    "blinks_count",
    "saccades_count",
    "pupil_baseline_mm",
    "pupil_mean_mm",
    "pupil_peak_mm",
    "pupil_auc",
    "pupil_quality",
    "hr_baseline_bpm",
    "hr_mean_bpm",
    "hrv_rmssd_ms",
    "eeg_segment_id",
    "eeg_epoch_quality",
    "alpha_power_pre",
    "previous_choice",
    "run_length",
    "adaptation_duration_ms",
    "excluded",
    "exclude_reason",
    "valid",
]


# -----------------------------------------------------------------------------
# 2. 示例数据生成（用于测试模板）
# -----------------------------------------------------------------------------

def generate_example_data(
    n_subjects: int = 5,
    n_trials_per_subject: int = 300,
    ambiguity_levels: int = 12,
    seed: int = 42,
) -> pd.DataFrame:
    """生成一份符合本模板字段的示例数据集。"""
    rng = np.random.default_rng(seed)

    records: List[Dict[str, Any]] = []
    ambiguities = np.linspace(-1.0, 1.0, ambiguity_levels)

    for s in range(n_subjects):
        subject_id = f"S{s+1:03d}"
        session_id = f"{subject_id}_01"

        for t in range(n_trials_per_subject):
            amb = rng.choice(ambiguities)
            # 简单的知觉决策 toy 生成：越接近边界 RT 越长，加噪声
            distance_to_boundary = abs(amb)
            base_rt = 600.0 + 400.0 * np.exp(-3.0 * distance_to_boundary)
            rt = base_rt + rng.normal(0, 80.0)
            rt = max(180.0, min(rt, 3000.0))

            # 选择概率由 sigmoid 决定
            prob_a = 1.0 / (1.0 + np.exp(-8.0 * amb))
            choice = "A" if rng.random() < prob_a else "B"
            choice_enc = 1.0 if choice == "A" else -1.0
            is_correct = (choice == "A" and amb > 0) or (choice == "B" and amb < 0)
            if abs(amb) < 0.05:
                is_correct = pd.NA  # 中性刺激无 correctness

            timed_out = rng.random() < 0.02  # 2% 超时
            if timed_out:
                rt = np.nan
                choice = None
                choice_enc = np.nan
                is_correct = pd.NA

            record = {
                "subject_id": subject_id,
                "session_id": session_id,
                "block_id": f"B{(t // 50) + 1:02d}",
                "trial_id": str(uuid.uuid4())[:8],
                "trial_number": t + 1,
                "stimulus_id": f"necker_{int((amb + 1.0) * 100):03d}",
                "ambiguity": abs(amb),
                "ambiguity_signed": amb,
                "condition": "control",
                "timestamp_onset": pd.Timestamp.now(),
                "timestamp_offset": pd.Timestamp.now() + pd.Timedelta(milliseconds=float(rt if not np.isnan(rt) else 1000)),
                "choice": choice,
                "choice_encoded": choice_enc,
                "rt_ms": rt,
                "is_correct": is_correct,
                "timed_out": timed_out,
                "response_device": "keyboard",
                "gaze_x": rng.normal(0.0, 0.02),
                "gaze_y": rng.normal(0.0, 0.02),
                "fixation_duration_ms": float(rt if not np.isnan(rt) else 1000),
                "blinks_count": rng.integers(0, 2),
                "saccades_count": rng.integers(0, 3),
                "pupil_baseline_mm": rng.normal(3.5, 0.1),
                "pupil_mean_mm": rng.normal(3.6, 0.1),
                "pupil_peak_mm": rng.normal(3.75, 0.12),
                "pupil_auc": rng.normal(1200.0, 100.0),
                "pupil_quality": rng.uniform(0.85, 1.0),
                "hr_baseline_bpm": rng.normal(72.0, 5.0),
                "hr_mean_bpm": rng.normal(73.0, 5.0),
                "hrv_rmssd_ms": rng.normal(45.0, 8.0),
                "eeg_segment_id": f"seg_{subject_id}_{t+1:03d}",
                "eeg_epoch_quality": rng.uniform(0.80, 1.0),
                "alpha_power_pre": rng.normal(1.2, 0.2),
                "previous_choice": rng.choice(["A", "B"]),
                "run_length": rng.integers(1, 5),
                "adaptation_duration_ms": 0.0,
                "excluded": False,
                "exclude_reason": "",
                "valid": not timed_out,
            }
            records.append(record)

    df = pd.DataFrame(records)
    df = df[COLUMN_ORDER]
    # 将可空布尔列转换为 pandas nullable boolean dtype
    df["is_correct"] = df["is_correct"].astype("boolean")
    df["timed_out"] = df["timed_out"].astype("boolean")
    df["excluded"] = df["excluded"].astype("boolean")
    df["valid"] = df["valid"].astype("boolean")
    return df


# -----------------------------------------------------------------------------
# 3. 数据验证函数
# -----------------------------------------------------------------------------

def validate_dataframe(df: pd.DataFrame, raise_on_error: bool = False) -> pd.DataFrame:
    """
    验证 DataFrame 是否包含全部必需字段，并检查基础取值范围。
    返回包含错误信息的 DataFrame。
    """
    errors: List[Dict[str, Any]] = []

    # 检查必需字段
    for col, meta in SCHEMA.items():
        if col not in df.columns:
            errors.append({"column": col, "error": "missing_column", "message": f"缺少必需字段: {col}"})
            continue

        # 类型检查（简化版）
        expected = meta.get("dtype", "")
        if expected == "float" and not pd.api.types.is_float_dtype(df[col]):
            errors.append({"column": col, "error": "dtype", "message": f"{col} 应为 float"})
        elif expected == "int" and not pd.api.types.is_integer_dtype(df[col]):
            errors.append({"column": col, "error": "dtype", "message": f"{col} 应为 int"})
        elif expected == "boolean" and not pd.api.types.is_bool_dtype(df[col]):
            errors.append({"column": col, "error": "dtype", "message": f"{col} 应为 boolean"})

        # 取值范围检查
        if "valid_range" in meta and not df[col].dropna().empty:
            lo, hi = meta["valid_range"]
            out_of_range = df[col].dropna().lt(lo) | df[col].dropna().gt(hi)
            if out_of_range.any():
                errors.append({
                    "column": col,
                    "error": "out_of_range",
                    "message": f"{col} 存在 {out_of_range.sum()} 个超出范围 [{lo}, {hi}] 的值",
                })

    error_df = pd.DataFrame(errors)
    if raise_on_error and not error_df.empty:
        raise ValueError(f"数据验证失败：\n{error_df.to_string(index=False)}")
    return error_df


def apply_quality_control(df: pd.DataFrame) -> pd.DataFrame:
    """
    示例质控规则：标记超时、过快反应、眼动离开中心、瞳孔质量低、EEG 质量低的试次。
    返回新增 excluded/exclude_reason/valid 列的 DataFrame（不删除行，仅标记）。
    """
    df = df.copy()
    df["excluded"] = False
    df["exclude_reason"] = ""

    def flag(row):
        reasons = []
        if row["timed_out"]:
            reasons.append("timeout")
        if pd.notna(row["rt_ms"]) and row["rt_ms"] < 200:
            reasons.append("too_fast")
        if abs(row["gaze_x"]) > 0.15 or abs(row["gaze_y"]) > 0.15:
            reasons.append("off_center_gaze")
        if row["pupil_quality"] < 0.8:
            reasons.append("bad_pupil")
        if row["eeg_epoch_quality"] < 0.75:
            reasons.append("bad_eeg")
        return reasons

    reasons = df.apply(flag, axis=1)
    df["excluded"] = reasons.str.len() > 0
    df["exclude_reason"] = reasons.apply(lambda x: ";".join(x))
    df["valid"] = ~df["excluded"] & df["choice"].notna() & df["rt_ms"].notna()
    return df


# -----------------------------------------------------------------------------
# 4. 基础描述统计
# -----------------------------------------------------------------------------

def compute_subject_summary(df: pd.DataFrame) -> pd.DataFrame:
    """按 subject 和 ambiguity 汇总行为指标。"""
    valid = df[df["valid"]].copy()
    summary = (
        valid.groupby(["subject_id", "ambiguity_signed"])
        .agg(
            n=("trial_id", "count"),
            p_a=("choice_encoded", lambda x: np.nanmean(x == 1.0)),
            rt_mean=("rt_ms", "mean"),
            rt_median=("rt_ms", "median"),
            rt_std=("rt_ms", "std"),
            pupil_mean=("pupil_mean_mm", "mean"),
            hrv_mean=("hrv_rmssd_ms", "mean"),
        )
        .reset_index()
    )
    return summary


# -----------------------------------------------------------------------------
# 5. 主函数：生成示例并保存
# -----------------------------------------------------------------------------

def main():
    print("生成 Necker 立方体临界慢化实验示例数据 ...")
    df = generate_example_data(n_subjects=5, n_trials_per_subject=300)
    df = apply_quality_control(df)

    print("验证数据字段 ...")
    errors = validate_dataframe(df)
    if errors.empty:
        print("  ✓ 数据验证通过")
    else:
        print(f"  ✗ 发现 {len(errors)} 个验证错误")
        print(errors.to_string(index=False))

    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "necker_critical_slowing_example.csv"
    df.to_csv(out_path, index=False)
    print(f"\n示例数据已保存至 {out_path}")
    print(f"总试次数：{len(df)}，有效试次数：{df['valid'].sum()}")

    summary = compute_subject_summary(df)
    summary_path = out_dir / "necker_critical_slowing_subject_summary.csv"
    summary.to_csv(summary_path, index=False)
    print(f"被试摘要已保存至 {summary_path}")


if __name__ == "__main__":
    main()
