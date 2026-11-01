# -*- coding: utf-8 -*-
"""P7-5e-359 判据：G1 映射锚定——M1–M4 书面映射登记 + MA1/MA2/MA3 逐条核验

口径（纪要六十四节）：G1 = 映射锚定 MA1–MA3；阻塞 226 的 mapping 半。
纪律：pyenv 精确分数（Fraction），无浮点断言；禁英文直引号（中文文本用「」）。
诚实边界：本判据只做「登记 + 逐条核验」，不建立锚定、不产生新判别证据、不关闭任何项。
"""
import pathlib
from fractions import Fraction as F

DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")
text = DIG.read_text(encoding="utf-8")

results = []


def chk(tag, name, cond, note=""):
    results.append((tag, name, bool(cond), note))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))


# ---------- 闭式与 2×2 估计器（与框架闭式同一口径，精确分数） ----------
def sval(m):
    return F(m, 2) + F(1, 8) + F(13, 128 * m) + F(41, 2000 * m * m) - F(39, 2000 * m ** 3)


def known(m):
    return F(m, 2) + F(1, 8) + F(13, 128 * m)


def det2(m1, m2):
    return F(1, m1 ** 2) * F(1, m2 ** 3) - F(1, m2 ** 2) * F(1, m1 ** 3)


# ---------- 映射登记表（命名对象，替代语料字符串计数） ----------
MA_OBJ = [
    dict(id="M1",
         fw="226 E 项（1/B*(m) 的 m⁻³ 系数 −39/2000）",
         obs="二维 H⁻ 两束缚态脱附临界场强 B*(1)、B*(2)",
         rel="s(m):=1/B*(m)=m/2+1/8+13/(128m)+D/m²+E/m³；由 m=1,2 两点 2×2 求 (D,E)",
         ma1=True, ma1_note="关系式书面且精确可算（反演命中 D=41/2000、E=−39/2000）",
         ma2=False, ma2_note="标度来源未登记：a_z=1 归一/有效质量/介电常数属 D5 待交付字段，无外部出处",
         ma3=False, ma3_note="锚通道 = 检验通道（同为 B*(1)、B*(2) 两点数据 ⇒ 自证）"),
    dict(id="M2",
         fw="碗形链层 2 同构量 h′(2)=13/600",
         obs="待定（Q1 四类候选全败）",
         rel="无：无量纲 h′ 与任何量纲量的关系式未建立",
         ma1=False, ma1_note="Q1 结构性缺位：物理曲率/比值 r2=15/4/谱桥/量纲桥四类候选全败",
         ma2=False, ma2_note="无量纲性构成一般性障碍：任何量纲映射需额外标度公设",
         ma3=False, ma3_note="无观测量 ⇒ 不可评"),
    dict(id="M3",
         fw="生成谱假说（k(2)=1/m⁵ 系数身份等）",
         obs="谱/参数链中的组合出现位置",
         rel="无：代数映射未建立（结构在哪些组合出现未定）",
         ma1=False, ma1_note="只有枚举链，无书面关系式",
         ma2=False, ma2_note="无关系式 ⇒ 不可评（1/m⁵ 生成函数亦未给出，属 G2）",
         ma3=False, ma3_note="不可评"),
    dict(id="M4",
         fw="闭式谱 m=11：1/B*(11)=5.6344",
         obs="S1 |M|=3 通道 1/γ*_meas=5.661±0.550",
         rel="γ=B/B₀（B₀ 由 ℏω_c=2Ry 约定）；s(m)=1/B*(m)=1/γ*(m)；通道匹配 m*=11",
         ma1=True, ma1_note="显式：同一 1/B* 量，m*=11 具名（δ=0.0011/0.0549）",
         ma2=True, ma2_note="无自由参数：闭式由 k_max=8 确定；B₀ 为外部约定（ℏω_c=2Ry，出处在册）",
         ma3=False, ma3_note="锚通道 = 检验通道：S1 同一数据既做通道匹配又做比对；无第二独立通道"),
]

