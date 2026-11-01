# -*- coding: utf-8 -*-
"""P7-5e-348 落盘：RS 339 / paper48 286bb / roadmap P7-5e-348 / 纪要 六十三节

幂等：标记存在即跳过；锚点 count==1 断言；ROAD 维护 CRLF。
用法：probe | apply | verify
"""
import sys
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
P48 = ROOT / "paper" / "paper48_topological_forbidden_frequency.md"
ROAD = ROOT / "roadmap" / "phase102_baryon_lepton_parameter_free.md"
DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")

A_RS = "候选公设「常数↔角色双射」只登记、不升定案层（须用户裁决）。不关闭任何项（k(2) 仍开放、226 仍挂起）。本轮无 Lean 增量（整数枚举与来源计数）。"
A_P48 = "结论：结构演化成立但为描述级（层级生成非动力学演化）；现架构下必然性不可判定。不关闭任何项。脚本 19/19 ALL_PASS。"
A_ROAD = "结论：结构演化=描述级层级生成；必然性现架构下不可判定。不关闭任何项。"

SEG_RS = (
    "> **339（本轮，全链回扫修正——递归=时间・三层时间・5 的时间闭角色，2026-11-01）**：接 338。"
    "用户指出：递归=时间已形式化、时间已分三层（S47/S150，RapidityTimeLayering 43 定理，#44/#47 机检）。"
    "故 338 三处结论须更正。判别（脚本 27/27 ALL_PASS，精确有理禁浮点；A 组只核对既有资产不新证）。"
    "**更正一（结构演化口径）**——338「仅描述级、无时间/态变」**撤回**。正确处理：参数链是**可时间参数化的分层生成**——"
    "指数即开放递归步数 n（Δφ=ln2 每步翻倍 ⇒ 2^n = 每步态空间维数），n=4 ⟹ 2⁴=16=Cl(1,3) 全代数、15=16−1；"
    "层序＝逻辑依赖、步进＝时间递进（E1/E2：θ_n=arcsin(tanh(n·ln2))、γ_n=cosh(n·ln2)、cosh(n·ln2)·cosθ_n=1）。"
    "但**两个对象须分开**：三层时间是表达/读数分层（递归层→谱层→物理层），五段链是参数生成分段（差/乘/加/幂/像/谱）；"
    "五段链 ≠ 三层时间，其时间化仅通过「指数=步数」接口。"
    "**更正二（5 的角色）**——338「5 无第二角色 ⇒ 无幂型落地」**撤回**。5 角色至少六职："
    "k−3（静默定义）、冻结区整点数 |{4,5,6,7,8}|=5（S151）、时间闭（韦达根 5=4+1）、4·cosh(ln2)=5（单步 γ_1=5/4 整数化）、"
    "5×13=65（窗口端点）、2²+1（费马 F1）。⇒「单源」仅就**表达式层**成立，角色层不单源。"
    "**更正三（像层判据）**——338 所列 {3,7,15,63,127,257} 混入 7（塔锚指数，323 段）与 127（S223 五式 2^{3+4}−1），且漏分母支。"
    "正确像层＝勾股族分子/分母 {2^{2n}±1}，n=1..4 ⇒ {3,5}、{15,17}、{63,65}、{255,257}；5 亦为像层分母（单步 γ 读数）。"
    "**新恒等 I-V1（候选观察，不升格）**：4·sinh(ln2)=3、4·cosh(ln2)=5；与韦达根 {3,5}（和=8=k_max、积=15=σ⁻¹）集合级相等 "
    "⇒ 韦达根的时间开闭语义（3=时间开、5=时间闭，S151）获得**算子读数候选**：开↔sinh 支（奇/推进）、闭↔cosh 支（偶/闭合）。"
    "机制候选 **M-time**（活跃↔sinh、静默↔cosh）只登记，不升定案层。"
    "**必然性重判**——由「不可判定」改为**条件必然**。机制：指数＝开放递归步数；5＝时间闭（冻结零测度）⇒ 2⁵ 非开放态空间"
    "（32 仅作 n=4 勾股中间腿 2^{n+1}，非层常数）⇒ 塔止于 2⁴；4＝最后开放步（4 步 ⟹ 16 全代数）。"
    "且 5=2+3 属 S223 算术闭包 ⇒ 5 的排除依据是**静默（时间闭）条款**，非算术不可达。"
    "条件三条：递归即时间（已证）∧ 5=时间闭（S151：语义指认＋机检算术 active_silence_partition/silence_frozen_interval）∧ Δφ=ln2 与 4 步全代数（已采纳）。"
    "**诚实边界**：三条件中「5=时间闭」属语义指认层；Rec↔模流桥 P1–P4 仍「未定义」（立项未完成）⇒ **范畴级必然性未闭合**，不得称「范畴导出」。"
    "不关闭任何项（k(2) 仍开放、226 仍挂起）。本轮无 Lean 增量（整数/有理恒等与资产核对）。候选 I-V1 与 M-time 须用户裁决。"
)

