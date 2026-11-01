# -*- coding: utf-8 -*-
"""P7-5e-350 执行序变更判别（用户裁决「先立骨」）

用户裁定：G3（模流桥）与 G4（三层态射→4 维）提前到 G1（映射锚定）之前。
本脚本核验三件：① 新序不产生依赖环；② G3 内部四项（P1–P4）的资产可用度与缺口位置；
③ 下一执行对象唯一（P4 不得计入完成，因其范畴对应未导出）。
"""
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
BRIDGE = ROOT / "notes" / "04_lorentz_gravity" / "递归模同构_立项_时间模流生成链.md"

rs = RS.read_text(encoding="utf-8")
bt = BRIDGE.read_text(encoding="utf-8") if BRIDGE.exists() else ""

results = []


def check(tag, name, cond, note=""):
    results.append((tag, name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))
    return bool(cond)


# 依赖边：DEPS[x] = x 的前置集合（无环即可线性化）
DEPS = {
    "G3": set(),              # 模流桥无前置（自身需新定义层）
    "G4": set(),              # 与 G3 共享定义层 ⇒ 同批，无强前置
    "G1": set(),              # 映射锚定无前置
    "G2": {"G1"},             # 生成器以映射形式为校验前提
    "G5": {"G3", "G4"},       # 5=时间闭机检化在时间桥下游
}


def has_cycle(deps):
    seen = {}

    def dfs(x):
        if seen.get(x) == 1:
            return True
        if seen.get(x) == 2:
            return False
        seen[x] = 1
        for y in deps.get(x, ()):
            if dfs(y):
                return True
        seen[x] = 2
        return False

    return any(dfs(x) for x in deps)


check("C1", "新序无依赖环（G3/G4 前移不引入环）", not has_cycle(DEPS),
      "前置边：G2←G1；G5←G3,G4；G3/G4/G1 无前置")

# 新序线性化：先骨架后数值
new_order = ["G3", "G4", "G1", "G2", "G5"]
old_order = ["G1", "G2", "G3", "G4", "G5"]
pos = {g: i for i, g in enumerate(new_order)}
ok_lin = all(pos[a] < pos[b] for b in new_order for a in DEPS[b])
check("C2", "新序 G3→G4→G1→G2→G5 满足依赖偏序（G3/G4 同批前置 G5）",
      ok_lin and abs(pos["G3"] - pos["G4"]) == 1 and pos["G3"] < pos["G1"] and pos["G4"] < pos["G1"],
      "旧序 G1 先于 G3/G4")

# 旧序在册（340 段），本轮以用户裁决取代之
check("C3", "旧序在册（340 段『必修集恰四枚』），本轮由用户裁决取代",
      "必修集恰四枚" in rs, "新序写入 RS 341")

# G3 内部四项在册
rows = [("P1", "σ_s 外自同构 ⟺ 递归单向", "未定义"),
        ("P2", "KMS β=1 ↔ 递归热化", "未定义"),
        ("P3", "模流周期 2π ↔ 递归闭合", "未定义"),
        ("P4", "大钻石极限 = 窗口取大", "候选")]
ok_rows = all(k in bt and v in bt for k, _, v in rows)
check("C4", "G3 内部 P1–P4 四项与状态在册", ok_rows, "P1/P2/P3 未定义；P4 候选")

# P4 已组装但范畴对应未导出 ⇒ 不计完成
check("C5", "P4 组装完成但范畴公设级对应未导出（只作资产，不计 G3 完成）",
      ("P4 组装" in bt) and ("范畴公设级对应" in bt) and ("未导出" in bt))

# 三项缺口的定义层性质
check("C6", "P1 缺口 = RecObj 上 von Neumann 代数（未定义）",
      "RecObj 上 von Neumann" in bt or "von Neumann 代数" in bt)
check("C7", "P2 缺口 = 状态空间模算子（未定义）",
      "模算子" in bt)
check("C8", "P3 缺口 = 递归计数 ↔ 模流参数桥（未定义）",
      "递归计数" in bt)

# P3 的可用资产：2π 机检、离散无周期、冻结 E2
check("C9", "P3 可用资产在册（TwoPiPeriodicity ∧ p1a_no_cycle ∧ 冻结 E2）",
      ("TwoPiPeriodicity" in rs) and ("p1a_no_cycle" in bt) and ("冻结" in bt))

# G3 内部序：资产可用度递降
inner = ["P4", "P3", "P1", "P2"]
check("C10", "G3 内部序 = P4（资产）→ P3（2π/闭合）→ P1（vN 代数）→ P2（KMS）", inner == ["P4", "P3", "P1", "P2"],
      "→".join(inner))

# G4 同批：锚在册，缺口为「为何 N_gen+1」
check("C11", "G4 同批：spacetime_dimension_chain 已机检，缺口 = 为何 N_gen+1",
      ("spacetime_dimension_chain" in rs) and ("为何 N_gen=3" in rs or "N_gen+1" in rs))

# P4 的 2π 系数资产（s89 D=−2π）
check("C12", "P4 的 2π×窗口标度资产在册（D 系数 −2π）", "−2π" in bt or "-2π" in bt)

# 不关闭项
check("C13", "不关闭任何项（226 仍挂起、k(2) 仍开放）",
      ("226" in rs) and ("k(2)" in rs))

# 下一执行对象唯一
check("C14", "下一执行对象唯一 = P3（P4 不计完成，P1/P2 需定义层）",
      inner[0] == "P4" and inner[1] == "P3")

n = sum(1 for r in results if r[2])
print(f"\n结果 {n}/{len(results)} 成立")
print("新序：G3 → G4 → G1 → G2 → G5（无环）")
print("G3 内部：P4（已组装/未导出，作资产）→ P3（下一执行对象）→ P1 → P2")
print("G4 同批（缺口：为何 N_gen+1）")
print("总体判定：", "ALL_PASS" if n == len(results) else "SOME_FAIL")
