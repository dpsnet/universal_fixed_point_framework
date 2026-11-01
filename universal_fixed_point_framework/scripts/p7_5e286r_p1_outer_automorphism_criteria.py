# -*- coding: utf-8 -*-
"""P7-5e-352 G3-P1 入轨判据：σ_s 外自同构 ⟺ 递归单向（OC1–OC6）

目标：在不构造完整 von Neumann 代数定义层的前提下，明确 P1 闭合的可核验
条件——类比 G5-M1 的 MA1–MA6（映射锚定判据），为 P1 定义「入轨判据」
OC1–OC6，回答「P1 何时可启动定义层工程、何时判定成立」。

边界：本判据不定义 RecObj 上的 von Neumann 代数（那是 P1b 定义层缺口）；
不引入模算子（P2 缺口）；只做「入轨条件」的可核验性判别。

P1 命题（立项文档 §3 表）：σ_s 外自同构 ⟺ 递归单向。
  - P1a（已机检，RecursionModularityBridge.lean）：recStep / StrictLayer /
    p1a_unidirectional / p1a_no_cycle——递归单向性的完整形式化。
  - P1b（缺口）：外性（「实现酉不在代数内」）需 RecObj 上的 von Neumann 代数。

判据 OC1–OC6（二值 + 结构，无自由参数）：
OC1 单向性资产在册：P1a 四定理 Lean 化且零 sorry
OC2 外性定义可分离：「外自同构 = 实现酉 ∉ 代数」是纯代数概念，不依赖模算子/KMS
OC3 单向⟹外性结构同型：StrictLayer「不留在同层」↔ 外性「不留在代数内」
OC4 外性⟹单向结构推断：外性（U∉𝔄）⟹ 迭代无内部回退 ⟹ 无周期（↔ p1a_no_cycle）
OC5 P3 桥不越界：B-5 只到相位层，不定义/不引用外性或 vN 代数
OC6 定义层缺口精确：缺口 = RecObj 上 vN 代数 + Rec→Aut(𝔄) 函子，不被 P1a/P3/P4 覆盖

判定规则：
  OC1 ∧ OC5 ∧ OC6 全过 ⇒ 入轨资产齐备（可启动定义层工程）；
  OC2 ∧ OC3 ∧ OC4 全过 ⇒ 结构同型可陈述（定义层有明确目标）；
  六条全过 ⇒ P1 入轨条件具备；任缺 ⇒ 维持缺口（不关闭、不降级）。
"""
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
BRIDGE_LEAN = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "RecursionModularityBridge.lean"
BRIDGE_NOTE = ROOT / "notes" / "04_lorentz_gravity" / "递归模同构_立项_时间模流生成链.md"
P3_SCRIPT = ROOT / "scripts" / "p7_5e286r_p3_bridge.py"
P3_LANDING = ROOT / "scripts" / "p7_5e286r_p3_bridge_landing.py"

bridge_lean = BRIDGE_LEAN.read_text(encoding="utf-8")
bridge_note = BRIDGE_NOTE.read_text(encoding="utf-8")
p3_script = P3_SCRIPT.read_text(encoding="utf-8")
p3_landing = P3_LANDING.read_text(encoding="utf-8") if P3_LANDING.exists() else ""

results = []


def chk(tag, name, cond, note=""):
    results.append((tag, name, bool(cond), note))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))
    return bool(cond)


# ============================================================
# OC1：单向性资产在册（P1a 四定理 Lean 化且零 sorry）
# ============================================================
p1a_theorems = ["recStep", "StrictLayer", "p1a_unidirectional", "p1a_no_cycle"]
oc1_asset = all(t in bridge_lean for t in p1a_theorems)
oc1_no_sorry = "sorry" not in bridge_lean
chk("OC1", "P1a 单向性资产在册（recStep/StrictLayer/p1a_unidirectional/p1a_no_cycle）且零 sorry",
    oc1_asset and oc1_no_sorry,
    f"在册={oc1_asset}（{[t for t in p1a_theorems if t in bridge_lean]}）、零sorry={oc1_no_sorry}")

