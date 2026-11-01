# -*- coding: utf-8 -*-
"""P7-5e-360 落盘：RS 351 / paper48 286bn / roadmap P7-5e-360 / 纪要 七十五节

内容：G2-1——闭式谱 5 系数由词表 {k=8, b=5, 幂基 2} 5/5 写出；单一有理式
P(m)/(16000m³) 在 m=1..12 精确相等；指数窗 [−3,+1] ⇒ 无 m⁻⁴/m⁻⁵ ⇒ 无 1/m⁵ 生成项；
k(2) 两候选均属同一词表 ⇒ 结构对称、仍不可择一。G2 未闭合；不关闭任何项。
幂等 + 锚点 count==1 + ROAD CRLF 纪律（read_keep / newline=''）。
"""
import sys
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
P48 = ROOT / "paper" / "paper48_topological_forbidden_frequency.md"
ROAD = ROOT / "roadmap" / "phase102_baryon_lepton_parameter_free.md"
DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")

A_RS = "本轮无 Lean 增量（映射登记与 MA1–MA3 逐条核验）。"
A_P48 = "**G1 未闭合**（映射登记 ≠ 锚定成立）。不关闭任何项。"
A_ROAD = "G1 未闭合（映射登记 ≠ 锚定成立），不关闭任何项（226 挂起、k(2) 开放）。"

SEG_RS = (
    "> **351（本轮，G2-1：生成器——闭式谱词表、单一有理式与 k(2) 两候选结构对称，2026-11-01）**：接 350。"
    "G2 口径（纪要六十四节）＝生成器 k(2)/1/m⁵；数值出口，以 G1 的映射形式为校验前提。"
    "本轮不新建定义层、无 Lean 增量，只做词表登记与形式复算（精确分数，无浮点）："
    "①**词表三原语** = {k=8（k_max）、b=5（静默）、幂基 2}；"
    "②**5 系数 5/5 可写**：1/2、1/k、13/2^(k−1)、(kb+1)/(2^(k−4)b³)、−(kb−1)/(2^(k−4)b³)；"
    "③**单一有理式** s(m)=P(m)/(2^(k−1)b³m³)=P(m)/(16000m³)，"
    "P(m)=8000m⁴+2000m³+1625m²+328m−312，m=1..12 与原闭式精确相等（12/12）；"
    "④**指数窗 [−3,+1]**：P 为 4 次多项式且常数项非零 ⇒ m⁻⁴/m⁻⁵ 位置为空，"
    "与四十六节「无 m⁻⁴/m⁻⁵ 项」一致 ⇒ **无 1/m⁵ 生成项**；"
    "⑤**两候选结构对称机检**：−3/272 = −(k−b)/(2^(k−4)(2^(k−4)+1))、"
    "−11/997 = −(2k−b)/(2^(k−5)b³−(k−b))，两式均只由词表生成 ⇒ 无结构偏好。"
    "判据脚本 `scripts/p7_5e286r_g2_generator_criteria.py` A1–F3，**22/22 ALL_PASS**。"
    "**判定**：k(2) 仍不可择一（提取误差未量化 + 结构对称 + 无 1/m⁵ 生成项）⇒ "
    "维持观察身份开放（不升格、不锁定、不关闭）。"
    "**G1 前提**：G1 登记 M3（生成谱假说）MA1 缺 ⇒ G2 的数值输出在 M3 映射建立前**不可证伪**。"
    "**诚实边界**：**表达式 ≠ 生成机制**——词表统一只是重述级登记，未给出 1/m⁵ 生成函数；"
    "指数窗为形式复算，不解释窗长 5 的语义；两候选不删除（保留未证伪路径）；**G2 未闭合**。"
    "不关闭任何项（226 仍挂起、k(2) 仍开放）。"
    "本轮无 Lean 增量（生成器词表与指数窗精确复算）；G2 未闭合。"
)

