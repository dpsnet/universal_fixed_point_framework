# -*- coding: utf-8 -*-
"""
S429 过程-域二维网格：步进选择的生成链机制（2026-10-29）

S428 已闭合组件语义。组合级开放点 = 步进选择：
  Cs    (反冲) : 指数 19 = 16+3（全态+活跃）——活跃步
  a_e   (g-2)  : 指数 18 = 16+2（全态+幂基）——幂基步
  Rb    (干涉) : 指数 18 = 16+2 ——幂基步
  Q22   (合并) : σ^7 ——对合幂

本脚本把 步进选择 形式化为：过程类型（事件/分裂/冻结）
→ 机制代数（活跃 3 / 幂基 2 / 对合 7）的映射，并与
测量域（时空 d_H / 统计 e / 冻结 sigma）构成二维网格。

核心观察候选：
  [域 = 测量代数域]（S423/S425）：时空->d_H、统计->e、冻结->sigma
  [过程 = 机制代数]（本轮）：
    事件（单点散射/因果发生——Rec 侧）-> 活跃 3 -> 步进 +3
    分裂（二态/双路径/循环——Sp 侧）-> 幂基 2 -> 步进 +2
    冻结（加权合并/粗粒化——静默侧）-> 对合 7 -> σ 幂 7
  [σ 幂次谱 = 机制代数谱]：{3,5,7,8} = {活跃, 静默, 对合, k_max}
    ——幂次谱成员本身就是过程机制代数（观察级）

输出：
  1. 二维网格（域 x 过程）——4 通道填入 + 空位预言
  2. 分类验证（4 通道 = 域 x 过程 唯一格子）
  3. 空位预言：未来通道的构造形式（链/步进/符号确定，系数 c∈F）
"""
GRID = {}  # (域, 过程) -> (通道, 构造)

def fill(domain, process, channel, construction, note):
    key = (domain, process)
    assert key not in GRID, f"格子冲突 {key}"
    GRID[key] = (channel, construction, note)

# 4 通道填入
fill("时空 d_H", "事件", "Cs_2018", "-(5/2)*ln15*e^-19",
     "反冲=单点散射=活跃步; 系数 SU/P=静默/幂基; 符号 -")
fill("时空 d_H", "分裂", "a_e_2023", "+2*ln15*e^-18",
     "g-2=自旋二分/进动=幂基步; 系数 2=幂基; 符号 +")
fill("统计 e", "分裂", "Rb_2020", "+8*e^-18",
     "干涉=双路径/相位=幂基步; 系数 8=k_max; 符号 +")
fill("冻结 sigma", "冻结", "Q22_2022", "+16*sigma^7",
     "合并=加权平均=对合折叠; 系数 16=全态; 符号 +")

# 过程 -> 机制代数 -> 步进（σ 域幂次谱对应）
PROCESS_MECH = {
    "事件": (3, "活跃", "Rec 侧——因果发生/推进"),
    "分裂": (2, "幂基", "Sp 侧——二态叠加/翻倍"),
    "冻结": (7, "对合", "静默侧——自逆折叠/粗粒化"),
}

# σ 幂次谱 = 机制代数谱
SIGMA_POW_SPECTRUM = {3: "活跃", 5: "静默", 7: "对合", 8: "k_max"}

print("=" * 100)
print("S429 过程-域二维网格（域 x 过程 -> 偏移构造）")
print("=" * 100)
domains = ["时空 d_H", "统计 e", "冻结 sigma"]
processes = ["事件", "分裂", "冻结"]
header = "          | " + " | ".join(f"{p:^14s}" for p in processes)
print(header)
print("-" * len(header))
for d in domains:
    row = f"{d:^10s} | "
    for p in processes:
        if (d, p) in GRID:
            ch, cst, note = GRID[(d, p)]
            cell = f"{ch}:{cst}"
        else:
            cell = "——空位——"
        row += f"{cell:^14s} | "
    print(row)
print("-" * len(header))
print("\n[过程 -> 机制代数 -> 步进]")
for p, (m, name, side) in PROCESS_MECH.items():
    print(f"  {p:^4s} -> {name}({m})  {side}")
print("\n[σ 幂次谱 = 机制代数谱]  {3,5,7,8} = {活跃, 静默, 对合, k_max}")

print("\n[分类验证] 4 通道 = 域 x 过程 唯一格子（无冲突）：")
for key in sorted(GRID):
    ch, cst, note = GRID[key]
    print(f"  ({key[0]}, {key[1]}) -> {ch}: {cst}")
    print(f"     语义: {note}")

print("\n[空位预言（先验，可证伪）] 新通道偏移构造形式（系数 c∈F）：")
preds = [
    ("统计 e x 事件", "单次计数/事件型统计实验",
     "+c*e^-(16+3) = +c*e^-19", "e 链, 活跃步, 只+"),
    ("冻结 sigma x 事件", "冻结过程的事件型",
     "+c*sigma^3", "sigma 链, 幂 3=活跃"),
    ("冻结 sigma x 分裂", "冻结过程的分裂型",
     "+c*sigma^5", "sigma 链, 幂 5=静默"),
    ("冻结 sigma x k_max", "未知过程型",
     "+c*sigma^8", "sigma 链, 幂 8=k_max"),
    ("时空 d_H x 冻结", "时空域的冻结过程",
     "?（混合构造待数据）", "d_H 链, 冻结步——开放"),
]
for cell, phys, form, rule in preds:
    print(f"  {cell:^22s}: {phys}\n     构造形式 = {form}\n     规则 = {rule}")

print("\n[合并] 链=测量代数域（S423/S425）、步进=过程机制代数（本轮）")
print("  两独立维度张成偏移构造空间——构造 = 系数 x 特征量(域)^(-基) x 步进")
print("  证伪条件：FNAL muon g-2 偏移若用活跃步(e^-19 族)而非幂基步(e^-18 族)")
print("  ——过程-机制映射被证伪")
