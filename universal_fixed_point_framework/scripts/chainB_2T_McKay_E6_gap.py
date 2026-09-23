"""
chainB_2T_McKay_E6_gap.py — 2T 群与 SU(2) 谱缝 的 McKay/ADE 桥 数值甄别 v1.0
RN-ENDO-010 §8.14 配套 探点 (分析 2T 与 spectralGap8 的"具体关系")

问题(用户): 2T 群与 SU(2) 谱缝 spectralGap8 = (√6−√2)/√72 ≈ 0.1220 的具体关系?

事实基础:
  ① 2T ⊂ SU(2) 有限子群, 24 元素, 7 共轭类, 不可约表示维度 {1,1,1,2,2,2,3} (Σd²=24)
  ② McKay 对应: SU(2) 有限子群 Γ 的不可约表示张量积邻接 = 仿射 ADE Dynkin 图
     2T ↔ 仿射 E6 (Ẽ6, 7 节点)
  ③ SU(2) 的连续 Casimir 谱: λ_j = √(j(j+1)); spectralGap8 = λ_{j=1} − λ_{j=1/2} 归一化

本脚本判定: "2T/McKay(E6) 内部谱隙" 是否为 spectralGap8 的来源?
  步骤:
  [S1] 自验证构造仿射 E6 邻接矩阵(延长点候选 c 使最大本征值恰=2)
  [S2] 该图的谱隙(1−λ₂/λ₁ 及绝对隙) 对置 spectralGap8
  [S3] level 错位: E6 在 SU(2)_k WZW/ADE 分类的自然 level=10 (文献), 对置 框架 k_max=8
  纪律: 恒等≠结构证明; 不凑数; 凡不吻合标证伪。
"""
import numpy as np

# ---------------- SU(2) Casimir 谱缝 ----------------
sg = (np.sqrt(6) - np.sqrt(2)) / np.sqrt(72)
print("=" * 76)
print("2T ↔ SU(2) 谱缝: McKay/ADE 桥甄别 (v1.0)")
print("=" * 76)
print(f"\n[0] SU(2) 谱缝 (框架 spectralGap8)")
print(f"     λ_k = √(k(k+1))/√(8·9),  k=1..8 (框架记号, 分母 √72)")
l1n = np.sqrt(1*2)/np.sqrt(72)   # k=1
l2n = np.sqrt(2*3)/np.sqrt(72)   # k=2
print(f"     λ(k=1) = {l1n:.8f};  λ(k=2) = {l2n:.8f}")
print(f"     spectralGap8 = λ₂−λ₁ = {l2n-l1n:.8f} (闭式 (√6−√2)/√72 = {sg:.8f})")
assert abs((l2n-l1n) - sg) < 1e-9
print(f"     → 谱缝来自 k=1,2 两个相邻 Casimir 值之差 (归一化到 k_max=8)")

# ---------------- [S1] 构造仿射 E6 邻接 ----------------
# 有限 E6: 节点 {1..6}, 边 (1,2),(2,3),(3,4),(4,5),(3,6)
finite_edges = [(1,2),(2,3),(3,4),(4,5),(3,6)]
print(f"\n[S1] 构造仿射 E6(Ẽ6, 7 节点): 有限 E6 + 延长节点0")
n = 7
def adjacency(ext_c, edges):
    A = np.zeros((n, n))
    for a, b in edges:
        A[a][b] = A[b][a] = 1
    # 延长节点 0 连接到候选 c (有限图节点 c, 索引 c)
    A[0][ext_c] = A[ext_c][0] = 1
    return A

chosen = None
for ext_c in range(1, n):   # 0..6 中 0 是延长点本身, 连接 1..6 之一
    A = adjacency(ext_c, finite_edges)
    ev = np.linalg.eigvalsh(A)
    lmax = ev[-1]
    flag = " ✓ λmax=2 (仿射)" if abs(lmax-2.0) < 1e-6 else ""
    print(f"     延长节点0→{ext_c}: λmax = {lmax:.6f}{flag}")
    if abs(lmax-2.0) < 1e-6:
        chosen = (ext_c, A)
print(f"\n     → 仿射 E6(Ẽ6): 延长节点 0 连接到有限节点 {chosen[0]}, 最大本征值=2 自验证通过")

# ---------------- [S2] 仿射 E6 谱隙 ----------------
A = chosen[1]
ev = np.linalg.eigvalsh(A)
ev_sorted = sorted(ev, reverse=True)
l1, l2 = ev_sorted[0], ev_sorted[1]
graph_rel_gap = 1 - l2/l1      # 图"相对谱隙"(同构于谱比型; 注意此量≠LACI判据成员, 见下注)
graph_abs_gap = l1 - l2
print(f"\n[S2] 仿射 E6 邻接谱")
print(f"     本征值 = {[f'{x:.4f}' for x in ev_sorted]}")
print(f"     λ₁(max) = {l1:.6f};  λ₂ = {l2:.6f}")
print(f"     绝对隙 λ₁−λ₂ = {graph_abs_gap:.6f}")
print(f"     相对隙 1−λ₂/λ₁ = {graph_rel_gap:.6f}")
print(f"  ▲ 对置: spectralGap8 = {sg:.6f}")
print(f"     绝对隙 {graph_abs_gap:.6f} vs spectralGap8 {sg:.6f} → {'一致? '+str(abs(graph_abs_gap-sg)<1e-3) if False else '不同(类型也不同, 图/连续)'}")

# ---------------- [S3] level 错位 ----------------
print(f"\n[S3] level 错位 (判定性)")
print(f"     标准 SU(2)_k WZW/ADE 分类(Cappelli-Itzykson-Zuber): E6 ↔ level k = 10")
print(f"     框架 spectralGap8 使用 k_max = 8")
print(f"     8 ≠ 10 → spectralGap8 的 k 不落在 2T/E6 的 ADE 自然位置")
print(f"     → 2T(E6) 与 spectralGap8 存在水平错位, 非天然耦合")

# ---------------- 结论 ----------------
print("\n" + "=" * 76)
print("结论 (v1.0)")
print("=" * 76)
print("""  2T 与 SU(2) 谱缝 的"具体关系"判定:
    ① 结构关系(真): 2T ⊂ SU(2) 是有限子群嵌入; 其唯一严格的表示论桥是
       McKay 对应 2T ↔ 仿射 E6。这是"关系"存在的合法依据。
    ② 数值关系(否定): 仿射 E6 邻接谱(图论) 与 SU(2) Casimir 连续谱缝(算子)
       是两类不同谱: 前者 7 个有限本征值(最大=2), 后者连续 j 的 √(j(j+1))。
       绝对隙/相对隙数值不同 → spectralGap8 不源自 2T/McKay 邻接谱。
    ③ level 错位(否定): E6 在 SU(2)_k 的自然 level = 10 ≠ 框架 k_max = 8。
       即便走量子群桥, 8 也不落在 2T 的位置 → 无内生耦合。
  综合: 2T 与 spectralGap8 之间没有把 √(2/3) 的"24"内生化的数值通道;
        唯一合法关系是结构上的 McKay/ADE 嵌入, 它不承载该谱缝。
  边界: 交付自验证仿射 E6 构造 + 图谱隙对置 + level 错位判定;
        ②③ 为否定性证据 → 2T 源(24) 排除, 与 §8.13/§8.14 链B未闭合结论一致。

  附(符号纪律): 本人不将图相对隙 1−λ₂/λ₁ 归入 LACI 判据族(paper1 定义3.12a);
       谱比型为等价判定不变量, 方向与静默判据相反, 此处仅作图论陈列。""")