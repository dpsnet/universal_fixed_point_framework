"""
小世界拓扑 k(Δ) 数据导出 —— 供报告表格插入
输出两个 CSV：
  1. smallworld_kdelta_series.csv  —— 逐点 k(Δ) 序列（Δ, local_std, local_stab, k_delta）
  2. smallworld_kdelta_summary.csv —— 汇总统计（平台均值、std、rel_std、范围、点数）
"""
import numpy as np
from pathlib import Path

WINDOW_HALF = 5
STABILITY_THETA = 0.1
MIN_WIDTH = 0.02
S4 = 1.0 / 15.0
LN_S4_INV = np.log(1.0 / S4)  # ln(15)

BASE = Path(r"e:\workspace\hyper-resolution\external_data_research\稳定岛：神秘的新世界\寻找稳定岛超密集测试3")
OUT_DIR = Path(r"e:\workspace\hyper-resolution\external_data_research")
CSV_IN = BASE / "stable_island_small_world.csv"


def load_csv(path):
    raw = np.loadtxt(path, delimiter=",", comments="#")
    return raw[:, 0], raw[:, 3]  # delta, fine


def sliding_local_std(fine, half=WINDOW_HALF):
    N = len(fine)
    out = np.zeros(N)
    for i in range(N):
        lo = max(0, i - half)
        hi = min(N, i + half + 1)
        out[i] = np.std(fine[lo:hi])
    return out


def main():
    delta, fine = load_csv(CSV_IN)
    global_std = np.std(fine)
    local_std = sliding_local_std(fine)
    local_stab = local_std / (global_std if global_std > 1e-12 else 1.0)
    k_delta = np.log(np.maximum(local_stab, 1e-18)) / (-LN_S4_INV)

    # 岛范围（小世界全域都是岛）
    mask_isl = np.ones(len(delta), dtype=bool)
    k_plat = k_delta[mask_isl]
    k_mean = float(np.mean(k_plat))
    k_std = float(np.std(k_plat))
    k_min = float(np.min(k_plat))
    k_max = float(np.max(k_plat))
    rel_std = k_std / k_mean

    # ---- 序列 CSV ----
    out_series = OUT_DIR / "smallworld_kdelta_series.csv"
    header = "delta,local_std,local_stability,k_delta"
    data = np.column_stack([delta, local_std, local_stab, k_delta])
    np.savetxt(out_series, data, delimiter=",", header=header, comments="", fmt="%.10e")
    print(f"[保存] 序列 CSV -> {out_series}  (N={len(delta)} 行)")

    # ---- 汇总 CSV ----
    out_summary = OUT_DIR / "smallworld_kdelta_summary.csv"
    with open(out_summary, "w", encoding="utf-8") as f:
        f.write("metric,value\n")
        f.write(f"graph_type,small_world\n")
        f.write(f"N_points,{len(delta)}\n")
        f.write(f"delta_min,{delta.min():.6f}\n")
        f.write(f"delta_max,{delta.max():.6f}\n")
        f.write(f"global_std_fine,{global_std:.10e}\n")
        f.write(f"island_range_delta_lo,{delta.min():.6f}\n")
        f.write(f"island_range_delta_hi,{delta.max():.6f}\n")
        f.write(f"island_width,{delta.max()-delta.min():.6f}\n")
        f.write(f"k_mean,{k_mean:.6f}\n")
        f.write(f"k_std,{k_std:.6f}\n")
        f.write(f"k_min,{k_min:.6f}\n")
        f.write(f"k_max,{k_max:.6f}\n")
        f.write(f"rel_std_percent,{rel_std*100:.4f}\n")
        f.write(f"ceiling_k,{int(np.ceil(k_mean))}\n")
        f.write(f"plateau_verdict,{('PASS' if rel_std < 0.3 else 'FAIL')} (criterion rel_std<30%)\n")
    print(f"[保存] 汇总 CSV -> {out_summary}")

    # 控制台回显
    print(f"\n=== 小世界 k(Δ) 汇总 ===")
    print(f"  Δ 范围       : [{delta.min():.3f}, {delta.max():.3f}]")
    print(f"  N 点数       : {len(delta)}")
    print(f"  global_std   : {global_std:.4e}")
    print(f"  k_mean       : {k_mean:.4f}")
    print(f"  k_std        : {k_std:.4f}")
    print(f"  k_min/max    : [{k_min:.4f}, {k_max:.4f}]")
    print(f"  rel_std      : {rel_std*100:.4f}%")
    print(f"  ⌈k_mean⌉     : {int(np.ceil(k_mean))}")


if __name__ == "__main__":
    main()