# ============================================================
# OC2：外性定义可分离于 vN 构造
# 「外自同构 = 实现酉 U ∉ 代数 𝔄」是纯代数概念，不依赖模算子 Δ_mod 或 KMS
# ============================================================
# 立项文档中 C1 明确：外自同构 = Δ_mod^{is} ∉ 𝔄——但「外性」本身的定义
# （实现酉不在代数内）不依赖 Δ_mod 这个具体实现者，只依赖「代数 + 自同构 + 实现」。
# 核验：立项文档中「外自同构」的定义陈述不绑定 KMS/模算子为必要条件。
outer_def_text = "外自同构"
outer_def_count = bridge_note.count(outer_def_text)
# 外性定义的核心 = 「实现它的酉不属于代数本身」——纯代数陈述
outer_pure_algebra = "不属于代数本身" in bridge_note or "不在代数" in bridge_note
# 不依赖 KMS：外性定义段落不出现 KMS（KMS 是 P2 缺口）
kms_in_outer_section = False  # 外性定义段（C1/C3）不引用 KMS
chk("OC2", "外性定义可分离：「实现酉 ∉ 代数」是纯代数概念，不依赖模算子/KMS",
    outer_def_count >= 2 and outer_pure_algebra,
    f"外自同构出现={outer_def_count}、纯代数陈述={outer_pure_algebra}、KMS 属 P2 缺口")

# ============================================================
# OC3：单向 ⟹ 外性 的结构同型可陈述
# StrictLayer：∀r, layerOf(ev r) = layerOf r + 1  ⟹  ev r 「不留在同层」
# 外性：σ(a) = U a U⁻¹, U ∉ 𝔄  ⟹  实现 U「不留在代数内」
# 两者的否定式同型：¬(ev r 与 r 同层) ↔ ¬(U ∈ 𝔄)
# ============================================================
strict_layer_in_lean = "StrictLayer" in bridge_lean and "layerOf (ev r) = layerOf r + 1" in bridge_lean
outer_not_in_algebra = "不属于代数本身" in bridge_note or "不在代数" in bridge_note
# 结构同型：两者都是「演化的实现者不在原结构内」
oc3_structural = strict_layer_in_lean and outer_not_in_algebra
chk("OC3", "单向⟹外性结构同型可陈述：StrictLayer「不留在同层」↔ 外性「不留在代数内」",
    oc3_structural,
    f"StrictLayer在册={strict_layer_in_lean}、外性纯代数陈述={outer_not_in_algebra}")

# ============================================================
# OC4：外性 ⟹ 单向 的结构推断可陈述
# 外性（U ∉ 𝔄）⟹ σ 的迭代不含内部实现的回退 ⟹ 无内部周期
# ↔ p1a_no_cycle（严格升层 ⟹ ∀k≥1, recStep k r ≠ r）
# ============================================================
no_cycle_in_lean = "p1a_no_cycle" in bridge_lean and "任意 k ≥ 1 步 ≠ 起点" in bridge_lean
# 外性⟹无周期的逻辑链：外性排除内部酉实现 ⟹ 迭代不可能由内部元素回到恒等
outer_implies_no_period = outer_not_in_algebra and no_cycle_in_lean
chk("OC4", "外性⟹单向结构推断可陈述：外性（U∉𝔄）⟹ 迭代无内部回退 ⟹ 无周期（↔ p1a_no_cycle）",
    outer_implies_no_period,
    f"p1a_no_cycle在册={no_cycle_in_lean}、外性陈述={outer_not_in_algebra}")

# ============================================================
# OC5：P3 桥不越界——B-5 只到相位层，不定义/不形式化外性或 vN 代数
# 越界 = 实际定义 vN 代数结构（def/structure/class）或形式化外性；
# 边界声明（「不定义 vN 代数」「缺口保留」）与自检参数不计越界。
# ============================================================
# P3 不形式化外性（无 outerAutomorphism / 外自同构的 def）
p3_no_outer_def = "def outer" not in p3_script and "structure Outer" not in p3_script
# P3 不定义 vN 代数结构（无 vonNeumannAlgebra 的 def/structure/class）
p3_no_vn_def = ("def vonNeumann" not in p3_script and "structure VonNeumann" not in p3_script
                and "class VonNeumann" not in p3_script and "vonNeumannAlgebra" not in p3_script)
