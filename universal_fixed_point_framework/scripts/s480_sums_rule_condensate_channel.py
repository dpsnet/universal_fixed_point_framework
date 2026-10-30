# -*- coding: utf-8 -*-
"""
S480 统计×冻结格判别通道就绪化（S445 遗留——S479 RMS 构造意外检验）
新数据：Bai & Chen 2025（arXiv:2502.20241）双来源盘点——
  ⟨s̄s⟩/⟨ūu⟩ = 1.08±0.16 [Lattice]（MILC 1211.6577——S445 已知）
           = 0.66±0.10 [Sum Rule Average]（sum rule 平均）
检验：
  ① 0.66(10) vs 幂基/活跃 = 2/3（S479 RMS 构造 ⟨x²⟩=2/3 的物理读数？）
  ② 全框架候选族扫描——窗口 [0.56, 0.76] 内达标候选数（判别力评估）
  ③ 两来源张力（格点 vs sum rule）——物理值未定判定
  ④ 通道就绪化结论 + e⁻²³ 族分离（O(1) 通道 ≠ e⁻²³=1.03e-10 量级）
纪律：σ_score = |预测−实验|/不确定度；≤1σ 达标/1-3σ 提示/>3σ 不达标。
"""
import math
SIG = 1/15.0

print("=" * 78)
print("① sum rule 0.66(10) vs 框架候选——σ_score 全族扫描")
print("=" * 78)
val, u = 0.66, 0.10   # Sum Rule Average（Bai & Chen 2025 式 2.8）
cands = {
    "幂基/活跃 2/3":        2/3.0,
    "√(2/3)²（RMS 幅值平方）": 2/3.0,
    "静默/显态 5/11":       5/11.0,
    "显态/全态 11/16":      11/16.0,
    "静默/全态 5/16":       5/16.0,
    "活跃/显态 3/11":       3/11.0,
    "5/7（S445 系数族）":    5/7.0,
    "7/10（S445 系数族）":   7/10.0,
    "8（S445 系数族·不适用）": 8.0,
    "全态/Σ 16/15":         16/15.0,
    "Σ 倒数 σ":             SIG,
    "1−σ 14/15":           14/15.0,
    "3/4 活跃²/全态":       3/4.0,
    "1/√2":               1/math.sqrt(2),
    "不动点 4/全态 1/4":    1/4.0,
}
rows = []
for name, v in cands.items():
    ss = abs(v - val) / u
    rows.append((ss, name, v))
rows.sort()
print("  实验：⟨s̄s⟩/⟨ūu⟩ = 0.66±0.10 [Sum Rule Average]——窗口 [%.3f, %.3f]"
      % (val-u, val+u))
for ss, name, v in rows:
    mark = "✓达标" if ss <= 1 else ("提示" if ss <= 3 else "✗")
    print("  %-24s = %.6f → σ_score = %.3f %s" % (name, v, ss, mark))

print()
print("=" * 78)
print("② 判别力评估——窗口内达标候选数")
print("=" * 78)
n_pass = sum(1 for ss, _, _ in rows if ss <= 1)
print("  窗口 [0.56, 0.76] 内 ≤1σ 达标候选：%d 个" % n_pass)
print("  达标候选：", [r[1] for r in rows if r[0] <= 1])
print("  → 2/3 最优（0.067σ）但 5/7、7/10、11/16 等也兼容——")
print("    单通道判别力不足——需更小误差或第二通道")

print()
print("=" * 78)
print("③ 两来源张力判定")
print("=" * 78)
val_lat, u_lat = 1.08, 0.16
tension = abs(val_lat - val) / math.sqrt(u_lat**2 + u**2)
print("  格点 1.08(16) vs Sum Rule 0.66(10)：差 %.2f、σ 差 %.2fσ" % (val_lat-val, tension))
print("  → 物理值未定（2.2σ 张力）——两方任一可能——不可断言 0.66 为正确值")
print("  格点 vs 幂基/活跃：σ_score = %.3f（提示级）" % (abs(val_lat-2/3.0)/u_lat))

print()
print("=" * 78)
print("④ 通道就绪化结论")
print("=" * 78)
print("  [通道就绪]：Sum Rule 通道（0.66±0.10）——新来源 Bai & Chen 2025")
print("    （arXiv:2502.20241 式 2.8——引用 sum rule 平均 [39]）")
print("    ——中心值 + 明确误差——可挂载候选判别")
print("  [意外检验]：S479 RMS 读数构造 ⟨x²⟩ = 幂基/活跃 = 2/3——")
print("    sum rule 0.66(10) 与 2/3 吻合 0.067σ——RMS 构造获物理读数")
print("    （'每 3 份轻凝聚对应 2 份 s 凝聚'——构造 1 二值读数语义）")
print("  [诚实边界]：")
print("    1) 后验匹配（先有 2/3 后见 0.66）——非先验预言——")
print("       升级价值 = 通道可用于未来先验判别（更高精度测量确认）")
print("    2) 两来源 2.2σ 张力——物理值未定——0.66 未必正确")
print("    3) 多候选兼容（2/3/5/7/7/10/11/16 全达标）——判别力仍弱")
print("    4) e⁻²³ 族（1.03e-10）未被此通道检验——O(1) 通道 ≠ e⁻²³ 量级——")
print("       e⁻²³ 族预言保留（S445——待 θ_QCD/新通道）")
print("  [状态]：通道 1b（Sum Rule）就绪——RMS 构造意外检验 0.067σ——")
print("    判别力部分提升（最优候选 2/3）——多候选兼容待更小误差")