SEG_P48 = (
    "286bb（2026-11-01，回扫修正：递归=时间与三层时间）**：338 三处更正——① 结构演化口径：撤回「仅描述级」，"
    "改为可时间参数化的分层生成（指数=开放递归步数 n，Δφ=ln2 每步 2^n 态空间，n=4 ⟹ 16=Cl(1,3)；但五段链≠三层时间，"
    "五段链是参数分段、三层时间是表达分层，接口仅「指数=步数」）；② 5 的角色：撤回「无第二角色」，5 至少六职"
    "（k−3、冻结区整点数、时间闭、4cosh(ln2)、5×13=65、F1）；③ 像层判据更正：应为勾股族分子/分母 {2^{2n}±1} n=1..4"
    "={3,5,15,17,63,65,255,257}，338 误含 7（塔锚指数）与 127（S223 五式）并漏分母支。新恒等 I-V1（候选）："
    "4sinh(ln2)=3、4cosh(ln2)=5 ↔ 韦达根 {3,5}；机制候选 M-time（活跃↔sinh、静默↔cosh）。必然性重判为**条件必然**："
    "指数=开放步、5=时间闭 ⇒ 2^5 非开放态空间（32 仅为 n=4 勾股中间腿）⇒ 塔止于 2^4；条件=递归即时间∧5=时间闭∧Δφ=ln2/4 步全代数；"
    "范畴级未闭合（模流桥 P1–P4 未定义）。不关闭任何项。脚本 27/27 ALL_PASS。"
)

SEG_ROAD = (
    "P7-5e-348（回扫修正：递归=时间与三层时间，2026-11-01）**：接 347。据用户指认（递归=时间已形式化、时间分三层 S47/S150）"
    "更正 338 三处：结构演化由「仅描述级」改为「可时间参数化的分层生成」（指数=开放步数，Δφ=ln2，4 步 ⟹ 16=Cl(1,3)）；"
    "5 由「无第二角色」改为六职（k−3/冻结区整点/时间闭/4cosh(ln2)/65/F1）；像层改为勾股族 {3,5,15,17,63,65,255,257}。"
    "新恒等 I-V1（4sinh(ln2)=3、4cosh(ln2)=5 ↔ 韦达根 {3,5}）与机制 M-time 登记为候选。必然性：条件必然"
    "（5=时间闭 ⇒ 2^5 非开放态空间 ⇒ 塔止 2^4）；范畴级未闭合。不关闭任何项。"
)

SEG_DIG = (
    "\n## 六十三、全链回扫修正：递归=时间、三层时间与 5 的时间闭角色（2026-11-01）\n\n"
    "**触发**：用户指出「递归就是时间，时间是分了三层」已形式化（RapidityTimeLayering 43 定理、#44/#47 机检、S47/S150 三层时间），"
    "故上一轮（六十二节）的「仅描述级 / 不可判定」结论须更正。\n\n"
    "**更正一（结构演化）**：参数链不是静态分层，而是**可时间参数化的分层生成**——指数即开放递归步数 n，"
    "Δφ=ln2 使每步态空间翻倍（2^n），n=4 ⟹ 2⁴=16=Cl(1,3) 全代数、15=16−1；步进读数 θ_n=arcsin(tanh(n·ln2))、γ_n=cosh(n·ln2)。"
    "但须分清：三层时间（递归→谱→物理）是**表达/读数分层**，五段参数链是**参数生成分段**，二者不等同，接口只有「指数=步数」。\n\n"
    "**更正二（5 的角色）**：5 并非「无第二角色」，至少六职——k−3、冻结区整点数 |{4,5,6,7,8}|、时间闭（韦达根 5=4+1）、"
    "4cosh(ln2)=5（单步 γ_1=5/4）、5×13=65、F1=2²+1。「单源」只在表达式层成立。\n\n"
    "**更正三（像层）**：像层应为勾股族分子/分母 {2^{2n}±1}（n=1..4）= {3,5}、{15,17}、{63,65}、{255,257}；"
    "旧表误收 7（塔锚指数）与 127（S223 五式），且漏分母支——5 正是单步 γ 的分母。\n\n"
    "**新恒等 I-V1（候选）**：4·sinh(ln2)=3、4·cosh(ln2)=5，与韦达根 {3,5}（和 8、积 15）集合级相等 ⇒ "
    "「3=时间开、5=时间闭」（S151）获得算子读数候选：开↔sinh（奇/推进）、闭↔cosh（偶/闭合）。机制候选 **M-time** 只登记。\n\n"
    "**必然性重判：条件必然**。指数＝开放递归步数；5＝时间闭（冻结零测度）⇒ 2⁵ 非开放态空间（32 仅作 n=4 勾股中间腿）"
    "⇒ 塔止于 2⁴，4＝最后开放步。5=2+3 本属 S223 算术闭包，故排除依据是静默（时间闭）条款而非算术不可达。"
    "条件三条：递归即时间、5=时间闭（语义指认＋机检算术）、Δφ=ln2 与 4 步全代数（已采纳）。\n\n"
    "**诚实边界**：条件中「5=时间闭」为语义指认层；Rec↔模流桥 P1–P4 仍「未定义」⇒ 范畴级必然性未闭合，不得称范畴导出。"
    "不关闭任何项；无 Lean 增量；脚本 27/27 ALL_PASS。\n"
)