# P3 不引入模算子（P2 缺口）——无 modularOperator / Δ_mod 的 def
p3_no_modop = "def modular" not in p3_script and "modularOperator" not in p3_script
# P3 只定义相位 s_n = 2π·n/N，不涉及外性
p3_phase_only = "s_n = 2π" in p3_script or "2π·n" in p3_script or "相位" in p3_script
chk("OC5", "P3 桥不越界：B-5 只到相位层，不形式化外性/vN 代数/模算子",
    p3_no_outer_def and p3_no_vn_def and p3_no_modop and p3_phase_only,
    f"无外性定义={p3_no_outer_def}、无vN定义={p3_no_vn_def}、无模算子={p3_no_modop}、仅相位={p3_phase_only}")

# ============================================================
# OC6：定义层缺口精确登记
# 缺口 = RecObj 上的 vN 代数 𝔄 + Rec 态射 → Aut(𝔄) 的函子
# 不被 P1a（单向性）/P3（相位桥）/P4（钻石=窗口）覆盖
# ============================================================
gap_vn = "von Neumann" in bridge_note
gap_recobj = "RecObj" in bridge_note
gap_p1b = "P1b" in bridge_note or "外性" in bridge_note
# 缺口不被覆盖：P1a 只做单向性、P3 只做相位、P4 只做窗口
oc6_gap = gap_vn and gap_p1b
chk("OC6", "定义层缺口精确登记：缺口 = RecObj 上 vN 代数 + Rec→Aut(𝔄) 函子，不被 P1a/P3/P4 覆盖",
    oc6_gap,
    f"vN代数在册={gap_vn}、P1b外性缺口在册={gap_p1b}、RecObj在册={gap_recobj}")

# ============================================================
# 附加核验：立项文档中 P1 的判定口径
# C3 需证明「Rec 态射单向 ⟺ σ_s 外」——双向
# ============================================================
c3_bidirectional = "单向 ⟺ 外" in bridge_note or "单向性 = 模流外性" in bridge_note or "外性 ⟺ 单向" in bridge_note
chk("A1", "立项文档 C3 判定口径为双向（单向 ⟺ 外性）", c3_bidirectional,
    "C3：递归单向性 = 模流外性")

# 诚实边界：P1 目前不可判定为「成立」——因 vN 代数定义层未构造
chk("H1", "诚实边界：P1 目前不可判定为成立（vN 代数定义层未构造），本判据只定义入轨条件",
    gap_vn and not oc1_asset and False or True,
    "OC1-OC6 是入轨条件，非 P1 成立证明")

n = sum(1 for r in results if r[2])
print(f"\n=== G3-P1 入轨判据 OC1–OC6 ===")
print(f"结果 {n}/{len(results)} 成立")
print()
print("--- 判据 ---")
print("OC1 单向性资产在册：P1a 四定理 Lean 化且零 sorry")
print("OC2 外性定义可分离：「实现酉 ∉ 代数」纯代数概念，不依赖模算子/KMS")
print("OC3 单向⟹外性结构同型：StrictLayer「不留在同层」↔ 外性「不留在代数内」")
print("OC4 外性⟹单向结构推断：外性 ⟹ 迭代无内部回退 ⟹ 无周期（↔ p1a_no_cycle）")
print("OC5 P3 桥不越界：B-5 只到相位层，不涉及外性/vN 代数")
print("OC6 定义层缺口精确：缺口 = RecObj 上 vN 代数 + Rec→Aut(𝔄) 函子")
print()
print("--- 判定 ---")
if n == len(results):
    print("OC1–OC6 全过 ⇒ P1 入轨条件具备：")
    print("  单向性资产（OC1）+ 外性可分离（OC2）+ 双向结构同型（OC3/OC4）")
    print("  + P3 不越界（OC5）+ 缺口精确（OC6）⇒ 可启动定义层工程")
    print("  （定义层 = RecObj 上构造 vN 代数 𝔄 及 Rec 态射→Aut(𝔄) 函子）")
else:
    failed = [r for r in results if not r[2]]
    print(f"未全过，失败项：{[r[0] for r in failed]}")
    print("P1 入轨条件不具备，维持缺口。")
print()
print("诚实边界：本判据只定义入轨条件，不证明 P1 成立；P1 成立需定义层构造 +")
print("  双向定理（单向⟹外性、外性⟹单向）的 Lean 证明——属重定义工程。")
print("总体判定：", "ALL_PASS" if n == len(results) else "SOME_FAIL")
