# -*- coding: utf-8 -*-
"""P7-5e-359 落盘：RS 350 / paper48 286bm / roadmap P7-5e-359 / 纪要 七十四节

内容：G1-1——审计口径修正（「映射未建立」计数=4 为字符串出现次数，非四项清单）
+ M1–M4 书面映射登记 + MA1/MA2/MA3 逐条核验（MA1 2/4、MA2 1/4、MA3 0/4
⇒ 4/4 未锚定）。G1 未闭合；不关闭任何项。
幂等 + 锚点 count==1 + ROAD CRLF 纪律（read_keep / newline=''）。
"""
import sys
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
P48 = ROOT / "paper" / "paper48_topological_forbidden_frequency.md"
ROAD = ROOT / "roadmap" / "phase102_baryon_lepton_parameter_free.md"
DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")

A_RS = "本轮 Lean 增量：G4-1 时空维数两公设结构层（SpacetimeDimensionTwoPostulates）；G4 未闭合。"
A_P48 = "**G4 未闭合**（结构骨架 ≠ 公设导出）。不关闭任何项。"
A_ROAD = "G4 未闭合（结构骨架 ≠ 公设导出），不关闭任何项。"

SEG_RS = (
    "> **350（本轮，G1-1：映射锚定——M1–M4 书面映射登记与 MA1/MA2/MA3 逐条核验，2026-11-01）**：接 349。"
    "G1 口径（纪要六十四节）＝映射锚定 MA1–MA3，阻塞 226 的 mapping 半。"
    "本轮不新建定义层、无 Lean 增量，只做两件事："
    "①**审计口径修正**——语料「映射未建立」计数=4 为字符串出现次数（含审计元记录自身），"
    "非四项预测清单；改为**命名登记** M1–M4；"
    "②**逐条核验 MA1–MA3**。"
    "登记表：M1 = 226 E 项（1/B*(m) 的 m⁻³ 系数 −39/2000）↔ 两束缚态脱附临界场 B*(1)、B*(2)，"
    "关系式 s(m):=1/B*(m)=m/2+1/8+13/(128m)+D/m²+E/m³，两点 2×2 反演精确命中 (D,E)=(41/2000,−39/2000)；"
    "M2 = h′(2)=13/600 ↔ 待定（Q1 结构性缺位，四类候选全败）；"
    "M3 = 生成谱假说（k(2)=1/m⁵ 等）↔ 谱/参数链组合出现位置（代数映射未建立）；"
    "M4 = 闭式谱 m=11 的 1/B*(11)=5.6344 ↔ S1 |M|=3 通道 1/γ*_meas=5.661±0.550（通道匹配 m*=11）。"
    "核验结果：**MA1 2/4**（M1、M4，关系式书面且精确可算）；"
    "**MA2 1/4**（M4，无量纲比值且标度由 ℏω_c=2Ry 外部约定｜M1 缺 D5 归一出处）；"
    "**MA3 0/4**（M1/M4 锚通道 = 检验通道；M2/M3 无通道）⇒ **4/4 未锚定**，"
    "「MA1–MA3 任缺 ⇒ 禁用数据」规则不变。判据脚本 `scripts/p7_5e286r_g1_mapping_anchoring_criteria.py` "
    "A1–F3，**22/22 ALL_PASS**（含 MA5 代数核 det 28/28 非退化与 s(11) 精确复算）。"
    "**最小补件**：M4 需第二独立通道（唯一 MA1∧MA2 过的接近锚定项）；"
    "M1 需 D5 归一出处 + 锚/检通道分离。"
    "**诚实边界**：映射登记 ≠ 锚定成立；0/4 三缺全过；只登记与核验，不产生新判别证据；**G1 未闭合**。"
    "不关闭任何项（226 仍挂起、k(2) 仍开放）。"
    "本轮无 Lean 增量（映射登记与 MA1–MA3 逐条核验）。"
)

