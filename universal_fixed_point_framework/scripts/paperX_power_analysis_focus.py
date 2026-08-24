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
Necker 临界慢化实验：N=24 被试的功效分析聚焦报告
==========================================================

基于 `scripts/paperX_power_analysis.py` 生成的 `data/necker_power_analysis.csv`，
提取 n_subjects=24 的所有设计，绘制功效随 trials_per_delta 变化的曲线，
并输出推荐设计的 CSV 摘要。

运行命令：
    python scripts/paperX_power_analysis_focus.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


def main():
    print("=" * 60)
    print("Necker 临界慢化实验：N=24 功效分析聚焦报告")
    print("=" * 60)

    in_path = Path("data") / "necker_power_analysis.csv"
    if not in_path.exists():
        print(f"错误：未找到 {in_path}，请先运行 scripts/paperX_power_analysis.py")
        return

    df = pd.read_csv(in_path)
    df_n24 = df[df["n_subjects"] == 24].copy().sort_values("n_trials_per_delta")

    if df_n24.empty:
        print("错误：CSV 中未找到 n_subjects=24 的数据")
        return

    print("\nN=24 时的功效表：")
    print(df_n24.to_string(index=False))

    # 推荐设计：达到 80% 功效且每被试总试次数最小的设计
    recommended = df_n24[df_n24["power"] >= 0.80].sort_values("total_trials_per_subject").iloc[0]
    print("\n推荐设计（N=24，达到 80% 功效且每被试负担最小）：")
    print(f"  被试数：{int(recommended['n_subjects'])}")
    print(f"  每 |δ| 等级试次数：{int(recommended['n_trials_per_delta'])}")
    print(f"  每被试总试次数：{int(recommended['total_trials_per_subject'])}")
    print(f"  实验总试次数：{int(recommended['total_trials'])}")
    print(f"  估计 γ 的标准误：{recommended['se_gamma']:.5f}")
    print(f"  估计功效：{recommended['power']:.6f}")

    # 保存聚焦 CSV
    out_csv = Path("data") / "necker_power_analysis_n24.csv"
    df_n24.to_csv(out_csv, index=False)
    print(f"\n聚焦 CSV 已保存至 {out_csv}")

    # 绘图
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df_n24["n_trials_per_delta"], df_n24["power"], 'o-', color='steelblue', lw=2, markersize=8)
    ax.axhline(0.80, color='red', linestyle='--', label="80% 功效阈值")
    rec_nt = int(recommended["n_trials_per_delta"])
    ax.axvline(rec_nt, color='green', linestyle=':', label=f"推荐设计：{rec_nt} trials/δ")
    ax.set_xlabel("每 |δ| 等级试次数")
    ax.set_ylabel("功效（检测到 γ≠1）")
    ax.set_title("N=24 被试：功效随每 δ 试次数的变化")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

    out_fig = Path("figs") / "paperX_power_analysis_n24.png"
    out_fig.parent.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_fig, dpi=150)
    print(f"聚焦图已保存至 {out_fig}")


if __name__ == "__main__":
    main()