# ---------- A 口径 ----------
chk("A1", "MA1–MA6 判据在册（纪要四十五节）",
    "MA1 显式性" in text and "MA2 无自由参数" in text and "MA3 锚定独立" in text
    and "MA4 可证伪" in text and "MA5 单值可逆" in text and "MA6 量纲闭合" in text,
    "六条逐条可核验，定义于 2026-11-01")

chk("A2", "G1 口径与执行序在册（六十四/六十五节）",
    "映射锚定 MA1–MA3" in text and "G3 → G4 → G1 → G2 → G5" in text,
    "G1 = 226 的 mapping 半；「先立骨」序中 G1 排第三")

chk("A3", "审计口径修正：语料「映射未建立=4」为字符串出现次数，非四项预测清单",
    text.count("映射未建立") >= 4 and len(MA_OBJ) == 4,
    "出现次数=%d（含审计元记录自身）；本轮以命名登记 M1–M4 替代字符串计数"
    % text.count("映射未建立"))

# ---------- B 登记表结构 ----------
chk("B1", "登记表恰四个命名对象 M1–M4", [o["id"] for o in MA_OBJ] == ["M1", "M2", "M3", "M4"],
    "M1 E 项本体 / M2 h′(2) / M3 生成谱假说 / M4 |M|=3 单通道对照")

chk("B2", "每对象四字段齐备（框架量/可观测量/关系式/MA1–MA3 判定）",
    all(set(o) >= {"fw", "obs", "rel", "ma1", "ma1_note", "ma2", "ma2_note", "ma3", "ma3_note"}
        for o in MA_OBJ))

chk("B3", "关系式不得含糊：M1/M4 有式，M2/M3 显式登记为「无」",
    MA_OBJ[0]["rel"].startswith("s(m)") and MA_OBJ[3]["rel"].startswith("γ=")
    and MA_OBJ[1]["rel"].startswith("无") and MA_OBJ[2]["rel"].startswith("无"),
    "不接受「可能对应」措辞（MA1 要求）")

# ---------- C 代数核 ----------
pairs = [(a, b) for a in range(1, 9) for b in range(a + 1, 9)]
chk("C1", "MA5 代数核：det=(m1−m2)/(m1³m2³)≠0（1≤m1<m2≤8 共 28 对）",
    all(det2(a, b) == F(a - b, a ** 3 * b ** 3) and det2(a, b) != 0 for a, b in pairs),
    "28/28 非退化；(1,2) det=%s" % det2(1, 2))

r1, r2, d = sval(1) - known(1), sval(2) - known(2), det2(1, 2)
E_sol = (F(1, 1 ** 2) * r2 - F(1, 2 ** 2) * r1) / d
D_sol = (r1 - F(1, 1 ** 3) * E_sol) / F(1, 1 ** 2)
chk("C2", "M1 两点反演精确命中 (D,E)=(41/2000,−39/2000)",
    (D_sol, E_sol) == (F(41, 2000), F(-39, 2000)), "D=%s E=%s" % (D_sol, E_sol))

s11 = sval(11)
ss = abs(F(5661, 1000) - F(56344, 10000)) / (F(550, 1000))
chk("C3", "M4 数值自洽：s(11) 与 5.6344 差 ≤1/10000；σ_score(四舍五入口径)=133/2750 ≤1",
    abs(s11 - F(56344, 10000)) <= F(1, 10000) and ss == F(133, 2750) and ss <= 1,
    "s(11)=%s（语料记 5.6344）σ_score=%s（≈0.0484，语料记 0.05）" % (s11, ss))

chk("C4", "γ 归一恒等在册：γ*(m)≡1/(1/B*(m))（B₀=1 归一）",
    "γ*(m)≡1/(1/B*(m))" in text and "B₀=1 归一" in text,
    "桥两端同构：1/γ* 与 1/B* 为同一量")