SEG_P48 = (
    "286bm（2026-11-01，G1-1：映射锚定——M1–M4 书面映射登记与 MA1/MA2/MA3 逐条核验）**："
    "G1 口径 = 映射锚定 MA1–MA3（226 的 mapping 半）。先做审计口径修正："
    "语料「映射未建立」计数=4 为字符串出现次数（含审计元记录自身），非四项预测清单；"
    "本轮改为命名登记 M1–M4，再逐条核验。"
    "M1 = 226 E 项（m⁻³ 系数 −39/2000）↔ 两束缚态脱附临界场 B*(1)、B*(2)，"
    "s(m):=1/B*(m)=m/2+1/8+13/(128m)+D/m²+E/m³，2×2 反演精确命中 (D,E)=(41/2000,−39/2000)；"
    "M2 = h′(2)=13/600 ↔ 待定（Q1 结构性缺位，四类候选全败）；"
    "M3 = 生成谱假说（k(2)=1/m⁵）↔ 组合出现位置（代数映射未建立）；"
    "M4 = 1/B*(11)=5.6344 ↔ S1 |M|=3 通道 1/γ*_meas=5.661±0.550（m*=11）。"
    "核验：MA1 2/4（M1、M4）、MA2 1/4（M4）、MA3 0/4 ⇒ 4/4 未锚定，禁用数据规则不变。"
    "判据 22/22 ALL_PASS。最小补件：M4 第二独立通道；M1 D5 归一出处 + 锚/检分离。"
    "诚实边界：**G1 未闭合**（映射登记 ≠ 锚定成立）。不关闭任何项。"
)

SEG_ROAD = (
    "P7-5e-359（G1-1：映射锚定——M1–M4 书面映射登记与 MA1/MA2/MA3 逐条核验，2026-11-01）**：接 358。"
    "G1 口径 = 映射锚定 MA1–MA3（226 的 mapping 半）。审计口径修正："
    "「映射未建立」计数=4 为字符串出现次数（含审计元记录自身），非四项预测清单 ⇒ 改命名登记 M1–M4。"
    "M1 = 226 E 项（m⁻³ 系数 −39/2000）↔ B*(1)、B*(2)，"
    "s(m):=1/B*(m)=m/2+1/8+13/(128m)+D/m²+E/m³，2×2 反演命中 (D,E)=(41/2000,−39/2000)；"
    "M2 = h′(2)=13/600 ↔ 待定（Q1 结构性缺位）；"
    "M3 = 生成谱假说（k(2)=1/m⁵）↔ 组合出现位置（代数映射未建立）；"
    "M4 = 1/B*(11)=5.6344 ↔ S1 |M|=3 通道 1/γ*_meas=5.661±0.550（m*=11）。"
    "MA1 2/4（M1、M4）、MA2 1/4（M4）、MA3 0/4 ⇒ 4/4 未锚定，禁用数据规则不变；判据 A1–F3 22/22 ALL_PASS。"
    "最小补件：M4 第二独立通道（唯一 MA1∧MA2 过项）；M1 D5 归一出处 + 锚/检通道分离。"
    "G1 未闭合（映射登记 ≠ 锚定成立），不关闭任何项（226 挂起、k(2) 开放）。"
)

