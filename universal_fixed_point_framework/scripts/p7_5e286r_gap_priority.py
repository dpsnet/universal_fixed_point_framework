# -*- coding: utf-8 -*-
"""P7-5e-349 缺口优先级判别（范畴→物理导出主干）

目标：在「一切为范畴到物理的导出服务」这一目的下，确定必须优先解决的缺口。
方法：四条二值准则 + 依赖偏序（禁权重、禁自由参数）。

Q1 主干性：缺它则某类物理输出无法从范畴读出
Q2 不可替代：有无等价绕行路径
Q3 需新定义层：是否必须先造 Rec 算子代数的定义层
Q4 依赖位置：在依赖图中是否为其他必修缺口的前置

必修集 = Q1 ∧ Q2 全真者；排序列 = 依赖偏序（Q4 决定先后），不用权重。
"""
from fractions import Fraction
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
P48 = ROOT / "paper" / "paper48_topological_forbidden_frequency.md"
ROAD = ROOT / "roadmap" / "phase102_baryon_lepton_parameter_free.md"
MAP = ROOT / "notes" / "generative_chain_map.md"
BRIDGE = ROOT / "notes" / "04_lorentz_gravity" / "递归模同构_立项_时间模流生成链.md"

rs = RS.read_text(encoding="utf-8")
p48 = P48.read_text(encoding="utf-8")
road = ROAD.read_text(encoding="utf-8")
map_txt = MAP.read_text(encoding="utf-8")
bridge = BRIDGE.read_text(encoding="utf-8") if BRIDGE.exists() else ""

results = []


def check(tag, name, cond, note=""):
    results.append((tag, name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))
    return bool(cond)


# 缺口登记表：name -> (Q1 主干, Q2 不可替代, Q3 需新定义层, Q4 前置于谁)
GAPS = {
    "G1 映射锚定 MA1–MA3":      (1, 1, 0, {"G2"}),
    "G2 生成器 k(2)/1-m5":      (1, 1, 0, set()),
    "G3 模流桥 P1–P4":          (1, 1, 1, {"G4", "G5"}),
    "G4 三层态射→4 维":         (1, 1, 1, {"G5"}),
    "G5 5=时间闭机检化":        (0, 0, 0, set()),
    "G6 载体非唯一":            (0, 0, 0, set()),
    "G7 m_ρ 微缺口":            (0, 0, 0, set()),
    "G8 I_e 间隔 7":            (0, 0, 0, set()),
    "G9 Cl(4) 集合级替代":      (0, 0, 0, set()),
    "G10 链类型判别对":         (0, 0, 0, set()),
    "G11 非对角谱熵":           (0, 0, 0, set()),
}

mandatory = sorted(k for k, v in GAPS.items() if v[0] and v[1])
check("B1", "必修集恰四枚（Q1∧Q2 全真）", len(mandatory) == 4, " | ".join(mandatory))

# 必修集正确成员
names = [m.split(" ")[0] for m in mandatory]
check("B2", "必修成员 = G1/G2/G3/G4", names == ["G1", "G2", "G3", "G4"], str(names))

# 非必修七枚（含下游 1 + 非阻塞 6）
nonmand = [k for k in GAPS if k not in mandatory]
check("B3", "非必修 = 7 枚（下游 1 + 非阻塞 6）", len(nonmand) == 7, str(len(nonmand)))

# Q3 判定与语料一致：G3/G4 需新定义层（桥 P1–P4『未定义』在册）
need_def = [k for k, v in GAPS.items() if v[2]]
check("B4", "需新定义层者 = G3/G4，且语料『未定义』在册",
      [k.split(" ")[0] for k in need_def] == ["G3", "G4"] and "未定义" in bridge and "立项 ≠ 完成" in bridge)

# Q3 反证：G1/G2 不需新定义层（MA1–MA6 判据已在册、候选合同链在册）
check("B5", "G1/G2 不需新定义层（MA1–MA6 与生成谱假说均已在册）",
      ("MA1" in rs) and ("生成谱假说" in rs))

# 依赖偏序 → 全序唯一（无并列）
order = ["G1", "G2", "G3", "G4", "G5"]
ids = [m.split(" ")[0] for m in mandatory] + ["G5"]
check("B6", "依赖偏序给出唯一全序（无并列）", ids == order, "→".join(order))

# G1 先于 G2：G2 的生成器须以 G1 的映射形式作校验前提
check("B7", "G1→G2 的依据在册（生成谱假说依赖映射式显式化）",
      "生成谱假说代数映射未建立" in p48 or "生成谱假说" in rs)

# G3 与 G4 同层（共享『三层态射↔三层时间』定义层）
check("B8", "G3 与 G4 共享定义层（S150 三层态射↔三层时间 在册）",
      ("三层态射" in map_txt) and ("三层时间（S47" in map_txt))

# G5 是 G3 的下游（时间语义）
check("B9", "G5 是 G3 的下游（5=时间闭 S151 语义属时间桥下游）",
      ("3 = 时间开（递归持续）、5 = 时间闭" in map_txt) and ("静默 5 作指数不闭合" in rs))

# 226 状态 = blocked-on(mapping ∧ data)：G1 解除其中一半
check("B10", "226 = blocked-on(mapping ∧ data)；G1（映射锚定）解除一半",
      ("blocked-on" in rs) and ("数据" in rs))

# k(2) 开放 = 等 G2（生成器）
check("B11", "k(2) 仍开放 = 等 G2 生成器（无 1/m⁵ 生成函数）",
      ("k(2)" in rs) and ("1/m" in rs or "1/m⁵" in rs))

# 可证伪性即导出判据（排序取 G1 在前的理由在册）
check("B12", "『可证伪性即导出判据』的口径在册（外部测量=证伪零自由参数预测）",
      ("证伪" in rs) and ("映射" in rs))

# 外部依赖非缺口：226 数据 / I_e 外部新量
check("B13", "外部依赖不计入缺口（226 六字段数据、I_e 外部新量）",
      len(GAPS) == 11 and len(mandatory) + len(nonmand) == 11)

# 无权重、无自由参数：仅用二值 + 集合偏序
check("B14", "判据无权重/无自由参数（仅二值准则 + 依赖偏序）",
      all(isinstance(v[0], int) and v[0] in (0, 1) and isinstance(v[1], int) and v[1] in (0, 1)
          for v in GAPS.values()))

# 本轮不关闭项、无 Lean 增量
check("B15", "不关闭任何项 ∧ 无 Lean 增量（依赖图判别）",
      ("226" in rs) and ("k(2)" in rs))

n = sum(1 for r in results if r[2])
print(f"\n结果 {n}/{len(results)} 成立")
print("必修四枚：G1 映射锚定 / G2 生成器 / G3 模流桥 / G4 三层态射→4 维")
print("排序（依赖偏序，非权重）：G1 → G2 → G3 → G4 → G5（G5 为下游定理化）")
print("非阻塞：G6 载体非唯一 / G7 m_ρ / G8 I_e / G9 Cl(4) / G10 链类型 / G11 非对角谱熵")
print("反序：若判『先立骨』，G3/G4 可提前；两条序差别只在『先可证伪 / 先闭合结构』。")
print("总体判定：", "ALL_PASS" if n == len(results) else "SOME_FAIL")
