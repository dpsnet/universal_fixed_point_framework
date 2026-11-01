# -*- coding: utf-8 -*-
"""P7-5e-349 落盘：RS 340 / paper48 286bc / roadmap P7-5e-349 / 纪要 六十四节

幂等：标记存在即跳过；锚点 count==1 断言；ROAD 维护 CRLF（read_keep/newline=''）。
用法：probe | apply | verify
"""
import sys
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
P48 = ROOT / "paper" / "paper48_topological_forbidden_frequency.md"
ROAD = ROOT / "roadmap" / "phase102_baryon_lepton_parameter_free.md"
DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")

A_RS = "本轮无 Lean 增量（整数/有理恒等与资产核对）。候选 I-V1 与 M-time 须用户裁决。"
A_P48 = "范畴级未闭合（模流桥 P1–P4 未定义）。不关闭任何项。脚本 27/27 ALL_PASS。"
A_ROAD = "范畴级未闭合。不关闭任何项。"

SEG_RS = (
    "> **340（本轮，缺口优先级判别——范畴→物理导出主干上的必修缺口，2026-11-01）**：接 339。"
    "用户问：一切应为范畴到物理的导出服务，能否确定必须优先解决的缺口。"
    "判据（无权重、无自由参数；二值 + 依赖偏序）：Q1 主干性（缺它则某类物理输出无法从范畴读出）；"
    "Q2 不可替代（有无等价绕行）；Q3 需新定义层（是否先造 Rec 算子代数）；Q4 依赖位置。"
    "**必修集恰四枚**（Q1∧Q2 全真）：① **G1 映射锚定 MA1–MA3**（数值出口：范畴→测量唯一可证伪接口；"
    "226 的 mapping 半阻塞即此；不需新定义层 ⇒ 可立即启动）；② **G2 生成器 k(2)/1/m⁵**（数值出口：范畴→值；"
    "参数链目前只能枚举，生成谱假说代数映射未建立；以 ① 的映射形式作校验前提）；"
    "③ **G3 模流桥 P1–P4**（结构出口：范畴→时间唯一桥；RapidityTimeLayering 43 定理现为数学恒等，物理时间读出停在这条桥上；"
    "需新定义层 RecObj→von Neumann 代数）；④ **G4 三层态射→4 维（N_gen+1）**（结构出口：唯一维度出口；"
    "与 ③ 共享「三层态射↔三层时间」定义层，故同批立项）。"
    "**下游可延一枚**：⑤ G5 的 5=时间闭机检化（M-time：活跃↔sinh/静默↔cosh）——只把「塔止 2⁴」由条件必然升为定理，"
    "不动任何物理读数。**非阻塞六枚**：G6 载体非唯一、G7 m_ρ 微缺口、G8 I_e 间隔 7、G9 Cl(4) 集合级替代、"
    "G10 链类型判别对、G11 非对角谱熵（已移出清单）。**外部依赖不计缺口**：226 六字段数据、G1 的链类型外部新量。"
    "**排序（依赖偏序而非权重）**：G1 → G2 → G3 → G4 → G5；理由：G1 无前置且为 G2 校验前提；G3/G4 共享定义层（重定义工程）；"
    "G5 在 G3 下游（时间语义）。**反序说明（须用户裁决）**：若取「先立骨」，G3/G4 可提至 G1 之前；"
    "两序差别仅在「先可证伪 / 先闭合结构」，本轮按「可证伪性即导出判据」取 G1 先。"
    "不关闭任何项（k(2) 仍开放、226 仍挂起）。本轮无 Lean 增量（依赖图与分类判别）。"
)

SEG_P48 = (
    "286bc（2026-11-01，缺口优先级判别）**：准则四问（主干性/不可替代/需新定义层/依赖位置），二值＋依赖偏序，无权重。"
    "必修四枚：G1 映射锚定 MA1–MA3（数值出口，226 半阻塞）、G2 生成器 k(2)/1/m⁵（数值出口）、"
    "G3 模流桥 P1–P4（结构出口/时间，需新定义层）、G4 三层态射→4 维（结构出口，与 G3 同层）。"
    "下游可延：G5（5=时间闭机检化，仅使 2⁴ 止点定理化）。非阻塞六枚：载体非唯一、m_ρ、I_e、Cl(4)、链类型、非对角谱熵。"
    "排序 G1→G2→G3→G4→G5；反序（先立骨）可把 G3/G4 提前，须用户裁决。不关闭任何项。脚本 15/15 ALL_PASS。"
)

