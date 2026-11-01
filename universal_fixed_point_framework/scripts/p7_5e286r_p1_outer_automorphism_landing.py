# -*- coding: utf-8 -*-
"""P7-5e-352 落盘：RS 343 / paper48 286bf / roadmap P7-5e-352 / 纪要 六十七节

内容：G3-P1 入轨判据 OC1–OC6（σ_s 外自同构 ⟺ 递归单向的入轨条件）。
幂等 + 锚点 count==1 + ROAD CRLF 纪律（read_keep / newline=''）。
"""
import sys
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
P48 = ROOT / "paper" / "paper48_topological_forbidden_frequency.md"
ROAD = ROOT / "roadmap" / "phase102_baryon_lepton_parameter_free.md"
DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")

A_RS = "不关闭任何项（226 仍挂起、k(2) 仍开放）。本轮无 Lean 增量（相位层结构判别）。"
A_P48 = "诚实边界：N=5 由 S151 语义指认非代数导出；P1/P2 缺口保留。不关闭任何项。"
A_ROAD = "边界=相位层，P1(vN代数)/P2(模算子) 缺口保留。不关闭任何项。"

SEG_RS = (
    "> **343（本轮，G3-P1 入轨判据 OC1–OC6：σ_s 外自同构 ⟺ 递归单向，2026-11-01）**：接 342（P3 B-5 相位桥）。"
    "执行「先立骨」下一对象 P1，但 P1 是重定义工程（需 RecObj 上 von Neumann 代数），本轮只做**入轨判据**——"
    "类比 G5-M1 的 MA1–MA6（映射锚定判据），明确 P1 闭合的可核验条件，不直接写 Lean 定义层。"
    "边界声明：不定义 RecObj 上的 von Neumann 代数（P1b 缺口）、不引入模算子（P2 缺口）；只做入轨条件判别。"
    "**判据 OC1–OC6**（脚本 8/8 ALL_PASS）："
    "OC1 单向性资产在册——P1a 四定理（recStep/StrictLayer/p1a_unidirectional/p1a_no_cycle）Lean 化且零 sorry；"
    "OC2 外性定义可分离——「外自同构 = 实现酉 ∉ 代数」是纯代数概念，不依赖模算子 Δ_mod 或 KMS；"
    "OC3 单向⟹外性结构同型可陈述——StrictLayer「ev 不留在同层」↔ 外性「U 不留在代数内」（两者否定式同型）；"
    "OC4 外性⟹单向结构推断可陈述——外性（U∉𝔄）⟹ 迭代无内部回退 ⟹ 无周期（↔ p1a_no_cycle）；"
    "OC5 P3 桥不越界——B-5 只到相位层，不形式化外性/vN 代数/模算子（边界声明提及不计）；"
    "OC6 定义层缺口精确——缺口 = RecObj 上 vN 代数 𝔄 + Rec 态射→Aut(𝔄) 函子，不被 P1a/P3/P4 覆盖。"
    "**判定**：OC1–OC6 全过 ⇒ P1 入轨条件具备——单向性资产（OC1）+ 外性可分离（OC2）+ 双向结构同型（OC3/OC4）"
    "+ P3 不越界（OC5）+ 缺口精确（OC6）⇒ 可启动定义层工程。"
    "**诚实边界**：入轨条件具备 ≠ P1 成立；P1 成立需定义层构造（RecObj 上 vN 代数 + Rec→Aut 函子）"
    "+ 双向定理（单向⟹外性、外性⟹单向）的 Lean 证明——属重定义工程，本轮不启动。"
    "不关闭任何项（226 仍挂起、k(2) 仍开放）。本轮无 Lean 增量（入轨判据定义）。"
)

SEG_P48 = (
    "286bf（2026-11-01，G3-P1 入轨判据 OC1–OC6）**：P1=σ_s 外自同构 ⟺ 递归单向；P1a（单向性）已机检，P1b（外性）需 vN 代数。"
    "本轮定义入轨判据 OC1–OC6（类比 MA1–MA6），脚本 8/8 ALL_PASS："
    "OC1 P1a 四定理在册零sorry；OC2 外性=实现酉∉代数（纯代数，不依赖模算子/KMS）；"
    "OC3 单向⟹外性同型（不留在同层↔不留在代数内）；OC4 外性⟹单向推断（U∉𝔄⟹无回退⟹无周期）；"
    "OC5 P3 B-5 不越界（仅相位层）；OC6 缺口=RecObj 上 vN 代数+Rec→Aut(𝔄) 函子。"
    "判定：入轨条件具备，可启动定义层工程；入轨≠成立，P1 成立需 vN 代数构造+双向定理证明。不关闭任何项。"
)

SEG_ROAD = (
    "P7-5e-352（G3-P1 入轨判据 OC1–OC6，2026-11-01）**：接 351。P1=σ_s 外 ⟺ 递归单向；"
    "P1a（单向性 recStep/StrictLayer/p1a_no_cycle）已机检，P1b（外性）需 RecObj 上 vN 代数。"
    "本轮定义入轨判据 OC1–OC6（类比 MA1–MA6）8/8 ALL_PASS："
    "OC1 单向性资产在册；OC2 外性可分离于模算子/KMS；OC3 单向⟹外性同型（不留在同层↔不留在代数内）；"
    "OC4 外性⟹单向推断（U∉𝔄⟹无周期）；OC5 P3 不越界；OC6 缺口=vN 代数+Rec→Aut 函子。"
    "判定：入轨条件具备，可启动定义层工程；入轨≠成立（需 vN 构造+双向定理）。不关闭任何项。"
)

