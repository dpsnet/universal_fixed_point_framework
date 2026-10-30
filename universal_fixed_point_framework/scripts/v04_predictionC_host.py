# -*- coding: utf-8 -*-
"""104az-217：预言 C 宿主定位 —— 氢谱线频率比族穷举
预言 C：κΛ・Δλ₁₆ = 16（代数侧已闭合：92800/231 × 231/5800 = 16）。
Δλ₁₆ = (21/100)×(11/58)：21/100 = Hγ 相对频率（ν/R = 1/4−1/25，精确量子力学）；11/58 无谱线宿主。
宿主搜索空间 = 氢谱线频率比族 ν/R = 1/m²−1/n²（m<n）。
目标：11/58、231/5800、21/100 的精确/近似宿主；并扫框架量组合交叉（11/58 = (N_active+k_max)/58）。
"""
from fractions import Fraction

N_MAX = 100
targets = {
    "11/58": Fraction(11, 58),
    "231/5800": Fraction(231, 5800),
    "21/100": Fraction(21, 100),
}

lines = []
for m in range(1, N_MAX):
    for n in range(m + 1, N_MAX + 1):
        v = Fraction(1, m * m) - Fraction(1, n * n)
        lines.append((m, n, v))

print("氢谱线频率比族：m<n≤%d，共 %d 条" % (N_MAX, len(lines)), flush=True)

for name, tv in targets.items():
    exact = [(m, n) for m, n, v in lines if v == tv]
    print("\n===== 目标 %s = %s =====" % (name, tv), flush=True)
    if exact:
        for m, n in exact:
            print("  精确命中：1/%d²−1/%d² = %s（谱线：n=%d→m=%d 跃迁）" % (m, n, tv, n, m), flush=True)
    else:
        # 最近邻（相对 dev）
        tf = float(tv)
        best = sorted(lines, key=lambda t: abs(float(t[2]) / tf - 1.0))[:8]
        print("  无精确命中；最近邻（相对 dev）：", flush=True)
        for m, n, v in best:
            dev = abs(float(v) / tf - 1.0)
            print("    1/%d²−1/%d² = %s（dev %+.2e）" % (m, n, v, dev), flush=True)

# 交叉：11/58 的框架量组合（11 = N_active+k_max = 3+8；58 素因子 2·29）
print("\n===== 交叉检查：11/58 因子结构 =====", flush=True)
print("11 = N_active + k_max = 3 + 8（塔第三项）；58 = 2×29（29 = 闭包家族，104az-259）", flush=True)
print("5800 = 静默²×232 = 25×(k_max×(2²·7+1)) = 25×8×29；Δλ₁₆ = (Hγ ν/R)×(11/58)", flush=True)

# 相邻谱线比（氢线频率比的比 = 谱线族内部结构）：ν(Hβ)/ν(Hγ) 等
hbeta = Fraction(1, 4) - Fraction(1, 9)   # 1/4−1/9 = 5/36（Hβ）
hgamma = Fraction(1, 4) - Fraction(1, 25)  # 21/100（Hγ）
hdelta = Fraction(1, 4) - Fraction(1, 36)  # 2/9（Hδ）
print("\n===== 巴耳末系相对频率（ν/R）=====", flush=True)
print("Hβ = %s（%.6f）" % (hbeta, float(hbeta)), flush=True)
print("Hγ = %s（%.6f）" % (hgamma, float(hgamma)), flush=True)
print("Hδ = %s（%.6f）" % (hdelta, float(hdelta)), flush=True)
print("Hγ/Hβ = %s（%.6f）" % (hgamma / hbeta, float(hgamma / hbeta)), flush=True)
print("Hβ/Hγ = %s（%.6f）" % (hbeta / hgamma, float(hbeta / hgamma)), flush=True)
print("对照 11/58 = %.6f；Hβ/Hγ = %.6f（dev %.2e）" % (
    float(Fraction(11, 58)), float(hbeta / hgamma), abs(float(hbeta / hgamma) / float(Fraction(11, 58)) - 1.0)), flush=True)