SEG_ROAD = (
    "P7-5e-349（缺口优先级判别，2026-11-01）**：接 348。按「一切为范畴→物理导出服务」定必修缺口四枚——"
    "G1 映射锚定（数值出口/226 半阻塞）、G2 生成器 k(2)（数值出口）、G3 模流桥 P1–P4（结构出口/时间/需新定义层）、"
    "G4 三层态射→4 维（结构出口/与 G3 同层）；下游可延 G5（5=时间闭机检化）；非阻塞六枚。"
    "排序 G1→G2→G3→G4→G5（依赖偏序无权重）；反序须用户裁决。不关闭任何项。"
)

SEG_DIG = (
    "\n## 六十四、缺口优先级：范畴→物理导出主干上的必修缺口（2026-11-01）\n\n"
    "**准则**（二值，无权重）：Q1 主干性（缺它则某类物理输出无法从范畴读出）｜Q2 不可替代（有无等价绕行）｜"
    "Q3 需新定义层｜Q4 依赖位置。必修＝Q1∧Q2。\n\n"
    "**必修四枚**\n\n"
    "| # | 缺口 | 出口 | 阻塞现状 | 是否需新定义层 |\n|---|---|---|---|---|\n"
    "| G1 | 映射锚定 MA1–MA3 | 数值 | 226 的 mapping 半阻塞；全部预测不可证伪 | 否（可立即启动） |\n"
    "| G2 | 生成器 k(2)/1/m⁵ | 数值 | 参数链只能枚举；生成谱假说映射未建立 | 否（以 G1 为校验前提） |\n"
    "| G3 | 模流桥 P1–P4 | 结构（时间） | 43 定理停在数学恒等；物理时间读出无桥 | 是（RecObj→von Neumann 代数） |\n"
    "| G4 | 三层态射→4 维 | 结构（时空） | 「为何 N_gen+1」归公设层 | 是（与 G3 共享定义层） |\n\n"
    "**下游可延**：G5（5=时间闭机检化，M-time）——只把「塔止 2⁴」由条件必然升为定理，不动任何读数。\n\n"
    "**非阻塞六枚**：载体非唯一、m_ρ 微缺口、I_e 间隔 7、Cl(4) 集合级替代、链类型判别对、非对角谱熵（已移出清单）。\n\n"
    "**排序（依赖偏序，非权重）**：G1 → G2 → G3 → G4 → G5。反序（「先立骨」把 G3/G4 提前）差别仅在"
    "「先可证伪 / 先闭合结构」，须用户裁决。\n\n"
    "**判据自我限定**：本轮只做排序，不关闭任何项、不新增公设；脚本 15/15 ALL_PASS，无 Lean 增量。\n"
)

MARK = {
    "rs": "> **340（本轮，缺口优先级判别",
    "p48": "286bc（2026-11-01，缺口优先级判别",
    "road": "P7-5e-349（缺口优先级判别",
    "dig": "六十四、缺口优先级",
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
        print("RS 340 已存在，跳过")
    else:
        assert rs.count(A_RS) == 1, "RS anchor count=%d" % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + nl_of(rs) + SEG_RS, 1)
        RS.write_text(rs, encoding="utf-8", newline="")
        print("RS 340 写入")
    if MARK["p48"] in p48:
        print("P48 286bc 已存在，跳过")
    else:
        assert p48.count(A_P48) == 1, "P48 anchor count=%d" % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + nl_of(p48) + SEG_P48, 1)
        P48.write_text(p48, encoding="utf-8", newline="")
        print("P48 286bc 写入")
    if MARK["road"] in road:
        print("ROAD 349 已存在，跳过")
    else:
        assert road.count(A_ROAD) == 1, "ROAD anchor count=%d" % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + "\r\n" + SEG_ROAD, 1)
        ROAD.write_text(road, encoding="utf-8", newline="")
        print("ROAD 349 写入")
    if MARK["dig"] in dig:
        print("DIGEST 六十四节 已存在，跳过")
    else:
        assert dig.endswith("\n"), "digest tail not newline"
        DIG.write_text(dig + SEG_DIG, encoding="utf-8", newline="")
        print("DIGEST 六十四节 写入")
    print("APPLY DONE（幂等）：340/286bc/P7-5e-349/六十四节")


def verify():
    rs, p48, road, dig = (read_keep(p) for p in (RS, P48, ROAD, DIG))
    ok = True
    for name, got in [("RS 340", rs.count(MARK["rs"])) , ("P48 286bc", p48.count(MARK["p48"])),
                      ("ROAD 349", road.count(MARK["road"])), ("DIGEST 六十四", dig.count(MARK["dig"]))]:
        print("%s count=%d" % (name, got))
        ok &= got == 1
    crlf, lf_solo = road.count("\r\n"), road.count("\n") - road.count("\r\n")
    print("ROAD CRLF=%d LF-solo=%d" % (crlf, lf_solo))
    ok &= lf_solo == 0
    print("VERIFY", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    {"probe": probe, "apply": apply, "verify": verify}[mode]()