SEG_P48 = (
    "286bn（2026-11-01，G2-1：生成器——闭式谱词表、单一有理式与 k(2) 两候选结构对称）**："
    "G2 口径 = 生成器 k(2)/1/m⁵（数值出口，以 G1 映射形式为校验前提）。"
    "词表三原语 {k=8, b=5, 幂基 2}：5 系数 5/5 可写为 1/2、1/k、13/2^(k−1)、"
    "(kb+1)/(2^(k−4)b³)、−(kb−1)/(2^(k−4)b³)；单一有理式 s(m)=P(m)/(16000m³)，"
    "P=8000m⁴+2000m³+1625m²+328m−312，m=1..12 精确相等；指数窗 [−3,+1] ⇒ 无 m⁻⁴/m⁻⁵ ⇒ "
    "无 1/m⁵ 生成项（与四十六节一致）；两候选 −3/272 = −(k−b)/(2^(k−4)(2^(k−4)+1))、"
    "−11/997 = −(2k−b)/(2^(k−5)b³−(k−b)) 同属词表 ⇒ 结构对称、仍不可择一（误差未量化）。"
    "判据 22/22 ALL_PASS。G1 前提：M3 MA1 缺 ⇒ G2 输出不可证伪。"
    "诚实边界：表达式 ≠ 生成机制；指数窗为形式复算；k(2) 维持观察身份开放。"
    "**G2 未闭合**（表达式 ≠ 生成机制）。不关闭任何项。"
)

SEG_ROAD = (
    "P7-5e-360（G2-1：生成器——闭式谱词表、单一有理式与 k(2) 两候选结构对称，2026-11-01）**：接 359。"
    "G2 口径 = 生成器 k(2)/1/m⁵（数值出口，以 G1 映射形式为校验前提）。"
    "词表 {k=8, b=5, 幂基 2}：5 系数 5/5 可写；单一有理式 P(m)/(16000m³) "
    "（P=8000m⁴+2000m³+1625m²+328m−312）在 m=1..12 精确相等；"
    "指数窗 [−3,+1] ⇒ 无 m⁻⁴/m⁻⁵ ⇒ 无 1/m⁵ 生成项；"
    "两候选 −3/272 = −(k−b)/(2^(k−4)(2^(k−4)+1))、−11/997 = −(2k−b)/(2^(k−5)b³−(k−b)) "
    "同属词表 ⇒ 结构对称、仍不可择一。判据 A1–F3 22/22 ALL_PASS。"
    "G1 前提：M3 MA1 缺 ⇒ G2 输出不可证伪。"
    "G2 未闭合（表达式 ≠ 生成机制），不关闭任何项（226 挂起、k(2) 开放）。"
)

SEG_DIG = (
    "\n## 七十五、G2-1：生成器——闭式谱词表、单一有理式与 k(2) 两候选结构对称（2026-11-01）\n\n"
    "**口径（六十四节表）**：G2 = 生成器 k(2)/1/m⁵；数值出口；以 G1 的映射形式为校验前提。"
    "本轮不新建定义层、无 Lean 增量，只做词表登记与形式复算（精确分数，无浮点）。\n\n"
    "**词表三原语**：{k = 8（k_max）、b = 5（静默）、幂基 2}。\n\n"
    "**5 系数 5/5 可写（精确）**\n\n"
    "| 位置 | 闭式系数 | 词表表达式 |\n|---|---|---|\n"
    "| m⁺¹ | 1/2 | 1 / 幂基 |\n"
    "| m⁰ | 1/8 | 1 / k |\n"
    "| m⁻¹ | 13/128 | (k + b) / 2^(k−1) |\n"
    "| m⁻² | 41/2000 | (k·b + 1) / (2^(k−4)·b³) |\n"
    "| m⁻³ | −39/2000 | −(k·b − 1) / (2^(k−4)·b³) |\n\n"
    "**单一有理式（新）**：s(m) = P(m) / (2^(k−1)·b³·m³) = P(m) / (16000 m³)，"
    "P(m) = 8000m⁴ + 2000m³ + 1625m² + 328m − 312；"
    "判据在 m=1..12 逐点精确相等（12/12）。这替代了「参数链只能枚举」的旧口径——"
    "但只到**表达式**层，不是生成机制。\n\n"
    "**指数窗 [−3, +1]（形式复算）**：P 为 4 次多项式、常数项非零 ⇒ "
    "最高指数 4−3 = +1、最低指数 0−3 = −3 ⇒ **m⁻⁴/m⁻⁵ 位置为空**，"
    "与四十六节「无 m⁻⁴/m⁻⁵ 项」一致 ⇒ 闭式谱**无 1/m⁵ 生成项**。\n\n"
    "**k(2) 两候选结构对称（机检）**\n"
    "- −3/272 = −(k − b) / [2^(k−4)(2^(k−4) + 1)]，272 = 2⁴(2⁴+1) = 16·17；\n"
    "- −11/997 = −(2k − b) / [2^(k−5)·b³ − (k − b)]，997 = 2³·5³ − 3 = 1000 − 3；\n"
    "- 两式均只由词表 {k, b, 幂基} 生成 ⇒ **无结构偏好**，四十六节的结构腿判读被机检确认。\n\n"
    "**判定**：k(2) 仍不可择一——三条腿同时不满足：数值腿（提取误差未量化，"
    "择一需误差 <1.040e-04 且候选间距 >2 倍误差）、结构腿（上式对称）、"
    "机制腿（窗内无 m⁻⁵ 项）⇒ **维持观察身份开放**（不升格、不锁定、不关闭）。\n\n"
    "**G1 前提（不改 G1）**：G1 登记 M3（生成谱假说）MA1 缺 ⇒ G2 的数值结论在 M3 映射"
    "建立前**不可证伪**；G2 不产生可用数据校验的预测。\n\n"
    "**诚实边界**：\n"
    "- **表达式 ≠ 生成机制**：词表统一是重述级登记，未给出 1/m⁵ 生成函数；\n"
    "- 指数窗只是形式复算（多项式次数），不解释「窗长 5 = k−3」的语义；\n"
    "- 两候选不删除（保留未证伪路径），本轮不新增判别证据；\n"
    "- **G2 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。\n"
)

