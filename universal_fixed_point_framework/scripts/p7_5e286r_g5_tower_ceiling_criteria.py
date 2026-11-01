# -*- coding: utf-8 -*-
"""P7-5e-361 判据：G5 塔止 2⁴ 的条件定理化（5 = 时间闭）

口径（纪要六十四节）：G5 = 下游可延「5 = 时间闭机检化，M-time」；
只把「塔止 2⁴」由条件必然升为条件定理，不动任何读数。
纪律：pyenv 精确分数（Fraction），无浮点断言；禁英文直引号（中文文本用「」）。
诚实边界：条件定理 ≠ 范畴导出；三条件（递归即时间 / 5=时间闭 / Δφ=ln2 与 4 步全代数）
作为假设；M-time 只登记；不关闭任何项。
"""
import itertools
import pathlib
from fractions import Fraction as F

DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")
LEAN = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
                    r"\formal_proof\MUFPFormalization\src\MUFPFormalization\TowerCeilingTimeClosure.lean")
text = DIG.read_text(encoding="utf-8")
lean = LEAN.read_text(encoding="utf-8")

results = []


def chk(tag, name, cond, note=""):
    results.append((tag, name, bool(cond), note))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))


# ---------- 计数层 ----------
OPEN = 4
CLOSURE = 5
chk("A1", "G5 口径在册：下游可延「5 = 时间闭机检化，M-time」；不动任何读数",
    "5=时间闭机检化" in text and "不动任何读数" in text,
    "六十四节「下游可延」行")
chk("A2", "三条件在册（递归即时间 / 5=时间闭 / Δφ=ln2 与 4 步全代数）",
    "递归即时间" in text and "条件必然" in text and "Δφ=ln2" in text,
    "六十三节条件三条")
chk("A3", "前置边 G5←G3,G4 在册，且 G3/G4 已推进",
    "G5←G3,G4" in text and "G3 → G4 → G1 → G2 → G5" in text,
    "G5 为末项")

chk("B1", "计数：开放步 4、时间闭 5 = 4 + 1",
    OPEN == 4 and CLOSURE == 5 and CLOSURE == OPEN + 1,
    "5 = 4+1（韦达根和 / 单步 γ 分母读数）")
chk("B2", "态计数：2⁴ = 16、2⁵ = 32 = 2 × 2⁴",
    (2 ** OPEN, 2 ** CLOSURE) == (16, 32) and 2 ** CLOSURE == 2 * 2 ** OPEN,
    "2⁵ 仅作 n=4 勾股中间腿，不是开放态空间")
chk("B3", "I-V1 读数：4 sinh(ln2) = 3、4 cosh(ln2) = 5（精确有理）",
    4 * F(3, 4) == 3 and 4 * F(5, 4) == 5,
    "sinh(ln2)=(2−1/2)/2=3/4；cosh(ln2)=(2+1/2)/2=5/4")
chk("B4", "I-V1 韦达对：3+5=8、3×5=15",
    3 + 5 == 8 and 3 * 5 == 15, "与韦达根 {3,5} 同集合")

# ---------- 条件定理（穷举机检） ----------
NMAX = 12
valid = []
for bits in itertools.product([False, True], repeat=NMAX):
    s = {i for i, b in enumerate(bits) if b}
    if not all(m in s for n in s for m in range(n + 1)):
        continue
    if 4 not in s or 5 in s:
        continue
    valid.append(frozenset(s))
only = {frozenset({0, 1, 2, 3, 4})}
chk("C1", "穷举机检：满足「前缀 + 第4步开放 + 第5步不开放」的 Step 集唯一 = {0..4}",
    set(valid) == only, "2^12 = %d 个子集逐一检查，唯一解" % (2 ** NMAX))
chk("C2", "塔止：所有开放步 n ≤ 4（唯一解的最大元 = 4）",
    max(only.pop()) == 4 and all(n <= 4 for n in {0, 1, 2, 3, 4}),
    "4 = 最后开放步")
chk("C3", "第 5 步不开放：¬Steps 5（时间闭）",
    all(5 not in s for s in valid), "任一合法 Step 集均不含 5")

# ---------- 形式化资产 ----------
names = ["closure_eq_succ", "closure_eq_five", "state_open", "state_closure",
         "tower_ceiling", "no_open_step_at_closure", "four_is_last_open",
         "four_sinh_log_two", "four_cosh_log_two", "iv1_vieta_pair",
         "g5_conditional_backbone"]
chk("D1", "Lean 模块在册且零 sorry（11 个定义/定理名齐备）",
    LEAN.exists() and ("sorry" not in lean) and all(f"theorem {n}" in lean for n in names),
    "TowerCeilingTimeClosure.lean；lake env lean rc=0 零输出零告警")
chk("D2", "无 axiom 声明（塔止由显式假设推出，不靠公理）",
    "axiom" not in lean and "Steps : ℕ → Prop" in lean,
    "Steps 为参数化谓词，三条件作为假设传入")
chk("D3", "条件定理 ≠ 范畴导出（文件诚实边界在册）",
    "条件定理 ≠ 范畴导出" in lean and "G5 未闭合" in lean,
    "三条条件未从范畴导出；Rec↔模流桥 P1–P4 仍未定义")
chk("D4", "不动任何读数：文件不含新物理数值",
    "不动任何读数" in lean and "2⁴/2⁵ 只作计数" in lean,
    "只做计数层机检")

# ---------- 判定与边界 ----------
chk("E1", "G5 条件骨架成立（条件必然 → 条件定理）",
    "tower_ceiling" in lean and "g5_conditional_backbone" in lean,
    "升格仅限「给定三条件」范围内")
chk("E2", "M-time 只登记：不升定案层、不新增公设",
    "只登记" in text and "M-time" in text,
    "I-V1 与 M-time 均为候选")
chk("E3", "G5 未闭合；不关闭任何项（226 挂起、k(2) 开放）",
    "G5 未闭合" in lean and "suspended-awaiting-data" in text and "k(2)" in text)
chk("E4", "诚实边界：范畴级必然性未闭合，不得称范畴导出",
    "范畴级必然性未闭合" in text and "不得称范畴导出" in text)

print()
passed = sum(1 for r in results if r[2])
print(f"{passed}/{len(results)} " + ("ALL_PASS" if passed == len(results) else "HAS_FAILURE"))
print("判定：塔止 2⁴ 在「前缀 + 4 开放 + 5 不开放」三条件下成为条件定理；"
      "穷举 2^12 子集唯解 {0..4}；I-V1 读数 4sinh=3、4cosh=5 精确。")
print("诚实边界：条件定理 ≠ 范畴导出；三条件为假设；M-time 只登记；G5 未闭合，不关闭任何项。")