SEG_DIG = (
    "\n## 六十七、G3-P1 入轨判据 OC1–OC6（σ_s 外自同构 ⟺ 递归单向，2026-11-01）\n\n"
    "**边界**：不定义 RecObj 上的 von Neumann 代数（P1b 缺口）、不引入模算子（P2 缺口）；只做入轨条件判别，不写 Lean 定义层。\n\n"
    "**P1 命题**（立项文档 §3）：σ_s 外自同构 ⟺ 递归单向。\n"
    "- P1a（已机检，RecursionModularityBridge.lean）：recStep / StrictLayer / p1a_unidirectional / p1a_no_cycle——递归单向性的完整形式化；\n"
    "- P1b（缺口）：外性（「实现酉不在代数内」）需 RecObj 上的 von Neumann 代数。\n\n"
    "**入轨判据 OC1–OC6**（类比 G5-M1 的 MA1–MA6）\n\n"
    "| 判据 | 内容 | 结果 |\n|---|---|---|\n"
    "| OC1 单向性资产 | P1a 四定理 Lean 化且零 sorry | ✓ |\n"
    "| OC2 外性可分离 | 「实现酉 ∉ 代数」纯代数概念，不依赖模算子/KMS | ✓ |\n"
    "| OC3 单向⟹外性 | StrictLayer「不留在同层」↔ 外性「不留在代数内」 | ✓ |\n"
    "| OC4 外性⟹单向 | 外性（U∉𝔄）⟹ 迭代无内部回退 ⟹ 无周期（↔ p1a_no_cycle） | ✓ |\n"
    "| OC5 P3 不越界 | B-5 只到相位层，不形式化外性/vN 代数/模算子 | ✓ |\n"
    "| OC6 缺口精确 | 缺口 = RecObj 上 vN 代数 𝔄 + Rec→Aut(𝔄) 函子 | ✓ |\n\n"
    "**判定 8/8 ALL_PASS**：OC1–OC6 全过 ⇒ P1 入轨条件具备。\n\n"
    "- 单向性资产（OC1）+ 外性可分离（OC2）+ 双向结构同型（OC3/OC4）+ P3 不越界（OC5）+ 缺口精确（OC6）⇒ 可启动定义层工程；\n"
    "- 定义层 = RecObj 上构造 vN 代数 𝔄 及 Rec 态射→Aut(𝔄) 函子。\n\n"
    "**诚实边界**：入轨条件具备 ≠ P1 成立。P1 成立需：① 定义层构造（vN 代数 + Rec→Aut 函子）；② 双向定理（单向⟹外性、外性⟹单向）的 Lean 证明——属重定义工程，本轮不启动。\n\n"
    "**保留缺口**：P1b（vN 代数定义层）、P2（KMS β=1 ⟺ 递归热化，需模算子）。本轮不关闭任何项。\n"
)

MARK = {
    "rs": "> **343（本轮，G3-P1 入轨判据",
    "p48": "286bf（2026-11-01，G3-P1 入轨判据",
    "road": "P7-5e-352（G3-P1 入轨判据",
    "dig": "六十七、G3-P1 入轨判据",
}


def read_keep(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def nl_of(t):
    return "\r\n" if "\r\n" in t else "\n"


def probe():
    rs, p48, road = (read_keep(p) for p in (RS, P48, ROAD))
    print("RS a1 count=%d" % rs.count(A_RS))
    print("P48 a2 count=%d" % p48.count(A_P48))
    print("ROAD a3 count=%d" % road.count(A_ROAD))
    print("ROAD CRLF=%d LF-solo=%d" % (road.count("\r\n"), road.count("\n") - road.count("\r\n")))


def apply():
    rs, p48, road, dig = (read_keep(p) for p in (RS, P48, ROAD, DIG))
    if MARK["rs"] in rs:
        print("RS 343 已存在，跳过")
    else:
        assert rs.count(A_RS) == 1, "RS anchor count=%d" % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + nl_of(rs) + SEG_RS, 1)
        RS.write_text(rs, encoding="utf-8", newline="")
        print("RS 343 写入")
    if MARK["p48"] in p48:
        print("P48 286bf 已存在，跳过")
    else:
        assert p48.count(A_P48) == 1, "P48 anchor count=%d" % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + nl_of(p48) + SEG_P48, 1)
        P48.write_text(p48, encoding="utf-8", newline="")
        print("P48 286bf 写入")
    if MARK["road"] in road:
        print("ROAD 352 已存在，跳过")
    else:
        assert road.count(A_ROAD) == 1, "ROAD anchor count=%d" % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + "\r\n" + SEG_ROAD, 1)
        ROAD.write_text(road, encoding="utf-8", newline="")
        print("ROAD 352 写入")
    if MARK["dig"] in dig:
        print("DIGEST 六十七节 已存在，跳过")
    else:
        assert dig.endswith("\n"), "digest tail not newline"
        DIG.write_text(dig + SEG_DIG, encoding="utf-8", newline="")
        print("DIGEST 六十七节 写入")
    print("APPLY DONE（幂等）：343/286bf/P7-5e-352/六十七节")


def verify():
    rs, p48, road, dig = (read_keep(p) for p in (RS, P48, ROAD, DIG))
    ok = True
    for name, got in [("RS 343", rs.count(MARK["rs"])), ("P48 286bf", p48.count(MARK["p48"])),
                      ("ROAD 352", road.count(MARK["road"])), ("DIGEST 六十七", dig.count(MARK["dig"]))]:
        print("%s count=%d" % (name, got))
        ok &= got == 1
    crlf, lf_solo = road.count("\r\n"), road.count("\n") - road.count("\r\n")
    print("ROAD CRLF=%d LF-solo=%d" % (crlf, lf_solo))
    ok &= lf_solo == 0
    print("VERIFY", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    {"probe": probe, "apply": apply, "verify": verify}[mode]()