MARK = {
    "rs": "> **351（本轮，G2-1：生成器",
    "p48": "286bn（2026-11-01，G2-1：生成器",
    "road": "P7-5e-360（G2-1：生成器",
    "dig": "七十五、G2-1：生成器",
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
    for k, v in MARK.items():
        print("MARK %s count=%d" % (k, (rs if k == 'rs' else p48 if k == 'p48' else road if k == 'road' else read_keep(DIG)).count(v)))


def apply():
    rs, p48, road, dig = (read_keep(p) for p in (RS, P48, ROAD, DIG))
    if MARK["rs"] in rs:
        print("RS 351 已存在，跳过")
    else:
        assert rs.count(A_RS) == 1, "RS anchor count=%d" % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + nl_of(rs) + SEG_RS, 1)
        RS.write_text(rs, encoding="utf-8", newline="")
        print("RS 351 写入")
    if MARK["p48"] in p48:
        print("P48 286bn 已存在，跳过")
    else:
        assert p48.count(A_P48) == 1, "P48 anchor count=%d" % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + nl_of(p48) + SEG_P48, 1)
        P48.write_text(p48, encoding="utf-8", newline="")
        print("P48 286bn 写入")
    if MARK["road"] in road:
        print("ROAD 360 已存在，跳过")
    else:
        assert road.count(A_ROAD) >= 1, "ROAD anchor count=%d" % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + "\r\n" + SEG_ROAD, 1)
        ROAD.write_text(road, encoding="utf-8", newline="")
        print("ROAD 360 写入")
    if MARK["dig"] in dig:
        print("DIGEST 七十五节 已存在，跳过")
    else:
        assert dig.endswith("\n"), "digest tail not newline"
        DIG.write_text(dig + SEG_DIG, encoding="utf-8", newline="")
        print("DIGEST 七十五节 写入")
    print("APPLY DONE（幂等）：351/286bn/P7-5e-360/七十五节")


def verify():
    rs, p48, road, dig = (read_keep(p) for p in (RS, P48, ROAD, DIG))
    ok = True
    for name, got in [("RS 351", rs.count(MARK["rs"])), ("P48 286bn", p48.count(MARK["p48"])),
                      ("ROAD 360", road.count(MARK["road"]))]:
        print("%s count=%d" % (name, got))
        ok &= got == 1
    dg = dig.count(MARK["dig"])
    print("DIGEST 七十五 count=%d" % dg)
    ok &= dg == 1
    crlf, lf_solo = road.count("\r\n"), road.count("\n") - road.count("\r\n")
    print("ROAD CRLF=%d LF-solo=%d" % (crlf, lf_solo))
    ok &= lf_solo == 0
    print("VERIFY", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    {"probe": probe, "apply": apply, "verify": verify}[mode]()
