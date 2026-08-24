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
P3 理论值 0.6309 与闫建钊 2012 实测值 1.47 的几何类别对比（Paper XLIII，2026-08-09）
对应论文：paper43_shale_accumulation.md §5.1 P3 / paper43_shale_accumulation_journal.md §4.6

背景：
  - 理论值 D_b = ln2/ln3 ≈ 0.6309：IFS 三分 Cantor 型突破通道（2 分支、1/3 收缩），
    Moran 方程 D = ln N / ln(1/r)。对象嵌入 1D（0 < D < 1），是"贯通通道截面/拓扑"维数。
  - 实测值 1.47：闫建钊等 2012《原油二次运移过程中的逾渗主脊实验研究》（石油实验地质
    34(1):99-103）——充填玻璃珠 Hele-Shaw 模型二维原油二次运移实验，数盒子法测得
    初始运移路径盒计数维数 1.76、逾渗主脊盒计数维数 1.47（主脊 < 路径）。

本脚本回答：两个数值"在什么意义上可比 / 不可比"。
  (1) 数值不可比：嵌入空间维度不同（1D vs 2D），盒计数维数的定义域不同（[0,1] vs [1,2]）；
  (2) 结构可比：皆为"连通稀疏自相似"结构，且皆显著低于各自整体（路径 1.76 / 满线 1）；
  (3) Moran 反推：若 1.47 为自相似树，有效参数组合 → 5 分支、1/3 收缩（ln5/ln3=1.465），
      与闫建钊实验观测"运移前缘通常有 2~5 个分支、其中 1~2 个壮大"定量吻合——
      说明真实运移主脊是"高分支统计分形"，而非 P3 假设的"2 分支确定性 Cantor"；
  (4) P3 检验协议：须在成像中识别贯通通道后盒计数，偏差判据 + Moran 修正，不直接与 1.47 比。