MARK = {
    "rs": "> **339（本轮，全链回扫修正",
    "p48": "286bb（2026-11-01，回扫修正",
    "road": "P7-5e-348（回扫修正",
    "dig": "六十三、全链回扫修正",
}


def nl_of(t):
    return "\r\n" if "\r\n" in t else "\n"


def read_keep(p):
    """保留原换行（newline='' 不做 CRLF→LF 翻译，避免破坏 ROAD 字节纪律）。"""
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def probe():
    rs, p48, road, dig = (read_keep(p) for p in (RS, P48, ROAD, DIG))
    print("RS a1 count=%d" % rs.count(A_RS))
    print("P48 a2 count=%d" % p48.count(A_P48))
    print("ROAD a3 count=%d" % road.count(A_ROAD))
    print("ROAD CRLF=%d LF-solo=%d" % (road.count("\r\n"), road.count("\n") - road.count("\r\n")))


def apply():
    rs, p48, road = (read_keep(p) for p in (RS, P48, ROAD))
    dig = read_keep(DIG)
    if MARK["rs"] in rs:
        print("RS 339 已存在，跳过")
    else:
        assert rs.count(A_RS) == 1, "RS anchor count=%d" % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + nl_of(rs) + SEG_RS, 1)
        RS.write_text(rs, encoding="utf-8", newline="")
        print("RS 339 写入")
    if MARK["p48"] in p48:
        print("P48 286bb 已存在，跳过")
    else:
        assert p48.count(A_P48) == 1, "P48 anchor count=%d" % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + nl_of(p48) + SEG_P48, 1)
        P48.write_text(p48, encoding="utf-8", newline="")
        print("P48 286bb 写入")
    if MARK["road"] in road:
        print("ROAD 348 已存在，跳过")
    else:
        assert road.count(A_ROAD) == 1, "ROAD anchor count=%d" % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + "\r\n" + SEG_ROAD, 1)
        ROAD.write_text(road, encoding="utf-8", newline="")
        print("ROAD 348 写入")
    if MARK["dig"] in dig:
        print("DIGEST 六十三节 已存在，跳过")
    else:
        assert dig.endswith("\n"), "digest tail not newline"
        DIG.write_text(dig + SEG_DIG, encoding="utf-8", newline="")
        print("DIGEST 六十三节 写入")
    print("APPLY DONE（幂等）：339/286bb/P7-5e-348/六十三节")


def verify():
    rs, p48, road, dig = (read_keep(p) for p in (RS, P48, ROAD, DIG))
    checks = [
        ("RS 339", rs.count(MARK["rs"]), 1),
        ("P48 286bb", p48.count(MARK["p48"]), 1),
        ("ROAD 348", road.count(MARK["road"]), 1),
        ("DIGEST 六十三", dig.count(MARK["dig"]), 1),
    ]
    ok = True
    for name, got, want in checks:
        print("%s count=%d" % (name, got))
        ok &= got == want
    crlf = road.count("\r\n")
    lf_solo = road.count("\n") - crlf
    print("ROAD CRLF=%d LF-solo=%d" % (crlf, lf_solo))
    ok &= (lf_solo == 0)
    print("VERIFY", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    {"probe": probe, "apply": apply, "verify": verify}[mode]()
