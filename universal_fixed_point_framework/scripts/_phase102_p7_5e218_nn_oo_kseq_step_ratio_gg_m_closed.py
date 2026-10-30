# -*- coding: utf-8 -*-
"""
P7-5e-218 NN: two k-sequences step ratios (index/exponent coefficient 2 shared)
        OO: GG-family m closed form m_k = (2^{3k+1}+21k-2)/7
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e218_nn_oo_kseq_step_ratio_gg_m_closed.json"

def k_j(j):
    return 2 ** (j - 2) * 3

def k_win(j):
    return 6 * 4 ** j

def k_n(n):
    return 2 ** (n - 4) * (7 * n + 2)

def m_k(k):
    n = (2 ** (3 * k + 1) - 2) // 7
    return n + 3 * k

# ---------- NN: step ratios ----------
NN1 = {"check": "★ NN1: 两 k 序列的 2 进步进——k_j 每步 ×2（指数系数 1：指数=j−2）、k_{2j+3} 每步 ×4（指数系数 2：指数=2j+1）、k_n 每步 ×2（指数系数 1：指数=n−4）；DD2 子列 n 步进 3 时 k_n 的 2 进部分 ×2^3=8",
       "k_j_ratio": k_j(5) / k_j(4), "k_win_ratio": k_win(5) / k_win(4),
       "k_n_ratio_base": 2,
       "ok": k_j(5) / k_j(4) == 2 and k_win(5) / k_win(4) == 4}

NN2 = {"check": "★ NN2: DD2 族与窗口对合族共享指数/下标系数 2（指数步进 = 2×下标步进：DD2 3→6、Bott 8→16）；k_j/k_n 基础族系数 1",
       "dd2": "下标步进 3 → 指数步进 6（2×3）",
       "bott": "下标步进 8 → 指数步进 16（2×8）",
       "k_j": "下标步进 1 → 指数步进 1（系数 1）",
       "k_n": "下标步进 1 → 指数步进 1（系数 1）"}

NN3 = {"check": "★ NN3: Bott 周期 8 在窗口对合族中 ↔ 指数步进 16（×2^16=65536）——系数 2 使周期翻倍",
       "ok": 4 ** 8 == 2 ** 16 == 65536}

# ---------- OO: m closed form ----------
OO_rows = []
for k in range(1, 8):
    m = m_k(k)
    closed = (2 ** (3 * k + 1) + 21 * k - 2) // 7
    OO_rows.append({"k": k, "m": m, "closed": closed, "ok": m == closed,
                    "ratio_prev": None if k == 1 else m / m_k(k - 1)})

OO1 = {"check": "★ OO1: GG 族 m 闭式 m_k = (2^{3k+1}+21k−2)/7——k=1..7 全 True",
       "all_ok": all(r["ok"] for r in OO_rows), "rows": OO_rows}
OO2 = {"check": "OO2: 渐近 m_k ≈ (2/7)·8^k（主导项 2^{3k+1}/7 = 2·8^k/7），余项 (21k−2)/7 = 3k − 2/7",
       "leading": "2·8^k/7", "remainder": "(21k−2)/7 = 3k − 2/7"}
OO3 = {"check": "OO3: m_{k+1}/m_k → 8（渐近）——GG 族 m 增长因子趋向 8 = 2^3（每 k 乘 8）",
       "ratios": [round(r["ratio_prev"], 4) for r in OO_rows if r["ratio_prev"]]}

conclusion = {
    "verdict": "NN（步进比）：★ k_j 每步 ×2（系数 1）、k_{2j+3} 每步 ×4（系数 2）、k_n 每步 ×2（系数 1）；★ DD2 族与窗口对合族共享指数/下标系数 2（指数步进=2×下标步进：3→6、8→16），k_j/k_n 基础族系数 1；★ Bott 周期 8 ↔ 指数步进 16（4^8=2^16=65536）——系数 2 使周期翻倍。OO（GG m 闭式）：★ m_k=(2^{3k+1}+21k−2)/7 精确闭式（k=1..7 全 True：5,24,155,1182,9377,74916,599207）；渐近 (2/7)·8^k（余项 3k−2/7）；m_{k+1}/m_k → 8 增长因子（4.8,6.46,7.63,7.93→8）。",
    "NN": {"NN1": NN1, "NN2": NN2, "NN3": NN3},
    "OO": {"OO1": OO1, "OO2": OO2, "OO3": OO3},
    "honest_limits": [
        "NN1 是指数系数核对（序列定义）",
        "NN2 是系数观察（2 vs 1）——'共享系数 2'为形式观察",
        "NN3 是恒等核对（4^8=2^16）",
        "OO1 是代数化简（闭式恒等）",
        "OO2/OO3 是渐近分析（主导项/比值）",
        "继承 187-217 候选层",
    ],
    "next_candidates": [
        "检验 PP：系数 2 族（DD2/窗口对合）与系数 1 族（k_j/k_n）在 D(n)=8k_n+1 中的汇合点（两族是否在某 n 重合）",
        "检验 QQ：m_k 闭式的 3k 余项与框架量（3=种子、7=主模数）的连接",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-219",
    ],
}

result = {
    "title": "P7-5e-218 NN: k-seq step ratios; OO: GG m closed form",
    "date": "2026-10-16",
    "NN": {"NN1": NN1, "NN2": NN2, "NN3": NN3},
    "OO": {"rows": OO_rows, "OO1": OO1, "OO2": OO2, "OO3": OO3},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-218 NN/OO: k-seq step ratios & GG m closed form")
print("=" * 76)
print("[NN1]", NN1["check"], "-> ok=%s" % NN1["ok"])
print("[NN2]", NN2["check"])
print("  %s | %s | %s | %s" % (NN2["dd2"], NN2["bott"], NN2["k_j"], NN2["k_n"]))
print("[NN3]", NN3["check"], "-> ok=%s" % NN3["ok"])
print("[OO m closed form]")
for r in OO_rows:
    print("  k=%d m=%7d closed=%7d ok=%s ratio=%s" % (r["k"], r["m"], r["closed"], r["ok"], r["ratio_prev"]))
print("[OO1]", OO1["check"], "-> all_ok=%s" % OO1["all_ok"])
print("[OO2]", OO2["check"])
print("[OO3]", OO3["check"], "-> ratios=%s" % OO3["ratios"])
print("[Conclusion]", conclusion["verdict"])
