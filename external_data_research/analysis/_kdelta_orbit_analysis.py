"""
k(Δ) 连续轨道分析 —— 从原始 CSV 计算等效静默层数的实值轨道
严格复现 find_stable_islands() 的窗口算法（±5 点），仅去掉 ⌈·⌉ 取整
输出：
  1. 四种拓扑的 k(Δ) vs Δ 叠加图（含稳定岛阴影 + 阈值线）
  2. 链式、星形、环形的独立放大图（标注平台区数值）
  3. 控制台汇总：各拓扑 k(Δ) 平台区均值、方差、阈值穿越点
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# ---- 中文字体（修复 Windows 乱码） ----
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern，支持 U+2212

# ---- 参数（与 stable_island_geometry.py 完全一致） ----
WINDOW_HALF = 5
STABILITY_THETA = 0.1
MIN_WIDTH = 0.02
S4 = 1.0 / 15.0
LN_S4_INV = np.log(1.0 / S4)  # ln(15) ≈ 2.70805

# ---- 路径 ----
BASE = Path(r"e:\workspace\hyper-resolution\external_data_research\稳定岛：神秘的新世界\寻找稳定岛超密集测试3")
OUT_DIR = Path(r"e:\workspace\hyper-resolution\external_data_research\analysis")
CSV_LIST = [
    ("chain",       "stable_island_chain.csv"),
    ("star",        "stable_island_star.csv"),
    ("ring",        "stable_island_ring.csv"),
    ("small_world", "stable_island_small_world.csv"),
]

LABEL_MAP = {
    "chain":       "链式 (Chain)",
    "star":        "星形 (Star)",
    "ring":        "环形 (Ring)",
    "small_world": "小世界 (Small World, p=0.1)",
}
COLOR_MAP = {
    "chain":       "#1f77b4",
    "star":        "#d62728",
    "ring":        "#2ca02c",
    "small_world": "#9467bd",
}

# ---- 工具：CSV 读取（忽略首行 # 注释） ----
def load_csv(path: Path):
    raw = np.loadtxt(path, delimiter=",", comments="#")
    delta = raw[:, 0]
    fine  = raw[:, 3]
    return delta, fine

# ---- 工具：逐点滑动窗口 local_std（与 find_stable_islands() 逐行一致） ----
def sliding_local_std(fine, half=WINDOW_HALF):
    N = len(fine)
    out = np.zeros(N)
    for i in range(N):
        lo = max(0, i - half)
        hi = min(N, i + half + 1)  # +1 因为 Python slice 右端不包含
        out[i] = np.std(fine[lo:hi])
    return out

# ---- 工具：稳定岛识别（与 find_stable_islands() 完全一致，返回边界索引） ----
def detect_islands(delta, fine, global_std, theta=STABILITY_THETA, min_width=MIN_WIDTH):
    N = len(delta)
    islands = []
    in_isl = False
    start_i = 0
    local_stab = sliding_local_std(fine) / (global_std if global_std > 1e-12 else 1.0)
    for i in range(1, N):
        if local_stab[i] < theta and not in_isl:
            in_isl = True
            start_i = i
        elif local_stab[i] >= theta and in_isl:
            in_isl = False
            end_i = i
            if delta[end_i] - delta[start_i] >= min_width:
                mask = (delta >= delta[start_i]) & (delta <= delta[end_i])
                isl_std = np.std(fine[mask])
                islands.append((start_i, end_i, isl_std))
    # ---- 边界处理：扫描结束仍在岛内（全范围或尾段大岛） ----
    if in_isl:
        end_i = N - 1
        if delta[end_i] - delta[start_i] >= min_width:
            mask = (delta >= delta[start_i]) & (delta <= delta[end_i])
            isl_std = np.std(fine[mask])
            islands.append((start_i, end_i, isl_std))
    return islands

# =================================================================
# 主计算
# =================================================================
results = {}   # graph -> dict(delta, fine, local_std, local_stab, k_delta, islands, global_std, gmean_k)

for gname, fname in CSV_LIST:
    path = BASE / fname
    if not path.exists():
        print(f"[SKIP] {fname} not found")
        continue
    delta, fine = load_csv(path)
    global_std = np.std(fine)
    local_std = sliding_local_std(fine)
    local_stab = local_std / (global_std if global_std > 1e-12 else 1.0)
    # 连续 k(Δ)：取消 ⌈·⌉，直接取实值
    with np.errstate(divide="ignore", invalid="ignore"):
        k_delta = np.log(np.maximum(local_stab, 1e-18)) / (-LN_S4_INV)  # ln(R)/ln(1/15) = -ln(R)/ln15
    islands = detect_islands(delta, fine, global_std)
    # 平台区指标：取岛内 Δ 范围的 k(Δ) 均值 & std
    plateau_stats = []
    for (si, ei, isl_std) in islands:
        mask = np.arange(len(delta)) >= si
        mask &= np.arange(len(delta)) <= ei
        k_plat = k_delta[mask]
        plateau_stats.append({
            "delta_lo": delta[si], "delta_hi": delta[ei],
            "k_mean":  np.mean(k_plat),
            "k_std":   np.std(k_plat),
            "k_min":   np.min(k_plat),
            "k_max":   np.max(k_plat),
            "n_pts":   int(mask.sum()),
        })
    results[gname] = {
        "delta": delta, "fine": fine,
        "local_std": local_std, "local_stab": local_stab,
        "k_delta": k_delta, "islands": islands,
        "global_std": global_std,
        "plateaus": plateau_stats,
    }
    # ---- 控制台汇总 ----
    print(f"\n{'='*60}")
    print(f"拓扑 = {LABEL_MAP[gname]}")
    print(f"  global_std(fine) = {global_std:.6e}")
    print(f"  识别稳定岛数     = {len(islands)}")
    for j, p in enumerate(plateau_stats, 1):
        print(f"  岛 #{j}: Δ∈[{p['delta_lo']:.3f}, {p['delta_hi']:.3f}]"
              f"  width={p['delta_hi']-p['delta_lo']:.3f}"
              f"  k_mean={p['k_mean']:.3f} ± {p['k_std']:.4f}"
              f"  k∈[{p['k_min']:.3f}, {p['k_max']:.3f}]"
              f"  N_pts={p['n_pts']}")

# =================================================================
# 图 1：四种拓扑 k(Δ) 叠加全景图
# =================================================================
plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3})
fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# 1a: k(Δ) 轨道 + 稳定岛阴影 + 阈值参考线
ax = axes[0]
k_threshold = np.log(STABILITY_THETA) / (-LN_S4_INV)  # θ=0.1 对应的 k
for gname in ["chain", "star", "ring", "small_world"]:
    if gname not in results: continue
    r = results[gname]
    ax.plot(r["delta"], r["k_delta"], lw=1.2, color=COLOR_MAP[gname], label=LABEL_MAP[gname], alpha=0.9)
    for (si, ei, _) in r["islands"]:
        ax.axvspan(r["delta"][si], r["delta"][ei], color=COLOR_MAP[gname], alpha=0.12, lw=0)
ax.axhline(k_threshold, color="black", ls="--", lw=1.3, label=f"阈值 k(θ=0.1) = {k_threshold:.3f}")
ax.axhline(1.87, color="gray", ls=":", lw=1.0, alpha=0.6, label="链式 Δ_c 反算 k=1.87")
ax.set_ylabel(r"连续等效静默层数 $k(\Delta) = \ln(R) / \ln(1/15)$（实值，不取整）")
ax.set_title(r"$k(\Delta)$ 连续轨道全景（四种拓扑）—— 阴影 = 稳定岛识别范围，虚线 = θ=0.1 阈值")
ax.legend(loc="upper right", fontsize=9)
ax.set_ylim(0, 10)

# 1b: local_stability = local_std/global_std（入/出岛判定的直接量）
ax = axes[1]
for gname in ["chain", "star", "ring", "small_world"]:
    if gname not in results: continue
    r = results[gname]
    ax.semilogy(r["delta"], np.maximum(r["local_stab"], 1e-10), lw=1.2,
                color=COLOR_MAP[gname], label=LABEL_MAP[gname], alpha=0.9)
ax.axhline(STABILITY_THETA, color="black", ls="--", lw=1.3, label=f"入岛阈值 θ = 0.1")
ax.set_xlabel(r"矛盾边耦合强度 $\Delta$")
ax.set_ylabel(r"局部稳定性 $\sigma_{\text{local}} / \sigma_{\text{global}}$（对数坐标）")
ax.legend(loc="lower right", fontsize=9)
ax.set_ylim(1e-9, 1.5)

plt.tight_layout()
out1 = OUT_DIR / "kdelta_orbit_panorama.png"
fig.savefig(out1, dpi=100)
plt.close(fig)
print(f"\n[保存] 全景图 -> {out1}")

# =================================================================
# 图 2：链式、星形、环形各自的 k(Δ) 放大图（标注平台区数值）
# =================================================================
fig, axes = plt.subplots(3, 1, figsize=(13, 11), sharex=True)
zoom_map = [("chain", axes[0]), ("star", axes[1]), ("ring", axes[2])]
for gname, ax in zoom_map:
    if gname not in results: continue
    r = results[gname]
    ax.plot(r["delta"], r["k_delta"], lw=1.4, color=COLOR_MAP[gname])
    for j, (si, ei, _) in enumerate(r["islands"], 1):
        dlo, dhi = r["delta"][si], r["delta"][ei]
        ax.axvspan(dlo, dhi, color=COLOR_MAP[gname], alpha=0.15, lw=0)
        # 取平台区 k 均值作为标注
        if r["plateaus"] and j-1 < len(r["plateaus"]):
            p = r["plateaus"][j-1]
            ax.hlines(p["k_mean"], dlo, dhi, color=COLOR_MAP[gname], lw=2.2, ls="-", alpha=0.85)
            ax.text((dlo+dhi)/2, p["k_mean"] + 0.08,
                    f"#{j}  $\\bar{{k}}$={p['k_mean']:.2f}$\\pm${p['k_std']:.3f}\nΔ∈[{dlo:.2f},{dhi:.2f}]",
                    ha="center", va="bottom", fontsize=9.5,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=COLOR_MAP[gname], alpha=0.85))
    ax.axhline(k_threshold, color="black", ls="--", lw=1.0, alpha=0.7, label=f"阈值 k(θ=0.1)={k_threshold:.3f}")
    ax.set_ylabel(f"{LABEL_MAP[gname]}\n" + r"$k(\Delta)$")
    ax.set_ylim(0, 6)
    ax.legend(loc="upper right", fontsize=8.5)

axes[-1].set_xlabel(r"矛盾边耦合强度 $\Delta$")
axes[0].set_title(r"各拓扑 $k(\Delta)$ 连续轨道放大 —— 标注平台区均值与方差（平台平坦=弱波动为连续轨道成立判据）")
plt.tight_layout()
out2 = OUT_DIR / "kdelta_orbit_zoom.png"
fig.savefig(out2, dpi=100)
plt.close(fig)
print(f"[保存] 放大图 -> {out2}")

# =================================================================
# 平台区存在性定量判定（控制台）
# =================================================================
print(f"\n{'='*60}")
print("平台区存在性定量判定：")
print(f"  阈值 k(θ=0.1) = {k_threshold:.4f}")
CRITERION = 0.3  # 平台区相对波动 < 30% 视为有效平台
for gname in ["chain", "star", "ring", "small_world"]:
    if gname not in results: continue
    r = results[gname]
    if not r["plateaus"]:
        if gname == "small_world" and r["global_std"] < 1e-7:
            # 小世界特殊判断：全域 k 值极高且平坦
            k_all = r["k_delta"]
            valid = np.isfinite(k_all)
            km, ks = np.mean(k_all[valid]), np.std(k_all[valid])
            rel = ks / max(km, 1e-9)
            verdict = "✓ 全域均匀静默（k 无岛，视为超稳定全局平台）" if rel < CRITERION else "✗"
            print(f"  {LABEL_MAP[gname]:<24s}:  k̄={km:.2f}±{ks:.3f}  rel_std={rel:.2%}  {verdict}")
        else:
            print(f"  {LABEL_MAP[gname]:<24s}:  无识别岛")
        continue
    for j, p in enumerate(r["plateaus"], 1):
        rel = p["k_std"] / max(p["k_mean"], 1e-9)
        verdict = "✓ 平台区存在" if rel < CRITERION else "✗ 平台区不显著（波动大）"
        print(f"  {LABEL_MAP[gname]:<24s} 岛#{j}: k̄={p['k_mean']:.3f}±{p['k_std']:.4f}  "
              f"rel_std={rel:.2%}  {verdict}")