# ---------- D MA1–MA3 逐条核验 ----------
ma1 = [o["id"] for o in MA_OBJ if o["ma1"]]
ma2 = [o["id"] for o in MA_OBJ if o["ma2"]]
ma3 = [o["id"] for o in MA_OBJ if o["ma3"]]
chk("D1", "MA1 显式性：2/4 通过（M1、M4）", ma1 == ["M1", "M4"],
    "M2/M3 无关系式 ⇒ 缺；M1 有机检命中的 2×2 反演式，M4 有 1/B* 同一量并置")
chk("D2", "MA2 无自由参数：1/4 通过（M4）", ma2 == ["M4"],
    "M4 无量纲比值、标度由 ℏω_c=2Ry 外部约定；M1 缺 D5 出处；M2/M3 不可评")
chk("D3", "MA3 锚定独立：0/4 通过 ⇒ 全局瓶颈", ma3 == [],
    "M1/M4 均锚=检同通道；M2/M3 无通道 ⇒ 四项全缺")

all3 = [o["id"] for o in MA_OBJ if o["ma1"] and o["ma2"] and o["ma3"]]
chk("D4", "判定：0/4 三缺全过 ⇒ 未锚定（维持挂起，禁用数据）", all3 == [],
    "MA1–MA3 任缺 ⇒ 未锚定（裁决规则 B2 仍生效）")
chk("D5", "缺口精确定位：M4 仅缺 MA3（唯一接近锚定项）；M1 缺 MA2∧MA3",
    (MA_OBJ[3]["ma1"] and MA_OBJ[3]["ma2"] and not MA_OBJ[3]["ma3"])
    and (MA_OBJ[0]["ma1"] and not MA_OBJ[0]["ma2"] and not MA_OBJ[0]["ma3"]),
    "M4 最小补件 = 第二独立通道；M1 最小补件 = D5 出处 + 通道独立")

# ---------- E 依据在册（只引用已登记资产，不新增判别证据） ----------
chk("E1", "M1 依据在册：P2 两点重构协议（2×2、精度 1/2000 与 1/8000）",
    "两点重构" in text and "1/2000" in text and "1/8000" in text and "2×2" in text)
chk("E2", "M2 依据在册：Q1 结构性缺位、四类候选全败",
    "结构性缺位" in text and "四类候选" in text and "h′(2)" in text)
chk("E3", "M3 依据在册：生成谱假说代数映射未建立（G2 口径）",
    "生成谱假说" in text and "代数映射未建立" in text)
chk("E4", "M4 依据在册：S1 |M|=3 通道、5.661±0.550 vs 5.6344、B₀ 出处",
    "|M|=3" in text and "1/γ*_meas=5.661±0.550" in text
    and "1/B*(11)=5.6344" in text and "B_0=2.35" in text
    and r"\hbar\omega_c=2\mathrm{Ry}" in text)

# ---------- F 边界与判定 ----------
chk("F1", "226 维持挂起（suspended-awaiting-data）", "suspended-awaiting-data" in text,
    "挂起 ≠ 关闭 ≠ 降级")
chk("F2", "不关闭任何项：k(2) 仍开放", "k(2)" in text and "不关闭任何项" in text,
    "本轮只登记映射，不关闭 226 / k(2)")
chk("F3", "诚实边界在册：MA1–MA3 任缺 ⇒ 未锚定且禁用数据",
    "MA1–MA3 任缺" in text and "禁用数据" in text and "未锚定" in text,
    "登记 ≠ 锚定成立；本判据无 Lean 增量")

print()
passed = sum(1 for r in results if r[2])
print(f"{passed}/{len(results)} " + ("ALL_PASS" if passed == len(results) else "HAS_FAILURE"))
print("判定：M1–M4 映射已书面登记；MA1 2/4、MA2 1/4、MA3 0/4 ⇒ 4/4 未锚定，"
      "226 的 mapping 半阻塞维持，禁用数据规则不变。")
print("最小补件：M4 需第二独立通道；M1 需 D5 归一出处 + 锚/检通道分离。")
print("诚实边界：映射登记 ≠ 锚定成立；不关闭任何项（226 挂起、k(2) 开放）。")