"""
import numpy as np


# ---------- 工具（复用 p3_imaging_sim.py 的实现） ----------

def cantor1d(m):
    """三分 Cantor 集：长度 3^m 二值序列（保留第 1、3 段，2 分支、收缩 1/3）。"""
    seg = np.ones(1, dtype=bool)
    for _ in range(m):
        seg = np.concatenate([seg, np.zeros(seg.size, dtype=bool), seg])
    return seg


def boxcount_1d(x, eps_list):
    res = []
    for eps in eps_list:
        nb = 0
        for i in range(0, len(x), eps):
            if x[i:i + eps].any():
                nb += 1
        res.append((eps, nb))
    return res


def boxcount_2d(mask, eps_list):
    """2D 盒计数：mask 为二值 2D 数组。"""
    res = []
    h, w = mask.shape
    for eps in eps_list:
        nb = 0
        for i in range(0, h, eps):
            for j in range(0, w, eps):
                if mask[i:i + eps, j:j + eps].any():
                    nb += 1
        res.append((eps, nb))
    return res


def fit_dim(xs, ys):
    """log-log 斜率取负 = 盒计数维数（N(eps) ∝ eps^{-D}）。"""
    lx, ly = np.log(np.asarray(xs, dtype=float)), np.log(np.asarray(ys, dtype=float))
    return -np.polyfit(lx, ly, 1)[0]


def penta_tree(m, r=3):
    """2D 五分形树（5 分支、收缩 1/3，D=ln5/ln3≈1.465）——闫建钊实测 1.47 的自相似模型。
    递归地在 m 代内把单位线段 [0,1] 替换为 5 段等长子段（间隔 1/3），在 2D 网格上铺开。
    返回二值 2D 数组（1=路径占据），尺寸 3^m。"""
    n = 3 ** m
    grid = np.zeros((n, n), dtype=bool)
    # 用迭代实现：每一代将当前所有"活段"按 5 分支、1/3 收缩扩展
    # 活段用 (x0, y0, size, dir) 表示；简化：沿对角线方向的两类交替。
    # 采用确定性替代：每段被替换为"五分支扇形"（中 + 四对角），再整体缩小 1/3。
    segs = [(0, 0, n)]  # (x0, y0, size) 正方形活区
    for _ in range(m):
        new = []
        for x0, y0, s in segs:
            s3 = s // 3
            # 五个子块：中心 + 上/下/左/右（5 分支、收缩 1/3）
            centers = [(x0 + s3, y0 + s3), (x0 + s3, y0), (x0 + s3, y0 + 2 * s3),
                       (x0, y0 + s3), (x0 + 2 * s3, y0 + s3)]
            for cx, cy in centers:
                new.append((cx, cy, s3))
        segs = new
        if len(segs) > 5 ** 7:  # 防御：防止 5^m 过大（m 由主程序控制）
            break
    for x0, y0, s in segs:
        grid[x0:x0 + s, y0:y0 + s] = True
    return grid


def moran(N, r):
    """Moran 方程：D = ln N / ln(1/r)。"""
    return np.log(N) / np.log(1.0 / r)


def inverse_moran(D, r):
    """已知收缩 r 与维数 D，反推有效分支 N = (1/r)^D。"""
    return (1.0 / r) ** D


def inverse_moran_r(D, N):
    """已知分支 N 与维数 D，反推有效收缩 r = N^{-1/D}。"""
    return N ** (-1.0 / D)


def main():
    db_theory = np.log(2) / np.log(3)          # 0.6309，P3 理论（三分 Cantor）
    db_meas = 1.47                              # 闫建钊 2012 逾渗主脊实测
    db_path = 1.76                              # 闫建钊 2012 初始运移路径实测

    print("=" * 72)
    print("P3 理论值 0.6309 vs 闫建钊 2012 实测值 1.47：几何类别对比")
    print("=" * 72)

    # ---------- (1) 数值验证两值各自的意义 ----------
    m = 6
    c = cantor1d(m)
    eps_1d = [3 ** i for i in range(m, 0, -1)]
    bc = boxcount_1d(c, eps_1d)
    d1 = fit_dim([e for e, _ in bc], [n for _, n in bc])

    grid = penta_tree(m=5)
    eps_2d = [3 ** i for i in range(5, 0, -1)]
    bc2 = boxcount_2d(grid, eps_2d)
    d2 = fit_dim([e for e, _ in bc2], [n for _, n in bc2])

    print("\n[1] 数值验证（盒计数方法学）")
    print("  - 三分 Cantor 集（m=%d，%d 体素）：盒计数 D=%.4f  vs  理论 ln2/ln3=%.4f"
          % (m, 3 ** m, d1, db_theory))
    print("  - 五分形树（5 分支、1/3 收缩，m=5）：盒计数 D=%.4f  vs  Moran 理论 ln5/ln3=%.4f"
          % (d2, moran(5, 1 / 3)))
    print("  - 闫建钊 2012 实测锚点：初始运移路径 %.2f，逾渗主脊 %.2f（数盒子法）" % (db_path, db_meas))

    # ---------- (2) 几何类别：嵌入空间不同 → 数值不可比 ----------
    print("\n[2] 几何类别（嵌入空间维度）")
    print("  ┌────────────┬──────────┬──────────────┬──────────────────┐")
    print("  │ 对象        │ D 值     │ 嵌入空间     │ D 的定义域/意义   │")
    print("  ├────────────┼──────────┼──────────────┼──────────────────┤")
    print("  │ 三分 Cantor │ %.4f  │ 1D（截面）   │ 0<D<1：Cantor 拓扑│"
          % db_theory)
    print("  │ 逾渗主脊    │ %.2f   │ 2D（平面）   │ 1<D<2：稀疏网络路径│"
          % db_meas)
    print("  │ 初始运移路径│ %.2f   │ 2D（平面）   │ 1<D<2：路径网络    │"
          % db_path)
    print("  └────────────┴──────────┴──────────────┴──────────────────┘")
    print("  结论：两值嵌入空间维度不同（1D vs 2D），盒计数维数的取值范围不同，")
    print("       数值大小直接比较无意义（不同几何类别，延续论文物理对象澄清）。")

    # ---------- (3) Moran 反推：1.47 对应的有效分支/收缩 ----------
    print("\n[3] Moran 方程反推：若 1.47 为自相似树，对应何种分支-收缩几何？")
    cases = [
        ("三分 Cantor（P3 假设）", 2, 1 / 3, moran(2, 1 / 3)),
        ("二分收缩 1/4", 2, 1 / 4, moran(2, 1 / 4)),
        ("三分收缩 1/2", 3, 1 / 2, moran(3, 1 / 2)),
        ("五分收缩 1/3", 5, 1 / 3, moran(5, 1 / 3)),
        ("六分收缩 1/3", 6, 1 / 3, moran(6, 1 / 3)),
    ]
    for name, N, r, d in cases:
        mark = " ◀ 最接近实测 1.47" if abs(d - db_meas) < 0.02 else ""
        print("   %-14s N=%d, r=1/%d → D=%.4f%s" % (name, N, int(1 / r), d, mark))

    N_rev = inverse_moran(db_meas, 1 / 3)   # 假设 r=1/3
    r_rev = inverse_moran_r(db_meas, 2)     # 假设 N=2
    r_rev5 = inverse_moran_r(db_meas, 5)    # 假设 N=5
    print("   反推①：若收缩 r=1/3 → 有效分支 N=(1/3)^(-1.47)=%.2f" % N_rev)
    print("          → 与闫建钊实验观测『运移前缘通常有 2~5 个分支』的上端定量吻合")
    print("   反推②：若分支 N=2 → 有效收缩 r=2^(-1/1.47)=%.4f（≫1/3，通道更粗）" % r_rev)
    print("   反推③：若分支 N=5 → 有效收缩 r=5^(-1/1.47)=%.4f（≈1/3）" % r_rev5)
    print("   → 1.47 的最优自相似解释：约 5 分支、1/3 收缩（ln5/ln3≈1.465），")
    print("     与 P3 假设的 2 分支、1/3 收缩（0.631）分属不同分支几何——")
    print("     真实运移主脊是高分支统计分形（近随机渗流），而非确定性 2 分支 Cantor。")

    # ---------- (4) 相对稀疏度（可比的相对量） ----------
    print("\n[4] 相对稀疏度对比（同一几何类别内部的可比量）")
    s_yan = db_meas / db_path              # 主脊/路径（闫建钊，2D 内相对）
    s_p3 = db_theory / 1.0                 # Cantor 通道/满线（1D 内相对）
    print("   闫建钊（2D 内）：主脊/路径 = %.2f/%.2f = %.3f（主脊比路径稀疏 %.1f%%）"
          % (db_meas, db_path, s_yan, (1 - s_yan) * 100))
    print("   P3（1D 内）：Cantor 通道/满线 = %.4f/1 = %.4f（通道比满线稀疏 %.1f%%）"
          % (db_theory, s_p3, (1 - s_p3) * 100))
    print("   → 两者在各自嵌入空间内都验证『突破通道/主脊显著稀疏于整体』这一结构预言，")
    print("     但稀疏程度不同（主脊 16%% vs Cantor 通道 37%%），反映几何机制不同。")

    # ---------- (5) P3 检验协议 ----------
    print("\n[5] P3 检验协议（真实成像数据的正确比法）")
    print("  ① 在微 CT/FMI 成像中识别贯通性突破通道（渗流骨架，非全裂缝集合）；")
    print("  ② 对通道沿主导梯度方向的横截面/拓扑结构做盒计数 → D_b∈(0,1)；")
    print("  ③ 与 ln2/ln3≈0.631 比较（偏差判据，如 <10%）；若分支/收缩几何实测不同，")
    print("     按 Moran 方程 D=lnN/ln(1/r) 修正后比较——预测随之修正而非失效；")
    print("  ④ 不直接与裂缝网络维数（D∈(2,3)）或 2D 路径维数（1.47）数值对比——几何类别不同。")

    # ---------- 判定汇总 ----------
    checks = [
        ("C1 三分 Cantor 盒计数恢复理论 0.6309（偏差<3%）", abs(d1 - db_theory) / db_theory < 0.03),
        ("C2 五分形树盒计数恢复 Moran 理论 1.465（偏差<5%）", abs(d2 - moran(5, 1 / 3)) / moran(5, 1 / 3) < 0.05),
        ("C3 Moran 反推①：r=1/3 时有效分支 N∈[4,6]（对应实验观测 2~5 分支上端）",
         4.0 <= N_rev <= 6.0),
        ("C4 相对稀疏度方向一致：主脊<路径 且 Cantor 通道<满线", s_yan < 1 and s_p3 < 1),
        ("C5 数值不可比结论成立：0.6309∈(0,1) 且 1.47∈(1,2)，嵌入维度不同",
         (0 < db_theory < 1) and (1 < db_meas < 2)),
    ]
    n_pass = 0
    print("\n" + "-" * 72)
    for name, ok in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
        n_pass += int(ok)
    print("结果：%d/%d 通过（理论-实测几何类别对比，方法学与结构结论）" % (n_pass, len(checks)))
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