SEG_DIG = (
    "\n## 七十四、G1-1：映射锚定——M1–M4 书面映射登记与 MA1/MA2/MA3 逐条核验（2026-11-01）\n\n"
    "**口径（六十四节表）**：G1 = 映射锚定 MA1–MA3；阻塞 226 的 mapping 半。"
    "本轮不新建定义层、无 Lean 增量，只做登记与逐条核验。\n\n"
    "**审计口径修正**：语料「映射未建立」计数=4 是**字符串出现次数**"
    "（其中两条为审计元记录自身），不是四项预测清单 ⇒ 单以计数作审计单元会把"
    "「元记录」误当「预测」。改为**命名登记** M1–M4，每个对象给出框架量、可观测量、关系式与逐条判定。\n\n"
    "**映射登记表（MA1/MA2/MA3 逐条）**\n\n"
    "| # | 框架量 ↔ 可观测量 | 关系式 | MA1 | MA2 | MA3 |\n|---|---|---|---|---|---|\n"
    "| M1 | 226 E 项（m⁻³ 系数 −39/2000）↔ B*(1)、B*(2) | "
    "s(m):=1/B*(m)=m/2+1/8+13/(128m)+D/m²+E/m³；两点 2×2 反演 | ✓ | ✗ | ✗ |\n"
    "| M2 | h′(2)=13/600 ↔ 待定 | 无（Q1 结构性缺位，四类候选全败） | ✗ | ✗ | 不可评 |\n"
    "| M3 | 生成谱假说（k(2)=1/m⁵）↔ 组合出现位置 | 无（代数映射未建立） | ✗ | 不可评 | 不可评 |\n"
    "| M4 | 1/B*(11)=5.6344 ↔ S1 \|M\|=3 通道 | "
    "γ=B/B₀（ℏω_c=2Ry 约定）；s=1/B*=1/γ*；通道 m*=11 | ✓ | ✓ | ✗ |\n\n"
    "**缺项理由**：M1 MA2 缺 D5 归一出处（a_z=1/有效质量/介电常数无外部出处在册）；"
    "M1 MA3 缺（锚与检验同为 B*(1)、B*(2) 同一两点 ⇒ 自证）；"
    "M4 MA3 缺（S1 同一数据既做通道匹配又做比对，无第二独立通道）。\n\n"
    "**核验结果**：MA1 **2/4**（M1、M4）、MA2 **1/4**（M4）、MA3 **0/4** ⇒ "
    "**4/4 未锚定**（无任一对象三缺全过），「MA1–MA3 任缺 ⇒ 禁用数据」规则不变。"
    "判据脚本 `scripts/p7_5e286r_g1_mapping_anchoring_criteria.py`（A1–F3）**22/22 ALL_PASS**："
    "C1 MA5 代数核 det=(m1−m2)/(m1³m2³)≠0（28/28）；C2 两点反演精确命中 "
    "(D,E)=(41/2000,−39/2000)；C3 s(11) 精确复算 119989921/21296000 与 5.6344 差 ≤1/10000、"
    "σ_score=133/2750 ≤1；C4 γ 归一恒等在册。\n\n"
    "**最小补件（按对象）**\n"
    "- **M4**：仅缺 MA3 —— 是唯一 MA1∧MA2 已过的**接近锚定项**，补第二独立通道即可重核；\n"
    "- **M1**：缺 MA2∧MA3 —— 需 D5 归一出处 + 锚/检通道分离；\n"
    "- **M2/M3**：MA1 缺 —— 属映射建立工程（M3 与 G2 同源），不属本轮。\n\n"
    "**诚实边界**：\n"
    "- **映射登记 ≠ 锚定成立**：本段只把「映射未建立」的计数式登记换成命名式登记并逐条判定；\n"
    "- 0/4 三缺全过；未产生任何新判别证据，未新增观测量或误差预算（MA4 不在本轮）；\n"
    "- M4 的 MA2 过项依据是「无量纲比值 + ℏω_c=2Ry 外部约定」，"
    "不构成对 S1 数据的独立性认证；\n"
    "- **G1 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。\n"
)

MARK = {
    "rs": "> **350（本轮，G1-1：映射锚定",
    "p48": "286bm（2026-11-01，G1-1：映射锚定",
    "road": "P7-5e-359（G1-1：映射锚定",
    "dig": "七十四、G1-1：映射锚定",
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
        print("RS 350 已存在，跳过")
    else:
        assert rs.count(A_RS) == 1, "RS anchor count=%d" % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + nl_of(rs) + SEG_RS, 1)
        RS.write_text(rs, encoding="utf-8", newline="")
        print("RS 350 写入")
    if MARK["p48"] in p48:
        print("P48 286bm 已存在，跳过")
    else:
        assert p48.count(A_P48) == 1, "P48 anchor count=%d" % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + nl_of(p48) + SEG_P48, 1)
        P48.write_text(p48, encoding="utf-8", newline="")
        print("P48 286bm 写入")
    if MARK["road"] in road:
        print("ROAD 359 已存在，跳过")
    else:
        assert road.count(A_ROAD) >= 1, "ROAD anchor count=%d" % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + "\r\n" + SEG_ROAD, 1)
        ROAD.write_text(road, encoding="utf-8", newline="")
        print("ROAD 359 写入")
    if MARK["dig"] in dig:
        print("DIGEST 七十四节 已存在，跳过")
    else:
        assert dig.endswith("\n"), "digest tail not newline"
        DIG.write_text(dig + SEG_DIG, encoding="utf-8", newline="")
        print("DIGEST 七十四节 写入")
    print("APPLY DONE（幂等）：350/286bm/P7-5e-359/七十四节")


def verify():
    rs, p48, road, dig = (read_keep(p) for p in (RS, P48, ROAD, DIG))
    ok = True
    for name, got in [("RS 350", rs.count(MARK["rs"])), ("P48 286bm", p48.count(MARK["p48"])),
                      ("ROAD 359", road.count(MARK["road"]))]:
        print("%s count=%d" % (name, got))
        ok &= got == 1
    dg = dig.count(MARK["dig"])
    print("DIGEST 七十四 count=%d" % dg)
    ok &= dg == 1
    crlf, lf_solo = road.count("\r\n"), road.count("\n") - road.count("\r\n")
    print("ROAD CRLF=%d LF-solo=%d" % (crlf, lf_solo))
    ok &= lf_solo == 0
    print("VERIFY", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    {"probe": probe, "apply": apply, "verify": verify}[mode]()
